# Learning Record Format

Ported near-verbatim from `/teach` — this discipline isn't affected by the content-creator adaptation. Records live in `./learning-records/`, numbered `0001-slug.md`, `0002-slug.md`, etc. Create the directory lazily.

They're the ADR-equivalent for a learner: non-obvious insights and stated prior knowledge that steer future modules and ZPD calibration.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for future modules.}
```

That's the whole format. A record can be one paragraph.

## Optional sections

- **Status** frontmatter (`active | superseded by LR-NNNN`)
- **Evidence** — how the user demonstrated it (answered an application question, cited prior experience)
- **Implications** — what this unlocks or rules out for future modules

## When to write one

1. The user demonstrated genuine understanding of something non-trivial (not mere exposure — evidence they can use it).
2. The user disclosed prior knowledge ("I already know X").
3. A misconception was corrected.
4. The mission shifted in response to exploring — cross-link to `MISSION.md` and update it.

### What does *not* qualify

- Material merely covered (coverage isn't learning — wait for evidence).
- Anything already in a `reference/` glossary as a term definition.
- Session-by-session activity logs.

## Supersession

When a later record contradicts an earlier one, mark the old one `Status: superseded by LR-NNNN` rather than deleting it.
