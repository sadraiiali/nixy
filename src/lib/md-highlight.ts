/**
 * Prism-based highlighter for mdsvex (Nix + Bash/shell + diff).
 */
import Prism from 'prismjs';
import 'prismjs/components/prism-bash.js';
import 'prismjs/components/prism-shell-session.js';
import 'prismjs/components/prism-nix.js';
import 'prismjs/components/prism-diff.js';

/** Richer Nix tokens: paths, attrs, more builtins (on top of Prism's grammar). */
if (Prism.languages.nix) {
	Prism.languages.insertBefore('nix', 'keyword', {
		// <nixpkgs>, <nixos-config>, …
		path: {
			pattern: /<(?:[A-Za-z0-9._+-]+\/)*[A-Za-z0-9._+-]+>/,
			alias: 'string'
		},
		// attr = …  (simple left-hand names)
		'attr-name': {
			pattern: /\b[a-zA-Z_][\w'-]*(?=\s*=)/,
			alias: 'property'
		}
	});

	// Extra common Nixpkgs helpers Prism's stock list misses
	const extraFns =
		/\b(?:mkDerivation|mkShell|mkShellNoCC|mkOption|mkEnableOption|mkIf|mkMerge|mkDefault|mkForce|mkOverride|mkPackageOption|callPackage|callPackages|overrideAttrs|overrideDerivation|optionalString|optionals|optional|concatStringsSep|concatMapStrings|writeText|writeScript|writeScriptBin|writeShellScript|writeShellScriptBin|writeShellApplication|runCommand|runCommandCC|stdenv|lib|pkgs|config|modulesPath|fetchFromGitHub|fetchFromGitLab|fetchzip|fetchgit|fetchpatch|symlinkJoin|buildEnv)\b/;
	const prev = Prism.languages.nix.function;
	Prism.languages.nix.function = [
		extraFns,
		...(Array.isArray(prev) ? prev : prev ? [prev] : [])
	];
}

function escapeHtml(s: string): string {
	return s
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;');
}

const LANG_MAP: Record<string, string> = {
	nix: 'nix',
	nixos: 'nix',
	nixpkgs: 'nix',
	bash: 'bash',
	sh: 'bash',
	shell: 'bash',
	zsh: 'bash',
	fish: 'bash',
	console: 'bash',
	terminal: 'bash',
	'shell-session': 'shell-session',
	session: 'shell-session',
	diff: 'diff',
	patch: 'diff',
	udiff: 'diff',
	json: 'json',
	javascript: 'javascript',
	js: 'javascript',
	ts: 'typescript',
	typescript: 'typescript',
	python: 'python',
	py: 'python',
	toml: 'toml',
	yaml: 'yaml',
	yml: 'yaml',
	text: 'text',
	plain: 'text',
	undefined: 'text',
	'': 'text'
};

/** Map fence labels + heuristics → Prism language id */
export function normalizeLang(lang: string, code = ''): string {
	const raw = (lang || '').trim().toLowerCase();

	if (raw && LANG_MAP[raw]) return LANG_MAP[raw]!;
	if (raw && Prism.languages[raw]) return raw;

	const sample = (code || '').trim();
	if (!sample) return 'text';

	// Unified diffs
	if (/^[+-]{3}\s/m.test(sample) || /^@@ /m.test(sample) || /^[+-].*\n[+-]/m.test(sample)) {
		return 'diff';
	}

	if (
		/^\$\s/m.test(sample) ||
		/^#\s?(!|nix|\[)/m.test(sample) ||
		/^nix-env\b/m.test(sample) ||
		/^nixos-rebuild\b/m.test(sample) ||
		/^nix-shell\b/m.test(sample) ||
		/^nix\s+(build|run|develop|flake)\b/m.test(sample)
	) {
		return sample.includes('[nix-shell') || /^\$\s/m.test(sample)
			? 'shell-session'
			: 'bash';
	}

	if (
		/\b(pkgs\.|mkShell|fetchTarball|stdenv|callPackage|overrideAttrs)\b/.test(sample) ||
		/^\s*\{\s*$/m.test(sample) ||
		/\blet\b[\s\S]*\bin\b/.test(sample) ||
		/\bimport\s*</.test(sample)
	) {
		return 'nix';
	}

	if (/^\/nix\/store\//.test(sample) && !sample.includes('\n')) {
		return 'text';
	}

	return raw || 'text';
}

/** Prism-highlight a fence → inner HTML (escaped when no grammar). */
export function highlightInner(code: string, lang: string): { id: string; html: string } {
	const id = normalizeLang(lang, code);
	const grammar = Prism.languages[id];
	const html =
		grammar != null ? Prism.highlight(code, grammar, id) : escapeHtml(code);
	return { id, html };
}

/**
 * Plain HTML fenced block for runtime markdown (e.g. marked in Tour of Nix).
 * Same Prism tokens / CSS classes as mdsvex (`.prose .language-nix …`).
 */
export function highlightCodeHtml(code: string, lang: string): string {
	const { id, html } = highlightInner(code, lang);
	return `<pre class="language-${id}" data-lang="${id}" dir="ltr"><code class="language-${id}">${html}</code></pre>\n`;
}

/**
 * Highlight fenced code for mdsvex → Svelte.
 * Uses JSON.stringify so `{`, `}`, `` ` ``, and `${` never break Svelte parsing
 * (template-literal embedding was fragile for Nix interpolations).
 */
export function highlightCode(code: string, lang: string): string {
	const { id, html } = highlightInner(code, lang);

	// {@html "…"} — JSON string is a valid Svelte expression
	const payload = JSON.stringify(html);
	return `<pre class="language-${id}" data-lang="${id}" dir="ltr"><code class="language-${id}">{@html ${payload}}</code></pre>`;
}
