<script lang="ts">
	import { browser } from '$app/environment';
	import { page } from '$app/state';
	import Icon from '$lib/components/Icon.svelte';
	import SiteBrand from '$lib/components/SiteBrand.svelte';
	import { helpCardSources } from '$lib/doc-sources';

	const AUTO_KEY = 'nixi-help-auto-shown';
	const DISMISS_KEY = 'nixi-help-dismissed';
	const AUTO_MAX = 3;

	let open = $state(false);
	let dismissed = $state(false);

	/** Only home `/` — not other routes */
	const isHome = $derived((page.url.pathname.replace(/\/$/, '') || '/') === '/');

	function readDismissed(): boolean {
		if (!browser) return false;
		try {
			return localStorage.getItem(DISMISS_KEY) === '1';
		} catch {
			return false;
		}
	}

	function readAutoCount(): number {
		if (!browser) return AUTO_MAX;
		try {
			const n = Number(localStorage.getItem(AUTO_KEY));
			return Number.isFinite(n) && n >= 0 ? Math.floor(n) : 0;
		} catch {
			return AUTO_MAX;
		}
	}

	function bumpAutoCount() {
		if (!browser) return;
		try {
			const next = Math.min(AUTO_MAX, readAutoCount() + 1);
			localStorage.setItem(AUTO_KEY, String(next));
		} catch {
			/* ignore */
		}
	}

	function show() {
		open = true;
	}

	function hide() {
		open = false;
	}

	/** Permanent dismiss — no more auto-show; card closes */
	function dismiss() {
		if (browser) {
			try {
				localStorage.setItem(DISMISS_KEY, '1');
				// stop further auto attempts
				localStorage.setItem(AUTO_KEY, String(AUTO_MAX));
			} catch {
				/* ignore */
			}
		}
		dismissed = true;
		open = false;
	}

	function onKey(e: KeyboardEvent) {
		if (!isHome || !open) return;
		if (e.key === 'Escape') {
			e.preventDefault();
			hide();
		}
	}

	// Sync dismissed from storage once on client
	$effect(() => {
		if (!browser) return;
		dismissed = readDismissed();
	});

	// Auto-show only on home `/`, at most 3 times, unless dismissed
	$effect(() => {
		if (!browser) return;
		if (!isHome) {
			open = false;
			return;
		}
		if (dismissed || readDismissed()) return;
		if (readAutoCount() >= AUTO_MAX) return;
		const t = setTimeout(() => {
			if ((page.url.pathname.replace(/\/$/, '') || '/') !== '/') return;
			if (readDismissed()) return;
			if (readAutoCount() >= AUTO_MAX) return;
			bumpAutoCount();
			open = true;
		}, 320);
		return () => clearTimeout(t);
	});
</script>

<svelte:window onkeydown={onKey} />

{#if isHome}
	<button
		type="button"
		class="help-fab"
		class:help-fab--active={open}
		aria-label="نیکسی چیه؟"
		aria-haspopup="dialog"
		aria-expanded={open}
		onclick={() => (open ? hide() : show())}
		data-no-panel
	>
		?
	</button>
{/if}

{#if isHome && open}
	<div
		class="help-card"
		role="dialog"
		aria-modal="false"
		aria-labelledby="help-card-title"
		data-no-panel
	>
		<header class="help-card__head">
			<div class="help-card__brand">
				<SiteBrand size="sm" />
			</div>
			<button type="button" class="help-card__x" aria-label="بستن" onclick={hide}>
				<Icon name="x" size={16} />
			</button>
		</header>

		<div class="help-card__body">
			<h2 id="help-card-title" class="help-card__title">نیکسی چیه؟</h2>
			<p>
				<strong>نیکسی</strong> یه راهنمای فارسی، ساده و خواناست برای Nix. مطالب از منابع رسمی
				انگلیسی جمع‌آوری و ترجمه شدن تا یادگیری Nix برات راحت‌تر و لذت‌بخش‌تر بشه.
			</p>
			<p>
				راستش دلم می‌خواست Nix رو یاد بگیرم و با خودم گفتم چرا به زبان خودمون نباشه؟ وقتی مطالب به
				فارسی باشن، فهمیدن و یادگرفتنشون خیلی راحت‌تره. برای همین همه‌چیز رو همین‌جا دور هم جمع
				کردم.
			</p>

			<h3 class="help-card__h">داخل نیکسی چی پیدا می‌کنی؟</h3>
			<ul>
				<li><strong>نیکس چگونه کار می‌کند</strong>: مدل ذهنی، انبار و بازگردانی</li>
				<li><strong>nix.dev</strong>: آموزش‌ها و راهنماهای گام‌به‌گام رسمی</li>
				<li><strong>راهنمای مرجع Nix</strong>: مستندات کامل نصب، زبان، انبار و دستورها</li>
				<li><strong>تور نیکس</strong>: یادگیری تعاملی زبان نیکس</li>
				<li><strong>واژه‌نامه</strong>: توضیحات ساده برای اصطلاحات تخصصی</li>
			</ul>

			<h3 class="help-card__h">چطور استفاده کنی؟</h3>
			<ul>
				<li>می‌تونی از کارت‌های صفحهٔ اصلی یا آیکون‌های بالای صفحه بین بخش‌ها جابه‌جا بشی.</li>
				<li>
					برای جستجوی سریع، <kbd dir="ltr">Ctrl</kbd>+<kbd dir="ltr">K</kbd> رو بزن.
				</li>
				<li>
					لینک‌های داخل متن معمولاً توی <strong>پنل چپ</strong> باز می‌شن؛ برای دیدن صفحه به‌صورت
					کامل می‌تونی روی «باز کردن صفحه» بزنی.
				</li>
				<li>عرض پنل چپ توی دسکتاپ از طریق کشیدن لبهٔ راستش قابل تغییره.</li>
				<li>
					تغییر فونت و اندازهٔ متن از
					<a href="/settings" onclick={hide}>تنظیمات</a>.
				</li>
			</ul>

			<h3 class="help-card__h">منابع و مجوزها</h3>
			<p>بیشتر مطالب از این منابع جمع‌آوری شدن. ترجمه فارسی ما برای هر بخش از همون مجوز منبع اصلی پیروی می‌کنه، مگه اینکه خلافش ذکر شده باشه:</p>
			<ul class="help-card__sources">
				{#each helpCardSources as src}
					<li>
						<a href={src.url} rel="noopener noreferrer" target="_blank" dir="ltr">{src.name}</a>
						{' '}
						(
						<a href={src.licenseUrl} rel="noopener noreferrer" target="_blank" dir="ltr"
							>{src.license}</a
						>)
					</li>
				{/each}
			</ul>
		</div>

		<footer class="help-card__foot">
			<button type="button" class="help-card__dismiss" onclick={dismiss}>
				دیگه نشون نده
			</button>
			<button type="button" class="help-card__ok" onclick={hide}>باشه</button>
		</footer>
	</div>
{/if}

<style>
	.help-fab {
		position: fixed;
		left: max(0.85rem, env(safe-area-inset-left, 0px));
		bottom: max(0.85rem, env(safe-area-inset-bottom, 0px));
		z-index: 90;
		width: 2.35rem;
		height: 2.35rem;
		margin: 0;
		padding: 0;
		border: 1px solid var(--line);
		border-radius: 999px;
		background: color-mix(in srgb, var(--bg) 92%, transparent);
		backdrop-filter: blur(10px);
		color: var(--muted);
		font-family: var(--font-ui);
		font-size: 1.05rem;
		font-weight: 800;
		line-height: 1;
		cursor: pointer;
		box-shadow: 0 4px 16px color-mix(in srgb, #0f172a 12%, transparent);
		transition:
			color 0.12s ease,
			border-color 0.12s ease,
			background 0.12s ease,
			transform 0.12s ease;
	}

	.help-fab:hover,
	.help-fab--active {
		color: var(--fg);
		border-color: color-mix(in srgb, var(--accent) 40%, var(--line));
		background: var(--surface);
	}

	.help-fab:hover {
		transform: translateY(-1px);
	}

	.help-fab:focus-visible {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}

	/* Floating card above the ? button (bottom-left) */
	.help-card {
		position: fixed;
		left: max(0.85rem, env(safe-area-inset-left, 0px));
		bottom: calc(0.85rem + 2.35rem + 0.55rem + env(safe-area-inset-bottom, 0px));
		z-index: 91;
		display: flex;
		flex-direction: column;
		width: min(22.5rem, calc(100vw - 1.7rem));
		max-height: min(70dvh, 28rem);
		border: 1px solid var(--line);
		border-radius: 0.85rem;
		background: var(--bg-soft);
		color: var(--fg);
		font-family: var(--font-ui);
		box-shadow:
			0 1px 0 color-mix(in srgb, #0f172a 4%, transparent),
			0 12px 36px color-mix(in srgb, #0f172a 14%, transparent);
		overflow: hidden;
		animation: help-card-in 0.18s cubic-bezier(0.2, 0.85, 0.25, 1) both;
	}

	@keyframes help-card-in {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: none;
		}
	}

	.help-card__head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		flex: none;
		padding: 0.7rem 0.8rem;
		border-bottom: 1px solid var(--line);
		background: var(--surface, var(--bg));
	}

	.help-card__brand {
		min-width: 0;
	}

	.help-card__x {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 1.9rem;
		height: 1.9rem;
		margin: 0;
		padding: 0;
		border: 1px solid transparent;
		border-radius: 0.4rem;
		background: transparent;
		color: var(--muted);
		cursor: pointer;
	}

	.help-card__x:hover {
		color: var(--fg);
		background: var(--bg);
		border-color: var(--line);
	}

	.help-card__body {
		flex: 1 1 auto;
		min-height: 0;
		overflow: auto;
		padding: 0.85rem 0.95rem 0.4rem;
		font-size: 0.86rem;
		line-height: var(--text-lh, 1.6);
		color: var(--text);
	}

	.help-card__title {
		margin: 0 0 0.5rem;
		font-size: 1rem;
		font-weight: 700;
		color: var(--fg);
		letter-spacing: -0.015em;
	}

	.help-card__h {
		margin: 0.9rem 0 0.3rem;
		font-size: 0.88rem;
		font-weight: 700;
		color: var(--fg);
	}

	.help-card__body p {
		margin: 0 0 0.5rem;
	}

	.help-card__body ul {
		margin: 0 0 0.5rem;
		padding-inline-start: 1.05rem;
	}

	.help-card__body li {
		margin: 0.2rem 0;
	}

	.help-card__body a {
		color: var(--accent);
		font-weight: 600;
		text-decoration: none;
	}

	.help-card__body a:hover {
		text-decoration: underline;
	}

	.help-card__sources {
		margin: 0 0 0.5rem;
		padding-inline-start: 1.05rem;
	}

	.help-card__sources li {
		margin: 0.25rem 0;
	}

	.help-card__body kbd {
		display: inline-block;
		padding: 0.05rem 0.3rem;
		border: 1px solid var(--line);
		border-radius: 0.28rem;
		background: var(--bg);
		font-size: 0.78em;
		font-weight: 600;
	}

	.help-card__foot {
		flex: none;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: flex-end;
		gap: 0.45rem;
		padding: 0.65rem 0.8rem 0.8rem;
		border-top: 1px solid var(--line);
		background: var(--surface, var(--bg));
	}

	.help-card__dismiss {
		margin: 0;
		margin-inline-end: auto;
		padding: 0.4rem 0.7rem;
		border: 1px solid transparent;
		border-radius: 0.45rem;
		background: transparent;
		color: var(--muted);
		font-family: var(--font-ui);
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
	}

	.help-card__dismiss:hover {
		color: var(--fg);
		background: var(--bg);
		border-color: var(--line);
	}

	.help-card__ok {
		margin: 0;
		padding: 0.4rem 0.95rem;
		border: 1px solid color-mix(in srgb, var(--accent) 40%, var(--line));
		border-radius: 0.45rem;
		background: color-mix(in srgb, var(--accent) 12%, var(--bg));
		color: var(--accent);
		font-family: var(--font-ui);
		font-size: 0.84rem;
		font-weight: 700;
		cursor: pointer;
	}

	.help-card__ok:hover {
		background: color-mix(in srgb, var(--accent) 20%, var(--bg));
	}

	@media (prefers-reduced-motion: reduce) {
		.help-card {
			animation: none;
		}
	}
</style>
