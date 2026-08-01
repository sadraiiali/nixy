#!/usr/bin/env node
/**
 * Build sitemap.xml from prerendered HTML under build/.
 * Run after `vite build` (see package.json).
 *
 * PUBLIC_SITE_URL — absolute origin (default https://nixy.a15d.at)
 */
import { readdir, writeFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const BUILD = path.join(ROOT, 'build');

const ORIGIN = (
	process.env.PUBLIC_SITE_URL ||
	process.env.SITE_URL ||
	'https://nixy.a15d.at'
).replace(/\/$/, '');

/** Paths that must not appear in the public sitemap (noindex / private). */
const EXCLUDE = new Set([
	'/404',
	'/settings',
	'/glossary-dev'
]);

async function walkHtml(dir, out = []) {
	let entries;
	try {
		entries = await readdir(dir, { withFileTypes: true });
	} catch (e) {
		if (e && e.code === 'ENOENT') {
			console.error('generate-sitemap: missing build/ — run vite build first');
			process.exit(1);
		}
		throw e;
	}
	for (const ent of entries) {
		const full = path.join(dir, ent.name);
		if (ent.isDirectory()) {
			// skip Vite asset trees (no HTML routes)
			if (ent.name === '_app' || ent.name === 'fonts') continue;
			await walkHtml(full, out);
			continue;
		}
		if (ent.isFile() && ent.name.endsWith('.html')) {
			out.push(full);
		}
	}
	return out;
}

/** build/pages/foo.html → /pages/foo ; build/index.html → / */
function htmlPathToUrl(file) {
	const rel = path.relative(BUILD, file).split(path.sep).join('/');
	if (rel === 'index.html') return '/';
	if (rel.endsWith('/index.html')) {
		return '/' + rel.slice(0, -'/index.html'.length);
	}
	if (rel.endsWith('.html')) {
		return '/' + rel.slice(0, -'.html'.length);
	}
	return '/' + rel;
}

function priorityFor(urlPath) {
	if (urlPath === '/') return '1.0';
	if (urlPath === '/glossary') return '0.8';
	if (
		urlPath === '/pages/nix-dev' ||
		urlPath === '/pages/nix-manual' ||
		urlPath === '/pages/nixpkgs-manual' ||
		urlPath === '/pages/tour-of-nix'
	) {
		return '0.9';
	}
	const depth = urlPath.split('/').filter(Boolean).length;
	if (depth <= 2) return '0.7';
	if (depth <= 4) return '0.6';
	return '0.5';
}

function changefreqFor(urlPath) {
	if (urlPath === '/') return 'weekly';
	if (urlPath.startsWith('/pages/')) return 'monthly';
	return 'monthly';
}

function escapeXml(s) {
	return s
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;');
}

async function main() {
	const files = await walkHtml(BUILD);
	const urls = [];
	const seen = new Set();

	for (const file of files) {
		const urlPath = htmlPathToUrl(file);
		if (EXCLUDE.has(urlPath)) continue;
		if (urlPath.includes('/_app')) continue;
		if (seen.has(urlPath)) continue;
		seen.add(urlPath);

		let lastmod;
		try {
			const st = await stat(file);
			lastmod = st.mtime.toISOString().slice(0, 10);
		} catch {
			lastmod = new Date().toISOString().slice(0, 10);
		}

		urls.push({
			loc: `${ORIGIN}${urlPath}`,
			lastmod,
			changefreq: changefreqFor(urlPath),
			priority: priorityFor(urlPath)
		});
	}

	urls.sort((a, b) => a.loc.localeCompare(b.loc));

	const body = urls
		.map(
			(u) => `  <url>
    <loc>${escapeXml(u.loc)}</loc>
    <lastmod>${u.lastmod}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`
		)
		.join('\n');

	const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${body}
</urlset>
`;

	const out = path.join(BUILD, 'sitemap.xml');
	await writeFile(out, xml, 'utf8');
	console.log(`generate-sitemap: ${urls.length} URLs → ${path.relative(ROOT, out)} (${ORIGIN})`);
}

main().catch((err) => {
	console.error(err);
	process.exit(1);
});
