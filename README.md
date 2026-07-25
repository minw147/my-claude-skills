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
- **[eye-tracking-analysis](ux-research/eye-tracking-analysis)** — predicts visual attention on a screenshot or URL in the first 3-5 seconds using Spectral Residual Saliency (heatmaps, clarity scores, fixation sequences, attention-share reports). Demo: [heatmap.mintleafux.com](https://heatmap.mintleafux.com/)
- **[pendo-code-block](ux-research/pendo-code-block)** — build and debug custom Pendo Guide Code Blocks (pendo.track() sandbox errors, guides stuck loading, multi-step auto-advance, drag-and-drop bugs).

### `content-creation/`
- **[learn-and-tell](content-creation/learn-and-tell)** — guides problem-posing-driven exploration of a topic, then turns confirmed highlights into a publishable artifact (video script, blog post, essay, presentation outline) calibrated to a specific audience.

## Adding a Skill

1. Pick (or create) a category folder at the repo root.
2. Add `<category>/<skill-name>/SKILL.md` with `name` and `description` frontmatter, plus instructions.
3. Drop in any `scripts/`, `references/`, `assets/` the skill needs.
4. Update the skill list above.

## Using These Skills

Point your Claude Code / Claude setup at `<category>/<skill-name>/` (or the whole repo) as a skills directory — no build or sync step required.

### Install/update via npx

From any project directory, install every skill into that project's `.claude/skills/`:

```bash
npx github:minw147/my-claude-skills
```

Install/update only specific skills or categories:

```bash
npx github:minw147/my-claude-skills eye-tracking-analysis pendo-code-block
npx github:minw147/my-claude-skills ux-research
```

Re-run the same command any time to pull the latest version — it overwrites the matching skill folders in place. Note: this repo is currently **private**, so `npx github:...` only works for accounts with access to it (via `git`'s normal auth) — make the repo public if you want others outside your account to run it.

---

**License:** Personal use
