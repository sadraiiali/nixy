/**
 * Frontend-only command palette index + search.
 * Built from static nav JSONs and chrome links (no network).
 */
import nixDevNav from '$lib/nix-dev-nav.json';
import nixManualNav from '$lib/nix-manual-nav.json';
import nixpkgsManualNav from '$lib/nixpkgs-manual-nav.json';
import tourOfNixNav from '$lib/tour-of-nix-nav.json';
/** SPA lesson ids (`?id=`) — path + topic only; written by tools.publish.tour_fa_json */
import tourLessons from '$lib/tour-of-nix-lessons.json';
import type { IconName } from '$lib/icons/registry';

export type CommandKind = 'nav' | 'page' | 'action';

export type CommandItem = {
	id: string;
	/** Display title (Farsi / English) */
	title: string;
	/** Secondary line (path or group) */
	subtitle?: string;
	/** Group label for UI */
	group: string;
	kind: CommandKind;
	/** Optional Lucide icon name */
	icon?: IconName;
	/** Navigate target (path + optional query) */
	href?: string;
	/** Optional action key handled by palette host */
	action?:
		| 'close-panel'
		| 'settings'
		| 'home'
		| 'theme-light'
		| 'theme-dark'
		| 'theme-system'
		| 'share-page';
	/** Precomputed lowercase haystack for search */
	search: string;
};

function cleanTitle(t: string): string {
	return t
		.replace(/<a\s+id="[^"]*"\s*><\/a>\s*/gi, '')
		.replace(/<[^>]+>/g, '')
		.replace(/`([^`]+)`/g, '$1')
		.replace(/\*\*([^*]+)\*\*/g, '$1')
		.replace(/\*([^*]+)\*/g, '$1')
		.replace(/\s+/g, ' ')
		.trim();
}

function normPath(p: string): string {
	return p.replace(/\/$/, '') || '/';
}

function haystack(...parts: (string | undefined)[]): string {
	return parts
		.filter(Boolean)
		.join(' ')
		.toLowerCase()
		.normalize('NFKD');
}

/** Static chrome destinations */
const CHROME: { href: string; title: string; group: string }[] = [
	{ href: '/', title: 'خانه', group: 'ناوبری' },
	{ href: '/pages/how-nix-works', title: 'چگونه Nix کار می‌کند', group: 'ناوبری' },
	{ href: '/pages/nix-dev', title: 'nix.dev', group: 'ناوبری' },
	{ href: '/pages/nix-manual', title: 'راهنمای مرجع Nix', group: 'ناوبری' },
	{ href: '/pages/nixpkgs-manual', title: 'راهنمای Nixpkgs', group: 'ناوبری' },
	{ href: '/pages/tour-of-nix', title: 'تور نیکس', group: 'ناوبری' },
	{ href: '/glossary', title: 'واژه‌نامه', group: 'ناوبری' },
	{ href: '/blog/do-not-be-afraid-of-ai', title: 'از هوش مصنوعی نترسید', group: 'ناوبری' },
	{
		href: '/blog/how-we-build-this-website',
		title: 'چگونه این وب‌سایت را ساختیم',
		group: 'ناوبری'
	},
	{ href: '/settings', title: 'تنظیمات', group: 'ناوبری' },
	{ href: '/licenses', title: 'مجوزها و نسبت‌دهی', group: 'ناوبری' }
];

function buildIndex(): CommandItem[] {
	const items: CommandItem[] = [];
	const seen = new Set<string>();

	const push = (item: Omit<CommandItem, 'search'> & { search?: string }) => {
		const id = item.id;
		if (seen.has(id)) return;
		seen.add(id);
		const search =
			item.search ??
			haystack(item.title, item.subtitle, item.group, item.href);
		items.push({ ...item, search });
	};

	for (const c of CHROME) {
		push({
			id: `nav:${c.href}`,
			title: c.title,
			subtitle: c.href,
			group: c.group,
			kind: 'nav',
			href: c.href
		});
	}

	// Actions
	push({
		id: 'action:close-panel',
		title: 'بستن پنل کناری',
		subtitle: 'بستن پیش‌نمایش صفحه',
		group: 'عمل‌ها',
		kind: 'action',
		action: 'close-panel'
	});
	push({
		id: 'action:share-page',
		title: 'اشتراک‌گذاری این صفحه',
		subtitle: 'کپی لینک یا ارسال در شبکه‌های اجتماعی',
		group: 'عمل‌ها',
		kind: 'action',
		icon: 'share-2',
		action: 'share-page',
		search: haystack(
			'اشتراک‌گذاری این صفحه',
			'اشتراک گذاری',
			'اشتراک',
			'share',
			'share page',
			'copy link',
			'کپی لینک',
			'واتس‌اپ',
			'whatsapp',
			'telegram',
			'تلگرام',
			'twitter',
			'ایکس'
		)
	});

	// Theme (appearance) — snappy palette names + EN/FA search tokens
	push({
		id: 'action:theme-light',
		title: 'نور روز',
		subtitle: 'Light mode · پوسته روشن',
		group: 'ظاهر',
		kind: 'action',
		icon: 'sun',
		action: 'theme-light',
		search: haystack(
			'نور روز',
			'light mode',
			'light',
			'theme light',
			'appearance light',
			'پوسته روشن',
			'حالت روشن',
			'روشن',
			'day',
			'daylight'
		)
	});
	push({
		id: 'action:theme-dark',
		title: 'شب‌نما',
		subtitle: 'Dark mode · پوسته تاریک',
		group: 'ظاهر',
		kind: 'action',
		icon: 'moon',
		action: 'theme-dark',
		search: haystack(
			'شب‌نما',
			'dark mode',
			'dark',
			'theme dark',
			'appearance dark',
			'پوسته تاریک',
			'حالت تاریک',
			'تاریک',
			'night'
		)
	});
	push({
		id: 'action:theme-system',
		title: 'هم‌سو با سیستم',
		subtitle: 'System theme · خودکار',
		group: 'ظاهر',
		kind: 'action',
		icon: 'monitor',
		action: 'theme-system',
		search: haystack(
			'هم‌سو با سیستم',
			'system theme',
			'system',
			'auto theme',
			'appearance system',
			'پوسته سیستم',
			'خودکار',
			'system'
		)
	});

	type NavPage = { route: string; title: string; section?: string; rel?: string };

	const sectionLabel: Record<string, string> = {
		root: 'شروع',
		tutorials: 'آموزش‌ها',
		guides: 'راهنماها',
		reference: 'مرجع',
		concepts: 'مفاهیم',
		contributing: 'مشارکت',
		'first-steps': 'گام‌های نخستین'
	};

	for (const p of nixDevNav.pages as NavPage[]) {
		const route = normPath(p.route);
		const title = cleanTitle(p.title);
		const sec = p.section || 'root';
		push({
			id: `page:${route}`,
			title,
			subtitle: route,
			group: `nix.dev · ${sectionLabel[sec] ?? sec}`,
			kind: 'page',
			href: route
		});
	}

	for (const p of nixManualNav.pages as NavPage[]) {
		const route = normPath(p.route);
		const title = cleanTitle(p.title);
		push({
			id: `page:${route}`,
			title,
			subtitle: route,
			group: 'راهنمای Nix',
			kind: 'page',
			href: route
		});
	}

	for (const p of (nixpkgsManualNav as { pages?: NavPage[] }).pages ?? []) {
		const route = normPath(p.route);
		const title = cleanTitle(p.title);
		push({
			id: `page:${route}`,
			title,
			subtitle: route,
			group: 'راهنمای Nixpkgs',
			kind: 'page',
			href: route
		});
	}

	// Tour lessons: SPA uses ?id=<path> (src/lib/tour-of-nix-lessons.json)
	type TourLesson = { path: string; topic: string };
	const tourList = tourLessons as TourLesson[];
	if (Array.isArray(tourList) && tourList.length) {
		for (const L of tourList) {
			const href = `/pages/tour-of-nix?id=${encodeURIComponent(L.path)}`;
			push({
				id: `tour:${L.path}`,
				title: cleanTitle(L.topic || L.path),
				subtitle: href,
				group: 'تور نیکس',
				kind: 'page',
				href,
				search: haystack(L.topic, L.path, 'تور', 'tour')
			});
		}
	} else {
		// fallback to published nav routes
		for (const p of tourOfNixNav.pages as NavPage[]) {
			const route = normPath(p.route);
			push({
				id: `tour:${route}`,
				title: cleanTitle(p.title),
				subtitle: route,
				group: 'تور نیکس',
				kind: 'page',
				href: route
			});
		}
	}

	return items;
}

let cached: CommandItem[] | null = null;

export function getCommandIndex(): CommandItem[] {
	if (!cached) cached = buildIndex();
	return cached;
}

/**
 * Simple frontend fuzzy-ish filter: all query tokens must appear in haystack.
 * Rank: title prefix > title includes > path includes > rest.
 */
export function searchCommands(query: string, limit = 40): CommandItem[] {
	const all = getCommandIndex();
	const q = query.trim().toLowerCase().normalize('NFKD');
	if (!q) {
		// default: actions first (share, theme, …), then chrome nav
		const actions = all.filter((i) => i.kind === 'action');
		const nav = all.filter((i) => i.kind === 'nav');
		return [...actions, ...nav].slice(0, 16);
	}

	const tokens = q.split(/\s+/).filter(Boolean);
	type Scored = { item: CommandItem; score: number };
	const scored: Scored[] = [];

	for (const item of all) {
		const h = item.search;
		if (!tokens.every((t) => h.includes(t))) continue;

		const title = item.title.toLowerCase();
		const sub = (item.subtitle ?? '').toLowerCase();
		let score = 0;
		if (title.startsWith(q)) score += 100;
		else if (title.includes(q)) score += 60;
		if (tokens.every((t) => title.includes(t))) score += 40;
		if (sub.includes(q)) score += 20;
		// shorter titles a bit higher
		score += Math.max(0, 20 - Math.min(20, title.length / 4));
		scored.push({ item, score });
	}

	scored.sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title, 'fa'));
	return scored.slice(0, limit).map((s) => s.item);
}
