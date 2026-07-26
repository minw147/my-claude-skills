---
name: learn-and-tell
description: Guide a content creator through problem-posing driven exploration of a topic — either learning it from scratch, or organizing knowledge they already have for an audience — then turn confirmed highlights into a publishable artifact (video script, blog post, essay, presentation outline) calibrated to a specific audience. Use when the user wants to explore a topic to eventually make content about it, wants help learning something new, or already knows a topic and wants help figuring out how to explain it clearly to others. Triggers include "I want to learn X and turn it into a video/blog/article", "help me dig into a topic and then write a script/prepare a talk", or "I know this stuff but I need help figuring out how to explain it."
license: MIT (see LICENSE; forked in spirit from Matt Pocock's /teach skill, MIT)
---

Treat the current directory as the workspace for one topic. All state lives here — see `references/WORKSPACE-LAYOUT.md` for the full file tree.

This is a fork of Anthropic/Matt Pocock's `/teach` skill (MIT — credit in `README.md`), adapted for content creators. The design rationale and decision history (glossary + ADRs) live in `CONTEXT.md` and `docs/adr/` — consult those if unsure why a rule below exists before overriding it.

## Two modes: Learn and Explain

Every workspace is one of these, chosen once at the mission interview (step 1 below) and recorded in `MISSION.md`:

**Learn Mode**: the user doesn't know the topic yet. They explore it, ask questions, build understanding — a publishable artifact is an optional eventual output, not the point of showing up. This is the direct descendant of `/teach`.

**Explain Mode**: the user already knows the topic — it's their own expertise, or something they've already worked out — and wants help figuring out how to explain it to someone who doesn't. This is not learning; the user isn't acquiring knowledge, they're organizing and pressure-testing knowledge they already have, from the perspective of the audience who'll eventually receive it.

The two modes share one pipeline shape — an **Explore phase** (accumulate material) followed by a **Create phase** (produce an artifact) — and share the ZPD engine, the highlights mechanism, `RESOURCES.md` grounding, and the glossary. What differs is **who poses the questions during Explore, and what gets maintained**:

| | Learn Mode | Explain Mode |
|---|---|---|
| Who asks questions during Explore | The user | The AI, playing the audience |
| ZPD is calculated for | The user (their own understanding) | The imagined audience (their assumed knowledge) |
| Explore phase produces | `./modules/*.html` files | A conversation (no files per exchange) |
| Wiki, `TOPIC-GRAPH.json`, `learning-style.md`, `learning-records/` | Yes | No — not applicable, nothing is being learned |
| Concept illustrations | AI decides per-module if one genuinely aids comprehension | Deferred to Create phase, as annotated suggestions on the draft |

Never auto-detect or silently switch modes. If it's ambiguous mid-session whether the user has drifted from one to the other, ask — don't guess. A mode can be revised the same way `MISSION.md`'s output-intent can (see `references/MISSION-FORMAT.md`), but that's a deliberate, confirmed change, not a silent pivot.

## Choosing a mode

1. **Mission**: if `MISSION.md` is missing, interview the user briefly:
   - Why this topic — what's pulling them toward it right now?
   - **Do you already know this, or are you here to learn it?** This is the mode question. If it's not obviously one or the other from how they framed the request, ask directly: "are you exploring this to learn it yourself, or do you already know it and want help figuring out how to explain it to someone else?"
   - Lightly, non-committally: "do you have a produced-content goal in mind, or are you just exploring for now? either is fine."
   - Use `references/MISSION-FORMAT.md`.
2. **Frame** (Learn Mode only): before the first module, propose a non-linear framework for the topic (parallel tracks, not a syllabus) — this is a first "wow" moment, don't skip it.
   **Explain Mode equivalent**: ask the user for the rough shape of what they want to communicate — their core thesis or argument, in their own words — then reflect back a proposed structure for the questioning session (which sub-parts of their explanation need pressure-testing) so they know what's coming. Don't invent a framework for territory the user already owns; ask for its shape first.

## The ZPD engine (shared by both modes)

Both modes run on the same underlying question: **what does this audience already know, and what's the single next thing that's "just challenging enough" to introduce?** — Vygotsky's Zone of Proximal Development, ported from `/teach`. What differs is whose knowledge state is being modeled. See `references/ZPD-ENGINE.md` for the full mechanics; summary:

- **Learn Mode**: the audience is the user. Their knowledge state comes from `learning-records/` (genuine demonstrated understanding) and `learning-style.md` (observed preferences) — read both before deciding what a module should cover next.
- **Explain Mode**: the audience is an imagined reader/viewer. Their knowledge state = an initial calibrated baseline (see `references/AUDIENCE-CALIBRATION.md`) **plus** everything already established in previously published pieces of this series, if any (see `references/SERIES-FORMAT.md`'s `Covered` entries — this is Explain Mode's equivalent of reading `learning-records/`) **plus** everything established so far in this session's conversation. Every explanation the user gives advances that cumulative state; the AI's job is to notice when the user's next point assumes something beyond it (a gap to surface) or redundantly re-explains something already covered (worth flagging, lower priority).

**Problem-posing quality, not correctness** (Learn Mode): there's no such thing as a wrong question, but there is such a thing as a low-yield one. A generative question builds a connection (to something covered earlier, to something outside this workspace) or opens the next module/branch. A procedural question is convergent, single-answer, and dead-ends immediately ("what year was X" with nothing following from the answer). Never tell the user their question was bad — that violates the mirror-not-judge stance (`docs/adr/0004`). Instead, model and nudge: reflect connective/generative framings back more often than you surface procedural ones, and if a module naturally raises a connective question the user hasn't voiced, you can surface it yourself as an option ("this also connects to X — want to follow that, or keep going on the main track?").

**The AI as questioner** (Explain Mode): this is the same generative-vs-procedural judgment, just inverted — the AI is now the one posing questions, playing the role of the audience (like the questioning half of a two-host format, where a good co-host's questions are the ones that unlock a sharper explanation and a bad one asks something nobody in the audience actually wondered). A good AI question in this mode probes exactly the gap between the calibrated baseline+cumulative state and what the user just said. A bad one is generic ("can you say more about that?") or asks about something already well-established. Judge your own questions by the same generative standard you're holding Learn Mode's problem-posing to.

## Explore Phase — Learn Mode (module loop)

1. **Write a module**: one topic at a time, in `./modules/0001-<slug>.html`, using `templates/module-template.html`. Ground every claim in `RESOURCES.md` (see `references/RESOURCES-FORMAT.md`) — never rely on parametric memory for anything that could end up published.
2. **Concept illustration — AI's judgment call, not automatic**: generate one via the `ai-multimodal` skill, save to `./images/`, embed it, **only when it substantively aids comprehension** — a process diagram, a map, a timeline that genuinely clarifies structure a reader/viewer couldn't hold in their head from prose alone. Skip it by default. An illustration added because "every module gets one" rather than because it earns its place is decoration, not a wow moment — don't add one you can't justify in one sentence.
3. **Update the graph**: add/update the node and edges in `TOPIC-GRAPH.json`, regenerate `TOPIC-GRAPH.md`. See `references/TOPIC-GRAPH-FORMAT.md` — one node per module file, no exceptions, even for appendices.
4. **Update the wiki — automatically, every module, no prompting required**: ingest the module into `./wiki/`, then regenerate the interactive viewer. See `references/WIKI-FORMAT.md`. Skip silently only for modules that introduce no reusable entity.
5. **Glossary**: if a term the user has now demonstrated understanding of (not merely been exposed to) is missing from the glossary, add it. See `references/GLOSSARY-FORMAT.md`.
6. **Problem-posing**: ask the user what question or scenario this raises for them. Do not score it, but nudge toward generative questions per the ZPD engine section above. Reflect it back (mirror, not judge) and let it decide what's next — main track, a new branch (`question-spawned` edge), or an appendix (`appendix` edge).
   - **If the user asks nothing**: that's fine, positive signal even — move on. Don't track or score the streak (no `signal`/`no_question_streak` field — see `docs/adr` for why this was simplified out).
7. **Draft a candidate highlight** silently if this module produced a real aha moment — do not show this to the user yet. See `references/HIGHLIGHT-FORMAT.md`.
8. **Observe learning style**: after any module with signal (not every time), jot an observation in `learning-style.md` per `references/LEARNING-STYLE-FORMAT.md`. Never interview for this; only ever record what's observed.
9. **Lightweight spaced review (optional, informal)**: if `learning-records/` shows a concept from several modules back that hasn't resurfaced, and a natural opening exists, suggest revisiting it in passing ("this connects back to X from a few modules ago — worth a quick recap, or are you solid on that?"). This is a nudge, never a quiz, never scored — see `references/ZPD-ENGINE.md` for why this stays informal.
10. **Self-check before moving on** — confirm: graph updated? wiki ingested (or explicitly skipped because no reusable entity)? glossary checked? highlight drafted or explicitly not warranted? These are invisible, easy-to-drop steps — treat this checklist as mandatory, not optional housekeeping.
11. Repeat from step 1, following the graph the user's questions are drawing.

## Explore Phase — Explain Mode (conversational loop)

No module files. State lives in the conversation itself, plus `MISSION.md` (mode + audience baseline), `RESOURCES.md`, and `./highlights/` candidates — use `NOTES.md` as a scratchpad if a session risks losing thread across a long conversation, not a full transcript.

1. **Calibrate the audience baseline** (if not already done): who is this for, what do they already know, what's completely new to them — see `references/AUDIENCE-CALIBRATION.md`. **If `SERIES.md` exists, read its `Published` section's `Covered` entries now, too** — the real audience for piece 3 has already read pieces 1 and 2, so their starting knowledge state is the calibrated baseline plus everything the series has already covered, not just the baseline alone. This combined state plus everything explained so far in this session is the audience's ZPD (see ZPD engine section above).
2. **User explains a chunk** of their topic/argument, in their own words.
3. **AI asks one question, playing the audience** — see "The AI as questioner" above. The question should surface either a real gap (something assumed beyond the current cumulative baseline) or a genuinely useful connection the audience would want made explicit — never a generic prompt for more detail.
4. **User responds**, refining or filling the gap. This response is itself new material — it advances the cumulative audience-knowledge state.
5. **Glossary**: if a term has now been articulated in a way that's actually audience-appropriate (not just used fluently between two experts), add it. See `references/GLOSSARY-FORMAT.md`.
6. **Draft a candidate highlight** silently if this exchange produced a sharper framing or an insight worth keeping — same rules as Learn Mode, see `references/HIGHLIGHT-FORMAT.md`.
7. **Self-check before moving on**: did the question actually probe a real gap (not generic)? glossary checked? highlight drafted or explicitly not warranted?
8. Repeat from step 2 until the user says they're ready to produce something, or the material clearly covers what they set out to communicate.

## Create Phase (shared by both modes)

Triggered by explicit user request naming a format (short video / blog / long video / essay / presentation) or just "help me make something out of this." In Learn Mode, never auto-switch — if highlights + module density strongly suggest the material is ready, make **one** gentle proposal, drop it if declined. In Explain Mode this phase is usually the point of the session, so proposing it once the core argument feels pressure-tested is expected, not intrusive.

1. **Calibrate audience — every artifact, not just once per workspace**: in Explain Mode this reuses/confirms the baseline already established in step 1 of the Explore phase above (recalibrate only if this artifact is genuinely for a different audience than the one already calibrated — see `docs/adr/0011`). In Learn Mode, this is the first time audience comes up — ask directly if not obvious. Now includes platform, not just who/what-they-know — see `references/AUDIENCE-CALIBRATION.md`.
2. **Series continuity check — only if `SERIES.md` exists or this is clearly not the first piece from this workspace**: read the `Published` section before deciding scope. Check for redundant overlap with what's already shipped, and whether this piece should acknowledge continuity with the last one. See `references/SERIES-FORMAT.md`.
3. **Surface candidates — hard gate, do not skip**: pull the silent candidate highlights relevant to what the user wants to produce, present them, let the user confirm/discard. **Only confirmed ones get written to `./highlights/`, and drafting does not start until this has actually happened** — a Create Mode session that goes straight to drafting without a persisted, confirmed highlight set is skipping a required step, not taking a shortcut.
4. **Judge fit and scope, don't refuse**: assess whether the confirmed highlights + material density can support the requested format for *this audience and platform* (see `references/OUTPUT-TEMPLATES-GUIDE.md` — no numeric thresholds, judge like an editor). If thin, offer to dig deeper rather than just saying no. If it looks too ambitious for one piece (trying to cover more than the format/platform can carry) or too narrow to sustain one on its own, say so and suggest a split or a merge — this is a suggestion for the user to weigh, not a refusal.
5. **Fill gaps**: if producing the piece surfaces a knowledge gap, drop back into a short Explore-phase detour to fill it (a module in Learn Mode, a clarifying exchange in Explain Mode), then return.
6. **Draft a structural version first — not the deliverable yet.** Using `templates/module-template.html`'s chunked format (one point per block, explicit `.bridge` transitions between them), lay out this piece's content and order. Structure and connective flow are far easier to verify here than in flowing prose, and far easier to lose track of after edits once it's prose. Save it as `./outputs/<slug>-structure.html`. See `references/WRITING-DISCIPLINE.md`.
7. **Get structural sign-off before converting to the final format.** The user reviews and adjusts *structure* here — reordering chunks, splitting/merging, fixing a weak bridge — not final prose. Don't skip to the target format until this is settled.
8. **Draft the actual requested artifact** using the matching template (`templates/short-video-script.md`, `templates/blog-post.md`, `templates/long-video-script.md`, `templates/essay.md`, `templates/presentation-outline.md`), translating the approved structural draft's order and connective logic into that format's own conventions — not restarting from scratch.
   - **Visual/asset suggestions happen here, not during Explore**: annotate the draft with where a visual would help and what kind — tailored to the format (a blog post might want an occasional diagram; a video script needs concrete shot/footage/image suggestions per section). Annotate, don't necessarily generate — actually sourcing or generating the asset is a separate step the user can ask for once the draft's shape is settled.
   - **Nothing gets introduced during drafting that wasn't already established.** Every claim in the draft must trace back to a module/exchange, a confirmed highlight, or `RESOURCES.md`. If the piece needs a claim that isn't already grounded, that's a knowledge gap — go back to step 5, don't just write it in.
   - **Run a de-AI-flavor pass** (the `humanizer` skill, if available) before saving — required, not optional polish. See `references/WRITING-DISCIPLINE.md`.
9. **Save** the result to `./outputs/`, never just print it and discard. If the user confirms it's actually been published (not just drafted), record it in `SERIES.md`'s `Published` section — create the file first if this is the first piece being tracked as part of a series.
10. **Propose what's next — suggestion only, never auto-start**: once a piece is saved, sketch what a next piece in the series could cover and roughly how much, grounded in unused highlights/branches and the series shape so far. Add it to `SERIES.md`'s `Planned` section as `status: awaiting confirmation` and ask the user directly. **Never start drafting a proposed piece without the user confirming it (or a modified version of it) first** — a `Planned` entry is a proposal sitting on the table, not a green light.

## Files this skill reads/writes

See `references/WORKSPACE-LAYOUT.md` for the complete directory tree and root-file list. Learn Mode uses the full tree (`modules/`, `images/`, `wiki/`, `TOPIC-GRAPH.json`/`.md`, `learning-style.md`, `learning-records/`); Explain Mode only needs `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `GLOSSARY.md`, `./highlights/`, `./outputs/`.

## The wiki layer (Learn Mode only)

`./wiki/` is a Karpathy-style LLM wiki — a third layer alongside `TOPIC-GRAPH.json` and the modules, tracking knowledge itself (entity/concept-level) rather than learning order. See `references/WIKI-FORMAT.md`. This does not apply to Explain Mode — there's no accumulating personal knowledge map to build; the audience-ZPD tracking (baseline + cumulative) already serves the "where are we" function that mode needs.

Single-topic vs multi-topic directories: if the current directory has its own `MISSION.md`, treat it as one workspace and build one wiki. If it has no `MISSION.md` but contains subdirectories that each have one, treat each subdirectory as its own topic — build (or update) each one's `./wiki/` independently, then optionally generate one cross-topic index at the parent level linking into each topic's wiki viewer.

## Explicitly out of scope this phase

No openflipbook integration (Phase 2 — see `README.md`), no formal quizzing or scoring in either mode (the lightweight spaced-review nudge in Learn Mode is a suggestion, never a test), no cross-workspace memory beyond this one topic's directory (except the explicit multi-topic wiki case above).
