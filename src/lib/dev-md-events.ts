/**
 * Event-sourced undo/redo for the WYSIWYG contenteditable editor.
 *
 * Stream of events (each carries before/after HTML + optional selection).
 * Cursor points at the last applied event; state = fold(events[0..cursor]).
 *
 * undo  → cursor--  and restore events[cursor].htmlAfter (or base if -1)
 * redo  → cursor++  and restore events[cursor].htmlAfter
 */

export type EditEventType =
	| 'init'
	| 'input'
	| 'paste'
	| 'cut'
	| 'link-edit'
	| 'link-remove'
	| 'format'
	| 'other';

export type SelectionBookmark = {
	/** Character offset in the root's text content */
	start: number;
	end: number;
};

export type EditEvent = {
	id: number;
	type: EditEventType;
	/** Document HTML after this event was applied */
	htmlAfter: string;
	/** Selection after this event (best-effort) */
	selection?: SelectionBookmark | null;
	/** wall-clock for debugging */
	at: number;
};

export type EditEventStore = {
	/** Base HTML before any user events (init) */
	baseHtml: string;
	events: EditEvent[];
	/** Index into events; -1 means baseHtml only */
	cursor: number;
	nextId: number;
	applying: boolean;
	maxEvents: number;
};

export function createEditEventStore(maxEvents = 150): EditEventStore {
	return {
		baseHtml: '',
		events: [],
		cursor: -1,
		nextId: 1,
		applying: false,
		maxEvents
	};
}

export function resetEditEvents(store: EditEventStore, html: string, sel?: SelectionBookmark | null) {
	store.baseHtml = html;
	store.events = [
		{
			id: store.nextId++,
			type: 'init',
			htmlAfter: html,
			selection: sel ?? null,
			at: Date.now()
		}
	];
	store.cursor = 0;
	store.applying = false;
}

/** Current HTML according to the event cursor */
export function currentHtml(store: EditEventStore): string {
	if (store.cursor < 0 || store.events.length === 0) return store.baseHtml;
	return store.events[store.cursor]?.htmlAfter ?? store.baseHtml;
}

export function canUndo(store: EditEventStore): boolean {
	return store.cursor > 0;
}

export function canRedo(store: EditEventStore): boolean {
	return store.cursor < store.events.length - 1;
}

/**
 * Append a new event (drops any redo branch beyond cursor).
 * No-op if html is unchanged from current.
 */
export function commitEvent(
	store: EditEventStore,
	type: EditEventType,
	htmlAfter: string,
	selection?: SelectionBookmark | null
): EditEvent | null {
	if (store.applying) return null;
	const prev = currentHtml(store);
	if (prev === htmlAfter) return null;

	// Truncate redo branch
	if (store.cursor < store.events.length - 1) {
		store.events = store.events.slice(0, store.cursor + 1);
	}

	const ev: EditEvent = {
		id: store.nextId++,
		type,
		htmlAfter,
		selection: selection ?? null,
		at: Date.now()
	};
	store.events.push(ev);
	store.cursor = store.events.length - 1;

	// Cap size (keep init + recent)
	while (store.events.length > store.maxEvents) {
		// drop second event (keep init at 0), merge base forward
		if (store.events.length < 2) break;
		const dropped = store.events.splice(1, 1)[0];
		if (dropped) store.baseHtml = dropped.htmlAfter;
		store.cursor = Math.max(0, store.cursor - 1);
	}

	return ev;
}

export function undoEvent(store: EditEventStore): EditEvent | null {
	if (!canUndo(store)) return null;
	store.cursor -= 1;
	return store.events[store.cursor] ?? null;
}

export function redoEvent(store: EditEventStore): EditEvent | null {
	if (!canRedo(store)) return null;
	store.cursor += 1;
	return store.events[store.cursor] ?? null;
}

/* ── Selection bookmarks (text offsets in root) ─────────────────────── */

export function getSelectionBookmark(root: HTMLElement): SelectionBookmark | null {
	const sel = window.getSelection();
	if (!sel || sel.rangeCount === 0) return null;
	const range = sel.getRangeAt(0);
	if (!root.contains(range.commonAncestorContainer)) return null;
	const pre = range.cloneRange();
	pre.selectNodeContents(root);
	pre.setEnd(range.startContainer, range.startOffset);
	const start = pre.toString().length;
	const end = start + range.toString().length;
	return { start, end };
}

export function restoreSelectionBookmark(root: HTMLElement, mark: SelectionBookmark | null | undefined) {
	if (!mark) return;
	const sel = window.getSelection();
	if (!sel) return;

	const pointAt = (offset: number): { node: Node; offset: number } | null => {
		const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
		let remaining = offset;
		let node = walker.nextNode();
		let last: Text | null = null;
		while (node) {
			if (node.nodeType === Node.TEXT_NODE) {
				last = node as Text;
				const len = last.length;
				if (remaining <= len) {
					return { node: last, offset: remaining };
				}
				remaining -= len;
			}
			node = walker.nextNode();
		}
		if (last) {
			return { node: last, offset: last.length };
		}
		return { node: root, offset: 0 };
	};

	const start = pointAt(mark.start);
	const end = pointAt(mark.end);
	if (!start || !end) return;
	try {
		const range = document.createRange();
		range.setStart(start.node, start.offset);
		range.setEnd(end.node, end.offset);
		sel.removeAllRanges();
		sel.addRange(range);
	} catch {
		/* ignore invalid ranges after DOM reshape */
	}
}

/** Apply store cursor state onto a contenteditable root */
export function applyStoreToRoot(store: EditEventStore, root: HTMLElement) {
	store.applying = true;
	try {
		const ev = store.cursor >= 0 ? store.events[store.cursor] : null;
		root.innerHTML = ev?.htmlAfter ?? store.baseHtml;
		restoreSelectionBookmark(root, ev?.selection);
	} finally {
		// next frame so input handlers ignore our write
		requestAnimationFrame(() => {
			store.applying = false;
		});
	}
}
