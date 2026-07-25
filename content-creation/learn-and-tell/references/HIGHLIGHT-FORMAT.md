# Highlight Format

A highlight is a candidate or confirmed "aha moment" — raw material for an output artifact. Two-stage lifecycle (see `docs/adr/0003`):

## Stage 1 — Candidate (silent)

At the end of any module that produced a genuine insight (not routine coverage), draft a candidate highlight in the AI's own working notes. **Do not show this to the user, do not announce it, do not write it to disk.** This is not a file the user opens — it's material the AI is quietly accumulating for the moment Create Mode gets triggered.

A candidate is worth drafting when the module produced something like:
- A causal/necessity connection that wasn't obvious before ("the Crusades ultimately weakened the Byzantine Empire instead of strengthening it")
- A cross-topic or cross-branch connection the user hadn't made
- A genuine surprise or reframe, not just a new fact

Routine coverage of a fact, however true, is not a highlight. When in doubt, don't draft one — false positives dilute the eventual set more than missed ones.

## Stage 2 — Confirmed (on Create Mode trigger)

When the user enters Create Mode, surface the relevant candidates (filtered to what's relevant to the topic/branch they want to produce from) and let them confirm or discard each one. Only confirmed highlights get written to `./highlights/`, one file per highlight:

```md
# <one-line summary>

**From module**: 0004b-europe-track.html
**Type**: causal-connection | reframe | cross-branch-link | surprise
**Text**: <the actual insight, in the user's or a close paraphrase of their own framing>
**Confirmed**: 2026-07-17
```

## Rules

- Never number/score highlights (no 0-5 rubric, no ranking shown to the user) — the ordering criterion for use in output is editorial judgment at Create Mode time, not a stored score.
- A discarded candidate is just dropped, not recorded as "rejected" anywhere — it was never shown as a judgment in the first place.
