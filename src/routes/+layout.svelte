<script lang="ts">
	import CommandPalette from '$lib/components/CommandPalette.svelte';
	import Icon from '$lib/components/Icon.svelte';
	import InAppPanel from '$lib/components/InAppPanel.svelte';
	import LinkCopyModal from '$lib/components/LinkCopyModal.svelte';
	import HelpAbout from '$lib/components/HelpAbout.svelte';
	import DevMdEditor from '$lib/components/DevMdEditor.svelte';
	import SiteBrand from '$lib/components/SiteBrand.svelte';
	import '../app.css';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { applyFontSize, readFontSize } from '$lib/font-size';
	import { applyFontFamily, readFontFamily } from '$lib/font-family';
	import { applyTheme, readTheme, watchSystemTheme } from '$lib/theme';
	import {
		inAppPanel,
		isEmbedContext,
		resolveInAppPanelHref
	} from '$lib/in-app-panel.svelte';
	import { enhanceExtLinkIcons } from '$lib/ext-link-icons';
	import { enhanceSamePageLinks } from '$lib/same-page-links';
	import { normalizeDocHref } from '$lib/normalize-doc-href';
	import { isExternalHref, isWebxdc } from '$lib/webxdc';
	import {
		FAVICON,
		SITE_DESCRIPTION,
		SITE_LOCALE,
		SITE_NAME,
		SITE_THEME_COLOR,
		SITE_TITLE,
		absoluteUrl
	} from '$lib/site-meta';
	import { registerWebMcpTools } from '$lib/webmcp';

	let { children } = $props();

	type NavItem = {
		href: string;
		label: string;
		icon: import('$lib/icons/registry').IconName;
		exact?: boolean;
		tip?: string;
	};

	/** Desktop header: icon-only + hover popover (no glossary — home card instead) */
	const navIcons: NavItem[] = [
		{ href: '/', label: 'خانه', icon: 'house', exact: true },
		{ href: '/pages/how-nix-works', label: 'چگونه کار می‌کند', icon: 'layers' },
		{ href: '/pages/nix-dev', label: 'nix.dev', icon: 'library' },
		{ href: '/pages/nix-manual', label: 'راهنمای Nix', icon: 'book-open' },
		{ href: '/pages/nixpkgs-manual', label: 'Nixpkgs', icon: 'layers' },
		{ href: '/pages/tour-of-nix', label: 'تور نیکس', icon: 'map' },
		{ href: '/settings', label: 'تنظیمات', icon: 'settings' }
	];

	/** Mobile drawer: same as desktop + glossary */
	const links: NavItem[] = [
		...navIcons.filter((i) => i.href !== '/settings'),
		{ href: '/glossary', label: 'واژه‌نامه', icon: 'book' },
		{ href: '/settings', label: 'تنظیمات', icon: 'settings' }
	];

	let menuOpen = $state(false);
	let linkModalOpen = $state(false);
	let linkModalHref = $state('');
	/** Ctrl/Cmd+K command palette */
	let cmdOpen = $state(false);
	/** iframe / forced embed after mount */
	let embedFrame = $state(false);
	let mainEl: HTMLElement | undefined = $state();
	/** Sticky header: hide while scrolling down; show at top / on scroll up */
	let headerHidden = $state(false);
	let lastScrollY = 0;



	/** searchParams is blocked during prerender — never throw in layout */
	function searchParam(name: string): string | null {
		try {
			return page.url.searchParams.get(name);
		} catch {
			return null;
		}
	}

	const embed = $derived(searchParam('embed') === '1' || embedFrame);
	const panelHref = $derived(inAppPanel.href);
	const panelOpen = $derived(panelHref != null && panelHref !== '');
	const panelSplit = $derived(inAppPanel.splitActive);
	const panelDrawer = $derived(inAppPanel.drawerActive);
	/** Home: brand in hero until scroll; then brand slides into sticky header */
	const isHome = $derived(
		(page.url.pathname.replace(/\/$/, '') || '/') === '/'
	);
	/** Absolute URLs for social previews (set PUBLIC_SITE_URL in production) */
	const canonicalUrl = $derived(absoluteUrl(page.url.pathname, page.url.origin));
	const ogImageUrl = $derived(absoluteUrl(FAVICON.ogImage, page.url.origin));
	/** Keep brand mounted while exit animation plays toward home / top of home */
	let brandVisible = $state(
		(page.url.pathname.replace(/\/$/, '') || '/') !== '/'
	);
	let brandLeaving = $state(false);
	/** Skip leave when first paint is already home (no prior brand) */
	let brandEverShown = $state(
		(page.url.pathname.replace(/\/$/, '') || '/') !== '/'
	);
	/** Home only: true once the in-page hero title has scrolled past the sticky bar */
	let homeHeroPast = $state(false);
	let brandLeaveTimer: ReturnType<typeof setTimeout> | null = null;

	function finishBrandLeave() {
		if (brandLeaveTimer) {
			clearTimeout(brandLeaveTimer);
			brandLeaveTimer = null;
		}
		brandVisible = false;
		brandLeaving = false;
	}

	function showBrandInHeader() {
		if (brandLeaveTimer) {
			clearTimeout(brandLeaveTimer);
			brandLeaveTimer = null;
		}
		brandVisible = true;
		brandLeaving = false;
		brandEverShown = true;
	}

	function startBrandLeave() {
		if (!brandVisible || brandLeaving) return;
		if (!brandEverShown) {
			brandVisible = false;
			return;
		}
		const reduce =
			typeof window !== 'undefined' &&
			window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		if (reduce) {
			finishBrandLeave();
			return;
		}
		brandLeaving = true;
		// Safety if animationend is skipped (tab background, etc.)
		brandLeaveTimer = setTimeout(finishBrandLeave, 220);
	}

	/** Non-home: always show brand. Home: show only after hero title scrolls past. */
	$effect(() => {
		if (!isHome) {
			homeHeroPast = false;
			showBrandInHeader();
			return;
		}
		if (homeHeroPast) {
			showBrandInHeader();
			return;
		}
		// At top of home — hide header brand (hero has it)
		if (!brandVisible || brandLeaving || !brandEverShown) {
			if (!brandEverShown) brandVisible = false;
			return;
		}
		startBrandLeave();
	});

	/** Watch home hero title vs sticky header — reveal brand when title leaves view */
	$effect(() => {
		if (!browser || !isHome) return;

		let io: IntersectionObserver | null = null;
		let raf = 0;

		const attach = () => {
			const title = document.querySelector('.home__title');
			if (!title) {
				// Hero not mounted yet (navigation) — try again next frame
				raf = requestAnimationFrame(attach);
				return;
			}
			const header = document.querySelector('.top') as HTMLElement | null;
			const headerH = Math.max(header?.offsetHeight ?? 56, 48);
			// Shrink root from the top by the sticky header so “past” means under the bar
			io = new IntersectionObserver(
				(entries) => {
					const e = entries[0];
					if (!e) return;
					// Not intersecting the area below the sticky header → scrolled past
					homeHeroPast = !e.isIntersecting;
				},
				{
					root: null,
					rootMargin: `-${headerH}px 0px 0px 0px`,
					threshold: 0
				}
			);
			io.observe(title);
			// Initial check (IO may not fire until next frame on some browsers)
			const rect = title.getBoundingClientRect();
			homeHeroPast = rect.bottom < headerH;
		};

		attach();

		return () => {
			if (raf) cancelAnimationFrame(raf);
			io?.disconnect();
		};
	});

	function onBrandAnimEnd(e: AnimationEvent) {
		if (!brandLeaving) return;
		if (e.animationName !== 'top-brand-out') return;
		finishBrandLeave();
	}

	function current(href: string, exact = false) {
		const path = page.url.pathname.replace(/\/$/, '') || '/';
		const h = href.replace(/\/$/, '') || '/';
		if (exact) return path === h;
		if (h === '/') return path === '/';
		return path === h || path.startsWith(h + '/');
	}

	function closeMenu() {
		menuOpen = false;
	}

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	/** Hide sticky header on scroll down; reveal at top or when scrolling up. */
	function onWindowScroll() {
		if (!browser) return;
		// Keep chrome visible while the mobile drawer is open
		if (menuOpen) {
			headerHidden = false;
			return;
		}
		const y = window.scrollY || document.documentElement.scrollTop || 0;
		const delta = y - lastScrollY;
		const nearTop = y < 8;
		if (nearTop) {
			headerHidden = false;
		} else if (delta > 4) {
			// scrolling down
			headerHidden = true;
		} else if (delta < -4) {
			// scrolling up
			headerHidden = false;
		}
		lastScrollY = y;
	}

	function onKey(e: KeyboardEvent) {
		// Ctrl/Cmd+K → command palette (also Ctrl+ن on Persian layout; physical KeyK)
		if (
			!embed &&
			(e.ctrlKey || e.metaKey) &&
			!e.altKey &&
			!e.shiftKey &&
			(e.key === 'k' || e.key === 'K' || e.key === 'ن' || e.code === 'KeyK')
		) {
			e.preventDefault();
			e.stopPropagation();
			cmdOpen = !cmdOpen;
			if (cmdOpen) closeMenu();
			return;
		}
		if (e.key === 'Escape' && menuOpen) closeMenu();
	}

	/**
	 * Capture-phase click routing (must run before SvelteKit’s router):
	 * 1) Webxdc external → copy modal
	 * 2) Embed iframe → keep navigations inside embed
	 * 3) Only *in-page body* links → side panel / drawer
	 */
	/**
	 * MyST docs link to foo.md — rewrite to SvelteKit routes (no .md)
	 * so panel + full navigation stay in-app.
	 */
	function rewriteDocLink(a: HTMLAnchorElement) {
		const raw = a.getAttribute('href');
		if (raw == null || raw === '') return;
		const next = normalizeDocHref(raw, page.url.href);
		if (next !== raw) {
			a.setAttribute('href', next);
		}
	}

	function onDocumentClick(e: MouseEvent) {
		if (!browser) return;
		if (e.button !== 0) return;
		if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

		const t = e.target;
		if (!(t instanceof Element)) return;

		// Dev edit context menu — leave alone
		if (t.closest('.dev-link-menu')) return;

		const a = t.closest('a');
		if (!a || !(a instanceof HTMLAnchorElement)) return;

		// Chrome / nav: default handling
		if (a.closest('[data-no-panel]')) return;

		// Strip .md before any routing / panel logic
		rewriteDocLink(a);

		const hrefAttr = a.getAttribute('href');

		if (isWebxdc && isExternalHref(hrefAttr)) {
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();
			linkModalHref = hrefAttr!.startsWith('//') ? `https:${hrefAttr}` : hrefAttr!;
			linkModalOpen = true;
			closeMenu();
			return;
		}

		// Same-page section links (#names-values): smooth scroll, never open panel
		if (smoothScrollSamePage(a, page.url.pathname, page.url.search)) {
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();
			return;
		}

		if (embed) {
			const next = resolveInAppPanelHref(a, page.url.pathname, page.url.search);
			if (!next) return;
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();
			try {
				const u = new URL(next, location.origin);
				u.searchParams.set('embed', '1');
				void goto(u.pathname + u.search + u.hash);
			} catch {
				void goto(next);
			}
			return;
		}

		const next = resolveInAppPanelHref(a, page.url.pathname, page.url.search);
		if (next) {
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();
			closeMenu();
			inAppPanel.openHref(next);
		}
		// External links: target=_blank from enhanceExtLinkIcons / rehype (new tab)
	}

	/** In-document #anchors → smooth scroll (TOC sections inside the same page). */
	function smoothScrollSamePage(
		a: HTMLAnchorElement,
		pathname: string,
		search: string
	): boolean {
		const raw = a.getAttribute('href');
		if (!raw) return false;

		let hash = '';
		let path = pathname;
		let q = search;

		if (raw.startsWith('#')) {
			hash = raw;
		} else {
			try {
				const u = new URL(raw, location.href);
				if (u.origin !== location.origin) return false;
				path = u.pathname;
				q = u.search;
				hash = u.hash;
			} catch {
				return false;
			}
		}

		if (!hash || hash === '#' || hash === '#top') return false;

		const norm = (p: string) => p.replace(/\/$/, '') || '/';
		if (norm(path) !== norm(pathname) || q !== search) return false;

		const id = decodeURIComponent(hash.slice(1));
		const el =
			document.getElementById(id) ||
			document.querySelector(`[id="${CSS.escape(id)}"]`) ||
			// Fallback: name= (older anchors) or [id] with unescaped lookup
			document.querySelector(`[name="${CSS.escape(id)}"]`);
		if (!el) return false;

		// Window is the real scroller (shell-main is not overflow:auto).
		// Offset a bit for the sticky header.
		const sticky = document.querySelector('.top') as HTMLElement | null;
		const offset = (sticky?.offsetHeight ?? 0) + 12;
		const y = el.getBoundingClientRect().top + window.scrollY - offset;
		window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });

		// Update URL hash without navigation / full jump
		try {
			const path = location.pathname + location.search + hash;
			history.replaceState(history.state, '', path);
		} catch {
			/* ignore */
		}
		return true;
	}

	// Keep scroll when entering/leaving split layout
	$effect(() => {
		const split = panelSplit;
		if (!browser) return;
		void split;
		inAppPanel.restoreScroll();
	});

	$effect(() => {
		page.url.pathname;
		closeMenu();
		// New route: show header again and resync scroll position
		headerHidden = false;
		if (browser) {
			lastScrollY = window.scrollY || document.documentElement.scrollTop || 0;
		}
	});

	// Stamp host icons + same-page section marks after each navigation
	$effect(() => {
		if (!browser) return;
		void page.url.pathname;
		void page.url.search;
		const run = () => {
			enhanceExtLinkIcons(document);
			enhanceSamePageLinks(document, page.url.pathname, page.url.search);
		};
		run();
		// mdsvex / panel content may settle a tick later
		const t = window.setTimeout(run, 50);
		const t2 = window.setTimeout(run, 200);
		return () => {
			clearTimeout(t);
			clearTimeout(t2);
		};
	});

	onMount(() => {
		if (!browser) return;
		applyFontSize(readFontSize());
		applyFontFamily(readFontFamily());
		applyTheme(readTheme());
		const stopThemeWatch = watchSystemTheme();
		// WebMCP: expose site tools to browser AI agents (no-op if API unsupported)
		const disposeWebMcp = registerWebMcpTools();
		embedFrame = isEmbedContext();
		inAppPanel.initWidth();
		inAppPanel.syncMode();
		enhanceExtLinkIcons(document);
		enhanceSamePageLinks(document, page.url.pathname, page.url.search);
		document.addEventListener('click', onDocumentClick, true);
		return () => {
			disposeWebMcp();
			stopThemeWatch();
			document.removeEventListener('click', onDocumentClick, true);
		};
	});
</script>

<!-- capture so Ctrl+K wins over page-level handlers / Monaco -->
<svelte:window onkeydowncapture={onKey} onscroll={onWindowScroll} />

<svelte:head>
	<!-- Brand: Nix snowflake logo as favicon (not default Svelte) -->
	<link rel="icon" href={FAVICON.svg} type="image/svg+xml" />
	<link rel="icon" href={FAVICON.ico} sizes="any" />
	<link rel="icon" href={FAVICON.png32} type="image/png" sizes="32x32" />
	<link rel="icon" href={FAVICON.png16} type="image/png" sizes="16x16" />
	<link rel="apple-touch-icon" href={FAVICON.apple} sizes="180x180" />
	<link rel="manifest" href={FAVICON.manifest} />
	<meta name="theme-color" content={SITE_THEME_COLOR} />
	<meta name="msapplication-TileColor" content={SITE_THEME_COLOR} />
	<meta name="msapplication-TileImage" content={FAVICON.icon192} />

	<title>{SITE_TITLE}</title>
	<meta name="description" content={SITE_DESCRIPTION} />
	<meta name="language" content="fa" />
	<meta name="application-name" content={SITE_NAME} />
	<link rel="canonical" href={canonicalUrl} />

	<!-- Open Graph (Telegram, Discord, LinkedIn, Facebook, …) -->
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:locale" content={SITE_LOCALE} />
	<meta property="og:title" content={SITE_TITLE} />
	<meta property="og:description" content={SITE_DESCRIPTION} />
	<meta property="og:url" content={canonicalUrl} />
	<meta property="og:image" content={ogImageUrl} />
	<meta property="og:image:type" content="image/png" />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />
	<meta property="og:image:alt" content={SITE_TITLE} />

	<!-- Twitter / X card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={SITE_TITLE} />
	<meta name="twitter:description" content={SITE_DESCRIPTION} />
	<meta name="twitter:image" content={ogImageUrl} />
	<meta name="twitter:image:alt" content={SITE_TITLE} />

	{#if embed}
		<meta name="robots" content="noindex" />
	{/if}
</svelte:head>

{#if embed}
	<div class="embed-shell">
		<main class="content embed-shell__content">
			{@render children()}
		</main>
	</div>
{:else}
	<div
		class="shell"
		class:menu-open={menuOpen}
		class:shell--split={panelSplit}
		class:shell--panel-open={panelOpen}
	>
		<!-- Stable chrome: never remount on panel open (preserves scroll) -->
		<div class="shell-work" class:shell-work--split={panelSplit}>
			{#if panelSplit}
				<div class="shell-split__panel" dir="ltr">
					<InAppPanel />
				</div>
			{/if}

			<div class="shell-main" class:shell-main--split={panelSplit} bind:this={mainEl} dir="rtl">
				{@render appChrome()}
			</div>
		</div>

		{#if panelDrawer}
			<InAppPanel />
		{/if}
	</div>
{/if}

{#if isWebxdc && !embed}
	<LinkCopyModal bind:open={linkModalOpen} href={linkModalHref} />
{/if}

{#if !embed}
	<CommandPalette bind:open={cmdOpen} />
	<HelpAbout />
	<DevMdEditor />
{/if}

{#snippet appChrome()}
	<header class="top" class:top--home={isHome && !brandVisible} class:top--hidden={headerHidden}>
		{#if brandVisible}
			<a
				class="top__brand"
				class:top__brand--enter={!brandLeaving}
				class:top__brand--leave={brandLeaving}
				href="/"
				data-no-panel
				onclick={closeMenu}
				onanimationend={onBrandAnimEnd}
				aria-label="نیکسی"
			>
				<SiteBrand size="sm" />
			</a>
		{/if}

		<nav class="top__nav top__nav--desktop" aria-label="اصلی" data-no-panel>
			{#each navIcons as item}
				<a
					class="top__icon-btn"
					href={item.href}
					aria-current={current(item.href, item.exact) ? 'page' : undefined}
					aria-label={item.label}
					data-tip={item.tip ?? item.label}
				>
					<Icon name={item.icon} size={18} />
				</a>
			{/each}
			<button
				type="button"
				class="top__icon-btn top__cmd"
				onclick={() => (cmdOpen = true)}
				aria-label="جستجو"
				data-tip="جستجو (Ctrl+K / Ctrl+ن)"
			>
				<Icon name="search" size={18} />
			</button>
		</nav>

		<button
			type="button"
			class="burger"
			aria-label={menuOpen ? 'بستن منو' : 'باز کردن منو'}
			aria-expanded={menuOpen}
			aria-controls="mobile-menu"
			onclick={toggleMenu}
		>
			{#if menuOpen}
				<Icon name="x" size={22} />
			{:else}
				<Icon name="menu" size={22} />
			{/if}
		</button>
	</header>

	<div id="mobile-menu" class="drawer" class:is-open={menuOpen} hidden={!menuOpen}>
		<nav class="drawer__nav" aria-label="منوی موبایل" data-no-panel>
			<button
				type="button"
				class="drawer__cmd"
				onclick={() => {
					closeMenu();
					cmdOpen = true;
				}}
			>
				<Icon name="search" size={20} />
				<span>جستجو</span>
			</button>
			{#each links as item}
				<a
					href={item.href}
					aria-current={current(item.href, item.exact) ? 'page' : undefined}
					onclick={closeMenu}
				>
					<Icon name={item.icon} size={20} />
					<span>{item.label}</span>
					<Icon name="arrow-right" size={18} dir class="drawer__arrow" />
				</a>
			{/each}
		</nav>
		<button type="button" class="drawer__close" onclick={closeMenu}>
			<Icon name="x" size={18} />
			<span>بستن</span>
		</button>
	</div>
	{#if menuOpen}
		<button type="button" class="drawer-backdrop" aria-label="بستن منو" onclick={closeMenu}
		></button>
	{/if}

	<main class="content">
		{@render children()}
	</main>

	<footer class="foot" data-no-panel>
		<span
			>نیکسی · یادداشت‌های فارسی Nix ·
			<a class="foot__link" href="/licenses">مجوزها و نسبت‌دهی</a>
			·
			<a
				class="foot__link"
				href="https://github.com/sadraiiali/nixy"
				target="_blank"
				rel="noopener noreferrer"
				>کد</a
			></span
		>
		<span class="foot__muted foot__credit">
			{#if isWebxdc}
				<span dir="ltr">Webxdc · offline</span>
			{:else}
				ساخته شده با
				<svg
					class="foot__heart"
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					width="12"
					height="12"
					aria-hidden="true"
					focusable="false"
				>
					<path
						fill="currentColor"
						d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
					/>
				</svg>
				+
				<a
					class="foot__ai-link"
					href="/blog/do-not-be-afraid-of-ai"
					title="از هوش مصنوعی نترسید — دربارهٔ ترجمه‌ی کنترل‌شده"
				>
					<svg
						class="foot__ai"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						width="14"
						height="14"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						aria-hidden="true"
						focusable="false"
					>
						<!-- robot -->
						<path d="M12 8V4H8" />
						<rect width="16" height="12" x="4" y="8" rx="2" />
						<path d="M2 14h2" />
						<path d="M20 14h2" />
						<path d="M15 13v2" />
						<path d="M9 13v2" />
					</svg>
				</a>
				توسط
				<a class="foot__link" href="https://a15d.at" target="_blank" rel="noopener noreferrer"
					>Alireza SadraiiRad</a
				>
			{/if}
		</span>
	</footer>
{/snippet}
