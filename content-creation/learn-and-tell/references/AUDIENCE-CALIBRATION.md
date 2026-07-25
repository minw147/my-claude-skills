# Audience Calibration

Every output artifact has a reader or listener who isn't the explorer. Explore Mode calibrates to *the user's* zone of proximal development (via `learning-style.md` and `learning-records/`) — Create Mode has to calibrate to someone else's. The same confirmed highlights, from the same exploration, can produce a Medium essay for a general audience, a UXR conference talk for domain peers, and a 60-second video for casual scrollers — and each needs a genuinely different depth of foundational explanation, jargon tolerance, and structural formality.

This step exists because it's easy to skip: the explorer already understands the material deeply, so the draft tends to default to *their* level of understanding, not the audience's. Calibrating explicitly is what prevents that default.

## What to establish, before drafting

- **Who, specifically.** Not "general audience" — closer to "UXR practitioners who've never touched LLM agents" or "Medium readers who follow AI/tech but aren't engineers." Specificity is what makes the rest of this useful.
- **What they already know.** This determines how much foundational setup the piece needs before it can use the interesting material. A UXR-conference audience may need zero explanation of research methodology but real scaffolding on LLM/agent concepts; a general Medium reader is the reverse.
- **What they're there for.** Entertainment/curiosity (casual video viewer) vs practical takeaway (conference attendee wanting something applicable to their own work) vs just a good read (essay reader) changes what counts as a satisfying ending.
- **Formality and voice.** A conference talk can carry a more structured, thesis-driven voice; an essay can carry more of the explorer's own personality and tangents; a short video needs to front-load everything.

## How to get this

Check `MISSION.md`'s output-intent note first — if the user already said who this is for when they started exploring, don't re-ask. Otherwise ask directly and briefly; this doesn't need a form, one or two questions is enough ("who's this for, and how familiar are they with this domain already?"). Don't guess silently and proceed — a wrong guess here produces a draft that has to be substantially rewritten, not lightly edited.

## Where it lives

Record the calibration in the artifact's own header (each template has a slot for it), not in a separate persistent workspace file — audience is a property of the artifact being produced, not of the workspace or the topic. The same workspace can and will produce artifacts for different audiences over time.

## How it should actually change the draft

Not just tone — audience calibration should visibly shape:
- **Which highlights get used at all.** A highlight that's obvious to domain peers might be the whole point for a general audience, and vice versa.
- **How much of the causal/necessity chain gets spelled out** vs assumed. Domain peers can skip steps a general reader needs walked through.
- **Whether jargon gets used or translated.** Don't just define every term either way — match what this audience would actually expect.
