# Pendo Code Block: Muuri Drag-and-Drop Reference

Facts 7, 11, and 12 from `SKILL.md`. Covers transform-based layout
libraries (e.g. [Muuri](https://github.com/haltu/muuri)) running inside the
Code Block sandbox.

**Optional.** `assets/card-sort-template/` does not use Muuri or any
transform-based library; it uses native HTML5 drag-and-drop specifically
to avoid the class of bug documented below (see its README's "Drag-and-drop
implementation" section). Read this file only when deliberately choosing
Muuri, or a similar transform-based library, for richer drag physics than
native HTML5 DnD provides.

If Muuri is used as the drag-and-drop grid engine for a card-sort
activity: it is a solid starting point, but its defaults are not tuned for
a card-sort's requirements (arbitrary drop order, no persistent DOM
reparenting) and produce visibly glitchy behavior out of the box inside
this sandbox specifically. Do not spend time chasing those defaults, apply
the three overrides below instead; they are the confirmed fix for each corresponding
class of glitch.

## Fact 7: Promote the transformed ancestor, not the dragged item

Transform-based layout libraries create new CSS stacking contexts. If a
library (e.g. Muuri) positions elements via `transform`, a child's
`z-index` bump cannot out-rank siblings outside that transformed ancestor's
stacking context; promote the ancestor instead. Avoid `transform` for
hover/interaction effects on top of such a library; use `box-shadow` etc.

**Concrete confirmed instance:** dragging an item between two
`transform`-positioned siblings (e.g. a Muuri Kanban row, `layout: {
horizontal: true }`) can render the dragged item behind whichever sibling
comes later in DOM order, direction-dependently, because the library
typically only reparents a migrated item's DOM node at drag *end*, not
mid-drag, so the item's own z-index stays trapped inside its *origin*
container's stacking context for the whole drag.

The fix that actually worked (a client card-sort project): do not bump the
dragged item's own z-index; instead temporarily bump the **origin
container's own** z-index for the drag's duration (a class toggled on
`dragStart`/`dragEnd`/`dragReleaseEnd`), which lifts the whole transformed
ancestor, dragged item included, above every sibling regardless of DOM
order. Worked code: `references/muuri-drag-drop-patterns.md`, pattern 3.

## Fact 11: Avoid Muuri's dragContainer option

Muuri's `dragContainer` option (reparenting a dragged item's DOM node into
a different container, e.g. `document.body`, for the drag's duration) is
unreliable inside this sandboxed iframe; avoid it.

Confirmed in a client card-sort project: setting `dragContainer` on a grid
made its dragged items go invisible **immediately on pickup**, before the
item ever left its origin container, the opposite of what the option is
meant to fix.

The correct pattern for "an item disappears once a drag crosses its own
container's edge" is *not* `dragContainer`; toggle `overflow: visible` on
the relevant scrollable ancestor(s) for the exact duration of the drag (via
`dragStart`/`dragEnd`/`dragReleaseEnd` listeners), leaving the item in its
native DOM parent throughout. Worked code:
`references/muuri-drag-drop-patterns.md`, pattern 2.

## Fact 12: Override dragSortPredicate when order carries no meaning

When a drag-and-drop task's item order carries no real meaning (an open
card sort, a simple bucket/group task, etc.), do not fight a drag library's
native overlap-percentage sort predicate; override it with a simpler
positional rule instead.

Muuri's default `dragSortPredicate` measures overlap against each grid's
rect *after* scroll-clipping, which produces hard-to-pin-down bugs under
different symptoms: a populated container's own empty space becoming
invisible to the overlap check, items landing in a neighboring container
near a boundary, a drop-highlight that does not match where the item
actually lands.

If the task does not care about order, replace the predicate entirely with
a plain `getBoundingClientRect()` pointer-hit-test against each candidate
container and always drop at a fixed position (e.g. index 0): a
function-form `dragSortPredicate` fully supersedes Muuri's built-in
predicate (the `dragSort` option becomes irrelevant once this is done).
Reuse the exact same hit-test to drive any drop-target highlight too, so
the highlight and the real drop target can never disagree. Worked code:
`references/muuri-drag-drop-patterns.md`, pattern 1.
