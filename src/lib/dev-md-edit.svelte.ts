/**
 * Shared state + actions for the dev-only WYSIWYG (contenteditable) page editor.
 */
import { invalidateAll } from '$app/navigation';
import { articleHtmlToMarkdown } from '$lib/html-to-md';

export type DevMdEditState = {
	open: boolean;
	pathname: string;
	/** Live editable root inside the article */
	bodyEl: HTMLElement | null;
	/** Snapshot of HTML when edit started (for dirty / cancel) */
	originalHtml: string;
	/**
	 * HTML copied from the rendered view right before edit mode mounts.
	 * Applied once into the contenteditable host so Svelte children are not
	 * mixed into a live contenteditable (which breaks Enter / caret).
	 */
	seedHtml: string | null;
	siteRel: string;
	docsRel: string | null;
	saving: boolean;
	dirty: boolean;
	errorMsg: string;
	statusMsg: string;
	/** Event-sourced history (updated by DevMdWysiwyg) */
	canUndo: boolean;
	canRedo: boolean;
};

/** Undo/redo handlers registered by the active WYSIWYG host */
export type DevMdHistHandlers = {
	undo: () => boolean;
	redo: () => boolean;
};

let histHandlers: DevMdHistHandlers | null = null;

function createState(): DevMdEditState {
	return {
		open: false,
		pathname: '',
		bodyEl: null,
		originalHtml: '',
		seedHtml: null,
		siteRel: '',
		docsRel: null,
		saving: false,
		dirty: false,
		errorMsg: '',
		statusMsg: '',
		canUndo: false,
		canRedo: false
	};
}

export const devMdEdit = $state(createState());

export function devMdSetHistHandlers(h: DevMdHistHandlers | null) {
	histHandlers = h;
	if (!h) {
		devMdEdit.canUndo = false;
		devMdEdit.canRedo = false;
	}
}

export function devMdSetHistFlags(canUndo: boolean, canRedo: boolean) {
	devMdEdit.canUndo = canUndo;
	devMdEdit.canRedo = canRedo;
}

export function devMdUndo(): boolean {
	return histHandlers?.undo() ?? false;
}

export function devMdRedo(): boolean {
	return histHandlers?.redo() ?? false;
}

export function devMdIsActive(pathname: string): boolean {
	const p = pathname.replace(/\/$/, '') || '/';
	return devMdEdit.open && devMdEdit.pathname === p;
}

export function devMdReset() {
	const el = devMdEdit.bodyEl;
	if (el) {
		el.removeAttribute('contenteditable');
		el.classList.remove('nd-article__wysiwyg--on');
	}
	Object.assign(devMdEdit, createState());
}

export function devMdMarkDirty() {
	if (!devMdEdit.open) return;
	const el = devMdEdit.bodyEl;
	if (!el) {
		devMdEdit.dirty = true;
		return;
	}
	devMdEdit.dirty = el.innerHTML !== devMdEdit.originalHtml;
	if (devMdEdit.statusMsg) devMdEdit.statusMsg = '';
}

export async function devMdOpen(pathname: string) {
	const p = pathname.replace(/\/$/, '') || '/';
	devMdEdit.errorMsg = '';
	devMdEdit.statusMsg = '';
	devMdEdit.pathname = p;
	devMdEdit.dirty = false;
	const res = await fetch(`/api/dev-md?pathname=${encodeURIComponent(p)}`);
	const data = await res.json().catch(() => ({}));
	if (!res.ok) {
		throw new Error(
			(data as { message?: string }).message || res.statusText || 'فایل Markdown پیدا نشد'
		);
	}
	devMdEdit.siteRel = String((data as { siteRel?: string }).siteRel ?? '');
	devMdEdit.docsRel = (data as { docsRel?: string | null }).docsRel
		? String((data as { docsRel: string }).docsRel)
		: null;

	// Snapshot rendered HTML BEFORE toggling edit (view host is unmounted after open)
	if (typeof document !== 'undefined') {
		const view = document.querySelector<HTMLElement>(
			`[data-dev-md-view="1"]`
		);
		devMdEdit.seedHtml = view ? view.innerHTML : '';
	} else {
		devMdEdit.seedHtml = '';
	}

	devMdEdit.open = true;
}

export async function devMdCancel() {
	if (devMdEdit.dirty && !confirm('تغییرات ذخیره نشده. ببندم؟')) return;
	const wasOpen = devMdEdit.open;
	devMdReset();
	if (wasOpen) await invalidateAll();
}

export async function devMdSave() {
	if (!devMdEdit.open || devMdEdit.saving) return;
	const el = devMdEdit.bodyEl;
	if (!el) {
		devMdEdit.errorMsg = 'ناحیهٔ ویرایش پیدا نشد';
		return;
	}
	devMdEdit.saving = true;
	devMdEdit.errorMsg = '';
	devMdEdit.statusMsg = '';
	try {
		const md = articleHtmlToMarkdown(el);
		const res = await fetch('/api/dev-md', {
			method: 'PUT',
			headers: { 'content-type': 'application/json' },
			body: JSON.stringify({
				pathname: devMdEdit.pathname,
				content: md
			})
		});
		const data = await res.json().catch(() => ({}));
		if (!res.ok) {
			throw new Error(
				(data as { message?: string }).message || res.statusText || 'ذخیره ناموفق'
			);
		}
		devMdEdit.siteRel = String((data as { site?: string }).site ?? devMdEdit.siteRel);
		const docs = (data as { docs?: string | null }).docs;
		devMdEdit.docsRel = docs ? String(docs) : devMdEdit.docsRel;
		const path = devMdEdit.pathname;
		// Exit edit briefly so the page re-renders from MD, then re-enter with a fresh snapshot
		devMdEdit.open = false;
		devMdEdit.bodyEl = null;
		devMdEdit.seedHtml = null;
		await invalidateAll();
		// wait for view DOM
		await new Promise<void>((r) => requestAnimationFrame(() => requestAnimationFrame(() => r())));
		const view = document.querySelector<HTMLElement>(`[data-dev-md-view="1"]`);
		devMdEdit.seedHtml = view ? view.innerHTML : '';
		devMdEdit.pathname = path;
		devMdEdit.open = true;
		devMdEdit.statusMsg = 'ذخیره شد';
		devMdEdit.dirty = false;
	} catch (e) {
		devMdEdit.errorMsg = e instanceof Error ? e.message : 'خطای ناشناخته';
	} finally {
		devMdEdit.saving = false;
	}
}
