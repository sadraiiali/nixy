/** UI font-family preference (self-hosted only; no CDN). */

export const FONT_FAMILY_STORAGE_KEY = 'nix-notes-font-family';

export type FontFamilyId = 'peyda' | 'iranyekan' | 'shabnam';

/** Default site font */
export const FONT_FAMILY_DEFAULT: FontFamilyId = 'peyda';

export const FONT_FAMILIES: {
	id: FontFamilyId;
	label: string;
	labelEn: string;
	stack: string;
}[] = [
	{
		id: 'peyda',
		label: 'پیدا',
		labelEn: 'Peyda',
		// PeydaFaNumWeb (Fontiran Pro v4, full weights) — self-hosted
		stack: "'Peyda', Tahoma, system-ui, sans-serif"
	},
	{
		id: 'iranyekan',
		label: 'ایران‌یکان',
		labelEn: 'IRANYekanX',
		// IRANYekanXFaNum (Fontiran Eco) — self-hosted
		stack: "'IRANYekanX', Tahoma, system-ui, sans-serif"
	},
	{
		id: 'shabnam',
		label: 'شبنم',
		labelEn: 'Shabnam',
		stack: "'Shabnam', Tahoma, system-ui, sans-serif"
	}
];

export function isFontFamilyId(v: unknown): v is FontFamilyId {
	return v === 'peyda' || v === 'iranyekan' || v === 'shabnam';
}

export function readFontFamily(): FontFamilyId {
	if (typeof localStorage === 'undefined') return FONT_FAMILY_DEFAULT;
	try {
		const raw = localStorage.getItem(FONT_FAMILY_STORAGE_KEY);
		if (isFontFamilyId(raw)) return raw;
		return FONT_FAMILY_DEFAULT;
	} catch {
		return FONT_FAMILY_DEFAULT;
	}
}

/**
 * Apply font family via data-font on <html> and CSS variables.
 * Styles live in app.css under html[data-font='…'].
 */
export function applyFontFamily(id: FontFamilyId): FontFamilyId {
	const next = isFontFamilyId(id) ? id : FONT_FAMILY_DEFAULT;
	const meta = FONT_FAMILIES.find((f) => f.id === next) ?? FONT_FAMILIES[0]!;

	if (typeof document !== 'undefined') {
		const html = document.documentElement;
		html.dataset.font = next;
		html.style.setProperty('--font', meta.stack);
		html.style.setProperty('--font-ui', meta.stack);
	}

	if (typeof localStorage !== 'undefined') {
		try {
			localStorage.setItem(FONT_FAMILY_STORAGE_KEY, next);
		} catch {
			/* private mode */
		}
	}

	return next;
}
