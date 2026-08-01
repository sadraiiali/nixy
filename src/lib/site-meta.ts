/**
 * Site-wide branding + absolute URL helpers for favicons / Open Graph / Twitter.
 */

export const SITE_NAME = 'نیکسی';
export const SITE_NAME_EN = 'Niksy';
/**
 * Default page / Open Graph title (target 30–60 chars for social previews).
 * Keep SITE_NAME short for the brand mark; use this for <title> + og:title.
 */
export const SITE_TITLE = 'نیکسی — آموزش و راهنمای فارسی Nix و NixOS';
export const SITE_DESCRIPTION =
	'راهنماهای فارسی Nix و NixOS — nix.dev، راهنمای مرجع، Nixpkgs و تور نیکس';
export const SITE_THEME_COLOR = '#5277C3';
export const SITE_LOCALE = 'fa_IR';

/** Optional public origin for absolute OG URLs (e.g. https://nix-notes.pages.dev). */
export function siteOrigin(fallbackOrigin?: string): string {
	const fromEnv = (import.meta.env.PUBLIC_SITE_URL as string | undefined)?.replace(/\/$/, '');
	if (fromEnv) return fromEnv;
	if (fallbackOrigin && !fallbackOrigin.includes('sveltekit-prerender')) {
		return fallbackOrigin.replace(/\/$/, '');
	}
	return '';
}

/** Absolute URL for a path on this site. Falls back to root-relative if origin unknown. */
export function absoluteUrl(path: string, origin?: string): string {
	const base = siteOrigin(origin);
	const p = path.startsWith('/') ? path : `/${path}`;
	return base ? `${base}${p}` : p;
}

export const FAVICON = {
	svg: '/favicon.svg',
	ico: '/favicon.ico',
	png32: '/favicon-32.png',
	png16: '/favicon-16.png',
	apple: '/apple-touch-icon.png',
	icon192: '/icon-192.png',
	icon512: '/icon-512.png',
	manifest: '/site.webmanifest',
	ogImage: '/og-image.png'
} as const;
