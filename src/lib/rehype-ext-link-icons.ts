/**
 * Rehype: prepend host icon markers for external links
 * (GitHub / YouTube / … / generic open-in-new).
 * Rendering only — does not change markdown source.
 *
 * Local hast-shaped types (avoids a hard dependency on `@types/hast`).
 * Relative import: this module is loaded from vite.config.ts (mdsvex rehype),
 * where SvelteKit's `$lib` alias is not available yet.
 */
import { extLinkKind } from './ext-link-kind';

type HastElement = {
	type: 'element';
	tagName: string;
	properties?: Record<string, unknown>;
	children?: unknown[];
};

type HastNode = {
	type?: string;
	tagName?: string;
	properties?: Record<string, unknown>;
	children?: unknown[];
};

function ensureExternalRel(props: Record<string, unknown>) {
	const raw = props.rel;
	const existing =
		typeof raw === 'string'
			? raw.split(/\s+/).filter(Boolean)
			: Array.isArray(raw)
				? raw.map(String)
				: [];
	const parts = new Set(existing);
	parts.add('noopener');
	parts.add('noreferrer');
	props.rel = [...parts].join(' ');
}

function walk(node: HastNode) {
	if (!node || typeof node !== 'object') return;

	if (node.type === 'element' && node.tagName === 'a') {
		const href = node.properties?.href;
		if (typeof href === 'string') {
			const kind = extLinkKind(href);
			if (kind) {
				// Absolute external hosts → open in a new tab (static HTML + no-JS)
				const props = (node.properties ??= {});
				if (props.target == null && props.download == null) {
					props.target = '_blank';
					ensureExternalRel(props);
				}

				const children = (node.children ?? []) as unknown[];
				const already = children.some(
					(c) =>
						c &&
						typeof c === 'object' &&
						(c as HastElement).type === 'element' &&
						(c as HastElement).tagName === 'span' &&
						Array.isArray((c as HastElement).properties?.className) &&
						((c as HastElement).properties!.className as string[]).includes('ext-link-icon')
				);
				if (!already) {
					const icon: HastElement = {
						type: 'element',
						tagName: 'span',
						properties: {
							className: ['ext-link-icon', `ext-link-icon--${kind}`],
							'aria-hidden': 'true'
						},
						children: []
					};
					node.children = [icon, ...children];
				}
			}
		}
	}

	if (Array.isArray(node.children)) {
		for (const c of node.children) {
			walk(c as HastNode);
		}
	}
}

export function rehypeExtLinkIcons() {
	return (tree: HastNode) => {
		walk(tree);
	};
}
