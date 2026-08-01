/** True when building/packaging the offline Webxdc app. */
export const isWebxdc =
	import.meta.env.VITE_WEBXDC === '1' || import.meta.env.VITE_WEBXDC === 'true';

/**
 * Glossary editing (save / approve / bulk actions) only on the Vite dev server.
 * Webxdc and production builds are read-only tables.
 */
export const canEditGlossary = import.meta.env.DEV && !isWebxdc;

export function isExternalHref(href: string | null | undefined): boolean {
	if (!href) return false;
	const h = href.trim();
	if (!h || h.startsWith('#') || h.startsWith('mailto:') || h.startsWith('tel:')) return false;
	// protocol-relative or absolute http(s)
	if (/^https?:\/\//i.test(h)) return true;
	if (h.startsWith('//')) return true;
	// scheme other than relative path
	if (/^[a-z][a-z0-9+.-]*:/i.test(h) && !h.startsWith('/')) return true;
	return false;
}
