<script lang="ts">
	import { blogPosts } from '$lib/blog-posts';
</script>

<header class="blog-page__header blog-page__header--index">
	<p class="blog-page__kicker">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			width="14"
			height="14"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			aria-hidden="true"
		>
			<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20" />
		</svg>
		یادداشت‌های نیکسی
	</p>
	<h1>وبلاگ</h1>
	<p class="blog-page__meta">
		یادداشت‌هایی دربارهٔ Nix، NixOS، ترجمهٔ فارسی، و ساخت همین سایت
	</p>
</header>

<ul class="blog-index" data-no-panel>
	{#each blogPosts as post}
		<li>
			<a class="blog-index__card" href={post.href} data-no-panel="1">
				<span class="blog-index__kicker">{post.kicker}</span>
				<span class="blog-index__title">{post.title}</span>
				<span class="blog-index__desc">{post.description}</span>
			</a>
		</li>
	{/each}
</ul>
