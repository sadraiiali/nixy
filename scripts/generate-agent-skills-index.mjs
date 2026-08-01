#!/usr/bin/env node
/**
 * Generate /.well-known/agent-skills/index.json (Agent Skills Discovery RFC v0.2.0).
 *
 * Scans static/.well-known/agent-skills/<name>/SKILL.md, computes sha256 digests,
 * and writes index.json next to those skills.
 *
 * @see https://github.com/cloudflare/agent-skills-discovery-rfc
 * @see https://agentskills.io/
 */
import { createHash } from 'node:crypto';
import { readdir, readFile, writeFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SKILLS_DIR = path.join(ROOT, 'static/.well-known/agent-skills');
const INDEX_PATH = path.join(SKILLS_DIR, 'index.json');
const SCHEMA = 'https://schemas.agentskills.io/discovery/0.2.0/schema.json';

/**
 * @param {string} md
 * @returns {{ name?: string, description?: string }}
 */
function parseFrontmatter(md) {
	const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(md);
	if (!m) return {};
	/** @type {Record<string, string>} */
	const out = {};
	for (const line of m[1].split(/\r?\n/)) {
		const kv = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
		if (!kv) continue;
		let v = kv[2].trim();
		if (
			(v.startsWith('"') && v.endsWith('"')) ||
			(v.startsWith("'") && v.endsWith("'"))
		) {
			v = v.slice(1, -1);
		}
		out[kv[1]] = v;
	}
	return { name: out.name, description: out.description };
}

/**
 * @param {string} name
 */
function validSkillName(name) {
	return (
		typeof name === 'string' &&
		name.length >= 1 &&
		name.length <= 64 &&
		/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)
	);
}

async function main() {
	let entries;
	try {
		entries = await readdir(SKILLS_DIR, { withFileTypes: true });
	} catch (e) {
		if (e && /** @type {NodeJS.ErrnoException} */ (e).code === 'ENOENT') {
			console.error('generate-agent-skills-index: missing', SKILLS_DIR);
			process.exit(1);
		}
		throw e;
	}

	/** @type {Array<{ name: string, type: 'skill-md', description: string, url: string, digest: string }>} */
	const skills = [];

	for (const ent of entries) {
		if (!ent.isDirectory()) continue;
		const skillMd = path.join(SKILLS_DIR, ent.name, 'SKILL.md');
		let st;
		try {
			st = await stat(skillMd);
		} catch {
			continue;
		}
		if (!st.isFile()) continue;

		const buf = await readFile(skillMd);
		const text = buf.toString('utf8');
		const fm = parseFrontmatter(text);
		const name = fm.name || ent.name;
		const description = fm.description;
		if (!validSkillName(name)) {
			console.error(`generate-agent-skills-index: invalid name for ${ent.name}: ${name}`);
			process.exit(1);
		}
		if (!description || description.length > 1024) {
			console.error(
				`generate-agent-skills-index: missing or too-long description for ${name}`
			);
			process.exit(1);
		}
		if (name !== ent.name) {
			console.warn(
				`generate-agent-skills-index: dir "${ent.name}" name frontmatter "${name}" — using frontmatter name in index; url path uses directory`
			);
		}

		const digest = 'sha256:' + createHash('sha256').update(buf).digest('hex');
		skills.push({
			name,
			type: 'skill-md',
			description,
			url: `/.well-known/agent-skills/${ent.name}/SKILL.md`,
			digest
		});
	}

	skills.sort((a, b) => a.name.localeCompare(b.name));

	const index = {
		$schema: SCHEMA,
		skills
	};

	const body = JSON.stringify(index, null, 2) + '\n';
	await writeFile(INDEX_PATH, body, 'utf8');
	console.log(
		`generate-agent-skills-index: wrote ${skills.length} skill(s) → ${path.relative(ROOT, INDEX_PATH)}`
	);
}

main().catch((err) => {
	console.error(err);
	process.exit(1);
});
