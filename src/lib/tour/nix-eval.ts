/**
 * Browser wrapper around the emscripten-built nix-instantiate from
 * https://github.com/nixcloud/tour_of_nix
 */

export type NixRunResult = {
	ok: boolean;
	output: string;
	expected?: string;
	match?: boolean;
	error?: string;
};

type EmscriptenModule = {
	arguments: string[];
	print: (text: string) => void;
	printErr: (text: string) => void;
	callMain: (args: string[]) => void;
	locateFile?: (path: string) => string;
	setStatus?: (s: string) => void;
	onRuntimeInitialized?: () => void;
	/** When false, emscripten does not auto-run main on load. */
	noInitialRun?: boolean;
	FS?: {
		writeFile: (path: string, data: string, opts?: { encoding: string }) => void;
	};
	[key: string]: unknown;
};

declare global {
	interface Window {
		Module?: EmscriptenModule;
		FS?: EmscriptenModule['FS'];
	}
}

const ASSET_BASE = '/tour-of-nix';
const EVAL_ARGS = ['-I', 'nixpkgs=nixpkgs', '--eval', '--strict', '--show-trace', '/test.nix'];

let loadPromise: Promise<void> | null = null;
let ready = false;

function getModule(): EmscriptenModule {
	if (typeof window === 'undefined') {
		throw new Error('nix-eval only runs in the browser');
	}
	if (!window.Module) {
		// Must exist before the script tag runs
		window.Module = {
			arguments: EVAL_ARGS,
			print: () => {},
			printErr: () => {},
			callMain: () => {},
			locateFile: (path: string) => `${ASSET_BASE}/${path}`,
			noInitialRun: true
		} as unknown as EmscriptenModule;
	}
	return window.Module;
}

export function isNixReady() {
	return ready;
}

/**
 * Emscripten's shell assigns Module.setStatus to a default that does
 * document.getElementById("progress").value = ... without null checks.
 * Our page has no #status / #progress / #spinner, so that crashes during
 * data download. Pin our handler so the shell cannot overwrite it.
 */
function pinSetStatus(Module: EmscriptenModule, onStatus?: (msg: string) => void) {
	const impl = (s: string) => {
		onStatus?.(s || '');
	};
	Object.defineProperty(Module, 'setStatus', {
		configurable: true,
		enumerable: true,
		get: () => impl,
		set: () => {
			/* ignore emscripten shell overwrite */
		}
	});
}

/** Optional stubs if something still reaches the stock setStatus. */
function ensureEmscriptenStatusDom() {
	if (typeof document === 'undefined') return;
	const ensure = (id: string, tag: string) => {
		if (document.getElementById(id)) return;
		const el = document.createElement(tag);
		el.id = id;
		el.hidden = true;
		el.setAttribute('aria-hidden', 'true');
		el.style.cssText = 'display:none!important';
		document.body.appendChild(el);
	};
	ensure('status', 'div');
	ensure('progress', 'progress');
	ensure('spinner', 'div');
}

export function loadNixRuntime(onStatus?: (msg: string) => void): Promise<void> {
	if (ready) return Promise.resolve();
	if (loadPromise) return loadPromise;

	loadPromise = new Promise<void>((resolve, reject) => {
		// Emscripten reads global `Module` at script start — must set first.
		const Module = getModule();
		Module.locateFile = (path: string) => `${ASSET_BASE}/${path}`;
		ensureEmscriptenStatusDom();
		pinSetStatus(Module, onStatus);
		Module.noInitialRun = false;

		let settled = false;
		const done = () => {
			if (settled) return;
			settled = true;
			ready = true;
			onStatus?.('');
			// expose FS from Module if not global
			const M = window.Module as EmscriptenModule & { FS?: typeof window.FS };
			if (M?.FS && !window.FS) window.FS = M.FS;
			resolve();
		};

		const prevInit = Module.onRuntimeInitialized;
		Module.onRuntimeInitialized = () => {
			prevInit?.();
			done();
		};

		const existing = document.querySelector<HTMLScriptElement>(
			'script[data-nix-instantiate]'
		);
		if (!existing) {
			const script = document.createElement('script');
			script.src = `${ASSET_BASE}/nix-instantiate.js`;
			script.async = true;
			script.dataset.nixInstantiate = '1';
			script.onerror = () => {
				if (!settled) {
					settled = true;
					reject(new Error('بارگذاری nix-instantiate.js ناموفق بود'));
				}
			};
			// Re-pin after the shell runs (it assigns Module.setStatus = …).
			script.onload = () => {
				pinSetStatus(Module, onStatus);
			};
			document.body.appendChild(script);
		} else {
			pinSetStatus(Module, onStatus);
		}

		const t0 = Date.now();
		const poll = () => {
			if (settled) return;
			const M = window.Module as EmscriptenModule & {
				FS?: typeof window.FS;
				calledRun?: boolean;
			};
			const fs = window.FS || M?.FS;
			if (fs && typeof M?.callMain === 'function' && M.calledRun) {
				done();
				return;
			}
			if (Date.now() - t0 > 180_000) {
				settled = true;
				reject(new Error('زمان بارگذاری nix-instantiate به پایان رسید'));
				return;
			}
			setTimeout(poll, 150);
		};
		setTimeout(poll, 300);
	});

	return loadPromise;
}

/**
 * nix-instantiate (emscripten) prints CSI color codes like ESC[31;1m …
 * A partial strip left the ESC (U+001B) which browsers show as ␛.
 */
function stripAnsi(text: string): string {
	return (
		String(text)
			// CSI sequences: ESC [ … letter  (colors, bold, etc.)
			.replace(/\u001b\[[\d;?]*[ -/]*[@-~]/g, '')
			// OSC: ESC ] … BEL or ST
			.replace(/\u001b\][^\u0007\u001b]*(?:\u0007|\u001b\\)?/g, '')
			// remaining ESC + one byte
			.replace(/\u001b./g, '')
			// stray CSI without ESC (defensive)
			.replace(/\[[\d;]*m/g, '')
			// control chars except \n \t
			.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '')
			// unicode “symbol for escape” if already converted
			.replace(/\u241b/g, '')
			.replaceAll('/test.nix', 'line')
			.replace(/\r\n/g, '\n')
			.replace(/\r/g, '\n')
	);
}

function cleanOutput(text: string): string {
	return stripAnsi(text).trim();
}

function runOnce(source: string): Promise<{ stdout: string; stderr: string }> {
	const Module = getModule() as EmscriptenModule & { FS?: typeof window.FS };
	const FS = window.FS || Module.FS;
	if (!FS?.writeFile) return Promise.reject(new Error('FS not ready'));

	let stdout = '';
	let stderr = '';

	Module.print = (text: string) => {
		stdout += (stdout ? '\n' : '') + text;
	};
	Module.printErr = (text: string) => {
		stderr += (stderr ? '\n' : '') + String(text);
	};
	Module.arguments = EVAL_ARGS;

	FS.writeFile('/test.nix', source, { encoding: 'utf8' });
	try {
		Module.callMain(EVAL_ARGS);
	} catch {
		// ExitStatus is thrown by emscripten; often fine
	}

	return Promise.resolve({
		stdout: cleanOutput(stdout),
		stderr: cleanOutput(stderr)
	});
}

/** Evaluate user code and compare against expected solution output. */
export async function runNixExercise(
	userCode: string,
	solutionCode: string
): Promise<NixRunResult> {
	await loadNixRuntime();

	// Expected output from solution
	const expectedRun = await runOnce(solutionCode || userCode);
	if (expectedRun.stderr && !expectedRun.stdout) {
		// solution itself failed — still run user and show raw
		const userRun = await runOnce(userCode);
		if (userRun.stderr && !userRun.stdout) {
			return { ok: false, output: userRun.stderr, error: userRun.stderr };
		}
		return {
			ok: true,
			output: userRun.stdout,
			expected: expectedRun.stdout || undefined,
			match: false
		};
	}

	const expected = expectedRun.stdout;
	const userRun = await runOnce(userCode);

	if (userRun.stderr && !userRun.stdout) {
		return {
			ok: false,
			output: userRun.stderr,
			expected,
			error: userRun.stderr,
			match: false
		};
	}

	const match = userRun.stdout === expected;
	return {
		ok: true,
		output: match
			? userRun.stdout
			: `خروجی شما:\n${userRun.stdout}\n\nخروجی مورد انتظار:\n${expected}`,
		expected,
		match
	};
}
