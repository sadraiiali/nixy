<script lang="ts">
	import { goto } from '$app/navigation';
	import Icon from '$lib/components/Icon.svelte';
	import { inAppPanel } from '$lib/in-app-panel.svelte';

	const href = $derived(inAppPanel.href);
	const open = $derived(href != null && href !== '');
	const mode = $derived(inAppPanel.mode);
	const gen = $derived(inAppPanel.generation);
	const resizing = $derived(inAppPanel.resizing);
	const widthPx = $derived(inAppPanel.widthPx);
	const embedSrc = $derived.by(() => {
		void gen;
		return inAppPanel.embedSrc();
	});
	const fullHref = $derived(inAppPanel.fullHref());
	const label = $derived(href ?? '');

	let dragStartX = 0;
	let dragStartW = 0;

	function close() {
		inAppPanel.close();
	}

	function openFull() {
		const next = fullHref;
		inAppPanel.close();
		if (next) void goto(next);
	}

	function onKey(e: KeyboardEvent) {
		if (!open) return;
		if (e.key === 'Escape') {
			e.preventDefault();
			close();
		}
	}

	function onResizePointerDown(e: PointerEvent) {
		if (mode !== 'split') return;
		e.preventDefault();
		e.stopPropagation();
		dragStartX = e.clientX;
		dragStartW = inAppPanel.widthPx;
		inAppPanel.resizing = true;
		const target = e.currentTarget as HTMLElement;
		target.setPointerCapture(e.pointerId);
		document.documentElement.classList.add('shell-resizing');
	}

	function onResizePointerMove(e: PointerEvent) {
		if (!inAppPanel.resizing) return;
		// Panel is fixed on the physical left — drag right widens
		const next = dragStartW + (e.clientX - dragStartX);
		inAppPanel.setWidth(next, { persist: false });
	}

	function endResize(e: PointerEvent) {
		if (!inAppPanel.resizing) return;
		inAppPanel.resizing = false;
		document.documentElement.classList.remove('shell-resizing');
		inAppPanel.setWidth(inAppPanel.widthPx, { persist: true });
		try {
			(e.currentTarget as HTMLElement).releasePointerCapture(e.pointerId);
		} catch {
			/* ignore */
		}
	}

	function onResizeKey(e: KeyboardEvent) {
		if (mode !== 'split') return;
		const step = e.shiftKey ? 40 : 12;
		if (e.key === 'ArrowLeft') {
			e.preventDefault();
			inAppPanel.setWidth(widthPx - step);
		} else if (e.key === 'ArrowRight') {
			e.preventDefault();
			inAppPanel.setWidth(widthPx + step);
		} else if (e.key === 'Home') {
			e.preventDefault();
			inAppPanel.setWidth(280);
		} else if (e.key === 'End') {
			e.preventDefault();
			inAppPanel.setWidth(900);
		}
	}

	$effect(() => {
		if (!open || typeof window === 'undefined') return;
		const onResize = () => inAppPanel.syncMode();
		window.addEventListener('resize', onResize);
		return () => window.removeEventListener('resize', onResize);
	});

	$effect(() => {
		if (!open || mode !== 'drawer' || typeof document === 'undefined') return;
		const prev = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		return () => {
			document.body.style.overflow = prev;
		};
	});
</script>

<svelte:window onkeydown={onKey} />

{#if open && embedSrc}
	{#if mode === 'drawer'}
		<button type="button" class="iap-scrim" aria-label="بستن پیش‌نمایش" onclick={close}></button>
	{/if}

	<aside
		class="iap"
		class:iap--split={mode === 'split'}
		class:iap--drawer={mode === 'drawer'}
		class:iap--resizing={resizing}
		aria-label="پیش‌نمایش صفحه"
	>
		{#if mode === 'split'}
			<button
				type="button"
				class="iap__resize"
				aria-label="تغییر عرض پیش‌نمایش"
				onpointerdown={onResizePointerDown}
				onpointermove={onResizePointerMove}
				onpointerup={endResize}
				onpointercancel={endResize}
				onkeydown={onResizeKey}
				ondblclick={() => inAppPanel.setWidth(Math.min(window.innerWidth * 0.5, 36 * 16))}
			></button>
		{/if}
		<header class="iap__bar">
			<span class="iap__path" dir="ltr" title={label}>{label}</span>
			<div class="iap__actions">
				<button type="button" class="iap__btn iap__btn--primary" onclick={openFull}>
					باز کردن صفحه
					<Icon name="arrow-up-right" size={14} />
				</button>
				<button type="button" class="iap__btn" onclick={close} aria-label="بستن">
					<Icon name="x" size={16} />
					<span class="iap__btn-label">بستن</span>
				</button>
			</div>
		</header>
		{#key `${gen}:${embedSrc}`}
			<iframe class="iap__frame" title="پیش‌نمایش" src={embedSrc}></iframe>
		{/key}
	</aside>
{/if}
