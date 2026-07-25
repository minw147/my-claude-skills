# My Claude Skills

A personal repository of Claude skills, organized by category. Each skill is a self-contained folder with a `SKILL.md` (instructions Claude reads) plus any supporting `scripts/`, `references/`, or `assets/`.

## Structure

```
<category>/
└── <skill-name>/
    ├── SKILL.md        # required — name, description, instructions
    ├── scripts/        # optional — helper code the skill runs
    ├── references/      # optional — docs the skill reads as needed
    └── assets/          # optional — templates, images, etc.
```

Categories group related skills together (e.g. `ux-research/` for skills that research, test, or evaluate how users perceive and interact with interfaces — as opposed to skills that build or design interfaces). Create a new category folder whenever a skill doesn't fit an existing one.

## Skills

### `ux-research/`
- **[eye-tracking-analysis](ux-research/eye-tracking-analysis)** — predicts visual attention on a screenshot or URL in the first 3-5 seconds using Spectral Residual Saliency (heatmaps, clarity scores, fixation sequences, attention-share reports).

## Adding a Skill

1. Pick (or create) a category folder at the repo root.
2. Add `<category>/<skill-name>/SKILL.md` with `name` and `description` frontmatter, plus instructions.
3. Drop in any `scripts/`, `references/`, `assets/` the skill needs.
4. Update the skill list above.

## Using These Skills

Point your Claude Code / Claude setup at `<category>/<skill-name>/` (or the whole repo) as a skills directory — no build or sync step required.

---

**License:** Personal use
