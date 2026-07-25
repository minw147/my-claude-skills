# MaxDiff Template

Starter Code Block for a MaxDiff (best-worst scaling) activity: a card
with a framing question and a two-column priority table, radio buttons for
"Highest Priority" on the left and "Lowest Priority" on the right, item
labels in between. Selecting an item as highest disables its lowest radio
(and vice versa), so the two can never conflict.

Copy this directory, edit `src/data.js` with a real question and items,
then build and preview.

## Build

```
node ../../scripts/build-code-block.js --config build.config.json
```

Pendo's Code Block editor has separate HTML/CSS/JS tabs. Only three files
ever get pasted into Pendo:

- `src/markup.html` → paste into the **HTML** tab.
- `src/styles.css` → paste into the **CSS** tab.
- `dist/code-block.js` (after building) → paste into the **JS** tab.

## Local preview

Open `preview.html` in a browser after building. Uses
`scripts/mock-pendo.js` to stub `window.pendo`; validates layout,
trial-cycling, and the highest/lowest mutual-exclusion logic only, not
real Pendo behavior. Verify live in the real staged guide before shipping
(SKILL.md fact 1).

## Trial sequencing

Per SKILL.md fact 8, all trials stay inside one Code Block step. Trial
state lives in this file's own JS (`trialIndex`, `currentItems`), and
`.step.advance()` is called once after `TRIAL_COUNT` trials finish, not
between trials. Each trial's own `pendo.track()` call still fires as it
completes. The last trial's button reads "Submit" instead of "Next".

`src/data.js`'s item-per-trial draw is a placeholder random sample; a real
study should use a proper balanced incomplete block design.

## Tests

`src/payload.test.js` covers the payload builder's cross-field invariants
(best != worst, both must be in the shown set):
`node --test src/payload.test.js`.
