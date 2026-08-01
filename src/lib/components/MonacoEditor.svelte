<script lang="ts">
	import { browser } from '$app/environment';
	import type * as Monaco from 'monaco-editor';
	import { ensureMonacoEnv } from '$lib/tour/monaco-env';
	import { registerNixLanguage } from '$lib/tour/nix-monaco-lang';

	interface Props {
		value?: string;
		language?: string;
		readonly?: boolean;
		disabled?: boolean;
		class?: string;
		/** Called when the user edits the document */
		onChange?: (value: string) => void;
		/** Ctrl/Cmd+Enter or Shift+Enter from the editor */
		onRun?: () => void;
	}

	let {
		value = '',
		language = 'nix',
		readonly = false,
		disabled = false,
		class: className = '',
		onChange,
		onRun
	}: Props = $props();

	let host: HTMLDivElement | undefined = $state();
	/** Bumps when the editor instance is ready so sync effects re-run */
	let readyTick = $state(0);

	let editor: Monaco.editor.IStandaloneCodeEditor | null = null;
	let monacoApi: typeof Monaco | null = null;
	let applyingExternal = false;
	let resizeObs: ResizeObserver | null = null;

	// Always-current props for async mount / keybindings (avoid stale closures)
	const propsRef: {
		value: string;
		language: string;
		readonly: boolean;
		disabled: boolean;
		onChange?: (value: string) => void;
		onRun?: () => void;
	} = {
		value: '',
		language: 'nix',
		readonly: false,
		disabled: false
	};
	$effect.pre(() => {
		propsRef.value = value;
		propsRef.language = language;
		propsRef.readonly = readonly;
		propsRef.disabled = disabled;
		propsRef.onChange = onChange;
		propsRef.onRun = onRun;
	});

	async function mountEditor(el: HTMLDivElement) {
		await ensureMonacoEnv();
		const monaco = await import('monaco-editor');
		monacoApi = monaco;
		registerNixLanguage(monaco);

		monaco.editor.defineTheme('ton-dark', {
			base: 'vs-dark',
			inherit: true,
			rules: [
				{ token: 'comment.nix', foreground: '64748b', fontStyle: 'italic' },
				{ token: 'keyword.nix', foreground: '93c5fd' },
				{ token: 'predefined.nix', foreground: 'c4b5fd' },
				{ token: 'string.nix', foreground: '86efac' },
				{ token: 'number.nix', foreground: 'fcd34d' },
				{ token: 'operator.nix', foreground: '94a3b8' },
				{ token: 'identifier.nix', foreground: 'e2e8f0' }
			],
			colors: {
				'editor.background': '#0f1419',
				'editor.foreground': '#e2e8f0',
				'editorLineNumber.foreground': '#475569',
				'editorLineNumber.activeForeground': '#94a3b8',
				'editor.selectionBackground': '#1e3a5f',
				'editor.lineHighlightBackground': '#151b23',
				'editorCursor.foreground': '#93c5fd',
				'editorWidget.background': '#151b23',
				'editorWidget.border': '#243044',
				'scrollbarSlider.background': '#33415588',
				'scrollbarSlider.hoverBackground': '#475569aa'
			}
		});

		const ed = monaco.editor.create(el, {
			value: propsRef.value,
			language: propsRef.language,
			readOnly: propsRef.readonly || propsRef.disabled,
			theme: 'ton-dark',
			automaticLayout: false,
			minimap: { enabled: false },
			fontSize: 13.5,
			lineHeight: 20,
			fontFamily: "ui-monospace, 'SF Mono', Menlo, Consolas, monospace",
			tabSize: 2,
			insertSpaces: true,
			scrollBeyondLastLine: false,
			wordWrap: 'on',
			wrappingIndent: 'same',
			renderLineHighlight: 'line',
			lineNumbers: 'on',
			glyphMargin: false,
			folding: true,
			padding: { top: 10, bottom: 10 },
			scrollbar: {
				verticalScrollbarSize: 8,
				horizontalScrollbarSize: 8,
				useShadows: false
			},
			overviewRulerLanes: 0,
			hideCursorInOverviewRuler: true,
			overviewRulerBorder: false,
			contextmenu: true,
			quickSuggestions: false,
			suggestOnTriggerCharacters: false,
			wordBasedSuggestions: 'off',
			parameterHints: { enabled: false },
			links: false,
			fixedOverflowWidgets: true
		});

		ed.onDidChangeModelContent(() => {
			if (applyingExternal) return;
			propsRef.onChange?.(ed.getValue());
		});

		const run = () => {
			propsRef.onRun?.();
		};
		// Ctrl+Enter (Windows/Linux), Cmd+Enter (macOS), Shift+Enter
		ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, run);
		ed.addCommand(monaco.KeyMod.Shift | monaco.KeyCode.Enter, run);

		const formatDoc = () => {
			if (propsRef.readonly || propsRef.disabled) return;
			void ed.getAction('editor.action.formatDocument')?.run();
		};
		// Format document (needs DocumentFormattingEditProvider — see nix-monaco-lang.ts)
		// Ctrl/Cmd+Shift+I · Shift+Alt+F · Ctrl/Cmd+Alt+I
		// Note: in Chrome/Firefox, Ctrl+Shift+I is DevTools and often cannot be captured.
		const formatKey =
			monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyI;
		ed.addCommand(formatKey, formatDoc);
		ed.addCommand(monaco.KeyMod.Shift | monaco.KeyMod.Alt | monaco.KeyCode.KeyF, formatDoc);
		ed.addCommand(
			monaco.KeyMod.CtrlCmd | monaco.KeyMod.Alt | monaco.KeyCode.KeyI,
			formatDoc
		);
		// Also re-bind via keybinding service so it wins over default when possible
		ed.addAction({
			id: 'ton.formatNix',
			label: 'Format Nix Document',
			keybindings: [
				formatKey,
				monaco.KeyMod.Shift | monaco.KeyMod.Alt | monaco.KeyCode.KeyF,
				monaco.KeyMod.CtrlCmd | monaco.KeyMod.Alt | monaco.KeyCode.KeyI
			],
			run: () => formatDoc()
		});

		resizeObs = new ResizeObserver(() => {
			ed.layout();
		});
		resizeObs.observe(el);
		requestAnimationFrame(() => ed.layout());

		return ed;
	}

	$effect(() => {
		if (!browser || !host) return;
		const el = host;
		let cancelled = false;

		void mountEditor(el).then((ed) => {
			if (cancelled) {
				ed.dispose();
				return;
			}
			editor = ed;
			readyTick++;
		});

		return () => {
			cancelled = true;
			resizeObs?.disconnect();
			resizeObs = null;
			editor?.dispose();
			editor = null;
		};
	});

	// External value updates (lesson change / reset)
	$effect(() => {
		const next = value;
		void readyTick;
		if (!editor) return;
		const cur = editor.getValue();
		if (cur === next) return;
		applyingExternal = true;
		editor.setValue(next);
		applyingExternal = false;
	});

	// language / readonly
	$effect(() => {
		void readyTick;
		const lang = language;
		const ro = readonly || disabled;
		if (!editor || !monacoApi) return;
		const model = editor.getModel();
		if (model && lang) {
			monacoApi.editor.setModelLanguage(model, lang);
		}
		editor.updateOptions({ readOnly: ro });
	});
</script>

<!-- Monaco owns focus inside; host is only a layout shell -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
	class="monaco-host {className}"
	bind:this={host}
	aria-label="Nix code editor"
	onkeydown={(e) => {
		// Capture format chords (Chrome may still steal Ctrl+Shift+I for DevTools)
		const isI = e.key === 'i' || e.key === 'I';
		const isF = e.key === 'f' || e.key === 'F';
		const mod = e.ctrlKey || e.metaKey;
		const format =
			(mod && e.shiftKey && isI && !e.altKey) ||
			(e.shiftKey && e.altKey && isF && !mod) ||
			(mod && e.altKey && isI && !e.shiftKey);
		if (!format || readonly || disabled) return;
		if (!editor) return;
		e.preventDefault();
		e.stopPropagation();
		void editor.getAction('editor.action.formatDocument')?.run();
	}}
></div>

<style>
	.monaco-host {
		flex: 1 1 auto;
		min-height: 0;
		width: 100%;
		position: relative;
		overflow: hidden;
		background: var(--ide-bg, #0f1419);
	}

	.monaco-host :global(.monaco-editor),
	.monaco-host :global(.overflow-guard) {
		border-radius: 0;
	}
</style>
