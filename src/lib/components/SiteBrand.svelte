<script lang="ts">
	/** Shared site mark: grayscale Nix logo with blue «فا» centered on it · نیکسی */
	let {
		size = 'md'
	}: {
		size?: 'sm' | 'md' | 'lg';
	} = $props();
</script>

<span class="site-brand site-brand--{size}">
	<span class="site-brand__mark">
		<img
			class="site-brand__logo"
			src="/icons/nix-snowflake.svg"
			alt=""
			width="28"
			height="28"
			decoding="async"
		/>
		<span class="site-brand__fa">فا</span>
	</span>
	<span class="site-brand__name">نیکسی</span>
</span>

<style>
	.site-brand {
		display: inline-flex;
		align-items: center;
		gap: 0.45rem;
		font-family: var(--font-ui);
		line-height: 1;
		color: inherit;
	}

	.site-brand__mark {
		position: relative;
		display: inline-flex;
		flex-shrink: 0;
		width: 1.35em;
		height: 1.35em;
		align-items: center;
		justify-content: center;
	}

	.site-brand__logo {
		display: block;
		width: 100%;
		height: 100%;
		object-fit: contain;
		/* Grayscale snowflake */
		filter: grayscale(1) contrast(1.05);
		opacity: 0.72;
	}

	/* Blue «فا» dead-center on the logo */
	.site-brand__fa {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0;
		padding: 0;
		border: none;
		background: none;
		box-shadow: none;
		font-weight: 800;
		font-size: 0.42em;
		letter-spacing: 0;
		line-height: 1;
		color: var(--accent);
		/* Keep readable on the snowflake arms */
		text-shadow:
			0 0 0.12em var(--bg),
			0 0 0.18em var(--bg),
			0 0 0.28em var(--bg);
		pointer-events: none;
		user-select: none;
	}

	.site-brand__name {
		font-weight: inherit;
		letter-spacing: inherit;
		white-space: nowrap;
	}

	.site-brand--sm {
		font-size: 1rem;
		gap: 0.4rem;
		font-weight: 700;
	}

	.site-brand--sm .site-brand__mark {
		width: 1.55rem;
		height: 1.55rem;
	}

	.site-brand--sm .site-brand__fa {
		font-size: 0.55rem;
	}

	.site-brand--md {
		font-size: 1.05rem;
		font-weight: 700;
	}

	.site-brand--lg {
		font-size: clamp(2.35rem, 6.5vw, 3.25rem);
		font-weight: 800;
		letter-spacing: -0.03em;
		gap: 0.55rem;
	}

	.site-brand--lg .site-brand__mark {
		width: 0.95em;
		height: 0.95em;
	}

	.site-brand--lg .site-brand__fa {
		font-size: 0.32em;
	}
</style>
