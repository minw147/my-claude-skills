# Workspace Layout

Current directory = workspace for one topic (same convention as `/teach`). Create dirs lazily — only when the first file of that kind is written.

```
<workspace>/
├── MISSION.md              # why exploring this topic + optional output-intent note
├── RESOURCES.md            # trusted sources — knowledge/wisdom, per teach's format
├── NOTES.md                # scratchpad, user preferences
├── learning-style.md       # free-observation record, see LEARNING-STYLE-FORMAT.md
├── TOPIC-GRAPH.json        # source of truth: nodes + edges, see TOPIC-GRAPH-FORMAT.md
├── TOPIC-GRAPH.md          # auto-generated human-readable view — never hand-edit
├── modules/                # 0001-<slug>.html, one file = one graph node, no exceptions
├── images/                 # one concept illustration per module, ai-multimodal-generated
├── highlights/             # CONFIRMED highlights only (candidates live only in AI's working notes until Create Mode surfaces them)
├── outputs/                # finished artifacts: short-video-script, blog-post, long-video-script, essay, presentation-outline instances — each calibrated to a specific audience, see AUDIENCE-CALIBRATION.md
├── learning-records/       # 0001-<slug>.md, non-obvious understanding/prior-knowledge records
├── reference/              # compressed cheat-sheets/glossaries referenced across modules
└── wiki/                   # Karpathy-style LLM wiki — entity pages + index.md + log.md + WIKI.md conventions, see WIKI-FORMAT.md
```

If the workspace deploys a static site (modules published via Vercel or similar), the generated wiki viewer HTML lives at the site root or a dedicated route (e.g. `wiki-viewer.html` or `wiki/index.html` at deploy root) — not buried in `./outputs/` — so it ships in the same deploy and is linked from the site nav.

## Rules ported unchanged from `/teach`

- **One mission per workspace.** Two unrelated topics = two workspaces (two directories).
- **Never trust parametric knowledge.** Populate `RESOURCES.md` before writing modules that make factual claims; cite sources in modules. This is *stricter* here than in `/teach`, not looser — output is meant to be published, so errors have real reputational cost.
- **ZPD calibration.** Read `learning-records/` and `learning-style.md` before picking what to teach next; a module should always feel "just challenging enough."
- **Learning records** capture genuine demonstrated understanding, disclosed prior knowledge, corrected misconceptions, or mission shifts — not a session log. Numbered `0001-<slug>.md` in `learning-records/`.

## What's new vs `/teach`

`images/`, `highlights/`, `outputs/`, `learning-style.md`, `TOPIC-GRAPH.json` + `.md`, `wiki/` don't exist in `/teach` — see `CONTEXT.md` for what each term means and `docs/adr/` for why they're shaped this way.
