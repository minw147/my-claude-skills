# Eye-Tracking Analysis Tool - Quick Start Guide

## 5-Second Setup

1. Open AI vision model (GPT-4V, Claude 3.5, Cursor, etc.)
2. **Reference the prompt:**
   - **In Cursor:** `@Eye_Tracking_Analysis_Prompt.md` 
   - **In ChatGPT/Claude:** Upload `Eye_Tracking_Analysis_Prompt.md` file
3. Upload your image + use examples below
4. Get professional eye-tracking report!

---

## Most Common Use Cases

### 1. Basic Analysis (General Heat Map)
```
"@Eye_Tracking_Analysis_Prompt.md

Generate a complete eye-tracking report for this [webpage/app/ad] following 
the prompt framework. Include heat map with legend and sequence report.
Also, generate a visual heat map image using the systematic workflow."

[Attach image]
```
**You'll get:** Complete heat map analysis, visual heat map image, fixation sequence, recommendations

---

### 2. Specific Element Analysis (Circle What You Want)
```
"@Eye_Tracking_Analysis_Prompt.md

I've circled the [CTA button/headline/form] in this image. 
What percentage of attention will it get? Provide a Regions Report following 
the prompt framework. Also, generate a visual heat map image showing this region."

[Attach image with circled area]
```
**You'll get:** 
- Exact attention % for your circled area
- Outline color (🔴 Red >70%, 🟡 Yellow 40-69%, 🔵 Blue <40%)
- Visual heat map image with your circled region highlighted
- Detailed analysis with recommendations

---

### 3. Compare Multiple Elements
```
"@Eye_Tracking_Analysis_Prompt.md

I've marked 3 areas:
1. [Element A]
2. [Element B]  
3. [Element C]

Following the prompt framework, calculate attention % for each and rank them.
Generate a visual heat map image showing all marked regions."

[Attach image with marked areas]
```
**You'll get:** Comparison of all marked areas with rankings, visual heat map image

---

### 4. A/B Test Prediction
```
"@Eye_Tracking_Analysis_Prompt.md

Which design will perform better? Following the prompt framework, generate 
heat map analysis and sequence report for both variants. Create visual heat 
map images for both."

[Attach 2 images]
```
**You'll get:** Side-by-side comparison with predicted winner, visual heat map images for both variants

---

### 5. Quick Check
```
"Will users notice the [specific element]?"
```
**You'll get:** Yes/No with probability % and reasoning

---

## Understanding the Color Legend

Every report includes this standard legend:

```
🔴 RED (70-99%):    HIGH attention - Most viewers WILL look here
🟡 YELLOW (40-69%):  MEDIUM attention - Many viewers will look here
🔵 BLUE (20-39%):    LOW attention - Some viewers will look here
⚫ DARK (1-19%):     MINIMAL attention - Few viewers will look here
```

### What It Means:
- **Red zone** = Success! Element is highly visible
- **Yellow zone** = Moderate - Could be improved
- **Blue zone** = Weak - Likely to be missed
- **Dark/ignored** = Problem! Users won't see this

---

## Key Metrics Explained

### Probability (%)
Likelihood that viewers will look at this region **within the first 3-5 seconds** (first-glance vision)
- **70-99%** = 🔴 RED zone - Most viewers will look here
- **40-69%** = 🟡 YELLOW zone - Many viewers will look here
- **20-39%** = 🔵 BLUE zone - Some viewers will look here
- **<20%** = ⚫ IGNORED - Few viewers will look here

**Note:** Each element has an independent probability (0-100%). Color zones (RED/YELLOW/BLUE) are based on probability, NOT attention score.

### Attention Score (%)
What percent of **total page attention** this element gets during first-glance vision
- **>20%** = Dominant element
- **10-20%** = Strong presence  
- **5-10%** = Noticeable
- **<5%** = Easily missed

**Note:** All elements' attention scores sum to ~100%. This is different from probability - an element can have 54% probability (54 out of 100 viewers look) but only 14% attention score (14% of total page attention).

### ROC Score (0.00-1.00)
How accurately we can predict fixations here
- **>0.75** = High confidence prediction (very predictable)
- **0.50-0.75** = Moderate confidence (somewhat predictable)
- **<0.50** = Low confidence (unpredictable, high variability)

**Note:** Higher ROC scores indicate more consistent attention patterns across viewers. Lower ROC scores indicate higher individual variation (some users notice, others don't).

### Key Distinction
- **Probability:** How many viewers will look (0-100% for each element independently)
- **Attention Score:** What % of total page attention this element gets (all elements sum to ~100%)

---

## Pro Tips

### Tip 1: Circle Specific Areas
Instead of: "Analyze this landing page"
**Better:** "I've circled the CTA button - what % attention will it get?"

### Tip 2: Ask for Comparisons
"Which gets more attention - the headline or the image?"

### Tip 3: Request Specific Reports
- "Include Regions Report" = Get AOI analysis
- "Include Sequence Report" = Get numbered fixations (①②③④)
- "Include heat map legend" = Get full color scale explanation

### Tip 4: Test Before Building
Upload wireframes or mockups BEFORE development to validate design decisions

### Tip 5: Use for A/B Tests
Test design variants before spending on real A/B testing

---

## Common Questions

**Q: Can I draw on the image before uploading?**
Yes! Circle, highlight, or draw boxes around areas you want analyzed.

**Q: What file types work?**
JPG, PNG, WebP - anything the AI vision model accepts

**Q: How accurate is this?**
85-90% as accurate as real eye-tracking for first-glance (0-5 seconds)

**Q: Does it work for mobile apps?**
Yes! Works for web, mobile, print, packaging, billboards, etc.

**Q: Can I analyze videos?**
Yes, but analyze key frames separately

**Q: How much does it cost?**
Just AI API costs (~$0.01-0.10 per analysis vs. $3,000-10,000 for real eye-tracking)

---

## Example Workflows

### UX Designer Workflow
1. Create wireframe/mockup
2. Upload to AI with prompt: "Generate heat map analysis"
3. Check if primary CTA gets >70% probability (RED zone)
4. If not, iterate design based on recommendations
5. Re-test until CTA reaches RED zone (70-99% probability)

### Marketer Workflow
1. Upload landing page screenshot
2. Circle: headline, CTA, hero image
3. Ask: "Calculate attention % for each circled region"
4. Get Regions Report with rankings
5. Optimize lowest-performing element
6. A/B test the change

### Product Manager Workflow
1. Upload 2 design variants
2. Ask: "Which design will have better conversion?"
3. Get ROC comparison and confidence level
4. Choose winning variant
5. Validate with real A/B test

---

## Report Sections You'll Receive

### 1. Heat Map Analysis (Always Included)
- Full color legend
- Zone-by-zone breakdown
- Attention percentages
- Visual features explanation

### 2. Regions Report (If You Circle Areas)
- **Probability** for each region (% of viewers who will look within first 3-5 seconds)
- **Attention Score** for each region (% of total page attention)
- Outline color assignment (based on probability: RED 70-99%, YELLOW 40-69%, BLUE 20-39%)
- Ranking vs. other elements
- Specific recommendations

### 3. Sequence Report (Always Included)
- First 4 fixation points (①②③④)
- Timing for each fixation
- Scan pattern (F-pattern, Z-pattern, etc.)
- Explanation for sequence

### 4. Executive Summary (Always Included)
- Overall performance score (0-100)
- Primary attention focus
- Critical findings
- Key metrics

### 5. Recommendations (Always Included)
- What works (keep it)
- What needs improvement (optimize)
- Critical issues (must fix)
- Expected impact of changes

---

## Generating Visual Heat Map Images

Generate professional heat map images automatically using Spectral Residual saliency analysis:

### Automated Workflow (v3.0):

**Step 1: Run Saliency Analysis**
```bash
python Eye_Tracking_Analysis_Instruction/generate_saliency_analysis.py your_screenshot.png
```

This automatically generates:
- `heatmap_output.jpg` - Visual heatmap overlay with JET colormap
- `saliency_metrics.json` - Calculated metrics (Clarity Score, Confidence Level, Attention Share)
- `heatmap_legend.png` - Color scale legend (automatically copied)

**Step 2: (Optional) Add Goal Boxes for Attention Share**
If you want to measure attention share for specific UI elements:
1. Create `goal_boxes.json` with bounding boxes for regions of interest
2. Re-run with goal boxes:
```bash
python Eye_Tracking_Analysis_Instruction/generate_saliency_analysis.py your_screenshot.png --goal-boxes goal_boxes.json
```

📖 **Detailed workflow guide**: See `HEATMAP_WORKFLOW_GUIDE.md`

💡 **Example to learn from**: Check out `Freckle_Example/` folder for a complete working example!

---

## Need Help?

- **Full documentation**: See `README.md`
- **Complete prompt**: See `Eye_Tracking_Analysis_Prompt.md`
- **Heat map generation**: See `HEATMAP_WORKFLOW_GUIDE.md` and `HEATMAP_GENERATION_CHECKLIST.md`
- **Scientific basis**: See `3MVAS_Article`

---

**Ready to start?** 
1. Reference `@Eye_Tracking_Analysis_Prompt.md` in your chat (or upload it)
2. Attach your image
3. Get professional eye-tracking insights in seconds!

