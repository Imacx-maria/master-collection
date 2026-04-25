/**
 * paste-guard.js — Paste interception and class conflict detection
 *
 * Intercepts @webflow/XscpData paste events on the Designer canvas.
 * Detects class name conflicts with existing site styles via canvas CSSOM.
 * Shows a toast overlay with resolution options.
 */

// eslint-disable-next-line no-var
var PasteGuard = (function () {
  'use strict';

  var _enabled = false;
  var _toastEl = null;

  // ─── Style Discovery ─────────────────────────────────────

  /**
   * Get existing class names from the Designer canvas iframe CSSOM.
   * Walks all iframes (Webflow uses iframes for the canvas) and reads
   * CSS rules to extract class names.
   * Returns a Set of class name strings.
   */
  function getCanvasClassNames() {
    var names = new Set();
    var iframes = document.querySelectorAll('iframe');

    for (var i = 0; i < iframes.length; i++) {
      var doc;
      try { doc = iframes[i].contentDocument; }
      catch (e) { continue; }
      if (!doc) continue;

      try {
        for (var s = 0; s < doc.styleSheets.length; s++) {
          var rules;
          try { rules = doc.styleSheets[s].cssRules; }
          catch (e) { continue; }

          for (var r = 0; r < rules.length; r++) {
            var sel = rules[r].selectorText;
            if (!sel) continue;
            var matches = sel.match(/\.([\w-]+)/g);
            if (matches) {
              for (var m = 0; m < matches.length; m++) {
                names.add(matches[m].substring(1));
              }
            }
          }
        }
      } catch (e) { /* cross-origin or security error */ }
    }

    return names;
  }

  // ─── XscpData Parsing ─────────────────────────────────────

  /**
   * Parse clipboard text as @webflow/XscpData.
   * Returns the parsed object or null if not valid XscpData.
   */
  function parseXscpData(text) {
    try {
      var parsed = JSON.parse(text);
      if (parsed && parsed.type === '@webflow/XscpData' && parsed.payload) {
        return parsed;
      }
    } catch (e) { /* not JSON */ }
    return null;
  }

  /**
   * Extract style names from XscpData payload.
   * Returns an array of style name strings.
   */
  function getPayloadStyleNames(payload) {
    var styles = payload.styles;
    if (!styles || !Array.isArray(styles)) return [];
    return styles
      .filter(function (s) { return s.name && s._id; })
      .map(function (s) { return s.name; });
  }

  /**
   * Strip cross-site CMS field bindings from all nodes.
   * These contain field IDs from the source site and are invalid on target.
   * Returns count of stripped nodes.
   */
  function stripCmsBindings(payload) {
    var stripped = 0;
    var nodes = payload.nodes;
    if (!nodes || !Array.isArray(nodes)) return stripped;

    for (var i = 0; i < nodes.length; i++) {
      var data = nodes[i].data;
      if (data && data.dyn && data.dyn.bind !== undefined) {
        delete data.dyn.bind;
        stripped++;
      }
    }
    return stripped;
  }

  // ─── Conflict Detection ───────────────────────────────────

  /**
   * Find style names from payload that already exist on the site.
   * Returns array of conflicting name strings.
   */
  function detectConflicts(payloadStyleNames, existingNames) {
    var conflicts = [];
    for (var i = 0; i < payloadStyleNames.length; i++) {
      if (existingNames.has(payloadStyleNames[i])) {
        conflicts.push(payloadStyleNames[i]);
      }
    }
    return conflicts;
  }

  // ─── Toast Overlay ────────────────────────────────────────

  /**
   * Inject toast CSS into the Designer page (once).
   */
  function injectStyles() {
    if (document.getElementById('fg-paste-guard-styles')) return;

    var style = document.createElement('style');
    style.id = 'fg-paste-guard-styles';
    style.textContent = [
      '#fg-toast {',
      '  position: fixed;',
      '  top: 12px;',
      '  left: 50%;',
      '  transform: translateX(-50%);',
      '  z-index: 2147483647;',
      '  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
      '  font-size: 13px;',
      '  padding: 10px 16px;',
      '  display: flex;',
      '  align-items: center;',
      '  gap: 10px;',
      '  box-shadow: 0 8px 24px rgba(0,0,0,0.18);',
      '  animation: fg-slide-in 0.2s ease;',
      '}',
      '#fg-toast.fg-clean {',
      '  background: #f0fdf4;',
      '  color: #15803d;',
      '  border: 1px solid rgba(21,128,61,0.35);',
      '}',
      '#fg-toast.fg-conflict {',
      '  background: #ffffff;',
      '  color: #0a0a0a;',
      '  border: 1px solid #e5e5e5;',
      '}',
      '#fg-toast .fg-label {',
      '  font-weight: 600;',
      '  white-space: nowrap;',
      '}',
      '#fg-toast .fg-btn {',
      '  padding: 5px 12px;',
      '  border: 1px solid #e5e5e5;',
      '  font-size: 12px;',
      '  font-weight: 600;',
      '  cursor: pointer;',
      '  white-space: nowrap;',
      '}',
      '#fg-toast .fg-btn-primary {',
      '  background: #0a0a0a;',
      '  color: #ffffff;',
      '  border-color: #0a0a0a;',
      '}',
      '#fg-toast .fg-btn-primary:hover {',
      '  opacity: 0.9;',
      '}',
      '#fg-toast .fg-btn-ghost {',
      '  background: #ffffff;',
      '  color: #0a0a0a;',
      '}',
      '#fg-toast .fg-btn-ghost:hover {',
      '  background: #f5f5f5;',
      '}',
      '#fg-toast .fg-btn-dismiss {',
      '  background: none;',
      '  border: none;',
      '  color: #666;',
      '  font-size: 11px;',
      '  cursor: pointer;',
      '  padding: 2px 6px;',
      '}',
      '#fg-toast .fg-btn-dismiss:hover {',
      '  color: #aaa;',
      '}',
      '@keyframes fg-slide-in {',
      '  from { opacity: 0; transform: translateX(-50%) translateY(-8px); }',
      '  to { opacity: 1; transform: translateX(-50%) translateY(0); }',
      '}',
      '@keyframes fg-fade-out {',
      '  from { opacity: 1; }',
      '  to { opacity: 0; }',
      '}',
    ].join('\n');

    document.head.appendChild(style);
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function removeToast() {
    if (_toastEl && _toastEl.parentNode) {
      _toastEl.parentNode.removeChild(_toastEl);
    }
    _toastEl = null;
  }

  /**
   * Show a brief green toast for clean pastes.
   * Auto-fades after 2 seconds.
   */
  function showCleanToast(cmsStripped) {
    removeToast();
    injectStyles();

    var toast = document.createElement('div');
    toast.id = 'fg-toast';
    toast.className = 'fg-clean';

    var msg = '\u2713 Paste Guard: clean';
    if (cmsStripped > 0) {
      msg += ' (' + cmsStripped + ' CMS binding' + (cmsStripped > 1 ? 's' : '') + ' stripped)';
    }

    toast.innerHTML = '<span class="fg-label">' + escapeHtml(msg) + '</span>';
    document.body.appendChild(toast);
    _toastEl = toast;

    setTimeout(function () {
      if (_toastEl === toast) {
        toast.style.animation = 'fg-fade-out 0.3s ease forwards';
        setTimeout(function () { removeToast(); }, 300);
      }
    }, 2000);
  }

  /**
   * Show conflict toast with action buttons.
   * Stays visible until user clicks an option.
   */
  function showConflictToast(count, onReuse, onKeepNew, onDismiss) {
    removeToast();
    injectStyles();

    var toast = document.createElement('div');
    toast.id = 'fg-toast';
    toast.className = 'fg-conflict';

    var label = document.createElement('span');
    label.className = 'fg-label';
    label.textContent = count + ' class conflict' + (count > 1 ? 's' : '');

    var btnReuse = document.createElement('button');
    btnReuse.className = 'fg-btn fg-btn-primary';
    btnReuse.textContent = 'Reuse Existing';
    btnReuse.addEventListener('click', function () { removeToast(); onReuse(); });

    var btnKeep = document.createElement('button');
    btnKeep.className = 'fg-btn fg-btn-ghost';
    btnKeep.textContent = 'Keep New';
    btnKeep.addEventListener('click', function () { removeToast(); onKeepNew(); });

    var btnDismiss = document.createElement('button');
    btnDismiss.className = 'fg-btn-dismiss';
    btnDismiss.textContent = 'Dismiss';
    btnDismiss.addEventListener('click', function () { removeToast(); onDismiss(); });

    toast.appendChild(label);
    toast.appendChild(btnReuse);
    toast.appendChild(btnKeep);
    toast.appendChild(btnDismiss);
    document.body.appendChild(toast);
    _toastEl = toast;
  }

  /**
   * Show a brief informational toast that auto-fades.
   */
  function showBriefToast(message) {
    removeToast();
    injectStyles();

    var toast = document.createElement('div');
    toast.id = 'fg-toast';
    toast.className = 'fg-clean';
    toast.innerHTML = '<span class="fg-label">' + escapeHtml(message) + '</span>';
    document.body.appendChild(toast);
    _toastEl = toast;

    setTimeout(function () {
      if (_toastEl === toast) {
        toast.style.animation = 'fg-fade-out 0.3s ease forwards';
        setTimeout(function () { removeToast(); }, 300);
      }
    }, 2500);
  }

  // ─── Clipboard Write ──────────────────────────────────────

  /**
   * Write JSON string to clipboard using copy event interception.
   * Sets both application/json and text/plain MIME types so Webflow
   * can read the data on subsequent paste.
   */
  function writeToClipboard(jsonStr) {
    var copyHandler = function (event) {
      event.clipboardData.setData('application/json', jsonStr);
      event.clipboardData.setData('text/plain', jsonStr);
      event.preventDefault();
      document.removeEventListener('copy', copyHandler, true);
    };
    document.addEventListener('copy', copyHandler, true);
    document.execCommand('copy');
  }

  // ─── Paste Listener ───────────────────────────────────────

  /**
   * Main paste event handler. Registered on document in capture phase
   * so it fires before any other paste handlers (including Webflow's).
   */
  function onPaste(event) {
    if (!_enabled) return;

    // Skip text inputs — don't intercept typing in search bars, etc.
    var target = event.target;
    if (target && (
      target.tagName === 'INPUT' ||
      target.tagName === 'TEXTAREA' ||
      target.isContentEditable
    )) return;

    // Read clipboard data
    var clipText = '';
    if (event.clipboardData) {
      clipText = event.clipboardData.getData('application/json') ||
                 event.clipboardData.getData('text/plain') || '';
    }
    if (!clipText) return;

    // Parse as XscpData — ignore non-Webflow pastes
    var xscp = parseXscpData(clipText);
    if (!xscp) return;

    var payload = xscp.payload;
    var payloadStyleNames = getPayloadStyleNames(payload);

    // Strip CMS bindings (always — JSON-only, safe)
    var cmsStripped = stripCmsBindings(payload);

    // If no styles to check, show clean toast
    // Re-write clipboard only if CMS bindings were stripped
    if (payloadStyleNames.length === 0) {
      if (cmsStripped > 0) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var strippedJson = JSON.stringify(xscp);
        writeToClipboard(strippedJson);
        window.postMessage({
          type: 'FG_PASTE_GUARD_RESOLVED',
          xscpJson: strippedJson
        }, '*');
        showCleanToast(cmsStripped);
      }
      return;
    }

    // Get existing class names from canvas CSSOM
    var existingNames = getCanvasClassNames();
    var conflicts = detectConflicts(payloadStyleNames, existingNames);

    if (conflicts.length === 0) {
      // No conflicts — rewrite clipboard if CMS bindings were stripped
      if (cmsStripped > 0) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var cleanJson = JSON.stringify(xscp);
        writeToClipboard(cleanJson);
        window.postMessage({
          type: 'FG_PASTE_GUARD_RESOLVED',
          xscpJson: cleanJson
        }, '*');
      }
      showCleanToast(cmsStripped);
      return;
    }

    // ── Conflicts found — block paste, show resolution toast ──

    event.preventDefault();
    event.stopImmediatePropagation();

    showConflictToast(
      conflicts.length,

      // onReuse: keep existing classes — write CMS-stripped version
      // Webflow will merge by name when IDs differ
      function () {
        var resolvedJson = JSON.stringify(xscp);
        writeToClipboard(resolvedJson);
        window.postMessage({
          type: 'FG_PASTE_GUARD_RESOLVED',
          xscpJson: resolvedJson
        }, '*');
        showBriefToast('\u2713 ' + conflicts.length + ' existing classes kept');
      },

      // onKeepNew: restore original clipboard, Webflow auto-renames with suffix
      function () {
        writeToClipboard(clipText);
        window.postMessage({
          type: 'FG_PASTE_GUARD_RESOLVED',
          xscpJson: clipText
        }, '*');
        showBriefToast('Original kept \u2014 pasting with Webflow rename');
      },

      // onDismiss: do nothing, paste was already blocked
      function () { /* user chose to cancel */ }
    );
  }

  // ─── Enable / Disable ─────────────────────────────────────

  function enable() {
    if (_enabled) return;
    _enabled = true;
    document.addEventListener('paste', onPaste, true);
    console.log('[Master Collection] Paste Guard enabled');
  }

  function disable() {
    if (!_enabled) return;
    _enabled = false;
    document.removeEventListener('paste', onPaste, true);
    removeToast();
    console.log('[Master Collection] Paste Guard disabled');
  }

  function isEnabled() {
    return _enabled;
  }

  // ─── Public API ────────────────────────────────────────────

  return {
    enable: enable,
    disable: disable,
    isEnabled: isEnabled,
    getCanvasClassNames: getCanvasClassNames,
  };
})();
