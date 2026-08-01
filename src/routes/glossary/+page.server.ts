import type { PageServerLoad } from './$types';
import { loadGlossary } from '$lib/glossary.server';

/** Public end-glossary: approved tech terms only. */
export const load: PageServerLoad = async () => {
	const glossary = loadGlossary();
	const entries = (glossary.entries ?? [])
		.filter((e) => e.is_tech && e.status === 'approved')
		.map((e) => ({
			term: e.term,
			translation: (e.translation || e.suggestion || '').trim(),
			count: e.count ?? 0
		}))
		.filter((e) => e.translation)
		.sort((a, b) => a.term.localeCompare(b.term, 'en', { sensitivity: 'base' }));

	return {
		version: glossary.version ?? 1,
		entries,
		count: entries.length
	};
};
