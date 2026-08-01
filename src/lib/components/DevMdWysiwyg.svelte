<script lang="ts">
	/**
	 * Wraps rendered doc body. When edit mode is on, becomes contenteditable.
	 * Right-click a link → context menu under the link.
	 * "ویرایش پیوند" → same menu, page 2 (edit form).
	 */
	import type { Snippet } from 'svelte';
	import Icon from '$lib/components/Icon.svelte';
	import { page } from '$app/state';
	import {
		devMdEdit,
		devMdIsActive,
		devMdMarkDirty,
		devMdSave,
		devMdSetHistFlags,
		devMdSetHistHandlers
	} from '$lib/dev-md-edit.svelte';
	import {
		applyStoreToRoot,
		canRedo,
		canUndo,
		commitEvent,
		createEditEventStore,
		getSelectionBookmark,
		redoEvent,
		resetEditEvents,
		type EditEventType,
		undoEvent
	} from '$lib/dev-md-events';

	let { children }: { children: Snippet } = $props();

	/** View host: Svelte-rendered MD (not contenteditable) */
	let viewEl: HTMLDivElement | undefined = $state();
	/** Edit host: pure contenteditable; Svelte never rewrites its children */
	let rootEl: HTMLDivElement | undefined = $state();
	const active = $derived(devMdIsActive(page.url.pathname));

	type MenuView = 'main' | 'edit';

	let menu = $state<{
		x: number;
		y: number;
		anchor: HTMLAnchorElement;
		view: MenuView;
		href: string;
		text: string;
	} | null>(null);

	/** Ignore the next window click (same gesture that opened a view) */
	let ignoreOutsideClick = false;

	/** Event-sourced history (undo/redo stream) */
	const eventStore = createEditEventStore(150);
	let histTimer: ReturnType<typeof setTimeout> | null = null;
	let composing = false;

	function refreshHistFlags() {
		devMdSetHistFlags(canUndo(eventStore), canRedo(eventStore));
	}

	function commitNow(type: EditEventType) {
		if (!rootEl || eventStore.applying || composing) return;
		const ev = commitEvent(eventStore, type, rootEl.innerHTML, getSelectionBookmark(rootEl));
		if (ev) refreshHistFlags();
	}

	function scheduleCommit(type: EditEventType = 'input') {
		if (eventStore.applying || composing) return;
		if (histTimer != null) clearTimeout(histTimer);
		// Coalesce rapid keystrokes into one event (event sourcing "batch")
		histTimer = setTimeout(() => {
			histTimer = null;
			commitNow(type);
		}, 180);
	}

	function flushPendingCommit() {
		if (histTimer != null) {
			clearTimeout(histTimer);
			histTimer = null;
			commitNow('input');
		}
	}

	function undoEdit() {
		if (!rootEl) return false;
		flushPendingCommit();
		if (!canUndo(eventStore)) return false;
		const ev = undoEvent(eventStore);
		if (!ev) return false;
		applyStoreToRoot(eventStore, rootEl);
		normalizeCodeDirection(rootEl);
		normalizeBlockAutoDir(rootEl);
		protectStructuralBlocks(rootEl);
		menu = null;
		devMdMarkDirty();
		refreshHistFlags();
		return true;
	}

	function redoEdit() {
		if (!rootEl) return false;
		flushPendingCommit();
		if (!canRedo(eventStore)) return false;
		const ev = redoEvent(eventStore);
		if (!ev) return false;
		applyStoreToRoot(eventStore, rootEl);
		normalizeCodeDirection(rootEl);
		normalizeBlockAutoDir(rootEl);
		protectStructuralBlocks(rootEl);
		menu = null;
		devMdMarkDirty();
		refreshHistFlags();
		return true;
	}

	/** True after seedHtml has been applied for this edit session */
	let editSeeded = false;

	/**
	 * When edit mode turns on, seed a detached contenteditable from seedHtml.
	 * We intentionally do NOT render `{@render children()}` inside the editable
	 * host — Svelte re-renders (dirty badge, etc.) were reordering Enter/newlines.
	 */
	$effect(() => {
		if (!active) {
			if (devMdEdit.bodyEl === rootEl) devMdEdit.bodyEl = null;
			menu = null;
			if (histTimer != null) {
				clearTimeout(histTimer);
				histTimer = null;
			}
			editSeeded = false;
			devMdSetHistHandlers(null);
			return;
		}
		if (!rootEl) return;

		devMdEdit.bodyEl = rootEl;
		devMdSetHistHandlers({ undo: undoEdit, redo: redoEdit });

		if (!editSeeded) {
			const seed =
				devMdEdit.seedHtml != null
					? devMdEdit.seedHtml
					: (viewEl?.innerHTML ?? '');
			rootEl.innerHTML = seed;
			devMdEdit.seedHtml = null;
			editSeeded = true;
			normalizeCodeDirection(rootEl);
			normalizeBlockAutoDir(rootEl);
			protectStructuralBlocks(rootEl);
			devMdEdit.originalHtml = rootEl.innerHTML;
			devMdEdit.dirty = false;
			resetEditEvents(eventStore, rootEl.innerHTML, getSelectionBookmark(rootEl));
			refreshHistFlags();
			queueMicrotask(() => {
				try {
					rootEl?.focus({ preventScroll: true });
				} catch {
					rootEl?.focus();
				}
			});
		}

		return () => {
			devMdSetHistHandlers(null);
		};
	});

	function onInput() {
		if (eventStore.applying || composing) return;
		scheduleCommit('input');
		devMdMarkDirty();
	}

	function onPaste() {
		if (eventStore.applying) return;
		// after paste DOM updates
		queueMicrotask(() => {
			flushPendingCommit();
			commitNow('paste');
			devMdMarkDirty();
		});
	}

	function onCut() {
		if (eventStore.applying) return;
		queueMicrotask(() => {
			flushPendingCommit();
			commitNow('cut');
			devMdMarkDirty();
		});
	}

	/** Block browser native undo/redo; route through our event store */
	function onBeforeInput(e: InputEvent) {
		if (!active || eventStore.applying) return;
		const t = e.inputType;
		if (t === 'historyUndo') {
			e.preventDefault();
			undoEdit();
			return;
		}
		if (t === 'historyRedo') {
			e.preventDefault();
			redoEdit();
			return;
		}
		// Space via beforeinput (some browsers / IME paths skip keydown Space)
		if (t === 'insertText' && e.data === ' ') {
			if (onMarkdownSpaceShortcut()) {
				e.preventDefault();
			}
			return;
		}
		// Enter / Backspace on empty bullet (backup if keydown missed)
		if (t === 'insertParagraph' || t === 'insertLineBreak') {
			if (tryExitEmptyListItem()) {
				e.preventDefault();
			}
			return;
		}
		if (t === 'deleteContentBackward') {
			if (tryHeadingBackspace() || tryListBackspace()) {
				e.preventDefault();
			}
		}
	}

	function onCompositionStart() {
		composing = true;
		flushPendingCommit();
	}

	function onCompositionEnd() {
		composing = false;
		scheduleCommit('input');
		devMdMarkDirty();
	}

	function armIgnoreOutsideClick() {
		ignoreOutsideClick = true;
		queueMicrotask(() => {
			// clear after the current click has finished bubbling
			setTimeout(() => {
				ignoreOutsideClick = false;
			}, 0);
		});
	}

	function onClick(e: MouseEvent) {
		if (!active) return;
		const t = e.target;
		if (t instanceof Element && t.closest('.dev-link-menu')) {
			e.stopPropagation();
			return;
		}
		if (menu) menu = null;

		// Click the --- line → select it (arrow keys land here too)
		if (t instanceof HTMLHRElement && rootEl?.contains(t)) {
			e.preventDefault();
			selectHr(t);
			return;
		}
		clearHrSelection();

		if (t instanceof HTMLAnchorElement || (t instanceof Element && t.closest('a'))) {
			e.preventDefault();
		}
	}

	/* ── Horizontal rule as a navigable / selectable “line” ─────────── */

	function clearHrSelection() {
		if (!rootEl) return;
		rootEl.querySelectorAll('hr.dev-hr--selected').forEach((h) => {
			h.classList.remove('dev-hr--selected');
		});
	}

	function selectHr(hr: HTMLHRElement) {
		if (!rootEl) return;
		clearHrSelection();
		hr.classList.add('dev-hr--selected');
		try {
			rootEl.focus({ preventScroll: true });
		} catch {
			rootEl.focus();
		}
		const sel = window.getSelection();
		if (!sel) return;
		const range = document.createRange();
		// Select the whole rule so it behaves like a “line”
		range.selectNode(hr);
		sel.removeAllRanges();
		sel.addRange(range);
		// Keep it in view
		hr.scrollIntoView({ block: 'nearest', behavior: 'auto' });
	}

	function selectedHr(): HTMLHRElement | null {
		if (!rootEl) return null;
		return rootEl.querySelector('hr.dev-hr--selected');
	}

	/** Direct child of the editable root that contains the caret */
	function topLevelBlockAtCaret(): HTMLElement | null {
		if (!rootEl) return null;
		const sel = window.getSelection();
		if (!sel || sel.rangeCount === 0) return null;
		let node: Node | null = sel.anchorNode;
		if (!node || !rootEl.contains(node)) return null;
		if (node === rootEl) return null;

		let el: HTMLElement | null =
			node.nodeType === Node.TEXT_NODE
				? (node.parentElement as HTMLElement | null)
				: node instanceof HTMLElement
					? node
					: node.parentElement;

		while (el && el.parentElement !== rootEl) {
			el = el.parentElement;
		}
		return el && el.parentElement === rootEl ? el : null;
	}

	function isCaretOnBlockEdge(block: HTMLElement, edge: 'start' | 'end'): boolean {
		const sel = window.getSelection();
		if (!sel || sel.rangeCount === 0 || !sel.isCollapsed) return false;

		const caretRange = sel.getRangeAt(0).cloneRange();
		caretRange.collapse(true);

		// Measure caret Y (temp marker if needed)
		let caretTop = 0;
		let caretBottom = 0;
		const rects = caretRange.getClientRects();
		if (rects.length > 0) {
			caretTop = rects[0].top;
			caretBottom = rects[0].bottom;
		} else {
			const mark = document.createElement('span');
			mark.textContent = '\u200b';
			mark.style.cssText = 'display:inline;padding:0;margin:0;border:0;line-height:inherit;';
			caretRange.insertNode(mark);
			const r = mark.getBoundingClientRect();
			caretTop = r.top;
			caretBottom = r.bottom;
			const parent = mark.parentNode;
			if (parent) {
				parent.removeChild(mark);
				parent.normalize?.();
			}
		}

		const full = document.createRange();
		full.selectNodeContents(block);
		const lineRects = [...full.getClientRects()].filter((r) => r.width > 0 || r.height > 0);
		if (lineRects.length === 0) return true;

		const tol = 6;
		if (edge === 'end') {
			const last = lineRects[lineRects.length - 1];
			// Same visual line as the last line of the block
			return caretTop >= last.top - tol;
		}
		const first = lineRects[0];
		return caretBottom <= first.bottom + tol;
	}

	function placeCaretInBlock(block: HTMLElement, atEnd: boolean) {
		// Lists: enter first/last item
		if (block.tagName === 'UL' || block.tagName === 'OL') {
			const items = block.querySelectorAll(':scope > li');
			const li = (atEnd ? items[items.length - 1] : items[0]) as HTMLElement | undefined;
			if (li) {
				placeCaretIn(li, atEnd);
				return;
			}
		}
		if (isHeadingTag(block.tagName) || block.tagName === 'P' || block.tagName === 'DIV') {
			if (atEnd) placeCaretIn(block, true);
			else placeCaretIn(block, false);
			return;
		}
		// Generic
		const sel = window.getSelection();
		if (!sel) return;
		const r = document.createRange();
		r.selectNodeContents(block);
		r.collapse(!atEnd);
		sel.removeAllRanges();
		sel.addRange(r);
	}

	/**
	 * Arrow Up/Down around --- (<hr>):
	 * stop on the rule as a selectable line, then continue to the next/prev block.
	 */
	function tryHrArrowNav(e: KeyboardEvent): boolean {
		if (!rootEl || eventStore.applying || composing) return false;
		if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return false;
		if (e.shiftKey) return false; // let extend-selection work
		const down = e.key === 'ArrowDown';

		// Already on the selected --- line
		const curHr = selectedHr();
		if (curHr) {
			e.preventDefault();
			clearHrSelection();
			if (down) {
				let next = curHr.nextElementSibling as HTMLElement | null;
				while (next && next.tagName === 'HR') {
					// skip double rules → select next hr or continue
					selectHr(next as HTMLHRElement);
					return true;
				}
				if (next) {
					placeCaretInBlock(next, false);
				} else {
					const p = makeBlock('p');
					p.innerHTML = '<br>';
					curHr.after(p);
					placeCaretIn(p);
					flushPendingCommit();
					commitNow('format');
					devMdMarkDirty();
				}
			} else {
				let prev = curHr.previousElementSibling as HTMLElement | null;
				while (prev && prev.tagName === 'HR') {
					selectHr(prev as HTMLHRElement);
					return true;
				}
				if (prev) {
					placeCaretInBlock(prev, true);
				} else {
					const p = makeBlock('p');
					p.innerHTML = '<br>';
					curHr.before(p);
					placeCaretIn(p);
					flushPendingCommit();
					commitNow('format');
					devMdMarkDirty();
				}
			}
			return true;
		}

		// Also: selection is the HR node without our class (native selectNode)
		const sel = window.getSelection();
		if (sel && sel.rangeCount > 0 && !sel.isCollapsed) {
			const n = sel.getRangeAt(0).commonAncestorContainer;
			const hr =
				n instanceof HTMLHRElement
					? n
					: n instanceof Element
						? n.querySelector?.('hr')
						: null;
			// If range is exactly one hr
			if (
				sel.anchorNode &&
				sel.focusNode &&
				sel.anchorNode === sel.focusNode &&
				sel.anchorNode.childNodes[sel.anchorOffset] instanceof HTMLHRElement
			) {
				const only = sel.anchorNode.childNodes[sel.anchorOffset] as HTMLHRElement;
				selectHr(only);
				// re-handle as selected
				return tryHrArrowNav(e);
			}
			if (hr instanceof HTMLHRElement && rootEl.contains(hr) && sel.toString() === '') {
				// selectNode(hr) often has empty string
				const range = sel.getRangeAt(0);
				if (
					range.startContainer === range.endContainer &&
					Math.abs(range.endOffset - range.startOffset) === 1
				) {
					const node = range.startContainer.childNodes[Math.min(range.startOffset, range.endOffset)];
					if (node instanceof HTMLHRElement) {
						selectHr(node);
						return tryHrArrowNav(e);
					}
				}
			}
		}

		const block = topLevelBlockAtCaret();
		if (!block) return false;

		if (down) {
			const next = block.nextElementSibling;
			if (next instanceof HTMLHRElement && isCaretOnBlockEdge(block, 'end')) {
				e.preventDefault();
				selectHr(next);
				return true;
			}
		} else {
			const prev = block.previousElementSibling;
			if (prev instanceof HTMLHRElement && isCaretOnBlockEdge(block, 'start')) {
				e.preventDefault();
				selectHr(prev);
				return true;
			}
		}
		return false;
	}

	/** Backspace/Delete while --- line is selected → remove it */
	function tryHrDelete(): boolean {
		const hr = selectedHr();
		if (!hr || !rootEl) return false;
		const prev = hr.previousElementSibling as HTMLElement | null;
		const next = hr.nextElementSibling as HTMLElement | null;
		clearHrSelection();
		hr.remove();
		if (next) placeCaretInBlock(next, false);
		else if (prev) placeCaretInBlock(prev, true);
		else {
			const p = makeBlock('p');
			p.innerHTML = '<br>';
			rootEl.appendChild(p);
			placeCaretIn(p);
		}
		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	function placeMenu(
		a: HTMLAnchorElement,
		view: MenuView,
		href: string,
		text: string
	) {
		const r = a.getBoundingClientRect();
		const menuW = view === 'edit' ? 280 : 230;
		const menuH = view === 'edit' ? 240 : 210;
		const gap = 6;
		let x = r.left;
		let y = r.bottom + gap;
		x = Math.max(8, Math.min(x, window.innerWidth - menuW - 8));
		if (y + menuH > window.innerHeight - 8) {
			y = Math.max(8, r.top - menuH - gap);
		}
		menu = { x, y, anchor: a, view, href, text };
	}

	function onContextMenu(e: MouseEvent) {
		if (!active) return;
		const t = e.target;
		if (!(t instanceof Element)) return;
		const a = t.closest('a');
		if (!(a instanceof HTMLAnchorElement)) return;
		if (rootEl && !rootEl.contains(a)) return;

		e.preventDefault();
		e.stopPropagation();
		armIgnoreOutsideClick();

		const href = a.getAttribute('href') || a.href || '';
		const text = (a.textContent || '').replace(/\s+/g, ' ').trim();
		placeMenu(a, 'main', href, text);
	}

	function openEditPage(e: Event) {
		e.preventDefault();
		e.stopPropagation();
		armIgnoreOutsideClick();
		if (!menu) return;
		const a = menu.anchor;
		const href = a.getAttribute('href') || a.href || menu.href || '';
		const text = (a.textContent || '').replace(/\s+/g, ' ').trim() || menu.text;
		// Switch view in place (same panel, under the link)
		placeMenu(a, 'edit', href, text);
	}

	function backToMain(e?: Event) {
		e?.preventDefault();
		e?.stopPropagation();
		armIgnoreOutsideClick();
		if (!menu) return;
		placeMenu(menu.anchor, 'main', menu.href, menu.text);
	}

	function applyLinkEdit(e: Event) {
		e.preventDefault();
		e.stopPropagation();
		if (!menu || menu.view !== 'edit') return;
		const { anchor, href, text } = menu;
		const h = href.trim();
		if (!h) {
			unwrapLink(anchor);
		} else {
			anchor.setAttribute('href', h);
			if (
				anchor.childElementCount === 0 ||
				[...anchor.children].every((c) =>
					['SPAN', 'EM', 'STRONG', 'CODE', 'KBD', 'B', 'I'].includes(c.tagName)
				)
			) {
				anchor.textContent = text;
			} else if (text && text !== (anchor.textContent || '').replace(/\s+/g, ' ').trim()) {
				anchor.textContent = text;
			}
		}
		menu = null;
		flushPendingCommit();
		commitNow('link-edit');
		devMdMarkDirty();
	}

	function unwrapLink(a: HTMLAnchorElement) {
		const parent = a.parentNode;
		if (!parent) return;
		while (a.firstChild) parent.insertBefore(a.firstChild, a);
		parent.removeChild(a);
		flushPendingCommit();
		commitNow('link-remove');
		devMdMarkDirty();
	}

	function removeLink(e: Event) {
		e.preventDefault();
		e.stopPropagation();
		if (!menu) return;
		unwrapLink(menu.anchor);
		menu = null;
	}

	function copyLinkHref(e: Event) {
		e.preventDefault();
		e.stopPropagation();
		if (!menu) return;
		const href = menu.anchor.getAttribute('href') || menu.anchor.href || '';
		void navigator.clipboard?.writeText(href);
		menu = null;
	}

	function openLinkNewTab(e: Event) {
		e.preventDefault();
		e.stopPropagation();
		if (!menu) return;
		const href = menu.anchor.getAttribute('href') || menu.anchor.href || '';
		if (href) window.open(href, '_blank', 'noopener,noreferrer');
		menu = null;
	}

	function isMod(e: KeyboardEvent) {
		return e.ctrlKey || e.metaKey;
	}

	function isSaveKey(e: KeyboardEvent) {
		return e.code === 'KeyS' || e.key === 'س' || e.key === 's' || e.key === 'S';
	}

	function isUndoKey(e: KeyboardEvent) {
		// Physical Z works on FA layout too (ظ on KeyZ)
		return e.code === 'KeyZ' || e.key === 'z' || e.key === 'Z' || e.key === 'ظ';
	}

	function isRedoKey(e: KeyboardEvent) {
		// Ctrl+Shift+Z or Ctrl+Y (FA: غ is often on Y)
		if (e.code === 'KeyY' || e.key === 'y' || e.key === 'Y' || e.key === 'غ') return true;
		if (isUndoKey(e) && e.shiftKey) return true;
		return false;
	}

	function isItalicKey(e: KeyboardEvent) {
		return e.code === 'KeyI' || e.key === 'i' || e.key === 'I' || e.key === 'ه';
	}

	function isBoldKey(e: KeyboardEvent) {
		return e.code === 'KeyB' || e.key === 'b' || e.key === 'B' || e.key === 'ذ';
	}

	function isUnderlineKey(e: KeyboardEvent) {
		return e.code === 'KeyU' || e.key === 'u' || e.key === 'U' || e.key === 'ع';
	}

	/** Ctrl+M → inline code (monospace) */
	function isCodeKey(e: KeyboardEvent) {
		return e.code === 'KeyM' || e.key === 'm' || e.key === 'M' || e.key === 'م' || e.key === 'ئ';
	}

	/** Ctrl+H → highlight (<mark>) — same toggle / exit as italic */
	function isHighlightKey(e: KeyboardEvent) {
		return e.code === 'KeyH' || e.key === 'h' || e.key === 'H' || e.key === 'ا' || e.key === 'آ';
	}

	function isBacktickKey(e: KeyboardEvent) {
		return e.key === '`' || e.code === 'Backquote' || e.key === 'Dead';
	}

	type InlineKind = 'italic' | 'bold' | 'underline' | 'code' | 'highlight';

	function wrapTagFor(kind: InlineKind): string {
		if (kind === 'italic') return 'em';
		if (kind === 'bold') return 'strong';
		if (kind === 'underline') return 'u';
		if (kind === 'highlight') return 'mark';
		return 'code';
	}

	/**
	 * Inline code/kbd → RTL + text-align right (matches Persian page).
	 * Fenced <pre> / pre>code → LTR + left (source listings).
	 */
	function applyCodeDir(el: HTMLElement) {
		const inPre = el.tagName === 'PRE' || !!el.closest('pre');
		if (inPre) {
			el.setAttribute('dir', 'ltr');
			el.style.direction = 'ltr';
			el.style.textAlign = 'left';
			el.style.unicodeBidi = 'isolate';
			return;
		}
		// Inline chip
		el.setAttribute('dir', 'rtl');
		el.style.direction = 'rtl';
		el.style.textAlign = 'right';
		el.style.unicodeBidi = 'isolate';
	}

	function createCodeElement(): HTMLElement {
		const code = document.createElement('code');
		applyCodeDir(code);
		return code;
	}

	/** Normalize code directions in the editor (seed / undo). */
	function normalizeCodeDirection(scope: HTMLElement = rootEl!) {
		if (!scope) return;
		scope.querySelectorAll('code, kbd').forEach((node) => {
			applyCodeDir(node as HTMLElement);
		});
		scope.querySelectorAll('pre').forEach((pre) => {
			applyCodeDir(pre as HTMLElement);
		});
	}

	/**
	 * Match view mode: document blocks stay RTL (same alignment / padding as .prose).
	 * dir=auto / plaintext flipped lines that started with Latin, numbers, or
	 * mixed inline styles — causing edit ↔ normal style jumps.
	 * English still types as LTR *runs* inside RTL via the Unicode bidi algorithm.
	 */
	/**
	 * Hub card grids are structural HTML (not prose). Lock them so
	 * contenteditable / Turndown cannot unwrap them into plain links.
	 * Title/desc spans stay editable for copy tweaks.
	 */
	function protectStructuralBlocks(scope: HTMLElement = rootEl!) {
		if (!scope) return;
		scope.querySelectorAll('.nd-hub-cards').forEach((node) => {
			const grid = node as HTMLElement;
			grid.setAttribute('contenteditable', 'false');
			grid.setAttribute('data-dev-md-protect', 'hub-cards');
			grid.querySelectorAll('a.nd-hub-card').forEach((a) => {
				(a as HTMLElement).setAttribute('contenteditable', 'false');
				a.querySelectorAll('.nd-hub-card__title, .nd-hub-card__desc').forEach((span) => {
					(span as HTMLElement).setAttribute('contenteditable', 'true');
				});
			});
		});
	}

	function normalizeBlockAutoDir(scope: HTMLElement = rootEl!) {
		if (!scope) return;
		const blocks =
			'p, h1, h2, h3, h4, h5, h6, blockquote, td, th, ul, ol, li, div';
		scope.querySelectorAll(blocks).forEach((node) => {
			const el = node as HTMLElement;
			if (el === scope) return;
			// Never redir code/pre chips here
			if (el.closest('pre') || el.tagName === 'CODE' || el.tagName === 'KBD') return;
			// Leave hub card chrome alone (layout is CSS-centered)
			if (el.closest('.nd-hub-cards')) return;
			// Drop edit-time auto dir that misaligns vs view
			if (el.getAttribute('dir') === 'auto') el.removeAttribute('dir');
			// Structure chrome RTL (lists, headings, body) — same as page shell
			if (
				['UL', 'OL', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'BLOCKQUOTE'].includes(
					el.tagName
				)
			) {
				el.setAttribute('dir', 'rtl');
			} else if (el.tagName === 'P' || el.tagName === 'LI' || el.tagName === 'DIV') {
				// Inherit page RTL; don't set auto
				el.removeAttribute('dir');
			}
			el.style.removeProperty('text-align');
			el.style.removeProperty('direction');
			el.style.removeProperty('unicode-bidi');
		});
		// Host itself: match article RTL
		if (scope === rootEl) {
			scope.setAttribute('dir', 'rtl');
			scope.style.removeProperty('unicode-bidi');
		}
	}

	function makeBlock(tag: string): HTMLElement {
		const el = document.createElement(tag);
		const t = tag.toLowerCase();
		if (['hr', 'br', 'img'].includes(t)) return el;
		// All structural blocks match view mode (RTL page)
		if (/^h[1-6]$/.test(t) || t === 'ul' || t === 'ol' || t === 'blockquote') {
			el.setAttribute('dir', 'rtl');
		}
		// p / li: inherit host RTL (no dir=auto)
		return el;
	}

	/** True if this element itself applies the format (tags + CSS style spans from browsers). */
	function elementAppliesFormat(el: HTMLElement, kind: InlineKind): boolean {
		const tag = el.tagName;
		if (kind === 'italic') {
			if (tag === 'EM' || tag === 'I') return true;
			const fs = (el.style?.fontStyle || '').toLowerCase();
			if (fs === 'italic' || fs === 'oblique') return true;
			const attr = (el.getAttribute('style') || '').toLowerCase();
			if (/font-style\s*:\s*(italic|oblique)/.test(attr)) return true;
			return false;
		}
		if (kind === 'bold') {
			if (tag === 'STRONG' || tag === 'B') return true;
			const fw = (el.style?.fontWeight || '').toLowerCase();
			if (fw === 'bold' || fw === 'bolder' || (!Number.isNaN(Number(fw)) && Number(fw) >= 600)) {
				return true;
			}
			const attr = (el.getAttribute('style') || '').toLowerCase();
			if (/font-weight\s*:\s*(bold|bolder|[6-9]00)/.test(attr)) return true;
			return false;
		}
		if (kind === 'underline') {
			if (tag === 'U') return true;
			const td = (el.style?.textDecorationLine || el.style?.textDecoration || '').toLowerCase();
			if (td.includes('underline')) return true;
			const attr = (el.getAttribute('style') || '').toLowerCase();
			if (/text-decoration[^;]*underline/.test(attr)) return true;
			return false;
		}
		if (kind === 'highlight') {
			if (tag === 'MARK') return true;
			if (el.classList?.contains('dev-md-highlight')) return true;
			return false;
		}
		// code
		return tag === 'CODE' || tag === 'KBD';
	}

	function closestInlineFormat(
		node: Node | null,
		kindOrTags: InlineKind | string[]
	): HTMLElement | null {
		let n: Node | null = node;
		while (n && n !== rootEl) {
			if (n instanceof HTMLElement) {
				if (n.tagName === 'PRE') return null;
				if (Array.isArray(kindOrTags)) {
					if (kindOrTags.includes(n.tagName)) return n;
				} else if (elementAppliesFormat(n, kindOrTags)) {
					return n;
				}
			}
			n = n.parentNode;
		}
		return null;
	}

	/**
	 * Leave an inline format at the caret so further typing is plain.
	 * Splits <em>hello|world</em> → <em>hello</em>|<em>world</em> (caret outside).
	 */
	function exitInlineFormat(formatEl: HTMLElement, sel: Selection) {
		const range = sel.getRangeAt(0);
		const inside =
			formatEl === range.commonAncestorContainer ||
			formatEl.contains(range.commonAncestorContainer);
		if (!inside) {
			const r = document.createRange();
			r.setStartAfter(formatEl);
			r.collapse(true);
			sel.removeAllRanges();
			sel.addRange(r);
			return;
		}

		// Extract everything from caret to end of the format element
		const afterRange = document.createRange();
		afterRange.selectNodeContents(formatEl);
		try {
			afterRange.setStart(range.startContainer, range.startOffset);
		} catch {
			afterRange.setStart(formatEl, formatEl.childNodes.length);
		}

		const afterFrag = afterRange.extractContents();
		const afterHasContent =
			afterFrag.childNodes.length > 0 &&
			((afterFrag.textContent || '').replace(/[\u200b\u200c\ufeff]/g, '').length > 0 ||
				!!afterFrag.querySelector?.('img, br, svg'));

		if (afterHasContent) {
			const tail = document.createElement(formatEl.tagName.toLowerCase());
			// Keep CSS-based format (span style=…) when splitting
			if (formatEl.getAttribute('style')) {
				tail.setAttribute('style', formatEl.getAttribute('style') || '');
			}
			if (formatEl.className) tail.className = formatEl.className;
			tail.appendChild(afterFrag);
			formatEl.after(tail);
		}

		// Drop empty head
		const headEmpty =
			!(formatEl.textContent || '').replace(/[\u200b\u200c\ufeff\s]/g, '') &&
			!formatEl.querySelector('img, svg, video');
		if (headEmpty) {
			const r = document.createRange();
			r.setStartBefore(formatEl);
			r.collapse(true);
			formatEl.remove();
			sel.removeAllRanges();
			sel.addRange(r);
		} else {
			// Caret outside; no extra space — keeps gap tight next to the chip
			placeOutsideInline(formatEl, sel, 'after', false);
		}
	}

	/** Strip zero-width fillers left from empty format toggles */
	function scrubFormatFillers(el: HTMLElement) {
		const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
		const doomed: Text[] = [];
		let node = walker.nextNode() as Text | null;
		while (node) {
			const cleaned = node.data.replace(/[\u200b\u200c\ufeff]/g, '');
			if (cleaned !== node.data) {
				if (cleaned.length === 0) doomed.push(node);
				else node.data = cleaned;
			}
			node = walker.nextNode() as Text | null;
		}
		for (const t of doomed) t.remove();
	}

	function formatElementIsEmpty(el: HTMLElement): boolean {
		scrubFormatFillers(el);
		return (
			!(el.textContent || '').replace(/\s+/g, '') &&
			!el.querySelector('img, svg, video, br')
		);
	}

	function isCaretAtFormatBoundary(el: HTMLElement, edge: 'start' | 'end'): boolean {
		const sel = window.getSelection();
		if (!sel || sel.rangeCount === 0 || !sel.isCollapsed) return false;
		const caret = sel.getRangeAt(0);
		const edgeRange = document.createRange();
		edgeRange.selectNodeContents(el);
		edgeRange.collapse(edge === 'start');
		try {
			return caret.compareBoundaryPoints(Range.START_TO_START, edgeRange) === 0;
		} catch {
			// Fallback: character offsets
			const pre = document.createRange();
			pre.selectNodeContents(el);
			pre.setEnd(caret.startContainer, caret.startOffset);
			const off = pre.toString().replace(/[\u200b\u200c\ufeff]/g, '').length;
			const total = (el.textContent || '').replace(/[\u200b\u200c\ufeff]/g, '').length;
			return edge === 'start' ? off === 0 : off >= total;
		}
	}

	function resolvedDirection(el: HTMLElement): 'rtl' | 'ltr' {
		// Fenced listings stay LTR; inline code is RTL
		if (el.tagName === 'PRE' || (el.tagName === 'CODE' && el.closest('pre'))) {
			return 'ltr';
		}
		if (el.tagName === 'CODE' || el.tagName === 'KBD') {
			return 'rtl';
		}
		let cur: HTMLElement | null = el;
		while (cur) {
			const d = getComputedStyle(cur).direction;
			if (d === 'rtl' || d === 'ltr') return d;
			cur = cur.parentElement;
		}
		return 'rtl'; // site default (Persian)
	}

	/** Drop leading/trailing spaces & bidi marks inside a format chip (avoids double gap). */
	function trimFormatEdgeSpaces(el: HTMLElement) {
		const texts: Text[] = [];
		const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
		let n = walker.nextNode() as Text | null;
		while (n) {
			texts.push(n);
			n = walker.nextNode() as Text | null;
		}
		if (!texts.length) return;
		const first = texts[0];
		const last = texts[texts.length - 1];
		first.data = first.data.replace(/^[\u200b\u200c\u200f\ufeff\s]+/, '');
		if (last !== first) {
			last.data = last.data.replace(/[\u200b\u200c\u200f\ufeff\s]+$/, '');
		} else {
			first.data = first.data.replace(/[\u200b\u200c\u200f\ufeff\s]+$/, '');
		}
		for (const t of texts) {
			if (!t.data) t.remove();
		}
	}

	/**
	 * Place caret + optional single space outside an inline format.
	 * One normal space only (no RLM padding) — extra marks looked like a wide gap
	 * on the left of the code in RTL. Isolate already handles bidi separation.
	 */
	function placeOutsideInline(
		formatEl: HTMLElement,
		sel: Selection,
		side: 'after' | 'before',
		withSpace: boolean
	) {
		scrubFormatFillers(formatEl);
		trimFormatEdgeSpaces(formatEl);

		if (formatElementIsEmpty(formatEl)) {
			const r = document.createRange();
			if (side === 'after') r.setStartAfter(formatEl);
			else r.setStartBefore(formatEl);
			r.collapse(true);
			const parent = formatEl.parentNode;
			formatEl.remove();
			sel.removeAllRanges();
			sel.addRange(r);
			parent?.normalize?.();
			return;
		}

		if (side === 'after') {
			let next = formatEl.nextSibling;
			// Collapse any existing bidi junk / multi-spaces after the chip to one space
			if (next instanceof Text) {
				next.data = next.data.replace(/^[\u200f\u200e\u200b\ufeff]+/, '');
				if (withSpace) {
					if (!/^\s/.test(next.data)) next.data = ' ' + next.data.replace(/^\s+/, '');
					else next.data = ' ' + next.data.replace(/^\s+/, ''); // single space
				} else {
					next.data = next.data.replace(/^\s+/, '');
				}
			} else if (withSpace) {
				next = document.createTextNode(' ');
				formatEl.after(next);
			}
			if (withSpace && next instanceof Text) {
				const r = document.createRange();
				r.setStart(next, 1);
				r.collapse(true);
				sel.removeAllRanges();
				sel.addRange(r);
			} else {
				const r = document.createRange();
				r.setStartAfter(formatEl);
				r.collapse(true);
				sel.removeAllRanges();
				sel.addRange(r);
			}
		} else {
			let prev = formatEl.previousSibling;
			if (prev instanceof Text) {
				prev.data = prev.data.replace(/[\u200f\u200e\u200b\ufeff]+$/, '');
				if (withSpace) {
					if (!/\s$/.test(prev.data)) prev.data = prev.data.replace(/\s+$/, '') + ' ';
					else prev.data = prev.data.replace(/\s+$/, '') + ' ';
				} else {
					prev.data = prev.data.replace(/\s+$/, '');
				}
			} else if (withSpace) {
				prev = document.createTextNode(' ');
				formatEl.before(prev);
			}
			if (withSpace && prev instanceof Text) {
				const r = document.createRange();
				r.setStart(prev, prev.length);
				r.collapse(true);
				sel.removeAllRanges();
				sel.addRange(r);
			} else {
				const r = document.createRange();
				r.setStartBefore(formatEl);
				r.collapse(true);
				sel.removeAllRanges();
				sel.addRange(r);
			}
		}
	}

	function inlineFormatAtCaret(): { el: HTMLElement; kind: InlineKind } | null {
		const sel = window.getSelection();
		if (!sel || !sel.anchorNode || !rootEl?.contains(sel.anchorNode)) return null;
		const kinds: InlineKind[] = ['code', 'highlight', 'italic', 'bold', 'underline'];
		for (const k of kinds) {
			const el = closestInlineFormat(sel.anchorNode, k);
			if (el) return { el, kind: k };
		}
		return null;
	}

	/**
	 * Leave inline format at an edge:
	 * - Code is always LTR: end + → → space outside (RTL-aware)
	 * - RTL formats (em on Persian): end + ← → space outside
	 */
	function tryExitInlineOnArrow(e: KeyboardEvent): boolean {
		if (!rootEl || eventStore.applying || composing) return false;
		if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return false;

		const sel = window.getSelection();
		if (!sel || !sel.isCollapsed || sel.rangeCount === 0) return false;

		const hit = inlineFormatAtCaret();
		if (!hit) return false;
		const { el: formatEl, kind } = hit;

		// Ensure code stays LTR while navigating
		if (kind === 'code') applyCodeDir(formatEl);

		const atEnd = isCaretAtFormatBoundary(formatEl, 'end');
		const atStart = isCaretAtFormatBoundary(formatEl, 'start');
		if (!atEnd && !atStart) return false;

		// Inline code is RTL; other formats follow element direction
		const dir = kind === 'code' ? 'rtl' : resolvedDirection(formatEl);
		// Outward from end: LTR → Right; RTL → Left (must not steal inward arrows)
		const wantExitAfter =
			atEnd &&
			((dir === 'ltr' && e.key === 'ArrowRight') ||
				(dir === 'rtl' && e.key === 'ArrowLeft'));
		const wantExitBefore =
			atStart &&
			((dir === 'ltr' && e.key === 'ArrowLeft') ||
				(dir === 'rtl' && e.key === 'ArrowRight'));

		if (!wantExitAfter && !wantExitBefore) return false;

		e.preventDefault();
		// Arrow exit: leave without injecting an extra space (user types space if needed)
		placeOutsideInline(formatEl, sel, wantExitAfter ? 'after' : 'before', false);
		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	/**
	 * Space at the end of LTR code (inside RTL prose): do NOT keep the space inside
	 * the isolate (it sticks to the Latin right). Exit the span and put a single
	 * space outside — no RLM padding (that looked like a huge gap on the left).
	 *
	 * Spaces mid-code still work (caret not at end).
	 */
	function tryExitCodeOnSpace(): boolean {
		if (!rootEl || eventStore.applying || composing) return false;
		const sel = window.getSelection();
		if (!sel || !sel.isCollapsed || sel.rangeCount === 0) return false;

		const code = closestInlineFormat(sel.anchorNode, 'code');
		if (!code) return false;
		if (!isCaretAtFormatBoundary(code, 'end')) return false;

		// Don't steal Space when empty (user may still type first char)
		scrubFormatFillers(code);
		const bare = (code.textContent || '').replace(/[\u200b\u200c\ufeff]/g, '');
		if (!bare.length) return false;

		placeOutsideInline(code, sel, 'after', true);
		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	function wrapRangeWithTag(range: Range, tag: string): HTMLElement {
		const el =
			tag === 'code' || tag === 'kbd' ? createCodeElement() : document.createElement(tag);
		if (tag === 'kbd') applyCodeDir(el);
		try {
			range.surroundContents(el);
		} catch {
			const frag = range.extractContents();
			el.appendChild(frag);
			range.insertNode(el);
		}
		return el;
	}

	function unwrapElement(el: HTMLElement) {
		const parent = el.parentNode;
		if (!parent) return;
		while (el.firstChild) parent.insertBefore(el.firstChild, el);
		parent.removeChild(el);
		parent.normalize?.();
	}

	function formatCssSelector(kind: InlineKind): string {
		if (kind === 'bold') return 'strong, b';
		if (kind === 'italic') return 'em, i';
		if (kind === 'underline') return 'u';
		if (kind === 'highlight') return 'mark';
		return 'code, kbd';
	}

	function stripFormatDeep(root: ParentNode, kind: InlineKind) {
		const sel = formatCssSelector(kind);
		// Unwrap nested format tags until none remain
		for (let i = 0; i < 20; i++) {
			const nodes = root.querySelectorAll(sel);
			if (!nodes.length) break;
			nodes.forEach((n) => unwrapElement(n as HTMLElement));
		}
		// Top-level child that is itself a format element
		const kids = [...root.childNodes];
		for (const kid of kids) {
			if (kid instanceof HTMLElement && elementAppliesFormat(kid, kind)) {
				unwrapElement(kid);
			}
		}
	}

	/** Non-whitespace text nodes that intersect the range */
	function textNodesInRange(range: Range): Text[] {
		const out: Text[] = [];
		const root =
			range.commonAncestorContainer.nodeType === Node.ELEMENT_NODE
				? range.commonAncestorContainer
				: range.commonAncestorContainer.parentNode;
		if (!root) return out;
		const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
		let n = walker.nextNode() as Text | null;
		while (n) {
			if (range.intersectsNode(n) && (n.data || '').replace(/\s+/g, '').length > 0) {
				out.push(n);
			}
			n = walker.nextNode() as Text | null;
		}
		return out;
	}

	/** True if every bit of selected text is already in this format (toggle should remove). */
	function rangeIsFullyFormatted(range: Range, kind: InlineKind): boolean {
		const startF = closestInlineFormat(range.startContainer, kind);
		const endF = closestInlineFormat(range.endContainer, kind);
		if (startF && startF === endF) return true;

		const texts = textNodesInRange(range);
		if (texts.length === 0) {
			// Selection might be an element node (e.g. whole <strong>)
			const ca = range.commonAncestorContainer;
			if (ca instanceof HTMLElement && elementAppliesFormat(ca, kind)) return true;
			if (startF && endF) return true;
			return false;
		}
		return texts.every((t) => !!closestInlineFormat(t, kind));
	}

	function selectionCoversElement(range: Range, el: HTMLElement): boolean {
		const a = range.toString().replace(/\s+/g, '');
		const b = (el.textContent || '').replace(/\s+/g, '');
		if (a.length > 0 && a === b) return true;
		try {
			const full = document.createRange();
			full.selectNodeContents(el);
			return (
				range.compareBoundaryPoints(Range.START_TO_START, full) <= 0 &&
				range.compareBoundaryPoints(Range.END_TO_END, full) >= 0
			);
		} catch {
			return a === b;
		}
	}

	/**
	 * Remove format from a non-collapsed selection.
	 * Handles: whole <strong>, partial inside one <strong>, multi-node selection.
	 */
	function removeFormatFromSelection(range: Range, kind: InlineKind, sel: Selection) {
		const startF = closestInlineFormat(range.startContainer, kind);
		const endF = closestInlineFormat(range.endContainer, kind);

		// Entirely inside one format element
		if (startF && startF === endF) {
			if (selectionCoversElement(range, startF)) {
				const marker = document.createTextNode('');
				startF.after(marker);
				unwrapElement(startF);
				const r = document.createRange();
				r.setStart(marker, 0);
				r.collapse(true);
				sel.removeAllRanges();
				sel.addRange(r);
				marker.parentNode?.normalize?.();
				return;
			}
			// Partial: split format → [bold before][plain mid][bold after]
			const afterR = document.createRange();
			afterR.selectNodeContents(startF);
			afterR.setStart(range.endContainer, range.endOffset);
			const afterFrag = afterR.extractContents();

			const midR = document.createRange();
			midR.selectNodeContents(startF);
			midR.setStart(range.startContainer, range.startOffset);
			const midFrag = midR.extractContents();
			stripFormatDeep(midFrag, kind);

			const tag = startF.tagName.toLowerCase();
			const plainFirst = midFrag.firstChild;
			const plainLast = midFrag.lastChild;

			// Insert plain mid after the (now shorter) format element
			startF.after(midFrag);

			// Trailing bold piece
			if (
				afterFrag.childNodes.length > 0 &&
				((afterFrag.textContent || '').replace(/[\u200b\ufeff\s]/g, '').length > 0 ||
					afterFrag.querySelector?.('img, br'))
			) {
				const tail = document.createElement(tag);
				if (startF.getAttribute('style')) {
					tail.setAttribute('style', startF.getAttribute('style') || '');
				}
				if (kind === 'code') applyCodeDir(tail);
				tail.appendChild(afterFrag);
				// after mid
				if (plainLast && plainLast.parentNode) {
					plainLast.parentNode.insertBefore(
						tail,
						plainLast.nextSibling
					);
				} else {
					startF.after(tail);
				}
			}

			// Drop empty head <strong></strong>
			if (
				!(startF.textContent || '').replace(/[\u200b\ufeff\s]/g, '') &&
				!startF.querySelector('img, br')
			) {
				startF.remove();
			}

			// Reselect the plain middle
			if (plainFirst && plainLast) {
				const r = document.createRange();
				r.setStartBefore(plainFirst);
				r.setEndAfter(plainLast);
				sel.removeAllRanges();
				sel.addRange(r);
			}
			return;
		}

		// Selection spans multiple nodes / fully covers bold regions
		const live = range.cloneRange();
		const frag = live.extractContents();
		stripFormatDeep(frag, kind);
		const first = frag.firstChild;
		const last = frag.lastChild;
		live.insertNode(frag);
		if (first && last) {
			try {
				const r = document.createRange();
				r.setStartBefore(first);
				r.setEndAfter(last);
				sel.removeAllRanges();
				sel.addRange(r);
			} catch {
				/* ignore */
			}
		}
		rootEl?.normalize();
	}

	function ensureEditorSelection(): Selection | null {
		if (!rootEl) return null;
		try {
			rootEl.focus({ preventScroll: true });
		} catch {
			rootEl.focus();
		}
		const sel = window.getSelection();
		if (!sel) return null;
		if (sel.rangeCount === 0 || !sel.anchorNode || !rootEl.contains(sel.anchorNode)) {
			const r = document.createRange();
			r.selectNodeContents(rootEl);
			r.collapse(false);
			sel.removeAllRanges();
			sel.addRange(r);
		}
		return sel;
	}

	/**
	 * Manual inline toggle (italic / bold / underline / code / highlight).
	 * Selection already bold → unbold (and same for other kinds).
	 */
	function toggleInlineKind(kind: InlineKind) {
		const sel = ensureEditorSelection();
		if (!sel || sel.rangeCount === 0) return;

		const tag = wrapTagFor(kind);

		if (!sel.isCollapsed) {
			const range = sel.getRangeAt(0);
			if (rangeIsFullyFormatted(range, kind)) {
				// OFF: remove bold/italic/… from the selection
				removeFormatFromSelection(range, kind, sel);
			} else {
				// ON: wrap selection
				const el = wrapRangeWithTag(range, tag);
				// Flatten nested same-format
				el.querySelectorAll(formatCssSelector(kind)).forEach((n) =>
					unwrapElement(n as HTMLElement)
				);
				const r = document.createRange();
				r.selectNodeContents(el);
				sel.removeAllRanges();
				sel.addRange(r);
			}
		} else {
			// Collapsed caret — toggle typing style on/off
			const inside = closestInlineFormat(sel.anchorNode, kind);
			if (inside) {
				// OFF: leave format so rest of text is normal
				exitInlineFormat(inside, sel);
			} else {
				// ON: insert empty format node, caret inside
				const el =
					kind === 'code' ? createCodeElement() : document.createElement(tag);
				const text = document.createTextNode('\u200b');
				el.appendChild(text);
				const range = sel.getRangeAt(0);
				range.insertNode(el);
				const r = document.createRange();
				r.setStart(text, 1);
				r.collapse(true);
				sel.removeAllRanges();
				sel.addRange(r);
			}
		}

		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
	}

	/**
	 * Backtick markdown:
	 * - selection + `  → wrap selection in <code>
	 * - `word` (closing `) → turn word into <code>
	 * - inside <code> + ` → exit code (rest is normal)
	 */
	function tryBacktickCode(): boolean {
		if (!rootEl || eventStore.applying || composing) return false;
		const sel = window.getSelection();
		if (!sel || sel.rangeCount === 0) return false;
		if (!sel.anchorNode || !rootEl.contains(sel.anchorNode)) return false;

		// Don't hijack inside fenced pre>code
		let n: Node | null = sel.anchorNode;
		while (n && n !== rootEl) {
			if (n instanceof HTMLElement && n.tagName === 'PRE') return false;
			n = n.parentNode;
		}

		// Selection → wrap as code
		if (!sel.isCollapsed) {
			toggleInlineKind('code');
			return true;
		}

		// Already in code → second ` exits (like toggle off)
		const inside = closestInlineFormat(sel.anchorNode, 'code');
		if (inside) {
			exitInlineFormat(inside, sel);
			flushPendingCommit();
			commitNow('format');
			devMdMarkDirty();
			return true;
		}

		// Closing backtick: find opening ` in the same block before caret
		const range = sel.getRangeAt(0);
		const block =
			(sel.anchorNode instanceof HTMLElement
				? sel.anchorNode
				: sel.anchorNode?.parentElement) ?? null;
		// walk to a sensible text container
		let host: HTMLElement | null = block;
		while (
			host &&
			host !== rootEl &&
			!['P', 'DIV', 'LI', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'TD', 'TH'].includes(
				host.tagName
			)
		) {
			host = host.parentElement;
		}
		if (!host || host === rootEl) {
			// still try with direct text node scan
			host = rootEl;
		}

		// Build plain text before caret within host + find last `
		const pre = document.createRange();
		pre.selectNodeContents(host);
		pre.setEnd(range.startContainer, range.startOffset);
		const before = pre.toString().replace(/\u200c/g, '');
		const tick = before.lastIndexOf('`');
		if (tick < 0) return false; // let browser insert a literal `

		const inner = before.slice(tick + 1);
		// Empty or has newline → not a markdown code span
		if (!inner.length || /[\n\r]/.test(inner)) return false;
		// Avoid matching across too much (whole paragraph)
		if (inner.length > 200) return false;

		// Delete from opening ` through caret, insert <code>inner</code>
		// Locate the opening backtick as a text position in host
		const opener = findTextPosition(host, tick);
		const closer = {
			node: range.startContainer,
			offset: range.startOffset
		};
		if (!opener) return false;

		const del = document.createRange();
		del.setStart(opener.node, opener.offset);
		del.setEnd(closer.node, closer.offset);
		del.deleteContents();

		const code = createCodeElement();
		code.textContent = inner;
		del.insertNode(code);

		// Caret after code
		const marker = document.createTextNode('');
		code.after(marker);
		const r = document.createRange();
		r.setStart(marker, 0);
		r.collapse(true);
		sel.removeAllRanges();
		sel.addRange(r);

		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	/** Map a character offset within element's textContent to a text node + offset */
	function findTextPosition(
		root: HTMLElement,
		charOffset: number
	): { node: Text; offset: number } | null {
		const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
		let remaining = charOffset;
		let node = walker.nextNode() as Text | null;
		while (node) {
			const len = node.length;
			if (remaining <= len) {
				return { node, offset: remaining };
			}
			remaining -= len;
			node = walker.nextNode() as Text | null;
		}
		return null;
	}

	function handleEditHotkeys(e: KeyboardEvent): boolean {
		if (!active || !isMod(e) || e.altKey) return false;
		if (isSaveKey(e) && !e.shiftKey) {
			e.preventDefault();
			e.stopPropagation();
			flushPendingCommit();
			void devMdSave();
			return true;
		}
		// Redo first (Ctrl+Shift+Z uses KeyZ)
		if (isRedoKey(e)) {
			e.preventDefault();
			e.stopPropagation();
			redoEdit();
			return true;
		}
		if (isUndoKey(e) && !e.shiftKey) {
			e.preventDefault();
			e.stopPropagation();
			undoEdit();
			return true;
		}
		// Inline styles: toggle on/off (second press = normal text for the rest)
		// Manual DOM — no execCommand (style spans broke toggle-off)
		if (!e.shiftKey && isItalicKey(e)) {
			e.preventDefault();
			e.stopPropagation();
			toggleInlineKind('italic');
			return true;
		}
		if (!e.shiftKey && isBoldKey(e)) {
			e.preventDefault();
			e.stopPropagation();
			toggleInlineKind('bold');
			return true;
		}
		if (!e.shiftKey && isUnderlineKey(e)) {
			e.preventDefault();
			e.stopPropagation();
			toggleInlineKind('underline');
			return true;
		}
		// Ctrl+M → inline code (`like this`)
		if (!e.shiftKey && isCodeKey(e)) {
			e.preventDefault();
			e.stopPropagation();
			toggleInlineKind('code');
			return true;
		}
		// Ctrl+H → highlight (same toggle / edge-exit as italic)
		if (!e.shiftKey && isHighlightKey(e)) {
			e.preventDefault();
			e.stopPropagation();
			toggleInlineKind('highlight');
			return true;
		}
		return false;
	}

	const BLOCK_TAGS = new Set([
		'P',
		'DIV',
		'LI',
		'H1',
		'H2',
		'H3',
		'H4',
		'H5',
		'H6',
		'BLOCKQUOTE',
		'PRE'
	]);

	function isHeadingTag(tag: string) {
		return /^H[1-6]$/.test(tag);
	}

	/**
	 * Nearest block for markdown shortcuts.
	 * Includes headings (so `##`+Space can re-level).
	 * If text sits directly in the contenteditable root, returns the root.
	 */
	function blockAtCaret(opts?: {
		allowHeading?: boolean;
		allowRoot?: boolean;
	}): { sel: Selection; block: HTMLElement } | null {
		if (!rootEl || eventStore.applying || composing) return null;
		const sel = window.getSelection();
		if (!sel || sel.rangeCount === 0 || !sel.isCollapsed) return null;
		const node = sel.anchorNode;
		if (!node || !rootEl.contains(node)) return null;

		let block: HTMLElement | null =
			node.nodeType === Node.TEXT_NODE
				? (node.parentElement as HTMLElement | null)
				: node instanceof HTMLElement
					? node
					: node.parentElement;
		while (block && block !== rootEl) {
			if (BLOCK_TAGS.has(block.tagName)) break;
			block = block.parentElement;
		}
		if (!block) return null;

		// Bare text / inline nodes as direct children of the editable root
		if (block === rootEl) {
			if (opts?.allowRoot === false) return null;
			return { sel, block: rootEl };
		}

		if (block.tagName === 'LI' || block.tagName === 'PRE' || block.tagName === 'BLOCKQUOTE') {
			return null;
		}
		if (isHeadingTag(block.tagName) && opts?.allowHeading === false) return null;
		return { sel, block };
	}

	/** Caret offset within block.textContent (for line-start markdown prefixes). */
	function caretOffsetInBlock(block: HTMLElement, sel: Selection): number {
		const range = sel.getRangeAt(0);
		const pre = range.cloneRange();
		pre.selectNodeContents(block);
		pre.setEnd(range.startContainer, range.startOffset);
		return pre.toString().replace(/\u200c/g, '').length;
	}

	function placeCaretIn(el: HTMLElement, atEnd = false) {
		const sel = window.getSelection();
		if (!sel) return;
		const range = document.createRange();
		if (atEnd) {
			range.selectNodeContents(el);
			range.collapse(false);
		} else if (el.childNodes.length === 0) {
			el.appendChild(document.createTextNode(''));
			range.setStart(el.firstChild!, 0);
			range.collapse(true);
		} else {
			range.setStart(el, 0);
			range.collapse(true);
		}
		sel.removeAllRanges();
		sel.addRange(range);
	}

	/** Place caret at a character offset inside element's text. */
	function placeCaretAtTextOffset(el: HTMLElement, offset: number) {
		const sel = window.getSelection();
		if (!sel) return;
		const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
		let remaining = Math.max(0, offset);
		let node = walker.nextNode() as Text | null;
		let last: Text | null = null;
		while (node) {
			last = node;
			const len = node.length;
			if (remaining <= len) {
				const range = document.createRange();
				range.setStart(node, remaining);
				range.collapse(true);
				sel.removeAllRanges();
				sel.addRange(range);
				return;
			}
			remaining -= len;
			node = walker.nextNode() as Text | null;
		}
		if (last) {
			const range = document.createRange();
			range.setStart(last, last.length);
			range.collapse(true);
			sel.removeAllRanges();
			sel.addRange(range);
		} else {
			placeCaretIn(el, true);
		}
	}

	function replaceBlock(block: HTMLElement, next: HTMLElement) {
		if (block === rootEl) {
			// Editable root: swap all content for the new node (+ keep structure clean)
			rootEl.replaceChildren(next);
		} else {
			block.replaceWith(next);
		}
	}

	/**
	 * Markdown-style: a block that is only --- / *** / ___ becomes a real <hr> line.
	 * Turndown would otherwise escape <p>---</p> as `\---` (literal dashes, not a rule).
	 */
	function tryPromoteDashLineToHr(): boolean {
		const ctx = blockAtCaret({ allowHeading: false, allowRoot: true });
		if (!ctx) return false;
		const { block } = ctx;

		const t = (block.textContent || '').replace(/\u200c/g, '').trim();
		if (!/^(?:-{3,}|\*{3,}|_{3,}|(?:-\s*){3,})$/.test(t)) return false;

		const hr = document.createElement('hr');
		const after = makeBlock('p');
		after.innerHTML = '<br>';
		if (block === rootEl) {
			rootEl.replaceChildren(hr, after);
		} else {
			block.replaceWith(hr);
			hr.after(after);
		}
		placeCaretIn(after);

		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	/**
	 * Markdown ATX at line start:
	 *   ## + Space  → <h2>…</h2>   (# → h1 … ###### → h6)
	 *   ## Title + Enter → heading + new paragraph
	 *
	 * Works in paragraphs, bare root text, and existing headings (re-level).
	 */
	function tryPromoteAtxHeading(trigger: 'space' | 'enter'): boolean {
		const ctx = blockAtCaret({ allowHeading: true, allowRoot: true });
		if (!ctx) return false;
		const { sel, block } = ctx;

		const raw = (block.textContent || '').replace(/\u200c/g, '');
		// Don't treat multi-line root dump as one heading line unless it's a single logical line
		if (block === rootEl && /[\n\r]/.test(raw) && raw.trim().includes('\n')) {
			// still allow if only one non-empty line of pure atx
			const lines = raw.split(/\n/).map((l) => l.trim()).filter(Boolean);
			if (lines.length !== 1) return false;
		}

		if (trigger === 'space') {
			const offset = caretOffsetInBlock(block, sel);
			const before = raw.slice(0, offset);
			// Caret must sit right after 1–6 hashes at the very start of the block
			const m = before.match(/^(#{1,6})$/);
			if (!m) return false;
			// No non-hash junk before caret; rest of line becomes the title
			const level = m[1].length;
			const title = raw.slice(offset).replace(/^\s+/, '');
			const h = makeBlock(`h${level}`) as HTMLHeadingElement;
			if (title) {
				h.textContent = title;
			} else {
				h.appendChild(document.createTextNode(''));
			}
			replaceBlock(block, h);
			// Caret at start of title (after the markdown prefix we consumed)
			placeCaretAtTextOffset(h, 0);
			flushPendingCommit();
			commitNow('format');
			devMdMarkDirty();
			return true;
		}

		// Enter: full ATX line with title (caret anywhere on that line)
		const t = raw.trim();
		const m = t.match(/^(#{1,6})[ \t]+(.+)$/);
		if (!m) return false;
		const level = m[1].length;
		const title = m[2].replace(/\s+#+\s*$/, '').trim();
		if (!title) return false;

		const h = makeBlock(`h${level}`) as HTMLHeadingElement;
		h.textContent = title;
		const after = makeBlock('p');
		after.innerHTML = '<br>';
		if (block === rootEl) {
			rootEl.replaceChildren(h, after);
		} else {
			block.replaceWith(h);
			h.after(after);
		}
		placeCaretIn(after);

		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	/**
	 * Markdown bullet at line start:
	 *   - + Space  → <ul><li>…</li></ul>
	 *   * + Space  → same
	 *   + + Space  → same
	 * Appends to the previous <ul> when the block sits right after a list.
	 * (Single `-` only — `---` stays a horizontal rule.)
	 */
	function tryPromoteBulletList(): boolean {
		const ctx = blockAtCaret({ allowHeading: false, allowRoot: true });
		if (!ctx) return false;
		const { sel, block } = ctx;
		if (isHeadingTag(block.tagName)) return false;

		const raw = (block.textContent || '').replace(/\u200c/g, '');
		if (block === rootEl && raw.includes('\n')) {
			const lines = raw
				.split(/\n/)
				.map((l) => l.trim())
				.filter(Boolean);
			if (lines.length !== 1) return false;
		}

		const offset = caretOffsetInBlock(block, sel);
		const before = raw.slice(0, offset);
		// Exactly one bullet marker before caret at line start
		if (!/^[-*+]$/.test(before)) return false;

		const rest = raw.slice(offset).replace(/^\s+/, '');
		const li = document.createElement('li');
		// no dir on li — keeps bullet gutter padding identical to view mode
		if (rest) li.textContent = rest;
		else li.appendChild(document.createTextNode(''));

		const prev =
			block === rootEl
				? null
				: (block.previousElementSibling as HTMLElement | null);

		if (prev && prev.tagName === 'UL') {
			// Continue existing list
			if (block === rootEl) {
				/* unreachable with prev */
			} else {
				block.remove();
			}
			prev.setAttribute('dir', 'rtl');
			prev.appendChild(li);
			placeCaretAtTextOffset(li, 0);
		} else {
			const ul = document.createElement('ul');
			ul.setAttribute('dir', 'rtl');
			ul.appendChild(li);
			replaceBlock(block, ul);
			placeCaretAtTextOffset(li, 0);
		}

		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	function listItemAtCaret(): { sel: Selection; li: HTMLElement; list: HTMLElement } | null {
		if (!rootEl || eventStore.applying || composing) return null;
		const sel = window.getSelection();
		if (!sel || !sel.isCollapsed || sel.rangeCount === 0) return null;
		const node = sel.anchorNode;
		if (!node || !rootEl.contains(node)) return null;

		let el: HTMLElement | null =
			node.nodeType === Node.TEXT_NODE
				? (node.parentElement as HTMLElement | null)
				: node instanceof HTMLElement
					? node
					: null;
		while (el && el !== rootEl && el.tagName !== 'LI') {
			el = el.parentElement;
		}
		if (!el || el.tagName !== 'LI') return null;
		const list = el.parentElement;
		if (!list || (list.tagName !== 'UL' && list.tagName !== 'OL')) return null;
		return { sel, li: el, list };
	}

	/**
	 * Tab in a bullet/numbered item → nest one level under the previous item.
	 * Shift+Tab → outdent one level.
	 */
	function tryListIndent(): boolean {
		const ctx = listItemAtCaret();
		if (!ctx) return false;
		const { sel, li, list } = ctx;
		const prev = li.previousElementSibling;
		if (!prev || prev.tagName !== 'LI') return false;

		const caretOff = caretOffsetInBlock(li, sel);
		const listTag = list.tagName === 'OL' ? 'ol' : 'ul';

		// Prefer an existing nested list of the same kind at the end of prev
		let nested: HTMLElement | null = null;
		for (let c = prev.lastElementChild; c; c = c.previousElementSibling as Element | null) {
			if (c.tagName === 'UL' || c.tagName === 'OL') {
				nested = c as HTMLElement;
				break;
			}
		}
		if (!nested) {
			nested = document.createElement(listTag);
			nested.setAttribute('dir', 'rtl');
			prev.appendChild(nested);
		} else {
			nested.setAttribute('dir', 'rtl');
		}

		nested.appendChild(li);
		placeCaretAtTextOffset(li, Math.min(caretOff, (li.textContent || '').length));
		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	function tryListOutdent(): boolean {
		const ctx = listItemAtCaret();
		if (!ctx) return false;
		const { sel, li, list } = ctx;

		// Must be inside a nested list (parent of list is an LI)
		const parentLi = list.parentElement;
		if (!parentLi || parentLi.tagName !== 'LI') return false;
		const outerList = parentLi.parentElement;
		if (!outerList || (outerList.tagName !== 'UL' && outerList.tagName !== 'OL')) {
			return false;
		}

		const caretOff = caretOffsetInBlock(li, sel);

		// Move this item (and following siblings in the nested list) after parentLi
		// Standard: only current item; keep later nested siblings in nested list
		parentLi.after(li);

		if (list.childElementCount === 0) {
			list.remove();
		}

		placeCaretAtTextOffset(li, Math.min(caretOff, (li.textContent || '').length));
		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	function tryListTab(e: KeyboardEvent): boolean {
		if (e.key !== 'Tab') return false;
		if (!listItemAtCaret()) return false;
		// Always prevent focus-steal when in a list
		e.preventDefault();
		if (e.shiftKey) tryListOutdent();
		else tryListIndent();
		return true;
	}

	/** Empty bullet (only br / zwsp / whitespace) — not real text or media */
	function isEffectivelyEmptyBlock(el: HTMLElement): boolean {
		const probe = el.cloneNode(true) as HTMLElement;
		probe.querySelectorAll('br').forEach((b) => b.remove());
		if (probe.querySelector('img, svg, video, iframe, table, pre, hr')) return false;
		const t = (probe.textContent || '')
			.replace(/[\u200b\u200c\u200d\ufeff\u00a0]/g, '')
			.replace(/\s+/g, '');
		return t.length === 0;
	}

	/**
	 * Lift list item out to a normal <p>.
	 * Splits the list when the item is in the middle.
	 */
	function exitListItemToParagraph(li: HTMLElement, list: HTMLElement) {
		const p = makeBlock('p');
		// Keep any residual content (usually empty → br)
		while (li.firstChild) p.appendChild(li.firstChild);
		if (isEffectivelyEmptyBlock(p)) {
			p.replaceChildren();
			p.innerHTML = '<br>';
		}

		const afterNodes: ChildNode[] = [];
		while (li.nextSibling) afterNodes.push(li.nextSibling);
		li.remove();

		if (list.childElementCount === 0) {
			// Was the only item
			list.replaceWith(p);
		} else if (afterNodes.length === 0) {
			// Was last item → paragraph after list
			list.after(p);
		} else {
			// Middle: keep items before, p, then new list with items after
			const afterList = document.createElement(list.tagName.toLowerCase());
			for (const n of afterNodes) afterList.appendChild(n);
			list.after(p);
			p.after(afterList);
			if (afterList.childElementCount === 0) afterList.remove();
		}

		// Drop list if it became empty (shouldn't, but safe)
		if (list.isConnected && list.childElementCount === 0) list.remove();

		placeCaretIn(p);
		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
	}

	/**
	 * Enter on empty bullet → normal paragraph (leave the list).
	 * Enter on non-empty bullet → browser default (new bullet line).
	 */
	function tryExitEmptyListItem(): boolean {
		const ctx = listItemAtCaret();
		if (!ctx) return false;
		if (!isEffectivelyEmptyBlock(ctx.li)) return false;
		exitListItemToParagraph(ctx.li, ctx.list);
		return true;
	}

	/**
	 * Backspace at the start of a heading → demote to normal paragraph (keep text).
	 * Matches common editors (Notion / Docs style).
	 */
	function tryHeadingBackspace(): boolean {
		if (!rootEl || eventStore.applying || composing) return false;
		const sel = window.getSelection();
		if (!sel || !sel.isCollapsed || sel.rangeCount === 0) return false;
		const node = sel.anchorNode;
		if (!node || !rootEl.contains(node)) return false;

		let el: HTMLElement | null =
			node.nodeType === Node.TEXT_NODE
				? (node.parentElement as HTMLElement | null)
				: node instanceof HTMLElement
					? node
					: null;
		while (el && el !== rootEl && !/^H[1-6]$/.test(el.tagName)) {
			el = el.parentElement;
		}
		if (!el || el === rootEl || !/^H[1-6]$/.test(el.tagName)) return false;

		// Only at the very start of the heading
		if (!isCaretAtFormatBoundary(el, 'start')) return false;

		const p = makeBlock('p');
		// Move all children (text + inline markup)
		while (el.firstChild) p.appendChild(el.firstChild);
		if (!(p.textContent || '').replace(/[\u200b\u200c\ufeff]/g, '').trim() && !p.querySelector('img, br')) {
			p.innerHTML = '<br>';
		}
		el.replaceWith(p);
		// Caret at start of the new paragraph
		placeCaretIn(p, false);
		// If empty <br> only, caret is fine; if text, put at offset 0
		if ((p.textContent || '').replace(/[\u200b\u200c\ufeff]/g, '').length > 0) {
			placeCaretAtTextOffset(p, 0);
		}

		flushPendingCommit();
		commitNow('format');
		devMdMarkDirty();
		return true;
	}

	/**
	 * Backspace in a bullet line:
	 * - empty item → normal paragraph
	 * - caret at start of non-empty item → merge into previous item, or unwrap first item to <p>
	 */
	function tryListBackspace(): boolean {
		const ctx = listItemAtCaret();
		if (!ctx) return false;
		const { sel, li, list } = ctx;

		const offset = caretOffsetInBlock(li, sel);
		if (offset !== 0) return false;

		if (isEffectivelyEmptyBlock(li)) {
			exitListItemToParagraph(li, list);
			return true;
		}

		const prev = li.previousElementSibling;
		if (prev && prev.tagName === 'LI') {
			// Merge into previous bullet
			const prevEl = prev as HTMLElement;
			const joinAt = (prevEl.textContent || '').replace(/\u200c/g, '').length;
			// Avoid gluing without a space if both sides have text
			if (
				joinAt > 0 &&
				(li.textContent || '').replace(/\u200c/g, '').trim().length > 0 &&
				!/\s$/.test(prevEl.textContent || '') &&
				!/^\s/.test(li.textContent || '')
			) {
				// soft join — no forced space (matches most editors)
			}
			while (li.firstChild) prevEl.appendChild(li.firstChild);
			li.remove();
			if (list.childElementCount === 0) list.remove();
			placeCaretAtTextOffset(prevEl, joinAt);
			flushPendingCommit();
			commitNow('format');
			devMdMarkDirty();
			return true;
		}

		// First item, caret at start → unwrap to normal paragraph above remaining list
		exitListItemToParagraph(li, list);
		return true;
	}

	function onMarkdownSpaceShortcut(): boolean {
		// Order: exit code → heading → hr (---) → bullet (-)
		return (
			tryExitCodeOnSpace() ||
			tryPromoteAtxHeading('space') ||
			tryPromoteDashLineToHr() ||
			tryPromoteBulletList()
		);
	}

	function onKeydown(e: KeyboardEvent) {
		if (handleEditHotkeys(e)) return;
		if (e.ctrlKey || e.metaKey || e.altKey) return;

		// Tab / Shift+Tab in bullets → indent / outdent
		if (tryListTab(e)) {
			e.stopPropagation();
			return;
		}

		// Leave inline code / em at edge: ← at end → space after + caret outside
		if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
			if (tryExitInlineOnArrow(e)) {
				e.stopPropagation();
				return;
			}
		}

		// `code` markdown + selection wrap
		if (isBacktickKey(e) && !e.shiftKey) {
			// On some layouts Dead key: only handle when key is actually `
			if (e.key === 'Dead' && e.code !== 'Backquote') {
				/* fall through */
			} else if (tryBacktickCode()) {
				e.preventDefault();
				e.stopPropagation();
				return;
			}
		}

		// ↑ / ↓ must land on --- as a selectable line
		if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
			if (tryHrArrowNav(e)) {
				e.stopPropagation();
			}
			return;
		}

		if (e.key === 'Enter') {
			// Enter on selected --- → new paragraph after the rule
			const hr = selectedHr();
			if (hr) {
				e.preventDefault();
				e.stopPropagation();
				clearHrSelection();
				const p = makeBlock('p');
				p.innerHTML = '<br>';
				hr.after(p);
				placeCaretIn(p);
				flushPendingCommit();
				commitNow('format');
				devMdMarkDirty();
				return;
			}
			if (
				tryExitEmptyListItem() ||
				tryPromoteAtxHeading('enter') ||
				tryPromoteDashLineToHr()
			) {
				e.preventDefault();
				e.stopPropagation();
				return;
			}
			// Browser-created blocks: keep RTL chrome matching view mode
			queueMicrotask(() => {
				if (rootEl) normalizeBlockAutoDir(rootEl);
			});
			return;
		}

		if (e.key === 'Backspace' || e.key === 'Delete') {
			if (tryHrDelete()) {
				e.preventDefault();
				e.stopPropagation();
				return;
			}
			if (e.key === 'Backspace' && (tryHeadingBackspace() || tryListBackspace())) {
				e.preventDefault();
				e.stopPropagation();
			}
			return;
		}

		// Space: ## → heading, --- → line, - → bullet
		if (e.key === ' ' || e.code === 'Space' || e.key === 'Spacebar') {
			if (onMarkdownSpaceShortcut()) {
				e.preventDefault();
			}
		}
	}

	function onWindowPointerDown(e: PointerEvent) {
		if (!menu || ignoreOutsideClick) return;
		const t = e.target;
		if (t instanceof Element && t.closest('.dev-link-menu')) return;
		menu = null;
	}

	function onWindowKey(e: KeyboardEvent) {
		// Capture undo/redo/save even if focus is odd (menu open, etc.)
		if (handleEditHotkeys(e)) return;
		if (e.key !== 'Escape' || !menu) return;
		e.preventDefault();
		if (menu.view === 'edit') backToMain();
		else menu = null;
	}

	function stop(e: Event) {
		e.stopPropagation();
	}
</script>

<!-- capture so Ctrl+Z is not stolen / missed when focus is on contenteditable -->
<svelte:window
	onpointerdown={onWindowPointerDown}
	onkeydowncapture={onWindowKey}
/>

{#if active}
	<!-- Editable host: no Svelte children — only manual innerHTML (stable Enter/caret) -->
	<div
		bind:this={rootEl}
		class="nd-article__wysiwyg nd-article__wysiwyg--on"
		data-dev-wysiwyg="1"
		contenteditable="true"
		role="textbox"
		tabindex="0"
		dir="rtl"
		aria-multiline="true"
		aria-label="ویرایش متن صفحه"
		oninput={onInput}
		onbeforeinput={onBeforeInput}
		onpaste={onPaste}
		oncut={onCut}
		oncompositionstart={onCompositionStart}
		oncompositionend={onCompositionEnd}
		onclick={onClick}
		onkeydown={onKeydown}
		oncontextmenu={onContextMenu}
	></div>
{:else}
	<!-- Read-only rendered MD; snapshot for edit mode via data-dev-md-view -->
	<div bind:this={viewEl} class="nd-article__wysiwyg" data-dev-md-view="1">
		{@render children()}
	</div>
{/if}

{#if menu}
	<div
		class="dev-link-menu"
		class:dev-link-menu--edit={menu.view === 'edit'}
		style:left="{menu.x}px"
		style:top="{menu.y}px"
		role="menu"
		tabindex="-1"
		data-no-panel
		onpointerdown={stop}
		onclick={stop}
		onkeydown={stop}
	>
		{#if menu.view === 'main'}
			<div class="dev-link-menu__href" dir="ltr" title={menu.href}>
				{menu.href || '—'}
			</div>
			<button
				type="button"
				class="dev-link-menu__item"
				role="menuitem"
				onpointerdown={stop}
				onclick={openEditPage}
			>
				ویرایش پیوند…
			</button>
			<button
				type="button"
				class="dev-link-menu__item"
				role="menuitem"
				onpointerdown={stop}
				onclick={copyLinkHref}
			>
				کپی آدرس
			</button>
			<button
				type="button"
				class="dev-link-menu__item"
				role="menuitem"
				onpointerdown={stop}
				onclick={openLinkNewTab}
			>
				باز کردن در تب جدید
			</button>
			<button
				type="button"
				class="dev-link-menu__item dev-link-menu__item--danger"
				role="menuitem"
				onpointerdown={stop}
				onclick={removeLink}
			>
				حذف پیوند (نگه داشتن متن)
			</button>
		{:else}
			<button
				type="button"
				class="dev-link-menu__back"
				onpointerdown={stop}
				onclick={backToMain}
			>
				<span class="dev-link-menu__back-icon" aria-hidden="true">
					<Icon name="arrow-right" size={14} />
				</span>
				بازگشت
			</button>
			<label class="dev-link-menu__field">
				متن
				<input
					class="dev-link-menu__input"
					type="text"
					bind:value={menu.text}
					dir="auto"
					onpointerdown={stop}
					onclick={stop}
				/>
			</label>
			<label class="dev-link-menu__field">
				آدرس
				<input
					class="dev-link-menu__input"
					type="text"
					bind:value={menu.href}
					dir="ltr"
					placeholder="/pages/… or https://…"
					onpointerdown={stop}
					onclick={stop}
				/>
			</label>
			<div class="dev-link-menu__edit-actions">
				<button
					type="button"
					class="dev-link-menu__action dev-link-menu__action--primary"
					onpointerdown={stop}
					onclick={applyLinkEdit}
				>
					اعمال
				</button>
				<button
					type="button"
					class="dev-link-menu__action"
					onpointerdown={stop}
					onclick={backToMain}
				>
					انصراف
				</button>
			</div>
		{/if}
	</div>
{/if}

<style>
	.nd-article__wysiwyg {
		min-width: 0;
		width: 100%;
	}

	.nd-article__wysiwyg--on {
		outline: none;
		caret-color: var(--accent);
		/* Same base direction as view mode (.prose / page RTL) — no plaintext flip */
		direction: rtl;
		text-align: start; /* = right in RTL */
		unicode-bidi: normal;
	}

	/* Keep block metrics identical to .prose (no UA contenteditable quirks) */
	.nd-article__wysiwyg--on :global(p),
	.nd-article__wysiwyg--on :global(blockquote),
	.nd-article__wysiwyg--on :global(h1),
	.nd-article__wysiwyg--on :global(h2),
	.nd-article__wysiwyg--on :global(h3),
	.nd-article__wysiwyg--on :global(h4),
	.nd-article__wysiwyg--on :global(h5),
	.nd-article__wysiwyg--on :global(h6) {
		direction: rtl;
		text-align: start;
		unicode-bidi: normal;
	}

	/* Lists: match viewer gutter (physical right for RTL discs) */
	.nd-article__wysiwyg--on :global(ul),
	.nd-article__wysiwyg--on :global(ol) {
		direction: rtl;
		list-style-position: outside;
		padding-inline-start: 0;
		padding-inline-end: 0;
		padding-left: 0;
		padding-right: 1.65rem !important;
		margin-top: 0;
		margin-bottom: 1rem;
	}

	.nd-article__wysiwyg--on :global(ul) {
		list-style-type: disc;
	}

	.nd-article__wysiwyg--on :global(ol) {
		list-style-type: decimal;
	}

	.nd-article__wysiwyg--on :global(ul ul),
	.nd-article__wysiwyg--on :global(ol ol),
	.nd-article__wysiwyg--on :global(ul ol),
	.nd-article__wysiwyg--on :global(ol ul) {
		margin-top: 0.35rem;
		margin-bottom: 0.35rem;
		padding-right: 1.35rem !important;
	}

	.nd-article__wysiwyg--on :global(li) {
		direction: rtl;
		text-align: start;
		margin: 0.35rem 0;
		padding-right: 0.15rem;
		padding-left: 0;
	}

	.nd-article__wysiwyg--on :global(a) {
		cursor: context-menu;
		text-decoration: underline;
		text-underline-offset: 0.12em;
	}

	.nd-article__wysiwyg--on :global(img) {
		pointer-events: none;
	}

	/* Horizontal rule must look like a clear line in edit mode */
	.nd-article__wysiwyg--on :global(hr) {
		border: none;
		border-top: 2px solid var(--line);
		margin: 1.25rem 0;
		height: 0;
		/* hit target for click / selection */
		padding: 0.55rem 0;
		background: transparent;
		background-clip: content-box;
		cursor: pointer;
		border-radius: 0.15rem;
	}

	/* Selected --- line (arrow up/down or click) */
	.nd-article__wysiwyg--on :global(hr.dev-hr--selected) {
		border-top-color: var(--accent);
		outline: 2px solid color-mix(in srgb, var(--accent) 55%, transparent);
		outline-offset: 2px;
		background: color-mix(in srgb, var(--accent) 10%, transparent);
		background-clip: padding-box;
	}

	.dev-link-menu {
		position: fixed;
		z-index: 13000;
		min-width: 13rem;
		max-width: min(20rem, calc(100vw - 1rem));
		padding: 0.3rem;
		border-radius: 0.55rem;
		background: var(--bg);
		border: 1px solid var(--line);
		box-shadow: 0 10px 28px color-mix(in srgb, #0f172a 16%, transparent);
		font-family: var(--font-ui);
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
	}

	.dev-link-menu--edit {
		min-width: 16rem;
		padding: 0.5rem;
		gap: 0.45rem;
	}

	.dev-link-menu__href {
		margin: 0 0.25rem 0.2rem;
		padding: 0.3rem 0.4rem;
		border-radius: 0.35rem;
		background: var(--bg-soft);
		font-family: ui-monospace, Menlo, Consolas, monospace;
		font-size: 0.65rem;
		color: var(--muted);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.dev-link-menu__item {
		display: block;
		width: 100%;
		margin: 0;
		padding: 0.45rem 0.55rem;
		border: none;
		border-radius: 0.35rem;
		background: transparent;
		color: var(--fg);
		font-family: var(--font-ui);
		font-size: 0.8rem;
		font-weight: 600;
		text-align: start;
		cursor: pointer;
	}
	.dev-link-menu__item:hover {
		background: color-mix(in srgb, var(--accent) 12%, var(--bg));
	}
	.dev-link-menu__item--danger:hover {
		background: color-mix(in srgb, #ef4444 12%, var(--bg));
		color: #b91c1c;
	}

	.dev-link-menu__back {
		display: inline-flex;
		align-items: center;
		gap: 0.3rem;
		align-self: flex-start;
		margin: 0;
		padding: 0.3rem 0.45rem;
		border: none;
		border-radius: 0.3rem;
		background: transparent;
		color: var(--accent);
		font-family: var(--font-ui);
		font-size: 0.75rem;
		font-weight: 700;
		cursor: pointer;
	}
	.dev-link-menu__back:hover {
		background: color-mix(in srgb, var(--accent) 10%, var(--bg));
	}
	.dev-link-menu__back-icon {
		display: inline-flex;
		line-height: 0;
	}

	.dev-link-menu__field {
		display: flex;
		flex-direction: column;
		gap: 0.22rem;
		font-size: 0.72rem;
		font-weight: 600;
		color: var(--muted);
		padding: 0 0.1rem;
	}

	.dev-link-menu__input {
		width: 100%;
		box-sizing: border-box;
		margin: 0;
		padding: 0.45rem 0.55rem;
		border: 1px solid var(--line);
		border-radius: 0.4rem;
		background: var(--bg-soft);
		color: var(--fg);
		font-family: inherit;
		font-size: 0.85rem;
		font-weight: 500;
	}
	.dev-link-menu__input:focus {
		outline: 2px solid color-mix(in srgb, var(--accent) 45%, transparent);
		outline-offset: 1px;
	}

	.dev-link-menu__edit-actions {
		display: flex;
		gap: 0.35rem;
		padding-top: 0.1rem;
	}

	.dev-link-menu__action {
		flex: 1;
		margin: 0;
		padding: 0.45rem 0.5rem;
		border: 1px solid var(--line);
		border-radius: 0.4rem;
		background: var(--bg-soft);
		color: var(--fg);
		font-family: var(--font-ui);
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
	}
	.dev-link-menu__action--primary {
		background: color-mix(in srgb, var(--accent) 16%, var(--bg));
		border-color: color-mix(in srgb, var(--accent) 40%, var(--line));
	}
</style>
