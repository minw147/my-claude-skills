# SERIES.md Format

Optional — create only once it's clear the user is producing more than one artifact meant to build on each other (a blog series, a video series), not for a single one-off piece. Lives at the workspace root, alongside `MISSION.md`.

Without this, each Create Phase pass has no memory of what's already shipped — the AI would either re-derive it by re-reading every file in `./outputs/` each time, or (worse) not check at all and risk repeating ground already covered.

**In Explain Mode, this file does double duty**: besides publishing logistics, its `Published` section is also the Explain-Mode equivalent of `learning-records/` (see `references/ZPD-ENGINE.md`) — the persisted record of what the real audience already knows, carried across sessions. A single conversation's cumulative state resets when the session ends; a multi-piece series doesn't, and the real reader of piece 3 has already read pieces 1 and 2. This only matters for Explain Mode — Learn Mode's `learning-records/` already does this job for the user's own understanding.

## Structure

```md
# Series: {topic/series name}

## Platform(s)
- {platform 1, e.g. Medium}
- {platform 2, e.g. MW_Web} — {note if different platforms serve different audiences/purposes}

## Pieces

### Published
1. **{title}** — {platform} — published {date}
   **Covered**: {the actual points/concepts/claims this piece established — detailed enough to seed the next piece's audience-ZPD baseline, not just a marketing-style one-liner. e.g. "established that Research Hub started skill-only with no GUI; introduced the 'button is a prompt' framing; did not yet cover the fault-tolerance argument."}
2. **{title}** — {platform} — published {date}
   **Covered**: {...}

### Planned (proposed by AI, awaiting user confirmation)
- **{rough title/angle}** — {format} — {one-line: what it would cover, roughly how much} — proposed {date} — status: awaiting confirmation | confirmed | declined
```

## Rules

- **Platform affects scope, not just tone.** A platform is often a proxy for both audience and format norms (see `references/AUDIENCE-CALIBRATION.md`, which now asks about platform explicitly) — factor it in when judging how much a single piece should try to cover, alongside the format guidance in `references/OUTPUT-TEMPLATES-GUIDE.md`.
- **Before drafting the next piece, read the entire `Published` section first — this is not optional, and it's more than a redundancy check.** In Explain Mode, the audience's ZPD baseline for this new piece is the original calibrated baseline **plus every `Covered` entry from every already-published piece in this series**, not just what's been said in the current conversation (see `references/ZPD-ENGINE.md`). Skipping this read means calibrating against a fictional first-time reader when the real one has already read N pieces.
- **`Covered` entries need to be specific enough to actually do this job.** "Covered the history of X" is too vague to tell whether a specific claim in the next draft would be new or repetitive to this audience. Write it the way you'd write a `learning-records/` entry — concrete enough to steer a real decision later.
- **The AI proposes, the user decides — always.** After saving a finished artifact, sketch what a next piece could cover and roughly how much, and add it to `Planned` with `status: awaiting confirmation`. Never start drafting a planned piece until the user has actually confirmed it (or a modified version of it) — a proposal sitting in `Planned` is not authorization to proceed.
- **Scope feedback is also a proposal, not a directive.** If a piece (proposed or user-requested) looks too ambitious for the format, or too thin to sustain one, say so and suggest a split or a merge — but the user, who drives content direction, makes the actual call.
- **Update `Published` immediately after the user confirms a piece has actually shipped** (not merely drafted and saved to `./outputs/` — drafting and publishing are different events; don't conflate them), writing the `Covered` entry at the same time while the piece's actual content is fresh. If the user hasn't confirmed publication yet, leave it out of `Published` rather than assuming.
