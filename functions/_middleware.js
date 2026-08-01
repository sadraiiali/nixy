/**
 * Markdown for Agents — content negotiation on Cloudflare Pages.
 *
 * When the client prefers `Accept: text/markdown`, convert HTML page bodies to
 * Markdown (RFC content negotiation). Browsers keep receiving HTML by default.
 *
 * Complements Cloudflare’s zone-level “Markdown for Agents” feature; this runs
 * at the Pages origin so the site works even without that zone setting.
 *
 * @see https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
 * @see https://isitagentready.com/.well-known/agent-skills/markdown-negotiation/SKILL.md
 */

/**
 * @param {string | null} accept
 * @returns {boolean}
 */
function prefersMarkdown(accept) {
	if (!accept) return false;
	let mdQ = 0;
	let htmlQ = 0;
	let sawMarkdown = false;

	for (const part of accept.split(',')) {
		const bits = part.trim().split(';').map((s) => s.trim());
		const type = (bits[0] || '').toLowerCase();
		let q = 1;
		for (let i = 1; i < bits.length; i++) {
			const m = /^q\s*=\s*([0-9.]+)/i.exec(bits[i]);
			if (m) {
				q = Math.min(1, Math.max(0, parseFloat(m[1]) || 0));
			}
		}
		if (type === 'text/markdown') {
			sawMarkdown = true;
			mdQ = Math.max(mdQ, q);
		} else if (type === 'text/html') {
			htmlQ = Math.max(htmlQ, q);
		}
	}

	// Only when text/markdown is explicit and not outranked by text/html
	return sawMarkdown && mdQ > 0 && mdQ >= htmlQ;
}

/**
 * @param {string} html
 * @param {string} name
 * @returns {string}
 */
function metaContent(html, name) {
	const re = new RegExp(
		`<meta[^>]+(?:name|property)=["']${name}["'][^>]+content=["']([^"']*)["']` +
			`|` +
			`<meta[^>]+content=["']([^"']*)["'][^>]+(?:name|property)=["']${name}["']`,
		'i'
	);
	const m = re.exec(html);
	return (m?.[1] || m?.[2] || '').trim();
}

/**
 * @param {string} html
 * @returns {string}
 */
function documentTitle(html) {
	const t = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(html);
	return t ? decodeEntities(t[1].replace(/\s+/g, ' ').trim()) : '';
}

/**
 * @param {string} s
 * @returns {string}
 */
function decodeEntities(s) {
	return s
		.replace(/&nbsp;/gi, ' ')
		.replace(/&amp;/gi, '&')
		.replace(/&lt;/gi, '<')
		.replace(/&gt;/gi, '>')
		.replace(/&quot;/gi, '"')
		.replace(/&#39;/gi, "'")
		.replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
		.replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(parseInt(n, 10)));
}

/**
 * Strip chrome and non-content so agents get the article body.
 * @param {string} html
 * @returns {string}
 */
function extractMainHtml(html) {
	let s = html;
	// Drop non-content blocks
	const strip = [
		/<script\b[\s\S]*?<\/script>/gi,
		/<style\b[\s\S]*?<\/style>/gi,
		/<noscript\b[\s\S]*?<\/noscript>/gi,
		/<svg\b[\s\S]*?<\/svg>/gi,
		/<!--[\s\S]*?-->/g,
		/<header\b[\s\S]*?<\/header>/gi,
		/<footer\b[\s\S]*?<\/footer>/gi,
		/<nav\b[\s\S]*?<\/nav>/gi,
		/<aside\b[\s\S]*?<\/aside>/gi
	];
	for (const re of strip) s = s.replace(re, '\n');

	// Prefer main content regions used by this site
	const regions = [
		/<main\b[^>]*>([\s\S]*?)<\/main>/i,
		/<article\b[^>]*class=["'][^"']*nd-article[^"']*["'][^>]*>([\s\S]*?)<\/article>/i,
		/<article\b[^>]*>([\s\S]*?)<\/article>/i,
		/<div\b[^>]*class=["'][^"']*\bcontent\b[^"']*["'][^>]*>([\s\S]*?)<\/div>/i,
		/<section\b[^>]*class=["'][^"']*\bhome\b[^"']*["'][^>]*>([\s\S]*?)<\/section>/i,
		/<body\b[^>]*>([\s\S]*?)<\/body>/i
	];
	for (const re of regions) {
		const m = re.exec(s);
		if (m?.[1] && m[1].replace(/<[^>]+>/g, '').trim().length > 40) {
			return m[1];
		}
	}
	return s;
}

/**
 * Collect JSON-LD blocks from original HTML.
 * @param {string} html
 * @returns {string[]}
 */
function extractJsonLd(html) {
	const out = [];
	const re = /<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
	let m;
	while ((m = re.exec(html))) {
		const raw = m[1].trim();
		if (raw) out.push(raw);
	}
	return out;
}

/**
 * @param {string} text
 * @returns {string}
 */
function escapeMd(text) {
	return text.replace(/([\\`*_{}\[\]()#+\-.!|>])/g, '\\$1');
}

/**
 * Lightweight HTML → Markdown (good enough for agent consumption).
 * @param {string} html
 * @returns {string}
 */
function htmlToMarkdown(html) {
	let s = html;

	// Normalize voids / line breaks
	s = s.replace(/\r\n?/g, '\n');
	s = s.replace(/<br\s*\/?>/gi, '\n');
	s = s.replace(/<\/(p|div|section|li|tr|h[1-6]|blockquote|pre)>/gi, '</$1>\n');

	// Fenced code: preserve <pre><code>
	s = s.replace(/<pre\b[^>]*>\s*<code\b[^>]*>([\s\S]*?)<\/code>\s*<\/pre>/gi, (_, code) => {
		const body = decodeEntities(code.replace(/<[^>]+>/g, ''));
		return `\n\n\`\`\`\n${body.replace(/\n$/, '')}\n\`\`\`\n\n`;
	});
	s = s.replace(/<pre\b[^>]*>([\s\S]*?)<\/pre>/gi, (_, code) => {
		const body = decodeEntities(code.replace(/<[^>]+>/g, ''));
		return `\n\n\`\`\`\n${body.replace(/\n$/, '')}\n\`\`\`\n\n`;
	});

	// Inline code
	s = s.replace(/<code\b[^>]*>([\s\S]*?)<\/code>/gi, (_, c) => {
		const t = decodeEntities(c.replace(/<[^>]+>/g, '')).replace(/`/g, '\\`');
		return `\`${t}\``;
	});

	// Images
	s = s.replace(/<img\b[^>]*>/gi, (tag) => {
		const alt = /alt=["']([^"']*)["']/i.exec(tag)?.[1] || '';
		const src = /src=["']([^"']*)["']/i.exec(tag)?.[1] || '';
		if (!src || src.startsWith('data:')) return '';
		return `![${decodeEntities(alt)}](${src})`;
	});

	// Links
	s = s.replace(/<a\b[^>]*href=["']([^"']*)["'][^>]*>([\s\S]*?)<\/a>/gi, (_, href, inner) => {
		const text = decodeEntities(inner.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());
		if (!text) return '';
		if (!href || href.startsWith('javascript:')) return text;
		return `[${text}](${href})`;
	});

	// Headings
	for (let level = 6; level >= 1; level--) {
		const re = new RegExp(`<h${level}\\b[^>]*>([\\s\\S]*?)<\\/h${level}>`, 'gi');
		s = s.replace(re, (_, inner) => {
			const text = decodeEntities(inner.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());
			return text ? `\n\n${'#'.repeat(level)} ${text}\n\n` : '\n';
		});
	}

	// Lists
	s = s.replace(/<li\b[^>]*>([\s\S]*?)<\/li>/gi, (_, inner) => {
		const text = decodeEntities(inner.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
		return text ? `\n- ${text}` : '';
	});
	s = s.replace(/<\/?ul\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?ol\b[^>]*>/gi, '\n');

	// Blockquote
	s = s.replace(/<blockquote\b[^>]*>([\s\S]*?)<\/blockquote>/gi, (_, inner) => {
		const text = decodeEntities(inner.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
		if (!text) return '';
		return '\n\n' + text.split(/\n+/).map((l) => `> ${l.trim()}`).join('\n') + '\n\n';
	});

	// Emphasis
	s = s.replace(/<(strong|b)\b[^>]*>([\s\S]*?)<\/\1>/gi, (_, __, inner) => {
		const t = decodeEntities(inner.replace(/<[^>]+>/g, '')).trim();
		return t ? `**${t}**` : '';
	});
	s = s.replace(/<(em|i)\b[^>]*>([\s\S]*?)<\/\1>/gi, (_, __, inner) => {
		const t = decodeEntities(inner.replace(/<[^>]+>/g, '')).trim();
		return t ? `*${t}*` : '';
	});

	// Paragraphs / remaining tags
	s = s.replace(/<\/?p\b[^>]*>/gi, '\n\n');
	s = s.replace(/<\/?div\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?span\b[^>]*>/gi, '');
	s = s.replace(/<\/?section\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?article\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?main\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?figure\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?figcaption\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?table\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?thead\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?tbody\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?tr\b[^>]*>/gi, '\n');
	s = s.replace(/<\/?t[hd]\b[^>]*>/gi, ' | ');
	s = s.replace(/<hr\s*\/?>/gi, '\n\n---\n\n');

	// Any leftover tags
	s = s.replace(/<[^>]+>/g, '');
	s = decodeEntities(s);

	// Cleanup whitespace
	s = s.replace(/[ \t]+\n/g, '\n');
	s = s.replace(/\n{3,}/g, '\n\n');
	return s.trim() + '\n';
}

/**
 * @param {string} markdown
 * @returns {number}
 */
function estimateTokens(markdown) {
	// Rough GPT-style estimate (~4 chars / token); ceil at least 1 for non-empty
	if (!markdown) return 0;
	return Math.max(1, Math.ceil(markdown.length / 4));
}

/**
 * @param {string} html
 * @returns {string}
 */
function buildMarkdownDocument(html) {
	const title =
		metaContent(html, 'title') ||
		metaContent(html, 'og:title') ||
		documentTitle(html);
	const description =
		metaContent(html, 'description') || metaContent(html, 'og:description');
	const image = metaContent(html, 'og:image');

	const fm = [];
	if (title) fm.push(`title: ${yamlScalar(title)}`);
	if (description) fm.push(`description: ${yamlScalar(description)}`);
	if (image) fm.push(`image: ${yamlScalar(image)}`);

	const body = htmlToMarkdown(extractMainHtml(html));
	const jsonLd = extractJsonLd(html);

	let out = '';
	if (fm.length) {
		out += `---\n${fm.join('\n')}\n---\n\n`;
	}
	out += body;
	if (jsonLd.length) {
		out += '\n```json\n' + jsonLd.join('\n') + '\n```\n';
	}
	return out;
}

/**
 * @param {string} value
 * @returns {string}
 */
function yamlScalar(value) {
	// Quote when needed for YAML safety
	if (/[:#{}[\],&*?|>!%@`]/.test(value) || value.includes('\n') || value.includes('"')) {
		return JSON.stringify(value);
	}
	return value;
}

/**
 * @param {Headers} headers
 * @param {string} name
 * @param {string} value
 */
function appendVary(headers, value) {
	const cur = headers.get('Vary');
	if (!cur) {
		headers.set('Vary', value);
		return;
	}
	const parts = cur.split(',').map((s) => s.trim().toLowerCase());
	if (!parts.includes(value.toLowerCase())) {
		headers.set('Vary', `${cur}, ${value}`);
	}
}

/**
 * @param {EventContext} context
 */
export async function onRequest(context) {
	const { request, next } = context;
	const wantMd = prefersMarkdown(request.headers.get('Accept'));

	/** @type {Response} */
	const response = await next();

	const contentType = response.headers.get('Content-Type') || '';
	if (!contentType.toLowerCase().includes('text/html')) {
		return response;
	}

	// Always advertise negotiation for HTML pages
	const headers = new Headers(response.headers);
	appendVary(headers, 'Accept');

	if (!wantMd) {
		return new Response(response.body, {
			status: response.status,
			statusText: response.statusText,
			headers
		});
	}

	// Don't convert error shells if empty; still try
	const html = await response.text();
	if (!html || html.length > 2_097_152) {
		// Mirror CF 2MB limit: fall back to HTML
		headers.set('Content-Type', contentType);
		return new Response(html, {
			status: response.status,
			statusText: response.statusText,
			headers
		});
	}

	const markdown = buildMarkdownDocument(html);
	const mdTokens = estimateTokens(markdown);
	const htmlTokens = estimateTokens(html);

	headers.set('Content-Type', 'text/markdown; charset=utf-8');
	headers.set('x-markdown-tokens', String(mdTokens));
	headers.set('x-original-tokens', String(htmlTokens));
	if (!headers.has('content-signal') && !headers.has('Content-Signal')) {
		headers.set('Content-Signal', 'ai-train=yes, search=yes, ai-input=yes');
	}
	// Body-specific headers no longer valid
	headers.delete('Content-Length');
	headers.delete('Content-Encoding');
	headers.delete('ETag');
	headers.delete('Last-Modified');
	headers.delete('Content-Range');

	return new Response(markdown, {
		status: 200,
		headers
	});
}
