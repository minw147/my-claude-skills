(function () {
'use strict';

// Replace with real study cards and starting categories before shipping.
// Participants can add more categories at runtime (see ui.js); these are
// just the ones shown at the start.
const CARD_SORT_CATEGORIES = [
  { id: 'cat-1', label: 'Category 1' },
  { id: 'cat-2', label: 'Category 2' },
  { id: 'cat-3', label: 'Category 3' },
];

// 14 placeholder cards so the pool list overflows its panel height and
// demonstrates its own internal scrollbar (see styles.css .cs-pool-list).
const CARD_SORT_CARDS = [
  { id: 'card-1', label: 'Card 1' },
  { id: 'card-2', label: 'Card 2' },
  { id: 'card-3', label: 'Card 3' },
  { id: 'card-4', label: 'Card 4' },
  { id: 'card-5', label: 'Card 5' },
  { id: 'card-6', label: 'Card 6' },
  { id: 'card-7', label: 'Card 7' },
  { id: 'card-8', label: 'Card 8' },
  { id: 'card-9', label: 'Card 9' },
  { id: 'card-10', label: 'Card 10' },
  { id: 'card-11', label: 'Card 11' },
  { id: 'card-12', label: 'Card 12' },
  { id: 'card-13', label: 'Card 13' },
  { id: 'card-14', label: 'Card 14' },
];

// Pure logic, no DOM/Pendo dependency, per SKILL.md's project-layout
// guidance: this is the automatable seam, keep it unit-tested (see
// payload.test.js), not just exercised through the UI.
//
// Pendo enforces per-property and total event-size limits on
// pendo.track() payloads (SKILL.md fact 4). Truncate on a Unicode
// code-point boundary, not raw bytes, so multi-byte characters never get
// split mid-character.
const CARD_SORT_MAX_PROPERTY_LENGTH = 500;

function truncateUnicodeSafe(value, maxLength) {
  const codePoints = Array.from(String(value));
  if (codePoints.length <= maxLength) {
    return String(value);
  }
  return codePoints.slice(0, maxLength).join('');
}

function buildCardSortPayload(studyName, placements) {
  if (!studyName) {
    throw new Error('studyName is required');
  }
  if (!Array.isArray(placements)) {
    throw new Error('placements must be an array of { cardId, categoryId }');
  }

  const serialized = placements
    .map((p) => `${p.cardId}:${p.categoryId}`)
    .join(',');

  return {
    studyName,
    placementCount: placements.length,
    placements: truncateUnicodeSafe(serialized, CARD_SORT_MAX_PROPERTY_LENGTH),
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { buildCardSortPayload, truncateUnicodeSafe, CARD_SORT_MAX_PROPERTY_LENGTH };
}

// UI + Pendo wiring for the card-sort activity. Depends on data.js and
// payload.js being concatenated before this file (see build.config.json).
// Styling lives in styles.css (paste into Pendo's CSS tab); the root
// element lives in markup.html (paste into Pendo's HTML tab).
//
// Uses native HTML5 drag-and-drop, not a transform-based library, so the
// stacking-context bugs in SKILL.md facts 7/11 (specific to
// transform-positioned libraries like Muuri) do not apply here. If richer
// drag physics are needed, swap this for Muuri and apply
// references/muuri-drag-drop.md's three fixes.
const STUDY_NAME = 'card-sort-study'; // rename per study; see fact 5

function advanceToNextGuideStep() {
  if (typeof pendo === 'undefined' || typeof pendo.getActiveGuide !== 'function') {
    return;
  }
  const activeGuide = pendo.getActiveGuide();
  if (activeGuide && activeGuide.step && typeof activeGuide.step.advance === 'function') {
    activeGuide.step.advance();
  }
}

function initCardSort(root) {
  const cardsById = new Map(CARD_SORT_CARDS.map((c) => [c.id, c]));
  const categories = CARD_SORT_CATEGORIES.map((c) => ({ ...c }));

  // buckets['pool'] and buckets[categoryId] are ordered arrays of card
  // ids. New arrivals are unshifted (placed at the front) so a
  // newly-moved card is visible without scrolling; order otherwise
  // carries no meaning for this task.
  const buckets = { pool: CARD_SORT_CARDS.map((c) => c.id) };
  categories.forEach((c) => { buckets[c.id] = []; });

  let addCategoryFormOpen = false;
  let nextCategoryNumber = categories.length + 1;

  function findBucketOf(cardId) {
    return Object.keys(buckets).find((bucketId) => buckets[bucketId].includes(cardId));
  }

  function moveCard(cardId, targetBucketId) {
    const sourceBucketId = findBucketOf(cardId);
    if (!sourceBucketId || sourceBucketId === targetBucketId) return;
    buckets[sourceBucketId] = buckets[sourceBucketId].filter((id) => id !== cardId);
    buckets[targetBucketId].unshift(cardId);
    render();
  }

  function addCategory(label) {
    const trimmed = label.trim();
    if (!trimmed) return;
    const id = `cat-custom-${nextCategoryNumber++}`;
    categories.push({ id, label: trimmed });
    buckets[id] = [];
    addCategoryFormOpen = false;
    render();
  }

  function renameCategory(categoryId, newLabel) {
    const trimmed = newLabel.trim();
    const category = categories.find((c) => c.id === categoryId);
    if (category && trimmed) {
      category.label = trimmed;
    }
    render();
  }

  function makeCardEl(cardId) {
    const card = cardsById.get(cardId);
    const el = document.createElement('div');
    el.className = 'cs-card';
    el.textContent = card.label;
    el.draggable = true;
    el.dataset.cardId = cardId;
    el.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', cardId);
      el.classList.add('cs-dragging');
    });
    el.addEventListener('dragend', () => el.classList.remove('cs-dragging'));
    return el;
  }

  function makeDroppable(el, bucketId) {
    el.addEventListener('dragover', (e) => {
      e.preventDefault();
      el.classList.add('cs-drop-hover');
    });
    el.addEventListener('dragleave', () => el.classList.remove('cs-drop-hover'));
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      el.classList.remove('cs-drop-hover');
      const cardId = e.dataTransfer.getData('text/plain');
      moveCard(cardId, bucketId);
    });
  }

  function render() {
    root.innerHTML = '';

    const layout = document.createElement('div');
    layout.className = 'cs-layout';

    // Left panel: unplaced cards.
    const poolPanel = document.createElement('div');
    poolPanel.className = 'cs-panel cs-pool-panel';
    poolPanel.innerHTML = '<p class="cs-panel-title">Cards</p>';
    const poolList = document.createElement('div');
    poolList.className = 'cs-pool-list';
    buckets.pool.forEach((cardId) => poolList.appendChild(makeCardEl(cardId)));
    makeDroppable(poolList, 'pool');
    poolPanel.appendChild(poolList);
    layout.appendChild(poolPanel);

    // Right panel: categories, top-aligned, horizontally scrollable.
    const categoriesPanel = document.createElement('div');
    categoriesPanel.className = 'cs-categories-panel';

    categories.forEach((category) => {
      const colEl = document.createElement('div');
      colEl.className = 'cs-category';

      const header = document.createElement('div');
      header.className = 'cs-category-header';

      const labelEl = document.createElement('span');
      labelEl.className = 'cs-category-label';
      labelEl.textContent = category.label;
      labelEl.title = 'Click to rename';
      labelEl.tabIndex = 0;
      const startEditing = () => {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'cs-category-label-input';
        input.value = category.label;
        header.replaceChild(input, labelEl);
        input.focus();
        input.select();
        input.addEventListener('blur', () => renameCategory(category.id, input.value));
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') input.blur();
          if (e.key === 'Escape') {
            input.value = category.label;
            input.blur();
          }
        });
      };
      labelEl.addEventListener('click', startEditing);
      labelEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') startEditing();
      });

      const countEl = document.createElement('span');
      countEl.className = 'cs-category-count';
      countEl.textContent = String(buckets[category.id].length);

      header.appendChild(labelEl);
      header.appendChild(countEl);
      colEl.appendChild(header);

      const body = document.createElement('div');
      body.className = 'cs-category-body';
      buckets[category.id].forEach((cardId) => body.appendChild(makeCardEl(cardId)));
      makeDroppable(body, category.id);
      colEl.appendChild(body);

      categoriesPanel.appendChild(colEl);
    });

    layout.appendChild(categoriesPanel);
    root.appendChild(layout);

    // Footer: add-category control on the left, submit on the right.
    const footer = document.createElement('div');
    footer.className = 'cs-footer';

    const footerLeft = document.createElement('div');
    footerLeft.className = 'cs-footer-left';
    if (addCategoryFormOpen) {
      const input = document.createElement('input');
      input.type = 'text';
      input.placeholder = 'Category name';
      const addBtn = document.createElement('button');
      addBtn.className = 'cs-btn cs-btn-primary';
      addBtn.textContent = 'Add';
      addBtn.addEventListener('click', () => addCategory(input.value));
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') addCategory(input.value);
      });
      const cancelBtn = document.createElement('button');
      cancelBtn.className = 'cs-btn cs-btn-secondary';
      cancelBtn.textContent = 'Cancel';
      cancelBtn.addEventListener('click', () => {
        addCategoryFormOpen = false;
        render();
      });
      footerLeft.appendChild(input);
      footerLeft.appendChild(addBtn);
      footerLeft.appendChild(cancelBtn);
      setTimeout(() => input.focus(), 0);
    } else {
      const addBtn = document.createElement('button');
      addBtn.className = 'cs-btn cs-btn-secondary';
      addBtn.type = 'button';
      addBtn.textContent = '+ Add category';
      addBtn.addEventListener('click', () => {
        addCategoryFormOpen = true;
        render();
      });
      footerLeft.appendChild(addBtn);
    }
    footer.appendChild(footerLeft);

    const submitBtn = document.createElement('button');
    submitBtn.className = 'cs-btn cs-btn-primary';
    submitBtn.textContent = 'Submit';
    submitBtn.disabled = buckets.pool.length > 0;
    submitBtn.addEventListener('click', () => {
      const placementList = [];
      categories.forEach((category) => {
        buckets[category.id].forEach((cardId) => {
          placementList.push({ cardId, categoryId: category.id });
        });
      });
      const payload = buildCardSortPayload(STUDY_NAME, placementList);
      if (typeof pendo !== 'undefined' && typeof pendo.track === 'function') {
        pendo.track('card_sort_completed', payload);
      }
      advanceToNextGuideStep();
    });
    footer.appendChild(submitBtn);
    root.appendChild(footer);
  }

  render();
}

document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('card-sort-root');
  if (root) {
    initCardSort(root);
  }
});
})();
