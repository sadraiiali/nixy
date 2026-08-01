<script lang="ts">
	import { browser } from '$app/environment';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import Icon from '$lib/components/Icon.svelte';
	import LinkCopyModal from '$lib/components/LinkCopyModal.svelte';
	import MonacoEditor from '$lib/components/MonacoEditor.svelte';
	import { marked, Renderer } from 'marked';
	import { extLinkKind } from '$lib/ext-link-kind';
	import { enhanceExtLinkIcons } from '$lib/ext-link-icons';
	import { highlightCodeHtml } from '$lib/md-highlight';
	import { formatNix } from '$lib/tour/nix-format';
	import { loadNixRuntime, runNixExercise, type NixRunResult } from '$lib/tour/nix-eval';
	import { isExternalHref } from '$lib/webxdc';

	/** Prism Nix/Bash/etc. for fenced blocks in the lesson pane (same CSS as mdsvex). */
	const lessonRenderer = new Renderer();
	lessonRenderer.code = ({ text, lang }) => highlightCodeHtml(text, lang ?? '');

	type Lesson = {
		topic: string;
		path: string;
		question: string;
		code: string;
		solution: string;
		youtube?: string;
	};

	let lessons = $state<Lesson[]>([]);
	let index = $state(0);
	let code = $state('');
	let output = $state('');
	let outputKind = $state<'idle' | 'ok' | 'bad' | 'err' | 'run'>('idle');
	let showSolution = $state(false);
	let solutionText = $state('');
	let status = $state('در حال آماده‌سازی…');
	let nixReady = $state(false);
	let running = $state(false);
	let loadError = $state('');
	/** Right lesson pane — scroll to top on next/prev */
	let docPaneEl: HTMLElement | undefined = $state();
	/** Left IDE column (for clamping output height) */
	let idePaneEl: HTMLElement | undefined = $state();
	/** Highlight left (ide) or right (doc) pane when hovering text refs */
	let highlightPane = $state<'ide' | 'doc' | null>(null);
	/** External links in lesson text → modal (tour only) */
	let extLinkOpen = $state(false);
	let extLinkHref = $state('');
	/** Full lesson index overlay on the right (doc) pane */
	let showLessonPicker = $state(false);
	let lessonListEl: HTMLElement | undefined = $state();

	/** Resizable output panel height (px), persisted */
	const OUT_H_KEY = 'nixi-tour-out-h';
	const OUT_H_MIN = 64;
	const OUT_H_DEFAULT = 120;
	let outHeightPx = $state(OUT_H_DEFAULT);
	let outResizing = $state(false);
	let outDragStartY = 0;
	let outDragStartH = 0;

	function clampOutHeight(px: number): number {
		const paneH = idePaneEl?.clientHeight ?? (browser ? window.innerHeight : 600);
		// Leave room for toolbar + Monaco + action buttons
		const max = Math.max(OUT_H_MIN, paneH - 220);
		return Math.round(Math.max(OUT_H_MIN, Math.min(px, max)));
	}

	function setOutHeight(px: number, persist = true) {
		const next = clampOutHeight(px);
		outHeightPx = next;
		if (persist && browser) {
			try {
				localStorage.setItem(OUT_H_KEY, String(next));
			} catch {
				/* ignore */
			}
		}
	}

	function onOutResizePointerDown(e: PointerEvent) {
		e.preventDefault();
		e.stopPropagation();
		outDragStartY = e.clientY;
		outDragStartH = outHeightPx;
		outResizing = true;
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
		document.documentElement.classList.add('ton-out-resizing');
	}

	function onOutResizePointerMove(e: PointerEvent) {
		if (!outResizing) return;
		// Handle is above the output: drag up → taller output
		const next = outDragStartH + (outDragStartY - e.clientY);
		setOutHeight(next, false);
	}

	function onOutResizePointerUp(e: PointerEvent) {
		if (!outResizing) return;
		outResizing = false;
		document.documentElement.classList.remove('ton-out-resizing');
		setOutHeight(outHeightPx, true);
		try {
			(e.currentTarget as HTMLElement).releasePointerCapture(e.pointerId);
		} catch {
			/* ignore */
		}
	}

	function onOutResizeKey(e: KeyboardEvent) {
		const step = e.shiftKey ? 40 : 12;
		if (e.key === 'ArrowUp') {
			e.preventDefault();
			setOutHeight(outHeightPx + step);
		} else if (e.key === 'ArrowDown') {
			e.preventDefault();
			setOutHeight(outHeightPx - step);
		} else if (e.key === 'Home') {
			e.preventDefault();
			setOutHeight(OUT_H_MIN);
		} else if (e.key === 'End') {
			e.preventDefault();
			setOutHeight(9999);
		}
	}

	$effect(() => {
		if (!browser) return;
		try {
			const raw = localStorage.getItem(OUT_H_KEY);
			const n = raw != null ? Number(raw) : NaN;
			if (Number.isFinite(n)) outHeightPx = clampOutHeight(n);
		} catch {
			/* ignore */
		}
		const onWinResize = () => setOutHeight(outHeightPx, false);
		window.addEventListener('resize', onWinResize);
		return () => window.removeEventListener('resize', onWinResize);
	});

	const lesson = $derived(lessons[index] ?? null);
	const questionHtml = $derived.by(() => {
		if (!lesson) return '';
		try {
			// GFM + Prism fences (nix fences in «کد اولیه» / «راه حل»)
			let html = marked.parse(lesson.question, {
				async: false,
				gfm: true,
				breaks: false,
				renderer: lessonRenderer
			}) as string;
			// Ensure external anchors open via our modal (no target=_blank hijack)
			// + inject GitHub / YouTube icon spans
			html = html.replace(
				/<a\s+([^>]*?)href="(https?:\/\/[^"]+)"([^>]*)>/gi,
				(_m, pre, href, post) => {
					const attrs = `${pre}${post}`
						.replace(/\s*target="[^"]*"/gi, '')
						.replace(/\s*rel="[^"]*"/gi, '');
					const kind = extLinkKind(href);
					const icon = kind
						? `<span class="ext-link-icon ext-link-icon--${kind}" aria-hidden="true"></span>`
						: '';
					return `<a ${attrs} href="${href}" class="ton-ext-link" data-ton-ext="1">${icon}`;
				}
			);
			// Desktop hover: highlight the matching pane (left = code, right = lesson)
			html = html
				.replace(
					/پنل سمت چپ/g,
					'<span class="ton-pane-ref" data-ton-pane="ide" tabindex="0">پنل سمت چپ</span>'
				)
				.replace(
					/پنل سمت راست/g,
					'<span class="ton-pane-ref" data-ton-pane="doc" tabindex="0">پنل سمت راست</span>'
				);
			return html;
		} catch {
			return `<pre>${lesson.question}</pre>`;
		}
	});

	function pathToIndex(path: string | null) {
		if (!path || !lessons.length) return 0;
		const i = lessons.findIndex((l) => l.path === path);
		return i >= 0 ? i : 0;
	}

	/** searchParams throws during prerender */
	function lessonIdFromUrl(): string | null {
		try {
			return page.url.searchParams.get('id');
		} catch {
			return null;
		}
	}

	// After lesson HTML paints, stamp any remaining host icons
	$effect(() => {
		if (!browser) return;
		void questionHtml;
		void index;
		requestAnimationFrame(() => {
			if (docPaneEl) enhanceExtLinkIcons(docPaneEl);
		});
	});

	function scrollDocToTop() {
		if (!browser) return;
		const el = docPaneEl;
		if (el) {
			el.scrollTop = 0;
			el.scrollTo?.({ top: 0, left: 0, behavior: 'instant' as ScrollBehavior });
		}
		// Phone: whole page scrolls — jump to the lesson (top), not the editor
		const narrow = window.matchMedia('(max-width: 900px)').matches;
		if (narrow) {
			const target = el ?? document.querySelector('.ton-app');
			if (target instanceof HTMLElement) {
				const y = target.getBoundingClientRect().top + window.scrollY - 8;
				window.scrollTo({ top: Math.max(0, y), left: 0, behavior: 'instant' });
			} else {
				window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
			}
		}
		requestAnimationFrame(() => {
			if (docPaneEl) docPaneEl.scrollTop = 0;
		});
	}

	function paneFromEventTarget(t: EventTarget | null): 'ide' | 'doc' | null {
		if (!(t instanceof Element)) return null;
		const ref = t.closest('[data-ton-pane]');
		if (!(ref instanceof HTMLElement)) return null;
		const v = ref.dataset.tonPane;
		return v === 'ide' || v === 'doc' ? v : null;
	}

	function onDocBodyPointerOver(e: PointerEvent) {
		const pane = paneFromEventTarget(e.target);
		if (pane) highlightPane = pane;
	}

	function onDocBodyPointerOut(e: PointerEvent) {
		const from = paneFromEventTarget(e.target);
		if (!from) return;
		const to = paneFromEventTarget(e.relatedTarget);
		if (to === from) return;
		if (highlightPane === from) highlightPane = null;
	}

	function onDocBodyFocusIn(e: FocusEvent) {
		const pane = paneFromEventTarget(e.target);
		if (pane) highlightPane = pane;
	}

	function onDocBodyFocusOut(e: FocusEvent) {
		const from = paneFromEventTarget(e.target);
		if (!from) return;
		const to = paneFromEventTarget(e.relatedTarget);
		if (to === from) return;
		if (highlightPane === from) highlightPane = null;
	}

	/** Tour-only: external links in the lesson pane open a center modal */
	function onDocBodyClick(e: MouseEvent) {
		if (!browser) return;
		const t = e.target;
		if (!(t instanceof Element)) return;
		const a = t.closest('a');
		if (!(a instanceof HTMLAnchorElement)) return;
		// footer / youtube under doc also use same handler if bubbled from body only
		const href = a.getAttribute('href');
		if (!isExternalHref(href)) return;
		e.preventDefault();
		e.stopPropagation();
		e.stopImmediatePropagation();
		extLinkHref = href!.startsWith('//') ? `https:${href}` : href!;
		extLinkOpen = true;
	}

	function setLesson(i: number, pushUrl = true) {
		if (!lessons.length) return;
		const next = Math.max(0, Math.min(lessons.length - 1, i));
		const changed = next !== index;
		index = next;
		const L = lessons[index]!;
		code = L.code ?? '';
		solutionText = L.solution ?? '';
		showSolution = false;
		output = '';
		outputKind = 'idle';
		highlightPane = null;
		if (changed || pushUrl) scrollDocToTop();
		if (pushUrl && browser) {
			const url = new URL(page.url);
			url.searchParams.set('id', L.path);
			goto(`${url.pathname}?${url.searchParams.toString()}`, {
				replaceState: false,
				keepFocus: true,
				noScroll: true
			});
		}
	}

	async function init() {
		try {
			status = 'بارگذاری درس‌ها…';
			const res = await fetch('/tour-of-nix/questions.fa.json');
			if (!res.ok) throw new Error('questions.fa.json');
			lessons = (await res.json()) as Lesson[];
			const id = lessonIdFromUrl();
			setLesson(pathToIndex(id), !id);

			status = 'بارگذاری مفسر Nix (اولین بار ~۲۵MB، فقط بار اول)…';
			await loadNixRuntime((s) => {
				if (s) status = s;
			});
			nixReady = true;
			status = '';
		} catch (e) {
			loadError = e instanceof Error ? e.message : String(e);
			status = '';
		}
	}

	$effect(() => {
		if (!browser) return;
		void init();
	});

	// react to browser back/forward
	$effect(() => {
		const id = lessonIdFromUrl();
		// also re-run when pathname/search identity changes
		void page.url.pathname;
		void page.url.search;
		if (!lessons.length || !id) return;
		const i = pathToIndex(id);
		if (i !== index) setLesson(i, false);
	});

	async function onRun() {
		if (!lesson || running) return;
		running = true;
		outputKind = 'run';
		output = 'در حال اجرا…';
		try {
			const result: NixRunResult = await runNixExercise(code, lesson.solution || code);
			if (!result.ok) {
				output = result.output || result.error || 'خطا';
				outputKind = 'err';
			} else if (result.match) {
				output = result.output;
				outputKind = 'ok';
			} else {
				output = result.output;
				outputKind = 'bad';
			}
		} catch (e) {
			output = e instanceof Error ? e.message : String(e);
			outputKind = 'err';
		} finally {
			running = false;
		}
	}

	function onReset() {
		if (!lesson) return;
		code = lesson.code ?? '';
		output = '';
		outputKind = 'idle';
		showSolution = false;
	}

	function onFormat() {
		if (!lesson) return;
		// Same formatter as Monaco Ctrl+Shift+I
		code = formatNix(code, { indentSize: 2 });
	}

	function openHelp() {
		if (!lesson) return;
		showSolution = true;
	}

	function closeHelp() {
		showSolution = false;
	}

	function onToggleSolution() {
		if (showSolution) closeHelp();
		else openHelp();
	}

	function openLessonPicker() {
		if (!lessons.length) return;
		showLessonPicker = true;
		requestAnimationFrame(() => {
			const active = lessonListEl?.querySelector<HTMLElement>('[aria-current="true"]');
			active?.focus();
			active?.scrollIntoView({ block: 'nearest' });
		});
	}

	function closeLessonPicker() {
		showLessonPicker = false;
	}

	function pickLesson(i: number) {
		closeLessonPicker();
		setLesson(i);
	}

	function onKey(e: KeyboardEvent) {
		if (showLessonPicker && e.key === 'Escape') {
			e.preventDefault();
			closeLessonPicker();
			return;
		}
		if (showSolution && e.key === 'Escape') {
			e.preventDefault();
			closeHelp();
			return;
		}
		if (extLinkOpen && e.key === 'Escape') {
			e.preventDefault();
			extLinkOpen = false;
			return;
		}
		// Ctrl/Cmd+Enter or Shift+Enter → run (works outside Monaco too)
		if (
			e.key === 'Enter' &&
			(e.ctrlKey || e.metaKey || e.shiftKey) &&
			!e.altKey
		) {
			e.preventDefault();
			void onRun();
			return;
		}
		// Shift+J next · Shift+K prev (lesson pager)
		if (e.shiftKey && !e.ctrlKey && !e.metaKey && !e.altKey) {
			const k = e.key.toLowerCase();
			// Allow even when Monaco focused — matches vim-ish nav outside typing letters without shift in editor
			if (k === 'j') {
				e.preventDefault();
				setLesson(index + 1);
			} else if (k === 'k') {
				e.preventDefault();
				setLesson(index - 1);
			}
		}
	}
</script>

<svelte:window onkeydown={onKey} />

<svelte:head>
	<title>
		{lesson ? `${index + 1}. ${lesson.topic}` : 'تور نیکس'} · نیکسی
	</title>
</svelte:head>

{#if loadError}
	<div class="ton-err">
		<p>بارگذاری تور ناموفق بود: {loadError}</p>
		<p>
			<a href="https://nixcloud.io/tour/" dir="ltr">نسخهٔ اصلی</a>
		</p>
	</div>
{:else}
	<div class="ton-app" class:ton-app--hl-ide={highlightPane === 'ide'} class:ton-app--hl-doc={highlightPane === 'doc'}>
		<!-- LEFT: terminal / editor (physical left, LTR) -->
		<section
			class="ton-pane ton-pane--ide"
			class:ton-pane--hl={highlightPane === 'ide'}
			class:ton-pane--ide-resizing={outResizing}
			dir="ltr"
			aria-label="پنل سمت چپ — ویرایشگر و ترمینال"
			bind:this={idePaneEl}
			style:--ton-out-h="{outHeightPx}px"
		>
			<div class="ton-ide-bar">
				<span class="ton-ide-bar__title">nix-instantiate</span>
				<span class="ton-ide-bar__meta" dir="ltr">
					{nixReady ? 'ready' : status || 'loading…'}
				</span>
			</div>

			<span class="ton-sr" id="ton-code-label">Nix code</span>
			<MonacoEditor
				class="ton-code"
				value={code}
				language="nix"
				disabled={!lesson}
				onChange={(v) => {
					code = v;
				}}
				onRun={() => {
					void onRun();
				}}
			/>

			<div class="ton-actions">
				<button type="button" class="ton-btn" onclick={onReset} disabled={!lesson}>
					<Icon name="rotate-ccw" size={14} />
					ریست
				</button>
				<button
					type="button"
					class="ton-btn"
					onclick={onFormat}
					disabled={!lesson}
					title="Format · Ctrl+Shift+I · Shift+Alt+F"
				>
					<Icon name="type" size={14} />
					فرمت
				</button>
				<button
					type="button"
					class="ton-btn"
					onclick={onToggleSolution}
					disabled={!lesson}
					aria-haspopup="dialog"
					aria-expanded={showSolution}
				>
					<Icon name="circle-help" size={14} />
					راهنما
				</button>
				<button
					type="button"
					class="ton-btn ton-btn--run"
					onclick={onRun}
					disabled={!lesson || !nixReady || running}
					title="Ctrl+Enter"
				>
					{#if running}
						<Icon name="loader-circle" size={14} class="ton-btn__spin" />
						در حال اجرا…
					{:else}
						<Icon name="play" size={14} />
						اجرا
					{/if}
				</button>
			</div>

			<div class="ton-out-head">
				<button
					type="button"
					class="ton-out-resize"
					class:ton-out-resize--active={outResizing}
					aria-label={`تغییر ارتفاع خروجی (${outHeightPx}px)`}
					title="کشیدن برای تغییر ارتفاع خروجی · دوبار کلیک = پیش‌فرض"
					onpointerdown={onOutResizePointerDown}
					onpointermove={onOutResizePointerMove}
					onpointerup={onOutResizePointerUp}
					onpointercancel={onOutResizePointerUp}
					onkeydown={onOutResizeKey}
					ondblclick={() => setOutHeight(OUT_H_DEFAULT)}
				></button>
				<label class="ton-label" for="ton-out">output</label>
			</div>
			<textarea
				id="ton-out"
				class="ton-out"
				class:ton-out--ok={outputKind === 'ok'}
				class:ton-out--bad={outputKind === 'bad'}
				class:ton-out--err={outputKind === 'err'}
				class:ton-out--run={outputKind === 'run'}
				readonly
				spellcheck="false"
				value={output}
				style:height="{outHeightPx}px"
				placeholder={nixReady ? 'نتیجهٔ ارزیابی اینجا نمایش داده می‌شود' : 'صبر کنید تا مفسر آماده شود…'}
			></textarea>
		</section>

		<!-- RIGHT: lesson text (Farsi RTL) -->
		<!-- svelte-ignore a11y_no_static_element_interactions a11y_click_events_have_key_events -->
		<section
			class="ton-pane ton-pane--doc"
			class:ton-pane--hl={highlightPane === 'doc'}
			class:ton-pane--doc-picker={showLessonPicker}
			dir="rtl"
			aria-label="پنل سمت راست — متن درس"
			bind:this={docPaneEl}
			onclickcapture={onDocBodyClick}
		>
			<div class="ton-doc-nav">
				<button
					type="button"
					class="ton-btn"
					onclick={() => setLesson(index + 1)}
					disabled={!lessons.length || index >= lessons.length - 1}
					title="Shift+J"
				>
					<Icon name="arrow-right" size={14} />
					بعدی
				</button>
				<button
					type="button"
					class="ton-doc-nav__count"
					dir="ltr"
					disabled={!lessons.length}
					aria-haspopup="dialog"
					aria-expanded={showLessonPicker}
					title="فهرست درس‌ها"
					onclick={openLessonPicker}
				>
					{lessons.length ? `${index + 1} / ${lessons.length}` : '—'}
				</button>
				<button
					type="button"
					class="ton-btn"
					onclick={() => setLesson(index - 1)}
					disabled={index <= 0}
					title="Shift+K"
				>
					قبلی
					<Icon name="arrow-left" size={14} />
				</button>
			</div>

			{#if lesson}
				<h1 class="ton-doc-title">{lesson.topic}</h1>
				<!-- svelte-ignore a11y_no_static_element_interactions -->
				<div
					class="ton-doc-body prose prose-fa"
					role="region"
					aria-label="متن درس"
					onpointerover={onDocBodyPointerOver}
					onpointerout={onDocBodyPointerOut}
					onfocusin={onDocBodyFocusIn}
					onfocusout={onDocBodyFocusOut}
				>
					{@html questionHtml}
				</div>
				{#if lesson.youtube}
					<p class="ton-yt">
						<a href={lesson.youtube} class="ton-ext-link" data-ton-ext="1" dir="ltr">
							YouTube
							<Icon name="arrow-up-right" size={12} />
						</a>
					</p>
				{/if}
			{:else}
				<p class="ton-doc-loading">{status || 'بارگذاری…'}</p>
			{/if}

			<p class="ton-src">
				<a href="https://nixcloud.io/tour/" class="ton-ext-link" data-ton-ext="1" dir="ltr">
					nixcloud.io/tour
					<Icon name="arrow-up-right" size={12} />
				</a>
				·
				<a
					href="https://github.com/nixcloud/tour_of_nix"
					class="ton-ext-link"
					data-ton-ext="1"
					dir="ltr"
				>
					github.com/nixcloud/tour_of_nix
				</a>
			</p>

			{#if showLessonPicker}
				<div class="ton-lesson-picker" role="presentation">
					<button
						type="button"
						class="ton-lesson-picker__mask"
						aria-label="بستن فهرست درس‌ها"
						onclick={closeLessonPicker}
					></button>
					<div
						class="ton-lesson-picker__panel"
						role="dialog"
						aria-modal="true"
						aria-labelledby="ton-lesson-picker-title"
					>
						<header class="ton-lesson-picker__head">
							<div>
								<p class="ton-lesson-picker__kicker" dir="ltr">
									{index + 1} / {lessons.length}
								</p>
								<h2 id="ton-lesson-picker-title" class="ton-lesson-picker__title">
									فهرست درس‌ها
								</h2>
							</div>
							<button
								type="button"
								class="ton-lesson-picker__x"
								aria-label="بستن"
								onclick={closeLessonPicker}
							>
								<Icon name="x" size={18} />
							</button>
						</header>
						<ol class="ton-lesson-picker__list" bind:this={lessonListEl}>
							{#each lessons as L, i}
								<li>
									<button
										type="button"
										class="ton-lesson-picker__item"
										class:is-current={i === index}
										aria-current={i === index ? 'true' : undefined}
										onclick={() => pickLesson(i)}
									>
										<span class="ton-lesson-picker__num" dir="ltr">{i + 1}</span>
										<span class="ton-lesson-picker__topic">{L.topic || L.path}</span>
										<span class="ton-lesson-picker__path" dir="ltr">{L.path}</span>
									</button>
								</li>
							{/each}
						</ol>
					</div>
				</div>
			{/if}
		</section>
	</div>
{/if}

<LinkCopyModal bind:open={extLinkOpen} href={extLinkHref} variant="browser" />

{#if showSolution && lesson}
	<div class="ton-help" role="presentation">
		<button type="button" class="ton-help__backdrop" aria-label="بستن" onclick={closeHelp}
		></button>
		<div
			class="ton-help__panel"
			role="dialog"
			aria-modal="true"
			aria-labelledby="ton-help-title"
		>
			<header class="ton-help__head">
				<div class="ton-help__head-text">
					<p class="ton-help__kicker">راهنما</p>
					<h2 id="ton-help-title" class="ton-help__title">{lesson.topic}</h2>
				</div>
				<button type="button" class="ton-help__x" aria-label="بستن" onclick={closeHelp}>
					<Icon name="x" size={18} />
				</button>
			</header>
			<p class="ton-help__hint">
				راه‌حل پیشنهادی این درس. می‌توانید کپی کنید و در ویرایشگر امتحان کنید.
			</p>
			<pre class="ton-help__code" dir="ltr"><code>{solutionText || '—'}</code></pre>
			<div class="ton-help__actions">
				<button
					type="button"
					class="ton-help__btn ton-help__btn--primary"
					onclick={() => {
						if (solutionText) {
							code = solutionText;
							closeHelp();
						}
					}}
				>
					استفاده در ویرایشگر
				</button>
				<button type="button" class="ton-help__btn" onclick={closeHelp}>بستن</button>
			</div>
		</div>
	</div>
{/if}
