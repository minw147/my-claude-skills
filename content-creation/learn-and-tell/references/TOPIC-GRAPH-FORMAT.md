# Topic Graph Format

`TOPIC-GRAPH.json` is the source of truth for a workspace's Question-Annotated Topic Graph. `TOPIC-GRAPH.md` is derived from it — regenerate it every time the JSON changes; never hand-edit the `.md`.

## `TOPIC-GRAPH.json` schema

```json
{
  "nodes": [
    {
      "id": "0001",
      "file": "modules/0001-timeline-skeleton.html",
      "title": "Timeline Skeleton",
      "status": "completed",
      "no_question_streak": 0,
      "created": "2026-07-17T10:00:00Z"
    }
  ],
  "edges": [
    {
      "from": "0004",
      "to": "0004b-europe-track",
      "type": "question-spawned",
      "question": "What was going on inside Europe itself? How did the individual countries form?",
      "user_note": "wants to understand intra-European formation before continuing main track",
      "timestamp": "2026-07-17T11:30:00Z"
    }
  ]
}
```

### Node fields

- `id`: matches the module's numeric/lettered prefix (`0001`, `0004b`, ...)
- `file`: relative path to the module HTML
- `status`: `completed` | `in-progress` | `planned`
- `no_question_streak`: consecutive modules ending with no user question — see SKILL.md step 5. Increment on no-question, reset to 0 the moment the user poses one.

### Edge types

- `prerequisite`: `from` must be understood before `to`
- `question-spawned`: `to` exists because the user's question during `from`'s problem-posing step led there
- `appendix`: `to` is a supplementary deep-dive off `from`, not required for the main track
- `merge`: two previously separate nodes/tracks converge into one going forward

### Hard rule

**One node per module file, always** — an appendix like `0004b` is its own node connected by an `appendix` edge, never folded into its parent's node record. An appendix can spawn its own further branches; it needs somewhere to hang them from.

## `TOPIC-GRAPH.md` (derived view)

Regenerate as a simple readable outline after every JSON update, e.g.:

```md
# Topic Graph: <workspace topic>

- 0001 Timeline Skeleton ✅
  - 0002 Rome & Christianity ✅ (prerequisite)
    - 0004b Europe Track ✅ (question-spawned — "what was going on inside Europe itself?")
  - 0003 Islamic Rise ✅ (prerequisite)
- 0004 Collision Era (planned)
```

This file is for the user to skim; the JSON is what the AI reads to decide what happens next.
