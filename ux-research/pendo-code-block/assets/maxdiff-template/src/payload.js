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
