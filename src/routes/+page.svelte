<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import SiteBrand from '$lib/components/SiteBrand.svelte';
	import AiGeneratedNotice from '$lib/components/AiGeneratedNotice.svelte';
	import { docSources } from '$lib/doc-sources';
	import type { IconName } from '$lib/icons/registry';

	const sources = docSources;

	const items: {
		href: string;
		title: string;
		desc: string;
		icon: IconName;
	}[] = [
		{
			href: '/pages/how-nix-works',
			title: 'نیکس چگونه کار می‌کند',
			desc: 'مدل · انبار · بازگردانی',
			icon: 'layers'
		},
		{
			href: '/pages/nix-dev',
			title: 'کل nix.dev (فارسی)',
			desc: 'آموزش‌ها · راهنماها · مفاهیم · مرجع',
			icon: 'library'
		},
		{
			href: '/pages/nix-manual',
			title: 'راهنمای مرجع Nix',
			desc: 'نصب · زبان · انبار · دستورات',
			icon: 'book-open'
		},
		{
			href: '/pages/nixpkgs-manual',
			title: 'راهنمای Nixpkgs',
			desc: 'بسته‌ها · stdenv · زبان‌ها · build helpers',
			icon: 'layers'
		},
		{
			href: '/pages/tour-of-nix',
			title: 'تور نیکس',
			desc: 'A tour of Nix · زبان نیکس تعاملی',
			icon: 'map'
		},
		{
			href: '/glossary',
			title: 'واژه‌نامه',
			desc: 'اصطلاحات تخصصی Nix و NixOS',
			icon: 'book'
		},
		{
			href: '/settings',
			title: 'تنظیمات',
			desc: 'قلم · اندازهٔ متن',
			icon: 'settings'
		}
	];

	function formatUpdated(iso: string): string {
		const d = new Date(iso + 'T12:00:00');
		if (Number.isNaN(d.getTime())) return iso;
		return new Intl.DateTimeFormat('fa-IR', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		}).format(d);
	}
</script>

<svelte:head>
	<title>نیکسی — آموزش و راهنمای فارسی Nix و NixOS</title>
	<meta name="description" content="راهنماهای فارسی Nix و NixOS — nix.dev، راهنمای مرجع، Nixpkgs و تور نیکس" />
	<meta property="og:title" content="نیکسی — آموزش و راهنمای فارسی Nix و NixOS" />
	<meta property="og:description" content="راهنماهای فارسی Nix و NixOS — nix.dev، راهنمای مرجع، Nixpkgs و تور نیکس" />
	<meta name="twitter:title" content="نیکسی — آموزش و راهنمای فارسی Nix و NixOS" />
	<meta name="twitter:description" content="راهنماهای فارسی Nix و NixOS — nix.dev، راهنمای مرجع، Nixpkgs و تور نیکس" />
	<!-- Agent discovery (RFC 8288 / RFC 9727 / Agent Skills Discovery); also via Link headers -->
	<link rel="api-catalog" href="/.well-known/api-catalog" type="application/linkset+json" />
	<link rel="describedby" href="/.well-known/agent-skills/index.json" type="application/json" />
	<link rel="service-desc" href="/glossary.json" type="application/json" />
	<link rel="service-doc" href="/" type="text/html" />
	<link rel="describedby" href="/sitemap.xml" type="application/xml" />
</svelte:head>

<section class="home">
	<h1 class="home__title"><SiteBrand size="lg" /></h1>
	<p class="home__lead">
		یادگیری Nix و NixOS به زبان فارسی. ساده، دقیق و روان
		<img
			class="home__lead-smiley"
			src="/icons/smiley.webp"
			alt=""
			width="20"
			height="20"
			decoding="async"
		/>
	</p>

	<div class="home__cards" data-no-panel>
		{#each items as item}
			<a class="home__card" href={item.href} data-no-panel="1">
				<span class="home__card-icon" aria-hidden="true">
					<Icon name={item.icon} size={22} />
				</span>
				<span class="home__card-title">{item.title}</span>
				<span class="home__card-desc">{item.desc}</span>
			</a>
		{/each}
	</div>
</section>

<section class="home-about" aria-labelledby="home-about-title">
	<h2 id="home-about-title" class="home-about__title">اصلاً چرا این سایت؟</h2>
	<p class="home-about__why">
		دوست داشتم نیکس رو به زبان فارسی یاد بگیرم، چون وقتی مطالب به زبان مادری باشه، فهمیدن و به یاد
		سپردنش خیلی راحت‌تره. واسه همین همه آموزش‌ها و مستنداتش رو همین‌جا یک‌جا جمع کردم.
	</p>

	<h3 class="home-about__sources-title">منابع اصلی</h3>
	<p class="home-about__sources-lead">
		محتوای این مستندات رو از سه منبع انگلیسی جمع‌آوری و به فارسی ترجمه کردیم. این ترجمه‌ی فارسی هم، مگر
		این‌که جایی خلافش رو مشخص کرده باشیم، دقیقاً تحت همون شرایط و مجوزهای انتشار هر کدوم از منابع اصلی
		در دسترسه.
	</p>
	<ul class="home-about__sources">
		{#each sources as src}
			<li class="home-about__source">
				<span class="home-about__source-line home-about__source-line--title">
					<a
						class="home-about__source-gh"
						href={src.git}
						rel="noopener noreferrer"
						target="_blank"
						aria-label="{src.name} روی گیت‌هاب"
						title="GitHub"
					>
						<Icon name="github" size={16} />
					</a>
					<a
						class="home-about__source-name"
						href={src.url}
						rel="noopener noreferrer"
						target="_blank"
					>
						{src.name}
					</a>
					<a
						class="home-about__source-license"
						href={src.licenseUrl}
						rel="noopener noreferrer"
						target="_blank"
						dir="ltr"
						title="فایل مجوز"
					>
						{src.license}
					</a>
				</span>
				<span class="home-about__source-line home-about__source-line--role">{src.role}</span>
				<span class="home-about__source-line home-about__source-line--updated">
					آخرین به‌روزرسانی این ترجمه:
					<time datetime={src.updated}>{formatUpdated(src.updated)}</time>
				</span>
			</li>
		{/each}
	</ul>
	<p class="home-about__licenses">
		<a href="/licenses">مجوزها و نسبت‌دهی</a>.
		کتابخانه‌ها، فونت‌ها، آیکون‌ها و ایموجی Fluent UI
	</p>
</section>

<section class="home-engage" aria-labelledby="home-engage-title">
	<h2 id="home-engage-title" class="home-engage__title">همکاری و گفتگو</h2>
	<p class="home-engage__lead">نیکسی با همراهی شما بهتر می‌شود.</p>
	<div class="home-engage__cards" data-no-panel>
		<a
			class="home-engage__card"
			href="https://a15d.at"
			target="_blank"
			rel="noopener noreferrer"
			data-no-panel="1"
		>
			<img
				class="home-engage__emoji"
				src="/icons/fluentui-emoji/light-bulb.webp"
				alt=""
				width="40"
				height="40"
				decoding="async"
			/>
			<span class="home-engage__card-title">درخواست ترجمه مقاله</span>
			<span class="home-engage__card-body">
				اگر مقاله یا راهنمایی از Nix یا NixOS مد نظر دارید که هنوز به فارسی برگردانده نشده، به من
				بگویید. تلاش می‌کنم آن را در نوبت ترجمه بگذارم.
			</span>
			<span class="home-engage__cta">درخواست ترجمه</span>
		</a>
		<a
			class="home-engage__card"
			href="https://a15d.at"
			target="_blank"
			rel="noopener noreferrer"
			data-no-panel="1"
		>
			<img
				class="home-engage__emoji"
				src="/icons/fluentui-emoji/memo.webp"
				alt=""
				width="40"
				height="40"
				decoding="async"
			/>
			<span class="home-engage__card-title">ارسال نظر و گزارش خطا</span>
			<span class="home-engage__card-body">
				اشکالی در متن‌ها دیده‌اید یا پیشنهادی برای بهبود سایت دارید؟ خیلی خوشحال می‌شوم نظرتان را
				بشنوم.
			</span>
			<span class="home-engage__cta">ارسال بازخورد</span>
		</a>
	</div>
</section>

<div class="home__ai-notice">
	<AiGeneratedNotice />
</div>
