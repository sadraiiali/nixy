<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';

	let {
		open = $bindable(false),
		href = '',
		/** webxdc: copy-only · browser: open + copy (tour of nix etc.) */
		variant = 'webxdc',
		onclose
	}: {
		open?: boolean;
		href?: string;
		variant?: 'webxdc' | 'browser';
		onclose?: () => void;
	} = $props();

	let copied = $state(false);
	let copyError = $state('');

	function close() {
		open = false;
		copied = false;
		copyError = '';
		onclose?.();
	}

	async function copy() {
		copyError = '';
		try {
			if (navigator.clipboard?.writeText) {
				await navigator.clipboard.writeText(href);
			} else {
				// fallback
				const ta = document.createElement('textarea');
				ta.value = href;
				ta.style.position = 'fixed';
				ta.style.left = '-9999px';
				document.body.appendChild(ta);
				ta.select();
				document.execCommand('copy');
				document.body.removeChild(ta);
			}
			copied = true;
			setTimeout(() => {
				copied = false;
			}, 2000);
		} catch (e) {
			copyError = e instanceof Error ? e.message : 'کپی نشد';
		}
	}

	function openExternal() {
		if (!href) return;
		window.open(href, '_blank', 'noopener,noreferrer');
	}

	function onKey(e: KeyboardEvent) {
		if (!open) return;
		if (e.key === 'Escape') {
			e.preventDefault();
			close();
		}
	}
</script>

<svelte:window onkeydown={onKey} />

{#if open}
	<div class="lcm" role="presentation">
		<button type="button" class="lcm__backdrop" aria-label="بستن" onclick={close}></button>
		<div
			class="lcm__panel"
			role="dialog"
			aria-modal="true"
			aria-labelledby="lcm-title"
		>
			<header class="lcm__head">
				<h2 id="lcm-title" class="lcm__title">لینک خارجی</h2>
				<button type="button" class="lcm__x" aria-label="بستن" onclick={close}>
					<Icon name="x" size={18} />
				</button>
			</header>
			<p class="lcm__hint">
				{#if variant === 'webxdc'}
					در Webxdc نمی‌توان لینک‌ها را مستقیماً باز کرد. لینک را کپی کنید و در مرورگر باز کنید.
				{:else}
					این لینک به سایت دیگری می‌رود. می‌توانید آن را در تب جدید باز کنید یا کپی کنید.
				{/if}
			</p>
			<div class="lcm__url" dir="ltr">
				<code>{href}</code>
			</div>
			{#if copyError}
				<p class="lcm__err">{copyError}</p>
			{/if}
			<div class="lcm__actions">
				{#if variant === 'browser'}
					<button type="button" class="lcm__btn lcm__btn--primary" onclick={openExternal}>
						باز کردن
						<Icon name="arrow-up-right" size={14} />
					</button>
				{/if}
				<button
					type="button"
					class="lcm__btn"
					class:lcm__btn--primary={variant === 'webxdc'}
					onclick={copy}
				>
					{copied ? 'کپی شد ✓' : 'کپی لینک'}
				</button>
				<button type="button" class="lcm__btn" onclick={close}>بستن</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.lcm {
		position: fixed;
		inset: 0;
		z-index: 200;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1rem;
	}

	.lcm__backdrop {
		position: absolute;
		inset: 0;
		border: none;
		margin: 0;
		padding: 0;
		background: color-mix(in srgb, #0f172a 45%, transparent);
		cursor: pointer;
	}

	.lcm__panel {
		position: relative;
		z-index: 1;
		width: min(28rem, 100%);
		padding: 1rem 1.1rem 1.15rem;
		border-radius: 0.85rem;
		border: 1px solid var(--line, #e5e7eb);
		background: var(--bg, #fff);
		color: var(--fg, #111);
		box-shadow: 0 18px 50px color-mix(in srgb, #0f172a 22%, transparent);
		font-family: var(--font-ui, inherit);
	}

	.lcm__head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.lcm__title {
		margin: 0;
		font-size: 1.05rem;
		font-weight: 700;
	}

	.lcm__x {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 2rem;
		height: 2rem;
		border: 1px solid var(--line, #e5e7eb);
		border-radius: 0.45rem;
		background: var(--bg-soft, #f7f7f8);
		color: var(--muted, #666);
		cursor: pointer;
	}

	.lcm__hint {
		margin: 0 0 0.75rem;
		font-size: 0.88rem;
		line-height: 1.55;
		color: var(--text, #555);
	}

	.lcm__url {
		margin: 0 0 0.85rem;
		padding: 0.65rem 0.75rem;
		border-radius: 0.5rem;
		border: 1px solid var(--line, #e5e7eb);
		background: var(--bg-soft, #f7f7f8);
		max-height: 8rem;
		overflow: auto;
		word-break: break-all;
	}

	.lcm__url code {
		font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
		font-size: 0.8rem;
		background: none;
		border: none;
		padding: 0;
		color: var(--fg, #111);
	}

	.lcm__err {
		margin: 0 0 0.5rem;
		font-size: 0.85rem;
		color: #b91c1c;
	}

	.lcm__actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		justify-content: flex-end;
	}

	.lcm__btn {
		display: inline-flex;
		align-items: center;
		gap: 0.3rem;
		margin: 0;
		padding: 0.45rem 0.9rem;
		border-radius: 0.45rem;
		border: 1px solid var(--line, #e5e7eb);
		background: var(--bg-soft, #f7f7f8);
		color: var(--fg, #111);
		font-weight: 600;
		font-size: 0.88rem;
		cursor: pointer;
		font-family: inherit;
	}

	.lcm__btn--primary {
		background: var(--accent, #0a33ff);
		border-color: var(--accent, #0a33ff);
		color: #fff;
	}

	.lcm__btn:hover {
		filter: brightness(1.05);
	}
</style>
