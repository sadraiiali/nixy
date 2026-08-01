<script lang="ts">
	import SeoHead from '$lib/components/SeoHead.svelte';

	let { children } = $props();
</script>

<SeoHead
	title="تور نیکس"
	description="درس‌های تعاملی زبان نیکس (Tour of Nix) — فارسی، با ویرایشگر و ارزیابی در مرورگر."
/>

<div class="ton-shell">
	{@render children()}
</div>
