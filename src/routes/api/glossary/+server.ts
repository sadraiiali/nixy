import { dev } from '$app/environment';
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { loadGlossary, saveGlossary, type GlossaryEntry, type GlossaryFile } from '$lib/glossary.server';

// Not prerenderable: has PUT (dev-only). Static deploys use static/glossary.json
// and server-loaded pages prerendered from glossary.server at build time.
export const prerender = false;

export const GET: RequestHandler = async () => {
	return json(loadGlossary());
};

export const PUT: RequestHandler = async ({ request }) => {
	// Editing is only allowed on the Vite dev server (not Webxdc / production).
	if (!dev) {
		error(403, 'ویرایش واژه‌نامه فقط در حالت dev مجاز است');
	}

	let body: unknown;
	try {
		body = await request.json();
	} catch {
		error(400, 'JSON نامعتبر');
	}

	const data = body as Partial<GlossaryFile>;
	if (!data || !Array.isArray(data.entries)) {
		error(400, 'فیلد entries لازم است');
	}

	const current = loadGlossary();
	const entries: GlossaryEntry[] = data.entries.map((raw) => {
		const e = raw as Partial<GlossaryEntry> & Record<string, unknown>;
		const statusRaw = String(e.status ?? 'pending');
		const status: GlossaryEntry['status'] =
			statusRaw === 'approved' || statusRaw === 'skipped' ? statusRaw : 'pending';
		return {
			term: String(e.term ?? '').trim(),
			suggestion: String(e.suggestion ?? ''),
			translation: String(e.translation ?? ''),
			notes: String(e.notes ?? ''),
			sources: Array.isArray(e.sources) ? e.sources.map(String) : [],
			count: Number(e.count) || 0,
			is_tech: Boolean(e.is_tech),
			status
		} satisfies GlossaryEntry;
	}).filter((e) => e.term);

	const next: GlossaryFile = {
		version: current.version ?? 1,
		docs: Array.isArray(data.docs) ? data.docs.map(String) : current.docs,
		entries
	};

	saveGlossary(next);
	return json({ ok: true, count: next.entries.length });
};
