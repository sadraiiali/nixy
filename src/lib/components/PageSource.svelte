<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import { page } from '$app/state';
	import contributorsDoc from '$lib/page-contributors.json';

	/**
	 * End-of-article source:
	 * 1) «منبع» card → published docs + GitHub icon
	 * 2) Contributor faces (left) + label (right); overflow → "…" → GitHub
	 */
	type Contributor = {
		login: string;
		name: string;
		commits?: number;
		url: string;
		avatar: string;
	};

	type PageEntry = {
		contributors?: Contributor[];
		github?: string | null;
		repo?: string;
		path?: string;
		ref?: string;
	};

	type Props = {
		/** Published docs / web URL */
		href: string;
		/** Short label shown in the card (e.g. nix.dev/install-nix) */
		label: string;
		/** Optional route key; defaults to current pathname */
		route?: string;
		/** Fallback GitHub repo URL if page map has no blob URL */
		git?: string;
		/** Max faces before "…" (default 8) */
		maxFaces?: number;
		/** @deprecated unused */
		avatar?: 'nixos' | 'nixcloud';
	};

	let {
		href,
		label,
		route,
		git = 'https://github.com/NixOS/nix',
		maxFaces = 8
	}: Props = $props();

	function normPath(p: string) {
		return (p || '/').replace(/\/$/, '') || '/';
	}

	const pageEntry = $derived.by((): PageEntry | null => {
		const key = normPath(route || page.url.pathname);
		const pages = (contributorsDoc as { pages?: Record<string, PageEntry> }).pages;
		return pages?.[key] ?? null;
	});

	const contributors = $derived.by((): Contributor[] => {
		const list = pageEntry?.contributors;
		return Array.isArray(list) ? list : [];
	});

	const visible = $derived(contributors.slice(0, maxFaces));
	const overflow = $derived(contributors.length > maxFaces);
	const hiddenCount = $derived(Math.max(0, contributors.length - maxFaces));

	/** Prefer per-file blob URL from map; else repo root from prop */
	const gitHref = $derived.by(() => {
		const blob = pageEntry?.github;
		if (blob) return blob;
		if (pageEntry?.repo) return `https://github.com/${pageEntry.repo}`;
		return git;
	});

	/**
	 * History page for this file (better for "see all authors").
	 * blob/… → commits/… when possible.
	 */
	const gitHistoryHref = $derived.by(() => {
		const blob = pageEntry?.github;
		if (blob && /\/blob\//.test(blob)) {
			return blob.replace('/blob/', '/commits/');
		}
		const repo = pageEntry?.repo;
		const path = pageEntry?.path;
		if (repo && path) {
			const ref = pageEntry?.ref || 'master';
			return `https://github.com/${repo}/commits/${ref}/${path}`;
		}
		return gitHref;
	});
</script>

<div class="nd-page-src-block">
	<div class="nd-page-src" dir="ltr">
		<span class="nd-page-src__label">منبع</span>
		<a
			class="nd-page-src__web"
			{href}
			rel="noopener noreferrer"
			target="_blank"
		>
			<span class="nd-page-src__url">{label}</span>
			<span class="nd-page-src__icon" aria-hidden="true">
				<Icon name="arrow-up-right" size={12} />
			</span>
		</a>
		<a
			class="nd-page-src__gh"
			href={gitHref}
			rel="noopener noreferrer"
			target="_blank"
			title="مشاهده در GitHub"
			aria-label="مشاهده منبع در GitHub"
		>
			<Icon name="github" size={18} />
		</a>
	</div>

	{#if contributors.length > 0}
		<div class="nd-page-contrib-row">
			<ul class="nd-page-contrib " dir="ltr" aria-label="مشارکت‌کنندگان صفحه">
				{#each visible as c (c.login)}
					<li>
						<a
							class="nd-page-contrib__person"
							href={c.url}
							rel="noopener noreferrer"
							target="_blank"
							title={`${c.name} (@${c.login})${c.commits ? ` · ${c.commits} commit` : ''}`}
							aria-label={`${c.name} (@${c.login})`}
						>
							<img
								class="nd-page-contrib__img"
								src={c.avatar}
								alt=""
								width="28"
								height="28"
								decoding="async"
								loading="lazy"
							/>
						</a>
					</li>
				{/each}
				{#if overflow}
					<li class="nd-page-contrib__more-item">
						<a
							class="nd-page-contrib__more"
							href={gitHistoryHref}
							rel="noopener noreferrer"
							target="_blank"
							title={`+${hiddenCount} نفر دیگر — مشاهده در GitHub`}
							aria-label={`و ${hiddenCount} مشارکت‌کننده دیگر؛ باز کردن در گیت‌هاب`}
						>
							…
						</a>
					</li>
				{/if}
			</ul>
			<span class="nd-page-contrib__label">مشارکت‌کنندگان</span>
		</div>
	{/if}
</div>


<style>

.nd-page-contrib  {
	margin-bottom: 0 !important;
}

.nd-page-contrib-row{
	padding-top:  1rem ;
}
.nd-page-contrib{
	direction : ltr;
}
</style>