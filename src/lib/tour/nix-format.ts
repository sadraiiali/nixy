/**
 * Lightweight Nix formatter for the tour Monaco editor.
 * Reindents from braces/brackets/parens and lightly normalizes spaces
 * around `=` / binary ops — strings & comments are left intact.
 */

export type FormatNixOptions = {
	indentSize?: number;
	insertFinalNewline?: boolean;
};

type Seg =
	| { kind: 'code'; text: string }
	| { kind: 'keep'; text: string }; // string / comment — do not re-space

/** Split source into code vs string/comment segments (single-line aware). */
function segmentLine(line: string): Seg[] {
	const segs: Seg[] = [];
	let i = 0;
	let buf = '';
	const flushCode = () => {
		if (buf) {
			segs.push({ kind: 'code', text: buf });
			buf = '';
		}
	};
	const flushKeep = (t: string) => {
		if (t) segs.push({ kind: 'keep', text: t });
	};

	while (i < line.length) {
		const ch = line[i]!;
		const next = line[i + 1] ?? '';

		// line comment
		if (ch === '#') {
			flushCode();
			flushKeep(line.slice(i));
			break;
		}
		// block comment (may not close on this line)
		if (ch === '/' && next === '*') {
			flushCode();
			let j = i + 2;
			let body = '/*';
			while (j < line.length) {
				if (line[j] === '*' && line[j + 1] === '/') {
					body += '*/';
					j += 2;
					break;
				}
				body += line[j]!;
				j++;
			}
			flushKeep(body);
			i = j;
			continue;
		}
		// indented string ''
		if (ch === "'" && next === "'") {
			flushCode();
			let j = i + 2;
			let body = "''";
			let interp = 0;
			while (j < line.length) {
				if (interp === 0 && line[j] === "'" && line[j + 1] === "'") {
					body += "''";
					j += 2;
					break;
				}
				if (interp === 0 && line[j] === '$' && line[j + 1] === '{') {
					body += '${';
					j += 2;
					interp = 1;
					continue;
				}
				if (interp > 0) {
					if (line[j] === '{') interp++;
					else if (line[j] === '}') interp--;
					body += line[j]!;
					j++;
					continue;
				}
				body += line[j]!;
				j++;
			}
			flushKeep(body);
			i = j;
			continue;
		}
		// " string
		if (ch === '"') {
			flushCode();
			let j = i + 1;
			let body = '"';
			while (j < line.length) {
				const c = line[j]!;
				body += c;
				if (c === '\\' && line[j + 1]) {
					body += line[j + 1]!;
					j += 2;
					continue;
				}
				if (c === '"') {
					j++;
					break;
				}
				j++;
			}
			flushKeep(body);
			i = j;
			continue;
		}

		buf += ch;
		i++;
	}
	flushCode();
	return segs;
}

/** Light spacing normalize on pure code (no strings/comments). */
function normalizeCodeSpacing(code: string): string {
	let s = code;
	// collapse runs of spaces/tabs
	s = s.replace(/[ \t]+/g, ' ');
	// spaces around == != <= >= && || -> ++ // (attr merge) first
	s = s.replace(/[ \t]*(==|!=|<=|>=|&&|\|\||->|\+\+|\/\/)[ \t]*/g, ' $1 ');
	// spaces around single = (assignment), not part of == != etc.
	s = s.replace(/([^\s=!<>])[ \t]*=[ \t]*(?!=)/g, '$1 = ');
	// spaces around single + * when binary
	s = s.replace(/([^\s(=[,:+\-*\/])[ \t]*\+[ \t]*(?!=)/g, '$1 + ');
	s = s.replace(/([^\s(=[,:\-+*\/])[ \t]*\*[ \t]*/g, '$1 * ');
	s = s.replace(/[ \t]+/g, ' ');
	// no space before , ; )
	s = s.replace(/[ \t]+([,;)])/g, '$1');
	// space after , ;
	s = s.replace(/([,;])(?!\s|$)/g, '$1 ');
	// space after keywords when glued to next token
	s = s.replace(
		/\b(let|in|rec|with|if|then|else|assert|inherit|or)\b(?=[^\s])/g,
		'$1 '
	);
	// space before { after word: rec{ → rec {
	s = s.replace(/([a-zA-Z0-9_')\]])\{/g, '$1 {');
	s = s.replace(/[ \t]{2,}/g, ' ');
	// keep edge spaces (needed when segment is between strings: `= ` + `"x"`)
	return s;
}

function needsJoinSpace(left: string, right: string): boolean {
	if (!left || !right) return false;
	if (/\s$/.test(left) || /^\s/.test(right)) return false;
	// `= "…"` / `+ "…"` / `"…" +`
	if (/[=+\-*<>]$/.test(left) && /^["']/.test(right)) return true;
	if (/["']$/.test(left) && /^[=+\-*<>]/.test(right)) return true;
	// word + string or string + word
	if (/[a-zA-Z0-9_]$/.test(left) && /^["']/.test(right)) return true;
	if (/["']$/.test(left) && /^[a-zA-Z0-9_]/.test(right)) return true;
	// code then comment
	if (/[^\s]$/.test(left) && right.startsWith('#')) return true;
	if (/[^\s]$/.test(left) && right.startsWith('/*')) return true;
	return false;
}

function processLineContent(line: string): string {
	const segs = segmentLine(line.trim());
	if (!segs.length) return '';
	let result = '';
	for (const seg of segs) {
		const piece = seg.kind === 'code' ? normalizeCodeSpacing(seg.text) : seg.text;
		if (!piece) continue;
		if (needsJoinSpace(result, piece)) result += ' ';
		result += piece;
	}
	return result.replace(/[ \t]{2,}/g, ' ').trim();
}

/** Net brace delta for a full line (strings/comments ignored). */
function lineDelta(line: string): { open: number; close: number; leadingClose: number } {
	let open = 0;
	let close = 0;
	let leadingClose = 0;
	let seenCode = false;

	const segs = segmentLine(line.trim());
	for (const seg of segs) {
		if (seg.kind === 'keep') {
			seenCode = true;
			continue;
		}
		for (const ch of seg.text) {
			if (ch === '{' || ch === '[' || ch === '(') {
				open++;
				seenCode = true;
			} else if (ch === '}' || ch === ']' || ch === ')') {
				if (!seenCode && open === 0) leadingClose++;
				close++;
				seenCode = true;
			} else if (!/\s/.test(ch)) {
				seenCode = true;
			}
		}
	}
	return { open, close, leadingClose };
}

/**
 * Format Nix source for the tour editor.
 */
export function formatNix(source: string, opts: FormatNixOptions = {}): string {
	const indentSize = opts.indentSize ?? 2;
	const insertFinalNewline = opts.insertFinalNewline !== false;

	const raw = source.replace(/\r\n?/g, '\n');
	if (!raw.trim()) {
		return insertFinalNewline ? '\n' : '';
	}

	const lines = raw.split('\n');
	let depth = 0;
	/** Extra indent after `let` until matching `in` at same level */
	let letDepth = 0;
	const out: string[] = [];

	for (const rawLine of lines) {
		if (!rawLine.trim()) {
			// collapse: only keep single blank (handled later)
			out.push('');
			continue;
		}

		const content = processLineContent(rawLine);
		const { open, close, leadingClose } = lineDelta(content);

		// `in` that closes a let: dedent letDepth first
		const isIn =
			/^in\b/.test(content) &&
			!content.startsWith('inherit') &&
			letDepth > 0;

		let lineDepth = depth - leadingClose;
		if (isIn) {
			letDepth = Math.max(0, letDepth - 1);
			lineDepth = Math.min(lineDepth, depth - leadingClose);
			// align `in` with its `let`
		} else if (letDepth > 0 && leadingClose === 0) {
			// body of let
			lineDepth = depth + letDepth;
		}

		lineDepth = Math.max(0, lineDepth);
		out.push(' '.repeat(lineDepth * indentSize) + content);

		// update depths after the line
		depth = Math.max(0, depth + open - close);

		if (/^let\b/.test(content)) {
			letDepth++;
		}
		// `in` already decremented letDepth above
	}

	// collapse 3+ blank lines → 1 blank
	let text = out.join('\n').replace(/\n{3,}/g, '\n\n');
	text = text.replace(/[ \t]+$/gm, '');
	text = text.replace(/^\n+/, '').replace(/\n+$/, '');
	if (insertFinalNewline) text += '\n';
	return text;
}
