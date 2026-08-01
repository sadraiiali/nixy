#!/usr/bin/env node
/**
 * Download GitHub (org/user) avatars and shrink to tiny circular WebP (~≤1 KiB).
 * Output: static/icons/sources/*.webp
 *
 * Runs on `npm run build` (and can be run alone). Offline: reuses existing files
 * if download fails.
 *
 * Usage:
 *   node scripts/fetch-source-avatars.mjs
 *   node scripts/fetch-source-avatars.mjs --force
 */
import { spawnSync } from 'node:child_process';
import { mkdir, writeFile, access, stat, copyFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { randomBytes } from 'node:crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT_DIR = path.join(ROOT, 'static/icons/sources');
const FORCE = process.argv.includes('--force');
const MAX_BYTES = 1200; // aim ~1 KiB
const SIZE = 32; // display at ~28–32 CSS px

/** id → GitHub login (org or user) used for https://github.com/{login}.png */
const AVATARS = [
	{ id: 'nixos', login: 'NixOS' },
	{ id: 'nixcloud', login: 'nixcloud' }
];

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

async function downloadPng(login, destPng) {
	const url = `https://github.com/${encodeURIComponent(login)}.png?size=64`;
	const res = await fetch(url, {
		headers: { 'User-Agent': 'nix-notes-build/0.1 (source-avatars)' },
		redirect: 'follow'
	});
	if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
	const buf = Buffer.from(await res.arrayBuffer());
	if (buf.length < 100) throw new Error(`tiny response for ${login}`);
	await writeFile(destPng, buf);
	return destPng;
}

/**
 * Encode PNG → circular WebP ≤ MAX_BYTES, trying lower quality if needed.
 */
function encodeCircularWebp(srcPng, destWebp) {
	const magick = which('magick') || which('convert');
	const ffmpeg = which('ffmpeg');

	const tryMagick = (size, quality) => {
		if (!magick) return false;
		const r = size / 2;
		// ImageMagick: resize, circular alpha mask, lossy webp
		const args =
			path.basename(magick) === 'convert'
				? [
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
					]
				: [
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
		const r0 = spawnSync(magick, args, { encoding: 'utf8' });
		return r0.status === 0;
	};

	const tryFfmpeg = (size, q) => {
		if (!ffmpeg) return false;
		// square lossy webp; CSS border-radius makes the circle
		const r = spawnSync(
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
				String(q),
				destWebp
			],
			{ encoding: 'utf8' }
		);
		return r.status === 0;
	};

	const ladder = [
		[SIZE, 50],
		[SIZE, 40],
		[SIZE, 30],
		[24, 45],
		[24, 35],
		[20, 40],
		[16, 40]
	];

	for (const [sz, q] of ladder) {
		const ok = tryMagick(sz, q) || tryFfmpeg(sz, q);
		if (!ok) continue;
		// check size asynchronously by caller
		return true;
	}
	return false;
}

async function fileSize(p) {
	const s = await stat(p);
	return s.size;
}

async function processOne({ id, login }) {
	const outWebp = path.join(OUT_DIR, `${id}.webp`);
	if (!FORCE && (await exists(outWebp))) {
		const n = await fileSize(outWebp);
		if (n > 0 && n <= MAX_BYTES * 2) {
			console.log(`  keep ${id}.webp (${n} B)`);
			return { id, path: outWebp, bytes: n, cached: true };
		}
	}

	const tmp = path.join(tmpdir(), `src-av-${randomBytes(4).toString('hex')}.png`);
	try {
		console.log(`  download github.com/${login}.png …`);
		await downloadPng(login, tmp);
		const ok = encodeCircularWebp(tmp, outWebp);
		if (!ok) {
			// last resort: copy raw png if tools missing (not ideal but better than nothing)
			if (await exists(outWebp)) {
				const n = await fileSize(outWebp);
				console.warn(`  warn: encode failed, kept existing ${id}.webp (${n} B)`);
				return { id, path: outWebp, bytes: n, cached: true };
			}
			throw new Error('no magick/ffmpeg to encode webp');
		}
		let n = await fileSize(outWebp);
		// If still large, force smaller ladder once more with ffmpeg/magick at 16px
		if (n > MAX_BYTES) {
			const magick = which('magick') || which('convert');
			const ffmpeg = which('ffmpeg');
			if (magick) {
				spawnSync(
					magick,
					[outWebp, '-resize', '16x16', '-quality', '30', outWebp],
					{ encoding: 'utf8' }
				);
				n = await fileSize(outWebp);
			} else if (ffmpeg) {
				const t2 = outWebp + '.tmp.webp';
				spawnSync(
					ffmpeg,
					[
						'-y',
						'-i',
						outWebp,
						'-vf',
						'scale=16:16',
						'-frames:v',
						'1',
						'-c:v',
						'libwebp',
						'-q:v',
						'25',
						t2
					],
					{ encoding: 'utf8' }
				);
				await copyFile(t2, outWebp).catch(() => {});
				n = await fileSize(outWebp);
			}
		}
		console.log(`  wrote ${id}.webp (${n} B)`);
		return { id, path: outWebp, bytes: n, cached: false };
	} catch (e) {
		if (await exists(outWebp)) {
			const n = await fileSize(outWebp);
			console.warn(`  warn: ${id}: ${e.message}; using cached (${n} B)`);
			return { id, path: outWebp, bytes: n, cached: true, error: String(e.message) };
		}
		console.error(`  error: ${id}: ${e.message}`);
		return { id, error: String(e.message) };
	}
}

async function main() {
	await mkdir(OUT_DIR, { recursive: true });
	console.log('fetch-source-avatars →', path.relative(ROOT, OUT_DIR));
	const results = [];
	for (const av of AVATARS) {
		results.push(await processOne(av));
	}
	const ok = results.filter((r) => r.path);
	const failed = results.filter((r) => !r.path);
	console.log(`done: ${ok.length} ok, ${failed.length} failed`);
	// Don't fail the whole build if network is down but files exist;
	// fail only if nothing usable for nixos (required).
	const nixos = results.find((r) => r.id === 'nixos');
	if (!nixos?.path) {
		console.error('fatal: missing nixos.webp avatar');
		process.exit(1);
	}
}

main().catch((e) => {
	console.error(e);
	process.exit(1);
});
