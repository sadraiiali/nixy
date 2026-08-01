<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';

	/** Fixed blog URL for the AI translation write-up */
	const href = '/blog/do-not-be-afraid-of-ai';
</script>

<aside class="ai-gen-notice" data-no-panel>
	<a class="ai-gen-notice__link" href={href}>
		<span class="ai-gen-notice__icon" aria-hidden="true">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				width="18"
				height="18"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<!-- robot / bot -->
				<path d="M12 8V4H8" />
				<rect width="16" height="12" x="4" y="8" rx="2" />
				<path d="M2 14h2" />
				<path d="M20 14h2" />
				<path d="M15 13v2" />
				<path d="M9 13v2" />
			</svg>
		</span>
		<span class="ai-gen-notice__body">
			<span class="ai-gen-notice__title">این صفحه با کمک هوش مصنوعی تولید شده است</span>
			<span class="ai-gen-notice__hint">
				ترجمه‌ی کنترل‌شده، نه ترجمه‌ی خام · از هوش مصنوعی نترسید
			</span>
		</span>
		<span class="ai-gen-notice__chev" aria-hidden="true">
			<Icon name="arrow-right" size={16} dir />
		</span>
	</a>
</aside>
