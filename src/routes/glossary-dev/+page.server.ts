import type { PageServerLoad } from './$types';
import { loadGlossary } from '$lib/glossary.server';

export const load: PageServerLoad = async () => {
	const glossary = loadGlossary();
	const entries = glossary.entries ?? [];
	const tech = entries.filter((e) => e.is_tech);
	const approved = tech.filter((e) => e.status === 'approved');
	const skipped = tech.filter((e) => e.status === 'skipped');
	const pending = tech.filter((e) => e.status === 'pending');
	const withTr = tech.filter((e) => (e.translation || '').trim());
	const multi = tech.filter((e) => e.term.includes(' '));
	const withNotes = tech.filter((e) => (e.notes || '').trim());
	const differs = tech.filter((e) => {
		const t = (e.translation || '').trim();
		const s = (e.suggestion || '').trim();
		return t && s && t !== s;
	});

	// per-source counts
	const bySource: Record<string, number> = {};
	for (const e of tech) {
		for (const s of e.sources || []) {
			bySource[s] = (bySource[s] || 0) + 1;
		}
	}

	return {
		glossary,
		stats: {
			total: entries.length,
			tech: tech.length,
			approved: approved.length,
			pending: pending.length,
			skipped: skipped.length,
			filled: withTr.length,
			multiword: multi.length,
			withNotes: withNotes.length,
			differs: differs.length,
			docs: glossary.docs,
			bySource
		}
	};
};
