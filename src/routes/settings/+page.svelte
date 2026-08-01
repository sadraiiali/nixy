<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import Icon from '$lib/components/Icon.svelte';
	import {
		FONT_DEFAULT,
		FONT_MAX,
		FONT_MIN,
		applyFontSize,
		readFontSize
	} from '$lib/font-size';
	import {
		FONT_FAMILIES,
		FONT_FAMILY_DEFAULT,
		applyFontFamily,
		readFontFamily,
		type FontFamilyId
	} from '$lib/font-family';
	import {
		THEMES,
		THEME_DEFAULT,
		applyTheme,
		readTheme,
		resolveTheme,
		watchSystemTheme,
		type ThemeId
	} from '$lib/theme';

	let fontSize = $state(FONT_DEFAULT);
	let fontFamily = $state<FontFamilyId>(FONT_FAMILY_DEFAULT);
	let theme = $state<ThemeId>(THEME_DEFAULT);
	let themeResolved = $state<'light' | 'dark'>('light');
	let savedFlash = $state(false);

	function flashSaved() {
		savedFlash = true;
		setTimeout(() => {
			savedFlash = false;
		}, 900);
	}

	/** Root size in px; 1rem = this value everywhere. */
	function setSize(px: number) {
		fontSize = applyFontSize(px);
		flashSaved();
	}

	function setFamily(id: FontFamilyId) {
		fontFamily = applyFontFamily(id);
		flashSaved();
	}

	function setTheme(id: ThemeId) {
		theme = applyTheme(id);
		themeResolved = resolveTheme(theme);
		flashSaved();
	}

	function preset(kind: 'sm' | 'md' | 'lg') {
		if (kind === 'sm') setSize(14);
		else if (kind === 'md') setSize(16);
		else setSize(19);
	}

	onMount(() => {
		if (!browser) return;
		fontSize = readFontSize();
		fontFamily = readFontFamily();
		theme = readTheme();
		applyFontFamily(fontFamily);
		applyTheme(theme);
		themeResolved = resolveTheme(theme);
		return watchSystemTheme((resolved) => {
			if (readTheme() === 'system') {
				themeResolved = resolved;
			}
		});
	});
</script>

<svelte:head>
	<title>تنظیمات · نیکسی</title>
	<meta name="description" content="تنظیمات نمایش نیکسی: تم، اندازهٔ قلم، خانوادهٔ فونت." />
	<meta property="og:title" content="تنظیمات · نیکسی" />
	<meta name="twitter:title" content="تنظیمات · نیکسی" />
	<meta name="robots" content="noindex" />
</svelte:head>

<section class="settings-page">
	<header class="settings-page__head">
		<h1>
			<Icon name="settings" size={28} class="settings-page__hicon" />
			تنظیمات
		</h1>
		<p class="settings-page__lead">
			پوسته، فونت و اندازهٔ پایه. ظاهر با متغیرهای CSS اعمال می‌شود و در
			مرورگر شما ذخیره می‌گردد.
		</p>
	</header>

	<div class="settings-page__card">
		<div class="settings-page__row">
			<span class="settings-page__label">
				<Icon name="eye" size={16} />
				پوسته (تم)
			</span>
			<span class="settings-page__px" dir="ltr">
				{THEMES.find((t) => t.id === theme)?.labelEn ?? theme}
				{#if theme === 'system'}
					· {themeResolved}
				{/if}
			</span>
		</div>

		<div class="settings-page__themes" role="radiogroup" aria-label="انتخاب پوسته">
			{#each THEMES as t}
				<button
					type="button"
					class="settings-page__theme-opt"
					class:is-active={theme === t.id}
					class:is-light={t.id === 'light' || (t.id === 'system' && themeResolved === 'light')}
					class:is-dark={t.id === 'dark' || (t.id === 'system' && themeResolved === 'dark')}
					role="radio"
					aria-checked={theme === t.id}
					onclick={() => setTheme(t.id)}
				>
					<span class="settings-page__theme-swatch" aria-hidden="true">
						<span class="settings-page__theme-swatch-bg"></span>
						<span class="settings-page__theme-swatch-fg"></span>
						<span class="settings-page__theme-swatch-accent"></span>
					</span>
					<span class="settings-page__theme-name">{t.label}</span>
					<span class="settings-page__theme-en" dir="ltr">{t.labelEn}</span>
					<span class="settings-page__theme-hint">{t.hint}</span>
				</button>
			{/each}
		</div>
	</div>

	<div class="settings-page__card">
		<div class="settings-page__row">
			<span class="settings-page__label">
				<Icon name="type" size={16} />
				فونت
			</span>
			<span class="settings-page__px" dir="ltr">
				{FONT_FAMILIES.find((f) => f.id === fontFamily)?.labelEn ?? fontFamily}
			</span>
		</div>

		<div class="settings-page__fonts" role="radiogroup" aria-label="انتخاب فونت">
			{#each FONT_FAMILIES as fam}
				<button
					type="button"
					class="settings-page__font-opt"
					class:is-active={fontFamily === fam.id}
					role="radio"
					aria-checked={fontFamily === fam.id}
					style:font-family={fam.stack}
					onclick={() => setFamily(fam.id)}
				>
					<span class="settings-page__font-name">{fam.label}</span>
					<span class="settings-page__font-en" dir="ltr">{fam.labelEn}</span>
					<span class="settings-page__font-preview">بسته، انبار Nix، ۱۲۳</span>
				</button>
			{/each}
		</div>
	</div>

	<div class="settings-page__card">
		<div class="settings-page__row">
			<span class="settings-page__label">
				<Icon name="type" size={16} />
				ROOT / 1rem
			</span>
			<span class="settings-page__px" dir="ltr">{fontSize}px = 1rem</span>
		</div>

		<input
			class="settings-page__range"
			type="range"
			min={FONT_MIN}
			max={FONT_MAX}
			step="1"
			value={fontSize}
			aria-label="اندازه پایه قلم به پیکسل (۱rem)"
			oninput={(e) => setSize(Number((e.currentTarget as HTMLInputElement).value))}
		/>

		<div class="settings-page__presets">
			<button type="button" class="blk-btn" onclick={() => preset('sm')}>کوچک ۱۴px</button>
			<button type="button" class="blk-btn" onclick={() => preset('md')}>متوسط ۱۶px</button>
			<button type="button" class="blk-btn" onclick={() => preset('lg')}>بزرگ ۱۹px</button>
		</div>

		<div class="settings-page__scale" dir="ltr">
			<p><strong>body</strong> 0.875rem / 1.5rem</p>
			<p><strong>h1</strong> 2rem / 3.25rem</p>
			<p><strong>h2</strong> 1.25rem / 2rem</p>
			<p><strong>h3</strong> 1.125rem / 1.75rem</p>
		</div>

		{#if savedFlash}
			<p class="settings-page__saved" role="status">
				<Icon name="circle-check" size={16} />
				ذخیره شد.
			</p>
		{/if}

		<p class="settings-page__sample">
			نمونه: بسته، انبار Nix، بازگردانی، متن فارسی با فونت و اندازهٔ فعلی.
		</p>
		<p class="settings-page__sample settings-page__sample--h">
			نمونهٔ عنوان (سبک h2)
		</p>
	</div>

	<p class="settings-page__back">
		<a href="/">
			<Icon name="arrow-left" size={18} dir />
			<span>بازگشت به خانه</span>
		</a>
	</p>
</section>

<style>
	.settings-page__themes {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.65rem;
		margin-top: 0.35rem;
	}

	.settings-page__theme-opt {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.15rem;
		padding: 0.75rem 0.85rem;
		border: 1px solid var(--line);
		border-radius: var(--radius);
		background: var(--bg-soft);
		color: var(--fg);
		cursor: pointer;
		text-align: start;
		transition:
			border-color 0.15s ease,
			box-shadow 0.15s ease,
			background 0.15s ease;
	}

	.settings-page__theme-opt:hover {
		border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
		background: var(--surface);
	}

	.settings-page__theme-opt.is-active {
		border-color: color-mix(in srgb, var(--accent) 55%, var(--line));
		background: color-mix(in srgb, var(--accent) 8%, var(--bg));
		box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent) 25%, transparent);
	}

	.settings-page__theme-swatch {
		display: grid;
		grid-template-columns: 1fr 1fr;
		grid-template-rows: 1.35rem 0.55rem;
		width: 100%;
		margin-bottom: 0.45rem;
		border-radius: 0.35rem;
		overflow: hidden;
		border: 1px solid var(--line);
	}

	.settings-page__theme-swatch-bg {
		grid-column: 1 / -1;
		background: #f7f7f8;
	}

	.settings-page__theme-opt.is-dark .settings-page__theme-swatch-bg {
		background: #19191a;
	}

	.settings-page__theme-swatch-fg {
		background: #2e2e38;
	}

	.settings-page__theme-opt.is-dark .settings-page__theme-swatch-fg {
		background: #bdbdbd;
	}

	.settings-page__theme-swatch-accent {
		background: #4a62a8;
	}

	.settings-page__theme-opt.is-dark .settings-page__theme-swatch-accent {
		background: #90aef4;
	}

	/* system card: split light/dark preview */
	.settings-page__themes .settings-page__theme-opt:first-child .settings-page__theme-swatch-bg {
		background: linear-gradient(90deg, #f7f7f8 50%, #19191a 50%);
	}

	.settings-page__themes .settings-page__theme-opt:first-child .settings-page__theme-swatch-fg {
		background: linear-gradient(90deg, #2e2e38 50%, #bdbdbd 50%);
	}

	.settings-page__themes .settings-page__theme-opt:first-child .settings-page__theme-swatch-accent {
		background: linear-gradient(90deg, #4a62a8 50%, #90aef4 50%);
	}

	.settings-page__theme-name {
		font-size: 1rem;
		font-weight: 700;
		color: var(--fg);
	}

	.settings-page__theme-en {
		font-size: 0.72rem;
		color: var(--muted);
		font-weight: 500;
	}

	.settings-page__theme-hint {
		margin-top: 0.25rem;
		font-size: 0.78rem;
		color: var(--text);
		line-height: 1.45;
	}

	.settings-page__fonts {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.65rem;
		margin-top: 0.35rem;
	}

	.settings-page__font-opt {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.2rem;
		padding: 0.75rem 0.85rem;
		border: 1px solid var(--line);
		border-radius: var(--radius);
		background: var(--bg-soft);
		color: var(--fg);
		cursor: pointer;
		text-align: start;
		transition:
			border-color 0.15s ease,
			box-shadow 0.15s ease,
			background 0.15s ease;
	}

	.settings-page__font-opt:hover {
		border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
		background: var(--surface);
	}

	.settings-page__font-opt.is-active {
		border-color: color-mix(in srgb, var(--accent) 55%, var(--line));
		background: color-mix(in srgb, var(--accent) 8%, var(--bg));
		box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent) 25%, transparent);
	}

	.settings-page__font-name {
		font-size: 1rem;
		font-weight: 700;
		color: var(--fg);
	}

	.settings-page__font-en {
		font-size: 0.72rem;
		color: var(--muted);
		font-weight: 500;
	}

	.settings-page__font-preview {
		margin-top: 0.35rem;
		font-size: 0.88rem;
		color: var(--text);
		line-height: 1.5;
	}

	.settings-page__scale {
		margin: 0.75rem 0 1rem;
		padding: 0.75rem 0.9rem;
		border: 1px solid var(--line);
		border-radius: var(--radius);
		background: var(--bg-soft);
		font-size: 0.8rem;
		line-height: 1.6;
		color: var(--muted);
	}
	.settings-page__scale p {
		margin: 0.2rem 0;
	}
	.settings-page__scale strong {
		color: var(--fg);
		font-family: ui-monospace, Menlo, Consolas, monospace;
		font-weight: 600;
		min-width: 2.5rem;
		display: inline-block;
	}
	.settings-page__sample--h {
		font-size: var(--h2-size);
		line-height: var(--h2-lh);
		font-weight: 700;
		color: var(--fg);
		margin-top: 0.75rem;
	}

	@media (max-width: 720px) {
		.settings-page__themes {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 520px) {
		.settings-page__fonts {
			grid-template-columns: 1fr;
		}
	}
</style>
