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
	import navData from '$lib/nix-dev-nav.json';

	let { children } = $props();

	type NavPage = { route: string; title: string; section: string; rel: string };

	type NavNode =
		| { kind: 'link'; page: NavPage }
		| {
				kind: 'group';
				key: string;
				title: string;
				/** Section intro page for this group, if any */
				index: NavPage | null;
				/** All pages under the group (including index) */
				pages: NavPage[];
		  };

	const pages = navData.pages as NavPage[];

	const sectionLabel: Record<string, string> = {
		root: 'شروع',
		tutorials: 'آموزش‌ها',
		guides: 'راهنماها',
		concepts: 'مفاهیم',
		reference: 'مرجع',
		contributing: 'مشارکت',
		acknowledgements: 'سپاس',
		'first-steps': 'گام‌های نخستین'
	};

	/** Preferred top-level section order in the side nav. */
	const sectionOrder = [
		'root',
		'first-steps',
		'tutorials',
		'guides',
		'concepts',
		'reference',
		'contributing',
		'acknowledgements'
	];

	function sectionBase(sec: string) {
		return sec === 'root' ? '/pages/nix-dev' : `/pages/nix-dev/${sec}`;
	}

	function norm(path: string) {
		return path.replace(/\/$/, '') || '/';
	}

	/** From shared NO_PANEL_PATHS — exact match only */
	const isHubIndex = $derived(isNoPanelPath(page.url.pathname));

	/** Build flat + nested nodes for one top-level section. */
	function buildNodes(sec: string, items: NavPage[]): NavNode[] {
		const base = sectionBase(sec);
		const b = norm(base);
		const buckets = new Map<string, NavPage[]>();
		let indexPage: NavPage | null = null;

		for (const item of items) {
			const r = norm(item.route);
			if (r === b) {
				indexPage = item;
				continue;
			}
			if (!r.startsWith(b + '/')) {
				// unexpected path — still list it
				const orphanKey = r;
				if (!buckets.has(orphanKey)) buckets.set(orphanKey, []);
				buckets.get(orphanKey)!.push(item);
				continue;
			}
			const rest = r.slice(b.length + 1);
			const seg = rest.split('/')[0]!;
			if (!buckets.has(seg)) buckets.set(seg, []);
			buckets.get(seg)!.push(item);
		}

		const nodes: NavNode[] = [];
		if (indexPage) nodes.push({ kind: 'link', page: indexPage });

		const keys = [...buckets.keys()].sort((a, b) => a.localeCompare(b));
		for (const key of keys) {
			const group = buckets.get(key)!;
			const groupBase = `${b}/${key}`;
			const gIndex = group.find((p) => norm(p.route) === groupBase) ?? null;
			const deeper = group.filter((p) => norm(p.route) !== groupBase);
			if (deeper.length === 0) {
				// single leaf page
				const only = gIndex ?? group[0]!;
				nodes.push({ kind: 'link', page: only });
			} else {
				// nested accordion group
				const title = gIndex?.title ?? deeper[0]?.title ?? key;
				nodes.push({
					kind: 'group',
					key,
					title: cleanTitle(title),
					index: gIndex,
					pages: group
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
	/** Accordion: at most one top-level section open (`''` = all closed). */
	let openSection = $state<string | null>(null);
	/** Accordion: at most one nested group open within the open section (`sec/key`). */
	let openGroup = $state<string | null>(null);

	const currentPage = $derived.by(() => {
		const path = norm(page.url.pathname);
		return pages.find((p) => norm(p.route) === path) ?? null;
	});

	const currentTitle = $derived(currentPage?.title ?? 'فهرست');

	const currentSection = $derived.by(() => {
		if (currentPage?.section) return currentPage.section || 'root';
		return 'root';
	});

	/** Nested group key for the current route, if any. */
	const currentGroupKey = $derived.by(() => {
		if (!currentPage) return null;
		const sec = currentSection;
		const base = norm(sectionBase(sec));
		const r = norm(currentPage.route);
		if (r === base || !r.startsWith(base + '/')) return null;
		const rest = r.slice(base.length + 1);
		const seg = rest.split('/')[0]!;
		// only a "group" if there is deeper nesting or an index + children
		const secItems = pages.filter((p) => (p.section || 'root') === sec);
		const groupBase = `${base}/${seg}`;
		const hasDeeper = secItems.some((p) => {
			const pr = norm(p.route);
			return pr.startsWith(groupBase + '/');
		});
		return hasDeeper ? `${sec}/${seg}` : null;
	});

	function sourceFromRel(rel: string): { href: string; label: string } {
		let p = rel.replace(/\\/g, '/').replace(/\.fa\.md$/i, '.md');
		if (p === 'index.md' || p.endsWith('/index.md')) {
			p = p.replace(/\/?index\.md$/i, '');
		} else {
			p = p.replace(/\.md$/i, '');
		}
		const href = p ? `https://nix.dev/${p}.html` : 'https://nix.dev/';
		const label = p ? `nix.dev/${p}` : 'nix.dev';
		return { href, label };
	}

	const sourceLink = $derived.by(() => {
		if (currentPage?.rel) return sourceFromRel(currentPage.rel);
		const path = norm(page.url.pathname);
		const rest = path.replace(/^\/pages\/nix-dev\/?/, '');
		return rest
			? { href: `https://nix.dev/${rest}.html`, label: `nix.dev/${rest}` }
			: { href: 'https://nix.dev/', label: 'nix.dev' };
	});

	function cleanTitle(title: string) {
		return title
			// MyST label anchors left in titles by accident
			.replace(/<a\s+id="[^"]*"\s*><\/a>\s*/gi, '')
			.replace(/<[^>]+>/g, '')
			.replace(/`([^`]+)`/g, '$1')
			.replace(/\*\*([^*]+)\*\*/g, '$1')
			.replace(/\*([^*]+)\*/g, '$1')
			.trim();
	}

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

	/** Accordion toggle for top-level sections — only one open. */
	function toggleSection(sec: string) {
		const currently = openSection ?? currentSection;
		if (currently === sec) {
			openSection = '';
			openGroup = '';
		} else {
			openSection = sec;
			// keep/open the nested group only if it belongs to this section
			if (currentGroupKey?.startsWith(sec + '/')) {
				openGroup = currentGroupKey;
			} else {
				openGroup = '';
			}
		}
	}

	/** Accordion toggle for nested groups — only one open. */
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
		// Shift+J next · Shift+K prev (same as bottom pager) — skip while typing
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

	// Close drawer on route change; open only the section (+ nested group) for this page
	$effect(() => {
		const path = page.url.pathname;
		closeNav();
		openSection = currentSection;
		openGroup = currentGroupKey ?? '';
		void path;
	});

	// Avoid body scroll under the sheet on small screens
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
	<title>{currentTitle === 'فهرست' ? 'nix.dev فارسی · نیکسی' : `${currentTitle} · nix.dev · نیکسی`}</title>
	<meta
		name="description"
		content={currentTitle === 'فهرست'
			? 'ترجمه‌ی فارسی مستندات nix.dev — آموزش‌ها، مفاهیم و راهنماها.'
			: `${currentTitle} — از مستندات فارسی nix.dev در نیکسی.`}
	/>
	<meta
		property="og:title"
		content={currentTitle === 'فهرست' ? 'nix.dev فارسی · نیکسی' : `${currentTitle} · nix.dev · نیکسی`}
	/>
	<meta
		property="og:description"
		content={currentTitle === 'فهرست'
			? 'ترجمه‌ی فارسی مستندات nix.dev — آموزش‌ها، مفاهیم و راهنماها.'
			: `${currentTitle} — از مستندات فارسی nix.dev در نیکسی.`}
	/>
	<meta
		name="twitter:title"
		content={currentTitle === 'فهرست' ? 'nix.dev فارسی · نیکسی' : `${currentTitle} · nix.dev · نیکسی`}
	/>
</svelte:head>

<div class="nd" class:nd--nav-open={navOpen}>
	<button
		type="button"
		class="nd-nav-toggle"
		class:nd-nav-toggle--open={navOpen}
		aria-expanded={navOpen}
		aria-controls="nd-nav-panel"
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
		id="nd-nav-panel"
		class="nd-nav"
		class:is-open={navOpen}
		aria-label="فهرست nix.dev"
	>
		<div class="nd-nav__head">
			<p class="nd-nav__brand">
				<a href="/pages/nix-dev" onclick={closeNav}>nix.dev</a>
				<span class="nd-nav__count">{navData.count}</span>
			</p>
			<button type="button" class="nd-nav__close" aria-label="بستن" onclick={closeNav}>
				<Icon name="x" size={18} />
			</button>
		</div>
		<p class="nd-nav__src">
			<a href="https://nix.dev/" dir="ltr">
				منابع اصلی
				<Icon name="arrow-up-right" size={12} />
			</a>
		</p>
		<nav class="nd-nav__body">
			{#each sections as [sec, items, nodes]}
				{@const hasCurrent = items.some((item) => isCurrent(item.route))}
				{@const secOpen = isSectionOpen(sec)}
				<details
					class="nd-sec"
					class:nd-sec--active={hasCurrent}
					open={secOpen}
				>
					<summary
						class="nd-sec__summary"
						onclick={(e) => {
							e.preventDefault();
							toggleSection(sec);
						}}
					>
						<span
							class="nd-chev"
							class:nd-chev--open={secOpen}
							aria-hidden="true"
						></span>
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
										{node.page.title}
									</a>
								</li>
							{:else}
								{@const groupId = `${sec}/${node.key}`}
								{@const gOpen = isGroupOpen(groupId)}
								{@const gHasCurrent = node.pages.some((p) => isCurrent(p.route))}
								<li class="nd-subwrap">
									<details
										class="nd-sub"
										class:nd-sub--active={gHasCurrent}
										open={gOpen}
									>
										<summary
											class="nd-sub__summary"
											onclick={(e) => {
												e.preventDefault();
												e.stopPropagation();
												// ensure parent section stays open
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
														{node.index.title}
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
															{child.title}
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
		class:nd-article--hub={isHubIndex}
		class:nd-article--dev-edit={devMdIsActive(page.url.pathname)}
		data-no-panel={isHubIndex ? '' : undefined}
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
			git="https://github.com/NixOS/nix.dev"
			avatar="nixos"
		/>
	</article>
</div>
