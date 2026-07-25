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
