# Wiki Format

`./wiki/` is a Karpathy-style LLM wiki layer (see [Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) — a persistent, incrementally-maintained knowledge artifact, distinct from `TOPIC-GRAPH.json`:

| | TOPIC-GRAPH.json | wiki/ |
|---|---|---|
| Granularity | module (whole lesson) | entity/concept |
| Answers | "what order did I learn things in, and why" | "what do I know about X, everywhere it appears" |
| Edges | prerequisite / question-spawned / appendix / merge | free-text `[[wikilinks]]` inside page bodies |

Both are maintained in parallel; neither replaces the other.

## Three-layer architecture (ported from Karpathy's gist)

1. **Raw sources (immutable)**: `../modules/**/*.html` — the wiki never edits these, only reads and synthesizes from them
2. **The wiki (maintained layer)**: this directory — LLM-generated markdown, created/updated/cross-referenced as new modules arrive
3. **The schema (configuration)**: `wiki/WIKI.md` — the workspace-local conventions doc (create it once, first time `wiki/` is built; see template below)

## Page schema

One file per entity/concept, kebab-case slug, e.g. `wiki/byzantine-empire.md`:

```markdown
---
title: Entity Name
aliases: [alt-name-1, alt-name-2]
appears_in: ["0002", "0004", "E3"]   # module ids that mention this entity
updated: YYYY-MM-DD
---

# Title

**One line**: single-sentence summary of what this is and why it matters in this workspace's context.

## Key facts (or Structure / Why it matters — whatever section shape fits the entity)
- bullet list of the key facts, each grounded in a specific module

## Related
[[other-entity-slug]] · [[another-entity-slug]]
```

Use `[[slug]]` for a plain link (label = other page's title) or `[[slug|custom label]]` for inline links inside prose (e.g. `[[crusades|First Crusade]]`).

## Operations

- **Ingest** (runs as SKILL.md Explore Mode step 5, every module): scan the just-written module for entities that (a) are new and worth their own page, or (b) already have a page and just gained a new mention/fact. For (a), create the page. For (b), append the module id to `appears_in` and merge in new facts — don't just overwrite, preserve what's still true. Then **backfill**: check whether any *existing* pages should now cross-reference the new/updated page in their own "Related" section, and add those links. This backfill step is the one most likely to be skipped — skipping it is how wikis rot into disconnected islands. Ingest is not done until the viewer (below) has also been regenerated from the updated `./wiki/` — the two happen together, same turn.
- **Query**: when the user asks "what do we know about X" or similar, read `wiki/<slug>.md` directly rather than re-deriving from modules.
- **Lint** (do periodically, or when asked): scan for orphan pages (nothing links to them — add links or fold them into a related page), `appears_in` entries pointing at module ids that no longer exist, and factual contradictions between pages that reference the same event — flag these to the user, don't silently resolve.

## `wiki/index.md`

Human-skimmable index, grouped by theme (not alphabetical) — regenerate the grouping whenever new pages are added:

```markdown
# Wiki Index — <topic>

## <Theme group 1>
- [[slug-a]] — one-line gloss
- [[slug-b]] — one-line gloss

## High-connectivity nodes
List the 2-4 pages with the most inbound `[[links]]` — these are the reader's best entry points.
```

## `wiki/log.md`

Chronological append-only log, one entry per ingest batch:

```markdown
## YYYY-MM-DD — <what triggered this update, e.g. module 0006 written>
New pages: `slug-a`, `slug-b`
Updated: `slug-c` (appears_in += 0006)
```

## `wiki/WIKI.md`

A short workspace-local copy of "page schema + operations" (condensed from this file) so a future session/agent working in just this directory has the convention without needing the skill's reference docs. Write it once when `wiki/` is first created; update only if this workspace's conventions genuinely diverge from the skill defaults.

## The interactive viewer

`templates/wiki-viewer.html` is a self-contained, dependency-free HTML template (reader mode with clickable `[[wikilinks]]` + a canvas-based force-directed graph mode) that embeds wiki content as an inline JS `PAGES` object — it does not fetch the `.md` files at runtime, so it must be regenerated from the current `wiki/` contents whenever you want an up-to-date interactive copy.

**When to regenerate**: automatically, in the same turn as any module whose ingest touched `./wiki/` (SKILL.md Explore Mode step 5) — not on request, not batched. A module that added or updated a wiki page and left the viewer stale is an unfinished step, the same way writing a module without updating `TOPIC-GRAPH.json` would be. Skip regeneration only when ingest itself was skipped (the module introduced no reusable entity).

**Regeneration procedure**:
1. Copy `templates/wiki-viewer.html` to `<workspace>/wiki-viewer.html` (or the deployed site's wiki route, see below) if it doesn't exist yet, or open the existing generated copy
2. Replace the `PAGES` object with one entry per current `wiki/*.md` file — `title`, `aliases`, `appears_in`, and `body` (body = the markdown after the frontmatter, verbatim, since the template's mini markdown renderer handles `##`, `**bold**`, lists, `` `code` ``, and `[[wikilinks]]`)
3. Replace the `GROUPS` array with the current theme grouping from `wiki/index.md`
4. Replace `NODES` (one entry per page: `id`, `en`, `category`, `desc` — `desc` reuses the page's "One line" summary; `category` picks whichever handful of buckets fit this workspace and drives the Linear/Chronological lane view, update `CATEGORY_ORDER` in the script to match) and `EDGES` (`[fromId, toId, type, weight]`, `type` = `'direct'` if the two pages link to each other, `'thematic'` if only one links to the other) — these power the graph view's tooltip, side panel, degree-tier coloring, and hub sizing, and must be kept in sync with the actual `[[wikilinks]]` inside `PAGES` bodies
5. Replace `MODULE_URLS` with the current mapping from module id → deployed lesson URL
6. Leave the rendering/graph-physics JS, `HUB_THRESHOLD`, `DEGREE_TIERS`, and `LABEL_THRESHOLD` untouched unless the user has asked for a redesign of the viewer itself (a separate, occasional task from a data resync)

## Mobile support (built in — do not re-derive per workspace)

The template already handles small screens: the reader sidebar becomes a slide-in drawer behind a hamburger button, the graph's side panel becomes a bottom sheet instead of a right-hand rail, and the canvas uses a real multi-touch engine (pinch-to-zoom, single-finger pan, tap-to-select decided by total displacement so touch jitter doesn't get mistaken for a drag) instead of mouse-only pointer handling. This is part of the base template — don't reintroduce mouse-only interaction or a fixed-width sidebar when instantiating for a new workspace.

The graph-only controls (Force/Linear layout, label density) live behind a single "⚙ Settings" toggle button rather than being permanently visible — they open a small dropdown panel, default to closed, and the whole `#graph-controls` block (gear + tier-chip legend) is hidden entirely while in reader view since those controls don't apply there. Keep control labels short and single-language (e.g. `Network`/`Chronological`, `All`/`3+`) — no bilingual duplication in one label. The reader/graph view toggle itself is the only control that's always visible regardless of view.

## UI language

The shipped template's chrome (nav labels, the settings panel, tooltip layout, button text) is written in English by default. This is **not** a fixed convention, though — when instantiating for a new workspace, write all UI copy in whatever language the user has been communicating in during the session; infer this from the conversation rather than asking, unless it's genuinely ambiguous (e.g. the user has been switching languages, or explicitly wants a bilingual audience). This applies to labels/buttons/panel headings, not to `PAGES` body content, which already follows the user's language naturally since it's authored during Explore Mode. It's easy to get this wrong by only swapping data (`PAGES`/`NODES`/`GROUPS`) and forgetting the surrounding template strings are still in the original template's language — check both.

## Keeping wiki pages light without dead-ending the reader

Wiki pages are deliberately thin — a one-line synthesis + a handful of bullets, not a rewrite of the module. That's the point (Karpathy's wiki is a compressed index, not a duplicate corpus) but it means a page can feel too thin on its own. Don't solve this by padding pages with content copied from the module — solve it by linking out: every page's `appears_in` module ids render as clickable pills (in both the reader view and the graph's side panel) pointing at `MODULE_URLS[id]`, so a reader who wants more just clicks through to the full original lesson. Keep pages light; make the door to "more" one click away instead.

**Where the regenerated copy lives**: if the workspace deploys a static site (modules published via Vercel or similar, same convention as `../modules/`), the viewer ships as part of that same site — at the deploy root or a dedicated route (e.g. `wiki-viewer.html` or `wiki/index.html`), linked from the site's lesson-index nav — not left sitting only in `./outputs/`. If the workspace has no deploy pipeline, `./outputs/wiki-viewer.html` (or published as an Artifact for the user to click through) is fine.
