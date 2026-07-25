# Scanning Pattern Reference

Use this when writing Section 3 (Sequence Report). Identify which pattern the layout most resembles, name it explicitly in the report, and use it to justify (or override) the raw algorithmic fixation order.

## F-Pattern (dense text, articles, search results)

Nielsen Norman Group's 2006 eyetracking study (232 users, thousands of pages), reconfirmed in 2017 and still holding on mobile: eyes move in roughly three strokes forming an "F" —
1. A horizontal sweep across the top of the content area
2. A second, shorter horizontal sweep further down
3. A vertical scan down the left side, since users increasingly skim rather than read right-ward

**Applies when**: text-heavy pages — articles, blog posts, search results, long-form landing pages. **Design implication**: front-load the most important words at the start of headlines/paragraphs (upper-left is highest-value); content past the first two lines of a paragraph gets sharply less attention.

## Z-Pattern (sparse, image-led layouts)

Eyes move top-left → top-right (horizontal) → diagonally down to bottom-left → bottom-right (horizontal) — tracing a "Z". Common on landing pages, ads, and any layout alternating image/text blocks left-to-right.

**Applies when**: sparse content, marketing/landing pages, hero sections with one clear CTA. **Design implication**: put the logo/brand top-left, primary nav or a secondary signal top-right, and the primary CTA bottom-right (the natural end of the scan).

## Gutenberg Diagram (evenly-weighted, low-density layouts)

Divides the page into four quadrants for Western (left-to-right) readers:
- **Primary optical area** (top-left) — first seen, highest value
- **Strong fallow area** (top-right) — seen but lower engagement
- **Weak fallow area** (bottom-left) — most often skipped
- **Terminal area** (bottom-right) — last seen, second-highest value — natural CTA position

**Applies when**: simple, evenly-spaced layouts without a strong visual hierarchy already pulling the eye (forms, plain text pages). Culturally/linguistically dependent — assumes left-to-right reading order.

## Layer-Cake Pattern (headings + skimmable structure)

Fixations cluster on headings and subheadings with only occasional dips into body text — in a heatmap it looks like horizontal stripes (fixation) separated by blank bands (skipped body copy). NN/G identifies this as the most *effective* scanning strategy for finding information without reading every word.

**Applies when**: pages with clear heading hierarchy — documentation, FAQs, pricing tables, feature lists.

## How to Use This in the Report

1. Classify the layout: dense text → F-pattern; sparse/hero/landing → Z-pattern or Gutenberg; heading-heavy → layer-cake. State which one in the Sequence Report's opening line.
2. Cross-check the algorithmic `fixation_order` against the named pattern's predicted hot zones (e.g. top-left primary optical area, bottom-right terminal area). Where they agree, cite both as reinforcing evidence. Where they disagree, say so explicitly and default to the **Hierarchy Correction Rule** in `references/report-format.md` (size/prominence overrides raw saliency) rather than silently picking one.
3. Never invent a pattern that doesn't match the actual layout — if it's genuinely ambiguous, say "natural flow, no single named pattern dominates" rather than forcing an F/Z/Gutenberg label.

Sources: [F-Shaped Pattern of Reading on the Web (NN/G)](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/) · [F-Shaped Pattern: Misunderstood, But Still Relevant (NN/G)](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) · [The Layer-Cake Pattern of Scanning Content (NN/G)](https://www.nngroup.com/articles/layer-cake-pattern-scanning/)
