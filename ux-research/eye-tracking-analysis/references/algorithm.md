# Algorithm: Spectral Residual Saliency

Condensed from the full technical explanation at [heatmap.mintleafux.com/SPECTRAL_RESIDUAL_EXPLANATION.html](https://heatmap.mintleafux.com/SPECTRAL_RESIDUAL_EXPLANATION.html) — read that for the full derivation, limitations, and related-work citations.

## The Big Idea

Predicts where eyes go first (0-5 seconds) by finding what stands out from the background — mimicking early, pre-attentive visual processing (detecting anomalies, not recognizing objects).

## How It Works

1. **Grayscale**: `I(x,y) = 0.299R + 0.587G + 0.114B` — isolates luminance, the primary driver of early attention.
2. **FFT**: transform to the frequency domain, `F(u,v) = FFT[I(x,y)]`. Separates repetitive patterns (low frequency = background) from unique features (high frequency = edges, text, objects).
3. **Log spectrum**: `L(u,v) = log(|F(u,v)|)` — compresses dynamic range.
4. **Spectral residual** (the key step): `R(u,v) = L(u,v) - h_n(u,v)*L(u,v)` — subtract a smoothed version of the log spectrum from itself. Common/repetitive patterns cancel out; what remains is what's unusual, which is what draws attention.
5. **Inverse FFT**: `S(x,y) = |IFFT[exp(R(u,v) + i·P(u,v))]|²` (using the original phase `P` to preserve spatial layout) — back to pixel space as a saliency map.
6. **Normalize** to 0-255 for the heatmap.

**Concretely**: a uniform red background is a repetitive (low-frequency) pattern that gets filtered out; white text on it creates sharp edges (high-frequency) that survive the residual step and get high saliency — matching where people actually look.

## Attention Share Math

```
attention_share (%) = (sum of saliency values in region / sum of all saliency values in image) × 100
```

All regions' shares sum to 100% of the image — this is what makes cross-region comparison valid (e.g. "the CTA gets 3x the attention share of the nav menu").

## Enhancements Beyond the Base Algorithm

These are added on top of vanilla Spectral Residual, implemented in `scripts/generate_saliency_analysis.py`:

- **Face detection boost**: `S_face = 0.7×S_original + 0.3×255` — faces get a 30% saliency boost (OpenCV Haar Cascade), since humans are biologically drawn to faces regardless of raw visual contrast.
- **Clarity Score**: `(1 - mean_saliency/max_saliency) × 100` — a proprietary metric not in the original paper. If mean saliency is close to max, attention is smeared everywhere (cluttered); if mean is much lower than max, there's one clear focal point (focused). See band interpretation in `references/report-format.md`.
- **Automatic zone detection**: contour + morphological operations to segment red/yellow/blue attention zones without manual region marking.
- **AI-powered element identification**: vision-based semantic naming of detected zones (e.g. "CTA Button" instead of raw coordinates) — see `references/workflow.md` Step 3.

## Limitations

Predicts bottom-up, initial attention only:
- ✅ First 0-5 seconds, contrast/edges/faces, where eyes land first
- ❌ Task-driven / top-down attention (after users form a goal)
- ❌ Semantic importance of small-but-critical elements (e.g. an error message)
- ❌ Extended viewing behavior beyond ~5 seconds

This predicts where users **look**, not what they **think** or **understand**.

## Citation

Original method:

> Hou, X., & Zhang, L. (2007). Saliency Detection: A Spectral Residual Approach. *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2007, pp. 1-8.

```bibtex
@inproceedings{hou2007saliency,
  title={Saliency Detection: A Spectral Residual Approach},
  author={Hou, Xiaodi and Zhang, Liqing},
  booktitle={IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2007},
  pages={1-8}
}
```

Implemented via OpenCV: `cv2.saliency.StaticSaliencySpectralResidual_create()` (requires `opencv-contrib-python`). Validated against the MIT Saliency Benchmark (MIT300/MIT1003), ~85-90% correlation with real eye-tracking fixation data.
