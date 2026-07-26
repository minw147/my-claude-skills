# Workspace Layout

Current directory = workspace for one topic (same convention as `/teach`). Create dirs lazily — only when the first file of that kind is written. The tree below differs by mode — see `MISSION.md`'s `## Mode` field and SKILL.md's "Two modes" section.

## Learn Mode

```
<workspace>/
├── MISSION.md              # why exploring this topic, Mode: Learn, + optional output-intent note
├── RESOURCES.md            # trusted sources — knowledge/wisdom, per teach's format
├── NOTES.md                # scratchpad, user preferences
├── GLOSSARY.md             # canonical terminology, see GLOSSARY-FORMAT.md
├── SERIES.md               # optional — only if producing an ongoing series of artifacts, see SERIES-FORMAT.md
├── learning-style.md       # free-observation record, see LEARNING-STYLE-FORMAT.md
├── TOPIC-GRAPH.json        # source of truth: nodes + edges, see TOPIC-GRAPH-FORMAT.md
├── TOPIC-GRAPH.md          # auto-generated human-readable view — never hand-edit
├── modules/                # 0001-<slug>.html, one file = one graph node, no exceptions
├── images/                 # concept illustrations, ai-multimodal-generated — only where they earn their place, not one per module by default
├── highlights/             # CONFIRMED highlights only (candidates live only in AI's working notes until Create Mode surfaces them)
├── outputs/                # <slug>-structure.html (structural draft, see WRITING-DISCIPLINE.md) + finished artifacts: short-video-script, blog-post, long-video-script, essay, presentation-outline instances — each calibrated to a specific audience, see AUDIENCE-CALIBRATION.md
├── learning-records/       # 0001-<slug>.md, non-obvious understanding/prior-knowledge records
├── reference/              # compressed cheat-sheets referenced across modules
└── wiki/                   # Karpathy-style LLM wiki — entity pages + index.md + log.md + WIKI.md conventions, see WIKI-FORMAT.md
```

If the workspace deploys a static site (modules published via Vercel or similar), the generated wiki viewer HTML lives at the site root or a dedicated route (e.g. `wiki-viewer.html` or `wiki/index.html` at deploy root) — not buried in `./outputs/` — so it ships in the same deploy and is linked from the site nav.

## Explain Mode

No modules, no images-by-default, no wiki, no topic graph, no learning-style/learning-records — there's no *personal* knowledge state being built, since the user already knows the material. Much leaner:

```
<workspace>/
├── MISSION.md              # why this topic, Mode: Explain, + optional output-intent note
├── RESOURCES.md            # trusted sources backing claims made during clarification
├── NOTES.md                # scratchpad — use this if a long session risks losing thread; not a full transcript
├── GLOSSARY.md             # canonical terminology, gated differently than Learn Mode — see GLOSSARY-FORMAT.md
├── SERIES.md               # optional, but doubles as the persisted audience-knowledge record across a multi-piece series (this mode's equivalent of learning-records/) — see SERIES-FORMAT.md
├── highlights/             # CONFIRMED highlights only, same rules as Learn Mode
└── outputs/                # <slug>-structure.html + finished artifacts, same as Learn Mode
```

The audience's assumed knowledge state (baseline + cumulative) lives in the conversation and `references/ZPD-ENGINE.md`'s mechanics, not in a file.

## Rules ported unchanged from `/teach`

- **One mission per workspace.** Two unrelated topics = two workspaces (two directories).
- **Never trust parametric knowledge.** Populate `RESOURCES.md` before writing modules or drafting artifacts that make factual claims. This is *stricter* here than in `/teach`, not looser — output is meant to be published, so errors have real reputational cost.
- **ZPD calibration, every step, actively** — not a rule applied once at workspace setup. Learn Mode: read `learning-records/` and `learning-style.md` before picking what to teach next. Explain Mode: track baseline + cumulative audience state. See `references/ZPD-ENGINE.md`.
- **Learning records** (Learn Mode only) capture genuine demonstrated understanding, disclosed prior knowledge, corrected misconceptions, or mission shifts — not a session log. Numbered `0001-<slug>.md` in `learning-records/`.

## What's new vs `/teach`

`highlights/`, `outputs/` (including its `-structure.html` structural-draft convention, see `references/WRITING-DISCIPLINE.md`), `SERIES.md`, `GLOSSARY.md`'s dual-mode gating, `TOPIC-GRAPH.json` + `.md`, `wiki/`, and the Explain Mode track itself don't exist in `/teach` — see `CONTEXT.md` for what each term means and `docs/adr/` for why they're shaped this way.
