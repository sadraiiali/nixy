<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import Icon from '$lib/components/Icon.svelte';
	import { settingsUi } from '$lib/settings-ui.svelte';

	/** Deep link: open modal and leave a light fallback page. */
	onMount(() => {
		if (!browser) return;
		settingsUi.show();
		// Prefer staying off a dedicated route when possible
		const ref = document.referrer;
		try {
			if (ref) {
				const u = new URL(ref);
				if (u.origin === location.origin && !u.pathname.replace(/\/$/, '').endsWith('/settings')) {
					void goto(u.pathname + u.search + u.hash, {
						replaceState: true,
						noScroll: true,
						keepFocus: true
					});
					return;
				}
			}
		} catch {
			/* ignore */
		}
		void goto('/', { replaceState: true, noScroll: true, keepFocus: true });
	});
</script>

<svelte:head>
	<title>تنظیمات · نیکسی</title>
	<meta
		name="description"
		content="تنظیمات نمایش نیکسی: تم، فونت متن، فونت ویرایشگر و اندازهٔ قلم."
	/>
	<meta property="og:title" content="تنظیمات · نیکسی" />
	<meta name="twitter:title" content="تنظیمات · نیکسی" />
	<meta name="robots" content="noindex" />
</svelte:head>

<section class="settings-page settings-page--fallback">
	<header class="settings-page__head">
		<h1>
			<Icon name="settings" size={28} class="settings-page__hicon" />
			تنظیمات
		</h1>
		<p class="settings-page__lead">
			پنجرهٔ تنظیمات در حال باز شدن است. اگر ظاهر نشد،
			<button type="button" class="settings-page__open" onclick={() => settingsUi.show()}>
				اینجا را بزنید
			</button>
			.
		</p>
	</header>
</section>

<style>
	.settings-page--fallback {
		max-width: 28rem;
		margin-inline: auto;
		padding: 2rem var(--pad, 1rem);
	}

	.settings-page__open {
		display: inline;
		margin: 0;
		padding: 0;
		border: none;
		background: none;
		color: var(--accent);
		font: inherit;
		font-weight: 700;
		cursor: pointer;
		text-decoration: underline;
		text-underline-offset: 0.15em;
	}
</style>
