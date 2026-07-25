# Output Format Recommendation Guide

When recommending short-video vs blog vs long-video vs essay vs presentation, judge like an editor assessing a pile of material for a specific audience — never apply a numeric rule like "3 highlights = short video." Density of insight varies wildly by topic, and the right format depends on who it's for as much as how much material exists. See `docs/adr/0005` and `references/AUDIENCE-CALIBRATION.md` (calibrate audience *before* this judgment, not after).

## What to weigh

- **Narrative completeness**: do the confirmed highlights, strung together, already form a beginning/middle/end, or are they scattered points needing connective tissue?
- **Density per highlight**: some single highlights carry enough weight to anchor an entire piece (a strong reframe); others are minor and need several stacked to mean anything.
- **Branch coverage**: a long-video- or presentation-worthy piece usually draws on multiple graph branches (main track + at least one question-spawned or appendix branch), not just a single linear run of modules.
- **Who it's for**: the same material that's "thin" for a general-audience blog post might be exactly enough for a presentation to domain peers, who need less foundational setup and can absorb a denser, faster-paced argument. Judge sufficiency against the calibrated audience, not in the abstract.
- **What the user is actually reaching for**: someone who says "help me make a short video" wants something snappy even if the material could support more — don't over-recommend length just because more material exists.

## Rough shape (guidance, not thresholds)

- **Short video**: one or two sharp highlights, minimal setup needed, works even off a single branch.
- **Blog post**: enough highlights to form a connected arc; benefits from citing 2+ branches or a prerequisite chain.
- **Essay**: similar material needs to blog post, but the exploration's actual shape (false starts, the branch that mattered) matters more than density — an essay can work with less material than a blog post if the *thinking process* itself is interesting.
- **Long video**: needs real narrative depth — multiple branches, appendices, or a track that's been explored over several sessions.
- **Presentation**: needs multiple branches like long video, but sufficiency is audience-relative — a domain-peer audience needs less connective material than a general one to feel a talk was substantive, because they fill gaps themselves.

## When the user's request doesn't match the depth

Never just refuse or silently comply with thin material. Offer a real choice:

> "These points work well for a short video, but a long video or a talk would feel thin — want to dig deeper into branch X, or pull in topic Y as well?"

Then let the user pick: dig deeper on the current branch, broaden which branches feed the piece, or proceed anyway if they're fine with it being lighter than usual.
