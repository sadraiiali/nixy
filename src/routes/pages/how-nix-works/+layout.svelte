<script lang="ts">
	import SeoHead from '$lib/components/SeoHead.svelte';
	import DevMdToolbar from '$lib/components/DevMdToolbar.svelte';
	import DevMdWysiwyg from '$lib/components/DevMdWysiwyg.svelte';
	import PageSource from '$lib/components/PageSource.svelte';
	import { page } from '$app/state';
	import { devMdIsActive } from '$lib/dev-md-edit.svelte';

	let { children } = $props();
</script>

<SeoHead
	title="نیکس چگونه کار می‌کند"
	description="راهنمای فارسی «نیکس چگونه کار می‌کند» مدیریت بستهٔ تابعی خالص، انبار نیکس، بازگردانی و NixOS."
/>

<article class="prose prose-fa doc-page nd-article" class:nd-article--dev-edit={devMdIsActive(page.url.pathname)}>
	{#if devMdIsActive(page.url.pathname)}
		<DevMdToolbar />
	{/if}
	<DevMdWysiwyg>
		{@render children()}
	</DevMdWysiwyg>

	<PageSource
		href="https://nixos.org/guides/how-nix-works/"
		label="nixos.org/guides/how-nix-works"
		git="https://github.com/NixOS/nix"
		avatar="nixos"
	/>
</article>
