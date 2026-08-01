<script lang="ts">
	import SeoHead from '$lib/components/SeoHead.svelte';
	import DevMdToolbar from '$lib/components/DevMdToolbar.svelte';
	import DevMdWysiwyg from '$lib/components/DevMdWysiwyg.svelte';
	import { page } from '$app/state';
	import { devMdIsActive } from '$lib/dev-md-edit.svelte';

	let { children } = $props();

	/** Per-slug SEO (extend when adding posts). */
	const metaByPath: Record<string, { title: string; description: string }> = {
		'/blog/do-not-be-afraid-of-ai': {
			title: 'از هوش مصنوعی نترسید',
			description:
				'هوش مصنوعی ترسناک نیست؛ با کنترل انسانی می‌توان از AI برای یادگیری و زندگی بهتر استفاده کرد.'
		},
		'/blog/how-we-build-this-website': {
			title: 'چگونه این وب‌سایت را ساختیم',
			description:
				'معماری نیکسی، ترجمه‌ی کنترل‌شده، واژه‌نامه، خط لولهٔ tools و ویرایشگر داخلی Ctrl+E.'
		}
	};

	function norm(p: string) {
		return p.replace(/\/$/, '') || '/';
	}

	const meta = $derived(
		metaByPath[norm(page.url.pathname)] ?? {
			title: 'وبلاگ نیکسی',
			description: 'یادداشت‌های نیکسی دربارهٔ Nix، NixOS و ابزارهای توسعه.'
		}
	);
</script>

<SeoHead title={meta.title} description={meta.description} />

<article
	class="prose prose-fa doc-page blog-page nd-article"
	class:nd-article--dev-edit={devMdIsActive(page.url.pathname)}
	data-no-panel
>
	{#if devMdIsActive(page.url.pathname)}
		<DevMdToolbar />
	{/if}
	<DevMdWysiwyg>
		{@render children()}
	</DevMdWysiwyg>
</article>
