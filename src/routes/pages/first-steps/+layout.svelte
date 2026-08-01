<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import DevMdToolbar from '$lib/components/DevMdToolbar.svelte';
	import DevMdWysiwyg from '$lib/components/DevMdWysiwyg.svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { devMdIsActive } from '$lib/dev-md-edit.svelte';

	let { children } = $props();

	const lessons = [
		{ href: '/pages/first-steps', label: 'فهرست', exact: true },
		{ href: '/pages/first-steps/ad-hoc-shell-environments', label: 'شل آنی' },
		{ href: '/pages/first-steps/reproducible-scripts', label: 'اسکریپت' },
		{ href: '/pages/first-steps/declarative-shell', label: 'شل اعلانی' },
		{ href: '/pages/first-steps/pinning-nixpkgs', label: 'سنجاق Nixpkgs' }
	];

	function isCurrent(href: string, exact = false) {
		const path = page.url.pathname.replace(/\/$/, '') || '/';
		const h = href.replace(/\/$/, '') || '/';
		if (exact) return path === h;
		return path === h || path.startsWith(h + '/');
	}

	const lessonIndex = $derived.by(() => {
		const path = page.url.pathname.replace(/\/$/, '') || '/';
		return lessons.findIndex((L) => {
			const h = L.href.replace(/\/$/, '') || '/';
			return path === h;
		});
	});

	function onKey(e: KeyboardEvent) {
		const t = e.target;
		if (t instanceof HTMLElement) {
			const tag = t.tagName;
			if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || t.isContentEditable)
				return;
		}
		if (!e.shiftKey || e.ctrlKey || e.metaKey || e.altKey) return;
		const k = e.key.toLowerCase();
		const i = lessonIndex;
		if (i < 0) return;
		if (k === 'j' && i < lessons.length - 1) {
			e.preventDefault();
			void goto(lessons[i + 1]!.href);
		} else if (k === 'k' && i > 0) {
			e.preventDefault();
			void goto(lessons[i - 1]!.href);
		}
	}
</script>

<svelte:window onkeydown={onKey} />

<svelte:head>
	<title>گام‌های نخستین · نیکسی</title>
</svelte:head>

<div class="lesson">
	<nav class="lesson__tabs" aria-label="درس‌ها">
		{#each lessons as item}
			<a
				href={item.href}
				aria-current={isCurrent(item.href, item.exact) ? 'page' : undefined}
			>
				{item.label}
			</a>
		{/each}
	</nav>

	<article class="prose prose-fa doc-page nd-article" class:nd-article--dev-edit={devMdIsActive(page.url.pathname)}>
		{#if devMdIsActive(page.url.pathname)}
			<DevMdToolbar />
		{/if}
		<DevMdWysiwyg>
			{@render children()}
		</DevMdWysiwyg>
	</article>

	<p class="lesson__src">
		منبع:
		<a href="https://nix.dev/tutorials/first-steps/" dir="ltr" class="lesson__ext">
			nix.dev/first-steps
			<Icon name="arrow-up-right" size={14} />
		</a>
	</p>
</div>
