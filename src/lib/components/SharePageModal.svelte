<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';

	let {
		open = $bindable(false),
		href = '',
		title = ''
	}: {
		open?: boolean;
		/** Absolute URL to share */
		href?: string;
		/** Optional page title for share text */
		title?: string;
	} = $props();

	let copied = $state(false);
	let copyError = $state('');

	const shareText = $derived(title ? `${title}\n${href}` : href);

	function close() {
		open = false;
		copied = false;
		copyError = '';
	}

	async function copy() {
		if (!href) return;
		copyError = '';
		try {
			if (navigator.clipboard?.writeText) {
				await navigator.clipboard.writeText(href);
			} else {
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

	function openShare(kind: 'wa' | 'x' | 'tg') {
		if (!href) return;
		const u = encodeURIComponent(href);
		const t = encodeURIComponent(shareText);
		const textOnly = encodeURIComponent(title ? `${title} ${href}` : href);
		let url = '';
		if (kind === 'wa') {
			url = `https://wa.me/?text=${textOnly}`;
		} else if (kind === 'x') {
			url = `https://twitter.com/intent/tweet?url=${u}${title ? `&text=${encodeURIComponent(title)}` : ''}`;
		} else {
			url = `https://t.me/share/url?url=${u}${title ? `&text=${encodeURIComponent(title)}` : ''}`;
		}
		window.open(url, '_blank', 'noopener,noreferrer');
	}

	function onKey(e: KeyboardEvent) {
		if (!open) return;
		if (e.key === 'Escape') {
			e.preventDefault();
			e.stopPropagation();
			close();
		}
	}

	$effect(() => {
		if (!open) return;
		const prev = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		return () => {
			document.body.style.overflow = prev;
		};
	});
</script>

<svelte:window onkeydowncapture={onKey} />

{#if open}
	<div class="spm" role="presentation">
		<button type="button" class="spm__backdrop" aria-label="بستن" onclick={close}></button>
		<div class="spm__panel" role="dialog" aria-modal="true" aria-labelledby="spm-title">
			<header class="spm__head">
				<h2 id="spm-title" class="spm__title">
					<span class="spm__title-icon" aria-hidden="true">
						<Icon name="share-2" size={18} />
					</span>
					اشتراک‌گذاری
				</h2>
				<button type="button" class="spm__x" aria-label="بستن" onclick={close}>
					<Icon name="x" size={18} />
				</button>
			</header>
			<p class="spm__lead">این صفحه را با دیگران به اشتراک بگذارید.</p>
			<div class="spm__url" dir="ltr">
				<code>{href}</code>
			</div>
			{#if copyError}
				<p class="spm__err" role="alert">{copyError}</p>
			{/if}
			<div class="spm__actions">
				<button type="button" class="spm__btn spm__btn--primary" onclick={copy}>
					{copied ? 'کپی شد!' : 'کپی لینک'}
				</button>
			</div>
			<div class="spm__share" role="group" aria-label="اشتراک در شبکه‌ها">
				<button type="button" class="spm__social spm__social--wa" onclick={() => openShare('wa')}>
					واتس‌اپ
				</button>
				<button type="button" class="spm__social spm__social--x" onclick={() => openShare('x')}>
					ایکس (توییتر)
				</button>
				<button type="button" class="spm__social spm__social--tg" onclick={() => openShare('tg')}>
					تلگرام
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.spm {
		position: fixed;
		inset: 0;
		z-index: 14000;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1rem;
	}

	.spm__backdrop {
		position: absolute;
		inset: 0;
		border: none;
		margin: 0;
		padding: 0;
		background: color-mix(in srgb, #0f172a 48%, transparent);
		backdrop-filter: blur(3px);
		cursor: pointer;
	}

	.spm__panel {
		position: relative;
		z-index: 1;
		width: min(28rem, 100%);
		padding: 1.05rem 1.15rem 1.2rem;
		border-radius: 0.85rem;
		border: 1px solid var(--line);
		background: var(--bg);
		color: var(--fg);
		box-shadow: 0 24px 64px color-mix(in srgb, #0f172a 28%, transparent);
		font-family: var(--font-ui);
	}

	.spm__head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.45rem;
	}

	.spm__title {
		margin: 0;
		display: inline-flex;
		align-items: center;
		gap: 0.45rem;
		font-size: 1.08rem;
		font-weight: 700;
		letter-spacing: -0.01em;
	}

	.spm__title-icon {
		display: inline-flex;
		color: var(--accent);
	}

	.spm__x {
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

	.spm__x:hover {
		color: var(--fg);
	}

	.spm__lead {
		margin: 0 0 0.75rem;
		font-size: 0.9rem;
		line-height: 1.55;
		color: var(--text);
	}

	.spm__url {
		margin: 0 0 0.85rem;
		padding: 0.65rem 0.75rem;
		border-radius: 0.5rem;
		border: 1px solid var(--line);
		background: var(--bg-soft);
		max-height: 7rem;
		overflow: auto;
		word-break: break-all;
	}

	.spm__url code {
		font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
		font-size: 0.8rem;
		background: none;
		border: none;
		padding: 0;
		color: var(--fg);
	}

	.spm__err {
		margin: 0 0 0.5rem;
		font-size: 0.85rem;
		color: #b91c1c;
	}

	.spm__actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.spm__btn {
		display: inline-flex;
		align-items: center;
		gap: 0.3rem;
		margin: 0;
		padding: 0.5rem 1rem;
		border-radius: 0.45rem;
		border: 1px solid var(--line);
		background: var(--bg-soft);
		color: var(--fg);
		font-weight: 600;
		font-size: 0.9rem;
		cursor: pointer;
		font-family: inherit;
	}

	.spm__btn--primary {
		background: var(--accent);
		border-color: var(--accent);
		color: #fff;
	}

	.spm__btn:hover {
		filter: brightness(1.05);
	}

	.spm__share {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 0.45rem;
	}

	.spm__social {
		margin: 0;
		padding: 0.55rem 0.4rem;
		border-radius: 0.45rem;
		border: 1px solid var(--line);
		background: var(--bg-soft);
		color: var(--fg);
		font-weight: 600;
		font-size: 0.82rem;
		cursor: pointer;
		font-family: inherit;
		transition:
			background 0.12s ease,
			border-color 0.12s ease;
	}

	.spm__social:hover {
		border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
		background: var(--surface);
	}

	.spm__social--wa:hover {
		border-color: #25d366;
		color: #128c7e;
	}

	.spm__social--x:hover {
		border-color: #111;
		color: var(--fg);
	}

	.spm__social--tg:hover {
		border-color: #2aabee;
		color: #229ed9;
	}

	@media (max-width: 420px) {
		.spm__share {
			grid-template-columns: 1fr;
		}
	}
</style>
