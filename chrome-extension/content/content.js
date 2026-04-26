/**
 * content.js — Message bridge between popup and content scripts
 *
 * Listens for messages from the popup and delegates to
 * DomDiscovery and DeletionEngine.
 */

(function () {
  'use strict';

  chrome.runtime.onMessage.addListener(function (msg, _sender, sendResponse) {
    switch (msg.type) {
      case 'PING':
        sendResponse({ ok: true });
        return false;

      case 'SCAN':
        handleScan(sendResponse);
        return false;

      case 'DELETE_ALL':
        handleDeleteAll(msg.totalCount, msg.mode, sendResponse);
        return true; // Keep channel open for async

      case 'CANCEL':
        DeletionEngine.cancel();
        sendResponse({ ok: true });
        return false;

      case 'PASTE_GUARD_ENABLE':
        PasteGuard.enable();
        sendResponse({ ok: true, enabled: true });
        return false;

      case 'PASTE_GUARD_DISABLE':
        PasteGuard.disable();
        sendResponse({ ok: true, enabled: false });
        return false;

      case 'PASTE_GUARD_STATUS':
        sendResponse({ ok: true, enabled: PasteGuard.isEnabled() });
        return false;

      default:
        sendResponse({ ok: false, error: 'Unknown message type' });
        return false;
    }
  });

  function handleScan(sendResponse) {
    try {
      var panel = DomDiscovery.findInteractionsPanel();
      if (!panel) {
        sendResponse({
          ok: false,
          error: 'Open the Interactions panel (lightning bolt icon) in the Designer for this to work.',
        });
        return;
      }

      var sections = DomDiscovery.scanAllSections(panel);
      sendResponse({
        ok: true,
        all:    sections.all,
        page:   sections.page,
        unused: sections.unused,
        names:  sections.names,
      });
    } catch (err) {
      sendResponse({ ok: false, error: err.message });
    }
  }

  function handleDeleteAll(totalCount, mode, sendResponse) {
    if (DeletionEngine.isRunning()) {
      sendResponse({ ok: false, error: 'Already running' });
      return;
    }

    mode = mode || 'all';

    DeletionEngine.deleteAll(totalCount, function (progress) {
      chrome.runtime.sendMessage({
        type: 'PROGRESS',
        status: progress.status,
        deleted: progress.deleted,
        total: progress.total,
        detail: progress.detail,
      });
    }, mode).then(function (result) {
      sendResponse({
        ok: true,
        deleted: result.deleted,
        errors: result.errors,
      });
    });
  }

  console.log('[Master Collection] Content script loaded on', window.location.href);

  // Auto-enable paste guard from saved preference
  try {
    chrome.storage.local.get('pasteGuardEnabled', function (data) {
      if (data.pasteGuardEnabled) {
        PasteGuard.enable();
      }
    });
  } catch (e) { /* storage unavailable */ }
})();
