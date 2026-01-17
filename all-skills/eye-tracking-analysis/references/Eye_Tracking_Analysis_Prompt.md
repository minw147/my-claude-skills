# AI-Powered Eye-Tracking Analysis Prompt v3.4
*AI-powered prediction of visual attention patterns using Spectral Residual Saliency methodology*

**NEW in v3.4:** Support for multiple images (up to 3) with combined report generation and overall recommendations section. PDF conversion included.

**NEW in v3.3:** Attention share percentages are now included directly in Section 2 (HEATMAP ANALYSIS) for each element mentioned, providing immediate quantitative metrics alongside visual descriptions.

**NEW in v3.2:** Automatic zone detection - the system now automatically detects and analyzes attention share for all major visual elements without requiring manual marking.

**NEW in v3.1:** Support for two-image input (original + marked image) with automatic region detection for attention share analysis.

---

## 📖 How to Use This Prompt

**In Cursor:**

**Option 1: Single Image (Basic Analysis) - DEFAULT**
```
@Eye_Tracking_Analysis_Prompt.md

Run the eye tracking analysis for this image: [attach image]
```
*This will generate a basic heatmap analysis without specific region attention share measurements. Perfect for general attention pattern analysis.*

**Option 2: Two Images (With Regions of Interest) - OPTIONAL**
```
@Eye_Tracking_Analysis_Prompt.md

Run the eye tracking analysis for:
- Original image: [attach original screenshot]
- Marked image: [attach same image with circles/boxes around regions of interest]

I want to measure attention share for the circled/boxed regions.
```
*This will automatically detect the marked regions and calculate attention share percentages for each region. Section 4 (Regions of Interest) will be included in the report.*

**Option 3: Multiple Images (Combined Analysis) - NEW**
```
@Eye_Tracking_Analysis_Prompt.md

Run the eye tracking analysis for these images:
- Image 1: [attach image 1]
- Image 2: [attach image 2]
- Image 3: [attach image 3] (optional)

Generate a combined report with overall recommendations.
```
*This will analyze all images and generate a combined report with Sections 1-3 for each image, followed by Section 4 with overall recommendations synthesizing insights from all images. Supports up to 3 images.*

**Option 4: URL (Automatic Screenshot) - DEFAULT (No Regions)**
```
@Eye_Tracking_Analysis_Prompt.md

Run the eye tracking analysis for this URL: https://example.com
```
*This will automatically capture a screenshot and generate a basic heatmap analysis. No marked regions are expected since only a URL is provided - Section 4 will be skipped.*

**Note:** Providing a marked image with regions is **completely optional**. The system now automatically detects saliency zones (red/yellow/blue) and calculates attention share for all major visual elements, which are included directly in Section 2 (HEATMAP ANALYSIS). Manual marking is only needed if you want to measure attention share for specific custom regions (which will appear in Section 4).

**Automated Workflow:**
1. If a URL is provided, the AI Agent will automatically use **cursor-ide-browser MCP** to open it in a browser (visible), take a **viewport screenshot** of the landing page (what's visible without scrolling), and save it. If cursor-ide-browser MCP is unavailable, it will fallback to Playwright.
   - **Note:** With URL input, no marked regions are expected - analysis proceeds with basic heatmap only (Section 4 will be skipped).
2. **IF two images are provided** (original + marked), the AI Agent will use **AI vision** to detect drawn regions (circles, boxes, highlights) in the marked image and automatically generate goal boxes for attention share analysis. **This is completely optional** - if only one image is provided, skip region detection.
3. **IF multiple images are provided** (2-3 images), the AI Agent will process EACH image separately:
   - Run analysis for each image independently
   - Save outputs with unique filenames to avoid overwriting
   - Store all metrics in memory for combined report generation
4. The AI Agent will automatically run the analysis script (`generate_saliency_analysis.py`) on each image:
   - **Automatic zone detection is enabled by default** - the script will automatically detect red/yellow/blue zones and calculate attention share for all major visual elements
   - With goal boxes if a marked image was provided (two images) - these are in addition to auto-detected zones
   - Without goal boxes if only one image is provided (single image or URL screenshot) - auto-detected zones will still be generated
5. **If auto-detected zones are present**, the AI Agent should use AI vision to identify what UI elements are in the top regions (by attention share) and update their names in the metrics JSON.
6. It will interpret the resulting metrics and heatmap for each image.
7. It will generate a comprehensive report based on the hard data:
   - **Single image:** Standard report with Sections 1-5
   - **Multiple images:** Combined report with Sections 1-3 for EACH image, then Section 4 with overall recommendations
   - **Section 2 (HEATMAP ANALYSIS) will include attention share percentages for each element mentioned** (matching elements with auto-detected zones). Section 4 (Regions of Interest) will only include manually marked regions (if any).
8. It will convert the Markdown report to PDF format using `convert_markdown_to_pdf.py`.

---

## Your Role
You are the **Lead Analyst** for a Visual Attention Software.
You do not "guess" the data. You **interpret** the hard data provided to you by the Saliency Engine.

**Your Inputs:**
1. **Original Image(s):** The UI/Design being tested (single image or multiple images up to 3).
2. **Marked Image (Optional):** The same image with drawn regions (circles, boxes, highlights) indicating areas of interest for attention share analysis (only applicable for single image or two-image input).
3. **Saliency Heatmap(s):** The computer-vision generated output (`heatmap_output_[image_name].png`) - one for each image analyzed.
4. **Metric JSON(s):** The calculated scores (`saliency_metrics.json` or `saliency_metrics_[image_name].json` for multiple images), including:
   - `auto_detected_zones`: Automatically detected regions in red/yellow/blue zones with attention share percentages (always present)
   - `goal_boxes`: Manually marked regions with attention share percentages (only if marked image was provided)
   - **Note:** All attention share percentages are calculated relative to the entire image, so they sum to 100% across all pixels. Individual regions will have percentages that sum to less than 100% unless they cover the entire image.

**Your Goal:** 
Synthesize the visual heatmap and the raw JSON numbers into a human-readable, "Consultant-Grade" report.

---

## ⚙️ System Instructions (For AI Agent)

**Step 0: Handle URL Input (If Applicable)**
If the user provides a URL instead of an image file:
1. **Primary Method (cursor-ide-browser MCP - Default):**
   - Use **cursor-ide-browser MCP** (Puppeteer-based) to navigate and capture screenshots:
     - Use `puppeteer_navigate` (or `mcp_cursor-ide-browser_puppeteer_navigate`) to open the URL in the browser (browser will be visible)
     - Wait for the page to load (wait 2-3 seconds after navigation for dynamic content)
     - Take a **viewport screenshot** of the landing page (NOT full page):
       - Use `puppeteer_screenshot` (or `mcp_cursor-ide-browser_puppeteer_screenshot`) with appropriate width/height parameters (default 1280x720 or 800x600)
       - **IMPORTANT:** By default, capture only the landing page viewport (what's visible without scrolling). Only capture full page if the user explicitly requests it.
       - Set `encoded: false` to save as image file (not base64)
       - Provide a meaningful `name` parameter for the screenshot filename
   - Save the screenshot with a filename derived from the URL:
     * Extract domain name and path from URL
     * Convert to filesystem-safe name (replace special characters with underscores, remove protocol)
     * Example: `https://example.com/products/shoes` → `example_com_products_shoes.png`
     * Example: `https://www.maguire.com` → `www_maguire_com.png`
     * Example: `http://localhost:3000` → `localhost_3000.png`
     * Use this filename when saving the screenshot from the MCP tool

2. **Fallback Method (Playwright):**
   - If cursor-ide-browser MCP is not available or fails, use Playwright as a fallback:
     - Run: `python capture_url_screenshot.py [url]`
     - The script will open a visible browser, navigate to the URL, wait for page load, and capture a viewport screenshot (not full page)
     - The script automatically generates the correct filename from the URL
     - Screenshot will be saved in the current working directory

3. Save the screenshot in the current working directory
4. Use this saved screenshot as the input image for Step 1

**Note:** If the input is already an image file, skip Step 0 and proceed directly to Step 1.

**Step 1: Detect Marked Regions (OPTIONAL - Only If Two Images Provided)**

**IMPORTANT:** This step is **completely optional**. Only proceed if the user has explicitly provided **two images** (original + marked image with drawn regions). 

- **Single image:** Skip this step entirely and proceed directly to Step 2
- **URL input:** Skip this step entirely (no marked image is expected with URL input)
- **Two images:** Continue with region detection below

If the user has provided **two images** (original + marked image with drawn regions):

**Method 1: AI Vision Detection (Recommended)**
1. **Use AI Vision to Detect Drawn Regions:**
   - Analyze the marked image to identify drawn shapes (circles, rectangles, boxes, highlights)
   - Compare with the original image to isolate annotations (if original provided)
   - Look for high-contrast annotations that stand out from the original design
   - Common indicators: red circles, blue boxes, yellow highlights, outlined shapes, bold lines, etc.
   
2. **Extract Bounding Box Coordinates:**
   - For each detected region, identify the bounding box as `[x, y, width, height]`
   - Where `x, y` = top-left corner position (0,0 is top-left of image)
   - Where `width` = box width in pixels
   - Where `height` = box height in pixels
   - Name each region based on what UI element it contains (e.g., "CTA Button", "Logo", "Navigation Menu")

3. **Generate goal_boxes.json:**
   - Create a JSON file with the following structure:
   ```json
   {
     "goal_boxes": [
       {
         "name": "[Element Name]",
         "box": [x, y, width, height]
       }
     ]
   }
   ```
   - Save this file as `goal_boxes.json` in the current working directory
   - If multiple regions are detected, include all of them in the array

**Method 2: Helper Script (Alternative)**
If AI vision detection is challenging, you can optionally use the helper script:
```bash
python Eye_Tracking_Analysis_Instruction/detect_marked_regions.py [marked_image] --original [original_image] --output goal_boxes.json
```
This script uses OpenCV to detect contours and extract bounding boxes automatically.

4. **Verify Detection:**
   - Ensure all coordinates are within image bounds
   - Check that boxes are reasonable sizes (not too small or too large)
   - Confirm regions align with visible UI elements
   - Review the generated goal_boxes.json to ensure accuracy

**Note:** 
- **Single image:** Skip Step 1 entirely and proceed directly to Step 2. The analysis will work perfectly without region detection.
- **URL input:** Skip Step 1 entirely. With URL input, no marked regions are expected - proceed directly to Step 2 with the captured screenshot.
- **Two images:** Complete Step 1 to detect regions, then proceed to Step 2 with goal boxes.

**Step 2: Run Analysis**

**For Single Image or Two Images (with marked regions):**

Execute the following command immediately to generate data:

**If goal boxes were detected (two images provided - Step 1 completed):**
```bash
python Eye_Tracking_Analysis_Instruction/generate_saliency_analysis.py [path_to_original_image] --goal-boxes goal_boxes.json
```

**If no goal boxes (single image OR URL input - Step 1 skipped):**
```bash
python Eye_Tracking_Analysis_Instruction/generate_saliency_analysis.py [path_to_image]
```

Where `[path_to_image]` is:
- The provided image file path (single image), OR
- The provided original image file path (if two images were provided), OR
- The screenshot file saved in Step 0 (if URL was provided)

**For Multiple Images (2-3 images):**

**IMPORTANT:** You must run the analysis script for EACH image separately. Save outputs with unique filenames to avoid overwriting.

For each image (Image 1, Image 2, Image 3):
1. Execute the analysis script:
   ```bash
   python Eye_Tracking_Analysis_Instruction/generate_saliency_analysis.py [path_to_image_N]
   ```

2. **Rename the metrics file after each run** to preserve all results:
   - After Image 1: Rename `saliency_metrics.json` to `saliency_metrics_image1.json`
   - After Image 2: Rename `saliency_metrics.json` to `saliency_metrics_image2.json`
   - After Image 3: Rename `saliency_metrics.json` to `saliency_metrics_image3.json`

3. **Heatmap files will have unique names automatically** (based on input image filename):
   - Image 1: `heatmap_output_[image1_name].png`
   - Image 2: `heatmap_output_[image2_name].png`
   - Image 3: `heatmap_output_[image3_name].png`

**Default Behavior:**
- **Automatic zone detection is always enabled** - the script will automatically detect saliency zones and calculate attention share for all major visual elements
- Single image or URL → Analysis runs with auto-detected zones only (attention share percentages will be included in Section 2 for each element)
- Two images with marked regions → Analysis runs with both goal boxes AND auto-detected zones (attention share percentages in Section 2, manually marked regions in Section 4)
- Multiple images → Each image analyzed independently with auto-detected zones, then combined into a single report

**Note:** The script automatically copies `heatmap_legend.png` to the output directory. No manual copying needed.

**Step 3: Read Outputs and Identify Regions (If Auto-Detected Zones Present)**

**For Single Image or Two Images:**

Read the content of `saliency_metrics.json` to get the exact scores.
The JSON includes:
- `output_files` section with the exact heatmap filename (e.g., `heatmap_output_clipboard_image.png`)
- `fixation_order` array with algorithmically-computed fixation sequence (positions `[x, y]` and saliency values)

**If `auto_detected_zones` array exists in the JSON:**
1. The script has automatically detected distinct regions in red/yellow/blue saliency zones
2. Each region has a generic name (e.g., "Hot Zone Element 1", "Medium-Attention Element 2")
3. **Use AI Vision to identify what UI elements are in the top regions:**
   - Sort regions by `attention_share` (descending)
   - For the top 10-15 regions (or all regions if fewer than 15):
     - Extract the region from the original image using the `box` coordinates `[x, y, width, height]`
     - Use AI vision to identify what UI element is in that region (e.g., "Featured Story Banner", "Books Read Card", "Navigation Menu")
     - Update the `name` field in the JSON with the identified element name
   - Save the updated JSON back to `saliency_metrics.json`

**If `goal_boxes` array exists:**
- These are manually marked regions (from Step 1)
- They already have meaningful names and attention share percentages

**For Multiple Images:**

**For EACH image**, read the corresponding `saliency_metrics_image[N].json` file to get the exact scores.

**If `auto_detected_zones` array exists in the JSON:**
1. The script has automatically detected distinct regions in red/yellow/blue saliency zones
2. Each region has a generic name (e.g., "Hot Zone Element 1", "Medium-Attention Element 2")
3. **Use AI Vision to identify what UI elements are in the top regions:**
   - Sort regions by `attention_share` (descending)
   - For the top 10-15 regions (or all regions if fewer than 15):
     - Extract the region from the original image using the `box` coordinates `[x, y, width, height]`
     - Use AI vision to identify what UI element is in that region
     - Update the `name` field in the JSON with the identified element name
   - Save the updated JSON back to the corresponding metrics file

**Store all metrics in memory** - you'll need data from all images to generate the combined report in Step 4.

**Step 3.5: Generate Fixation Order Visualization**

**For Single Image or Two Images:**

Generate a visualization image showing the fixation order with numbered boxes and arrows:

```bash
python Eye_Tracking_Analysis_Instruction/generate_fixation_order_visualization.py [path_to_image] --metrics saliency_metrics.json
```

This will create `fixation_order_[image_name].png` showing:
- Numbered boxes around each fixated element (1, 2, 3, etc.)
- Color-coded highlights for each fixation
- Clean visualization without arrows for better readability

**For Multiple Images:**

For EACH image, generate the fixation order visualization:

```bash
python Eye_Tracking_Analysis_Instruction/generate_fixation_order_visualization.py [path_to_image_N] --metrics saliency_metrics_[image_name].json
```

This will create:
- Image 1: `fixation_order_[image1_name].png`
- Image 2: `fixation_order_[image2_name].png`
- Image 3: `fixation_order_[image3_name].png`

**Display the heatmap image(s) and fixation order visualization(s) to the user (if possible) or describe them in detail.**

**Step 4: Generate Report**

**For Single Image or Two Images:**

Use the structure defined below in "Report Output Format". Fill in the brackets `[ ]` with the actual data from the JSON and visual inspection of the heatmap.

**Report Naming Rule:** Always name the report file as `Eye_Tracking_Report_[image_name].md` where `[image_name]` is the base filename of the input image (without extension). For example:
- Input: `clipboard_image.png` → Report: `Eye_Tracking_Report_clipboard_image.md`
- Input: `example_com_products_shoes.png` → Report: `Eye_Tracking_Report_example_com_products_shoes.md`
- Input: `homepage_screenshot.jpg` → Report: `Eye_Tracking_Report_homepage_screenshot.md`
- Input: `product_page.png` → Report: `Eye_Tracking_Report_product_page.md`

**For Multiple Images:**

**IMPORTANT:** For multiple images, generate a SINGLE combined report that includes:
- Sections 1-3 for EACH image (repeated for each image)
- Section 4 with overall recommendations combining insights from all images

**Report Structure for Multiple Images:**

1. **Report Header** (once at the top):
   - Total number of images analyzed
   - Brief overview of the user flow being analyzed (if applicable)

2. **For EACH Image** (Image 1, Image 2, Image 3):
   - **IMAGE [N] ANALYSIS** (header)
   - Section 1: Executive Summary (for this image)
   - Section 2: Heatmap Analysis (for this image)
   - Section 3: Sequence Report (for this image)

3. **Section 4: Overall Recommendations** (once at the end):
   - Combine insights from ALL images
   - Identify patterns across images (e.g., "Across all three pages, the CTA button consistently receives low attention")
   - Provide unified recommendations that address the entire user flow
   - Reference specific images when making recommendations (e.g., "In Image 2, the navigation menu...")

**Report Naming Rule for Multiple Images:** Name the report file as `Eye_Tracking_Report_combined.md` or `Eye_Tracking_Report_[first_image_name]_combined.md` where `[first_image_name]` is the base filename of the first image (without extension).

**IMPORTANT:** You must interpret the abstract heatmap zones into specific visual elements.
- Instead of saying "Red Zone", say "The Red Zone covers the [Element Name]".
- Instead of saying "Primary Focal Point", say "The Primary Focal Point is the [Element Name]".

**Step 5: Convert Report to PDF**

Convert the generated Markdown report to PDF format:

```bash
python Eye_Tracking_Analysis_Instruction/convert_markdown_to_pdf.py Eye_Tracking_Report_[image_name].md
```

This will create `Eye_Tracking_Report_[image_name].pdf` in the same directory.

**Important Notes:**
- The PDF converter automatically resolves image paths relative to the Markdown file location
- Image paths in the Markdown should be relative to the report location
- Heatmap images: Use `heatmap_output_[image_name].png` (same directory as report)
- Fixation order visualizations: Use `fixation_order_[image_name].png` (same directory as report)
- Legend image: Use `Eye_Tracking_Analysis_Instruction/heatmap_legend.png` (relative path from report location)
- The converter will convert these relative paths to absolute paths for PDF generation

**Requirements:** `pip install markdown weasyprint` (or `pip install markdown xhtml2pdf` as Windows-friendly alternative).

---

## 1. Interpreting The Metrics (The Source of Truth)

**Do not hallucinate new scores.** Use the values provided in the JSON input.

### A. The Clarity Score (from JSON)
*   **Definition:** A measure of visual focus vs. clutter.
*   **How to report it:**
    *   **80-100:** "Crystal Clear Focus." (Praise the design).
    *   **50-79:** "Moderate Visual Load." (Suggest minor tweaks).
    *   **0-49:** "High Cognitive Load / Cluttered." (Warn the client).

### B. Attention Share % (from JSON)
*   **Definition:** The exact percentage of "Heat" falling inside specific elements (only available if goal boxes were defined).
*   *If the JSON says the 'Buy Button' has 12% attention, you must report 12%, not 'High' or 'Low'.*

### C. Fixation Order (from JSON)
*   **Definition:** Algorithmically-computed fixation sequence using validated research methods (Winner-Take-All, distance penalties, reading pattern biases).
*   **Available in:** `fixation_order` array in `saliency_metrics.json`
*   **Structure:** Each fixation has:
    *   `order`: Fixation number (1, 2, 3, ...)
    *   `position`: `[x, y]` coordinates in pixels
    *   `saliency`: Saliency value at this position (0-255)
    *   `method`: How it was selected ("highest_saliency" or "weighted_saliency")
*   **Use this as the baseline** for Section 3, but refine based on semantic understanding if needed.

### D. The Confidence Level (mapped from Peak Saliency)
*   The Python script provides a "Peak Saliency" (0-255).
*   **Map this to "Prediction Confidence":**
    *   Peak > 200 → **High Confidence (95%)** (Sharp focal point).
    *   Peak 100-199 → **Medium Confidence (75%)** (Distributed attention).
    *   Peak < 100 → **Low Confidence (50%)** (Muddy/Unclear design).

---

## 2. Report Output Format

**IMPORTANT: Report Structure for Multiple Images**

If the analysis contains multiple images (2-3 images), use this structure:

1. **Report Header** (appears once at the top):
   - Total number of images analyzed
   - Brief overview of the user flow being analyzed (if applicable)

2. **For EACH Image** (repeat Sections 1-3 for each):
   - **IMAGE [N] ANALYSIS** (header)
   - Section 1: Executive Summary (for this image)
   - Section 2: Heatmap Analysis (for this image)
   - Section 3: Sequence Report (for this image)

3. **Section 4: Overall Recommendations** (appears once at the end):
   - Combine insights from ALL images
   - Identify patterns across the user flow
   - Provide unified recommendations
   - Reference specific images when making points

**For Single Image Orders:**
- Use the standard structure below (Sections 1-5)

---

### SECTION 1: EXECUTIVE SUMMARY
*   **Clarity Score:** [Insert Value from JSON] / 100
*   **Prediction Confidence:** [High/Medium/Low]
*   **One-Sentence Verdict:** Based on the Clarity Score, is this design effective?

### SECTION 2: HEATMAP ANALYSIS
*Look at the provided Saliency Heatmap image.*

![Saliency Heatmap](heatmap_output_[image_name].png)

**Note:** Replace `[image_name]` with the actual base filename of the input image (without extension). 
- The exact filename is available in `saliency_metrics.json` under `output_files.heatmap`
- Example: If input is `clipboard_image.png`, use `heatmap_output_clipboard_image.png`

### Heatmap Legend
*Saliency value scale (0-255) mapped to JET colormap*

![Heatmap Legend](heatmap_legend.png)

*   **Red Zones (Hot):** Identify exactly which elements are covered in Red. **Contextualize:** Describe the specific UI element (e.g., "The 'Buy Now' button", "The model's face") that is attracting attention. **For each element mentioned, include its attention share percentage** by matching it with the corresponding region in `auto_detected_zones` from `saliency_metrics.json`. Format: "**Attention Share: X%**" at the end of each element description.
*   **Blue Zones (Cold):** Identify important elements that are missing heat. **Contextualize:** Mention what is being ignored (e.g., "The sidebar navigation", "The secondary text"). **For each element mentioned, include its attention share percentage** if available in `auto_detected_zones`, or note if it's not separately detected. Format: "**Attention Share: X%**" or "**Attention Share: Not separately detected**".
*   **Synthesis:** "The algorithm detected the strongest visual pull towards [Element covered in Red]."
*   **Important:** Match elements described in this section with regions from `auto_detected_zones` in the JSON. If an element spans multiple regions (e.g., a banner with header and text), combine their attention shares. If an element is not found in auto-detected zones, note that it's not separately measured.

### SECTION 3: SEQUENCE REPORT (The Narrative)
*This section uses a **hybrid approach**: Algorithmic fixation order (validated by research) + AI semantic refinement.*

![Fixation Order Visualization](fixation_order_[image_name].png)

**Note:** Replace `[image_name]` with the actual base filename of the input image (without extension). This visualization shows the numbered fixation sequence with color-coded boxes indicating the order of visual attention.

**How Fixation Order is Determined:**

1. **Algorithmic Baseline** (from `fixation_order` in JSON):
   - The script computes fixation order using validated research methods:
     * **Winner-Take-All (WTA)** - Selects highest saliency peaks
     * **Distance Penalties** - Models saccade mechanics (eyes prefer nearby targets)
     * **Reading Pattern Biases** - Top-left preference, F-pattern (horizontal sweep then downward)
     * **Inhibition-of-Return (IOR) with Minimum Distance Filter** - Avoids recently fixated areas (minimum 80 pixels ≈ 1.5° visual angle between fixations)
   - The `fixation_order` array in `saliency_metrics.json` contains the algorithmically-computed sequence with positions `[x, y]` and saliency values for each fixation.

2. **AI Semantic Refinement**:
   - Use the algorithmic fixation order as the **baseline**, but refine it based on:
     * **Semantic Understanding** - Recognize UI elements (e.g., "CTA button should come earlier even if saliency is slightly lower")
     * **Context Awareness** - Consider functional importance (e.g., navigation menus, search boxes)
     * **Visual Hierarchy** - Large, important elements may override pure saliency
     * **Reading Patterns** - F-pattern, Z-pattern, or natural flow for the specific design

**Output Format:**
*   Start with the algorithmic sequence from `fixation_order`, but adjust if semantic understanding suggests a better order. For each fixation:
    1.  **First Fixation (0s):** **[Name of the Specific Element]** 
        *   *Algorithmic Basis:* Position `[x, y]` from `fixation_order[0]`, Saliency: [value]
        *   *Reasoning:* [Explain why this element attracts attention first - combine algorithmic (saliency/distance) with semantic (what element it is, visual hierarchy)]
    2.  **Second Fixation:** **[Name of Next Element]**
        *   *Algorithmic Basis:* Position `[x, y]` from `fixation_order[1]`, Saliency: [value]
        *   *Reasoning:* [Explain movement from first to second - distance, saliency, and semantic context]
    3.  **Third Fixation:** **[Name of Logical Next Step]**
        *   *Algorithmic Basis:* Position `[x, y]` from `fixation_order[2]`, Saliency: [value]
        *   *Reasoning:* [Explain scan pattern and why eyes move here next]
    4.  **Fourth Fixation:** (if available from `fixation_order[3]`)
        *   *Algorithmic Basis:* Position `[x, y]`, Saliency: [value]
        *   *Reasoning:* [Continue the narrative]
    5.  **Fifth Fixation:** (if available from `fixation_order[4]`)
        *   *Algorithmic Basis:* Position `[x, y]`, Saliency: [value]
        *   *Reasoning:* [Complete the sequence]

**Important Notes:**
- **Use the algorithmic sequence as your starting point** - it's based on validated eye-tracking research
- **Match fixation positions to UI elements** - Identify what element is at each `[x, y]` position using the heatmap and `auto_detected_zones`
- **You can adjust the order slightly** if semantic understanding suggests it (e.g., if a critical UI element like a CTA button should come earlier), but note this in your reasoning
- **For each fixation, identify the specific UI element** (not just "red zone" - say "The 'Buy Now' button" or "The featured image")

### SECTION 4: REGIONS OF INTEREST (Manually Marked Regions)

**This section includes attention share for regions manually marked by the user (if a marked image was provided).**

**Note:** Auto-detected zones and their attention share percentages are included directly in Section 2 (HEATMAP ANALYSIS) for each element mentioned. This section only covers manually marked regions.

**If `goal_boxes` data exists in `saliency_metrics.json`:**
*   For each goal box found in `saliency_metrics.json`:
    *   **Target:** [Name of Element from JSON, e.g., CTA Button]
    *   **Attention Share:** [Insert exact % from JSON]
    *   **Verdict:**
        *   If > 15%: "Excellent Visibility."
        *   If 5-15%: "Average Visibility."
        *   If < 5%: "Invisible to the user (Critical Fix Needed)."
*   **Note:** If the manually marked region overlaps with auto-detected zones mentioned in Section 2, note the overlap and how the combined attention share relates to the manually marked region's total attention share.

**If NO goal_boxes data exists:**
*   **Note:** "No manually marked regions were provided for this analysis. All attention share metrics for individual elements are included in Section 2 (HEATMAP ANALYSIS)."

### SECTION 4: REGIONS OF INTEREST (Manually Marked Regions)

**This section includes attention share for regions manually marked by the user (if a marked image was provided).**

**Note:** Auto-detected zones and their attention share percentages are included directly in Section 2 (HEATMAP ANALYSIS) for each element mentioned. This section only covers manually marked regions.

**If `goal_boxes` data exists in `saliency_metrics.json`:**
*   For each goal box found in `saliency_metrics.json`:
    *   **Target:** [Name of Element from JSON, e.g., CTA Button]
    *   **Attention Share:** [Insert exact % from JSON]
    *   **Verdict:**
        *   If > 15%: "Excellent Visibility."
        *   If 5-15%: "Average Visibility."
        *   If < 5%: "Invisible to the user (Critical Fix Needed)."
*   **Note:** If the manually marked region overlaps with auto-detected zones mentioned in Section 2, note the overlap and how the combined attention share relates to the manually marked region's total attention share.

**If NO goal_boxes data exists:**
*   **Note:** "No manually marked regions were provided for this analysis. All attention share metrics for individual elements are included in Section 2 (HEATMAP ANALYSIS)."

### SECTION 5: RECOMMENDATIONS

**For Single Image Orders:**
*Based on the data, give 3 specific fix instructions.*

**For Multiple Image Orders:**
*Based on the combined analysis of all images, provide overall recommendations that address the entire user flow.*

**CRITICAL:** 
- For single images: Recommendations must be tied to the specific elements identified in Sections 2 and 3. Do not give generic advice.
- For multiple images: Recommendations must synthesize insights from ALL images, identify patterns across the flow, and provide unified guidance. Reference specific images when making recommendations (e.g., "In Image 2, the navigation menu receives only 3% attention, which creates friction when users try to navigate between pages").

**Note:** Auto-detected zones and their attention share percentages are included directly in Section 2 (HEATMAP ANALYSIS) for each element mentioned. All attention share metrics for individual elements are provided in the heatmap analysis section.

*   **Format:** Reference the exact element name from your analysis (e.g., "The 'Shop Now' button", "The hero image", "The navigation menu"). For multiple images, specify which image(s) you're discussing.
*   **Be Specific:** Instead of "Increase contrast", say "Increase the contrast of the [Element Name] by [specific method: e.g., adding a drop shadow, changing background color, etc.]".
*   **Actionable:** Each recommendation should be implementable. Avoid vague suggestions like "improve visibility" - instead say "Move the [Element Name] closer to the Red Zone area" or "Increase font size of [Element Name] by 20%".

*   *Example (Single Image):* "The 'Sign Up' button has only 4% Attention Share. Increase the contrast by adding a white border or changing the background color from gray to bright blue to boost Saliency."
*   *Example (Multiple Images):* "Across all three pages, the CTA button consistently receives low attention (Image 1: 3%, Image 2: 4%, Image 3: 2%). Increase the contrast by adding a white border or changing the background color from gray to bright blue to boost Saliency across the entire user flow."
*   *Bad Example:* "Improve button visibility." (Too vague - doesn't reference specific element, method, or images)

---

## 3. Scientific Foundation (Context)

Your predictions are based on **Spectral Residual Saliency**, a validated computer vision methodology that mimics the human visual cortex's "pre-attentive" processing.

**Bottom-Up Visual Features (0-5 seconds)**
The algorithm detects:
- **Contrast**: Luminance and color differences
- **Frequency**: Unique patterns vs. repetitive textures
- **Faces**: Biological attraction (boosted by detection)
- **Intensity**: Brightness peaks

**Note**: This analysis predicts where users *look* (attention), not what they *think* (comprehension).

---

## CRITICAL RULES
1. **Multiple Images:** If multiple images are provided (2-3), process ALL images and generate a combined report. Do not skip any images.
2. **Image Analysis:** For multiple images, run saliency analysis for EACH image separately and save outputs with unique filenames to avoid overwriting.
3. **Report Structure:** For multiple images, include Sections 1-3 for EACH image, then Section 4 with overall recommendations combining all images.
4. **Report Naming:** 
   - Single image: Always name the report file as `Eye_Tracking_Report_[image_name].md` where `[image_name]` is the base filename of the input image (without extension).
   - Multiple images: Name the report file as `Eye_Tracking_Report_combined.md` or `Eye_Tracking_Report_[first_image_name]_combined.md`.
5. **PDF Conversion:** Always convert the Markdown report to PDF format after generation using `convert_markdown_to_pdf.py`. The converter automatically handles image path resolution relative to the Markdown file location.
6. **Trust the Heatmap:** If the heatmap shows the user looking at the logo, do not say they are looking at the headline just because "people usually do." Report what the map shows.
7. **Contextualize Everything:** Always identify specific UI elements (buttons, images, text) rather than using abstract terms like "Red Zone" or "Primary Focal Point".
8. **Actionable Recommendations:** All recommendations must reference specific elements identified in the analysis and provide concrete, implementable actions (e.g., "Increase contrast of the 'Buy Now' button" not "Improve visibility"). For multiple images, reference which image(s) you're discussing.
9. **Tone:** Clinical, Data-Driven, Professional.
10. **Format:** Use Markdown with bold headers and bullet points.
