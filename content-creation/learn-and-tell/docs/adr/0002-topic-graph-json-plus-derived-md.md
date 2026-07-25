# Topic Graph: JSON source of truth, Markdown derived view

The Question-Annotated Topic Graph is persisted as `TOPIC-GRAPH.json` (nodes, edges, edge types, edge metadata) with `TOPIC-GRAPH.md` auto-generated from it as a human-readable summary. The Markdown file is never hand-edited.

Considered keeping it as a single hand-maintained Markdown file, matching the prose style of `MISSION.md`/`NOTES.md` in `/teach`. Rejected: the graph isn't a note for the user to read, it's a decision input — the AI uses it to decide whether a question should spawn a branch, extend an appendix, or stay on the main track, and Phase 2 (the openflipbook fork) needs to render it directly. Prose can't hold edge direction and type precisely enough for either purpose. The trade-off is one extra artifact to keep in sync per module; acceptable since only the AI writes it.
