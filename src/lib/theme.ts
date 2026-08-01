/**
 * Color theme preference (light | dark | system).
 * Applied via data-theme on <html>; tokens live in app.css.
 */

export const THEME_STORAGE_KEY = 'nix-notes-theme';

export type ThemeId = 'light' | 'dark' | 'system';

export const THEME_DEFAULT: ThemeId = 'system';

export const THEMES: {
	id: ThemeId;
	label: string;
	labelEn: string;
	/** Short description (Farsi) */
	hint: string;
}[] = [
	{
		id: 'system',
		label: 'سیستم',
		labelEn: 'System',
		hint: 'هم‌سو با حالت روشن/تاریک دستگاه'
	},
	{
		id: 'light',
		label: 'روشن',
		labelEn: 'Light',
		hint: 'پس‌زمینه روشن، متن تیره'
	},
	{
		id: 'dark',
		label: 'تاریک',
		labelEn: 'Dark',
		hint: 'پس‌زمینه تیره، متن روشن'
	}
];

export function isThemeId(v: unknown): v is ThemeId {
	return v === 'light' || v === 'dark' || v === 'system';
}

export function readTheme(): ThemeId {
	if (typeof localStorage === 'undefined') return THEME_DEFAULT;
	try {
		const raw = localStorage.getItem(THEME_STORAGE_KEY);
		if (isThemeId(raw)) return raw;
		return THEME_DEFAULT;
	} catch {
		return THEME_DEFAULT;
	}
}

/** Resolved palette for the current preference (system → light|dark). */
export function resolveTheme(id: ThemeId = readTheme()): 'light' | 'dark' {
	if (id === 'light' || id === 'dark') return id;
	if (typeof window !== 'undefined' && typeof window.matchMedia === 'function') {
		return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
	}
	return 'light';
}

/**
 * Apply theme: data-theme on <html>, color-scheme, and --theme-resolved.
 * Styles for each palette are in app.css under html[data-theme=…] / system media.
 */
export function applyTheme(id: ThemeId): ThemeId {
	const next = isThemeId(id) ? id : THEME_DEFAULT;
	const resolved = resolveTheme(next);

	if (typeof document !== 'undefined') {
		const html = document.documentElement;
		html.dataset.theme = next;
		html.dataset.themeResolved = resolved;
		html.style.colorScheme = resolved;
		// Help native form controls / scrollbars
		html.style.setProperty('color-scheme', resolved);
	}

	if (typeof localStorage !== 'undefined') {
		try {
			localStorage.setItem(THEME_STORAGE_KEY, next);
		} catch {
			/* private mode */
		}
	}

	return next;
}

/** Listen for OS theme changes when preference is `system`. Returns cleanup. */
export function watchSystemTheme(onChange?: (resolved: 'light' | 'dark') => void): () => void {
	if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
		return () => {};
	}
	const mq = window.matchMedia('(prefers-color-scheme: dark)');
	const handler = () => {
		const pref = readTheme();
		if (pref !== 'system') return;
		applyTheme('system');
		onChange?.(resolveTheme('system'));
	};
	mq.addEventListener('change', handler);
	return () => mq.removeEventListener('change', handler);
}
