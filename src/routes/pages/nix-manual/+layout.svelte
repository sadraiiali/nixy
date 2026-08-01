<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import DevMdToolbar from '$lib/components/DevMdToolbar.svelte';
	import DevMdWysiwyg from '$lib/components/DevMdWysiwyg.svelte';
	import PageSource from '$lib/components/PageSource.svelte';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { isNoPanelPath } from '$lib/no-panel-paths';
	import { devMdIsActive } from '$lib/dev-md-edit.svelte';
	import navData from '$lib/nix-manual-nav.json';

	let { children } = $props();

	type NavPage = {
		route: string;
		title: string;
		section: string;
		rel: string;
		source?: string;
	};

	type NavNode =
		| { kind: 'link'; page: NavPage }
		| {
				kind: 'group';
				key: string;
				title: string;
				index: NavPage | null;
				pages: NavPage[];
		  };

	const pages = navData.pages as NavPage[];
	const webBase =
		(navData as { webBase?: string }).webBase?.replace(/\/$/, '') ||
		'https://nix.dev/manual/nix/stable';

	const sectionLabel: Record<string, string> = {
		root: 'شروع',
		introduction: 'مقدمه',
		'quick-start': 'شروع سریع',
		installation: 'نصب',
		store: 'انبار',
		language: 'زبان Nix',
		'package-management': 'مدیریت بسته',
		'command-ref': 'مرجع دستورات',
		architecture: 'معماری',
		protocols: 'پروتکل‌ها',
		'advanced-topics': 'موضوعات پیشرفته',
		development: 'توسعه',
		glossary: 'واژه‌نامه',
		'c-api': 'C API'
	};

	const sectionOrder = [
		'root',
		'installation',
		'store',
		'language',
		'package-management',
		'command-ref',
		'architecture',
		'protocols',
		'advanced-topics',
		'development',
		'glossary',
		'c-api'
	];

	function sectionBase(sec: string) {
		return sec === 'root' ? '/pages/nix-manual' : `/pages/nix-manual/${sec}`;
	}

	function norm(path: string) {
		return path.replace(/\/$/, '') || '/';
	}

	function cleanTitle(title: string) {
		return title
			.replace(/<a\s+id="[^"]*"\s*><\/a>\s*/gi, '')
			.replace(/<[^>]+>/g, '')
			.replace(/`([^`]+)`/g, '$1')
			.replace(/\*\*([^*]+)\*\*/g, '$1')
			.replace(/\*([^*]+)\*/g, '$1')
			.trim();
	}

	function buildNodes(sec: string, items: NavPage[]): NavNode[] {
		const base = sectionBase(sec);
		const b = norm(base);

		// Root: flat list (home + top-level pages), keep publish order
		if (sec === 'root') {
			const nodes: NavNode[] = [];
			for (const item of items) {
				nodes.push({ kind: 'link', page: item });
			}
			return nodes;
		}

		const buckets = new Map<string, NavPage[]>();
		let indexPage: NavPage | null = null;

		for (const item of items) {
			const r = norm(item.route);
			if (r === b) {
				indexPage = item;
				continue;
			}
			if (!r.startsWith(b + '/')) {
				if (!buckets.has(r)) buckets.set(r, []);
				buckets.get(r)!.push(item);
				continue;
			}
			const rest = r.slice(b.length + 1);
			const seg = rest.split('/')[0]!;
			if (!buckets.has(seg)) buckets.set(seg, []);
			buckets.get(seg)!.push(item);
		}

		const nodes: NavNode[] = [];
		if (indexPage) nodes.push({ kind: 'link', page: indexPage });

		// Preserve SUMMARY / publish order within section
		const orderKeys: string[] = [];
		const seenKey = new Set<string>();
		for (const item of items) {
			const r = norm(item.route);
			if (indexPage && r === norm(indexPage.route)) continue;
			const key = r.startsWith(b + '/') ? r.slice(b.length + 1).split('/')[0]! : r;
			if (!seenKey.has(key)) {
				seenKey.add(key);
				orderKeys.push(key);
			}
		}

		for (const key of orderKeys) {
			const group = buckets.get(key);
			if (!group?.length) continue;
			const groupBase = `${b}/${key}`;
			const gIndex = group.find((p) => norm(p.route) === groupBase) ?? null;
			const deeper = group.filter((p) => norm(p.route) !== groupBase);
			if (deeper.length === 0) {
				nodes.push({ kind: 'link', page: gIndex ?? group[0]! });
			} else {
				const title = gIndex?.title ?? deeper[0]?.title ?? key;
				// keep child order as in items
				const orderedPages = items.filter((p) => group.includes(p));
				nodes.push({
					kind: 'group',
					key,
					title: cleanTitle(title),
					index: gIndex,
					pages: orderedPages.length ? orderedPages : group
				});
			}
		}
		return nodes;
	}

	const sections = $derived.by(() => {
		const map = new Map<string, NavPage[]>();
		for (const p of pages) {
			const s = p.section || 'root';
			if (!map.has(s)) map.set(s, []);
			map.get(s)!.push(p);
		}
		const ordered: [string, NavPage[], NavNode[]][] = [];
		const seen = new Set<string>();
		for (const sec of sectionOrder) {
			if (!map.has(sec)) continue;
			const items = map.get(sec)!;
			ordered.push([sec, items, buildNodes(sec, items)]);
			seen.add(sec);
		}
		for (const [sec, items] of map) {
			if (seen.has(sec)) continue;
			ordered.push([sec, items, buildNodes(sec, items)]);
		}
		return ordered;
	});

	let navOpen = $state(false);
	let openSection = $state<string | null>(null);
	let openGroup = $state<string | null>(null);

	const currentPage = $derived.by(() => {
		const path = norm(page.url.pathname);
		return pages.find((p) => norm(p.route) === path) ?? null;
	});

	const currentTitle = $derived(
		currentPage ? cleanTitle(currentPage.title) : 'راهنمای مرجع Nix'
	);

	const currentSection = $derived.by(() => {
		if (currentPage?.section) return currentPage.section || 'root';
		const path = norm(page.url.pathname);
		const rest = path.replace(/^\/pages\/nix-manual\/?/, '');
		if (!rest) return 'root';
		return rest.split('/')[0] || 'root';
	});

	const currentGroupKey = $derived.by(() => {
		if (!currentPage) return null;
		const sec = currentSection;
		if (sec === 'root') return null;
		const base = norm(sectionBase(sec));
		const r = norm(currentPage.route);
		if (r === base || !r.startsWith(base + '/')) return null;
		const rest = r.slice(base.length + 1);
		const seg = rest.split('/')[0]!;
		const secItems = pages.filter((p) => (p.section || 'root') === sec);
		const groupBase = `${base}/${seg}`;
		const hasDeeper = secItems.some((p) => norm(p.route).startsWith(groupBase + '/'));
		return hasDeeper ? `${sec}/${seg}` : null;
	});

	function sourceFromPage(p: NavPage | null): { href: string; label: string } {
		if (p?.source) {
			const href = p.source;
			const label = href.replace(/^https?:\/\//, '');
			return { href, label };
		}
		if (p?.rel) {
			let path = p.rel.replace(/\\/g, '/');
			if (path === 'SUMMARY.md' || path === 'index.md') {
				return { href: `${webBase}/`, label: webBase.replace(/^https?:\/\//, '') };
			}
			if (path.endsWith('/index.md')) {
				path = path.slice(0, -'/index.md'.length);
				const href = `${webBase}/${path}/`;
				return { href, label: href.replace(/^https?:\/\//, '') };
			}
			path = path.replace(/\.md$/i, '');
			const href = `${webBase}/${path}.html`;
			return { href, label: href.replace(/^https?:\/\//, '') };
		}
		const path = norm(page.url.pathname).replace(/^\/pages\/nix-manual\/?/, '');
		if (!path) return { href: `${webBase}/`, label: webBase.replace(/^https?:\/\//, '') };
		const href = `${webBase}/${path}.html`;
		return { href, label: href.replace(/^https?:\/\//, '') };
	}

	const sourceLink = $derived(sourceFromPage(currentPage));

	const pageIndex = $derived.by(() => {
		const path = norm(page.url.pathname);
		return pages.findIndex((p) => norm(p.route) === path);
	});

	const prevPage = $derived(pageIndex > 0 ? pages[pageIndex - 1]! : null);
	const nextPage = $derived(
		pageIndex >= 0 && pageIndex < pages.length - 1 ? pages[pageIndex + 1]! : null
	);

	function isCurrent(route: string) {
		return norm(page.url.pathname) === norm(route);
	}

	function isSectionOpen(sec: string) {
		const active = openSection ?? currentSection;
		return sec === active;
	}

	function isGroupOpen(groupId: string) {
		const active = openGroup ?? currentGroupKey;
		return active === groupId;
	}

	function toggleSection(sec: string) {
		const currently = openSection ?? currentSection;
		if (currently === sec) {
			openSection = '';
			openGroup = '';
		} else {
			openSection = sec;
			if (currentGroupKey?.startsWith(sec + '/')) {
				openGroup = currentGroupKey;
			} else {
				openGroup = '';
			}
		}
	}

	function toggleGroup(groupId: string) {
		const currently = openGroup ?? currentGroupKey;
		if (currently === groupId) {
			openGroup = '';
		} else {
			openGroup = groupId;
		}
	}

	function closeNav() {
		navOpen = false;
	}

	function toggleNav() {
		navOpen = !navOpen;
	}

	function isTypingTarget(t: EventTarget | null) {
		if (!(t instanceof HTMLElement)) return false;
		const tag = t.tagName;
		if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true;
		if (t.isContentEditable) return true;
		if (t.closest('.monaco-editor, [contenteditable="true"]')) return true;
		return false;
	}

	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			closeNav();
			return;
		}
		if (isTypingTarget(e.target)) return;
		if (!e.shiftKey || e.ctrlKey || e.metaKey || e.altKey) return;
		const k = e.key.toLowerCase();
		if (k === 'j' && nextPage) {
			e.preventDefault();
			void goto(nextPage.route);
		} else if (k === 'k' && prevPage) {
			e.preventDefault();
			void goto(prevPage.route);
		}
	}

	$effect(() => {
		const path = page.url.pathname;
		closeNav();
		openSection = currentSection;
		openGroup = currentGroupKey ?? '';
		void path;
	});

	$effect(() => {
		if (!browser) return;
		const wide = window.matchMedia('(min-width: 1594px)').matches;
		if (navOpen && !wide) {
			const prev = document.body.style.overflow;
			document.body.style.overflow = 'hidden';
			return () => {
				document.body.style.overflow = prev;
			};
		}
	});
</script>

<svelte:window onkeydown={onKey} />

<svelte:head>
	<title>{currentTitle} · راهنمای Nix · نیکسی</title>
	<meta name="description" content={`${currentTitle} — راهنمای مرجع Nix (فارسی) در نیکسی.`} />
	<meta property="og:title" content={`${currentTitle} · راهنمای Nix · نیکسی`} />
	<meta property="og:description" content={`${currentTitle} — راهنمای مرجع Nix (فارسی) در نیکسی.`} />
	<meta name="twitter:title" content={`${currentTitle} · راهنمای Nix · نیکسی`} />
</svelte:head>

<div class="nd" class:nd--nav-open={navOpen}>
	<button
		type="button"
		class="nd-nav-toggle"
		class:nd-nav-toggle--open={navOpen}
		aria-expanded={navOpen}
		aria-controls="nm-nav-panel"
		onclick={toggleNav}
	>
		<Icon name="menu" size={16} />
		<span class="nd-nav-toggle__label">{currentTitle}</span>
		<span class="nd-nav-toggle__count" dir="ltr">{navData.count}</span>
		<span class="nd-nav-toggle__action">
			{navOpen ? 'بستن' : 'فهرست'}
		</span>
	</button>

	{#if navOpen}
		<button
			type="button"
			class="nd-nav-backdrop"
			aria-label="بستن فهرست"
			onclick={closeNav}
		></button>
	{/if}

	<aside
		id="nm-nav-panel"
		class="nd-nav"
		class:is-open={navOpen}
		aria-label="فهرست راهنمای مرجع Nix"
	>
		<div class="nd-nav__head">
			<p class="nd-nav__brand">
				<a href="/pages/nix-manual" onclick={closeNav}>راهنمای Nix</a>
				<span class="nd-nav__count">{navData.count}</span>
			</p>
			<button type="button" class="nd-nav__close" aria-label="بستن" onclick={closeNav}>
				<Icon name="x" size={18} />
			</button>
		</div>
		<p class="nd-nav__src">
			<a href={webBase + '/'} dir="ltr" rel="noopener noreferrer" target="_blank">
				منبع اصلی
				<Icon name="arrow-up-right" size={12} />
			</a>
		</p>
		<nav class="nd-nav__body">
			{#each sections as [sec, items, nodes]}
				{@const hasCurrent = items.some((item) => isCurrent(item.route))}
				{@const secOpen = isSectionOpen(sec)}
				<details class="nd-sec" class:nd-sec--active={hasCurrent} open={secOpen}>
					<summary
						class="nd-sec__summary"
						onclick={(e) => {
							e.preventDefault();
							toggleSection(sec);
						}}
					>
						<span class="nd-chev" class:nd-chev--open={secOpen} aria-hidden="true"></span>
						<span class="nd-sec__title">{sectionLabel[sec] ?? sec}</span>
					</summary>
					<ul class="nd-sec__list">
						{#each nodes as node}
							{#if node.kind === 'link'}
								<li>
									<a
										href={node.page.route}
										aria-current={isCurrent(node.page.route) ? 'page' : undefined}
										onclick={closeNav}
									>
										{cleanTitle(node.page.title)}
									</a>
								</li>
							{:else}
								{@const groupId = `${sec}/${node.key}`}
								{@const gOpen = isGroupOpen(groupId)}
								{@const gHasCurrent = node.pages.some((p) => isCurrent(p.route))}
								<li class="nd-subwrap">
									<details class="nd-sub" class:nd-sub--active={gHasCurrent} open={gOpen}>
										<summary
											class="nd-sub__summary"
											onclick={(e) => {
												e.preventDefault();
												e.stopPropagation();
												openSection = sec;
												toggleGroup(groupId);
											}}
										>
											<span
												class="nd-chev nd-chev--sm"
												class:nd-chev--open={gOpen}
												aria-hidden="true"
											></span>
											<span class="nd-sub__title">{node.title}</span>
										</summary>
										<ul class="nd-sub__list">
											{#if node.index}
												<li>
													<a
														href={node.index.route}
														aria-current={isCurrent(node.index.route)
															? 'page'
															: undefined}
														onclick={closeNav}
													>
														{cleanTitle(node.index.title)}
													</a>
												</li>
											{/if}
											{#each node.pages as child}
												{#if !node.index || norm(child.route) !== norm(node.index.route)}
													<li>
														<a
															href={child.route}
															aria-current={isCurrent(child.route)
																? 'page'
																: undefined}
															onclick={closeNav}
														>
															{cleanTitle(child.title)}
														</a>
													</li>
												{/if}
											{/each}
										</ul>
									</details>
								</li>
							{/if}
						{/each}
					</ul>
				</details>
			{/each}
		</nav>
	</aside>

	<article
		class="prose prose-fa nd-article doc-page"
		class:nd-article--hub={isNoPanelPath(page.url.pathname)}
		class:nd-article--dev-edit={devMdIsActive(page.url.pathname)}
		data-no-panel={isNoPanelPath(page.url.pathname) ? '' : undefined}
	>
		{#if devMdIsActive(page.url.pathname)}
			<DevMdToolbar />
		{/if}
		<DevMdWysiwyg>
			{@render children()}
		</DevMdWysiwyg>

		{#if prevPage || nextPage}
			<nav class="nd-pager" aria-label="صفحه قبل و بعد">
				{#if prevPage}
					<a
						class="nd-pager__card nd-pager__card--prev"
						href={prevPage.route}
					>
						<span class="nd-pager__dir">
							<span class="nd-pager__icon" aria-hidden="true">
								<Icon name="arrow-right" size={16} />
							</span>
							قبلی
						</span>
						<span class="nd-pager__title">{cleanTitle(prevPage.title)}</span>
						{#if sectionLabel[prevPage.section]}
							<span class="nd-pager__sec">{sectionLabel[prevPage.section]}</span>
						{/if}
					</a>
				{:else}
					<span class="nd-pager__card nd-pager__card--empty" aria-hidden="true"></span>
				{/if}

				{#if nextPage}
					<a
						class="nd-pager__card nd-pager__card--next"
						href={nextPage.route}
					>
						<span class="nd-pager__dir">
							بعدی
							<span class="nd-pager__icon" aria-hidden="true">
								<Icon name="arrow-left" size={16} />
							</span>
						</span>
						<span class="nd-pager__title">{cleanTitle(nextPage.title)}</span>
						{#if sectionLabel[nextPage.section]}
							<span class="nd-pager__sec">{sectionLabel[nextPage.section]}</span>
						{/if}
					</a>
				{:else}
					<span class="nd-pager__card nd-pager__card--empty" aria-hidden="true"></span>
				{/if}
			</nav>
		{/if}

		<PageSource
			href={sourceLink.href}
			label={sourceLink.label}
			git="https://github.com/NixOS/nix"
			avatar="nixos"
		/>
	</article>
</div>
