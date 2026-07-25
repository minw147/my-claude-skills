# Pendo Code Block: API Behavior Reference

Full rationale and confirmed-vs-untested caveats behind the 12 core facts
indexed in `SKILL.md`.

## Official docs vs. undocumented behavior

Pendo's own doc on this feature is [Customize your guides with code](https://support.pendo.io/hc/en-us/articles/360032206011-Customize-your-guides-with-code).
Treat it as thin: it explicitly states custom code is **unsupported/no-SLA,
outside Technical Support's scope**. It documents `pendo.dom()`,
`pendo.designerEnabled` (a flag to detect Design-Studio-preview vs. real
staged/published code, useful for gating diagnostic-only code),
`pendo.onGuideDismissed()`/`attachEvent()`/`detachEvent()`, and
`pendo.showGuideById()`.

Everything about multi-step advance (`getActiveGuide()`, `.step.advance()`,
`goToStep()`) is **not** in Pendo's official docs, it was found purely by
diagnostic logging against a real guide (see `diagnostic-and-layout.md`).
Treat it as reverse-engineered, not a stable contract.

## Fact 1: Preview from the real host page

Never trust the Visual Design Studio's own "Preview" button for a Code
Block, it is broken and hangs forever on "Loading Guide...". Do final
verification with the browser console open on the real preview/live view,
not just the editor pane; the editor pane's timing is more forgiving and
can hide real load-order bugs.

## Fact 2: Inline everything into one IIFE

Code Blocks run in a sandboxed, cross-origin iframe; Pendo does not
guarantee a separately `<script src>`-loaded file finishes before the JS
tab runs. Concatenate all dependencies (vendored libs, data, UI logic) into
one generated file via a small build script, and paste only the generated
file into the JS tab. Never hand-edit the generated file.

This rules out directly embedding a real component-library runtime shipped
as ES modules with a cross-file `import` graph (untested without a real
bundler run). What transfers cleanly: a component library's plain design
tokens (colors, spacing, radius, elevation, type scale) are just CSS
values, copy the literal values into a local `:root` block instead of
importing the component runtime.

## Fact 3: window.pendo, not window.top.pendo

`window.pendo` works inside the sandbox; `window.top.pendo` does not
(cross-origin `SecurityError`). Call `pendo.track(eventName,
propertiesObject)` directly to capture data, do not rely on
clipboard-write for export, it is unreliable in the sandbox.
`window.confirm()`/`alert()` work fine.

Confirmed: previewing an unstaged guide does not create real track events;
the guide must be staged (at minimum) before `pendo.track()` calls actually
land in Track Events / Data Explorer.

## Fact 4: Respect event-size limits

Pendo enforces per-property and total event-size limits on `pendo.track()`
payloads. If a payload can grow unboundedly, write a pure, unit-tested
function that flattens and truncates safely (Unicode code-point boundary)
before tracking.

## Fact 5: Track event names are subscription-wide

Track event names are shared across the whole subscription, not scoped to
one guide; any guide firing the same `eventName` feeds the same Data
Explorer bucket. Reusing a name across unrelated studies mixes their data.
Rename per study by default, or add a distinguishing property (e.g.
`studyName`) and filter by it.

## Fact 6: Auto-advance a multi-step guide

```js
function advanceToNextGuideStep() {
  if (typeof pendo === 'undefined' || typeof pendo.getActiveGuide !== 'function') {
    return;
  }
  const activeGuide = pendo.getActiveGuide();
  if (activeGuide && activeGuide.step && typeof activeGuide.step.advance === 'function') {
    activeGuide.step.advance();
  }
}
```

Call this right after completion/track-event logic fires. Gotchas:

- `pendo.getActiveGuide().steps` at the top level is a page-matched subset
  (often just the current step); the **full** step list is at
  `pendo.getActiveGuide().guide.steps`.
- A Code Block step's `advanceMethod` is blank by default (Pendo only
  auto-wires that for native elements), this is expected, not a bug; call
  `.advance()` directly.
- `pendo.goToStep(guide, stepId)` exists for out-of-order jumps; prefer
  `.advance()` otherwise. Confirmed **not** to work for jumping multiple
  steps forward (e.g. skipping steps 3-5 to land on step 6 from step 2),
  live-tested in a client card-sort project; the call did not move the
  guide at all. Jumping to an adjacent/nearby step is untested, do not
  assume it works for any target step without testing that specific jump
  live first. To skip a disqualified participant past several steps,
  showing an inline message and dismissing the guide entirely (fact 10) is
  a confirmed-working alternative to routing through remaining native steps.

## Fact 8: Repeated-trial tasks stay in one step

Pendo has no native way to repeat a guide step N times with different data
each time. Manage the whole sequence with its own JS state (a "current
screen" variable plus a render function) inside one step, and call
`.step.advance()` (fact 6) only once, after the entire sequence finishes,
not between individual trials. Fire each trial's own track event as it
completes, not batched to the end, so partial completion stays measurable.
Since steps share no runtime, small helpers like `advanceToNextGuideStep()`
get duplicated verbatim into every step that needs them; expected, not a smell.

## Fact 9: height: 100vh is conditional

Reach for `height: 100vh` (or any forced height) only if the layout has a
region that needs to scroll (so `overflow-y: auto` + `min-height: 0` have
something to divide against). Forcing it on a short, non-scrolling layout
just stretches the guide to fill the viewport and leaves dead empty space
below the actual content.

## Fact 10: Dismiss the guide from inside a Code Block

```js
if (typeof pendo !== 'undefined' && typeof pendo.onGuideDismissed === 'function') {
  pendo.onGuideDismissed();
}
```

`pendo.onGuideDismissed()` is dual-purpose: called *with* a callback
argument, it registers a listener for guide dismissal (Pendo's official
docs cover this use); called with **no arguments**, it actively
dismisses/closes the currently displayed guide. Confirmed live in a client
card-sort project's screener step; matches Pendo's own snippets repo
(`github.com/pendo-io/snippets`, e.g. `dismissWhenClickOutsideGuide.js`)
and a Pendo Help Center post ("How to auto close a Guide").

It fires **immediately, with no delay**. If a message needs to be visible
first (e.g. a "Thank you" note shown to a screened-out participant), render
the message, then call this inside a `setTimeout` (1.5-3s), not
synchronously right after; calling it synchronously closed the guide before
the message could ever render in live testing.

Also flags a Design-Studio-editor-only gotcha: the editor re-runs the
script continuously while typing, and a top-level `const` breaks that
re-run. Use `let`/`var` at the top level, or wrap everything in one IIFE
(fact 2), which sidesteps it automatically.

See `references/muuri-drag-drop.md` for facts 7, 11, and 12 (transform
stacking contexts, `dragContainer`, and `dragSortPredicate`).
