(function () {
'use strict';

// Replace with a real study question and items before shipping. Each
// trial shows ITEMS_PER_TRIAL items pulled from MAXDIFF_ITEMS; a real
// study should use a balanced incomplete block design, this template uses
// a simple random draw as a placeholder.
const MAXDIFF_QUESTION = 'Which of the problems would you say are your highest and lowest priority to address?';

const MAXDIFF_ITEMS = [
  { id: 'item-1', label: 'Finding product-market fit for a new product/feature is an ongoing challenge' },
  { id: 'item-2', label: "It's difficult to get everyone to agree on the product roadmap" },
  { id: 'item-3', label: "I am stuck working on a product I don't believe in" },
  { id: 'item-4', label: 'Aligning the whole team around a shared mission is difficult' },
  { id: 'item-5', label: 'We lack the data we need to make confident product decisions' },
  { id: 'item-6', label: 'Cross-team dependencies slow down every release' },
];

const ITEMS_PER_TRIAL = 4;

// Trial count scales with item count rather than being a fixed number:
// each item should appear MIN_APPEARANCES_PER_ITEM times minimum across
// the whole sequence (a common MaxDiff rule of thumb is 3-5 appearances
// per item for a stable best-worst estimate). This is still a stand-in
// for a real balanced incomplete block design, which would also control
// which items co-occur, not just how many times each appears.
const MIN_APPEARANCES_PER_ITEM = 4;
const TRIAL_COUNT = Math.ceil((MIN_APPEARANCES_PER_ITEM * MAXDIFF_ITEMS.length) / ITEMS_PER_TRIAL);

// Pure logic, no DOM/Pendo dependency, per SKILL.md's project-layout
// guidance: this is the automatable seam, keep it unit-tested (see
// payload.test.js).
//
// Unlike the card-sort payload, this is fixed-size (a trial index plus a
// small, bounded set of item ids), so it needs no truncation (fact 4).
// Instead it needs cross-field invariant validation: best and worst must
// both be shown in the trial, and must not be the same item, per the
// UI-level invariant the skill's layout guidance calls out as a second
// line of defense, not just enforced in the UI.
function buildMaxDiffScreenPayload(studyName, trialIndex, shownItemIds, bestItemId, worstItemId) {
  if (!studyName) {
    throw new Error('studyName is required');
  }
  if (!Array.isArray(shownItemIds) || shownItemIds.length === 0) {
    throw new Error('shownItemIds must be a non-empty array');
  }
  if (!shownItemIds.includes(bestItemId)) {
    throw new Error('bestItemId must be one of the shown items');
  }
  if (!shownItemIds.includes(worstItemId)) {
    throw new Error('worstItemId must be one of the shown items');
  }
  if (bestItemId === worstItemId) {
    throw new Error('bestItemId and worstItemId must differ');
  }

  return {
    studyName,
    trialIndex,
    shownItemCount: shownItemIds.length,
    bestItemId,
    worstItemId,
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { buildMaxDiffScreenPayload };
}

// UI + Pendo wiring for the MaxDiff (best-worst scaling) activity.
// Depends on data.js and payload.js being concatenated before this file.
// Styling lives in styles.css (paste into Pendo's CSS tab); the root
// element lives in markup.html (paste into Pendo's HTML tab).
//
// Per SKILL.md fact 8: this repeated-trial task stays inside one Code
// Block step. State (current trial index) lives in JS here, not as
// separate guide steps, and .step.advance() is called once after the
// entire sequence finishes, not between individual trials. Each trial's
// own track event still fires as it completes.
const STUDY_NAME = 'maxdiff-study'; // rename per study; see fact 5

function advanceToNextGuideStep() {
  if (typeof pendo === 'undefined' || typeof pendo.getActiveGuide !== 'function') {
    return;
  }
  const activeGuide = pendo.getActiveGuide();
  if (activeGuide && activeGuide.step && typeof activeGuide.step.advance === 'function') {
    activeGuide.step.advance();
  }
}

function pickTrialItems() {
  const shuffled = [...MAXDIFF_ITEMS].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, ITEMS_PER_TRIAL);
}

function initMaxDiff(root) {
  let trialIndex = 0;
  let selectedBest = null;
  let selectedWorst = null;
  let currentItems = pickTrialItems();

  function selectBest(itemId) {
    selectedBest = itemId;
    // An item can't be both highest and lowest priority in the same
    // trial; the radio the user just picked wins the conflict.
    if (selectedWorst === itemId) selectedWorst = null;
    render();
  }

  function selectWorst(itemId) {
    selectedWorst = itemId;
    if (selectedBest === itemId) selectedBest = null;
    render();
  }

  function submitTrial() {
    const shownItemIds = currentItems.map((i) => i.id);
    const payload = buildMaxDiffScreenPayload(
      STUDY_NAME,
      trialIndex,
      shownItemIds,
      selectedBest,
      selectedWorst
    );
    if (typeof pendo !== 'undefined' && typeof pendo.track === 'function') {
      pendo.track('maxdiff_trial_completed', payload);
    }

    trialIndex += 1;
    if (trialIndex >= TRIAL_COUNT) {
      advanceToNextGuideStep();
      return;
    }
    selectedBest = null;
    selectedWorst = null;
    currentItems = pickTrialItems();
    render();
  }

  function render() {
    root.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'md-card';

    const progress = document.createElement('p');
    progress.className = 'md-progress';
    progress.textContent = `Question ${trialIndex + 1} of ${TRIAL_COUNT}`;
    card.appendChild(progress);

    const question = document.createElement('p');
    question.className = 'md-question';
    question.textContent = MAXDIFF_QUESTION;
    card.appendChild(question);

    const table = document.createElement('div');
    table.className = 'md-table';

    const blankHeader = document.createElement('div');
    const highestHeader = document.createElement('div');
    highestHeader.className = 'md-header-cell md-header-highest';
    highestHeader.textContent = 'Highest Priority';
    const lowestHeader = document.createElement('div');
    lowestHeader.className = 'md-header-cell md-header-lowest';
    lowestHeader.textContent = 'Lowest Priority';
    table.appendChild(highestHeader);
    table.appendChild(blankHeader);
    table.appendChild(lowestHeader);

    currentItems.forEach((item) => {
      const row = document.createElement('div');
      row.className = 'md-row';

      const bestCell = document.createElement('div');
      bestCell.className = 'md-radio-cell';
      const bestRadio = document.createElement('input');
      bestRadio.type = 'radio';
      bestRadio.name = 'md-best';
      bestRadio.checked = selectedBest === item.id;
      bestRadio.disabled = selectedWorst === item.id;
      bestRadio.addEventListener('change', () => selectBest(item.id));
      bestCell.appendChild(bestRadio);

      const labelCell = document.createElement('div');
      labelCell.className = 'md-label-cell';
      labelCell.textContent = item.label;

      const worstCell = document.createElement('div');
      worstCell.className = 'md-radio-cell';
      const worstRadio = document.createElement('input');
      worstRadio.type = 'radio';
      worstRadio.name = 'md-worst';
      worstRadio.checked = selectedWorst === item.id;
      worstRadio.disabled = selectedBest === item.id;
      worstRadio.addEventListener('change', () => selectWorst(item.id));
      worstCell.appendChild(worstRadio);

      row.appendChild(bestCell);
      row.appendChild(labelCell);
      row.appendChild(worstCell);
      table.appendChild(row);
    });

    card.appendChild(table);
    root.appendChild(card);

    const footer = document.createElement('div');
    footer.className = 'md-footer';
    const nextBtn = document.createElement('button');
    nextBtn.className = 'md-btn';
    nextBtn.textContent = trialIndex + 1 >= TRIAL_COUNT ? 'Submit' : 'Next';
    nextBtn.disabled = !(selectedBest && selectedWorst);
    nextBtn.addEventListener('click', submitTrial);
    footer.appendChild(nextBtn);
    root.appendChild(footer);
  }

  render();
}

document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('maxdiff-root');
  if (root) {
    initMaxDiff(root);
  }
});
})();
