/** Shared blog post catalog (index + nav + SEO helpers). */
export type BlogPost = {
	href: string;
	title: string;
	description: string;
	kicker: string;
};

export const blogPosts: BlogPost[] = [
	{
		href: '/blog/do-not-be-afraid-of-ai',
		title: 'از هوش مصنوعی نترسید',
		description:
			'چرا AI ترسناک نیست و چطور می‌توانیم با کنترل انسانی از آن برای یادگیری و زندگی بهتر استفاده کنیم',
		kicker: 'صفحه · هوش مصنوعی'
	},
	{
		href: '/blog/how-we-build-this-website',
		title: 'چگونه این وب‌سایت را ساختیم',
		description:
			'معماری نیکسی، ترجمه‌ی کنترل‌شده با AI، واژه‌نامه، و ویرایشگر داخلی Markdown',
		kicker: 'یادداشت · ساخت سایت'
	}
];

export const blogPostMetaByPath: Record<string, { title: string; description: string }> =
	Object.fromEntries(
		blogPosts.map((p) => [p.href, { title: p.title, description: p.description }])
	);
