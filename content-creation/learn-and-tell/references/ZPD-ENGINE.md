# The ZPD Engine

Ported from `/teach`'s Zone of Proximal Development concept, generalized to work for both modes. The core question is always: **what does this audience already know, and what's the single next thing that's "just challenging enough" to introduce?** Too easy and it's boring/redundant; too far ahead and it's incomprehensible. Getting this right — actively, every step, rather than passively waiting for the user to steer — is the actual "wow" mechanic this skill is built around. Passively following wherever the user's own questions happen to lead is not the same thing as this, and isn't a substitute for it.

## Learn Mode: ZPD of the user

The audience being modeled is the user themselves. Their knowledge state comes from:

- **`learning-records/`** — genuine demonstrated understanding, disclosed prior knowledge, corrected misconceptions. Read before deciding what a module should cover next.
- **`learning-style.md`** — observed preferences (narrative style, cognitive style, exploration breadth). This shapes *how* to teach the next thing, not *what* the next thing is.

Before writing a module, ask: given what's in `learning-records/` so far, what's the smallest next step that builds directly on confirmed understanding without requiring a leap the user hasn't demonstrated they can make? This is an active judgment made every module, not a rule applied once at workspace setup.

## Explain Mode: ZPD of the imagined audience

There's no real second person answering questions here — the "audience" is imagined, and its knowledge state has to be defined some other way. It's defined as:

**Audience ZPD = the initial calibrated baseline (see `references/AUDIENCE-CALIBRATION.md`) + everything established in previously published pieces of this series, if any (see `references/SERIES-FORMAT.md`'s `Covered` entries) + everything established in this session's conversation so far.**

The series term matters: a single conversation's cumulative state resets when the session ends, but a real reader of piece 3 has already read pieces 1 and 2 — their actual knowledge didn't reset. If `SERIES.md` exists, read its `Published` section's `Covered` entries before calibrating a new piece; skipping this means calibrating against a fictional first-time reader instead of the real one.

This is deterministic, not a guess: the baseline is set once, explicitly, at the start of Explore Mode ("who is this for, what do they know, what's new to them"), then extended by whatever the series record shows. From there, every point the user successfully explains in the current session is added to the cumulative state — the audience "now knows" whatever's been said, exactly as if they were reading along. The AI's job each turn is to compare the user's next point against that cumulative state:

- **Assumes something beyond it** → real gap, worth a question.
- **Sits comfortably within it** → fine, no question needed, let it proceed.
- **Redundantly restates something already covered** → lower-priority, but worth flagging if it's slowing the piece down.

This is what makes the audience-ZPD judgment concrete instead of vibes-based: at any point, "what does the audience know" has a specific, checkable answer — the baseline plus a running list of what's been explained.

## Generative vs. procedural questions

Neither mode should ever judge a question as *wrong* — there's no such thing here (`docs/adr/0004`, mirror not judge). But questions do differ in how generative they are:

- **Generative**: builds a connection (to something covered earlier, to something outside the workspace) or opens the next branch/section. These are worth following and worth modeling more of.
- **Procedural**: convergent, single-correct-answer, dead-ends immediately with nothing following from the answer (e.g. "what year did X happen").

**In Learn Mode**, the user is the one asking — never tell them a question was low-value, but do nudge: reflect connective framings back more often, and if a module naturally surfaces a connective question the user hasn't voiced, offer it as an option rather than waiting.

**In Explain Mode**, the AI is the one asking (playing the audience) — hold your own questions to the same standard. A good question here surfaces a real gap between the cumulative audience state and what the user just said, or asks for a connection the audience would genuinely want made explicit. A bad one is generic ("can you say more?") or probes something already well-established — that's the AI failing its own half of this mechanic, not a neutral question.

## Fluency vs. storage strength (Learn Mode only, kept lightweight)

Ported from `/teach`: **fluency** (feeling like you get it, in the moment) is not the same as **storage strength** (actually retaining it later). Desirable-difficulty techniques that build the latter: retrieval practice (recalling from memory rather than re-reading), spacing (revisiting after a gap), interleaving (mixing related-but-distinct topics).

This skill keeps this *informal*, deliberately, because formal testing/scoring would break the "not a tutor, mirror not judge" stance (`docs/adr/0004`) that the rest of the design depends on. In practice: if `learning-records/` shows a concept from several modules back hasn't resurfaced and a natural opening exists, suggest a quick recap in passing — a nudge the user can wave off, never a graded check. This does not apply to Explain Mode; there's no user-retention concern when the user already knows the material and isn't the one being taught.
