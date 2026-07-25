/**
 * Mock `window.pendo` for local preview of a Code Block's UI/interaction
 * logic ONLY. Load this before the built Code Block script in a local
 * preview harness (see assets/*-template/preview.html).
 *
 * SCOPE WARNING: this validates layout, styling, and interaction logic
 * (drag-and-drop, card rendering, choice state) since those do not depend
 * on the real Pendo sandbox. It does NOT validate anything SKILL.md's
 * diagnostic methodology requires the real staged guide for:
 *   - whether pendo.track() calls actually land in Data Explorer (they do
 *     not, even against the real Pendo agent, until the guide is staged)
 *   - real multi-step advance behavior (.step.advance(), goToStep())
 *   - the Design-Studio-editor const/IIFE re-run quirk
 *   - Muuri stacking-context / dragContainer bugs specific to the real
 *     sandboxed iframe (facts 7 and 11 were confirmed in the live guide;
 *     re-confirm any drag-and-drop fix in the real guide before shipping)
 *
 * A study that "works" against this mock is ready for real-guide testing.
 * It is not ready to ship until it has also been verified live, per fact 1.
 */
(function (global) {
  'use strict';

  const trackLog = [];

  const mockGuide = {
    steps: [{ id: 'mock-step' }],
    guide: { steps: [{ id: 'mock-step' }] },
    step: {
      advance() {
        console.log('[mock-pendo] step.advance() called');
      },
    },
  };

  global.pendo = {
    dom() {
      return null;
    },
    designerEnabled: false,
    track(eventName, propertiesObject) {
      trackLog.push({ eventName, propertiesObject, at: new Date().toISOString() });
      console.log('[mock-pendo] track:', eventName, propertiesObject);
    },
    getActiveGuide() {
      return mockGuide;
    },
    goToStep(_guide, stepId) {
      console.log('[mock-pendo] goToStep() called with', stepId, '(no-op in mock)');
    },
    onGuideDismissed(callback) {
      if (typeof callback === 'function') {
        console.log('[mock-pendo] onGuideDismissed(callback) registered (no-op in mock)');
        return;
      }
      console.log('[mock-pendo] onGuideDismissed() called with no arguments, guide dismissed (mock)');
    },
    showGuideById() {
      console.log('[mock-pendo] showGuideById() called (no-op in mock)');
    },
    _mock: {
      trackLog,
    },
  };
})(window);
