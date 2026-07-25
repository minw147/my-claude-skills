# learn-and-tell

A **Claude Code skill** for content creators: explore a topic through problem-posing driven learning, then turn the exploration into publishable content (video script, blog post). Forked in spirit from the `/teach` skill (MIT, Matt Pocock) — `/teach` itself is a Hermes skill, but learn-and-tell targets Claude Code's skill format (`.claude/skills/`), not Hermes.

## Language

**Workspace**:
The current working directory when the skill runs. Holds all state for one topic — same convention as `/teach`. No separate path-management logic; the user `cd`s into a directory to start a new topic.

**Module**:
The unit of teaching content — one self-contained HTML file in `./modules/`, numbered `0001-<dash-case-name>.html`. Renamed from `/teach`'s "lesson" because "lesson" implies a linear curriculum; learn-and-tell's modules form a non-linear, question-driven graph. **Every module file is its own Topic Graph node, with no exceptions** — an appendix like `0005b` is a distinct node connected to `0005` by an `appendix` edge, never content folded into an existing node. This is because an appendix can itself spawn further questions and diverge in its own direction; collapsing it into its parent would give it nowhere to branch from.
_Avoid_: Lesson, chapter, page.

**Question-Annotated Topic Graph**:
The structure of a user's exploration, persisted as `TOPIC-GRAPH.json` (source of truth: nodes + edges) with `TOPIC-GRAPH.md` as an auto-generated human-readable view. One node per Module file (see **Module**) — never a fragment or sub-section of a node. Edges carry a `type` (`prerequisite` | `question-spawned` | `appendix` | `merge`) and metadata (`question`, `timestamp`, `user_note`). Distinct from a course outline — the shape emerges from the user's questions, not a fixed syllabus.
_Avoid_: Curriculum, syllabus, course map.

**Highlight**:
A candidate or confirmed "aha moment" from the user's exploration — a raw material for output. Has two states: *candidate* (drafted silently by the AI at the end of a module, not shown to the user) and *confirmed* (surfaced and written to `./highlights/` only once Create Mode is triggered and the user selects from the candidates).
_Avoid_: Insight, takeaway, note.

**Mission**:
`MISSION.md` — the reason the user is exploring this topic, ported from `/teach`'s format with one addition: an optional output-intent note ("has a produced-content goal in mind, or exploring freely for now"). Grounds what the AI teaches next and, once Create Mode exists in the workspace, what it recommends producing.
_Avoid_: Goal, objective, brief.

**Output artifact**:
The actual filled-in, publish-ready document produced by Create Mode (a blog post, a video script) — written to `./outputs/`. Distinct from a **Highlight** (raw, pre-selection material) and an **Output template** (the empty structural shape in `templates/`, e.g. `blog-post.md`). Persisted in the workspace, not just handed to the user and forgotten — so a later session can revise it or produce a second format from the same confirmed highlights without re-deriving anything.
_Avoid_: Output, export, deliverable.

**Learning-style profile**:
`learning-style.md` — a free-form, observation-based record of how a specific user thinks and explores (narrative preference, cognitive style, exploration breadth, output-format preference, question density, feedback style). Not a questionnaire or a fixed typology (deliberately not VARK-style) — dimensions in `LEARNING-STYLE-FORMAT.md` are prompts for observation, not fields to fill in up front.
_Avoid_: Learning style quiz, personality profile, user segment.

**Explore Mode**:
The default mode. The user has a topic they're curious about but no fixed output target yet. The AI follows their curiosity, generates modules, and runs problem-posing after each one.

**Create Mode**:
Entered when the user explicitly signals they want to turn part of their exploration into a publishable artifact (e.g. "help me turn this into a video script"). The AI's role shifts to filling knowledge gaps and structuring the confirmed highlights into an output template.
_Avoid_: Production mode, export mode.

**Audience calibration**:
The Create Mode step that establishes who a specific artifact is for — what they already know, what they're there for, what tone/formality fits — before drafting. Scoped **per artifact, not per workspace**: the same exploration can produce a general-audience essay and a domain-peer presentation, each needing different calibration. Not the same thing as ZPD calibration in Explore Mode, which is about the explorer's own understanding — this is about the *reader's* or *listener's* understanding.
_Avoid_: Target audience, persona, reader profile.

**Problem-posing**:
The core interaction after each module: the user poses a question or scenario, rather than the AI quizzing the user. The question itself is the signal of understanding, not something to be scored.

**Metacognitive mirror**:
The AI's stance during problem-posing — it reflects the user's question back (structuring it, asking what it points to) rather than judging it as good/bad or right/wrong. Judging would outsource the user's own self-evaluation, which is the actual skill being trained.
_Avoid_: Grader, judge, evaluator.

**No-question signal**:
The event where a user does not pose a question at the end of a module. Treated as a positive/neutral signal ("this was easy enough, move faster") rather than a failure, and recorded on the relevant Topic Graph node. Repeated occurrences prompt the AI to check whether the user wants to accelerate.
