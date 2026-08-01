/**
 * Secondary panel for in-app page peeks:
 * wide → split (physical left), narrow → overlay drawer.
 *
 * Open/close is instant in JS; sequencing is pure CSS
 * (see --iap-* timing vars in app.css).
 */

import { isNoPanelPath } from '$lib/no-panel-paths';
import { normalizeDocPathname } from '$lib/normalize-doc-href';

/** Viewport width at which split mode is used (expand). Below → drawer. */
export const PANEL_SPLIT_MIN = 1100;

export type PanelMode = 'split' | 'drawer';

const PANEL_WIDTH_KEY = 'nixi-panel-width';
/** Min / max panel width (px) when resizing on desktop split. */
export const PANEL_WIDTH_MIN = 280;
export const PANEL_WIDTH_MAX_MAIN = 360; // leave at least this for main column

function panelModeForWidth(w: number): PanelMode {
	return w >= PANEL_SPLIT_MIN ? 'split' : 'drawer';
}

function defaultPanelWidthPx(): number {
	if (typeof window === 'undefined') return 480;
	const rem = parseFloat(getComputedStyle(document.documentElement).fontSize || '16') || 16;
	return Math.round(Math.min(window.innerWidth * 0.5, 36 * rem));
}

function clampPanelWidth(px: number): number {
	if (typeof window === 'undefined') {
		return Math.max(PANEL_WIDTH_MIN, Math.min(px, 720));
	}
	const max = Math.max(
		PANEL_WIDTH_MIN,
		Math.min(window.innerWidth * 0.85, window.innerWidth - PANEL_WIDTH_MAX_MAIN)
	);
	return Math.round(Math.max(PANEL_WIDTH_MIN, Math.min(px, max)));
}

function normalizePath(p: string): string {
	// also drop .md / index leftovers from MyST links
	return normalizeDocPathname(p.replace(/\/$/, '') || '/');
}

class InAppPanel {
	/** Absolute path + search + hash to show in the panel (null = closed). */
	href = $state<string | null>(null);
	mode = $state<PanelMode>('split');
	/** Desktop split panel width in px (right edge is the resize handle). */
	widthPx = $state(480);
	/** True while user is dragging the panel edge. */
	resizing = $state(false);
	/** Bumps when the same href is opened again so the iframe reloads. */
	generation = $state(0);
	/**
	 * Main page scroll (window) saved when the panel first opens.
	 * Restored on open animation + close — never re-captured while open.
	 */
	savedScrollY = $state(0);
	/** True after capture until close restores (avoids overwriting with 0). */
	private hasSavedScroll = false;
	private restoreTimers: ReturnType<typeof setTimeout>[] = [];
	private pinUntil = 0;
	private onScrollPin: (() => void) | null = null;

	get open() {
		return this.href != null && this.href !== '';
	}

	get splitActive() {
		return this.open && this.mode === 'split';
	}

	get drawerActive() {
		return this.open && this.mode === 'drawer';
	}

	/** Load saved width and push CSS var (call once on app mount). */
	initWidth() {
		if (typeof window === 'undefined') return;
		let w = defaultPanelWidthPx();
		try {
			const raw = localStorage.getItem(PANEL_WIDTH_KEY);
			if (raw) {
				const n = Number(raw);
				if (Number.isFinite(n) && n > 0) w = n;
			}
		} catch {
			/* ignore */
		}
		this.setWidth(w, { persist: false });
	}

	/** Apply width to state + `--iap-panel-w` (and optionally localStorage). */
	setWidth(px: number, opts: { persist?: boolean } = {}) {
		const w = clampPanelWidth(px);
		this.widthPx = w;
		if (typeof document !== 'undefined') {
			document.documentElement.style.setProperty('--iap-panel-w', `${w}px`);
		}
		if (opts.persist !== false && typeof localStorage !== 'undefined') {
			try {
				localStorage.setItem(PANEL_WIDTH_KEY, String(w));
			} catch {
				/* ignore */
			}
		}
	}

	syncMode() {
		if (typeof window === 'undefined') return;
		this.mode = panelModeForWidth(window.innerWidth);
		// Keep width legal if viewport shrank
		if (this.mode === 'split') this.setWidth(this.widthPx, { persist: false });
	}

	/** Read the real main-page scroller (window — shell-main is not overflow:auto). */
	private readWindowScroll(): number {
		if (typeof window === 'undefined') return 0;
		return (
			window.scrollY ||
			document.documentElement.scrollTop ||
			document.body.scrollTop ||
			0
		);
	}

	captureScroll() {
		if (typeof window === 'undefined') return;
		// Only capture when panel is closed / first open — keep while open
		this.savedScrollY = this.readWindowScroll();
		this.hasSavedScroll = true;
	}

	private clearRestoreTimers() {
		for (const t of this.restoreTimers) clearTimeout(t);
		this.restoreTimers = [];
		if (this.onScrollPin && typeof window !== 'undefined') {
			window.removeEventListener('scroll', this.onScrollPin, true);
			this.onScrollPin = null;
		}
		this.pinUntil = 0;
	}

	private applySavedScroll() {
		if (typeof window === 'undefined' || !this.hasSavedScroll) return;
		const y = this.savedScrollY;
		// Always window — do NOT zero window and write shell-main.scrollTop
		// (shell-main is not a scroll container; that was wiping scroll).
		window.scrollTo({ top: y, left: 0, behavior: 'instant' as ScrollBehavior });
		document.documentElement.scrollTop = y;
		document.body.scrollTop = y;
	}

	private armScrollPin(ms = 520) {
		if (typeof window === 'undefined') return;
		this.pinUntil = performance.now() + ms;
		if (!this.onScrollPin) {
			this.onScrollPin = () => {
				if (performance.now() > this.pinUntil) return;
				this.applySavedScroll();
			};
			window.addEventListener('scroll', this.onScrollPin, { capture: true, passive: true });
		}
		this.restoreTimers.push(
			setTimeout(() => {
				if (this.onScrollPin) {
					window.removeEventListener('scroll', this.onScrollPin, true);
					this.onScrollPin = null;
				}
			}, ms + 40)
		);
	}

	/**
	 * Pin main page scroll to savedScrollY.
	 * Re-applies across frames + layout/margin animation so the browser
	 * cannot jump the main pane when the left panel opens.
	 */
	restoreScroll() {
		if (typeof window === 'undefined') return;
		if (!this.hasSavedScroll) return;

		this.clearRestoreTimers();

		this.applySavedScroll();
		requestAnimationFrame(() => {
			this.applySavedScroll();
			requestAnimationFrame(() => this.applySavedScroll());
		});
		// Cover margin/panel CSS transition (~0.1s delay + 0.26s dur)
		for (const ms of [16, 50, 100, 180, 280, 400, 520]) {
			this.restoreTimers.push(setTimeout(() => this.applySavedScroll(), ms));
		}
		this.armScrollPin(520);
	}

	openHref(href: string) {
		this.syncMode();
		// Capture only on first open; switching panel pages must keep scroll
		if (!this.open) {
			this.captureScroll();
		}
		this.href = href;
		this.generation += 1;
		// Layout class flips immediately; CSS runs the timed sequence
		this.restoreScroll();
	}

	close() {
		// Do NOT re-capture — while open, window may have been nudged; keep original
		this.href = null;
		this.restoreScroll();
		// After restore pulses finish, allow a fresh capture on next open
		this.restoreTimers.push(
			setTimeout(() => {
				this.applySavedScroll();
				this.hasSavedScroll = false;
			}, 560)
		);
	}

	/** URL loaded inside the iframe (adds embed=1). */
	embedSrc(): string | null {
		if (!this.href) return null;
		try {
			const u = new URL(
				this.href,
				typeof location !== 'undefined' ? location.origin : 'http://local'
			);
			u.searchParams.set('embed', '1');
			return u.pathname + u.search + u.hash;
		} catch {
			return this.href;
		}
	}

	/** Clean path for “open full page” (no embed). */
	fullHref(): string | null {
		if (!this.href) return null;
		try {
			const u = new URL(
				this.href,
				typeof location !== 'undefined' ? location.origin : 'http://local'
			);
			u.searchParams.delete('embed');
			return u.pathname + u.search + u.hash;
		} catch {
			return this.href;
		}
	}
}

export const inAppPanel = new InAppPanel();

/** True when this document is the panel iframe (or ?embed=1). */
export function isEmbedContext(): boolean {
	if (typeof window === 'undefined') return false;
	try {
		if (window.self !== window.top) return true;
	} catch {
		return true;
	}
	const q = new URLSearchParams(window.location.search);
	return q.get('embed') === '1';
}

/**
 * True only for links in the page *body* (prose / article text).
 * Top / bottom / right nav and other chrome always navigate normally.
 */
export function isInPageContentLink(anchor: HTMLAnchorElement): boolean {
	if (anchor.dataset.noPanel === '1' || anchor.dataset.noPanel === '') return false;
	if (anchor.closest('[data-no-panel]')) return false;
	// Hub landing cards always full-page navigate
	if (anchor.classList.contains('nd-hub-card') || anchor.closest('.nd-hub-cards')) return false;

	if (
		anchor.closest(
			[
				'.top',
				'.drawer',
				'.foot',
				'.iap',
				'.iap__bar',
				'.iap__resize',
				'.nd-nav',
				'.nd-nav-toggle',
				'.nd-nav-backdrop',
				'.nd-pager',
				'.nd-page-src-block',
				'.nd-page-src',
				'.nd-page-src__gh',
				'.nd-page-contrib-row',
				'.nd-page-contrib',
				'.nd-hub-cards',
				'.lesson__tabs',
				'.ton-doc-nav',
				'.ton-ide-bar',
				'.ton-actions',
				'.ton-out-resize',
				'.ton-out-head',
				'.ton-src',
				'.home__list',
				'nav',
				'header',
				'footer'
			].join(', ')
		)
	) {
		return false;
	}

	// Paths listed in NO_PANEL_PATHS (exact match only)
	try {
		if (typeof location !== 'undefined' && isNoPanelPath(location.pathname)) {
			return false;
		}
	} catch {
		/* ignore */
	}

	const body = anchor.closest(
		[
			'main.content .prose',
			'main.content .nd-article',
			'main.content .doc-page',
			'main.content .ton-doc-body',
			'main.content .eg',
			'main.content article',
			'.embed-shell .prose',
			'.embed-shell .nd-article',
			'.embed-shell article'
		].join(', ')
	);
	return !!body;
}

/**
 * Resolve an <a href> to an in-app path+search+hash if we should open it in the panel.
 * Returns null when the click should use normal navigation.
 */
export function resolveInAppPanelHref(
	anchor: HTMLAnchorElement,
	currentPathname: string,
	currentSearch = ''
): string | null {
	if (!isInPageContentLink(anchor)) return null;

	const raw = anchor.getAttribute('href');
	if (raw == null || raw === '' || raw.startsWith('mailto:') || raw.startsWith('tel:')) {
		return null;
	}

	if (anchor.target === '_blank' || anchor.hasAttribute('download')) return null;

	const cur = normalizePath(currentPathname);
	const curSearch = currentSearch || (typeof location !== 'undefined' ? location.search : '');

	// Same-page section links (#names-values) → NEVER panel; scroll in-page instead
	if (raw.startsWith('#')) {
		return null;
	}

	let url: URL;
	try {
		url = new URL(raw, typeof location !== 'undefined' ? location.href : 'http://local/');
	} catch {
		return null;
	}

	if (typeof location !== 'undefined' && url.origin !== location.origin) return null;
	if (url.searchParams.get('embed') === '1') return null;

	const path = normalizePath(url.pathname);

	// Same document (path + query), even with #hash → stay on page, no panel
	if (path === cur && url.search === curSearch) {
		return null;
	}

	// Different in-app page → left panel / drawer
	return path + url.search + url.hash;
}
