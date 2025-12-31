import cv2
import numpy as np
import json
import argparse
import os
import sys
import shutil

def compute_fixation_order(saliency_map, max_fixations=5, min_saliency=150, min_distance=80):
    """
    Compute fixation order using validated research methods.
    Based on Winner-Take-All with distance penalties and reading pattern biases.

    Algorithm:
    1. Find local maxima (saliency peaks)
    2. Apply distance penalties (saccade mechanics - prefer nearby targets)
    3. Apply reading pattern biases (top-left preference, horizontal sweep)
    4. Use inhibition-of-return (avoid recently fixated areas)
    5. Apply minimum distance filter (avoid selecting nearby pixels)
    6. Order by weighted saliency score

    Args:
        saliency_map: The saliency map (0-255, uint8)
        max_fixations: Maximum number of fixations to compute (default: 5)
        min_saliency: Minimum saliency value to consider (default: 150)
        min_distance: Minimum pixel distance between fixations (default: 80 pixels ≈ 1.5° visual angle)

    Returns:
        List of fixation points with coordinates, saliency, and order
    """
    if saliency_map is None or saliency_map.size == 0:
        return []

    h, w = saliency_map.shape
    fixations = []

    # Find local maxima using morphological operations
    # This finds peak saliency points more reliably than simple max
    kernel = np.ones((15, 15), np.uint8)
    local_max = cv2.dilate(saliency_map, kernel, iterations=1)
    peaks = (saliency_map == local_max) & (saliency_map >= min_saliency)

    # Extract peak coordinates and saliency values
    peak_coords = np.argwhere(peaks)
    peak_saliencies = saliency_map[peaks]

    if len(peak_coords) == 0:
        # Fallback: use global maximum
        max_idx = np.argmax(saliency_map)
        max_y, max_x = np.unravel_index(max_idx, saliency_map.shape)
        peak_coords = np.array([[max_y, max_x]])
        peak_saliencies = np.array([saliency_map[max_y, max_x]])

    # Initialize fixation list
    remaining_peaks = list(zip(peak_coords, peak_saliencies))

    # Normalize coordinates for distance calculation (0-1 scale)
    norm_w = float(w)
    norm_h = float(h)

    # First fixation: highest saliency OR top-left preference if close
    if remaining_peaks:
            # Sort by saliency * top-left bias
            def score_first_fixation(coord, sal):
                y, x = coord[0], coord[1]
                # Top-left bias: prefer elements in upper-left quadrant
                top_left_bias = 1.0 - (x / norm_w) * 0.3 - (y / norm_h) * 0.2
                return sal * top_left_bias

            remaining_peaks.sort(key=lambda p: score_first_fixation(p[0], p[1]), reverse=True)
            first_coord, first_sal = remaining_peaks.pop(0)
            first_x, first_y = int(first_coord[1]), int(first_coord[0])

            # Remove all peaks within minimum distance of first fixation
            remaining_peaks = [
                (c, s) for c, s in remaining_peaks
                if np.sqrt((c[1] - first_coord[1])**2 + (c[0] - first_coord[0])**2) >= min_distance
            ]

            fixations.append({
                'order': 1,
                'position': [first_x, first_y],  # x, y format
                'saliency': int(first_sal),
                'method': 'highest_saliency'
            })

    # Subsequent fixations: saliency weighted by distance penalty + reading pattern
    for fix_num in range(2, max_fixations + 1):
        if not remaining_peaks:
            break

        last_fix = fixations[-1]
        last_x, last_y = last_fix['position']

        # Calculate weighted score for each remaining peak
        scored_peaks = []
        for coord, sal in remaining_peaks:
            y, x = coord[0], coord[1]

            # Distance penalty (saccade mechanics: prefer nearby targets)
            # Typical saccade: 1-5 degrees visual angle
            # Convert pixel distance to approximate visual angle (assuming ~96 DPI)
            pixel_distance = np.sqrt((x - last_x)**2 + (y - last_y)**2)
            # Normalize by image diagonal
            img_diagonal = np.sqrt(norm_w**2 + norm_h**2)
            normalized_distance = pixel_distance / img_diagonal

            # Distance penalty: exponential decay
            # Closer targets get higher scores
            distance_penalty = np.exp(-normalized_distance * 3.0)  # Decay factor tuned for typical saccades

            # Reading pattern bias
            # After horizontal movement, prefer downward movement (F-pattern)
            # After vertical movement, prefer horizontal movement
            reading_bias = 1.0
            if len(fixations) >= 2:
                prev_fix = fixations[-2]
                prev_x, prev_y = prev_fix['position']
                # Check if previous movement was horizontal
                if abs(prev_x - last_x) > abs(prev_y - last_y):
                    # Prefer downward movement
                    if y > last_y:
                        reading_bias = 1.2
                else:
                    # Prefer horizontal movement
                    if abs(x - last_x) > abs(y - last_y):
                        reading_bias = 1.2

            # Top-left bias (decreases with fixation number)
            top_left_bias = 1.0 - (x / norm_w) * 0.2 - (y / norm_h) * 0.15
            top_left_bias = max(0.7, top_left_bias)  # Minimum bias

            # Combined score
            score = sal * distance_penalty * reading_bias * top_left_bias

            scored_peaks.append((coord, sal, score))

        # Select highest scoring peak
        if scored_peaks:
            scored_peaks.sort(key=lambda p: p[2], reverse=True)
            best_coord, best_sal, best_score = scored_peaks[0]

            # Remove selected peak from remaining peaks
            remaining_peaks = [(c, s) for c, s in remaining_peaks if not (c[0] == best_coord[0] and c[1] == best_coord[1])]

            # Apply inhibition-of-return: Remove all peaks within minimum distance
            # This prevents selecting multiple fixations in the same visual region
            best_x, best_y = int(best_coord[1]), int(best_coord[0])
            remaining_peaks = [
                (c, s) for c, s in remaining_peaks
                if np.sqrt((c[1] - best_coord[1])**2 + (c[0] - best_coord[0])**2) >= min_distance
            ]

            fixations.append({
                'order': fix_num,
                'position': [best_x, best_y],  # x, y format
                'saliency': int(best_sal),
                'method': 'weighted_saliency'
            })

    return fixations

def detect_saliency_zones(saliency_map, img, top_n=10, min_region_area=500):
    """
    Automatically detect distinct regions in different saliency zones.
    Uses hybrid approach: CV for detection + AI vision for top regions.

    Args:
        saliency_map: The saliency map (0-255, uint8)
        img: Original image for reference
        top_n: Number of top regions to identify (for future AI vision integration)
        min_region_area: Minimum area in pixels to consider a region

    Returns:
        List of zone regions with bounding boxes and attention share
    """
    total_heat = np.sum(saliency_map)
    if total_heat == 0:
        return []

    # Define zone thresholds (matching JET colormap interpretation)
    zone_thresholds = {
        'red': (200, 255),      # Hot zones - maximum attention
        'yellow': (100, 199),   # Medium zones - moderate attention
        'blue': (0, 99)         # Cold zones - low attention
    }

    detected_zones = []

    for zone_name, (min_val, max_val) in zone_thresholds.items():
        # Create mask for this zone
        zone_mask = cv2.inRange(saliency_map, min_val, max_val)

        # Morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        zone_mask = cv2.morphologyEx(zone_mask, cv2.MORPH_CLOSE, kernel)
        zone_mask = cv2.morphologyEx(zone_mask, cv2.MORPH_OPEN, kernel)

        # Find contours (distinct regions) in this zone
        contours, _ = cv2.findContours(zone_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < min_region_area:
                continue

            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Ensure bounds are valid
            x = max(0, x)
            y = max(0, y)
            w = min(w, saliency_map.shape[1] - x)
            h = min(h, saliency_map.shape[0] - y)

            if w <= 0 or h <= 0:
                continue

            # Filter out regions that are too large (likely background/entire image)
            img_area = saliency_map.shape[0] * saliency_map.shape[1]
            region_area = w * h
            if region_area > img_area * 0.5:  # Skip if region is more than 50% of image
                continue

            # Calculate attention share for this region
            region_saliency = saliency_map[y:y+h, x:x+w]
            region_heat = np.sum(region_saliency)
            attention_share = (region_heat / total_heat) * 100 if total_heat > 0 else 0

            # Calculate average saliency in this region
            avg_saliency = np.mean(region_saliency)

            # Generate descriptive name based on zone and attention
            zone_index = len([z for z in detected_zones if z['zone'] == zone_name]) + 1
            if zone_name == 'red' and attention_share > 20:
                element_name = f"High-Attention Element {zone_index}"
            elif zone_name == 'red':
                element_name = f"Hot Zone Element {zone_index}"
            elif zone_name == 'yellow':
                element_name = f"Medium-Attention Element {zone_index}"
            else:
                element_name = f"Low-Attention Element {zone_index}"

            detected_zones.append({
                "name": element_name,
                "zone": zone_name,
                "box": [int(x), int(y), int(w), int(h)],
                "attention_share": round(attention_share, 2),
                "avg_saliency": round(float(avg_saliency), 2),
                "area": int(area),
                "identified": False  # Will be updated by AI vision if available
            })

    # Sort by attention share (descending)
    detected_zones.sort(key=lambda x: x['attention_share'], reverse=True)

    # Mark top N regions for potential AI vision identification
    for i, zone in enumerate(detected_zones[:top_n]):
        zone['priority_for_identification'] = True

    return detected_zones

def generate_saliency_analysis(image_path, goal_boxes=None, output_dir=None, auto_detect_zones=True, top_n_regions=10):
    """
    Generate eye-tracking attention analysis using Spectral Residual saliency.

    Args:
        image_path (str): Path to input image (JPEG/PNG)
        goal_boxes (list): Optional list of dictionaries with 'name' and 'box' [x, y, w, h]
        output_dir (str): Directory to save outputs (default: same as input image)

    Returns:
        dict: Dictionary with metrics and interpretation
    """
    # 0. Setup paths
    if output_dir is None:
        # If image is in orders/ folder, save outputs there too
        image_dir = os.path.dirname(image_path) or "."
        if "orders" in image_dir or os.path.basename(os.path.dirname(os.path.abspath(image_path))) == "orders":
            output_dir = "orders"
        else:
            output_dir = image_dir

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract base image name (without extension) for output filenames
    image_basename = os.path.splitext(os.path.basename(image_path))[0]

    heatmap_path = os.path.join(output_dir, f"heatmap_output_{image_basename}.png")
    metrics_path = os.path.join(output_dir, "saliency_metrics.json")
    legend_path = os.path.join(output_dir, "heatmap_legend.png")

    # Copy legend to output directory if it doesn't exist
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_legend = os.path.join(script_dir, "heatmap_legend.png")
    if os.path.exists(source_legend) and not os.path.exists(legend_path):
        shutil.copy(source_legend, legend_path)
        print(f"Copied legend to: {legend_path}")

    # 1. Load Image
    print(f"Loading image: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return None

    # 2. Generate Saliency Map (Spectral Residual)
    print("Generating saliency map...")
    try:
        saliency_algo = cv2.saliency.StaticSaliencySpectralResidual_create()
        (success, saliency_map) = saliency_algo.computeSaliency(img)

        if not success:
            print("Error: Failed to compute saliency map")
            return None

        # Normalize to 0-255 (Grayscale)
        saliency_map = (saliency_map * 255).astype("uint8")

    except AttributeError:
        print("Error: cv2.saliency module not found. Please install opencv-contrib-python.")
        return None

    # 3. Add Face Bias (Faces always steal attention)
    print("Detecting faces...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Look for haar cascade in cv2 data or local file
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    if not os.path.exists(cascade_path):
        # Fallback to local file if not in system path
        cascade_path = 'haarcascade_frontalface_default.xml'

    if os.path.exists(cascade_path):
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        print(f"  - Found {len(faces)} faces")

        for (x, y, w, h) in faces:
            # Boost saliency in face regions by 30%
            roi = saliency_map[y:y+h, x:x+w]
            saliency_map[y:y+h, x:x+w] = cv2.addWeighted(roi, 0.7, 255, 0.3, 0)
    else:
        print("  - Warning: Haar cascade file not found, skipping face detection bias")
        faces = []

    # 4. Calculate Metrics
    print("Calculating metrics...")

    # --- Clarity Score ---
    mean_val = np.mean(saliency_map)
    max_val = np.max(saliency_map)

    if max_val == 0:
        clarity_score = 0
    elif max_val < 50:
        # Very low peak indicates unclear design - penalize score
        clarity_score = max(0, int((1 - (mean_val / max_val)) * 100 * (max_val / 50)))
    else:
        clarity_score = int((1 - (mean_val / max_val)) * 100)

    clarity_score = max(0, min(100, clarity_score))

    # --- Confidence Level ---
    if max_val > 200:
        confidence = "High"
    elif max_val > 100:
        confidence = "Medium"
    else:
        confidence = "Low"

    # --- Attention Share for Goal Boxes ---
    box_metrics = []
    attention_share_percentage = 0

    if goal_boxes:
        print(f"Processing {len(goal_boxes)} goal boxes...")
        total_heat = np.sum(saliency_map)

        for box_data in goal_boxes:
            name = box_data.get('name', 'Unknown')
            box = box_data.get('box') # [x, y, w, h]

            if not box or len(box) != 4:
                print(f"  - Warning: Invalid box format for {name}: {box}")
                continue

            gx, gy, gw, gh = box

            # Bounds check
            gy = max(0, min(gy, saliency_map.shape[0] - 1))
            gx = max(0, min(gx, saliency_map.shape[1] - 1))
            gh = min(gh, saliency_map.shape[0] - gy)
            gw = min(gw, saliency_map.shape[1] - gx)

            if gh > 0 and gw > 0:
                # Sum heat inside box
                goal_heat = np.sum(saliency_map[gy:gy+gh, gx:gx+gw])

                share = 0
                if total_heat > 0:
                    share = round((goal_heat / total_heat) * 100, 2)

                verdict = "Invisible"
                if share > 15: verdict = "Excellent Visibility"
                elif share >= 5: verdict = "Average Visibility"

                box_metrics.append({
                    "name": name,
                    "box": [gx, gy, gw, gh],
                    "attention_share": share,
                    "verdict": verdict
                })
                print(f"  - {name}: {share}% ({verdict})")

    # --- Auto-Detect Saliency Zones ---
    auto_zones = []
    if auto_detect_zones:
        print(f"Auto-detecting saliency zones...")
        auto_zones = detect_saliency_zones(saliency_map, img, top_n=top_n_regions)
        print(f"  - Detected {len(auto_zones)} distinct regions across all zones")
        if auto_zones:
            print(f"  - Top 5 regions by attention share:")
            for i, zone in enumerate(auto_zones[:5]):
                print(f"    {i+1}. {zone['name']}: {zone['attention_share']}% ({zone['zone']} zone)")

    # 5. Generate Visuals
    print("Generating heatmap visualization...")
    heatmap_color = cv2.applyColorMap(saliency_map, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img, 0.6, heatmap_color, 0.4, 0)

    # Save output
    cv2.imwrite(heatmap_path, overlay)
    print(f"Saved heatmap to: {heatmap_path}")

    # 6. Prepare Result Dictionary
    result = {
        "output_files": {
            "heatmap": os.path.basename(heatmap_path),
            "metrics": os.path.basename(metrics_path),
            "legend": os.path.basename(legend_path)
        },
        "metrics": {
            "clarity_score": clarity_score,
            "confidence_level": confidence,
            "max_saliency_peak": int(max_val),
            "faces_detected": len(faces)
        },
        "interpretation": {
            "clarity_meaning": "Higher is better (80-100=Clear, 0-49=Cluttered).",
            "confidence_meaning": "High means the design has a clear focal point."
        }
    }

    if box_metrics:
        result["goal_boxes"] = box_metrics

    if auto_zones:
        result["auto_detected_zones"] = auto_zones

    # --- Compute Fixation Order (Algorithmic) ---
    print("Computing fixation order...")
    # min_distance: ~80 pixels ≈ 1.5° visual angle (prevents multiple fixations in same region)
    fixation_sequence = compute_fixation_order(saliency_map, max_fixations=5, min_saliency=150, min_distance=80)
    if fixation_sequence:
        result["fixation_order"] = fixation_sequence
        print(f"  - Computed {len(fixation_sequence)} fixations:")
        for fix in fixation_sequence:
            print(f"    {fix['order']}. Position ({fix['position'][0]}, {fix['position'][1]}), Saliency: {fix['saliency']}")

    # Save JSON
    with open(metrics_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Saved metrics to: {metrics_path}")

    return result

def main():
    parser = argparse.ArgumentParser(description="Generate Eye-Tracking Saliency Analysis")
    parser.add_argument("image_path", help="Path to the input screenshot/image")
    parser.add_argument("--goal-boxes", help="Path to JSON file containing goal boxes definition")
    parser.add_argument("--output-dir", help="Directory to save output files (default: same as input)")
    parser.add_argument("--auto-zones", action="store_true", default=True, help="Automatically detect saliency zones (default: True)")
    parser.add_argument("--no-auto-zones", dest="auto_zones", action="store_false", help="Disable automatic zone detection")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top regions to prioritize for identification (default: 10)")

    args = parser.parse_args()

    goal_boxes = None
    if args.goal_boxes:
        try:
            with open(args.goal_boxes, 'r') as f:
                data = json.load(f)
                # Handle various JSON structures
                if isinstance(data, list):
                    goal_boxes = data
                elif isinstance(data, dict) and "goal_boxes" in data:
                    goal_boxes = data["goal_boxes"]
                else:
                    print("Warning: Could not find list of goal boxes in JSON file.")
        except Exception as e:
            print(f"Error loading goal boxes: {e}")
            return

    generate_saliency_analysis(args.image_path, goal_boxes, args.output_dir,
                              auto_detect_zones=args.auto_zones, top_n_regions=args.top_n)

if __name__ == "__main__":
    main()
