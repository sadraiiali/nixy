/**
 * Resolve browser pathnames → on-disk Markdown for the dev page editor.
 * Server-only (uses node:fs / path).
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sanitizeMdForSitePage } from '$lib/html-to-md';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

export type DevMdTarget = {
	/** Absolute path written for live site content (mdsvex) */
	sitePath: string;
	/** Project-relative site path (for UI) */
	siteRel: string;
	/** Absolute path under docs/fa when a source mirror exists */
	docsPath: string | null;
	docsRel: string | null;
};

function normUrlPath(p: string): string {
	let s = (p || '/').split('?')[0].split('#')[0] || '/';
	if (!s.startsWith('/')) s = '/' + s;
	s = s.replace(/\/+/g, '/');
	if (s.length > 1 && s.endsWith('/')) s = s.slice(0, -1);
	return s;
}

function underRoot(abs: string, ...allowed: string[]): boolean {
	const real = path.resolve(abs);
	const root = path.resolve(ROOT);
	if (!real.startsWith(root + path.sep) && real !== root) return false;
	return allowed.some((dir) => {
		const base = path.resolve(ROOT, dir);
		return real === base || real.startsWith(base + path.sep);
	});
}

/**
 * Map browser path → site +page.md (+ optional docs/fa for manuals).
 * Supports `/pages/...` and `/blog/...`.
 */
export function resolveDevMdTarget(urlPathname: string): DevMdTarget | null {
	const p = normUrlPath(urlPathname);

	// ── Blog posts: /blog/slug → src/routes/blog/slug/+page.md ──
	if (p.startsWith('/blog/')) {
		const rest = p.slice('/blog/'.length);
		if (!rest || rest.includes('..')) return null;
		const parts = rest.split('/').filter(Boolean);
		if (parts.some((seg) => seg === '.' || seg === '..' || seg.includes('\0'))) return null;

		const sitePath = path.join(ROOT, 'src/routes/blog', ...parts, '+page.md');
		if (!existsSync(sitePath) || !underRoot(sitePath, 'src/routes/blog')) return null;

		const siteRel = path.relative(ROOT, sitePath).replace(/\\/g, '/');
		return { sitePath, siteRel, docsPath: null, docsRel: null };
	}

	if (!p.startsWith('/pages/')) return null;

	// /pages/foo/bar → pages/foo/bar
	const rest = p.slice('/pages/'.length);
	if (!rest || rest.includes('..')) return null;

	const parts = rest.split('/').filter(Boolean);
	if (parts.some((seg) => seg === '.' || seg === '..' || seg.includes('\0'))) return null;

	// Prefer directory/+page.md, then file.md style is not used (all mdsvex are +page.md)
	const siteCandidate = path.join(ROOT, 'src/routes/pages', ...parts, '+page.md');
	const siteIndex = path.join(ROOT, 'src/routes/pages', ...parts.slice(0, -1), '+page.md');

	let sitePath: string | null = null;
	if (existsSync(siteCandidate)) sitePath = siteCandidate;
	// /pages/nix-dev → pages/nix-dev/+page.md already covered by candidate with parts=['nix-dev']

	if (!sitePath) {
		// try parent for trailing index-style (shouldn't happen with norm)
		if (existsSync(siteIndex) && parts.length === 0) sitePath = siteIndex;
	}
	if (!sitePath || !underRoot(sitePath, 'src/routes/pages')) return null;

	const siteRel = path.relative(ROOT, sitePath).replace(/\\/g, '/');

	// docs/fa mirror
	let docsPath: string | null = null;
	let docsRel: string | null = null;
	const head = parts[0];
	let docsParts: string[] | null = null;

	if (head === 'nixpkgs-manual') {
		docsParts = ['nixpkgs-manual', ...parts.slice(1)];
	} else if (head === 'nix-manual') {
		docsParts = ['nix-manual', ...parts.slice(1)];
	} else if (head === 'nix-dev') {
		// /pages/nix-dev/guides/faq → docs/fa/guides/faq.md
		docsParts = parts.slice(1);
		if (docsParts.length === 0) docsParts = ['index'];
	} else if (head === 'first-steps') {
		docsParts = ['first-steps', ...parts.slice(1)];
	} else if (head === 'tour-of-nix') {
		docsParts = ['tour-of-nix', ...parts.slice(1)];
	} else if (head === 'how-nix-works') {
		docsParts = null; // often only site page
	}

	if (docsParts) {
		// map empty → index.md; last segment as .md
		let relMd: string;
		if (docsParts.length === 0 || (docsParts.length === 1 && docsParts[0] === 'index')) {
			if (head === 'nix-dev') relMd = 'index.md';
			else relMd = path.join(head === 'nix-dev' ? '' : head, 'index.md');
		}
		if (docsParts[docsParts.length - 1] === 'index') {
			relMd = path.join(...docsParts.slice(0, -1), 'index.md');
		} else {
			relMd = path.join(...docsParts) + '.md';
		}
		// clean double
		relMd = relMd.replace(/\\/g, '/').replace(/^\/+/, '');
		const abs = path.join(ROOT, 'docs/fa', relMd);
		if (existsSync(abs) && underRoot(abs, 'docs/fa')) {
			docsPath = abs;
			docsRel = path.relative(ROOT, abs).replace(/\\/g, '/');
		}
	}

	return { sitePath, siteRel, docsPath, docsRel };
}

export function readDevMd(target: DevMdTarget): string {
	return readFileSync(target.sitePath, 'utf8');
}

export function writeDevMd(target: DevMdTarget, content: string): { site: string; docs: string | null } {
	// {#id} is invalid Svelte once mdsvex compiles MD — normalize to <span id> + escape braces
	const text = sanitizeMdForSitePage(content);
	if (!underRoot(target.sitePath, 'src/routes/pages', 'src/routes/blog')) {
		throw new Error('مسیر سایت خارج از محدوده مجاز است');
	}
	writeFileSync(target.sitePath, text, 'utf8');

	let docs: string | null = null;
	if (target.docsPath && underRoot(target.docsPath, 'docs/fa')) {
		writeFileSync(target.docsPath, text, 'utf8');
		docs = target.docsRel;
	}
	return { site: target.siteRel, docs };
}
