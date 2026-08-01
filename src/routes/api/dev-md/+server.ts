/**
 * Dev-only Markdown page editor API.
 * GET  ?pathname=/pages/...|/blog/...  → { content, siteRel, docsRel }
 * PUT  { pathname, content } → write +page.md (+ docs/fa when present)
 */
import { dev } from '$app/environment';
import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { readDevMd, resolveDevMdTarget, writeDevMd } from '$lib/dev-md.server';

export const prerender = false;

function assertDev() {
	if (!dev) {
		error(403, 'ویرایش Markdown فقط در حالت dev مجاز است');
	}
}

export const GET: RequestHandler = async ({ url }) => {
	assertDev();
	const pathname = url.searchParams.get('pathname') || '';
	const target = resolveDevMdTarget(pathname);
	if (!target) {
		error(404, 'برای این مسیر فایل Markdown پیدا نشد');
	}
	try {
		const content = readDevMd(target);
		return json({
			ok: true,
			pathname,
			content,
			siteRel: target.siteRel,
			docsRel: target.docsRel
		});
	} catch (e) {
		error(500, e instanceof Error ? e.message : 'خواندن فایل ناموفق بود');
	}
};

export const PUT: RequestHandler = async ({ request }) => {
	assertDev();
	let body: unknown;
	try {
		body = await request.json();
	} catch {
		error(400, 'JSON نامعتبر');
	}
	const data = body as { pathname?: string; content?: string };
	const pathname = String(data.pathname ?? '');
	if (typeof data.content !== 'string') {
		error(400, 'فیلد content (رشته) لازم است');
	}
	const target = resolveDevMdTarget(pathname);
	if (!target) {
		error(404, 'برای این مسیر فایل Markdown پیدا نشد');
	}
	try {
		const written = writeDevMd(target, data.content);
		return json({ ok: true, ...written });
	} catch (e) {
		error(500, e instanceof Error ? e.message : 'نوشتن فایل ناموفق بود');
	}
};
