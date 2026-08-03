<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Icon from '$lib/components/Icon.svelte';
	import SharePageModal from '$lib/components/SharePageModal.svelte';
	import { inAppPanel } from '$lib/in-app-panel.svelte';
	import { searchCommands, type CommandItem } from '$lib/command-index';
	import { settingsUi } from '$lib/settings-ui.svelte';
	import { applyTheme, type ThemeId } from '$lib/theme';

	let {
		open = $bindable(false)
	}: {
		open?: boolean;
	} = $props();

	let query = $state('');
	let active = $state(0);
	let inputEl: HTMLInputElement | undefined = $state();
	let listEl: HTMLElement | undefined = $state();
	let shareOpen = $state(false);
	let shareHref = $state('');
	let shareTitle = $state('');

	const results = $derived(searchCommands(query));

	$effect(() => {
		// reset selection when results change
		void results;
		active = 0;
	});

	$effect(() => {
		if (!browser || !open) return;
		query = '';
		active = 0;
		// focus after paint
		requestAnimationFrame(() => {
			inputEl?.focus();
			inputEl?.select();
		});
		const prev = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		return () => {
			document.body.style.overflow = prev;
		};
	});

	function close() {
		open = false;
		query = '';
		active = 0;
	}

	function runThemeAction(action: CommandItem['action']): ThemeId | null {
		if (action === 'theme-light') return 'light';
		if (action === 'theme-dark') return 'dark';
		if (action === 'theme-system') return 'system';
		return null;
	}

	function openSharePage() {
		if (browser) {
			shareHref = window.location.href;
			shareTitle =
				typeof document !== 'undefined' ? document.title.replace(/\s*·\s*نیکسی\s*$/, '').trim() : '';
		} else {
			shareHref = page.url.href;
			shareTitle = '';
		}
		close();
		// open after palette closes so focus/overflow don't clash
		requestAnimationFrame(() => {
			shareOpen = true;
		});
	}

	function runItem(item: CommandItem) {
		if (item.action === 'close-panel') {
			inAppPanel.close();
			close();
			return;
		}
		if (item.action === 'share-page') {
			openSharePage();
			return;
		}
		if (item.action === 'settings') {
			close();
			requestAnimationFrame(() => settingsUi.show());
			return;
		}
		const themeId = runThemeAction(item.action);
		if (themeId) {
			applyTheme(themeId);
			close();
			return;
		}
		if (item.href) {
			const href = item.href;
			// Settings: open modal instead of navigating
			const path = href.split('?')[0]?.replace(/\/$/, '') || '/';
			if (path === '/settings') {
				close();
				requestAnimationFrame(() => settingsUi.show());
				return;
			}
			close();
			// full navigation (not side panel) — user chose deliberately
			void goto(href);
			return;
		}
		close();
	}

	function onKey(e: KeyboardEvent) {
		if (!open) return;
		if (e.key === 'Escape') {
			e.preventDefault();
			e.stopPropagation();
			close();
			return;
		}
		if (e.key === 'ArrowDown') {
			e.preventDefault();
			e.stopPropagation();
			if (!results.length) return;
			active = (active + 1) % results.length;
			scrollActive();
			return;
		}
		if (e.key === 'ArrowUp') {
			e.preventDefault();
			e.stopPropagation();
			if (!results.length) return;
			active = (active - 1 + results.length) % results.length;
			scrollActive();
			return;
		}
		// PageUp / PageDown: move within palette list only (not the page behind)
		if (e.key === 'PageDown' || e.key === 'PageUp') {
			e.preventDefault();
			e.stopPropagation();
			if (!results.length || !listEl) return;
			const dir = e.key === 'PageDown' ? 1 : -1;
			const sample = listEl.querySelector<HTMLElement>('[data-cmd-i]');
			const itemH = Math.max(28, sample?.offsetHeight ?? 48);
			const page = Math.max(1, Math.floor(listEl.clientHeight / itemH) - 1);
			active = Math.min(results.length - 1, Math.max(0, active + dir * page));
			scrollActive();
			return;
		}
		if (e.key === 'Enter') {
			e.preventDefault();
			e.stopPropagation();
			const item = results[active];
			if (item) runItem(item);
		}
	}

	function scrollActive() {
		requestAnimationFrame(() => {
			const el = listEl?.querySelector<HTMLElement>(`[data-cmd-i="${active}"]`);
			el?.scrollIntoView({ block: 'nearest' });
		});
	}

	function groupOf(items: CommandItem[]): { group: string; items: { item: CommandItem; i: number }[] }[] {
		const map = new Map<string, { item: CommandItem; i: number }[]>();
		items.forEach((item, i) => {
			const g = item.group;
			if (!map.has(g)) map.set(g, []);
			map.get(g)!.push({ item, i });
		});
		return [...map.entries()].map(([group, rows]) => ({ group, items: rows }));
	}

	const grouped = $derived(groupOf(results));
</script>

<!-- capture so PageUp/Down don't scroll the document behind the palette -->
<svelte:window onkeydowncapture={onKey} />

{#if open}
	<div class="cmdk" role="presentation">
		<button type="button" class="cmdk__backdrop" aria-label="بستن" onclick={close}></button>
		<div
			class="cmdk__panel"
			role="dialog"
			aria-modal="true"
			aria-label="جستجو و فرمان"
		>
			<div class="cmdk__search">
				<span class="cmdk__search-icon" aria-hidden="true">
					<Icon name="search" size={18} />
				</span>
				<input
					bind:this={inputEl}
					class="cmdk__input"
					type="search"
					placeholder="جستجوی صفحات و فرمان‌ها…"
					autocomplete="off"
					autocorrect="off"
					spellcheck="false"
					bind:value={query}
					aria-controls="cmdk-list"
					aria-autocomplete="list"
				/>
				<kbd class="cmdk__kbd" dir="ltr">Esc</kbd>
			</div>

			<div class="cmdk__list" id="cmdk-list" role="listbox" bind:this={listEl}>
				{#if results.length === 0}
					<p class="cmdk__empty">نتیجه‌ای پیدا نشد.</p>
				{:else}
					{#each grouped as g}
						<p class="cmdk__group">{g.group}</p>
						{#each g.items as { item, i }}
							<button
								type="button"
								class="cmdk__item"
								class:is-active={i === active}
								role="option"
								aria-selected={i === active}
								data-cmd-i={i}
								onmouseenter={() => (active = i)}
								onclick={() => runItem(item)}
							>
								{#if item.icon}
									<span class="cmdk__item-icon" aria-hidden="true">
										<Icon name={item.icon} size={16} />
									</span>
								{/if}
								<span class="cmdk__item-body">
									<span class="cmdk__item-title">{item.title}</span>
									{#if item.subtitle}
										<span class="cmdk__item-sub" dir="ltr">{item.subtitle}</span>
									{/if}
								</span>
							</button>
						{/each}
					{/each}
				{/if}
			</div>

			<footer class="cmdk__foot" dir="ltr">
				<span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>
				<span><kbd>↵</kbd> open</span>
				<span><kbd>esc</kbd> close</span>
			</footer>
		</div>
	</div>
{/if}

<SharePageModal bind:open={shareOpen} href={shareHref} title={shareTitle} />

<style>
	.cmdk {
		position: fixed;
		inset: 0;
		z-index: 13000;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: min(18vh, 7rem) 1rem 1rem;
		pointer-events: auto;
	}

	.cmdk__backdrop {
		position: absolute;
		inset: 0;
		border: none;
		margin: 0;
		padding: 0;
		background: color-mix(in srgb, #0f172a 48%, transparent);
		backdrop-filter: blur(3px);
		cursor: pointer;
	}

	.cmdk__panel {
		position: relative;
		z-index: 1;
		width: min(36rem, 100%);
		max-height: min(70dvh, 32rem);
		display: flex;
		flex-direction: column;
		border-radius: 0.85rem;
		border: 1px solid var(--line);
		background: var(--bg);
		color: var(--fg);
		box-shadow: 0 24px 64px color-mix(in srgb, #0f172a 28%, transparent);
		overflow: hidden;
		animation: cmdk-in 0.14s ease-out;
		font-family: var(--font-ui);
	}

	@keyframes cmdk-in {
		from {
			opacity: 0;
			transform: translateY(-6px) scale(0.98);
		}
		to {
			opacity: 1;
			transform: none;
		}
	}

	.cmdk__search {
		display: flex;
		align-items: center;
		gap: 0.55rem;
		padding: 0.75rem 0.9rem;
		border-bottom: 1px solid var(--line);
		flex: 0 0 auto;
	}

	.cmdk__search-icon {
		display: inline-flex;
		color: var(--muted);
		opacity: 0.85;
	}

	.cmdk__input {
		flex: 1 1 auto;
		min-width: 0;
		margin: 0;
		padding: 0.25rem 0;
		border: none;
		outline: none;
		background: transparent;
		color: var(--fg);
		font-family: inherit;
		font-size: 1rem;
		font-weight: 500;
	}

	.cmdk__input::placeholder {
		color: var(--faint);
	}

	.cmdk__kbd {
		flex-shrink: 0;
		padding: 0.12rem 0.4rem;
		border: 1px solid var(--line);
		border-radius: 0.3rem;
		background: var(--bg-soft);
		color: var(--muted);
		font-size: 0.68rem;
		font-family: ui-monospace, Menlo, Consolas, monospace;
	}

	.cmdk__list {
		flex: 1 1 auto;
		min-height: 0;
		overflow: auto;
		padding: 0.4rem 0.4rem 0.55rem;
		-webkit-overflow-scrolling: touch;
	}

	.cmdk__empty {
		margin: 1.25rem 0.75rem;
		text-align: center;
		color: var(--muted);
		font-size: 0.9rem;
	}

	.cmdk__group {
		margin: 0.55rem 0.55rem 0.25rem;
		font-size: 0.68rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		color: var(--muted);
		text-transform: uppercase;
	}

	.cmdk__item {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.65rem;
		width: 100%;
		margin: 0;
		padding: 0.55rem 0.7rem;
		border: none;
		border-radius: 0.45rem;
		background: transparent;
		color: var(--fg);
		text-align: start;
		cursor: pointer;
		font-family: inherit;
	}

	.cmdk__item:hover,
	.cmdk__item.is-active {
		background: color-mix(in srgb, var(--accent) 12%, var(--bg-soft));
	}

	.cmdk__item-icon {
		flex: 0 0 auto;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 1.65rem;
		height: 1.65rem;
		border-radius: 0.35rem;
		background: var(--bg-soft);
		color: var(--muted);
	}

	.cmdk__item.is-active .cmdk__item-icon,
	.cmdk__item:hover .cmdk__item-icon {
		color: var(--accent);
		background: color-mix(in srgb, var(--accent) 14%, var(--bg));
	}

	.cmdk__item-body {
		flex: 1 1 auto;
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 0.12rem;
	}

	.cmdk__item-title {
		font-size: 0.92rem;
		font-weight: 600;
		line-height: 1.35;
	}

	.cmdk__item-sub {
		font-size: 0.72rem;
		color: var(--muted);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.cmdk__foot {
		display: flex;
		flex-wrap: wrap;
		gap: 0.85rem;
		padding: 0.45rem 0.85rem;
		border-top: 1px solid var(--line);
		background: var(--bg-soft);
		color: var(--muted);
		font-size: 0.68rem;
		flex: 0 0 auto;
	}

	.cmdk__foot kbd {
		display: inline-block;
		margin-inline-end: 0.15rem;
		padding: 0.05rem 0.28rem;
		border: 1px solid var(--line);
		border-radius: 0.25rem;
		background: var(--bg);
		font-family: var(--font-mono);
		font-size: 0.65rem;
	}

	/* Phone: no keyboard chrome (Esc / navigate / open) */
	@media (max-width: 720px) {
		.cmdk__kbd,
		.cmdk__foot {
			display: none;
		}
	}
</style>
