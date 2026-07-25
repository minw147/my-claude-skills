# Pendo Code Block: Diagnostic Methodology and Project Layout

## Diagnostic methodology for anything undocumented

Do not guess an unconfirmed Pendo API surface and ship it. If behavior is
not already covered in `pendo-api-behavior.md` or `muuri-drag-drop.md`:

1. Add a clearly-marked `// TEMPORARY DIAGNOSTIC` console-logging block
   (e.g. `Object.keys(pendo)`, or logging a suspect return value's full
   shape).
2. Rebuild, and test live in the actual staged guide; diagnostics must run
   against a real guide, not a local mock.
3. Read back the real console output, and narrow the next round of logging
   based on what is actually there; do not re-guess method names,
   enumerate the real object.
4. Once confirmed, remove all diagnostic logging and replace it with the
   real, permanent implementation. Document the finding by appending to
   the project's own setup doc so the next project does not repeat the
   investigation.

## Suggested project layout

- Keep small source files separate: study data, a shared payload-building
  module, UI logic.
- Use a `build.js` (or similarly-named per activity) to concatenate
  everything into one generated JS file, wrapped in an IIFE. Inline only
  what the activity actually needs: a drag-and-drop activity inlines
  vendored Muuri/pako; a non-drag activity (e.g. a MaxDiff best-worst-scale
  step) inlines nothing but its own payload builder, data, and UI logic.
- Give any pure logic independent of the DOM/Pendo (e.g. a track-event
  payload builder) a real unit test file (`node --test`); this is usually
  the only automatable seam. Validate UI-level invariants here too (e.g.
  "these two ids must differ") as a second line of defense, not just in
  the UI.
- Write a `MANUAL_VERIFICATION.md` checklist for everything that cannot be
  unit-tested (drag/drop or other interaction, sandbox behavior, whether
  events land in Pendo's Data Explorer, multi-step advance).
- Write a `README.md` that points to the spec and explains the file
  list/workflow.

## Using the bundled build script and templates

`scripts/build-code-block.js` is the generalized version of the per-project
`build.js` pattern above: a config-driven script that concatenates an
ordered file list into one IIFE-wrapped output (`node build-code-block.js
--config build.config.json`). It was worth extracting for this skill even
though any single internal repo had only proven the pattern twice, because
a bundled skill serves indefinitely many future projects; each one is a
new use case for the config shape, not a repeat of the same two.

`assets/card-sort-template/` and `assets/maxdiff-template/` are working
starter projects built on top of that script, ready to copy and adapt: edit
`src/data.js`, run the build, open `preview.html` for a mocked local
preview (`scripts/mock-pendo.js`; see the preview banner and fact 1 for
what it does not validate), then verify live in the real staged guide.

Keep the two payload builders separate rather than merging them into one
helper: the card-sort payload handles unbounded-text truncation, the
MaxDiff payload handles small-fixed-shape cross-field validation instead.
They solve genuinely different problems; only extract a shared scaffold if
a third payload shape reveals a real common core.
