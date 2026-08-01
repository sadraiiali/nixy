<script lang="ts">
	/**
	 * Per-page title/description that also updates Open Graph + Twitter tags.
	 * Root layout already sets site defaults; this overrides them for the current page.
	 */
	import { page } from '$app/state';
	import {
		FAVICON,
		SITE_DESCRIPTION,
		SITE_NAME,
		SITE_TITLE,
		absoluteUrl
	} from '$lib/site-meta';

	let {
		title,
		description = SITE_DESCRIPTION,
		/** Use summary card without large image (rare). */
		card = 'summary_large_image' as 'summary' | 'summary_large_image'
	}: {
		title: string;
		description?: string;
		card?: 'summary' | 'summary_large_image';
	} = $props();

	const fullTitle = $derived(
		!title || title === SITE_NAME || title === SITE_TITLE
			? SITE_TITLE
			: title.endsWith(` · ${SITE_NAME}`) || title.endsWith(` · نیکسی`)
				? title
				: `${title} · ${SITE_NAME}`
	);
	const canonicalUrl = $derived(absoluteUrl(page.url.pathname, page.url.origin));
	const ogImageUrl = $derived(absoluteUrl(FAVICON.ogImage, page.url.origin));
</script>

<svelte:head>
	<title>{fullTitle}</title>
	<meta name="description" content={description} />
	<link rel="canonical" href={canonicalUrl} />

	<meta property="og:title" content={fullTitle} />
	<meta property="og:description" content={description} />
	<meta property="og:url" content={canonicalUrl} />
	<meta property="og:image" content={ogImageUrl} />

	<meta name="twitter:card" content={card} />
	<meta name="twitter:title" content={fullTitle} />
	<meta name="twitter:description" content={description} />
	<meta name="twitter:image" content={ogImageUrl} />
</svelte:head>
