<script lang="ts">
	import SeoHead from '$lib/components/SeoHead.svelte';
	import DevMdToolbar from '$lib/components/DevMdToolbar.svelte';
	import DevMdWysiwyg from '$lib/components/DevMdWysiwyg.svelte';
	import { page } from '$app/state';
	import { devMdIsActive } from '$lib/dev-md-edit.svelte';

	let { children } = $props();
</script>

<SeoHead
	title="سینتکس Markdown · تست"
	description="صفحهٔ نمونه‌ی کامل سینتکس Markdown این سایت (mdsvex، Prism، کادرهای اخطار، کارت‌های هاب)."
/>

<article
	class="prose prose-fa doc-page nd-article"
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
