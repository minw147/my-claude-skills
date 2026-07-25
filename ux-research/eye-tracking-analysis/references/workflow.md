# Workflow Details

## URL Input (Step 0)

If given a URL instead of an image:

1. **Primary**: use browser automation (Puppeteer/Playwright/cursor-ide-browser MCP, whichever is available) to navigate to the URL, wait 2-3s for dynamic content, then capture a **viewport screenshot** (not full page — what's visible without scrolling, typically 1200x800 or 800x600).
2. **Fallback**: run `scripts/capture_url.py <url>` — opens a visible browser via Selenium, navigates, waits, captures a viewport screenshot, and saves it with a filesystem-safe filename derived from the URL (e.g. `https://example.com/shoes` → `example_com_shoes.png`).
3. Save the screenshot in the working directory and use it as the input image for the saliency analysis step.

Skip this step entirely if the input is already an image file.

## Marked-Region Detection (Step 1, optional)

Only applies when **two images** are provided (original + a copy with circles/boxes drawn around regions of interest). Skip entirely for a single image or a URL — no marked regions are expected in those cases.

1. **Preferred — vision detection**: inspect the marked image for drawn shapes (circles, rectangles, highlights), compare against the original to isolate the annotations, and extract each one's bounding box `[x, y, width, height]` (top-left origin). Name each region after the UI element it contains (e.g. "CTA Button", "Logo").
2. **Alternative — script**: `python scripts/detect_marked_regions.py <marked_image> --original <original_image> --output goal_boxes.json` (uses OpenCV contour detection).
3. Write the result to `goal_boxes.json`:
   ```json
   { "goal_boxes": [ { "name": "CTA Button", "box": [x, y, width, height] } ] }
   ```
4. Verify: coordinates within image bounds, boxes a reasonable size, regions align with visible elements.

## Running the Analysis (Step 2)

```bash
python scripts/generate_saliency_analysis.py <image_path> [--goal-boxes goal_boxes.json]
```

- With `goal_boxes.json` (from Step 1) → metrics include both `goal_boxes` and auto-detected `auto_detected_zones`.
- Without it (single image or URL screenshot) → metrics include `auto_detected_zones` only. This is the default and normal case.

Automatic zone detection is always on — it needs no flag.

## Reading Outputs & Naming Zones (Step 3)

Read `saliency_metrics.json`. It includes:
- `output_files.heatmap` — the exact heatmap filename to embed in the report
- `fixation_order` — algorithmically-computed sequence (`order`, `position: [x, y]`, `saliency`, `method`)
- `auto_detected_zones` — always present; generic names like "Hot Zone Element 1"
- `goal_boxes` — only present if Step 1 ran; already has meaningful names

For `auto_detected_zones`: sort by `attention_share` descending, and for the top 10-15 regions (or all, if fewer), use vision on the corresponding `box` crop of the original image to identify the real UI element, then update the JSON's `name` field in place before writing the report.

## Multiple Images (2-3 images)

Run Steps 0-3 independently **per image**, saving outputs with unique names to avoid overwriting:
- After each run, rename `saliency_metrics.json` → `saliency_metrics_image<N>.json`
- Heatmap filenames are already unique (derived from each input image's filename)
- Store all metrics in memory; the combined report (see `references/report-format.md`) needs data from every image at once

## PDF Export (Step 5, optional)

```bash
python scripts/convert_markdown_to_pdf.py Eye_Tracking_Report_<image_name>.md
```

Requires `pip install markdown xhtml2pdf`. The converter resolves image paths in the Markdown relative to the report's location automatically — reference `heatmap_output_<name>.png` (same directory as the report) and `assets/heatmap_legend.png` (relative path from the report) as-is.

## Report File Naming

- Single image: `Eye_Tracking_Report_<image_name>.md` (base filename, no extension) — e.g. `clipboard_image.png` → `Eye_Tracking_Report_clipboard_image.md`
- Multiple images: `Eye_Tracking_Report_combined.md` or `Eye_Tracking_Report_<first_image_name>_combined.md`
