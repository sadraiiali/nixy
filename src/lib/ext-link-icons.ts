/**
 * Client-side: stamp host icons onto anchors (tour HTML, dynamic content)
 * and open cross-origin links in a new tab.
 * Idempotent — safe to run on every navigation.
 */
import { EXT_LINK_SELECTOR, extLinkKind } from '$lib/ext-link-kind';

function isSameOriginAbsolute(href: string): boolean {
	if (typeof location === 'undefined') return false;
	try {
		const u = new URL(href, location.href);
		return u.origin === location.origin;
	} catch {
		return false;
	}
}

/** Merge noopener/noreferrer into existing rel without duplicates. */
function ensureExternalRel(a: HTMLAnchorElement) {
	const parts = new Set((a.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
	parts.add('noopener');
	parts.add('noreferrer');
	a.setAttribute('rel', [...parts].join(' '));
}

/** Cross-origin http(s) links open in a new tab; same-origin stay in-app. */
function enhanceExternalTarget(a: HTMLAnchorElement, href: string) {
	if (isSameOriginAbsolute(href)) return;
	if (a.hasAttribute('download')) return;
	// Explicit same-tab override
	if (a.dataset.sameTab === '1' || a.getAttribute('target') === '_self') return;
	a.setAttribute('target', '_blank');
	ensureExternalRel(a);
}

export function enhanceExtLinkIcons(root: ParentNode = document): number {
	if (typeof document === 'undefined') return 0;
	let n = 0;
	const anchors = root.querySelectorAll<HTMLAnchorElement>(EXT_LINK_SELECTOR);
	for (const a of anchors) {
		const href = a.getAttribute('href') || '';
		if (!href) continue;

		// Outside this site → new window/tab
		enhanceExternalTarget(a, href);

		if (a.querySelector(':scope > .ext-link-icon')) continue;
		// Cards that already draw their own host icon
		if (a.classList.contains('home-about__source')) continue;
		const kind = extLinkKind(href);
		if (!kind) continue;
		// Same-site absolute URLs are not “open in new page” external sites
		if (kind === 'ext' && isSameOriginAbsolute(href)) continue;
		const span = document.createElement('span');
		span.className = `ext-link-icon ext-link-icon--${kind}`;
		span.setAttribute('aria-hidden', 'true');
		a.insertBefore(span, a.firstChild);
		n += 1;
	}
	return n;
}
