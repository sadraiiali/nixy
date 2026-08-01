/**
 * Minimal Nix language support for Monaco (tokenizer + config + format).
 * Not a full grammar — enough for tour exercises.
 */
import type * as Monaco from 'monaco-editor';
import { formatNix } from './nix-format';

let registered = false;

export function registerNixLanguage(monaco: typeof Monaco) {
	if (registered) return;
	registered = true;

	monaco.languages.register({ id: 'nix' });

	monaco.languages.setLanguageConfiguration('nix', {
		comments: {
			lineComment: '#',
			blockComment: ['/*', '*/']
		},
		brackets: [
			['{', '}'],
			['[', ']'],
			['(', ')']
		],
		autoClosingPairs: [
			{ open: '{', close: '}' },
			{ open: '[', close: ']' },
			{ open: '(', close: ')' },
			{ open: '"', close: '"' },
			{ open: "''", close: "''" }
		],
		surroundingPairs: [
			{ open: '{', close: '}' },
			{ open: '[', close: ']' },
			{ open: '(', close: ')' },
			{ open: '"', close: '"' }
		],
		// Word-based selection / format range defaults
		wordPattern:
			/(-?\d*\.\d\w*)|([^\`\~\!\@\#\%\^\&\*\(\)\-\=\+\[\{\]\}\\\|\;\:\'\"\,\.\<\>\/\?\s]+)/g
	});

	// Required for editor.action.formatDocument (Ctrl+Shift+I / Shift+Alt+F)
	monaco.languages.registerDocumentFormattingEditProvider('nix', {
		provideDocumentFormattingEdits(model) {
			const text = model.getValue();
			const tabSize = model.getOptions().tabSize || 2;
			const formatted = formatNix(text, { indentSize: tabSize });
			if (formatted === text) return [];
			return [
				{
					range: model.getFullModelRange(),
					text: formatted
				}
			];
		}
	});

	monaco.languages.registerDocumentRangeFormattingEditProvider('nix', {
		provideDocumentRangeFormattingEdits(model, range) {
			const text = model.getValueInRange(range);
			const tabSize = model.getOptions().tabSize || 2;
			const formatted = formatNix(text, {
				indentSize: tabSize,
				// Partial range: don't force final newline mid-file
				insertFinalNewline: false
			});
			if (formatted === text) return [];
			return [{ range, text: formatted }];
		}
	});

	monaco.languages.setMonarchTokensProvider('nix', {
		defaultToken: '',
		tokenPostfix: '.nix',

		keywords: [
			'assert',
			'else',
			'if',
			'in',
			'inherit',
			'let',
			'or',
			'rec',
			'then',
			'with'
		],

		builtins: [
			'abort',
			'baseNameOf',
			'dirOf',
			'fetchTarball',
			'import',
			'isNull',
			'map',
			'removeAttrs',
			'throw',
			'toString'
		],

		operators: [
			'=',
			'==',
			'!=',
			'<',
			'<=',
			'>',
			'>=',
			'&&',
			'||',
			'->',
			'//',
			'++',
			'+',
			'-',
			'*',
			'/',
			'!',
			'?',
			'@',
			':'
		],

		symbols: /[=><!~?:&|+\-*/^%]+/,

		escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,

		tokenizer: {
			root: [
				[/#.*$/, 'comment'],
				[/\/\*/, 'comment', '@comment'],
				[/''/, 'string', '@indentedString'],
				[/"/, 'string', '@string'],
				[/\b\d+(\.\d+)?\b/, 'number'],
				[
					/[a-zA-Z_][\w'-]*/,
					{
						cases: {
							'@keywords': 'keyword',
							'@builtins': 'predefined',
							'@default': 'identifier'
						}
					}
				],
				[/[{}()\[\]]/, '@brackets'],
				[/@symbols/, { cases: { '@operators': 'operator', '@default': '' } }],
				[/[;,.]/, 'delimiter'],
				[/\s+/, 'white']
			],

			comment: [
				[/[^/*]+/, 'comment'],
				[/\*\//, 'comment', '@pop'],
				[/[/*]/, 'comment']
			],

			string: [
				[/[^\\"]+/, 'string'],
				[/@escapes/, 'string.escape'],
				[/\\./, 'string.escape.invalid'],
				[/"/, 'string', '@pop']
			],

			indentedString: [
				[/[^'$]+/, 'string'],
				[/\$\{/, { token: 'delimiter.bracket', next: '@interpolation' }],
				[/''\$/, 'string.escape'],
				[/'''/, 'string.escape'],
				[/''/, 'string', '@pop'],
				[/./, 'string']
			],

			interpolation: [
				[/\}/, { token: 'delimiter.bracket', next: '@pop' }],
				{ include: 'root' }
			]
		}
	});
}
