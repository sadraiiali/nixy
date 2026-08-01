<script lang="ts">
	import { icons, type IconName } from '$lib/icons/registry';

	type Props = {
		name: IconName;
		/** CSS pixels */
		size?: number | string;
		class?: string;
		/** Flip horizontally in RTL (for “forward” arrows) */
		dir?: boolean;
		label?: string;
	};

	let {
		name,
		size = 18,
		class: className = '',
		dir = false,
		label
	}: Props = $props();

	const svg = $derived(icons[name] ?? '');
	const sizeCss = $derived(typeof size === 'number' ? `${size}px` : size);
</script>

{#if label}
	<span
		class="icon {className}"
		class:icon--dir={dir}
		style="--icon-size: {sizeCss}"
		role="img"
		aria-label={label}
	>
		{@html svg}
	</span>
{:else}
	<span class="icon {className}" class:icon--dir={dir} style="--icon-size: {sizeCss}" aria-hidden="true">
		{@html svg}
	</span>
{/if}
