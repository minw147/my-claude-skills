# Card Sort Template

Starter Code Block for a card-sorting activity. Copy this directory, edit
`src/data.js` with real cards/starting categories, then build and preview.

This is an open card sort: category labels are placeholders, participants
are expected to rename and add their own. Layout: cards to sort sit in a
left panel; categories sit in a right panel that scrolls horizontally as
more are added, all top-aligned.

- Drag a card from the pool into a category, back to the pool to unsort
  it, or between categories if a participant changes their mind.
- Click a category's title to rename it inline (Enter to save, Escape to
  cancel).
- "+ Add category" lives in the footer, left-aligned next to Submit, not
  in the scrolling category row, so it's always reachable without
  scrolling right.
- Item order within a category carries no meaning for this task; a newly
  moved card is placed at the top of its new category so it's visible
  without scrolling.

## Build

```
node ../../scripts/build-code-block.js --config build.config.json
```

Produces `dist/code-block.js`, an IIFE-wrapped file for Pendo's Code Block
**JS** tab. Pendo's Code Block editor has separate HTML/CSS/JS tabs:

- `src/markup.html` → paste into the **HTML** tab.
- `src/styles.css` → paste into the **CSS** tab.
- `dist/code-block.js` (after building) → paste into the **JS** tab.

## Local preview

Open `preview.html` in a browser after building. This uses
`scripts/mock-pendo.js` to stub `window.pendo`, so it validates layout,
styling, and drag-and-drop only, not real Pendo behavior. See the banner
in `preview.html` and SKILL.md fact 1: always do final verification in the
real staged guide before shipping.

## Drag-and-drop implementation

Uses native HTML5 drag-and-drop, not a transform-based library, so
SKILL.md facts 7 and 11 (Muuri-specific stacking-context and
`dragContainer` bugs) do not apply to this template. To swap in Muuri for
richer drag physics, see `references/muuri-drag-drop.md` in the skill root
and apply its three fixes.

## Tests

`src/payload.test.js` covers the pure payload-building logic
(`node --test src/payload.test.js`). Add UI-level manual verification
(drag/drop, add-category, re-sorting between categories) to a
`MANUAL_VERIFICATION.md` per the skill's suggested project layout.
