/**
 * Convert mdsvex-rendered article HTML → Markdown safe for site `+page.md`.
 *
 * mdsvex compiles MD to Svelte, so raw `{#id}` / `{...}` break the compiler.
 * We emit HTML anchors (like publish) and escape leftover braces.
 */
import TurndownService from 'turndown';

function escapeHtmlText(s: string): string {
	return s
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;');
}

/** Rebuild hub-card markup from live DOM (Turndown would flatten to MD links). */
function serializeNdHubCard(a: HTMLElement): string {
	const href = a.getAttribute('href') || '';
	const titleEl = a.querySelector('.nd-hub-card__title');
	const descEl = a.querySelector('.nd-hub-card__desc');
	const title = (titleEl?.textContent ?? '').replace(/\s+/g, ' ').trim();
	const desc = (descEl?.textContent ?? '').replace(/\s+/g, ' ').trim();
	// Fallback if spans were unwrapped in contenteditable
	const fallback = !title && !desc ? (a.textContent || '').replace(/\s+/g, ' ').trim() : '';
	const t = title || fallback;
	const d = desc;
	const lines = [
		`  <a class="nd-hub-card" href="${escapeHtmlText(href)}" data-no-panel="1">`,
		`    <span class="nd-hub-card__title">${escapeHtmlText(t)}</span>`
	];
	if (d) {
		lines.push(`    <span class="nd-hub-card__desc">${escapeHtmlText(d)}</span>`);
	}
	lines.push(`  </a>`);
	return lines.join('\n');
}

function serializeNdHubCards(el: HTMLElement): string {
	const cards = Array.from(el.querySelectorAll(':scope > a.nd-hub-card, :scope a.nd-hub-card'));
	// de-dupe if nested matches
	const seen = new Set<Element>();
	const unique: HTMLElement[] = [];
	for (const c of cards) {
		if (seen.has(c)) continue;
		seen.add(c);
		unique.push(c as HTMLElement);
	}
	if (unique.length === 0) return '';
	const body = unique.map(serializeNdHubCard).join('\n');
	return `\n\n<div class="nd-hub-cards" data-no-panel>\n${body}\n</div>\n\n`;
}

function makeTurndown(): TurndownService {
	const td = new TurndownService({
		headingStyle: 'atx',
		codeBlockStyle: 'fenced',
		bulletListMarker: '-',
		emDelimiter: '*',
		strongDelimiter: '**',
		hr: '---',
		fence: '```'
	});

	/**
	 * Preserve nix.dev hub cards as HTML. Default Turndown turns them into
	 * flat markdown links and the card UI disappears after save.
	 */
	td.addRule('ndHubCards', {
		filter: (node) =>
			node.nodeName === 'DIV' &&
			(node as HTMLElement).classList.contains('nd-hub-cards'),
		replacement: (_content, node) => serializeNdHubCards(node as HTMLElement)
	});

	/** Orphan hub card (wrapper lost in edit) — still emit structured HTML. */
	td.addRule('ndHubCard', {
		filter: (node) => {
			if (node.nodeName !== 'A') return false;
			const el = node as HTMLElement;
			if (!el.classList.contains('nd-hub-card')) return false;
			// Parent rule already handles cards inside the grid
			return !el.closest('.nd-hub-cards');
		},
		replacement: (_content, node) =>
			`\n\n<div class="nd-hub-cards" data-no-panel>\n${serializeNdHubCard(node as HTMLElement)}\n</div>\n\n`
	});

	// Empty id anchors stay as HTML (Svelte-safe)
	// Fragment targets: use <span id> (not empty <a id>) so Svelte a11y is clean
	td.addRule('anchorId', {
		filter: (node) => {
			const el = node as HTMLElement;
			const isEmptyTarget =
				(el.nodeName === 'A' || el.nodeName === 'SPAN') &&
				!!el.getAttribute('id') &&
				!el.getAttribute('href') &&
				!(el.textContent || '').trim();
			return isEmptyTarget;
		},
		replacement: (_content, node) => {
			const id = (node as HTMLElement).getAttribute('id') || '';
			return id ? `<span id="${id}"></span>` : '';
		}
	});

	// Headings: `# <span id="…"></span> Title`  (never `{#id}` — Svelte block syntax)
	td.addRule('headingWithId', {
		filter: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
		replacement: (content, node) => {
			const level = Number((node as HTMLElement).nodeName.charAt(1));
			const el = node as HTMLElement;
			const idEl =
				el.querySelector(':scope > a[id]:not([href])') ||
				el.querySelector(':scope > span[id]');
			const id = idEl?.getAttribute('id') || el.getAttribute('id') || '';
			let text = content
				// turndown may leave our anchor HTML or []{#id} noise
				.replace(/<(?:a|span)\s+id="[^"]*"\s*><\/(?:a|span)>\s*/gi, '')
				.replace(/^\s*\[\]\{#[^}]+\}\s*/g, '')
				.replace(/\s*\{#[^}]+\}/g, '')
				.replace(/\n+/g, ' ')
				.trim();
			const hashes = '#'.repeat(level);
			const anchor = id ? `<span id="${id}"></span> ` : '';
			return `\n\n${hashes} ${anchor}${text}\n\n`;
		}
	});

	td.addRule('fencedCode', {
		filter: (node) =>
			node.nodeName === 'PRE' &&
			node.firstChild != null &&
			(node.firstChild as HTMLElement).nodeName === 'CODE',
		replacement: (_content, node) => {
			const pre = node as HTMLElement;
			const code = pre.querySelector('code');
			const raw = code?.textContent ?? pre.textContent ?? '';
			const lang =
				(code?.getAttribute('class') || pre.getAttribute('class') || '')
					.split(/\s+/)
					.find((c) => c.startsWith('language-'))
					?.replace(/^language-/, '') || '';
			const body = raw.replace(/\n$/, '');
			return `\n\n\`\`\`${lang}\n${body}\n\`\`\`\n\n`;
		}
	});

	td.addRule('dropExtIcons', {
		filter: (node) =>
			node.nodeName === 'SPAN' &&
			(node as HTMLElement).classList.contains('ext-link-icon'),
		replacement: () => ''
	});

	td.addRule('kbd', {
		filter: ['kbd'],
		replacement: (content) => `\`${content}\``
	});

	// Highlight stays as HTML <mark> (safe for mdsvex; no special MD syntax)
	td.addRule('markHighlight', {
		filter: ['mark'],
		replacement: (content) => {
			const inner = content.trim();
			return inner ? `<mark>${inner}</mark>` : '';
		}
	});

	/**
	 * A block that is only --- / *** / ___ (or spaced - - -) is a thematic break.
	 * Default Turndown escapes these as `\---` which renders as literal text, not a line.
	 */
	td.addRule('thematicBreakFromDashes', {
		filter: (node) => {
			if (!['P', 'DIV'].includes(node.nodeName)) return false;
			const el = node as HTMLElement;
			// Skip if it has meaningful children (links, images, etc.)
			if (el.querySelector('a, img, pre, code, table, ul, ol, h1, h2, h3, h4, h5, h6, hr')) {
				return false;
			}
			const t = (el.textContent || '').replace(/\u200c/g, '').trim();
			// --- or *** or ___ (3+ same), optional spaces between: - - -
			return /^(?:-{3,}|\*{3,}|_{3,}|(?:-\s*){3,})$/.test(t);
		},
		replacement: () => '\n\n---\n\n'
	});

	// Explicit hr → always emit markdown thematic break (never escaped)
	td.addRule('horizontalRule', {
		filter: ['hr'],
		replacement: () => '\n\n---\n\n'
	});

	/**
	 * Paragraph typed as markdown ATX heading (`# Title`) must become a real heading.
	 * Default Turndown escapes as `\# Title` → literal hash, not <h1>.
	 */
	td.addRule('atxHeadingFromParagraph', {
		filter: (node) => {
			if (!['P', 'DIV'].includes(node.nodeName)) return false;
			const el = node as HTMLElement;
			if (el.querySelector('a, img, pre, code, table, ul, ol, h1, h2, h3, h4, h5, h6, hr')) {
				return false;
			}
			const t = (el.textContent || '').replace(/\u200c/g, '').trim();
			return /^#{1,6}\s+\S/.test(t);
		},
		replacement: (_content, node) => {
			const t = ((node as HTMLElement).textContent || '').replace(/\u200c/g, '').trim();
			const m = t.match(/^(#{1,6})\s+(.+)$/);
			if (!m) return t;
			const hashes = m[1];
			const title = m[2].replace(/\s+#+\s*$/, '').trim(); // strip trailing ### close style
			return `\n\n${hashes} ${title}\n\n`;
		}
	});

	/**
	 * Paragraph typed as markdown bullet (`- item` / `* item`) → real list.
	 * Default Turndown escapes as `\- item` (literal dash, not a list).
	 */
	td.addRule('bulletFromParagraph', {
		filter: (node) => {
			if (!['P', 'DIV'].includes(node.nodeName)) return false;
			const el = node as HTMLElement;
			if (el.querySelector('a, img, pre, code, table, ul, ol, h1, h2, h3, h4, h5, h6, hr')) {
				return false;
			}
			const t = (el.textContent || '').replace(/\u200c/g, '').trim();
			// Single marker only — not --- thematic breaks
			return /^[-*+]\s+\S/.test(t) && !/^[-*_]{3,}/.test(t);
		},
		replacement: (_content, node) => {
			const t = ((node as HTMLElement).textContent || '').replace(/\u200c/g, '').trim();
			const m = t.match(/^[-*+]\s+(.+)$/);
			if (!m) return t;
			return `\n\n- ${m[1].trim()}\n\n`;
		}
	});

	return td;
}

const turndown = makeTurndown();

function prepareArticleHtml(root: HTMLElement): string {
	const clone = root.cloneNode(true) as HTMLElement;
	clone
		.querySelectorAll(
			'.nd-pager, .nd-page-src-block, .nd-page-src, .nd-page-src__gh, .nd-page-contrib-row, .nd-page-contrib, .lesson__src, .dev-md-toolbar, .dev-md-fab, .dev-md-hint, .link-pop'
		)
		.forEach((n) => n.remove());
	// Editor-only chrome on structural blocks
	clone.querySelectorAll('[data-dev-md-protect], [contenteditable]').forEach((el) => {
		el.removeAttribute('data-dev-md-protect');
		el.removeAttribute('contenteditable');
	});
	// Edit-only dir attributes from the WYSIWYG (not meaningful in Markdown source)
	clone
		.querySelectorAll(
			'[dir="auto"], [dir="rtl"], ul[dir], ol[dir], li[dir], p[dir], blockquote[dir], h1[dir], h2[dir], h3[dir], h4[dir], h5[dir], h6[dir]'
		)
		.forEach((el) => {
			// keep dir on code/kbd/pre (bidi for chips / fences)
			if (el.closest('code, kbd, pre') || ['CODE', 'KBD', 'PRE'].includes(el.tagName)) {
				return;
			}
			// keep hub cards free of dir noise
			if (el.closest('.nd-hub-cards')) {
				el.removeAttribute('dir');
				return;
			}
			el.removeAttribute('dir');
		});
	clone.querySelectorAll('code, kbd, pre').forEach((el) => {
		const h = el as HTMLElement;
		// Strip editor inline styles; CSS handles dir in view mode
		h.style.removeProperty('direction');
		h.style.removeProperty('unicode-bidi');
		h.style.removeProperty('text-align');
		if (!h.getAttribute('style')?.trim()) h.removeAttribute('style');
		const inPre = h.tagName === 'PRE' || !!h.closest('pre');
		if (inPre) {
			h.setAttribute('dir', 'ltr');
		} else if (h.tagName === 'CODE' || h.tagName === 'KBD') {
			h.setAttribute('dir', 'rtl');
		}
	});
	return clone.innerHTML;
}

/** Escape `{` `}` so mdsvex→Svelte does not treat them as blocks/expressions. */
export function svelteEscapeMdBraces(md: string): string {
	const parts = md.split(/(```[\s\S]*?```)/);
	return parts
		.map((chunk, i) => {
			if (i % 2 === 1) return chunk; // fenced code unchanged
			// Two-phase replace so the braces inside `{'{'}` are not re-escaped
			return chunk
				.replace(/\{/g, '\0OB\0')
				.replace(/\}/g, '\0CB\0')
				.replace(/\0OB\0/g, "{'{'}")
				.replace(/\0CB\0/g, "{'}'}");
		})
		.join('');
}

/**
 * Convert MyST/mdBook heading ids to HTML fragment targets before brace-escape.
 * Uses <span id> (not empty <a id>) so Svelte a11y does not warn.
 *   # Title {#id}  →  # <span id="id"></span> Title
 *   []{#id}        →  <span id="id"></span>
 */
export function normalizeMdIdsForSite(md: string): string {
	let out = md;
	// []{#id}
	out = out.replace(/\[\]\{#([A-Za-z][\w:.-]*)\}/g, '<span id="$1"></span>');
	// Heading lines: # Title {#id}  or  # Title {#id} trailing space
	out = out.replace(
		/^(#{1,6})\s+(.+?)\s*\{#([A-Za-z][\w:.-]*)\}\s*$/gm,
		(_, hashes: string, title: string, id: string) =>
			`${hashes} <span id="${id}"></span> ${title.trim()}`
	);
	// leftover bare {#id} mid-line
	out = out.replace(/\{#([A-Za-z][\w:.-]*)\}/g, '<span id="$1"></span>');
	// Migrate legacy empty <a id> fragment targets
	out = out.replace(/<a\s+id="([^"]+)"\s*><\/a>/gi, '<span id="$1"></span>');
	return out;
}

/**
 * Unescape sole-line `\---` / `\*\*\*` / `\_\_\_` so they render as <hr>, not literal dashes.
 * Turndown (and some editors) escape thematic-break markers by default.
 */
export function normalizeThematicBreaks(md: string): string {
	return md.replace(/^[ \t]*\\([-*_])\1{2,}[ \t]*$/gm, '---');
}

/**
 * Unescape ATX heading markers at line start: `\# Title` → `# Title`.
 * (Outside fenced code; caller should run per non-fence chunk or on full md after turndown.)
 */
export function normalizeEscapedAtxHeadings(md: string): string {
	const parts = md.split(/(```[\s\S]*?```)/);
	return parts
		.map((chunk, i) => {
			if (i % 2 === 1) return chunk;
			// \# Title, \## Sub, … (1–6 hashes, optional spaces after backslash)
			return chunk.replace(/^[ \t]*\\(#{1,6})([ \t]+|\s*$)/gm, '$1$2');
		})
		.join('');
}

/** Unescape list markers: `\- item` / `\* item` → `- item` */
export function normalizeEscapedListMarkers(md: string): string {
	const parts = md.split(/(```[\s\S]*?```)/);
	return parts
		.map((chunk, i) => {
			if (i % 2 === 1) return chunk;
			// \- item or \* item or \+ item at line start (not \---)
			return chunk.replace(/^[ \t]*\\([-*+])([ \t]+)/gm, '$1$2');
		})
		.join('');
}

/** Full pipeline: HTML root → site-safe Markdown */
export function articleHtmlToMarkdown(root: HTMLElement): string {
	const html = prepareArticleHtml(root);
	let md = turndown.turndown(html);
	md = md.replace(/\n{3,}/g, '\n\n').trim() + '\n';
	md = normalizeThematicBreaks(md);
	md = normalizeEscapedAtxHeadings(md);
	md = normalizeEscapedListMarkers(md);
	md = normalizeMdIdsForSite(md);
	md = svelteEscapeMdBraces(md);
	return md;
}

/** Sanitize any MD string before writing to +page.md (ids + braces). */
export function sanitizeMdForSitePage(md: string): string {
	let out = md.replace(/\r\n/g, '\n');
	out = normalizeThematicBreaks(out);
	out = normalizeEscapedAtxHeadings(out);
	out = normalizeEscapedListMarkers(out);
	out = normalizeMdIdsForSite(out);
	out = svelteEscapeMdBraces(out);
	if (!out.endsWith('\n')) out += '\n';
	return out;
}
