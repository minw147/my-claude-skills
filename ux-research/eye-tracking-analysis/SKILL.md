---
name: eye-tracking-analysis
description: Predicts visual attention from a screenshot or URL using Spectral Residual Saliency — heatmaps, clarity scores, fixation sequences, and attention-share reports for UI and landing-page reviews.
license: MIT
version: 2.0.0
---

# Eye-Tracking Analysis

## Overview

Predict where a viewer's eyes go in the first 3-5 seconds of looking at a screenshot, website, or UI design, using Spectral Residual Saliency — a validated computer-vision method (~85-90% accuracy vs. real eye-tracking studies). Produce a heatmap, a clarity score, a predicted fixation sequence, auto-detected attention zones, and a written report with actionable recommendations.

## When to Use

Invoke this skill when asked to:
- Analyze a landing page, UI mockup, or ad creative for visual attention/hierarchy
- Predict which elements users will notice first, or miss entirely
- Compare two or more design variants (A/B test) for attention differences
- Measure attention share for a specific marked element (a CTA button, headline, etc.)

## Core Workflow

1. Obtain the input image.
   - Given a URL instead of an image: capture a screenshot first — run `scripts/capture_url.py <url>`. Fallback method in `references/workflow.md`.
   - Given two images (original + one with circled/boxed regions of interest): extract them as goal boxes — run `scripts/detect_marked_regions.py <marked_image> --original <original_image> --output goal_boxes.json`, or identify the regions via vision and write `goal_boxes.json` in the format in `references/workflow.md`.
2. Run the saliency analysis:
   ```bash
   python scripts/generate_saliency_analysis.py <image_path> [--goal-boxes goal_boxes.json]
   ```
   Produces `saliency_metrics.json` and `heatmap_output_<name>.png` in the same directory.
3. Read `saliency_metrics.json`. If `auto_detected_zones` is present, use vision to identify the actual UI element in each of the top zones (by `attention_share`) and rename it from its generic placeholder (e.g. "Hot Zone Element 1" → "Sign Up Button").
4. Write the report following the exact structure and metric-interpretation rules in `references/report-format.md`. Do not invent numbers — use only what the JSON provides.
5. For multiple images (up to 3): repeat steps 1-3 per image with unique output filenames (`references/workflow.md`), then produce one combined report per `references/report-format.md`'s multi-image structure.
6. Save the report as `Eye_Tracking_Report_<image_name>.md`. Optionally convert to PDF:
   ```bash
   python scripts/convert_markdown_to_pdf.py Eye_Tracking_Report_<image_name>.md
   ```
   Requires `pip install markdown xhtml2pdf`.

## Reference Files

- `references/workflow.md` — full procedure for URL capture, region detection, multi-image handling, PDF export, and file-naming conventions
- `references/report-format.md` — metric-interpretation rules and the exact report section structure/formatting
- `references/reading-patterns.md` — F-pattern, Z-pattern, Gutenberg diagram, and layer-cake scanning research (NN/G), used to ground the Sequence Report in real UX literature instead of raw saliency numbers alone
- `references/algorithm.md` — how Spectral Residual Saliency actually computes the heatmap, clarity score, and attention share, plus the original Hou & Zhang (2007) citation

## Setup

```bash
pip install opencv-contrib-python selenium webdriver-manager markdown xhtml2pdf
```

`assets/heatmap_legend.png` is copied automatically into each output directory by the analysis script.

## Scientific Foundation

Spectral Residual Saliency originates from Hou, X., & Zhang, L. (2007), *Saliency Detection: A Spectral Residual Approach*, IEEE CVPR 2007, pp. 1-8. Full math, our enhancements (face-boost, clarity score), and citation/BibTeX are in `references/algorithm.md`; the complete write-up (with related work and limitations) is published at [heatmap.mintleafux.com/SPECTRAL_RESIDUAL_EXPLANATION.html](https://heatmap.mintleafux.com/SPECTRAL_RESIDUAL_EXPLANATION.html).

## Troubleshooting

- **Missing legend in output**: the script copies it from `assets/` — verify `assets/heatmap_legend.png` exists in the skill folder.
- **Side-by-side image rendering bug** in generated Markdown: ensure a blank line between consecutive `![]()` image tags.
- **`cv2.saliency` import error**: install `opencv-contrib-python`, not just `opencv-python`.
