<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let q = $state('');

	const filtered = $derived.by(() => {
		const query = q.trim().toLowerCase();
		if (!query) return data.entries;
		return data.entries.filter((e) => {
			const hay = `${e.term} ${e.translation}`.toLowerCase();
			return hay.includes(query);
		});
	});
</script>

<svelte:head>
	<title>واژه‌نامه · {data.count} واژه · نیکسی</title>
	<meta name="description" content="واژه‌نامهٔ تأییدشدهٔ اصطلاحات Nix / NixOS (انگلیسی ↔ فارسی)" />
	<meta property="og:title" content={`واژه‌نامه · ${data.count} واژه · نیکسی`} />
	<meta property="og:description" content="واژه‌نامهٔ تأییدشدهٔ اصطلاحات Nix / NixOS (انگلیسی ↔ فارسی)" />
	<meta name="twitter:title" content={`واژه‌نامه · ${data.count} واژه · نیکسی`} />
	<meta name="twitter:description" content="واژه‌نامهٔ تأییدشدهٔ اصطلاحات Nix / NixOS (انگلیسی ↔ فارسی)" />
</svelte:head>

<section class="eg">
	<header class="eg-head">
		<div class="eg-head__title">
			<h1>واژه‌نامه</h1>
			<span class="eg-pill" dir="ltr">{data.count} terms</span>
			<span class="eg-pill eg-pill--muted" dir="ltr">v{data.version}</span>
		</div>
		<p class="eg-lead">
			اصطلاحات تخصصی تأییدشدهٔ Nix و NixOS؛ انگلیسی ↔ فارسی.
		</p>
	</header>

	<div class="eg-bar">
		<input
			class="eg-search"
			type="search"
			placeholder="جستجو: term یا ترجمه…"
			bind:value={q}
			aria-label="جستجو در واژه‌نامه"
		/>
		<span class="eg-bar__count" dir="ltr">{filtered.length} / {data.count}</span>
	</div>

	<div class="eg-table-wrap">
		<table class="eg-table">
			<thead>
				<tr>
					<th class="c-idx">#</th>
					<th class="c-en">English</th>
					<th class="c-fa">فارسی</th>
				</tr>
			</thead>
			<tbody>
				{#each filtered as e, i (e.term)}
					<tr>
						<td class="c-idx" dir="ltr">{i + 1}</td>
						<td class="c-en" dir="ltr"><code class="term">{e.term}</code></td>
						<td class="c-fa" dir="auto">{e.translation}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	{#if filtered.length === 0}
		<p class="eg-empty">موردی با این جستجو پیدا نشد.</p>
	{/if}
</section>

<style>
	.eg {
		max-width: 52rem;
		margin: 0 auto;
		padding: 0.25rem 0 2rem;
	}

	.eg-head {
		margin-bottom: 1rem;
	}

	.eg-head__title {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.45rem 0.65rem;
		margin-bottom: 0.35rem;
	}

	.eg-head h1 {
		margin: 0;
		font-size: 1.45rem;
		font-weight: 800;
		letter-spacing: -0.02em;
	}

	.eg-pill {
		display: inline-flex;
		align-items: center;
		padding: 0.15rem 0.5rem;
		border-radius: 999px;
		font-size: 0.72rem;
		font-weight: 600;
		background: var(--bg-soft, #f3f4f6);
		border: 1px solid var(--line, #e5e7eb);
		color: var(--muted, #666);
	}

	.eg-pill--muted {
		opacity: 0.85;
	}

	.eg-lead {
		margin: 0;
		color: var(--text, #555);
		font-size: 0.95rem;
		line-height: 1.55;
	}

	.eg-bar {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.55rem;
		margin: 1rem 0 0.75rem;
	}

	.eg-search {
		flex: 1 1 14rem;
		min-width: 0;
		padding: 0.5rem 0.75rem;
		border: 1px solid var(--line, #e5e7eb);
		border-radius: 0.5rem;
		background: var(--bg, #fff);
		color: var(--fg, #111);
		font-family: var(--font-ui, inherit);
		font-size: 0.9rem;
	}

	.eg-search:focus {
		outline: none;
		border-color: #93c5fd;
		box-shadow: 0 0 0 3px #93c5fd33;
	}

	.eg-bar__count {
		font-size: 0.78rem;
		color: var(--muted, #666);
		font-variant-numeric: tabular-nums;
	}

	.eg-table-wrap {
		overflow-x: auto;
		border: 1px solid var(--line, #e5e7eb);
		border-radius: 0.65rem;
		background: var(--bg, #fff);
	}

	.eg-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}

	.eg-table th,
	.eg-table td {
		padding: 0.55rem 0.75rem;
		border-bottom: 1px solid var(--line, #e5e7eb);
		vertical-align: top;
	}

	.eg-table th {
		text-align: start;
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--muted, #666);
		background: var(--bg-soft, #f7f7f8);
		position: sticky;
		top: 0;
		z-index: 1;
	}

	.eg-table tbody tr:last-child td {
		border-bottom: none;
	}

	.eg-table tbody tr:hover {
		background: color-mix(in srgb, var(--bg-soft, #f3f4f6) 70%, transparent);
	}

	.c-idx {
		width: 2.5rem;
		color: var(--muted, #888);
		font-variant-numeric: tabular-nums;
		font-size: 0.8rem;
	}

	.c-en {
		width: 38%;
		min-width: 8rem;
	}

	.term {
		font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
		font-size: 0.86rem;
		padding: 0.1rem 0.35rem;
		border-radius: 0.3rem;
		background: var(--bg-soft, #f3f4f6);
		border: 1px solid var(--line, #e5e7eb);
		color: var(--fg, #111);
		word-break: break-word;
	}

	.c-fa {
		line-height: 1.55;
	}

	.eg-empty {
		margin: 1.25rem 0 0;
		text-align: center;
		color: var(--muted, #666);
	}
</style>
