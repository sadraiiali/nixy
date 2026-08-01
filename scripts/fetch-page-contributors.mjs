#!/usr/bin/env node
/**
 * Fetch GitHub file contributors for each docs page and write:
 *   - src/lib/page-contributors.json  (route → people)
 *   - static/icons/contributors/{login}.webp  (tiny circular ~≤1 KiB)
 *
 * ## How contributors are discovered
 * Default: scrape github.com HTML history pages (no REST API quota):
 *   https://github.com/{owner}/{repo}/commits/{ref}/{path}
 * Optional: --api uses GET /repos/…/commits?path=… (60/h without token, 5000/h with).
 * Avatars: github.com/{user}.png (CDN, free either way).
 *
 *   node scripts/fetch-page-contributors.mjs
 *   node scripts/fetch-page-contributors.mjs --force
 *   node scripts/fetch-page-contributors.mjs --sections nix-dev,nix-manual
 *   node scripts/fetch-page-contributors.mjs --limit 20
 *   node scripts/fetch-page-contributors.mjs --api   # REST instead of HTML
 *
 * Existing map entries are kept unless --force; avatars are reused when present.
 */
import { spawnSync } from 'node:child_process';
import {
	mkdir,
	writeFile,
	readFile,
	access,
	stat
} from 'node:fs/promises';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { randomBytes } from 'node:crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const MAP_PATH = path.join(ROOT, 'src/lib/page-source-map.json');
const OUT_JSON = path.join(ROOT, 'src/lib/page-contributors.json');
const AVATAR_DIR = path.join(ROOT, 'static/icons/contributors');

const FORCE = process.argv.includes('--force');
/** If true, sleep until rate-limit reset when remaining=0 (default: fail fast). */
const WAIT_RESET = process.argv.includes('--wait-reset');
const args = process.argv.slice(2);
function argVal(name, fallback = null) {
	const i = args.indexOf(name);
	if (i === -1 || !args[i + 1]) return fallback;
	return args[i + 1];
}

const SECTION_FILTER = (argVal('--sections', '') || '')
	.split(',')
	.map((s) => s.trim())
	.filter(Boolean);
const LIMIT = Number(argVal('--limit', '0')) || 0;
const MAX_CONTRIB = 12;
/** Commit list pages per file (each page = 1 REST API call). Default 1. */
const COMMIT_PAGES = Math.max(1, Number(argVal('--commit-pages', '1')) || 1);
const PER_PAGE = 100;
const CONCURRENCY = Math.max(1, Number(argVal('--concurrency', '2')) || 2);
const AVATAR_SIZE = 32;
const MAX_AVATAR_BYTES = 1400;
/** Max seconds to wait on a single rate-limit hit when --wait-reset */
const MAX_WAIT_S = Number(argVal('--max-wait', '120')) || 120;

class RateLimitError extends Error {
	/**
	 * @param {string} message
	 * @param {{ remaining?: number, reset?: number, limit?: number }} info
	 */
	constructor(message, info = {}) {
		super(message);
		this.name = 'RateLimitError';
		this.remaining = info.remaining;
		this.reset = info.reset;
		this.limit = info.limit;
	}
}

function loadDotenv() {
	try {
		const text = readFileSync(path.join(ROOT, '.env'), 'utf8');
		for (const raw of text.split('\n')) {
			const line = raw.trim();
			if (!line || line.startsWith('#') || !line.includes('=')) continue;
			const eq = line.indexOf('=');
			const key = line.slice(0, eq).trim();
			let val = line.slice(eq + 1).trim();
			if (
				(val.startsWith('"') && val.endsWith('"')) ||
				(val.startsWith("'") && val.endsWith("'"))
			) {
				val = val.slice(1, -1);
			}
			if (!(key in process.env) || process.env[key] === '') {
				process.env[key] = val;
			}
		}
	} catch {
		/* no .env */
	}
}

function which(cmd) {
	const r = spawnSync('sh', ['-c', `command -v ${cmd}`], { encoding: 'utf8' });
	return r.status === 0 ? r.stdout.trim() : '';
}

async function exists(p) {
	try {
		await access(p);
		return true;
	} catch {
		return false;
	}
}

function sleep(ms) {
	return new Promise((r) => setTimeout(r, ms));
}

function ghHeaders(token) {
	const headers = {
		'User-Agent': 'nix-notes-build/0.1 (page-contributors)',
		Accept: 'application/vnd.github+json',
		'X-GitHub-Api-Version': '2022-11-28'
	};
	if (token) headers.Authorization = `Bearer ${token}`;
	return headers;
}

/**
 * Read core REST rate-limit bucket.
 * @returns {Promise<{ limit: number, remaining: number, reset: number, used: number }>}
 */
async function getRateLimit(token) {
	const res = await fetch('https://api.github.com/rate_limit', {
		headers: ghHeaders(token)
	});
	if (!res.ok) {
		return { limit: token ? 5000 : 60, remaining: -1, reset: 0, used: 0 };
	}
	const j = await res.json();
	const core = j.resources?.core || j.rate || {};
	return {
		limit: Number(core.limit ?? 0),
		remaining: Number(core.remaining ?? 0),
		reset: Number(core.reset ?? 0),
		used: Number(core.used ?? 0)
	};
}

function formatReset(resetUnix) {
	if (!resetUnix) return '?';
	const ms = resetUnix * 1000 - Date.now();
	const s = Math.max(0, Math.ceil(ms / 1000));
	const when = new Date(resetUnix * 1000).toLocaleTimeString();
	return `${s}s (at ${when})`;
}

function logRateLimit(rl, label = 'rate-limit') {
	console.log(
		`${label}: remaining=${rl.remaining}/${rl.limit}  used=${rl.used}  reset_in=${formatReset(rl.reset)}`
	);
}

/**
 * @param {string} url
 * @param {string} token
 * @param {{ waitReset?: boolean }} opts
 */
async function ghFetch(url, token, opts = {}) {
	const waitReset = opts.waitReset ?? WAIT_RESET;
	const headers = ghHeaders(token);

	for (let attempt = 0; attempt < 4; attempt++) {
		const res = await fetch(url, { headers });
		const remaining = Number(res.headers.get('x-ratelimit-remaining') ?? -1);
		const reset = Number(res.headers.get('x-ratelimit-reset') || 0);
		const limit = Number(res.headers.get('x-ratelimit-limit') || 0);

		if (res.status === 403 || res.status === 429) {
			const body = await res.text().catch(() => '');
			const isRate =
				remaining === 0 ||
				/rate limit/i.test(body) ||
				res.status === 429 ||
				/secondary rate/i.test(body);

			if (!isRate) {
				throw new Error(`GitHub ${res.status} ${url}: ${body.slice(0, 200)}`);
			}

			const waitMs = reset
				? Math.max(1000, reset * 1000 - Date.now() + 1000)
				: 5000 * (attempt + 1);
			const waitS = Math.round(waitMs / 1000);

			console.warn(
				`  API rate-limit hit (${res.status}) remaining=${remaining}/${limit || '?'} reset_in=${formatReset(reset)}`
			);
			console.warn(
				`  note: this is the Commits REST API, not avatar downloads (images are free CDN).`
			);

			if (!waitReset || waitS > MAX_WAIT_S) {
				throw new RateLimitError(
					`GitHub API rate limit exhausted (remaining=${remaining}/${limit || '?'}). ` +
						`Resets in ${formatReset(reset)}. ` +
						(token
							? 'Token is set but quota is empty — wait for reset or reduce --limit.'
							: 'No GITHUB_TOKEN: unauthenticated limit is only 60 req/h. Add GITHUB_TOKEN=ghp_… to .env (5000/h).') +
						(waitS > MAX_WAIT_S && !waitReset
							? ` Re-run with --wait-reset to sleep up to ${MAX_WAIT_S}s, or wait ~${waitS}s.`
							: ''),
					{ remaining, reset, limit }
				);
			}

			console.warn(`  --wait-reset: sleeping ${Math.min(waitS, MAX_WAIT_S)}s …`);
			await sleep(Math.min(waitMs, MAX_WAIT_S * 1000));
			continue;
		}

		if (res.status === 404) return null;
		if (!res.ok) {
			const body = await res.text().catch(() => '');
			throw new Error(`GitHub ${res.status} ${url}: ${body.slice(0, 200)}`);
		}

		// Soft warning when running low
		if (remaining >= 0 && remaining <= 5) {
			console.warn(
				`  API quota low: remaining=${remaining}/${limit} reset_in=${formatReset(reset)}`
			);
		}
		return res.json();
	}
	throw new RateLimitError(`GitHub rate limit retries exhausted: ${url}`);
}

/** Bots / non-humans we never show as page authors */
const SKIP_LOGINS = new Set([
	'web-flow',
	'github-actions',
	'github-actions[bot]',
	'dependabot',
	'dependabot[bot]',
	'renovate',
	'renovate[bot]',
	'nixos-discourse',
	'actions-user'
]);

/**
 * Scrape github.com commits HTML for a file path — does NOT use REST API quota.
 * Counts `commits?author=` links on the history page(s).
 */
async function commitsFromHtml(owner, repo, filePath, ref = 'master') {
	const byLogin = new Map();
	const base = `https://github.com/${owner}/${repo}/commits/${encodeURIComponent(ref)}/${filePath
		.split('/')
		.map(encodeURIComponent)
		.join('/')}`;

	for (let page = 1; page <= COMMIT_PAGES; page++) {
		const url = page === 1 ? base : `${base}?page=${page}`;
		const res = await fetch(url, {
			headers: {
				'User-Agent':
					'Mozilla/5.0 (compatible; nix-notes-build/0.1; +https://github.com/NixOS/nix.dev)',
				Accept: 'text/html'
			},
			redirect: 'follow'
		});
		if (res.status === 404) break;
		if (!res.ok) {
			throw new Error(`commits HTML ${res.status} ${url}`);
		}
		const html = await res.text();
		// e.g. href="/NixOS/nix.dev/commits?author=fricklerhandwerk"
		const re =
			/commits\?author=([A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38})/g;
		let m;
		let hits = 0;
		while ((m = re.exec(html)) !== null) {
			const login = m[1];
			if (SKIP_LOGINS.has(login)) continue;
			hits++;
			const prev = byLogin.get(login) || {
				login,
				name: login,
				avatar_url: null,
				commits: 0
			};
			prev.commits += 1;
			byLogin.set(login, prev);
		}
		if (hits === 0) break;
		if (hits < 30) break; // likely last page
	}
	return [...byLogin.values()].sort((a, b) => b.commits - a.commits);
}

/** REST API path (uses quota) — only with --api */
async function commitsFromApi(owner, repo, filePath, token) {
	const byLogin = new Map();
	for (let page = 1; page <= COMMIT_PAGES; page++) {
		const q = new URL(`https://api.github.com/repos/${owner}/${repo}/commits`);
		q.searchParams.set('path', filePath);
		q.searchParams.set('per_page', String(PER_PAGE));
		q.searchParams.set('page', String(page));
		const data = await ghFetch(q.toString(), token);
		if (!data || !Array.isArray(data) || data.length === 0) break;
		for (const c of data) {
			const author = c.author;
			const login = author?.login;
			if (!login || SKIP_LOGINS.has(login)) continue;
			const prev = byLogin.get(login) || {
				login,
				name: c.commit?.author?.name || author.login,
				avatar_url: author.avatar_url || null,
				commits: 0
			};
			prev.commits += 1;
			if (author.avatar_url) prev.avatar_url = author.avatar_url;
			byLogin.set(login, prev);
		}
		if (data.length < PER_PAGE) break;
	}
	return [...byLogin.values()].sort((a, b) => b.commits - a.commits);
}

/**
 * Prefer HTML scrape (no REST quota). Use --api for REST commits listing.
 */
async function commitsForPath(owner, repo, filePath, token, ref = 'master') {
	const useApi = process.argv.includes('--api');
	if (!useApi) {
		const list = await commitsFromHtml(owner, repo, filePath, ref);
		if (list.length > 0) return list;
		console.warn(`  html: no authors for ${filePath}`);
		return [];
	}
	return commitsFromApi(owner, repo, filePath, token);
}

function encodeCircularWebp(srcPng, destWebp) {
	const magick = which('magick') || which('convert');
	const ffmpeg = which('ffmpeg');
	const ladder = [
		[AVATAR_SIZE, 50],
		[AVATAR_SIZE, 35],
		[24, 40],
		[20, 35],
		[16, 40]
	];

	for (const [size, quality] of ladder) {
		const r = size / 2;
		if (magick) {
			const args = [
				srcPng,
				'-resize',
				`${size}x${size}`,
				'-background',
				'none',
				'-gravity',
				'center',
				'(',
				'+clone',
				'-alpha',
				'transparent',
				'-fill',
				'white',
				'-draw',
				`circle ${r},${r} ${r},0`,
				')',
				'-compose',
				'copyopacity',
				'-composite',
				'-quality',
				String(quality),
				destWebp
			];
			const out = spawnSync(magick, args, { encoding: 'utf8' });
			if (out.status === 0) return true;
		}
		if (ffmpeg) {
			const out = spawnSync(
				ffmpeg,
				[
					'-y',
					'-i',
					srcPng,
					'-vf',
					`scale=${size}:${size}:flags=lanczos`,
					'-frames:v',
					'1',
					'-c:v',
					'libwebp',
					'-lossless',
					'0',
					'-compression_level',
					'6',
					'-q:v',
					String(quality),
					destWebp
				],
				{ encoding: 'utf8' }
			);
			if (out.status === 0) return true;
		}
	}
	return false;
}

async function ensureAvatar(login, avatarUrl, force) {
	const dest = path.join(AVATAR_DIR, `${login}.webp`);
	if (!force && (await exists(dest))) {
		const n = (await stat(dest)).size;
		if (n > 0 && n < 8000) return `/icons/contributors/${login}.webp`;
	}
	const url =
		avatarUrl ||
		`https://avatars.githubusercontent.com/${encodeURIComponent(login)}?s=64`;
	// Prefer github.com/{login}.png (stable redirect)
	const pngUrl = `https://github.com/${encodeURIComponent(login)}.png?size=64`;
	const tmp = path.join(
		tmpdir(),
		`contrib-${login}-${randomBytes(3).toString('hex')}.png`
	);
	try {
		let res = await fetch(pngUrl, {
			headers: { 'User-Agent': 'nix-notes-build/0.1' },
			redirect: 'follow'
		});
		if (!res.ok) {
			res = await fetch(url, {
				headers: { 'User-Agent': 'nix-notes-build/0.1' },
				redirect: 'follow'
			});
		}
		if (!res.ok) throw new Error(`avatar HTTP ${res.status}`);
		const buf = Buffer.from(await res.arrayBuffer());
		await writeFile(tmp, buf);
		const ok = encodeCircularWebp(tmp, dest);
		if (!ok) throw new Error('encode failed (need magick or ffmpeg)');
		let n = (await stat(dest)).size;
		if (n > MAX_AVATAR_BYTES) {
			// one more shrink
			const magick = which('magick') || which('convert');
			if (magick) {
				spawnSync(magick, [dest, '-resize', '16x16', '-quality', '30', dest]);
				n = (await stat(dest)).size;
			}
		}
		return `/icons/contributors/${login}.webp`;
	} catch (e) {
		if (await exists(dest)) return `/icons/contributors/${login}.webp`;
		console.warn(`  avatar ${login}: ${e.message}`);
		return null;
	}
}

async function mapPool(items, concurrency, fn) {
	const results = new Array(items.length);
	let i = 0;
	async function worker() {
		while (i < items.length) {
			const idx = i++;
			results[idx] = await fn(items[idx], idx);
		}
	}
	await Promise.all(
		Array.from({ length: Math.min(concurrency, items.length) }, () => worker())
	);
	return results;
}

async function writeDoc(outPages, people) {
	const doc = {
		version: 1,
		description:
			'Per-page GitHub file contributors (from commits on the source path). Generated by scripts/fetch-page-contributors.mjs.',
		generatedAt: new Date().toISOString(),
		count: Object.keys(outPages).length,
		people,
		pages: outPages
	};
	await writeFile(OUT_JSON, JSON.stringify(doc, null, 2) + '\n', 'utf8');
	return doc;
}

async function main() {
	loadDotenv();
	const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
	if (!token) {
		console.warn(
			'warn: no GITHUB_TOKEN — unauthenticated REST API is only 60 req/h.'
		);
		console.warn(
			'      Avatar PNGs do NOT use this quota. Commits-per-file API does.'
		);
		console.warn('      Add to .env:  GITHUB_TOKEN=ghp_xxxxxxxx  (classic PAT, public_repo or fine-grained read)');
	} else {
		console.log(`auth: GITHUB_TOKEN set (len=${token.length})`);
	}

	const useApi = process.argv.includes('--api');
	console.log(
		useApi
			? 'mode: REST API commits (--api) — uses rate limit'
			: 'mode: HTML scrape of github.com/…/commits/… (no REST quota)'
	);

	let rl0 = { limit: 0, remaining: -1, reset: 0, used: 0 };
	if (useApi) {
		rl0 = await getRateLimit(token);
		logRateLimit(rl0, 'API rate-limit (start)');
		if (rl0.remaining === 0) {
			console.error('');
			console.error('GitHub REST API quota is empty (remaining=0).');
			console.error(`Resets in ${formatReset(rl0.reset)}.`);
			console.error(
				'Tip: drop --api to use HTML scrape (no quota), or set GITHUB_TOKEN and wait for reset.'
			);
			process.exit(2);
		}
	}

	// Rough budget check
	if (!(await exists(MAP_PATH))) {
		console.error('missing', path.relative(ROOT, MAP_PATH));
		console.error('run: uv run python -m tools.publish.page_source_map');
		process.exit(1);
	}

	const sourceMap = JSON.parse(await readFile(MAP_PATH, 'utf8'));
	/** @type {Record<string, any>} */
	let existing = { version: 1, pages: {}, people: {} };
	if (!FORCE && (await exists(OUT_JSON))) {
		try {
			existing = JSON.parse(await readFile(OUT_JSON, 'utf8'));
			if (!existing.pages) existing.pages = {};
			if (!existing.people) existing.people = {};
		} catch {
			/* fresh */
		}
	}

	await mkdir(AVATAR_DIR, { recursive: true });

	const pages = Object.values(sourceMap.pages || {}).filter((p) => {
		if (!p?.repo || !p?.rel) return false;
		if (SECTION_FILTER.length && !SECTION_FILTER.includes(p.section)) return false;
		return true;
	});

	const sectionRank = { 'nix-dev': 0, 'how-nix-works': 1, 'nix-manual': 2, 'nixpkgs-manual': 3 };
	pages.sort(
		(a, b) =>
			(sectionRank[a.section] ?? 9) - (sectionRank[b.section] ?? 9) ||
			a.route.localeCompare(b.route)
	);

	const work = LIMIT > 0 ? pages.slice(0, LIMIT) : pages;
	const needFetch = work.filter(
		(p) => FORCE || !existing.pages?.[p.route]?.contributors?.length
	);
	console.log(
		`pages: work=${work.length} need_fetch=${needFetch.length}  ` +
			`commit_pages=${COMMIT_PAGES} concurrency=${CONCURRENCY} force=${FORCE}`
	);

	const outPages = { ...(existing.pages || {}) };
	const people = { ...(existing.people || {}) };

	let fetched = 0;
	let skipped = 0;
	let failed = 0;
	/** @type {RateLimitError | null} */
	let rateLimited = null;
	let stop = false;

	await mapPool(work, CONCURRENCY, async (page) => {
		if (stop) return;
		const route = page.route;
		if (!FORCE && outPages[route]?.contributors?.length) {
			skipped++;
			return;
		}
		const [owner, repo] = String(page.repo).split('/');
		if (!owner || !repo) {
			failed++;
			return;
		}
		// Nav sometimes stores local FA filenames (*.fa.md); upstream is English *.md
		let relEn = String(page.rel || '')
			.replace(/\\/g, '/')
			.replace(/\.fa\.md$/i, '.md');
		// Legacy /pages/nix-dev/first-steps/* mirrors tutorials/first-steps/* upstream
		if (relEn === 'first-steps/index.md' || relEn.startsWith('first-steps/')) {
			relEn = 'tutorials/' + relEn;
		}
		const filePath = [page.tree, relEn].filter(Boolean).join('/').replace(/\/+/g, '/');
		try {
			const ref = page.ref || 'master';
			const list = await commitsForPath(owner, repo, filePath, token, ref);
			const top = list.slice(0, MAX_CONTRIB);
			const contribs = [];
			for (const c of top) {
				// Avatars: free CDN — not rate-limited by REST API
				const local = await ensureAvatar(c.login, c.avatar_url, false);
				const entry = {
					login: c.login,
					name: c.name || c.login,
					commits: c.commits,
					url: `https://github.com/${c.login}`,
					avatar: local || c.avatar_url || `https://github.com/${c.login}.png?size=64`
				};
				contribs.push(entry);
				people[c.login] = {
					login: c.login,
					name: entry.name,
					avatar: entry.avatar,
					url: entry.url
				};
			}
			outPages[route] = {
				route,
				section: page.section,
				rel: page.rel,
				repo: page.repo,
				path: filePath,
				github: page.github || null,
				contributors: contribs
			};
			fetched++;
			const names = contribs.map((x) => x.login).join(', ') || '(none)';
			console.log(`  ✓ ${route}  (${contribs.length}) ${names}`);
		} catch (e) {
			if (e instanceof RateLimitError) {
				rateLimited = e;
				stop = true;
				console.warn(`  stop: ${e.message}`);
				return;
			}
			failed++;
			console.warn(`  ✗ ${route}: ${e.message}`);
			if (!outPages[route]) {
				outPages[route] = {
					route,
					section: page.section,
					rel: page.rel,
					repo: page.repo,
					path: filePath,
					github: page.github || null,
					contributors: [],
					error: String(e.message)
				};
			}
		}
	});

	const doc = await writeDoc(outPages, people);
	if (useApi) {
		const rl1 = await getRateLimit(token).catch(() => null);
		if (rl1) logRateLimit(rl1, 'API rate-limit (end)');
	}

	console.log(
		`wrote ${path.relative(ROOT, OUT_JSON)}  pages=${doc.count}  ` +
			`fetched=${fetched} skipped=${skipped} failed=${failed}`
	);
	console.log(`avatars → ${path.relative(ROOT, AVATAR_DIR)} (CDN; not API quota)`);

	if (rateLimited) {
		console.error('');
		console.error('Exited early because GitHub REST API rate limit was hit.');
		console.error('Partial results were saved. Re-run without --api, or after reset.');
		process.exit(2);
	}
}

main().catch((e) => {
	console.error(e);
	process.exit(1);
});
