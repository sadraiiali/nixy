<script lang="ts">
	/**
	 * Dev-only hotkeys for WYSIWYG inline edit (contenteditable on rendered page).
	 * Uses e.code so FA keyboard still works: KeyS / س, KeyE / ث
	 */
	import { browser, dev } from '$app/environment';
	import { page } from '$app/state';
	import {
		devMdCancel,
		devMdEdit,
		devMdOpen,
		devMdReset,
		devMdSave
	} from '$lib/dev-md-edit.svelte';

	const pathname = $derived((page.url.pathname.replace(/\/$/, '') || '/') as string);
	const canEdit = $derived(
		dev &&
			browser &&
			(pathname.startsWith('/pages/') || pathname.startsWith('/blog/'))
	);

	$effect(() => {
		const p = pathname;
		if (devMdEdit.open && devMdEdit.pathname && devMdEdit.pathname !== p) {
			devMdReset();
		}
	});

	/** Physical key or FA letter on that key (Persian layout). */
	function isSaveChord(e: KeyboardEvent): boolean {
		if (e.shiftKey || e.altKey) return false;
		if (!(e.ctrlKey || e.metaKey)) return false;
		// Physical S, or typed س (same key on FA), or Latin s
		return e.code === 'KeyS' || e.key === 'س' || e.key === 's' || e.key === 'S';
	}

	function isEditChord(e: KeyboardEvent): boolean {
		if (e.shiftKey || e.altKey) return false;
		if (!(e.ctrlKey || e.metaKey)) return false;
		// Physical E, or typed ث (same key on FA), or Latin e
		return e.code === 'KeyE' || e.key === 'ث' || e.key === 'e' || e.key === 'E';
	}

	function onKey(e: KeyboardEvent) {
		if (!canEdit) return;

		if (devMdEdit.open && e.key === 'Escape' && !e.ctrlKey && !e.metaKey) {
			// let link-edit dialog handle Esc first if focused elsewhere
			e.preventDefault();
			void devMdCancel();
			return;
		}

		if (isEditChord(e)) {
			e.preventDefault();
			if (devMdEdit.open) void devMdCancel();
			else
				void devMdOpen(pathname).catch((err) => {
					const msg = err instanceof Error ? err.message : 'خطا در باز کردن ویرایشگر';
					devMdEdit.errorMsg = msg;
					alert(msg);
				});
			return;
		}

		if (devMdEdit.open && isSaveChord(e)) {
			e.preventDefault();
			void devMdSave();
		}
	}
</script>

<svelte:window onkeydown={onKey} />
