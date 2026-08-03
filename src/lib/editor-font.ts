/** Monospace / code-editor font preference (system stacks; no CDN). */

export const EDITOR_FONT_STORAGE_KEY = 'nix-notes-editor-font';
export const EDITOR_FONT_SIZE_STORAGE_KEY = 'nix-notes-editor-font-size';
export const EDITOR_FONT_EVENT = 'nix-editor-font';

export type EditorFontId =
	| 'system'
	| 'jetbrains'
	| 'fira'
	| 'cascadia'
	| 'ibm'
	| 'source';

export const EDITOR_FONT_DEFAULT: EditorFontId = 'system';
export const EDITOR_FONT_SIZE_DEFAULT = 14;
export const EDITOR_FONT_SIZE_MIN = 11;
/** Allow large code for accessibility / projectors */
export const EDITOR_FONT_SIZE_MAX = 36;

export const EDITOR_FONTS: {
	id: EditorFontId;
	label: string;
	labelEn: string;
	stack: string;
	hint: string;
}[] = [
	{
		id: 'system',
		label: 'سیستم',
		labelEn: 'System Mono',
		stack: "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace",
		hint: 'فونت mono پیش‌فرض سیستم‌عامل'
	},
	{
		id: 'jetbrains',
		label: 'جت‌برینز',
		labelEn: 'JetBrains Mono',
		stack: "'JetBrains Mono', 'JetBrainsMono Nerd Font', ui-monospace, Menlo, Consolas, monospace",
		hint: 'اگر روی سیستم نصب باشد'
	},
	{
		id: 'fira',
		label: 'فیرا',
		labelEn: 'Fira Code',
		stack: "'Fira Code', 'Fira Mono', ui-monospace, Menlo, Consolas, monospace",
		hint: 'لیگاتورهای کد؛ در صورت نصب محلی'
	},
	{
		id: 'cascadia',
		label: 'کاسکدیا',
		labelEn: 'Cascadia Code',
		stack: "'Cascadia Code', 'Cascadia Mono', Consolas, ui-monospace, monospace",
		hint: 'معمول روی ویندوز / ترمینال'
	},
	{
		id: 'ibm',
		label: 'آی‌بی‌ام',
		labelEn: 'IBM Plex Mono',
		stack: "'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace",
		hint: 'خوانا برای مستندات و ترمینال'
	},
	{
		id: 'source',
		label: 'سورس',
		labelEn: 'Source Code Pro',
		stack: "'Source Code Pro', ui-monospace, Menlo, Consolas, monospace",
		hint: 'Adobe Source Code Pro'
	}
];

export function isEditorFontId(v: unknown): v is EditorFontId {
	return (
		v === 'system' ||
		v === 'jetbrains' ||
		v === 'fira' ||
		v === 'cascadia' ||
		v === 'ibm' ||
		v === 'source'
	);
}

export function clampEditorFontSize(px: number): number {
	return Math.min(
		EDITOR_FONT_SIZE_MAX,
		Math.max(EDITOR_FONT_SIZE_MIN, Math.round(px))
	);
}

export function readEditorFont(): EditorFontId {
	if (typeof localStorage === 'undefined') return EDITOR_FONT_DEFAULT;
	try {
		const raw = localStorage.getItem(EDITOR_FONT_STORAGE_KEY);
		if (isEditorFontId(raw)) return raw;
		return EDITOR_FONT_DEFAULT;
	} catch {
		return EDITOR_FONT_DEFAULT;
	}
}

export function readEditorFontSize(): number {
	if (typeof localStorage === 'undefined') return EDITOR_FONT_SIZE_DEFAULT;
	try {
		const raw = localStorage.getItem(EDITOR_FONT_SIZE_STORAGE_KEY);
		if (!raw) return EDITOR_FONT_SIZE_DEFAULT;
		const n = Number(raw);
		return Number.isNaN(n) ? EDITOR_FONT_SIZE_DEFAULT : clampEditorFontSize(n);
	} catch {
		return EDITOR_FONT_SIZE_DEFAULT;
	}
}

/** Live size from CSS var (settings / Ctrl+scroll), falling back to storage. */
export function readCssEditorFontSizeFromDom(): number {
	if (typeof document === 'undefined') return readEditorFontSize();
	const raw = getComputedStyle(document.documentElement)
		.getPropertyValue('--editor-font-size')
		.trim();
	const n = parseFloat(raw);
	if (Number.isFinite(n) && n > 0) return clampEditorFontSize(n);
	return readEditorFontSize();
}

function notifyEditorFont() {
	if (typeof window === 'undefined') return;
	window.dispatchEvent(new CustomEvent(EDITOR_FONT_EVENT));
}

/**
 * Apply mono font stack via CSS vars + data attribute.
 * Used by prose code, pre blocks, and Monaco.
 */
export function applyEditorFont(id: EditorFontId): EditorFontId {
	const next = isEditorFontId(id) ? id : EDITOR_FONT_DEFAULT;
	const meta = EDITOR_FONTS.find((f) => f.id === next) ?? EDITOR_FONTS[0]!;

	if (typeof document !== 'undefined') {
		const html = document.documentElement;
		html.dataset.editorFont = next;
		html.style.setProperty('--font-mono', meta.stack);
	}

	if (typeof localStorage !== 'undefined') {
		try {
			localStorage.setItem(EDITOR_FONT_STORAGE_KEY, next);
		} catch {
			/* private mode */
		}
	}

	notifyEditorFont();
	return next;
}

export function applyEditorFontSize(px: number): number {
	const next = clampEditorFontSize(px);

	if (typeof document !== 'undefined') {
		const html = document.documentElement;
		html.style.setProperty('--editor-font-size', `${next}px`);
		html.dataset.editorFontSize = String(next);
	}

	if (typeof localStorage !== 'undefined') {
		try {
			localStorage.setItem(EDITOR_FONT_SIZE_STORAGE_KEY, String(next));
		} catch {
			/* private mode */
		}
	}

	notifyEditorFont();
	return next;
}

/** Resolved stack currently applied (or default). */
export function resolveEditorFontStack(id?: EditorFontId): string {
	const key = id && isEditorFontId(id) ? id : readEditorFont();
	return EDITOR_FONTS.find((f) => f.id === key)?.stack ?? EDITOR_FONTS[0]!.stack;
}
