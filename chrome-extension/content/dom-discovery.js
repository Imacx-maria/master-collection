/**
 * dom-discovery.js — Webflow Designer DOM selectors and React fiber walking
 *
 * Provides functions to locate the Interactions panel, find action buttons,
 * walk the React fiber tree, and extract interaction metadata.
 *
 * Supports section-aware scanning:
 *   'all'      — every interaction in the panel
 *   'page'     — only "On this page" section
 *   'unused'   — only "All interactions" section (not on this page)
 */

// eslint-disable-next-line no-var
var DomDiscovery = (function () {
  'use strict';

  // ─── Section Detection ─────────────────────────────────────

  /**
   * Find section header elements inside the Interactions panel.
   * Returns { allHeader, pageHeader } — either may be null.
   */
  function findSectionHeaders() {
    var result = { allHeader: null, pageHeader: null };

    // Look through all text-bearing elements for the two known headings
    var candidates = document.querySelectorAll(
      'h1, h2, h3, h4, h5, h6, span, div, p, [class*="Header"], [class*="header"], [class*="SectionTitle"], [class*="sectionTitle"]'
    );

    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      // Only consider elements whose direct text (not children's) matches
      var directText = getDirectTextContent(el).toLowerCase().trim();

      if (directText === 'all interactions' || directText === 'all animation') {
        result.allHeader = el;
      } else if (directText === 'on this page') {
        result.pageHeader = el;
      }
    }

    return result;
  }

  /**
   * Get only the direct text of an element (not nested children).
   */
  function getDirectTextContent(el) {
    var text = '';
    for (var i = 0; i < el.childNodes.length; i++) {
      if (el.childNodes[i].nodeType === Node.TEXT_NODE) {
        text += el.childNodes[i].textContent;
      }
    }
    return text || el.textContent || '';
  }

  /**
   * Given a section header element, find the container of interaction rows
   * that belong to that section (everything between this header and the next,
   * or to the end of the panel).
   */
  function getSectionContainer(headerEl) {
    if (!headerEl) return null;

    // Walk up a few levels to find the section wrapper
    var section = headerEl;
    for (var i = 0; i < 6; i++) {
      if (!section.parentElement) break;
      section = section.parentElement;
      // If this ancestor has Actions buttons, it's likely the section container
      if (section.querySelectorAll('button[aria-label="Actions"]').length > 0) {
        return section;
      }
    }

    return null;
  }

  // ─── Panel & Buttons ───────────────────────────────────────

  /**
   * Find the Interactions panel in the Designer sidebar.
   */
  function findInteractionsPanel() {
    var headers = findSectionHeaders();

    // Try to find a common panel that contains both sections
    var startEl = headers.allHeader || headers.pageHeader;
    if (startEl) {
      var parent = startEl.parentElement;
      for (var i = 0; i < 12 && parent; i++) {
        if (parent.querySelectorAll('button[aria-label="Actions"]').length > 0) {
          return parent;
        }
        parent = parent.parentElement;
      }
    }

    // Fallback: common ancestor of all Actions buttons
    var buttons = document.querySelectorAll('button[aria-label="Actions"]');
    if (buttons.length > 0) {
      return findCommonAncestor(buttons);
    }

    return null;
  }

  /**
   * Find common ancestor element for a NodeList of elements.
   */
  function findCommonAncestor(elements) {
    if (elements.length === 0) return null;
    if (elements.length === 1) return elements[0].parentElement;

    var ancestor = elements[0].parentElement;
    while (ancestor) {
      var containsAll = true;
      for (var j = 0; j < elements.length; j++) {
        if (!ancestor.contains(elements[j])) {
          containsAll = false;
          break;
        }
      }
      if (containsAll) return ancestor;
      ancestor = ancestor.parentElement;
    }
    return document.body;
  }

  /**
   * Find Actions buttons, optionally filtered by section.
   * @param {Element|null} panel
   * @param {'all'|'page'|'unused'} mode
   */
  function findActionButtons(panel, mode) {
    mode = mode || 'all';

    if (mode === 'all') {
      var container = panel || document;
      return Array.from(container.querySelectorAll('button[aria-label="Actions"]'));
    }

    // Section-aware: find headers, then scope to the right section
    var headers = findSectionHeaders();

    if (mode === 'page') {
      var pageSection = getSectionContainer(headers.pageHeader);
      if (pageSection) {
        return Array.from(pageSection.querySelectorAll('button[aria-label="Actions"]'));
      }
      // Fallback: if no "On this page" section found, return empty
      return [];
    }

    if (mode === 'unused') {
      // "Unused" = buttons in the "All interactions" section that are NOT
      // also in the "On this page" section.
      var allSection = getSectionContainer(headers.allHeader);
      var pageSectionForUnused = getSectionContainer(headers.pageHeader);

      if (!allSection) {
        // No "All interactions" section — return everything as fallback
        var fallback = panel || document;
        return Array.from(fallback.querySelectorAll('button[aria-label="Actions"]'));
      }

      var allButtons = Array.from(allSection.querySelectorAll('button[aria-label="Actions"]'));

      if (!pageSectionForUnused) {
        return allButtons; // No page section, so all are "unused"
      }

      // Filter out buttons that are inside the page section
      return allButtons.filter(function (btn) {
        return !pageSectionForUnused.contains(btn);
      });
    }

    // Unknown mode — return all
    var fallbackContainer = panel || document;
    return Array.from(fallbackContainer.querySelectorAll('button[aria-label="Actions"]'));
  }

  /**
   * Find the "Delete" menu item in a visible context menu.
   */
  function findDeleteInContextMenu() {
    var menuItems = document.querySelectorAll(
      '[role="menuitem"], [role="option"], [class*="ContextMenu"] button, [class*="contextMenu"] button, [class*="dropdown"] button, [class*="Dropdown"] button'
    );

    for (var i = 0; i < menuItems.length; i++) {
      var text = (menuItems[i].textContent || '').trim().toLowerCase();
      if (text === 'delete') {
        return menuItems[i];
      }
    }

    // Broader search
    var allButtons = document.querySelectorAll('button, [role="menuitem"], div[tabindex]');
    for (var j = 0; j < allButtons.length; j++) {
      var btnText = (allButtons[j].textContent || '').trim();
      if (btnText === 'Delete' && isVisible(allButtons[j])) {
        return allButtons[j];
      }
    }

    return null;
  }

  /**
   * Find the confirmation "Delete" button in a dialog.
   */
  function findConfirmDeleteButton() {
    var dialogs = document.querySelectorAll(
      '[role="dialog"], [role="alertdialog"], [class*="Modal"], [class*="modal"], [class*="Dialog"], [class*="dialog"]'
    );

    for (var i = 0; i < dialogs.length; i++) {
      if (!isVisible(dialogs[i])) continue;
      var buttons = dialogs[i].querySelectorAll('button');
      for (var j = 0; j < buttons.length; j++) {
        var text = (buttons[j].textContent || '').trim().toLowerCase();
        if (text === 'delete' || text === 'yes, delete' || text === 'confirm') {
          return buttons[j];
        }
      }
    }

    return null;
  }

  /**
   * Check if an element is visible.
   */
  function isVisible(el) {
    if (!el) return false;
    var style = window.getComputedStyle(el);
    return (
      style.display !== 'none' &&
      style.visibility !== 'hidden' &&
      style.opacity !== '0' &&
      el.offsetWidth > 0
    );
  }

  // ─── React Fiber Walking ─────────────────────────────────────

  function getReactFiber(el) {
    if (!el) return null;
    var key = Object.keys(el).find(function (k) {
      return k.startsWith('__reactFiber$') || k.startsWith('__reactInternalInstance$');
    });
    return key ? el[key] : null;
  }

  function walkFiberForComponent(fiber, componentName) {
    var current = fiber;
    var depth = 0;

    while (current && depth < 50) {
      var type = current.type;
      if (type) {
        var name = type.displayName || type.name || (typeof type === 'string' ? type : null);
        if (name && name.includes(componentName)) {
          return current;
        }
      }
      current = current.return;
      depth++;
    }
    return null;
  }

  function extractDeleteInfo(fiber) {
    if (!fiber || !fiber.memoizedProps) return null;
    var props = fiber.memoizedProps;

    if (typeof props.onDelete === 'function') {
      return {
        onDelete: props.onDelete,
        interactionId: props.interactionId || props.id || null,
        name: props.name || props.displayName || null,
      };
    }

    if (props.children && typeof props.children === 'object') {
      var childProps = props.children.props;
      if (childProps && typeof childProps.onDelete === 'function') {
        return {
          onDelete: childProps.onDelete,
          interactionId: childProps.interactionId || childProps.id || null,
          name: childProps.name || childProps.displayName || null,
        };
      }
    }

    return null;
  }

  function getDeleteInfoFromButton(button) {
    var fiber = getReactFiber(button);
    if (!fiber) return null;

    var componentNames = [
      'IX3InteractionRowItem',
      'InteractionRowItem',
      'InteractionRow',
      'RowItem',
    ];

    for (var i = 0; i < componentNames.length; i++) {
      var rowFiber = walkFiberForComponent(fiber, componentNames[i]);
      if (rowFiber) {
        var info = extractDeleteInfo(rowFiber);
        if (info) return info;
      }
    }

    // Broader search
    var current = fiber;
    var depth = 0;
    while (current && depth < 30) {
      if (current.memoizedProps && typeof current.memoizedProps.onDelete === 'function') {
        return {
          onDelete: current.memoizedProps.onDelete,
          interactionId: current.memoizedProps.interactionId || current.memoizedProps.id || null,
          name: current.memoizedProps.name || current.memoizedProps.displayName || null,
        };
      }
      current = current.return;
      depth++;
    }

    return null;
  }

  // ─── Interaction Metadata ────────────────────────────────────

  function getInteractionName(button) {
    var row = button.parentElement;
    for (var i = 0; i < 5 && row; i++) {
      var textEls = row.querySelectorAll('span, p, div');
      for (var j = 0; j < textEls.length; j++) {
        if (textEls[j].contains(button)) continue;
        var text = (textEls[j].textContent || '').trim();
        if (text && text.length > 0 && text.length < 100 && text !== 'Actions') {
          return text;
        }
      }
      row = row.parentElement;
    }
    return '(unnamed)';
  }

  /**
   * Scan interactions by mode.
   * @param {Element|null} panel
   * @param {'all'|'page'|'unused'} mode
   * @returns {{ name: string, buttonIndex: number }[]}
   */
  function scanInteractions(panel, mode) {
    mode = mode || 'all';
    var buttons = findActionButtons(panel, mode);
    return buttons.map(function (btn, i) {
      return { name: getInteractionName(btn), buttonIndex: i };
    });
  }

  /**
   * Scan all sections and return counts for each mode.
   * @param {Element|null} panel
   * @returns {{ all: number, page: number, unused: number, names: { all: string[], page: string[], unused: string[] } }}
   */
  function scanAllSections(panel) {
    var allIx = scanInteractions(panel, 'all');
    var pageIx = scanInteractions(panel, 'page');
    var unusedIx = scanInteractions(panel, 'unused');

    return {
      all: allIx.length,
      page: pageIx.length,
      unused: unusedIx.length,
      names: {
        all: allIx.map(function (ix) { return ix.name; }),
        page: pageIx.map(function (ix) { return ix.name; }),
        unused: unusedIx.map(function (ix) { return ix.name; }),
      },
    };
  }

  // ─── Scroll Container ────────────────────────────────────────

  function getScrollContainer(panel) {
    if (!panel) return null;

    var candidates = panel.querySelectorAll('*');
    for (var i = 0; i < candidates.length; i++) {
      var style = window.getComputedStyle(candidates[i]);
      if (
        (style.overflowY === 'auto' || style.overflowY === 'scroll') &&
        candidates[i].scrollHeight > candidates[i].clientHeight
      ) {
        return candidates[i];
      }
    }

    if (panel.scrollHeight > panel.clientHeight) {
      return panel;
    }

    return panel;
  }

  function scrollToLoadMore(container) {
    return new Promise(function (resolve) {
      if (!container) {
        resolve(false);
        return;
      }

      var prevScrollTop = container.scrollTop;
      container.scrollTop += container.clientHeight * 0.8;

      setTimeout(function () {
        resolve(container.scrollTop !== prevScrollTop);
      }, 400);
    });
  }

  // ─── Public API ──────────────────────────────────────────────

  return {
    findInteractionsPanel: findInteractionsPanel,
    findActionButtons: findActionButtons,
    findDeleteInContextMenu: findDeleteInContextMenu,
    findConfirmDeleteButton: findConfirmDeleteButton,
    getReactFiber: getReactFiber,
    walkFiberForComponent: walkFiberForComponent,
    extractDeleteInfo: extractDeleteInfo,
    getDeleteInfoFromButton: getDeleteInfoFromButton,
    getInteractionName: getInteractionName,
    scanInteractions: scanInteractions,
    scanAllSections: scanAllSections,
    getScrollContainer: getScrollContainer,
    scrollToLoadMore: scrollToLoadMore,
    isVisible: isVisible,
  };
})();
