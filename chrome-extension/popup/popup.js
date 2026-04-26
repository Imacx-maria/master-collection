/**
 * popup.js — Popup UI logic and messaging to content script
 *
 * Modes: 'all' (every interaction), 'page' (on this page), 'unused' (not on this page)
 */

(function () {
  'use strict';

  // ─── Elements ──────────────────────────────────────────────

  var stateNotDesigner = document.getElementById('state-not-designer');
  var stateScanning    = document.getElementById('state-scanning');
  var stateResults     = document.getElementById('state-results');
  var stateConfirm     = document.getElementById('state-confirm');
  var stateDeleting    = document.getElementById('state-deleting');
  var stateDone        = document.getElementById('state-done');
  var stateError       = document.getElementById('state-error');

  var modeAll    = document.getElementById('mode-all');
  var modePage   = document.getElementById('mode-page');
  var modeUnused = document.getElementById('mode-unused');
  var countAll   = document.getElementById('count-all');
  var countPage  = document.getElementById('count-page');
  var countUnused = document.getElementById('count-unused');
  var ixPreview  = document.getElementById('ix-preview');
  var btnRescan  = document.getElementById('btn-rescan');

  var confirmCount = document.getElementById('confirm-count');
  var confirmScope = document.getElementById('confirm-scope');
  var btnConfirmYes = document.getElementById('btn-confirm-yes');
  var btnConfirmNo  = document.getElementById('btn-confirm-no');

  var progressText   = document.getElementById('progress-text');
  var progressBar    = document.getElementById('progress-bar');
  var progressDetail = document.getElementById('progress-detail');
  var btnCancel      = document.getElementById('btn-cancel');

  var doneMessage = document.getElementById('done-message');
  var btnClose    = document.getElementById('btn-close');

  var errorMessage = document.getElementById('error-message');
  var btnRetry     = document.getElementById('btn-retry');

  // Paste Guard elements
  var stateGuard    = document.getElementById('state-guard');
  var guardToggle   = document.getElementById('guard-toggle');
  var guardStatus   = document.getElementById('guard-status');

  // Tab elements
  var tabIx    = document.getElementById('tab-ix');
  var tabGuard = document.getElementById('tab-guard');
  var themeToggle = document.getElementById('theme-toggle');

  var _scanData = null;   // { all, page, unused, names }
  var _activeTabId = null;
  var _selectedMode = null; // 'all' | 'page' | 'unused'
  var _contentReady = false;
  var _activeTab = 'guard'; // 'guard' | 'ix'
  var _themeMode = 'system'; // 'system' | 'light' | 'dark'

  var MODE_LABELS = {
    all:    'all',
    page:   'on-this-page',
    unused: 'unused',
  };

  var THEME_LABELS = {
    system: 'System',
    light: 'Light',
    dark: 'Dark',
  };

  function applyTheme(mode) {
    _themeMode = mode === 'light' || mode === 'dark' ? mode : 'system';
    if (_themeMode === 'system') {
      document.body.removeAttribute('data-theme');
    } else {
      document.body.setAttribute('data-theme', _themeMode);
    }
    themeToggle.textContent = THEME_LABELS[_themeMode];
    themeToggle.setAttribute('aria-label', 'Theme: ' + THEME_LABELS[_themeMode]);
  }

  function nextThemeMode(mode) {
    if (mode === 'system') return 'light';
    if (mode === 'light') return 'dark';
    return 'system';
  }

  function restoreTheme() {
    chrome.storage.local.get('masterCollectionCompanionTheme', function (data) {
      applyTheme(data.masterCollectionCompanionTheme || 'system');
    });
  }

  // ─── State Management ──────────────────────────────────────

  var ixStates = [
    stateNotDesigner, stateScanning, stateResults,
    stateConfirm, stateDeleting, stateDone, stateError,
  ];
  var allStates = ixStates.concat([stateGuard]);

  function showState(stateEl) {
    allStates.forEach(function (s) { s.hidden = true; });
    stateEl.hidden = false;
  }

  function switchTab(tab) {
    _activeTab = tab;

    tabIx.classList.toggle('active', tab === 'ix');
    tabGuard.classList.toggle('active', tab === 'guard');

    allStates.forEach(function (s) { s.hidden = true; });

    if (tab === 'ix') {
      if (!_contentReady) {
        showState(stateNotDesigner);
      } else if (_scanData) {
        showState(stateResults);
      } else {
        doScan();
      }
    } else if (tab === 'guard') {
      showState(stateGuard);
      if (_contentReady) {
        queryGuardStatus();
      }
    }
  }

  function queryGuardStatus() {
    sendToContent({ type: 'PASTE_GUARD_STATUS' }, function (res) {
      if (res.ok) {
        guardToggle.checked = res.enabled;
        updateGuardStatusText(res.enabled);
      }
    });
  }

  function updateGuardStatusText(enabled) {
    if (enabled) {
      guardStatus.textContent = 'Active - intercepting XscpData pastes.';
      guardStatus.classList.add('active');
    } else {
      guardStatus.textContent = 'Toggle on to guard pastes.';
      guardStatus.classList.remove('active');
    }
  }

  // ─── Tab Detection ─────────────────────────────────────────

  function getActiveDesignerTab(callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      if (tabs.length === 0) {
        callback(null);
        return;
      }

      var tab = tabs[0];
      if (tab.url && tab.url.match(/^https:\/\/.*\.design\.webflow\.com\/|^https:\/\/webflow\.com\/design\//)) {
        callback(tab);
      } else {
        callback(null);
      }
    });
  }

  // ─── Messaging ─────────────────────────────────────────────

  function sendToContent(msg, callback) {
    if (!_activeTabId) {
      callback({ ok: false, error: 'No active tab' });
      return;
    }

    chrome.tabs.sendMessage(_activeTabId, msg, function (response) {
      if (chrome.runtime.lastError) {
        callback({ ok: false, error: chrome.runtime.lastError.message });
        return;
      }
      callback(response || { ok: false, error: 'No response' });
    });
  }

  // ─── IX Actions ───────────────────────────────────────────

  function doScan() {
    showState(stateScanning);

    sendToContent({ type: 'SCAN' }, function (res) {
      if (!res.ok) {
        errorMessage.textContent = res.error || 'Scan failed';
        showState(stateError);
        return;
      }

      _scanData = {
        all:    res.all    || 0,
        page:   res.page   || 0,
        unused: res.unused || 0,
        names:  res.names  || { all: [], page: [], unused: [] },
      };

      // Update counts
      countAll.textContent   = _scanData.all;
      countPage.textContent  = _scanData.page;
      countUnused.textContent = _scanData.unused;

      // Enable/disable cards based on count
      modeAll.disabled    = _scanData.all === 0;
      modePage.disabled   = _scanData.page === 0;
      modeUnused.disabled = _scanData.unused === 0;

      // Hide preview until a mode is hovered/selected
      ixPreview.hidden = true;

      showState(stateResults);
    });
  }

  function showPreview(mode) {
    if (!_scanData || !_scanData.names[mode]) return;

    var names = _scanData.names[mode];
    ixPreview.innerHTML = '';

    var show = names.slice(0, 5);
    show.forEach(function (name) {
      var div = document.createElement('div');
      div.className = 'ix-name';
      div.textContent = name;
      ixPreview.appendChild(div);
    });

    if (names.length > 5) {
      var more = document.createElement('div');
      more.className = 'ix-more';
      more.textContent = '... and ' + (names.length - 5) + ' more';
      ixPreview.appendChild(more);
    }

    ixPreview.hidden = names.length === 0;
  }

  function startDelete(mode) {
    _selectedMode = mode;
    var count = _scanData[mode] || 0;

    confirmCount.textContent = count;
    confirmScope.textContent = MODE_LABELS[mode];
    showState(stateConfirm);
  }

  function doDelete() {
    var count = _scanData[_selectedMode] || 0;

    showState(stateDeleting);
    progressText.textContent = 'Deleting... 0/' + count;
    progressBar.style.width = '0%';
    progressDetail.textContent = '';
    btnCancel.disabled = false;
    btnCancel.textContent = 'Cancel';

    sendToContent(
      { type: 'DELETE_ALL', totalCount: count, mode: _selectedMode },
      function (res) {
        if (res.ok) {
          doneMessage.textContent =
            'Deleted ' + res.deleted + ' interaction' + (res.deleted !== 1 ? 's' : '') + '.';
          if (res.errors && res.errors.length > 0) {
            doneMessage.textContent +=
              ' (' + res.errors.length + ' error' + (res.errors.length !== 1 ? 's' : '') + ')';
          }
          showState(stateDone);
        } else {
          errorMessage.textContent = res.error || 'Delete failed';
          showState(stateError);
        }
      }
    );
  }

  // ─── Progress Listeners ────────────────────────────────────

  chrome.runtime.onMessage.addListener(function (msg) {
    if (msg.type === 'PROGRESS') {
      var pct = msg.total > 0 ? Math.round((msg.deleted / msg.total) * 100) : 0;
      progressText.textContent = 'Deleting... ' + msg.deleted + '/' + msg.total;
      progressBar.style.width = pct + '%';
      progressDetail.textContent = msg.detail || '';

      if (msg.status === 'done') {
        doneMessage.textContent =
          'Deleted ' + msg.deleted + ' interaction' + (msg.deleted !== 1 ? 's' : '') + '.';
        showState(stateDone);
      } else if (msg.status === 'cancelled') {
        doneMessage.textContent =
          'Cancelled. Deleted ' + msg.deleted + ' of ' + msg.total + '.';
        showState(stateDone);
      } else if (msg.status === 'error') {
        errorMessage.textContent = msg.detail || 'Error during deletion';
        showState(stateError);
      }
    }
  });

  // ─── Event Listeners ──────────────────────────────────────

  // Tab switching
  tabIx.addEventListener('click', function () { switchTab('ix'); });
  tabGuard.addEventListener('click', function () { switchTab('guard'); });
  themeToggle.addEventListener('click', function () {
    var nextMode = nextThemeMode(_themeMode);
    applyTheme(nextMode);
    chrome.storage.local.set({ masterCollectionCompanionTheme: nextMode });
  });

  // Guard toggle
  guardToggle.addEventListener('change', function () {
    var enabled = guardToggle.checked;
    var msgType = enabled ? 'PASTE_GUARD_ENABLE' : 'PASTE_GUARD_DISABLE';

    sendToContent({ type: msgType }, function (res) {
      if (res.ok) {
        updateGuardStatusText(res.enabled);
        // Persist preference
        chrome.storage.local.set({ pasteGuardEnabled: res.enabled });
      }
    });
  });

  // Mode cards — click to select and go to confirm
  modeAll.addEventListener('click', function () { startDelete('all'); });
  modePage.addEventListener('click', function () { startDelete('page'); });
  modeUnused.addEventListener('click', function () { startDelete('unused'); });

  // Hover preview
  modeAll.addEventListener('mouseenter', function () { showPreview('all'); });
  modePage.addEventListener('mouseenter', function () { showPreview('page'); });
  modeUnused.addEventListener('mouseenter', function () { showPreview('unused'); });

  btnConfirmYes.addEventListener('click', function () { doDelete(); });
  btnConfirmNo.addEventListener('click', function () { showState(stateResults); });

  btnRescan.addEventListener('click', function () { doScan(); });

  btnCancel.addEventListener('click', function () {
    sendToContent({ type: 'CANCEL' }, function () {});
    btnCancel.disabled = true;
    btnCancel.textContent = 'Cancelling...';
  });

  btnClose.addEventListener('click', function () { window.close(); });
  btnRetry.addEventListener('click', function () { doScan(); });

  // ─── Init ──────────────────────────────────────────────────

  restoreTheme();

  getActiveDesignerTab(function (tab) {
    if (!tab) {
      showState(stateNotDesigner);
      return;
    }

    _activeTabId = tab.id;

    sendToContent({ type: 'PING' }, function (res) {
      if (res.ok) {
        _contentReady = true;
        // Restore guard toggle from storage
        chrome.storage.local.get('pasteGuardEnabled', function (data) {
          guardToggle.checked = !!data.pasteGuardEnabled;
          updateGuardStatusText(!!data.pasteGuardEnabled);
        });
        switchTab('guard');
      } else {
        chrome.scripting.executeScript(
          {
            target: { tabId: _activeTabId },
            files: [
              'content/dom-discovery.js',
              'content/deletion-engine.js',
              'content/paste-guard.js',
              'content/content.js',
            ],
          },
          function () {
            if (chrome.runtime.lastError) {
              errorMessage.textContent =
                'Could not inject content script: ' + chrome.runtime.lastError.message;
              showState(stateError);
              return;
            }
            _contentReady = true;
            // Restore guard toggle from storage
            chrome.storage.local.get('pasteGuardEnabled', function (data) {
              guardToggle.checked = !!data.pasteGuardEnabled;
              updateGuardStatusText(!!data.pasteGuardEnabled);
            });
            setTimeout(function () { switchTab('guard'); }, 300);
          }
        );
      }
    });
  });
})();
