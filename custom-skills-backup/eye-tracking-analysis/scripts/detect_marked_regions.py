"""
Helper script to detect marked regions in an annotated image.

This script uses OpenCV to detect drawn shapes (circles, rectangles, contours)
that indicate regions of interest. It extracts bounding box coordinates and
generates a goal_boxes.json file for use with generate_saliency_analysis.py.

Usage:
    python detect_marked_regions.py marked_image.png original_image.png [output.json]

The script will:
1. Compare the marked image to the original to detect annotations
2. Extract bounding boxes for detected regions
3. Generate goal_boxes.json with coordinates
"""

import cv2
import numpy as np
import json
import sys
import argparse
import os

def detect_drawn_regions(marked_image_path, original_image_path=None, output_path="goal_boxes.json"):
    """
    Detect drawn regions (circles, boxes, highlights) in a marked image.

    Args:
        marked_image_path (str): Path to image with drawn annotations
        original_image_path (str, optional): Path to original unmarked image for comparison
        output_path (str): Path to save goal_boxes.json (default: goal_boxes.json)

    Returns:
        list: List of dictionaries with 'name' and 'box' [x, y, w, h]
    """
    # Load marked image
    marked_img = cv2.imread(marked_image_path)
    if marked_img is None:
        print(f"Error: Could not load marked image from {marked_image_path}")
        return None

    print(f"Analyzing marked image: {marked_image_path}")

    # Convert to grayscale for processing
    marked_gray = cv2.cvtColor(marked_img, cv2.COLOR_BGR2GRAY)

    # If original image provided, use difference to isolate annotations
    if original_image_path and os.path.exists(original_image_path):
        original_img = cv2.imread(original_image_path)
        if original_img is not None:
            # Resize original to match marked image if needed
            if original_img.shape[:2] != marked_img.shape[:2]:
                original_img = cv2.resize(original_img, (marked_img.shape[1], marked_img.shape[0]))

            original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

            # Calculate difference to find annotations
            diff = cv2.absdiff(marked_gray, original_gray)
            # Threshold to get significant differences (annotations)
            _, diff_binary = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

            print("Using difference method with original image")
            working_img = diff_binary
        else:
            print("Warning: Could not load original image, using marked image directly")
            working_img = marked_gray
    else:
        # No original image - try to detect bright/high-contrast annotations
        print("No original image provided - detecting high-contrast annotations")

        # Convert to HSV to detect bright colors (common for annotations)
        marked_hsv = cv2.cvtColor(marked_img, cv2.COLOR_BGR2HSV)

        # Create masks for common annotation colors (red, blue, yellow, green)
        # Red annotations (0-10 and 170-180 hue)
        red_mask1 = cv2.inRange(marked_hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
        red_mask2 = cv2.inRange(marked_hsv, np.array([170, 100, 100]), np.array([180, 255, 255]))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        # Blue annotations
        blue_mask = cv2.inRange(marked_hsv, np.array([100, 100, 100]), np.array([130, 255, 255]))

        # Yellow annotations
        yellow_mask = cv2.inRange(marked_hsv, np.array([20, 100, 100]), np.array([30, 255, 255]))

        # Green annotations
        green_mask = cv2.inRange(marked_hsv, np.array([40, 100, 100]), np.array([80, 255, 255]))

        # Combine all annotation masks
        annotation_mask = cv2.bitwise_or(red_mask, cv2.bitwise_or(blue_mask, cv2.bitwise_or(yellow_mask, green_mask)))

        # Also look for high contrast edges that might be drawn lines
        edges = cv2.Canny(marked_gray, 50, 150)

        # Combine annotation colors with edges
        working_img = cv2.bitwise_or(annotation_mask, edges)

    # Detect contours (shapes)
    contours, _ = cv2.findContours(working_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and extract bounding boxes
    goal_boxes = []
    min_area = 500  # Minimum area to consider (filter out noise)
    max_boxes = 20  # Maximum number of regions to detect

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        # Filter by area
        if area < min_area:
            continue

        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)

        # Filter out boxes that are too large (likely false positives)
        img_area = marked_img.shape[0] * marked_img.shape[1]
        if (w * h) > img_area * 0.5:  # Skip if box is more than 50% of image
            continue

        # Add padding to ensure full coverage
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(marked_img.shape[1] - x, w + 2 * padding)
        h = min(marked_img.shape[0] - y, h + 2 * padding)

        # Name the region
        region_name = f"Region {len(goal_boxes) + 1}"

        goal_boxes.append({
            "name": region_name,
            "box": [int(x), int(y), int(w), int(h)]
        })

        print(f"  - Detected {region_name}: [{x}, {y}, {w}, {h}] (area: {area:.0f})")

        if len(goal_boxes) >= max_boxes:
            print(f"  - Stopping at {max_boxes} regions (limit reached)")
            break

    if len(goal_boxes) == 0:
        print("Warning: No regions detected. Try:")
        print("  - Using brighter/more contrasting colors for annotations")
        print("  - Ensuring annotations are clearly visible")
        print("  - Providing the original unmarked image for comparison")
        return None

    print(f"\nDetected {len(goal_boxes)} regions")

    # Save to JSON
    output_data = {
        "goal_boxes": goal_boxes,
        "source_image": os.path.basename(marked_image_path),
        "detection_method": "opencv_contour_detection"
    }

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Saved goal boxes to: {output_path}")

    return goal_boxes

def main():
    parser = argparse.ArgumentParser(
        description="Detect marked regions in an annotated image and generate goal_boxes.json"
    )
    parser.add_argument("marked_image", help="Path to marked/annotated image")
    parser.add_argument("--original", help="Path to original unmarked image (optional, improves detection)")
    parser.add_argument("--output", "-o", default="goal_boxes.json", help="Output JSON file path (default: goal_boxes.json)")

    args = parser.parse_args()

    if not os.path.exists(args.marked_image):
        print(f"Error: Marked image not found: {args.marked_image}")
        sys.exit(1)

    goal_boxes = detect_drawn_regions(args.marked_image, args.original, args.output)

    if goal_boxes:
        print(f"\nSuccess! Generated {len(goal_boxes)} goal boxes.")
        print(f"Now run:")
        print(f"  python generate_saliency_analysis.py [original_image] --goal-boxes {args.output}")
    else:
        print("\nFailed to detect regions. Check image and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
