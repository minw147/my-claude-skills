# Target Claude Code's skill format, not Hermes

learn-and-tell is built as a Claude Code skill (`.claude/skills/`), even though its direct inspiration — `/teach` — is a Hermes skill (`hermes/skills/teach/`).

This is worth recording because a reader following the credit chain back to `/teach` would reasonably assume the same runtime. It isn't a value judgment on Hermes; it's a distribution choice — Claude Code's skill format is what the target user (a solo content creator, not necessarily running Hermes) already has access to. `SKILL.md` frontmatter, invocation conventions, and any tool-calling assumptions should follow Claude Code's conventions, not Hermes's, even where they diverge from `/teach`'s original file.
