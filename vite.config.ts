import { mdsvex } from 'mdsvex';
import adapterStatic from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, type Plugin } from 'vite';
import { highlightCode } from './src/lib/md-highlight';
import { remarkStripMdExt } from './src/lib/remark-strip-md-ext';
import { rehypeExtLinkIcons } from './src/lib/rehype-ext-link-icons';

const isWebxdc =
	process.env.WEBXDC === '1' ||
	process.env.VITE_WEBXDC === '1' ||
	process.env.VITE_WEBXDC === 'true';

/**
 * Prepend Fontiran license banner into production CSS that loads Peyda /
 * IRANYekanX. Vite minify strips normal comments; this runs after minify so
 * the codes exist in the deployed CSS file (not shown in the UI).
 */
function fontiranLicenseCssBanner(): Plugin {
	const banner = `/*!
 * Fontiran proprietary webfonts (self-hosted; not shown in UI).
 * This font is considered a proprietary software. See www.fontiran.com
 * --------------------------------------------------------------------------------------
 * Peyda FaNum Web v4 Pro — license: (7TJXCV0A) https://fontiran.com/license/7TJXCV0A
 * IRANYekanX FaNum — license: (L04ARHMJ) https://fontiran.com/license/L04ARHMJ
 * --------------------------------------------------------------------------------------
 */
`;
	return {
		name: 'fontiran-license-css-banner',
		apply: 'build',
		enforce: 'post',
		generateBundle(_opts, bundle) {
			for (const item of Object.values(bundle)) {
				if (item.type !== 'asset') continue;
				if (!item.fileName.endsWith('.css')) continue;
				const raw = item.source;
				const src = typeof raw === 'string' ? raw : Buffer.from(raw).toString('utf8');
				if (!src.includes('font-family:Peyda') && !src.includes('font-family: Peyda')) {
					continue;
				}
				if (src.includes('7TJXCV0A') && src.includes('/*!')) continue;
				item.source = banner + src;
			}
		}
	};
}

/** Shared prerender knobs: docs have legacy MyST links that 404 — don't fail the build. */
const prerenderOpts = {
	handleHttpError: 'warn' as const,
	handleMissingId: 'warn' as const,
	handleUnseenRoutes: 'ignore' as const,
	handleInvalidUrl: 'warn' as const,
	entries: ['*'] as ('*' | `/${string}`)[]
};

export default defineConfig({
	// ensure client code sees VITE_WEBXDC during webxdc builds
	envPrefix: ['VITE_'],
	plugins: [
		// After Kit emits CSS assets — production only (apply: 'build')
		fontiranLicenseCssBanner(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for app .svelte files. Leave mdsvex .md/.svx on defaults
				// (compiled output is classic Svelte, not runes).
				runes: ({ filename }) => {
					const parts = filename.split(/[/\\]/);
					if (parts.includes('node_modules')) return undefined;
					if (filename.endsWith('.md') || filename.endsWith('.svx')) return undefined;
					return true;
				}
			},

			// Static site: Cloudflare Pages (`build/`) or offline Webxdc (`build-webxdc/`)
			adapter: isWebxdc
				? adapterStatic({
						// fully self-contained offline package
						pages: 'build-webxdc',
						assets: 'build-webxdc',
						fallback: 'index.html',
						precompress: false,
						strict: false
					})
				: adapterStatic({
						// Cloudflare Pages (wrangler pages_build_output_dir)
						pages: 'build',
						assets: 'build',
						// SPA-style shell for client routes that miss a prerendered file
						fallback: '404.html',
						precompress: false,
						strict: false
					}),

			// relative asset URLs work when Webxdc serves from package root
			paths: isWebxdc ? { relative: true } : undefined,

			prerender: {
				...prerenderOpts,
				// Absolute OG/canonical URLs in static HTML when PUBLIC_SITE_URL is set
				origin:
					process.env.PUBLIC_SITE_URL?.replace(/\/$/, '') ||
					'https://nixy.a15d.at'
			},

			preprocess: [
				mdsvex({
					extensions: ['.svx', '.md'],
					// Keep ASCII quotes so Svelte brace escapes like {'{'} stay valid JS
					smartypants: false,
					// MyST/Sphinx links keep .md — strip for SvelteKit routes
					remarkPlugins: [remarkStripMdExt],
					// Prepend GitHub / YouTube icons on rendered anchors
					rehypePlugins: [rehypeExtLinkIcons],
					highlight: {
						highlighter: (code, lang) => highlightCode(code, lang ?? '')
					}
				})
			],
			extensions: ['.svelte', '.svx', '.md']
		})
	]
});
