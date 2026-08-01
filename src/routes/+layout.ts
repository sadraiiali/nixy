import { isWebxdc } from '$lib/webxdc';

// Fully static export for Cloudflare Pages + Webxdc.
// (url.searchParams is only read behind browser/try guards in layouts.)
export const prerender = true;

// Webxdc packages prefer trailing slashes; site uses no trailing slash.
export const trailingSlash = isWebxdc ? 'always' : 'never';
