const test = require('node:test');
const assert = require('node:assert/strict');
const { buildCardSortPayload, truncateUnicodeSafe, CARD_SORT_MAX_PROPERTY_LENGTH } = require('./payload.js');

test('buildCardSortPayload requires a studyName', () => {
  assert.throws(() => buildCardSortPayload('', []), /studyName is required/);
});

test('buildCardSortPayload requires placements to be an array', () => {
  assert.throws(() => buildCardSortPayload('study-1', null), /placements must be an array/);
});

test('buildCardSortPayload serializes placements in order', () => {
  const payload = buildCardSortPayload('study-1', [
    { cardId: 'card-1', categoryId: 'cat-1' },
    { cardId: 'card-2', categoryId: 'cat-2' },
  ]);
  assert.strictEqual(payload.studyName, 'study-1');
  assert.strictEqual(payload.placementCount, 2);
  assert.strictEqual(payload.placements, 'card-1:cat-1,card-2:cat-2');
});

test('truncateUnicodeSafe leaves short strings untouched', () => {
  assert.strictEqual(truncateUnicodeSafe('abc', 10), 'abc');
});

test('truncateUnicodeSafe truncates on a code-point boundary, not raw bytes', () => {
  // U+1F600 (grinning face) is a 4-byte UTF-8 / 2-UTF-16-code-unit character
  // but a single Unicode code point; Array.from must not split it.
  const emoji = '\u{1F600}';
  const input = 'a'.repeat(5) + emoji + 'b'.repeat(5);
  const truncated = truncateUnicodeSafe(input, 6);
  assert.strictEqual(truncated, 'a'.repeat(5) + emoji);
  assert.ok(!truncated.includes('�'), 'must not contain a replacement character from a split surrogate pair');
});

test('buildCardSortPayload truncates an oversized serialized string', () => {
  const placements = Array.from({ length: 200 }, (_, i) => ({
    cardId: `card-${i}`,
    categoryId: `cat-${i}`,
  }));
  const payload = buildCardSortPayload('study-1', placements);
  assert.ok(payload.placements.length <= CARD_SORT_MAX_PROPERTY_LENGTH);
  assert.strictEqual(payload.placementCount, 200, 'count reflects real placements, not the truncated string');
});
