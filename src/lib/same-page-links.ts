/**
 * Mark same-page section links (#hash or path+hash to current route)
 * so the UI can show “this page / section” affordance.
 */

function normPath(p: string): string {
	return (p.replace(/\/$/, '') || '/').toLowerCase();
}

/** True if href targets a section on the current document. */
export function isSamePageSectionHref(
	href: string,
	pathname: string,
	search = ''
): boolean {
	const raw = href.trim();
	if (!raw || raw === '#' || raw === '#top') return false;

	// Pure in-page hash
	if (raw.startsWith('#')) {
		return raw.length > 1;
	}

	// mailto / external schemes
	if (/^(mailto:|tel:|javascript:|data:)/i.test(raw)) return false;

	try {
		const base =
			typeof location !== 'undefined'
				? location.origin + pathname + search
				: 'http://local' + pathname + search;
		const u = new URL(raw, base);
		if (!u.hash || u.hash === '#' || u.hash === '#top') return false;

		if (typeof location !== 'undefined' && u.origin !== location.origin) {
			return false;
		}

		return normPath(u.pathname) === normPath(pathname) && u.search === (search || '');
	} catch {
		return false;
	}
}

/**
 * Stamp class + icon on same-page section anchors.
 * Idempotent.
 */
export function enhanceSamePageLinks(
	root: ParentNode = document,
	pathname?: string,
	search?: string
): number {
	if (typeof document === 'undefined') return 0;
	const path =
		pathname ??
		(typeof location !== 'undefined' ? location.pathname : '/');
	const q = search ?? (typeof location !== 'undefined' ? location.search : '');

	let n = 0;
	// Only mark links inside article / lesson body (not TOC / chrome)
	const scope =
		root.querySelectorAll?.(
			'.prose a[href], .nd-article a[href], .doc-page a[href], .ton-doc-body a[href], main.content article a[href]'
		) ?? root.querySelectorAll('a[href]');

	for (const a of scope) {
		if (!(a instanceof HTMLAnchorElement)) continue;
		// Skip anchors that are only heading ids (empty text + no real nav intent)
		if (a.closest('.nd-nav, .nd-pager, .top, .cmdk, .iap, header, footer')) continue;

		const href = a.getAttribute('href') || '';
		if (!isSamePageSectionHref(href, path, q)) {
			// clean previous marks if navigation changed
			if (a.classList.contains('inpage-link')) {
				a.classList.remove('inpage-link');
				a.querySelector(':scope > .inpage-link-icon')?.remove();
				a.removeAttribute('data-inpage');
				if (a.getAttribute('title') === 'بخشی در همین صفحه') a.removeAttribute('title');
			}
			continue;
		}

		if (a.classList.contains('inpage-link')) continue;

		a.classList.add('inpage-link');
		a.dataset.inpage = '1';
		if (!a.getAttribute('title')) {
			a.setAttribute('title', 'بخشی در همین صفحه');
		}
		// drop any leftover icon from older builds
		a.querySelector(':scope > .inpage-link-icon')?.remove();
		n += 1;
	}
	return n;
}
