/**
 * deletion-engine.js — Sequential interaction deletion with dual strategy
 *
 * Strategy A: React fiber → call onDelete() directly (fast, no UI flicker)
 * Strategy B: DOM click automation (fallback — reliable)
 *
 * Handles virtual scrolling, progress reporting, and cancellation.
 */

// eslint-disable-next-line no-var
var DeletionEngine = (function () {
  'use strict';

  let _cancelled = false;
  let _running = false;
  let _totalDeleted = 0;
  let _totalToDelete = 0;
  let _progressCallback = null;

  const MAX_CONSECUTIVE_FAILURES = 5;
  const MAX_EMPTY_SCROLL_ROUNDS = 3;
  const SETTLE_DELAY_MS = 400;

  // ─── Utilities ───────────────────────────────────────────────

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Wait for DOM to settle using MutationObserver.
   * Resolves when no mutations occur for `quietMs` or after `maxMs`.
   */
  function waitForDomSettle(quietMs, maxMs) {
    quietMs = quietMs || 300;
    maxMs = maxMs || 2000;

    return new Promise((resolve) => {
      let timer = null;
      let resolved = false;

      const done = () => {
        if (resolved) return;
        resolved = true;
        observer.disconnect();
        clearTimeout(maxTimer);
        clearTimeout(timer);
        resolve();
      };

      const observer = new MutationObserver(() => {
        clearTimeout(timer);
        timer = setTimeout(done, quietMs);
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
      });

      // Start the quiet timer immediately
      timer = setTimeout(done, quietMs);

      // Hard max timeout
      const maxTimer = setTimeout(done, maxMs);
    });
  }

  /**
   * Wait for an element matching a condition to appear.
   */
  function waitForElement(findFn, timeoutMs) {
    timeoutMs = timeoutMs || 3000;

    return new Promise((resolve) => {
      const el = findFn();
      if (el) {
        resolve(el);
        return;
      }

      let resolved = false;

      const observer = new MutationObserver(() => {
        if (resolved) return;
        const found = findFn();
        if (found) {
          resolved = true;
          observer.disconnect();
          clearTimeout(timer);
          resolve(found);
        }
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true,
      });

      const timer = setTimeout(() => {
        if (!resolved) {
          resolved = true;
          observer.disconnect();
          resolve(null);
        }
      }, timeoutMs);
    });
  }

  // ─── Strategy A: React Fiber ─────────────────────────────────

  /**
   * Attempt to delete via React fiber onDelete() call.
   * Returns true if successful, false otherwise.
   */
  function tryFiberDelete(button) {
    try {
      const info = DomDiscovery.getDeleteInfoFromButton(button);
      if (!info || typeof info.onDelete !== 'function') {
        return false;
      }

      // Call onDelete with the interaction ID if available
      if (info.interactionId) {
        info.onDelete(info.interactionId);
      } else {
        info.onDelete();
      }

      return true;
    } catch (err) {
      console.warn('[IX Cleaner] Fiber delete failed:', err.message);
      return false;
    }
  }

  // ─── Strategy B: DOM Click Automation ────────────────────────

  /**
   * Simulate a mouse click on an element.
   */
  function simulateClick(el) {
    if (!el) return;
    el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
    el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
    el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
  }

  /**
   * Attempt to delete via DOM click automation.
   * Click Actions → Delete menu item → Confirm dialog.
   * Returns true if successful, false otherwise.
   */
  async function tryDomClickDelete(button) {
    try {
      // Step 1: Click the Actions button to open context menu
      simulateClick(button);
      await sleep(200);

      // Step 2: Wait for and click "Delete" in the context menu
      const deleteItem = await waitForElement(
        () => DomDiscovery.findDeleteInContextMenu(),
        2000
      );

      if (!deleteItem) {
        // Try to dismiss any open menu
        document.body.click();
        await sleep(100);
        return false;
      }

      simulateClick(deleteItem);
      await sleep(200);

      // Step 3: Check for confirmation dialog
      const confirmBtn = await waitForElement(
        () => DomDiscovery.findConfirmDeleteButton(),
        1500
      );

      if (confirmBtn) {
        simulateClick(confirmBtn);
        await sleep(200);
      }

      // If no confirm dialog appeared, the delete may have happened directly
      return true;
    } catch (err) {
      console.warn('[IX Cleaner] DOM click delete failed:', err.message);
      // Try to dismiss any open menus
      document.body.click();
      await sleep(100);
      return false;
    }
  }

  // ─── Main Deletion Loop ──────────────────────────────────────

  /**
   * Report progress to the popup via callback.
   */
  function reportProgress(status, detail) {
    if (_progressCallback) {
      _progressCallback({
        status: status, // 'progress' | 'done' | 'error' | 'cancelled'
        deleted: _totalDeleted,
        total: _totalToDelete,
        detail: detail || '',
      });
    }
  }

  /**
   * Delete interactions in the panel.
   *
   * @param {number} totalCount - Expected total from scan
   * @param {function} onProgress - Callback for progress updates
   * @param {'all'|'page'|'unused'} mode - Which section to delete from
   * @returns {Promise<{deleted: number, errors: string[]}>}
   */
  async function deleteAll(totalCount, onProgress, mode) {
    mode = mode || 'all';
    if (_running) {
      return { deleted: 0, errors: ['Already running'] };
    }

    _running = true;
    _cancelled = false;
    _totalDeleted = 0;
    _totalToDelete = totalCount;
    _progressCallback = onProgress;

    const errors = [];
    let consecutiveFailures = 0;
    let emptyScrollRounds = 0;

    try {
      while (!_cancelled) {
        // Find the panel fresh each iteration (React may re-render)
        const panel = DomDiscovery.findInteractionsPanel();
        const buttons = DomDiscovery.findActionButtons(panel, mode);

        if (buttons.length === 0) {
          // No buttons visible — try scrolling to load more
          const scrollContainer = DomDiscovery.getScrollContainer(panel);
          const didScroll = await DomDiscovery.scrollToLoadMore(scrollContainer);

          if (didScroll) {
            await waitForDomSettle(300, 1000);
            const newButtons = DomDiscovery.findActionButtons(panel, mode);
            if (newButtons.length === 0) {
              emptyScrollRounds++;
              if (emptyScrollRounds >= MAX_EMPTY_SCROLL_ROUNDS) {
                break; // No more interactions
              }
              continue;
            }
            emptyScrollRounds = 0;
          } else {
            emptyScrollRounds++;
            if (emptyScrollRounds >= MAX_EMPTY_SCROLL_ROUNDS) {
              break; // Can't scroll further, no buttons — done
            }
            await sleep(300);
            continue;
          }

          continue; // Re-enter loop to get fresh buttons
        }

        emptyScrollRounds = 0;

        // Take the first button
        const button = buttons[0];
        const name = DomDiscovery.getInteractionName(button);

        // Strategy A: fiber delete
        let deleted = tryFiberDelete(button);

        if (!deleted) {
          // Strategy B: DOM click
          deleted = await tryDomClickDelete(button);
        }

        if (deleted) {
          _totalDeleted++;
          consecutiveFailures = 0;
          reportProgress('progress', 'Deleted: ' + name);

          // Wait for React to re-render the list
          await waitForDomSettle(SETTLE_DELAY_MS, 1500);
        } else {
          consecutiveFailures++;
          errors.push('Failed to delete: ' + name);

          if (consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
            reportProgress('error', 'Too many consecutive failures (' + MAX_CONSECUTIVE_FAILURES + '). Stopped.');
            break;
          }

          // Wait before retrying
          await sleep(500);
        }
      }

      if (_cancelled) {
        reportProgress('cancelled', 'Cancelled by user');
      } else {
        reportProgress('done', 'Finished');
      }
    } catch (err) {
      console.error('[IX Cleaner] Unexpected error:', err);
      errors.push('Unexpected error: ' + err.message);
      reportProgress('error', err.message);
    } finally {
      _running = false;
      _progressCallback = null;
    }

    return { deleted: _totalDeleted, errors: errors };
  }

  /**
   * Cancel the running deletion operation.
   */
  function cancel() {
    _cancelled = true;
  }

  /**
   * Check if the engine is currently running.
   */
  function isRunning() {
    return _running;
  }

  // ─── Public API ──────────────────────────────────────────────

  return {
    deleteAll,
    cancel,
    isRunning,
  };
})();
