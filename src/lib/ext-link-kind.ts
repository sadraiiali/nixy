/** Detect external host icon kind from an href. */

export type ExtLinkKind = 'gh' | 'yt' | 'dc' | 'x' | 'wp' | 'al' | 'ext';

/** Absolute http(s) / protocol-relative URL (opens outside the app). */
function isAbsoluteHttp(href: string): boolean {
	return /^(?:https?:)?\/\//i.test(href.trim());
}

export function extLinkKind(href: string): ExtLinkKind | null {
	const h = href.trim();
	if (!h) return null;
	// X / Twitter (x.com, twitter.com, mobile.twitter.com)
	if (/(?:^|\/\/)(?:www\.)?(?:x\.com|twitter\.com)\b/i.test(h)) return 'x';
	// Discourse (NixOS forum + common Discourse hosts)
	if (
		/discourse\.nixos\.org/i.test(h) ||
		/(?:^|\/\/)(?:[\w-]+\.)?discourse\.(?:group|org|com)\b/i.test(h)
	) {
		return 'dc';
	}
	// Arch Linux wiki / site
	if (/archlinux\.org/i.test(h)) return 'al';
	// Wikipedia (any language subdomain + wikimedia)
	if (/wikipedia\.org|wikimedia\.org|wikidata\.org/i.test(h)) return 'wp';
	// YouTube
	if (/youtube\.com|youtu\.be/i.test(h)) return 'yt';
	// GitHub
	if (/github\.com|githubusercontent\.com/i.test(h)) return 'gh';
	// Generic website (open in new page) — absolute http(s) only
	if (isAbsoluteHttp(h)) return 'ext';
	return null;
}

/** CSS selector for absolute external links (host-specific + generic http) */
export const EXT_LINK_SELECTOR = [
	'a[href^="http://"]',
	'a[href^="https://"]',
	'a[href^="//"]'
].join(', ');
