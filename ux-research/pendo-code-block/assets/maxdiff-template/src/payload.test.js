const test = require('node:test');
const assert = require('node:assert/strict');
const { buildMaxDiffScreenPayload } = require('./payload.js');

const SHOWN = ['item-1', 'item-2', 'item-3', 'item-4'];

test('requires a studyName', () => {
  assert.throws(
    () => buildMaxDiffScreenPayload('', 0, SHOWN, 'item-1', 'item-2'),
    /studyName is required/
  );
});

test('requires a non-empty shownItemIds array', () => {
  assert.throws(
    () => buildMaxDiffScreenPayload('study-1', 0, [], 'item-1', 'item-2'),
    /non-empty array/
  );
});

test('rejects a bestItemId not in the shown set', () => {
  assert.throws(
    () => buildMaxDiffScreenPayload('study-1', 0, SHOWN, 'item-99', 'item-2'),
    /bestItemId must be one of the shown items/
  );
});

test('rejects a worstItemId not in the shown set', () => {
  assert.throws(
    () => buildMaxDiffScreenPayload('study-1', 0, SHOWN, 'item-1', 'item-99'),
    /worstItemId must be one of the shown items/
  );
});

test('rejects best and worst being the same item', () => {
  assert.throws(
    () => buildMaxDiffScreenPayload('study-1', 0, SHOWN, 'item-1', 'item-1'),
    /must differ/
  );
});

test('builds a valid fixed-shape payload', () => {
  const payload = buildMaxDiffScreenPayload('study-1', 2, SHOWN, 'item-1', 'item-3');
  assert.deepStrictEqual(payload, {
    studyName: 'study-1',
    trialIndex: 2,
    shownItemCount: 4,
    bestItemId: 'item-1',
    worstItemId: 'item-3',
  });
});
