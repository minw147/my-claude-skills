# Writing Discipline

Ported from `/teach`'s lesson-writing principles, which currently only govern `./modules/*.html` — this file extends the same discipline to **everything drafted in Create Phase**, in both modes. This exists because going straight from raw material (highlights, conversation) to flowing prose (a blog post, a video script) skips the structural discipline that makes modules read well, and that gap is a real source of generic, "AI-flavored" output.

## What made the modules good, restated as rules

- **Tufte-style clarity.** Clean typography, generous whitespace, one idea visually separated from the next — never a wall of undifferentiated paragraphs.
- **One clear point per chunk.** Each visual block (`.key-point`, `.analogy-box`, etc. in `templates/module-template.html`) carries exactly one idea. If a chunk is doing two jobs, split it.
- **Explicit bridges, not implied adjacency.** A `.bridge` block states *why* the next chunk follows from this one. Two paragraphs that are merely next to each other, with the connection left for the reader to infer, is exactly the failure mode this prevents — and exactly what's easy to lose when editing flowing prose (see "Structural draft first" below).
- **Concrete over generic.** A point grounded in a specific example, number, or quote beats a general statement restating the same idea abstractly. This is also the single biggest lever against sounding AI-written — generic, hedge-everything, could-apply-to-any-topic phrasing is the tell.
- **Cite as you go.** Every claim traces to `RESOURCES.md`, a confirmed highlight, or the conversation itself (already a hard rule — see SKILL.md Create Phase) — but it's restated here because ungrounded claims are also usually the genericly-worded ones.

## Structural draft first (Create Phase, both modes)

Before drafting the actual requested format (blog post, video script, essay, presentation), **draft a structural version using `templates/module-template.html`** — chunked the same way a module is, with explicit bridges between chunks — representing this piece's content and order. This is not the deliverable; it's a checkpoint.

Why this order, specifically: structure and connective flow are easy to verify in a chunked, visually separated HTML document and easy to lose track of in flowing prose — especially after a few rounds of edits, where a paragraph moved or cut can silently break the transition into the next one without it being obvious on the page. Catching that in a wall of prose requires re-reading the whole thing closely; catching it in a chunked structural draft is closer to glancing at a table of contents.

1. **Draft the structural version**: one chunk per point, in argument order, each chunk a `.key-point`/`.analogy-box`/similar block, each transition an explicit `.bridge`. Save it alongside the eventual output, e.g. `./outputs/<slug>-structure.html`.
2. **The user reviews structure, not prose.** Reorder chunks, ask for a chunk to be split or merged, flag a weak or missing bridge — all easier to do here than after the piece is flowing prose.
3. **Only once the structure is approved**, generate the actual requested format from it — preserving the approved order and connective logic, translated into that format's own conventions (paragraph flow for a blog post, spoken pacing and shot suggestions for a video script, etc.). Don't restart from scratch in the target format; the structural draft *is* the outline being translated, not a discarded scratch step.
4. **Run a de-AI-flavor pass before saving the final artifact** — the `humanizer` skill, if available, is built exactly for this (inflated language, hedge-everything phrasing, generic connective tissue, other tells). Treat this as a required step before step 7 of Create Phase (save to `./outputs/`), not an optional polish.

This applies regardless of mode — Learn Mode's Create Phase artifacts (produced from confirmed highlights across modules) benefit from the same structural-draft-first discipline as Explain Mode's.
