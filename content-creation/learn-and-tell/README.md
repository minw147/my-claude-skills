# learn-and-tell

A Claude Code skill for content creators: explore a topic through **problem-posing driven learning**, then turn what you actually discovered into a publishable artifact — video script, blog post, essay, or presentation outline. Learning is the means; a real artifact — with your own thinking in it — is the end.

Not a tutor. The AI never quizzes or scores you — you pose the questions, and they decide where the exploration goes next. Every output artifact is calibrated to a specific audience (a Medium essay and a conference talk drawn from the same exploration need different depth, jargon, and framing), and everything in it has to trace back to what was actually established during exploration — the same "never trust parametric knowledge" discipline that governs the learning modules also governs the final artifact, since it's still teaching someone, just a different audience.

See `BRAINSTORM.md` for the full design rationale, `CONTEXT.md` for the glossary of terms this skill uses, and `docs/adr/` for the specific trade-offs behind how it's built.

## Install

```bash
npx github:minw147/learn-and-tell
```

Installs to `~/.claude/skills/learn-and-tell` (available in every project) by default. Only `SKILL.md`, `references/`, and `templates/` are installed — the dev-only design docs (`BRAINSTORM.md`, `CONTEXT.md`, `docs/adr/`) stay in this repo, not in your skills directory.

Options:
- `--local` — install to `./.claude/skills/learn-and-tell` (this project only) instead of the user-level directory
- `--dir=<path>` — install to a custom directory
- `--force` / `-f` — overwrite an existing install

## Usage

```
cd <your-topic-directory>
```

Then invoke the skill and say what you want to explore. Everything — mission, modules, the question graph, the wiki, highlights, and produced artifacts — lives in that directory. See `references/WORKSPACE-LAYOUT.md` for the full file tree, and `SKILL.md` for the two-mode loop (Explore / Create).

## Producing an artifact

Create Mode is triggered explicitly — say what you want ("turn this into a blog post", "help me prepare a conference talk") and it kicks in; it never switches on its own. Five output shapes are supported out of the box: short video script, blog post, long video script, essay (Medium-style), and presentation outline (slides + speaker notes) — see `templates/`. Before drafting, the skill asks who the piece is actually for, since that audience's own background — not yours — determines how much foundational context to include, how dense the jargon can be, and what tone fits. See `references/AUDIENCE-CALIBRATION.md` and `references/OUTPUT-TEMPLATES-GUIDE.md`.

## The wiki layer

Alongside `TOPIC-GRAPH.json` (module-level: what order things were learned, and why), every workspace also maintains `./wiki/` — a [Karpathy-style LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) of entity/concept pages, cross-referenced via `[[wikilinks]]`, synthesized incrementally from whatever modules mention that entity. See `references/WIKI-FORMAT.md` and `docs/adr/0010-wiki-layer-is-separate-from-topic-graph.md`.

The wiki also ships with a self-contained, dependency-free interactive viewer (`templates/wiki-viewer.html`) — a reader mode with clickable wikilinks and a canvas-based force-directed graph mode (degree-tier coloring, Force/Linear layout toggle, mobile touch support).

## Credit

learn-and-tell is a deliberate adaptation, not an original invention, of three sources:

**Teaching methodology and workspace conventions** — forked in spirit from the `/teach` skill:
- Original prompt concept: Suzanne (Anthropic), shared via [@trq212](https://twitter.com/trq212)
- Packaged as `/teach`: [Matt Pocock — mattpocock/skills](https://github.com/mattpocock/skills) (MIT License)
- Tutorial: https://www.aihero.dev/learn-anything-with-my-teach-skill
- Collected into: [alexknowshtml/claude-skills](https://github.com/alexknowshtml/claude-skills)

learn-and-tell adapts `/teach`'s workspace-as-directory convention, mission-driven grounding, ZPD calibration, and "never trust parametric knowledge" sourcing discipline, then extends it for a content-creator use case: problem-posing instead of quizzing, a non-linear Question-Annotated Topic Graph instead of a linear lesson sequence, and a Create Mode that turns confirmed highlights into publishable artifacts. It's packaged using Claude Code's `SKILL.md` conventions (frontmatter, invocation) rather than Hermes's — a distribution choice, not a restriction; the instructions themselves are plain markdown and could be adapted to Hermes, Cursor, or any other tool that reads project-level agent instructions. See `docs/adr/0009-claude-code-skill-not-hermes.md`.

**The wiki layer** — the `./wiki/` directory and its ingest/query/lint operations are a direct application of [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): raw sources stay immutable, an LLM incrementally maintains a persistent cross-referenced knowledge layer on top of them, and upkeep cost stays near zero because the LLM (not a human) does the bookkeeping. See `references/WIKI-FORMAT.md` and `docs/adr/0010-wiki-layer-is-separate-from-topic-graph.md` for how it's adapted here (entity pages instead of general notes, `[[wikilinks]]` back to the specific modules that ground each claim).

**"Every concept gets an illustration"** — inspired by [openflipbook (eren23/openflipbook)](https://github.com/eren23/openflipbook) (MIT License), an open-source clone of flipbook.page's infinite-canvas experience. Only the illustration principle is borrowed (via the `ai-multimodal` skill) — no openflipbook code or infrastructure is used.

## License

MIT — see `LICENSE`. Per the terms above, this is a derivative work; the original copyright notices for `/teach` (Matt Pocock) are preserved in spirit through this credit section, as required by MIT's attribution clause.
