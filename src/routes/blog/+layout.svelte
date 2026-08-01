<script lang="ts">
	import SeoHead from '$lib/components/SeoHead.svelte';
	import DevMdToolbar from '$lib/components/DevMdToolbar.svelte';
	import DevMdWysiwyg from '$lib/components/DevMdWysiwyg.svelte';
	import { page } from '$app/state';
	import { devMdIsActive } from '$lib/dev-md-edit.svelte';
	import { blogPostMetaByPath } from '$lib/blog-posts';

	let { children } = $props();

	function norm(p: string) {
		return p.replace(/\/$/, '') || '/';
	}

	const path = $derived(norm(page.url.pathname));
	const isIndex = $derived(path === '/blog');
	const isPost = $derived(!isIndex);

	const meta = $derived(
		blogPostMetaByPath[path] ?? {
			title: isIndex ? 'وبلاگ' : 'وبلاگ نیکسی',
			description: 'یادداشت‌های نیکسی دربارهٔ Nix، NixOS و ابزارهای توسعه.'
		}
	);
</script>

<SeoHead title={meta.title} description={meta.description} />

<article
	class="prose prose-fa doc-page blog-page nd-article"
	class:nd-article--dev-edit={devMdIsActive(page.url.pathname)}
	class:blog-page--index={isIndex}
	data-no-panel
>
	{#if isPost && devMdIsActive(page.url.pathname)}
		<DevMdToolbar />
	{/if}
	{#if isPost}
		<DevMdWysiwyg>
			{@render children()}
		</DevMdWysiwyg>
	{:else}
		{@render children()}
	{/if}
</article>
