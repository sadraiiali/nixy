/**
 * Normalize MyST/Sphinx-style doc links for SvelteKit routes.
 * e.g. content-address.md → content-address
 *      foo/index.md → foo
 *      ./bar.md#hash → ./bar#hash
 */

/** Strip trailing /index and .md from a pathname (no query/hash). */
export function normalizeDocPathname(pathname: string): string {
	let p = pathname || '/';
	// decode once if needed (leave as-is on failure)
	try {
		p = decodeURIComponent(p);
	} catch {
		/* keep */
	}
	// .../file.md → .../file
	if (p.toLowerCase().endsWith('.md')) {
		p = p.slice(0, -3);
	}
	// .../index → ...
	if (p === '/index' || p.endsWith('/index')) {
		p = p.replace(/\/index$/, '') || '/';
	}
	// collapse empty
	if (p === '') p = '/';
	return p;
}

/**
 * Normalize a full href (relative or absolute path + optional ? and #).
 * Leaves external URLs, mailto, tel, and pure #hash alone.
 */
export function normalizeDocHref(href: string, baseHref?: string): string {
	const raw = href.trim();
	if (!raw) return raw;
	if (
		raw.startsWith('#') ||
		raw.startsWith('mailto:') ||
		raw.startsWith('tel:') ||
		raw.startsWith('javascript:') ||
		raw.startsWith('data:')
	) {
		return raw;
	}

	// Absolute external
	if (/^[a-z][a-z0-9+.-]*:/i.test(raw) && !raw.startsWith('/')) {
		try {
			const u = new URL(raw);
			if (typeof location !== 'undefined' && u.origin !== location.origin) {
				return raw;
			}
			// same-origin absolute URL
			const path = normalizeDocPathname(u.pathname);
			return path + u.search + u.hash;
		} catch {
			return raw;
		}
	}

	// Relative or root-relative: resolve against base when available
	try {
		const base =
			baseHref ||
			(typeof location !== 'undefined' ? location.href : 'http://local/');
		const u = new URL(raw, base);
		// if external after resolve
		if (typeof location !== 'undefined' && u.origin !== location.origin) {
			return raw;
		}
		const path = normalizeDocPathname(u.pathname);
		// Prefer path-only form for same-origin so SK router is happy
		if (raw.startsWith('/') || raw.startsWith('.') || !raw.includes('://')) {
			// Keep relative if input was relative without leading /
			if (!raw.startsWith('/') && !/^[a-z][a-z0-9+.-]*:/i.test(raw)) {
				// Rebuild relative-ish: use absolute path (SvelteKit is fine with /pages/...)
				return path + u.search + u.hash;
			}
			return path + u.search + u.hash;
		}
		return path + u.search + u.hash;
	} catch {
		// Fallback: naive strip on string
		return raw
			.replace(/\.md(?=[#?]|$)/i, '')
			.replace(/\/index(?=[#?]|$)/i, '');
	}
}
