import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

export type GlossaryEntry = {
	term: string;
	suggestion: string;
	translation: string;
	notes: string;
	sources: string[];
	count: number;
	is_tech: boolean;
	status: 'pending' | 'approved' | 'skipped';
};

export type GlossaryFile = {
	version: number;
	docs: string[];
	entries: GlossaryEntry[];
};

export function glossaryPath(): string {
	// Project root (one level above src)
	return join(process.cwd(), 'glossary.json');
}

export function loadGlossary(): GlossaryFile {
	const path = glossaryPath();
	if (!existsSync(path)) {
		return { version: 1, docs: [], entries: [] };
	}
	const data = JSON.parse(readFileSync(path, 'utf-8')) as GlossaryFile;
	data.entries = data.entries ?? [];
	data.docs = data.docs ?? [];
	return data;
}

export function saveGlossary(data: GlossaryFile): void {
	const path = glossaryPath();
	data.entries = [...(data.entries ?? [])].sort((a, b) => {
		const sa = a.status === 'pending' ? 0 : 1;
		const sb = b.status === 'pending' ? 0 : 1;
		if (sa !== sb) return sa - sb;
		const ta = a.is_tech ? 0 : 1;
		const tb = b.is_tech ? 0 : 1;
		if (ta !== tb) return ta - tb;
		return a.term.localeCompare(b.term);
	});
	writeFileSync(path, JSON.stringify(data, null, 2) + '\n', 'utf-8');
}
