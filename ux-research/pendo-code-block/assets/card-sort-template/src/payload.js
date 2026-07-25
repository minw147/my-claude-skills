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
