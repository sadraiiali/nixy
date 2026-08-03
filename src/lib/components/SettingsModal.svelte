<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import Icon from '$lib/components/Icon.svelte';
	import {
		EDITOR_FONTS,
		EDITOR_FONT_DEFAULT,
		EDITOR_FONT_SIZE_DEFAULT,
		EDITOR_FONT_SIZE_MAX,
		EDITOR_FONT_SIZE_MIN,
		applyEditorFont,
		applyEditorFontSize,
		readEditorFont,
		readEditorFontSize,
		type EditorFontId
	} from '$lib/editor-font';
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
	import { settingsUi, type SettingsTab } from '$lib/settings-ui.svelte';
	import {
		THEMES,
		THEME_DEFAULT,
		applyTheme,
		readTheme,
		resolveTheme,
		watchSystemTheme,
		type ThemeId
	} from '$lib/theme';
	import type { IconName } from '$lib/icons/registry';

	const TABS: {
		id: SettingsTab;
		label: string;
		icon: IconName;
		hint: string;
	}[] = [
		{ id: 'appearance', label: 'ظاهر', icon: 'eye', hint: 'پوسته روشن، تیره یا سیستم' },
		{ id: 'text', label: 'متن', icon: 'type', hint: 'فونت و اندازهٔ متن سایت' },
		{ id: 'editor', label: 'ویرایشگر', icon: 'terminal', hint: 'فونت mono برای کد' }
	];

	const MOBILE_MQ = '(max-width: 720px)';

	let fontSize = $state(FONT_DEFAULT);
	let fontFamily = $state<FontFamilyId>(FONT_FAMILY_DEFAULT);
	let editorFont = $state<EditorFontId>(EDITOR_FONT_DEFAULT);
	let editorFontSize = $state(EDITOR_FONT_SIZE_DEFAULT);
	let theme = $state<ThemeId>(THEME_DEFAULT);
	let themeResolved = $state<'light' | 'dark'>('light');
	let savedFlash = $state(false);
	let panelEl: HTMLElement | undefined = $state();
	/** Phone: menu list vs drilled-in section (desktop ignores). */
	let mobileDrill = $state(false);
	/** Prefer correct first paint on client (avoid desktop modal flash on phones). */
	let isMobile = $state(
		typeof window !== 'undefined' ? window.matchMedia(MOBILE_MQ).matches : false
	);

	const open = $derived(settingsUi.open);
	const tab = $derived(settingsUi.tab);
	const activeTabMeta = $derived(TABS.find((t) => t.id === tab) ?? TABS[0]!);
	const mobileTitle = $derived(
		isMobile && mobileDrill ? activeTabMeta.label : 'تنظیمات'
	);

	function flashSaved() {
		savedFlash = true;
		setTimeout(() => {
			savedFlash = false;
		}, 900);
	}

	function close() {
		mobileDrill = false;
		settingsUi.hide();
	}

	function setTab(id: SettingsTab) {
		settingsUi.tab = id;
		if (isMobile) mobileDrill = true;
	}

	/** Phone header back: leave section → menu, or leave menu → close. */
	function onBack() {
		if (isMobile && mobileDrill) {
			mobileDrill = false;
			return;
		}
		close();
	}

	function setSize(px: number) {
		fontSize = applyFontSize(px);
		flashSaved();
	}

	function setFamily(id: FontFamilyId) {
		fontFamily = applyFontFamily(id);
		flashSaved();
	}

	function setEditorFamily(id: EditorFontId) {
		editorFont = applyEditorFont(id);
		flashSaved();
	}

	function setEditorSize(px: number) {
		editorFontSize = applyEditorFontSize(px);
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

	function editorPreset(kind: 'sm' | 'md' | 'lg' | 'xl') {
		if (kind === 'sm') setEditorSize(12);
		else if (kind === 'md') setEditorSize(14);
		else if (kind === 'lg') setEditorSize(18);
		else setEditorSize(28);
	}

	function syncFromStorage() {
		if (!browser) return;
		fontSize = readFontSize();
		fontFamily = readFontFamily();
		editorFont = readEditorFont();
		editorFontSize = readEditorFontSize();
		theme = readTheme();
		themeResolved = resolveTheme(theme);
	}

	function onKey(e: KeyboardEvent) {
		if (!open) return;
		if (e.key === 'Escape') {
			e.preventDefault();
			e.stopPropagation();
			onBack();
		}
	}

	$effect(() => {
		if (!open || !browser) return;
		syncFromStorage();
		// Opening settings: start at root menu on phone
		if (isMobile) mobileDrill = false;
		const prev = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		requestAnimationFrame(() => {
			panelEl?.focus();
		});
		return () => {
			document.body.style.overflow = prev;
		};
	});

	onMount(() => {
		if (!browser) return;
		const mq = window.matchMedia(MOBILE_MQ);
		const syncMq = () => {
			isMobile = mq.matches;
			if (!mq.matches) mobileDrill = false;
		};
		syncMq();
		mq.addEventListener('change', syncMq);
		const stopTheme = watchSystemTheme((resolved) => {
			if (readTheme() === 'system') {
				themeResolved = resolved;
			}
		});
		return () => {
			mq.removeEventListener('change', syncMq);
			stopTheme();
		};
	});
</script>

<svelte:window onkeydowncapture={onKey} />

{#if open}
	<div class="sm" class:sm--mobile={isMobile} role="presentation">
		{#if !isMobile}
			<button type="button" class="sm__backdrop" aria-label="بستن" onclick={close}></button>
		{/if}
		<div
			class="sm__panel"
			class:sm__panel--mobile={isMobile}
			class:sm__panel--drill={isMobile && mobileDrill}
			role="dialog"
			aria-modal="true"
			aria-labelledby="sm-title"
			tabindex="-1"
			bind:this={panelEl}
		>
			<!-- Phone: sticky page header with back -->
			{#if isMobile}
				<header class="sm__page-head">
					<button type="button" class="sm__back" aria-label="بازگشت" onclick={onBack}>
						<Icon name="arrow-right" size={20} dir />
						<span class="sm__back-label">بازگشت</span>
					</button>
					<h2 id="sm-title" class="sm__page-title">{mobileTitle}</h2>
					<span class="sm__page-head-trail" aria-live="polite">
						{#if savedFlash}
							<span class="sm__saved sm__saved--head">
								<Icon name="circle-check" size={14} />
								ذخیره
							</span>
						{/if}
					</span>
				</header>
			{/if}

			<!-- Desktop side nav / Phone root menu -->
			<aside
				class="sm__nav"
				class:sm__nav--hidden-mobile={isMobile && mobileDrill}
				aria-label="بخش‌های تنظیمات"
			>
				{#if !isMobile}
					<header class="sm__nav-head">
						<span class="sm__nav-icon" aria-hidden="true">
							<Icon name="settings" size={18} />
						</span>
						<h2 id="sm-title" class="sm__nav-title">تنظیمات</h2>
					</header>
				{/if}

				{#if isMobile && !mobileDrill}
					<p class="sm__menu-lead">ظاهر، فونت متن و فونت ویرایشگر کد.</p>
				{/if}

				<div
					class="sm__tabs"
					class:sm__tabs--menu={isMobile}
					role="tablist"
					aria-orientation={isMobile ? 'vertical' : 'vertical'}
					aria-label="بخش‌ها"
				>
					{#each TABS as t}
						<button
							type="button"
							class="sm__tab"
							class:sm__tab--row={isMobile}
							class:is-active={!isMobile && tab === t.id}
							role="tab"
							id="sm-tab-{t.id}"
							aria-selected={tab === t.id}
							aria-controls="sm-panel-{t.id}"
							tabindex={!isMobile && tab === t.id ? 0 : isMobile ? 0 : -1}
							onclick={() => setTab(t.id)}
						>
							<span class="sm__tab-icon" aria-hidden="true">
								<Icon name={t.icon} size={isMobile ? 20 : 16} />
							</span>
							<span class="sm__tab-text">
								<span class="sm__tab-label">{t.label}</span>
								{#if isMobile}
									<span class="sm__tab-hint">{t.hint}</span>
								{/if}
							</span>
							{#if isMobile}
								<span class="sm__tab-chevron" aria-hidden="true">
									<Icon name="chevron-left" size={18} dir />
								</span>
							{/if}
						</button>
					{/each}
				</div>
				{#if !isMobile && savedFlash}
					<p class="sm__saved" role="status">
						<Icon name="circle-check" size={14} />
						ذخیره شد
					</p>
				{/if}
			</aside>

			<!-- Content: desktop always; phone only when drilled in -->
			<div
				class="sm__body"
				class:sm__body--hidden-mobile={isMobile && !mobileDrill}
			>
				{#if !isMobile}
					<header class="sm__body-head">
						<h3 class="sm__body-title">{activeTabMeta.label}</h3>
						<button type="button" class="sm__x" aria-label="بستن" onclick={close}>
							<Icon name="x" size={18} />
						</button>
					</header>
				{/if}

				<div class="sm__scroll">
					{#if tab === 'appearance'}
						<div
							class="sm__section"
							role="tabpanel"
							id="sm-panel-appearance"
							aria-labelledby="sm-tab-appearance"
						>
							<div class="sm__row">
								<span class="sm__label">پوسته (تم)</span>
								<span class="sm__px" dir="ltr">
									{THEMES.find((t) => t.id === theme)?.labelEn ?? theme}
									{#if theme === 'system'}
										· {themeResolved}
									{/if}
								</span>
							</div>
							<div class="sm__themes" role="radiogroup" aria-label="انتخاب پوسته">
								{#each THEMES as t}
									<button
										type="button"
										class="sm__theme-opt"
										class:is-active={theme === t.id}
										class:is-light={t.id === 'light' ||
											(t.id === 'system' && themeResolved === 'light')}
										class:is-dark={t.id === 'dark' ||
											(t.id === 'system' && themeResolved === 'dark')}
										role="radio"
										aria-checked={theme === t.id}
										onclick={() => setTheme(t.id)}
									>
										<span class="sm__theme-swatch" aria-hidden="true">
											<span class="sm__theme-swatch-bg"></span>
											<span class="sm__theme-swatch-fg"></span>
											<span class="sm__theme-swatch-accent"></span>
										</span>
										<span class="sm__theme-name">{t.label}</span>
										<span class="sm__theme-en" dir="ltr">{t.labelEn}</span>
										<span class="sm__theme-hint">{t.hint}</span>
									</button>
								{/each}
							</div>
						</div>
					{:else if tab === 'text'}
						<div
							class="sm__section"
							role="tabpanel"
							id="sm-panel-text"
							aria-labelledby="sm-tab-text"
						>
							<div class="sm__row">
								<span class="sm__label">فونت رابط</span>
								<span class="sm__px" dir="ltr">
									{FONT_FAMILIES.find((f) => f.id === fontFamily)?.labelEn ?? fontFamily}
								</span>
							</div>
							<div class="sm__fonts" role="radiogroup" aria-label="انتخاب فونت">
								{#each FONT_FAMILIES as fam}
									<button
										type="button"
										class="sm__font-opt"
										class:is-active={fontFamily === fam.id}
										role="radio"
										aria-checked={fontFamily === fam.id}
										style:font-family={fam.stack}
										onclick={() => setFamily(fam.id)}
									>
										<span class="sm__font-name">{fam.label}</span>
										<span class="sm__font-en" dir="ltr">{fam.labelEn}</span>
										<span class="sm__font-preview">بسته، انبار Nix، ۱۲۳</span>
									</button>
								{/each}
							</div>

							<div class="sm__row sm__row--spaced">
								<span class="sm__label">اندازهٔ پایه (1rem)</span>
								<span class="sm__px" dir="ltr">{fontSize}px</span>
							</div>
							<input
								class="sm__range"
								type="range"
								min={FONT_MIN}
								max={FONT_MAX}
								step="1"
								value={fontSize}
								aria-label="اندازه پایه قلم به پیکسل"
								oninput={(e) =>
									setSize(Number((e.currentTarget as HTMLInputElement).value))}
							/>
							<div class="sm__presets">
								<button type="button" class="sm__blk" onclick={() => preset('sm')}
									>کوچک ۱۴</button
								>
								<button type="button" class="sm__blk" onclick={() => preset('md')}
									>متوسط ۱۶</button
								>
								<button type="button" class="sm__blk" onclick={() => preset('lg')}
									>بزرگ ۱۹</button
								>
							</div>
							<p class="sm__sample">
								نمونه: بسته، انبار Nix، بازگردانی — متن فارسی با فونت و اندازهٔ فعلی.
							</p>
						</div>
					{:else}
						<div
							class="sm__section"
							role="tabpanel"
							id="sm-panel-editor"
							aria-labelledby="sm-tab-editor"
						>
							<p class="sm__lead">
								فونت mono برای بلوک‌های کد، کد درون‌خطی، و ویرایشگر تور نیکس (Monaco).
								فونت‌های اختیاری فقط در صورت نصب روی سیستم اعمال می‌شوند.
							</p>
							<div class="sm__row">
								<span class="sm__label">فونت ویرایشگر</span>
								<span class="sm__px" dir="ltr">
									{EDITOR_FONTS.find((f) => f.id === editorFont)?.labelEn ?? editorFont}
								</span>
							</div>
							<div
								class="sm__fonts sm__fonts--editor"
								role="radiogroup"
								aria-label="فونت ویرایشگر"
							>
								{#each EDITOR_FONTS as fam}
									<button
										type="button"
										class="sm__font-opt"
										class:is-active={editorFont === fam.id}
										role="radio"
										aria-checked={editorFont === fam.id}
										style:font-family={fam.stack}
										onclick={() => setEditorFamily(fam.id)}
									>
										<span class="sm__font-name" dir="ltr">{fam.labelEn}</span>
										<span class="sm__font-en">{fam.label}</span>
										<span class="sm__font-preview" dir="ltr"
											>{'{'} pkgs ? "hello" : null {'}'}</span
										>
										<span class="sm__font-hint">{fam.hint}</span>
									</button>
								{/each}
							</div>

							<div class="sm__row sm__row--spaced">
								<span class="sm__label">اندازهٔ کد</span>
								<span class="sm__px" dir="ltr">{editorFontSize}px</span>
							</div>
							<input
								class="sm__range"
								type="range"
								min={EDITOR_FONT_SIZE_MIN}
								max={EDITOR_FONT_SIZE_MAX}
								step="1"
								value={editorFontSize}
								aria-label="اندازه فونت ویرایشگر و کد"
								oninput={(e) =>
									setEditorSize(Number((e.currentTarget as HTMLInputElement).value))}
							/>
							<div class="sm__presets sm__presets--editor">
								<button type="button" class="sm__blk" onclick={() => editorPreset('sm')}
									>۱۲</button
								>
								<button type="button" class="sm__blk" onclick={() => editorPreset('md')}
									>۱۴</button
								>
								<button type="button" class="sm__blk" onclick={() => editorPreset('lg')}
									>۱۸</button
								>
								<button type="button" class="sm__blk" onclick={() => editorPreset('xl')}
									>۲۸</button
								>
							</div>
							<pre
								class="sm__code-sample"
								dir="ltr"
								style:font-family={EDITOR_FONTS.find((f) => f.id === editorFont)?.stack}
								style:font-size="{editorFontSize}px"
							><code>nix-env -iA nixpkgs.hello
# {`let x = 1; in x + 2`}</code></pre>
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.sm {
		position: fixed;
		inset: 0;
		z-index: 14500;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: max(0.75rem, env(safe-area-inset-top, 0px))
			max(0.75rem, env(safe-area-inset-right, 0px))
			max(0.75rem, env(safe-area-inset-bottom, 0px))
			max(0.75rem, env(safe-area-inset-left, 0px));
	}

	.sm--mobile {
		padding: 0;
		align-items: stretch;
		justify-content: stretch;
	}

	.sm__backdrop {
		position: absolute;
		inset: 0;
		border: none;
		margin: 0;
		padding: 0;
		background: color-mix(in srgb, #0f172a 48%, transparent);
		backdrop-filter: blur(4px);
		cursor: pointer;
	}

	.sm__panel {
		position: relative;
		z-index: 1;
		display: flex;
		width: min(52rem, 100%);
		height: min(36rem, calc(100vh - 1.5rem));
		max-height: calc(100dvh - 1.5rem);
		border-radius: 0.75rem;
		border: 1px solid var(--line);
		background: var(--bg);
		color: var(--fg);
		box-shadow: 0 28px 80px color-mix(in srgb, #0f172a 32%, transparent);
		font-family: var(--font-ui);
		overflow: hidden;
		outline: none;
	}

	.sm__panel--mobile {
		width: 100%;
		height: 100%;
		max-height: none;
		min-height: 100dvh;
		border-radius: 0;
		border: none;
		box-shadow: none;
		flex-direction: column;
		/* iOS safe areas */
		padding-top: env(safe-area-inset-top, 0px);
		padding-bottom: env(safe-area-inset-bottom, 0px);
		padding-inline: env(safe-area-inset-left, 0px) env(safe-area-inset-right, 0px);
	}

	/* ── Phone page header ── */
	.sm__page-head {
		display: grid;
		grid-template-columns: minmax(4.5rem, 1fr) auto minmax(4.5rem, 1fr);
		align-items: center;
		gap: 0.35rem;
		flex: 0 0 auto;
		min-height: 3.25rem;
		padding: 0.35rem 0.65rem;
		border-bottom: 1px solid var(--line);
		background: color-mix(in srgb, var(--bg) 92%, var(--bg-soft));
		/* sticky feel under safe area */
		position: sticky;
		top: 0;
		z-index: 2;
	}

	.sm__back {
		display: inline-flex;
		align-items: center;
		justify-content: flex-start;
		gap: 0.15rem;
		margin: 0;
		padding: 0.4rem 0.35rem;
		border: none;
		border-radius: 0.45rem;
		background: transparent;
		color: var(--accent);
		font: inherit;
		font-size: 0.92rem;
		font-weight: 600;
		cursor: pointer;
		min-height: 2.5rem;
		-webkit-tap-highlight-color: transparent;
	}

	.sm__back:active {
		background: color-mix(in srgb, var(--accent) 10%, transparent);
	}

	.sm__back-label {
		line-height: 1;
	}

	.sm__page-title {
		margin: 0;
		justify-self: center;
		font-size: 1.05rem;
		font-weight: 700;
		letter-spacing: -0.015em;
		text-align: center;
		white-space: nowrap;
	}

	.sm__page-head-trail {
		justify-self: end;
		min-height: 1.25rem;
		display: flex;
		align-items: center;
		justify-content: flex-end;
	}

	.sm__saved--head {
		margin: 0;
		font-size: 0.72rem;
	}

	.sm__menu-lead {
		margin: 0.15rem 1rem 0.85rem;
		font-size: 0.9rem;
		line-height: 1.5;
		color: var(--text);
	}

	.sm__nav {
		flex: 0 0 11.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		padding: 0.85rem 0.65rem;
		background: var(--bg-soft);
		border-inline-end: 1px solid var(--line);
		min-width: 0;
	}

	.sm__panel--mobile .sm__nav {
		flex: 1 1 auto;
		border-inline-end: none;
		background: var(--bg);
		padding: 0.5rem 0 1.25rem;
		overflow: auto;
		min-height: 0;
	}

	.sm__nav--hidden-mobile {
		display: none;
	}

	.sm__nav-head {
		display: flex;
		align-items: center;
		gap: 0.45rem;
		padding: 0.35rem 0.55rem 0.75rem;
	}

	.sm__nav-icon {
		display: inline-flex;
		color: var(--accent);
	}

	.sm__nav-title {
		margin: 0;
		font-size: 0.95rem;
		font-weight: 700;
		letter-spacing: -0.01em;
	}

	.sm__tabs {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		flex: 1 1 auto;
	}

	.sm__tabs--menu {
		gap: 0;
		padding: 0 0.65rem;
	}

	.sm__tab {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		width: 100%;
		margin: 0;
		padding: 0.5rem 0.65rem;
		border: none;
		border-radius: 0.45rem;
		background: transparent;
		color: var(--text);
		font: inherit;
		font-size: 0.88rem;
		font-weight: 600;
		cursor: pointer;
		text-align: start;
		transition:
			background 0.12s ease,
			color 0.12s ease;
		-webkit-tap-highlight-color: transparent;
	}

	.sm__tab:hover {
		background: color-mix(in srgb, var(--fg) 6%, transparent);
		color: var(--fg);
	}

	.sm__tab.is-active {
		background: color-mix(in srgb, var(--accent) 12%, var(--bg));
		color: var(--fg);
		box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 22%, transparent);
	}

	/* Phone: full-width list rows */
	.sm__tab--row {
		gap: 0.75rem;
		padding: 0.95rem 0.85rem;
		border-radius: 0.65rem;
		margin-bottom: 0.4rem;
		background: var(--bg-soft);
		border: 1px solid var(--line);
		color: var(--fg);
		font-size: 1rem;
		box-shadow: none;
	}

	.sm__tab--row:hover,
	.sm__tab--row:active {
		background: color-mix(in srgb, var(--accent) 8%, var(--bg-soft));
		border-color: color-mix(in srgb, var(--accent) 30%, var(--line));
		box-shadow: none;
	}

	.sm__tab-icon {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		flex: 0 0 auto;
		width: 2.15rem;
		height: 2.15rem;
		border-radius: 0.5rem;
		background: color-mix(in srgb, var(--accent) 12%, var(--bg));
		color: var(--accent);
	}

	.sm__tab:not(.sm__tab--row) .sm__tab-icon {
		width: auto;
		height: auto;
		background: transparent;
		color: inherit;
	}

	.sm__tab-text {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.15rem;
		flex: 1 1 auto;
		min-width: 0;
	}

	.sm__tab-label {
		font-weight: 700;
		line-height: 1.25;
	}

	.sm__tab-hint {
		font-size: 0.78rem;
		font-weight: 500;
		color: var(--muted);
		line-height: 1.35;
	}

	.sm__tab-chevron {
		display: inline-flex;
		color: var(--faint, var(--muted));
		flex: 0 0 auto;
	}

	.sm__saved {
		margin: 0.35rem 0.55rem 0;
		display: inline-flex;
		align-items: center;
		gap: 0.3rem;
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--ok);
	}

	.sm__body {
		flex: 1 1 auto;
		display: flex;
		flex-direction: column;
		min-width: 0;
		min-height: 0;
		background: var(--bg);
	}

	.sm__panel--mobile .sm__body {
		flex: 1 1 auto;
		min-height: 0;
	}

	.sm__body--hidden-mobile {
		display: none;
	}

	.sm__body-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 0.85rem 1.1rem 0.65rem;
		border-bottom: 1px solid var(--line-soft);
		flex: 0 0 auto;
	}

	.sm__body-title {
		margin: 0;
		font-size: 1.05rem;
		font-weight: 700;
		letter-spacing: -0.015em;
	}

	.sm__x {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 2rem;
		height: 2rem;
		border: 1px solid var(--line);
		border-radius: 0.45rem;
		background: var(--bg-soft);
		color: var(--muted);
		cursor: pointer;
	}

	.sm__x:hover {
		color: var(--fg);
	}

	.sm__scroll {
		flex: 1 1 auto;
		overflow: auto;
		padding: 1rem 1.15rem 1.35rem;
		min-height: 0;
		-webkit-overflow-scrolling: touch;
	}

	.sm__panel--mobile .sm__scroll {
		padding: 1rem 1rem calc(1.5rem + env(safe-area-inset-bottom, 0px));
	}

	.sm__section {
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.sm__lead {
		margin: 0 0 1rem;
		font-size: 0.88rem;
		line-height: 1.55;
		color: var(--text);
	}

	.sm__row {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		margin-bottom: 0.75rem;
		font-weight: 600;
		font-size: 0.78rem;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--muted);
		gap: 0.5rem;
	}

	.sm__row--spaced {
		margin-top: 1.35rem;
	}

	.sm__label {
		color: var(--fg);
		letter-spacing: 0.02em;
		text-transform: none;
		font-size: 0.88rem;
	}

	.sm__px {
		font-variant-numeric: tabular-nums;
		font-weight: 700;
		font-size: 0.75rem;
		border: 1px solid var(--line);
		padding: 0.15rem 0.45rem;
		border-radius: 0.3rem;
		background: var(--bg-soft);
		color: var(--fg);
		text-transform: none;
		letter-spacing: 0;
		flex: 0 0 auto;
	}

	.sm__themes {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.55rem;
	}

	.sm__theme-opt {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.12rem;
		padding: 0.7rem 0.75rem;
		border: 1px solid var(--line);
		border-radius: 0.55rem;
		background: var(--bg-soft);
		color: var(--fg);
		cursor: pointer;
		text-align: start;
		font: inherit;
		transition:
			border-color 0.15s ease,
			box-shadow 0.15s ease,
			background 0.15s ease;
	}

	.sm__theme-opt:hover {
		border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
		background: var(--surface);
	}

	.sm__theme-opt.is-active {
		border-color: color-mix(in srgb, var(--accent) 55%, var(--line));
		background: color-mix(in srgb, var(--accent) 8%, var(--bg));
		box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent) 25%, transparent);
	}

	.sm__theme-swatch {
		display: grid;
		grid-template-columns: 1fr 1fr;
		grid-template-rows: 1.25rem 0.5rem;
		width: 100%;
		margin-bottom: 0.4rem;
		border-radius: 0.3rem;
		overflow: hidden;
		border: 1px solid var(--line);
	}

	.sm__theme-swatch-bg {
		grid-column: 1 / -1;
		background: #f7f7f8;
	}

	.sm__theme-opt.is-dark .sm__theme-swatch-bg {
		background: #19191a;
	}

	.sm__theme-swatch-fg {
		background: #2e2e38;
	}

	.sm__theme-opt.is-dark .sm__theme-swatch-fg {
		background: #bdbdbd;
	}

	.sm__theme-swatch-accent {
		background: #4a62a8;
	}

	.sm__theme-opt.is-dark .sm__theme-swatch-accent {
		background: #90aef4;
	}

	.sm__themes .sm__theme-opt:first-child .sm__theme-swatch-bg {
		background: linear-gradient(90deg, #f7f7f8 50%, #19191a 50%);
	}

	.sm__themes .sm__theme-opt:first-child .sm__theme-swatch-fg {
		background: linear-gradient(90deg, #2e2e38 50%, #bdbdbd 50%);
	}

	.sm__themes .sm__theme-opt:first-child .sm__theme-swatch-accent {
		background: linear-gradient(90deg, #4a62a8 50%, #90aef4 50%);
	}

	.sm__theme-name {
		font-size: 0.92rem;
		font-weight: 700;
	}

	.sm__theme-en {
		font-size: 0.7rem;
		color: var(--muted);
		font-weight: 500;
	}

	.sm__theme-hint {
		margin-top: 0.2rem;
		font-size: 0.75rem;
		color: var(--text);
		line-height: 1.4;
	}

	.sm__fonts {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.55rem;
	}

	.sm__fonts--editor {
		grid-template-columns: 1fr 1fr;
	}

	.sm__font-opt {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.15rem;
		padding: 0.7rem 0.75rem;
		border: 1px solid var(--line);
		border-radius: 0.55rem;
		background: var(--bg-soft);
		color: var(--fg);
		cursor: pointer;
		text-align: start;
		font: inherit;
		transition:
			border-color 0.15s ease,
			box-shadow 0.15s ease,
			background 0.15s ease;
	}

	.sm__font-opt:hover {
		border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
		background: var(--surface);
	}

	.sm__font-opt.is-active {
		border-color: color-mix(in srgb, var(--accent) 55%, var(--line));
		background: color-mix(in srgb, var(--accent) 8%, var(--bg));
		box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent) 25%, transparent);
	}

	.sm__font-name {
		font-size: 0.92rem;
		font-weight: 700;
	}

	.sm__font-en {
		font-size: 0.7rem;
		color: var(--muted);
		font-weight: 500;
	}

	.sm__font-preview {
		margin-top: 0.3rem;
		font-size: 0.85rem;
		color: var(--text);
		line-height: 1.45;
	}

	.sm__font-hint {
		margin-top: 0.2rem;
		font-size: 0.72rem;
		color: var(--muted);
		line-height: 1.4;
		font-family: var(--font-ui);
	}

	.sm__range {
		width: 100%;
		accent-color: var(--fg);
		margin-bottom: 0.75rem;
		height: 1.25rem;
	}

	.sm__presets {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 0.45rem;
		margin-bottom: 0.35rem;
	}

	.sm__presets--editor {
		grid-template-columns: repeat(4, 1fr);
	}

	.sm__blk {
		font: inherit;
		font-family: var(--font);
		font-weight: 600;
		font-size: 0.8rem;
		min-height: 2.35rem;
		border: 1px solid var(--line);
		border-radius: 0.4rem;
		background: var(--bg-soft);
		color: var(--fg);
		cursor: pointer;
	}

	.sm__blk:hover {
		background: var(--fg);
		color: var(--bg);
	}

	.sm__sample {
		margin: 1rem 0 0;
		padding: 0.85rem 0 0;
		border-top: 1px solid var(--line-soft);
		font-size: 1em;
		line-height: 1.65;
		color: var(--fg);
	}

	.sm__code-sample {
		margin: 1rem 0 0;
		padding: 0.85rem 1rem;
		border: 1px solid var(--line);
		border-radius: 0.5rem;
		background: var(--ide-bg, #0f1419);
		color: var(--ide-fg, #e2e8f0);
		overflow: auto;
		line-height: 1.55;
	}

	.sm__code-sample code {
		font: inherit;
		background: none;
		border: none;
		padding: 0;
		color: inherit;
	}

	@media (max-width: 720px) {
		.sm__themes {
			grid-template-columns: 1fr;
		}

		.sm__fonts,
		.sm__fonts--editor {
			grid-template-columns: 1fr;
		}
	}
</style>
