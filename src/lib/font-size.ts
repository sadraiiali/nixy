/** Root font-size preference (px on <html>). All UI type uses rem → scales with settings. */

export const FONT_STORAGE_KEY = 'nix-notes-font-size';
/** Base size: 16px → 1rem. Zarinpal body ratios scale from this. */
export const FONT_DEFAULT = 16;
export const FONT_MIN = 14;
export const FONT_MAX = 22;

export function clampFontSize(px: number): number {
	return Math.min(FONT_MAX, Math.max(FONT_MIN, Math.round(px)));
}

export function readFontSize(): number {
	if (typeof localStorage === 'undefined') return FONT_DEFAULT;
	try {
		const raw = localStorage.getItem(FONT_STORAGE_KEY);
		if (!raw) return FONT_DEFAULT;
		const n = Number(raw);
		return Number.isNaN(n) ? FONT_DEFAULT : clampFontSize(n);
	} catch {
		return FONT_DEFAULT;
	}
}

/**
 * Sets <html> font-size so every rem in the app scales.
 * Also exposes --user-font-size for CSS.
 */
export function applyFontSize(px: number): number {
	const next = clampFontSize(px);
	if (typeof document !== 'undefined') {
		const html = document.documentElement;
		html.style.setProperty('--user-font-size', `${next}px`);
		html.style.fontSize = `${next}px`;
		html.dataset.fontSize = String(next);
	}
	if (typeof localStorage !== 'undefined') {
		try {
			localStorage.setItem(FONT_STORAGE_KEY, String(next));
		} catch {
			/* private mode */
		}
	}
	return next;
}

export function pxToRem(px: number, base = FONT_DEFAULT): string {
	return `${px / base}rem`;
}
