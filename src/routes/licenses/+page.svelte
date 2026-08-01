<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';

	type AttrItem = {
		name: string;
		license: string;
		licenseUrl: string;
		homeUrl: string;
		desc: string;
	};

	const software: AttrItem[] = [
		{
			name: 'SvelteKit',
			license: 'MIT',
			licenseUrl: 'https://github.com/sveltejs/kit/blob/main/LICENSE',
			homeUrl: 'https://kit.svelte.dev/',
			desc: 'به عنوان چارچوب اصلی وب برای ساخت و بهینه‌سازی صفحات این سایت استفاده شده است.'
		},
		{
			name: 'Svelte',
			license: 'MIT',
			licenseUrl: 'https://github.com/sveltejs/svelte/blob/main/LICENSE.md',
			homeUrl: 'https://svelte.dev/',
			desc: 'کتابخانهٔ محوری رابط کاربری که ساختار تعاملی صفحات نیکسی را مدیریت می‌کند.'
		},
		{
			name: 'Vite',
			license: 'MIT',
			licenseUrl: 'https://github.com/vitejs/vite/blob/main/LICENSE',
			homeUrl: 'https://vite.dev/',
			desc: 'ابزار ساخت و توسعهٔ سریع که فرآیند کامپایل و آماده‌سازی کدهای سایت را بر عهده دارد.'
		},
		{
			name: 'mdsvex',
			license: 'MIT',
			licenseUrl: 'https://github.com/pngwn/MDsveX/blob/master/LICENSE',
			homeUrl: 'https://mdsvex.pngwn.io/',
			desc: 'برای پردازش و تبدیل پرونده‌های مارک‌دان به صفحات قابل نمایش در سایت به کار می‌رود.'
		},
		{
			name: 'Monaco Editor',
			license: 'MIT',
			licenseUrl: 'https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt',
			homeUrl: 'https://microsoft.github.io/monaco-editor/',
			desc: 'ویرایشگر قدرتمند کد که در بخش تور نیکسی برای نوشتن و آزمایش کدها استفاده شده است.'
		},
		{
			name: 'marked',
			license: 'MIT',
			licenseUrl: 'https://github.com/markedjs/marked/blob/master/LICENSE.md',
			homeUrl: 'https://marked.js.org/',
			desc: 'کتابخانه‌ای سبک برای تجزیه و تبدیل سریع متن‌های مارک‌دان.'
		},
		{
			name: 'Turndown',
			license: 'MIT',
			licenseUrl: 'https://github.com/mixmark-io/turndown/blob/master/LICENSE',
			homeUrl: 'https://github.com/mixmark-io/turndown',
			desc: 'ابزاری برای تبدیل کدهای HTML به متن‌های ساختاریافتهٔ مارک‌دان.'
		},
		{
			name: 'PrismJS',
			license: 'MIT',
			licenseUrl: 'https://github.com/PrismJS/prism/blob/master/LICENSE',
			homeUrl: 'https://prismjs.com/',
			desc: 'موتور برجسته‌سازی و رنگ‌آمیزی کدهای برنامه‌نویسی در بخش‌های مختلف مستندات.'
		}
	];

	const iconsEmoji: AttrItem[] = [
		{
			name: 'Lucide',
			license: 'ISC',
			licenseUrl: 'https://github.com/lucide-icons/lucide/blob/main/LICENSE',
			homeUrl: 'https://lucide.dev/',
			desc: 'مجموعه آیکون‌های مدرن و هماهنگ که در سراسر رابط کاربری سایت استفاده شده‌اند.'
		},
		{
			name: 'Fluent UI Emoji',
			license: 'MIT',
			licenseUrl: 'https://github.com/microsoft/fluentui-emoji/blob/main/LICENSE',
			homeUrl: 'https://github.com/microsoft/fluentui-emoji',
			desc: 'مجموعه ایموجی‌های مایکروسافت؛ «Slightly smiling face» در عنوان صفحهٔ اصلی، و «Light bulb» / «Memo» در کارت‌های درخواست ترجمه و بازخورد (WebP).'
		}
	];

	const fonts: AttrItem[] = [
		{
			name: 'Peyda (پیدا)',
			license: 'Fontiran (تجاری)',
			licenseUrl: 'https://fontiran.com/',
			homeUrl: 'https://fontiran.com/',
			desc: 'فونت فارسی رابط کاربری (Fontiran Pro). فایل‌های باینری فونت در مخزن commit نمی‌شوند؛ برای بازتوزیع فایل‌های فونت باید مجوز جداگانه از Fontiran داشته باشید.'
		},
		{
			name: 'IRANYekanX (ایران‌یکان)',
			license: 'Fontiran (تجاری)',
			licenseUrl: 'https://fontiran.com/',
			homeUrl: 'https://fontiran.com/',
			desc: 'فونت خوانا و استاندارد فارسی (Fontiran Eco) که به‌صورت self-hosted در تنظیمات سایت در دسترس است. بازتوزیع فایل فونت نیازمند مجوز Fontiran است.'
		},
		{
			name: 'Shabnam (شبنم)',
			license: 'SIL OFL 1.1',
			licenseUrl: 'https://github.com/rastikerdar/shabnam-font/blob/master/OFL.txt',
			homeUrl: 'https://github.com/rastikerdar/shabnam-font',
			desc: 'فونت آزاد فارسی (راستیکردار) که به‌عنوان گزینهٔ متن‌باز برای خوانایی بهتر متن‌ها استفاده می‌شود.'
		}
	];

	const docs: AttrItem[] = [
		{
			name: 'nix.dev',
			license: 'CC BY-SA 4.0',
			licenseUrl: 'https://github.com/NixOS/nix.dev/blob/master/LICENSE.md',
			homeUrl: 'https://nix.dev/',
			desc: 'منبع اصلی مقالات و راهنماهای کاربردی برای یادگیری و کار با نیکس؛ ترجمه‌ی فارسی در این سایت.'
		},
		{
			name: 'Nix reference manual',
			license: 'LGPL-2.1',
			licenseUrl: 'https://github.com/NixOS/nix/blob/master/COPYING',
			homeUrl: 'https://nix.dev/manual/nix/stable/',
			desc: 'راهنمای رسمی و مرجع جامع سیستم نیکس که ترجمه‌ی بخش‌هایی از آن در سایت موجود است.'
		},
		{
			name: 'Nixpkgs manual',
			license: 'MIT',
			licenseUrl: 'https://github.com/NixOS/nixpkgs/blob/master/COPYING',
			homeUrl: 'https://nixos.org/manual/nixpkgs/stable/',
			desc: 'راهنمای مجموعهٔ بسته‌های Nixpkgs؛ محتوای ترجمه‌شده تحت شرایط مجوز منبع اصلی.'
		},
		{
			name: 'A tour of Nix',
			license: 'LGPL-2.1',
			licenseUrl: 'https://github.com/nixcloud/tour_of_nix/blob/master/COPYING',
			homeUrl: 'https://nixcloud.io/tour/',
			desc: 'آموزش تعاملی و گام‌به‌گام زبان نیکس که الهام‌بخش بخش تور سایت بوده است.'
		}
	];
</script>

<svelte:head>
	<title>مجوزها و نسبت‌دهی · نیکسی</title>
	<meta
		name="description"
		content="آشنایی با کتابخانه‌ها، فونت‌ها، آیکون‌ها و منابع مستنداتی استفاده‌شده در نیکسی و مجوزهای آن‌ها."
	/>
	<meta property="og:title" content="مجوزها و نسبت‌دهی · نیکسی" />
	<meta name="twitter:title" content="مجوزها و نسبت‌دهی · نیکسی" />
</svelte:head>

<section class="licenses-page">
	<header class="licenses-page__head">
		<p class="tag" dir="ltr">LICENSES</p>
		<h1>
			<Icon name="book-open" size={28} class="licenses-page__hicon" />
			مجوزها و نسبت‌دهی
		</h1>
		<p class="licenses-page__lead">
			ما در نیکسی برای ساخت این مجموعه از ابزارها و منابع متن‌باز مختلفی بهره برده‌ایم. در این صفحه
			می‌توانید فهرست این موارد و مجوزهای هر کدام را مشاهده کنید.
		</p>
	</header>

	<section class="licenses-page__section" aria-labelledby="lic-software">
		<h2 id="lic-software">نرم‌افزارها و کتابخانه‌ها</h2>
		<ul class="licenses-page__list">
			{#each software as item}
				<li class="licenses-page__item">
					<div class="licenses-page__item-top">
						<a class="licenses-page__name" href={item.homeUrl} target="_blank" rel="noopener noreferrer"
							>{item.name}</a
						>
						<a
							class="licenses-page__badge"
							href={item.licenseUrl}
							target="_blank"
							rel="noopener noreferrer"
							dir="ltr"
							title="متن مجوز"
						>
							{item.license}
						</a>
					</div>
					<p class="licenses-page__desc">{item.desc}</p>
				</li>
			{/each}
		</ul>
	</section>

	<section class="licenses-page__section" aria-labelledby="lic-icons">
		<h2 id="lic-icons">آیکون‌ها و ایموجی‌ها</h2>
		<ul class="licenses-page__list">
			{#each iconsEmoji as item}
				<li class="licenses-page__item">
					<div class="licenses-page__item-top">
						<a class="licenses-page__name" href={item.homeUrl} target="_blank" rel="noopener noreferrer"
							>{item.name}</a
						>
						<a
							class="licenses-page__badge"
							href={item.licenseUrl}
							target="_blank"
							rel="noopener noreferrer"
							dir="ltr"
							title="متن مجوز"
						>
							{item.license}
						</a>
					</div>
					<p class="licenses-page__desc">{item.desc}</p>
					{#if item.name === 'Fluent UI Emoji'}
						<p class="licenses-page__sample">
							<img
								src="/icons/smiley.webp"
								alt="Slightly smiling face — Fluent UI Emoji"
								width="32"
								height="32"
								decoding="async"
							/>
							<span dir="ltr">Slightly smiling face · MIT · Microsoft</span>
						</p>
					{/if}
				</li>
			{/each}
		</ul>
	</section>

	<section class="licenses-page__section" aria-labelledby="lic-fonts">
		<h2 id="lic-fonts">فونت‌ها</h2>
		<ul class="licenses-page__list">
			{#each fonts as item}
				<li class="licenses-page__item">
					<div class="licenses-page__item-top">
						<a class="licenses-page__name" href={item.homeUrl} target="_blank" rel="noopener noreferrer"
							>{item.name}</a
						>
						<a
							class="licenses-page__badge"
							href={item.licenseUrl}
							target="_blank"
							rel="noopener noreferrer"
							dir="ltr"
							title="متن مجوز / ناشر"
						>
							{item.license}
						</a>
					</div>
					<p class="licenses-page__desc">{item.desc}</p>
				</li>
			{/each}
		</ul>
	</section>

	<section class="licenses-page__section" aria-labelledby="lic-docs">
		<h2 id="lic-docs">منابع محتوا و مستندات</h2>
		<ul class="licenses-page__list">
			{#each docs as item}
				<li class="licenses-page__item">
					<div class="licenses-page__item-top">
						<a class="licenses-page__name" href={item.homeUrl} target="_blank" rel="noopener noreferrer"
							>{item.name}</a
						>
						<a
							class="licenses-page__badge"
							href={item.licenseUrl}
							target="_blank"
							rel="noopener noreferrer"
							dir="ltr"
							title="متن مجوز"
						>
							{item.license}
						</a>
					</div>
					<p class="licenses-page__desc">{item.desc}</p>
				</li>
			{/each}
		</ul>
	</section>

	<section class="licenses-page__section" aria-labelledby="lic-site">
		<h2 id="lic-site">کد منبع وب‌سایت</h2>
		<p class="licenses-page__site-note">
			کد منبع و رابط کاربری این سایت یک پروژهٔ شخصی برای گردآوری و ارائهٔ مستندات ترجمه‌شده است.
			برای محتوای ترجمه‌شده، قوانین و مجوزهای مربوط به منابع اصلی مستندات همچنان برقرار است.
		</p>
	</section>

	<p class="licenses-page__back">
		<a href="/">
			<Icon name="arrow-left" size={18} dir />
			<span>بازگشت به خانه</span>
		</a>
	</p>
</section>

<style>
	.licenses-page {
		max-width: 40rem;
		margin: 0 auto;
		padding: 0.25rem 0 2rem;
	}

	.licenses-page__head {
		margin-bottom: 1.75rem;
	}

	.licenses-page__head :global(.tag) {
		margin: 0 0 0.45rem;
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		color: var(--muted);
		font-family: var(--font-ui);
	}

	.licenses-page__head h1 {
		margin: 0 0 0.65rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: clamp(1.45rem, 3.5vw, 1.75rem);
		font-weight: 800;
		letter-spacing: -0.02em;
		color: var(--fg);
		font-family: var(--font-ui);
	}

	/* class is applied inside Icon.svelte — must be :global for scoped CSS */
	.licenses-page__head h1 :global(.licenses-page__hicon) {
		color: var(--accent);
		flex-shrink: 0;
	}

	.licenses-page__lead {
		margin: 0;
		color: var(--text);
		font-size: 0.98rem;
		line-height: var(--text-lh);
		font-weight: 450;
	}

	.licenses-page__section {
		margin-bottom: 1.85rem;
	}

	.licenses-page__section h2 {
		margin: 0 0 0.75rem;
		font-size: 1.05rem;
		font-weight: 700;
		color: var(--fg);
		font-family: var(--font-ui);
	}

	.licenses-page__list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.55rem;
	}

	.licenses-page__item {
		padding: 0.85rem 0.95rem;
		border: 1px solid var(--line);
		border-radius: 0.65rem;
		background: var(--bg-soft);
	}

	.licenses-page__item-top {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 0.45rem 0.75rem;
		margin-bottom: 0.35rem;
	}

	.licenses-page__name {
		font-weight: 700;
		color: var(--fg);
		text-decoration: none;
		font-family: var(--font-ui);
	}

	.licenses-page__name:hover {
		color: var(--accent);
	}

	.licenses-page__badge {
		flex-shrink: 0;
		padding: 0.12rem 0.45rem;
		border-radius: 0.3rem;
		border: 1px solid var(--line);
		background: var(--bg);
		color: var(--muted);
		font-size: 0.72rem;
		font-weight: 600;
		text-decoration: none;
		font-family: ui-monospace, Menlo, Consolas, monospace;
	}

	.licenses-page__badge:hover {
		border-color: color-mix(in srgb, var(--accent) 40%, var(--line));
		color: var(--accent);
	}

	.licenses-page__desc {
		margin: 0;
		color: var(--text);
		font-size: 0.9rem;
		line-height: var(--text-lh);
	}

	.licenses-page__sample {
		display: flex;
		align-items: center;
		gap: 0.55rem;
		margin: 0.65rem 0 0;
		padding: 0.45rem 0.55rem;
		border-radius: 0.45rem;
		background: var(--bg);
		border: 1px solid var(--line);
		color: var(--muted);
		font-size: 0.78rem;
	}

	.licenses-page__sample img {
		width: 1.75rem;
		height: 1.75rem;
		object-fit: contain;
	}

	.licenses-page__site-note {
		margin: 0;
		padding: 0.9rem 1rem;
		border: 1px solid var(--line);
		border-radius: 0.65rem;
		background: var(--bg-soft);
		color: var(--text);
		font-size: 0.92rem;
		line-height: var(--text-lh);
	}

	.licenses-page__back {
		margin: 1.5rem 0 0;
	}

	.licenses-page__back a {
		display: inline-flex;
		align-items: center;
		gap: 0.35rem;
		color: var(--accent);
		font-weight: 600;
		text-decoration: none;
		font-family: var(--font-ui);
	}

	.licenses-page__back a:hover {
		text-decoration: underline;
		text-underline-offset: 0.15em;
	}
</style>
