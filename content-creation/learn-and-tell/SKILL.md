---
name: learn-and-tell
description: Guide a content creator through problem-posing driven exploration of a topic, then turn confirmed highlights into a publishable artifact — video script, blog post, essay, or presentation outline — calibrated to a specific audience. Use when the user wants to explore a topic to eventually make content about it, or says things like "I want to learn X and turn it into a video/blog/article", "help me dig into a topic and then write a script/prepare a talk".
license: MIT (see LICENSE; forked in spirit from Matt Pocock's /teach skill, MIT)
---

Treat the current directory as the workspace for one topic. All state lives here — see `references/WORKSPACE-LAYOUT.md` for the full file tree.

This is **not a tutor**. The user drives what gets explored; the AI never quizzes or scores. It is a fork of Anthropic/Matt Pocock's `/teach` skill (MIT — credit in `README.md`), adapted for content creators: learning is the means, a publishable artifact is the end. The design rationale and decision history (glossary + ADRs) live in the source project at `D:\learn-and-tell\` (`CONTEXT.md`, `docs/adr/`) — consult those if unsure why a rule below exists before overriding it.

## Two modes, one pipeline

**Explore Mode** (default): the user has a topic, no fixed output yet. Generate modules, run problem-posing after each, follow curiosity.

**Create Mode**: entered ONLY when the user explicitly says so ("help me turn this into a video script"). Never auto-switch. If highlights + module density strongly suggest the material is ready, make **one** gentle proposal — if declined, drop it, don't repeat.

Both modes read/write the same `TOPIC-GRAPH.json`, `./highlights/`, `learning-style.md`, `./wiki/`.

## Explore Mode loop

1. **Mission**: if `MISSION.md` is missing, interview the user briefly — why this topic, and (lightly, non-committally) "do you have a produced-content goal in mind, or are you just exploring for now? either is fine". Use `references/MISSION-FORMAT.md`.
2. **Frame**: before the first module, propose a non-linear framework for the topic (parallel tracks, not a syllabus) — this is a first "wow" moment, don't skip it.
3. **Write a module**: one topic at a time, in `./modules/0001-<slug>.html`, using `templates/module-template.html`. Ground every claim in `RESOURCES.md` (see `references/RESOURCES-FORMAT.md`) — never rely on parametric memory for anything that could end up published. Generate one concept illustration per module via the `ai-multimodal` skill, save to `./images/`, embed it.
4. **Update the graph**: add/update the node and edges in `TOPIC-GRAPH.json`, regenerate `TOPIC-GRAPH.md`. See `references/TOPIC-GRAPH-FORMAT.md` — one node per module file, no exceptions, even for appendices.
5. **Update the wiki — automatically, every module, no prompting required**: ingest the module into `./wiki/` (new entity pages for anything that reappears or is likely to reappear across modules, `appears_in` backfilled on existing pages that got a new mention, cross-references added both ways), **then regenerate the interactive viewer** from `templates/wiki-viewer.html` (or the workspace's existing instantiated copy) so `PAGES`/`GROUPS`/`NODES`/`EDGES`/`MODULE_URLS` reflect the just-updated `./wiki/` contents. See `references/WIKI-FORMAT.md`. Skip silently for modules that introduce no reusable entity (e.g. pure review/drill modules) — but if the wiki *was* touched, the viewer regeneration is not optional or batched anymore; do it in the same turn as the module, without being asked. If the workspace deploys a static site (e.g. via Vercel, same convention as `./modules/`), the viewer belongs alongside the deployed lessons — not buried in `./outputs/` — and if this workspace already has an established "deploy after content changes" routine (e.g. documented in `NOTES.md`), run that same deploy now too so the live site stays in sync; otherwise leave the regenerated file ready and say so.
6. **Problem-posing**: ask the user what question or scenario this raises for them. Do not score it. Reflect it back (mirror, not judge) and let it decide what's next — main track, a new branch (`question-spawned` edge), or an appendix (`appendix` edge).
   - **If the user asks nothing**: mark a `no-question` signal on the node (positive, not negative). On repeated no-question streaks, check in: "you seem to have picked this up quickly — want to speed up, or go deeper?"
7. **Draft a candidate highlight** silently if this module produced a real aha moment — do not show this to the user yet. See `references/HIGHLIGHT-FORMAT.md`.
8. **Observe learning style**: after any module with signal (not every time), jot an observation in `learning-style.md` per `references/LEARNING-STYLE-FORMAT.md`. Never interview for this; only ever record what's observed.
9. Repeat from step 3, following the graph the user's questions are drawing.

## Create Mode loop

Triggered by explicit user request naming a format (short video / blog / long video / essay / presentation) or just "help me make something out of this".

1. **Calibrate audience — every artifact, not just once per workspace**: before anything else, establish who this specific piece is for — a Medium essay, a UXR conference talk, and a short video from the *same* exploration can have three different audiences. Ask directly if it's not obvious ("who is this for, and what do they already know? what part would be completely new to them?"); check `MISSION.md`'s output-intent note first in case it's already stated. This isn't a one-time workspace setting — recalibrate per artifact, since the same highlights can serve very different audiences. What's established here (who they are, what they already know, what tone/formality fits) is what "just challenging enough for the reader" (the audience's own ZPD, not the explorer's) actually means for this piece — see `references/AUDIENCE-CALIBRATION.md`. Record the calibration in the artifact's own header (see templates) rather than a separate persistent file.
2. **Surface candidates**: pull the silent candidate highlights relevant to what the user wants to produce, present them, let the user confirm/discard. Only confirmed ones get written to `./highlights/`.
3. **Judge fit, don't refuse**: assess whether the confirmed highlights + graph density can support the requested format for *this audience* (see `references/OUTPUT-TEMPLATES-GUIDE.md` — no numeric thresholds, judge like an editor). If it's thin for what they asked, don't just say no — offer to dig deeper on the current branch, or broaden which branches feed the piece.
4. **Fill gaps**: if producing the piece surfaces a knowledge gap, drop back into a short Explore Mode detour (a module) to fill it, then return.
5. **Draft the artifact** using the matching template (`templates/short-video-script.md`, `templates/blog-post.md`, `templates/long-video-script.md`, `templates/essay.md`, `templates/presentation-outline.md`), reusing `./images/` where they fit or regenerating at higher quality for publish use. Let the audience calibration from step 1 drive jargon density, how much foundational context to include, and structural formality — not just which template gets picked.
   - **Nothing gets introduced during drafting that wasn't already established during Explore Mode.** The artifact is teaching this audience, exactly as a module teaches the user — so the same "never trust parametric knowledge" discipline from `references/RESOURCES-FORMAT.md` applies here, not just to modules. Every claim in the draft must trace back to a module, a confirmed highlight, or `RESOURCES.md` — smoothing a transition or making an opening hook land is fine, inventing a supporting fact or example to make the narrative flow better is not. If the piece needs a claim that isn't already grounded, that's a knowledge gap — go back to step 4, don't just write it in.
6. **Save** the result to `./outputs/`, never just print it and discard.

## Files this skill reads/writes

See `references/WORKSPACE-LAYOUT.md` for the complete directory tree and root-file list (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `TOPIC-GRAPH.json`, `TOPIC-GRAPH.md`, `learning-style.md`, plus `./modules/`, `./highlights/`, `./outputs/`, `./images/`, `./learning-records/`, `./reference/`, `./wiki/`).

## The wiki layer (Karpathy-style LLM wiki)

`./wiki/` is a third layer alongside `TOPIC-GRAPH.json` and the modules — not a replacement for either. TOPIC-GRAPH tracks *learning order* (module-level, why X came before Y). The wiki tracks *knowledge itself* (entity/concept-level, cross-referenced via `[[wikilinks]]`, synthesized from whatever modules mention that entity). See `references/WIKI-FORMAT.md` for the page schema, the ingest/query/lint operations, and how to (re)generate the interactive viewer from `templates/wiki-viewer.html`.

Single-topic vs multi-topic directories: if the current directory has its own `MISSION.md`, treat it as one workspace and build one wiki. If it has no `MISSION.md` but contains subdirectories that each have one, treat each subdirectory as its own topic — build (or update) each one's `./wiki/` independently, then optionally generate one cross-topic index at the parent level linking into each topic's wiki viewer.

## Explicitly out of scope this phase

No openflipbook integration (Phase 2 — see `README.md`), no numeric problem-posing rubric shown to the user, no cross-workspace memory beyond this one topic's directory (except the explicit multi-topic wiki case above).
