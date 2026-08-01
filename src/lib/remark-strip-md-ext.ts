/**
 * Remark plugin: rewrite MyST-style links
 *   store/foo.md#bar  →  store/foo#bar
 *   ./index.md        →  .
 * so compiled mdsvex pages match SvelteKit routes.
 */
import type { Root, Link, Definition } from 'mdast';

function rewriteUrl(url: string): string {
	if (!url || url.startsWith('#') || url.startsWith('mailto:') || url.startsWith('tel:')) {
		return url;
	}
	// leave absolute external alone
	if (/^[a-z][a-z0-9+.-]*:/i.test(url)) return url;

	const hashIdx = url.indexOf('#');
	const qIdx = url.indexOf('?');
	let cut = url.length;
	if (hashIdx >= 0) cut = Math.min(cut, hashIdx);
	if (qIdx >= 0) cut = Math.min(cut, qIdx);
	const path = url.slice(0, cut);
	const rest = url.slice(cut);

	let next = path.replace(/\.md$/i, '');
	if (next === 'index' || next.endsWith('/index')) {
		next = next.replace(/\/?index$/i, '') || '.';
	}
	return next + rest;
}

function walk(node: { type?: string; url?: string; children?: unknown[] }) {
	if (!node || typeof node !== 'object') return;
	if ((node.type === 'link' || node.type === 'definition') && typeof node.url === 'string') {
		(node as Link | Definition).url = rewriteUrl(node.url);
	}
	if (Array.isArray(node.children)) {
		for (const c of node.children) walk(c as typeof node);
	}
}

export function remarkStripMdExt() {
	return (tree: Root) => {
		walk(tree as unknown as { type?: string; url?: string; children?: unknown[] });
	};
}
