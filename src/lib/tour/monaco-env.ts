/**
 * Monaco worker setup for Vite. Call once before creating any editor.
 *
 * monaco-editor@0.56 package exports map `./*` → `./esm/vs/*.js`, so
 * workers are imported as `monaco-editor/editor/editor.worker` (not the full
 * `monaco-editor/esm/vs/editor/...` path).
 *
 * Loaded dynamically so SSR never touches `?worker` imports.
 */

let configured = false;
let configuring: Promise<void> | null = null;

export async function ensureMonacoEnv(): Promise<void> {
	if (configured || typeof window === 'undefined') return;
	if (configuring) return configuring;

	configuring = (async () => {
		const { default: EditorWorker } = await import(
			'monaco-editor/editor/editor.worker?worker'
		);
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		(self as any).MonacoEnvironment = {
			getWorker() {
				return new EditorWorker();
			}
		};
		configured = true;
	})();

	return configuring;
}
