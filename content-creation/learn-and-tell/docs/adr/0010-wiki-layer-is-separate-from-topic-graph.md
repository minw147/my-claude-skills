# The wiki is a third layer, not a replacement for TOPIC-GRAPH.json

`./wiki/` was added as a Karpathy-style LLM wiki (see [Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) — a persistent, incrementally-maintained set of entity/concept pages, cross-referenced via `[[wikilinks]]`, synthesized from whatever modules mention that entity.

The temptation was to fold this into `TOPIC-GRAPH.json` (ADR 0002) since both are "graphs of the topic." That would have been wrong: they answer different questions at different granularity. TOPIC-GRAPH is module-level and answers "what order did I learn things in, and why" (prerequisite / question-spawned / appendix / merge edges between whole lesson files). The wiki is entity-level and answers "what do I know about X, everywhere it appears" — a query TOPIC-GRAPH structurally cannot answer, since a single module can (and usually does) touch a dozen entities that also recur across other modules.

Concretely: a workspace with 12 modules produced a TOPIC-GRAPH with 12-ish nodes, but a wiki with 17 entity pages, because entities like "the Byzantine Empire" recur across 5 different modules and deserve one page with 5 backlinks, not 5 disconnected mentions. Both layers are maintained in parallel on every module write (SKILL.md Explore Mode steps 4 and 5); neither is optional once the other exists.

This also seeded the interactive viewer (`templates/wiki-viewer.html`) — a canvas force-graph + reader view, built independently, unrelated to the openflipbook credit in `README.md` (which is only about the "every concept gets an illustration" principle).
