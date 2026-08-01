/**
 * WebMCP — expose site tools to browser AI agents.
 * @see https://webmachinelearning.github.io/webmcp/
 * @see https://isitagentready.com/.well-known/agent-skills/webmcp/SKILL.md
 */
import { goto } from '$app/navigation';
import { searchCommands } from '$lib/command-index';
import { SITE_DESCRIPTION, SITE_NAME, SITE_TITLE } from '$lib/site-meta';

type JsonSchema = Record<string, unknown>;

type ToolExecuteCallback = (input: Record<string, unknown>) => Promise<unknown>;

type ModelContextTool = {
	name: string;
	title?: string;
	description: string;
	inputSchema?: JsonSchema;
	execute: ToolExecuteCallback;
	annotations?: { readOnlyHint?: boolean; untrustedContentHint?: boolean };
};

type ModelContext = {
	registerTool?: (
		tool: ModelContextTool,
		options?: { signal?: AbortSignal }
	) => Promise<void>;
	/** Older / experimental surface used by some scanners */
	provideContext?: (ctx: {
		tools: Array<{
			name: string;
			description: string;
			inputSchema?: JsonSchema;
			execute: ToolExecuteCallback;
		}>;
	}) => void | Promise<void>;
};

type NavModelContext = ModelContext | undefined;

function getModelContext(): ModelContext | null {
	if (typeof document === 'undefined') return null;
	const docCtx = (document as Document & { modelContext?: ModelContext }).modelContext;
	if (docCtx) return docCtx;
	const nav = navigator as Navigator & { modelContext?: NavModelContext };
	return nav.modelContext ?? null;
}

function currentPath(): string {
	return window.location.pathname + window.location.search + window.location.hash;
}

async function fetchGlossaryEntries(): Promise<
	Array<{
		term: string;
		suggestion?: string;
		translation?: string;
		notes?: string;
		status?: string;
	}>
> {
	try {
		const res = await fetch('/glossary.json', { credentials: 'same-origin' });
		if (!res.ok) return [];
		const data = (await res.json()) as { entries?: unknown[] };
		if (!Array.isArray(data.entries)) return [];
		return data.entries as Array<{
			term: string;
			suggestion?: string;
			translation?: string;
			notes?: string;
			status?: string;
		}>;
	} catch {
		return [];
	}
}

function toolDefs(): ModelContextTool[] {
	return [
		{
			name: 'get_site_info',
			title: 'Site info',
			description:
				'Return high-level information about Niksy (نیکسی): Persian Nix/NixOS documentation site name, title, description, and current URL.',
			inputSchema: {
				type: 'object',
				properties: {},
				additionalProperties: false
			},
			annotations: { readOnlyHint: true },
			execute: async () => ({
				name: SITE_NAME,
				title: SITE_TITLE,
				description: SITE_DESCRIPTION,
				url: window.location.href,
				path: currentPath(),
				language: 'fa'
			})
		},
		{
			name: 'get_current_page',
			title: 'Current page',
			description:
				'Return the current page path, full URL, and document title as shown in the browser.',
			inputSchema: {
				type: 'object',
				properties: {},
				additionalProperties: false
			},
			annotations: { readOnlyHint: true },
			execute: async () => ({
				url: window.location.href,
				path: currentPath(),
				title: document.title
			})
		},
		{
			name: 'list_sections',
			title: 'List main sections',
			description:
				'List the main documentation hubs on this site (home, how Nix works, nix.dev, Nix manual, Nixpkgs manual, Tour of Nix, glossary, settings, licenses).',
			inputSchema: {
				type: 'object',
				properties: {},
				additionalProperties: false
			},
			annotations: { readOnlyHint: true },
			execute: async () => ({
				sections: [
					{ href: '/', title: 'خانه (Home)' },
					{ href: '/pages/how-nix-works', title: 'چگونه Nix کار می‌کند' },
					{ href: '/pages/nix-dev', title: 'nix.dev (Persian)' },
					{ href: '/pages/nix-manual', title: 'راهنمای مرجع Nix' },
					{ href: '/pages/nixpkgs-manual', title: 'راهنمای Nixpkgs' },
					{ href: '/pages/tour-of-nix', title: 'تور نیکس (Tour of Nix)' },
					{ href: '/glossary', title: 'واژه‌نامه (Glossary)' },
					{ href: '/licenses', title: 'مجوزها (Licenses)' },
					{ href: '/settings', title: 'تنظیمات (Settings)' },
					{ href: '/.well-known/api-catalog', title: 'API catalog (RFC 9727)' },
					{
						href: '/.well-known/agent-skills/index.json',
						title: 'Agent Skills discovery index'
					},
					{ href: '/glossary.json', title: 'Glossary JSON feed' },
					{ href: '/sitemap.xml', title: 'Sitemap' }
				]
			})
		},
		{
			name: 'search_site',
			title: 'Search site',
			description:
				'Search Niksy documentation pages and navigation (Persian and English titles/paths). Returns matching pages with href, title, and group. Use navigate_to to open a result.',
			inputSchema: {
				type: 'object',
				properties: {
					query: {
						type: 'string',
						description: 'Search query (Persian or English keywords)'
					},
					limit: {
						type: 'integer',
						description: 'Max results (default 12, max 40)',
						minimum: 1,
						maximum: 40
					}
				},
				required: ['query'],
				additionalProperties: false
			},
			annotations: { readOnlyHint: true },
			execute: async (input) => {
				const query = String(input.query ?? '').trim();
				const limit = Math.min(40, Math.max(1, Number(input.limit) || 12));
				const hits = searchCommands(query, limit)
					.filter((i) => i.href)
					.map((i) => ({
						title: i.title,
						subtitle: i.subtitle ?? null,
						group: i.group,
						href: i.href,
						kind: i.kind
					}));
				return { query, count: hits.length, results: hits };
			}
		},
		{
			name: 'navigate_to',
			title: 'Navigate',
			description:
				'Navigate the browser to a site-relative path (e.g. /pages/nix-dev, /glossary, /pages/nix-manual/language/syntax). Prefer paths from search_site or list_sections.',
			inputSchema: {
				type: 'object',
				properties: {
					path: {
						type: 'string',
						description: 'Absolute path on this origin, starting with /'
					}
				},
				required: ['path'],
				additionalProperties: false
			},
			annotations: { readOnlyHint: false },
			execute: async (input) => {
				let path = String(input.path ?? '').trim();
				if (!path.startsWith('/')) {
					return { ok: false, error: 'path must start with /' };
				}
				// Block protocol-relative / external
				if (path.startsWith('//') || /:[/\\]/.test(path)) {
					return { ok: false, error: 'only same-origin paths are allowed' };
				}
				await goto(path);
				return { ok: true, path: currentPath(), title: document.title };
			}
		},
		{
			name: 'lookup_glossary',
			title: 'Lookup glossary',
			description:
				'Look up Nix/NixOS terminology in the Persian glossary. Matches term, suggestion, and translation fields. Returns matching entries.',
			inputSchema: {
				type: 'object',
				properties: {
					query: {
						type: 'string',
						description: 'English or Persian term to look up'
					},
					limit: {
						type: 'integer',
						description: 'Max entries (default 10, max 30)',
						minimum: 1,
						maximum: 30
					}
				},
				required: ['query'],
				additionalProperties: false
			},
			annotations: { readOnlyHint: true, untrustedContentHint: false },
			execute: async (input) => {
				const query = String(input.query ?? '').trim().toLowerCase();
				const limit = Math.min(30, Math.max(1, Number(input.limit) || 10));
				if (!query) return { query, count: 0, entries: [] };
				const entries = await fetchGlossaryEntries();
				const tokens = query.split(/\s+/).filter(Boolean);
				const hits = entries
					.filter((e) => {
						const hay = [e.term, e.suggestion, e.translation, e.notes]
							.filter(Boolean)
							.join(' ')
							.toLowerCase();
						return tokens.every((t) => hay.includes(t));
					})
					.slice(0, limit)
					.map((e) => ({
						term: e.term,
						suggestion: e.suggestion ?? '',
						translation: e.translation ?? '',
						notes: e.notes ?? '',
						status: e.status ?? ''
					}));
				return { query, count: hits.length, entries: hits };
			}
		},
		{
			name: 'get_page_markdown_hint',
			title: 'Markdown content negotiation hint',
			description:
				'Explain how agents can fetch the current page as Markdown via HTTP content negotiation (Accept: text/markdown), and return the current page URL for such a request.',
			inputSchema: {
				type: 'object',
				properties: {},
				additionalProperties: false
			},
			annotations: { readOnlyHint: true },
			execute: async () => ({
				url: window.location.href,
				acceptHeader: 'text/markdown',
				exampleCurl: `curl -H 'Accept: text/markdown' '${window.location.href}'`,
				note: 'Response Content-Type is text/markdown; charset=utf-8 when negotiation succeeds.'
			})
		}
	];
}

/**
 * Register WebMCP tools for the lifetime of the page. Returns a dispose fn
 * that aborts registration (unregisters tools when supported).
 */
export function registerWebMcpTools(): () => void {
	const ac = new AbortController();
	const { signal } = ac;

	void (async () => {
		const ctx = getModelContext();
		if (!ctx || signal.aborted) return;

		const tools = toolDefs();

		// Prefer imperative registerTool (current WebMCP draft)
		if (typeof ctx.registerTool === 'function') {
			for (const tool of tools) {
				if (signal.aborted) return;
				try {
					await ctx.registerTool(tool, { signal });
				} catch (err) {
					// API may reject if feature policy / secure context missing — non-fatal
					console.debug('[webmcp] registerTool failed', tool.name, err);
				}
			}
			return;
		}

		// Fallback: provideContext batch API (some scanners / early previews)
		if (typeof ctx.provideContext === 'function') {
			try {
				await ctx.provideContext({
					tools: tools.map((t) => ({
						name: t.name,
						description: t.description,
						inputSchema: t.inputSchema,
						execute: t.execute
					}))
				});
			} catch (err) {
				console.debug('[webmcp] provideContext failed', err);
			}
		}
	})();

	return () => ac.abort();
}
