# Report Format

## Interpreting the Metrics (Source of Truth)

Never invent scores — use only the values in `saliency_metrics.json`.

**Clarity Score** (0-100, measures visual focus vs. clutter):
- 80-100 → "Crystal Clear Focus" (praise the design)
- 50-79 → "Moderate Visual Load" (suggest minor tweaks)
- 0-49 → "High Cognitive Load / Cluttered" (warn about it)

**Attention Share %** — exact percentage of total visual "heat" inside a region (`auto_detected_zones` or `goal_boxes`). Report the number exactly; never round to "High"/"Low" in place of the figure.

**Fixation Order** (`fixation_order` array) — algorithmically-computed sequence via Winner-Take-All + distance penalties + reading-pattern bias + inhibition-of-return. Use as the baseline; adjust order slightly only when semantic importance clearly overrides raw saliency (e.g. a CTA button should come earlier), and say so explicitly when doing so — see the **Hierarchy Correction Rule** below for the one specific, named case where this applies.

**Hierarchy Correction Rule (Size Dominance Over Edge Density)**: small, high-contrast text (e.g. a tight promotional caption) often scores a higher raw saliency peak than a much larger element nearby, because tightly-kerned edges create strong edge density — a known artifact of spectral-residual saliency, not a reflection of what a human actually looks at first. When a fixation's raw peak lands on a small element that sits in the same visual field as a substantially larger one (roughly 10x+ area difference), state explicitly that you're applying this rule, name both elements and their approximate sizes, and reassign the larger element as the more plausible fixation — human vision prioritizes size/prominence in the foveal capture range over pure contrast. Never apply this silently; always name it as an explicit override of the raw algorithmic order.

**Confidence Level** (mapped from `max_saliency_peak`, 0-255):
- Peak > 200 → **High** (95%) — sharp focal point
- Peak 100-199 → **Medium** (75%) — distributed attention
- Peak < 100 → **Low** (50%) — muddy/unclear design

## Report Structure

For **multiple images**: a header (image count + flow overview) once, then Sections 1-3 repeated per image, then one Section 4 (overall recommendations synthesizing all images, referencing them by name). For a **single image**: Sections 1-5 below.

Contextualize everything — never say "the Red Zone," say what's actually there ("the Red Zone covers the 'Sign Up' button").

### 1. Executive Summary
- Clarity Score: `[value]`/100
- Prediction Confidence: `[level]`
- One-sentence verdict: is the design effective?

### 2. Heatmap Analysis
Embed `![Saliency Heatmap](heatmap_output_<name>.png)` and `![Heatmap Legend](assets/heatmap_legend.png)` (blank line between consecutive images — see Troubleshooting in `SKILL.md`).

- **Red zones (hot)**: name the specific element, cite its `attention_share`.
- **Blue zones (cold)**: name what's being missed; cite `attention_share` if separately detected, else note "Not separately detected."
- **Synthesis**: one line naming the strongest pull, e.g. "the algorithm detected the strongest visual pull toward the 'Model 3' title."

### 3. Sequence Report (Narrative)

Before narrating fixations, classify the layout's scanning pattern (F-pattern, Z-pattern, Gutenberg diagram, or layer-cake — see `references/reading-patterns.md`) and state it in one opening line. Use the named pattern's known hot zones to reinforce or challenge the algorithmic order, not just raw saliency numbers in isolation.

For each fixation in `fixation_order` (typically 3-5):
1. **Position in sequence** (First/Second/... Fixation): name the element at that `position`.
   - *Algorithmic basis*: position `[x, y]`, saliency value.
   - *Reasoning*: why the eye lands/moves here — combine the algorithmic basis (distance, saliency), the identified scanning pattern (`references/reading-patterns.md`), and semantic reasoning (what the element is, why it matters). Note explicitly if diverging from raw algorithmic order per the Fixation Order rule above.

### 4. Regions of Interest (only if `goal_boxes` present)

For each goal box: name, exact attention-share %, and verdict:
- \>15% → "Excellent Visibility"
- 5-15% → "Average Visibility"
- <5% → "Invisible to the user (Critical Fix Needed)"

If no `goal_boxes`: state that all attention-share metrics for individual elements are already in Section 2.

### 5. Recommendations

Exactly 3 (single image) or synthesized-across-images (multi-image) specific, actionable fixes. Each must:
- Reference the exact element name from Sections 2-3 — never generic ("the CTA button" not "important elements")
- Say precisely what to change and how (e.g. "increase contrast of the 'Buy Now' button by switching its background from gray to a saturated blue" — not "improve visibility")
- For multi-image: identify cross-image patterns and reference which image(s) each point applies to

Tone throughout: clinical, data-driven, professional. Markdown with bold headers and bullet points.
