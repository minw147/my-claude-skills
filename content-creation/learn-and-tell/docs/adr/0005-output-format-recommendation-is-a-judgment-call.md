# No numeric thresholds for output-format recommendations

When recommending short-video vs blog vs long-video format, the AI judges based on the material's density and narrative completeness — like an editor — rather than applying a fixed rule (e.g. "<3 highlights → short video, 5+ → blog"). If the user's requested format doesn't match the current depth, the AI offers a choice (dig deeper on this topic, or broaden scope) rather than refusing.

Numeric thresholds were the original brainstorm's proposal and were explicitly rejected: highlight "density" varies wildly by topic (a single history highlight can carry more weight than three in another domain), so a fixed count is precision theater. This is a deliberate deviation from an already-written, more mechanical-looking spec — worth recording so a future reader doesn't "restore" the thresholds thinking the qualitative version was an oversight.
