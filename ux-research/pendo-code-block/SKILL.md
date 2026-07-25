---
name: pendo-code-block
description: "This skill should be used when building or debugging a Pendo Guide Code Block: pendo.track() sandbox errors, guides stuck on \"Loading Guide...\", multi-step auto-advance, or drag-and-drop bugs."
---

# Pendo Code Block

Build and debug custom Pendo Guide Code Blocks (HTML/CSS/JS pasted into a
Pendo guide's Visual Design Studio). Custom code in a Code Block is
unsupported/no-SLA per Pendo's own docs, so treat undocumented behavior as
reverse-engineered, not a stable contract, and verify anything not already
covered in `references/pendo-api-behavior.md` using the diagnostic
methodology in `references/diagnostic-and-layout.md` before shipping it.

## When to use this

- Setting up a new Pendo Code Block from scratch, start from
  `assets/card-sort-template/` or `assets/maxdiff-template/` rather than a
  blank file.
- A Code Block's guide hangs on "Loading Guide..." in the Design Studio.
- `window.pendo` / `pendo.track()` / sandbox errors inside a Code Block.
- Wanting a multi-step guide to auto-advance when a Code Block completes.
- Debugging drag-and-drop layout bugs (Muuri or similar transform-based
  libraries) inside the sandboxed iframe.
- Any "does Pendo support X from inside a Code Block" question, check
  `references/pendo-api-behavior.md` first, then use the diagnostic
  methodology if the answer isn't already documented there.

## Quick-reference index

Full detail, rationale, and confirmed-vs-untested caveats for every item
below live in `references/pendo-api-behavior.md` (facts 1-6, 8-10) and
`references/muuri-drag-drop.md` (facts 7, 11, 12).

1. Always preview from the guide's real host page, never the Design
   Studio's own broken "Preview" button.
2. Inline every dependency into one IIFE via a build script; never rely on
   a separately-loaded `<script src>` finishing first.
3. Use `window.pendo` (not `window.top.pendo`) and call `pendo.track()`
   directly; stage the guide before expecting track events to land.
4. Flatten and truncate `pendo.track()` payloads safely; Pendo enforces
   per-property and total event-size limits.
5. Scope track event names per study (constants or a `studyName` property);
   names are shared across the whole subscription, not per-guide.
6. Call `activeGuide.step.advance()` to auto-advance a multi-step guide;
   `advanceMethod` is blank by default for Code Block steps.
7. Promote a transformed ancestor's z-index during drag, not the dragged
   item's own, when using transform-based layout libraries (e.g. Muuri).
8. Keep repeated-trial/multi-screen tasks inside one Code Block step; Pendo
   has no native step-repeat mechanism.
9. Reach for `height: 100vh` only when the layout has a region that needs
   to scroll, not as a default.
10. Call `pendo.onGuideDismissed()` with no arguments to close the guide
    from inside a Code Block; it fires immediately, with no delay.
11. Avoid Muuri's `dragContainer` option inside this sandbox; toggle
    `overflow: visible` on the scrollable ancestor instead.
12. Override Muuri's default `dragSortPredicate` with a positional
    hit-test when item order carries no meaning (e.g. an open card sort).

## Bundled resources

Pendo's Code Block editor has three separate panes: HTML, CSS, and JS. Its
own "Preview" button is broken for Code Blocks (fact 1), so without a local
preview option, every single change, even a one-line CSS tweak, means
pasting into the real guide and waiting on Pendo's UI just to see it. The
mock-pendo harness below exists to close that loop locally.

- `scripts/build-code-block.js`, concatenates a project's source files into
  one IIFE-wrapped output (fact 2). Config-driven:
  `node scripts/build-code-block.js --config path/to/build.config.json`.
- `scripts/mock-pendo.js`, a stub `window.pendo` for local UI/interaction
  preview only, load it before the built output in a preview harness. Does
  **not** validate real track events, staging, or multi-step advance; see
  the scope warning in the file itself and fact 1.
- `assets/card-sort-template/` and `assets/maxdiff-template/`, working
  starter Code Blocks built on the two scripts above. Within each:
  - **Only three files ever get pasted into Pendo**, one per tab:
    `src/markup.html` (HTML tab), `src/styles.css` (CSS tab), and the
    *built* `dist/code-block.js` (JS tab), not `src/ui.js` directly, it
    has to go through the build script first.
  - `src/data.js`, `src/payload.js`, `src/ui.js`, and `src/payload.test.js`
    are source and tests that get concatenated into `dist/code-block.js`;
    edit these, then rebuild, rather than editing the built file.
  - `preview.html` combines all three pasted-into-Pendo pieces locally
    (via the mock-pendo stub) so layout and interaction can be iterated on
    in a real browser without touching Pendo at all. Open it after
    building; rebuild and refresh to see changes.

Workflow: copy a template, edit `src/data.js`, build, iterate against
`preview.html` for layout/interaction, then paste the three tab files into
Pendo and verify live in the real staged guide (fact 1) before shipping.

For the diagnostic methodology (how to safely investigate anything not
covered above) and the suggested project layout for a Code Block build,
see `references/diagnostic-and-layout.md`.
