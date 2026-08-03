# Markdown syntax kitchen sink

Internal **test page** at `/test/syntax`. It collects Markdown (and a few HTML) forms this app actually renders via mdsvex, Prism, and site CSS. Use it to check layout, RTL, code LTR, callouts, and editor round-trips.

## Table of contents

- [Paragraphs and emphasis](#paragraphs)
- [Headings and anchors](#headings)
- [Links](#links)
- [Images](#images)
- [Lists](#lists)
- [Blockquotes](#blockquotes)
- [Admonitions / callouts](#admonitions)
- [Inline code and kbd](#inline-code)
- [Fenced code blocks](#fenced-code)
- [Tables](#tables)
- [Thematic breaks](#hr)
- [Highlight mark](#mark)
- [Hub cards](#hub-cards)
- [Mixed RTL sample](#mixed)

---

## Paragraphs and emphasis

<span id="paragraphs"></span>

A plain paragraph with **bold**, *italic*, ***bold italic***, and a bit of `inline code` mixed into the sentence so wrapping and isolation stay visible.

You can also use __underscore bold__ and _underscore italic_ if the parser accepts them.

Hard line break after two spaces:  
second line should sit under the first.

## Headings and anchors

<span id="headings"></span>

# Heading 1 (rare on body pages)

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

Heading with an explicit fragment target:

## <span id="named-heading"></span> Named heading

Link to that fragment: [jump to named heading](#named-heading).

## Links

<span id="links"></span>

- Internal path: [first steps](/pages/first-steps)
- Internal docs: [install Nix](/pages/nix-dev/install-nix)
- External HTTPS: [nixos.org](https://nixos.org/)
- External GitHub: [NixOS/nix](https://github.com/NixOS/nix)
- YouTube-style (icon via rehype): [example video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
- Autolink: <https://nix.dev/>
- Reference-style link: [Nix manual][nix-manual]
- Link with title attribute: [Nixpkgs](https://github.com/NixOS/nixpkgs "Nixpkgs repository")

[nix-manual]: /pages/nix-manual

Email-like (if allowed): <noreply@example.com>

## Images

<span id="images"></span>

Inline image with alt text (site icon):

![Nix snowflake](/icons/nix-snowflake.svg)

Linked image:

[![NixOS boot menu](https://nixos.org/images/screenshots/nixos-boot-menu.png)](https://nixos.org/images/screenshots/nixos-boot-menu.png)

## Lists

<span id="lists"></span>

Unordered:

- Alpha
- Bravo
  - Nested one
  - Nested two
- Charlie

Ordered:

1. First
2. Second
   1. Nested ordered
   2. Nested ordered again
3. Third

Tight list with inline code: `nix`, `nixos-rebuild`, `/nix/store`.

Loose list:

- Paragraph one in a list item.

  Second paragraph in the same item.

- Another item.

Task-style (GFM, if enabled):

- [x] Done item
- [ ] Open item

## Blockquotes

<span id="blockquotes"></span>

> A simple literary quote. Nested code like `hello` should stay LTR.
>
> Second paragraph in the same quote.

> Nested quotes:
>
> > Inner quote line.

## Admonitions / callouts

<span id="admonitions"></span>

Site publish converts MyST directives into blockquotes with
`<span class="admonition-kind" data-kind="…"></span>` plus a **title** line.

> <span class="admonition-kind" data-kind="note"></span>
>
> **Note**
>
> This is a note callout. Links work: [nix.dev](https://nix.dev/).

> <span class="admonition-kind" data-kind="tip"></span>
>
> **Tip**
>
> Prefer `nix shell` for ad-hoc tools.

> <span class="admonition-kind" data-kind="hint"></span>
>
> **Hint**
>
> Same family as tip in CSS.

> <span class="admonition-kind" data-kind="important"></span>
>
> **Important**
>
> Read this before upgrading.

> <span class="admonition-kind" data-kind="attention"></span>
>
> **Attention**
>
> Same family as important.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **Warning**
>
> Flakes may copy the whole tree into the store.

> <span class="admonition-kind" data-kind="caution"></span>
>
> **Caution**
>
> Check permissions first.

> <span class="admonition-kind" data-kind="danger"></span>
>
> **Danger**
>
> Destructive operation.

> <span class="admonition-kind" data-kind="error"></span>
>
> **Error**
>
> Build failed.

> <span class="admonition-kind" data-kind="seealso"></span>
>
> **See also**
>
> Related: [glossary](/glossary).

> <span class="admonition-kind" data-kind="example"></span>
>
> **Example**
>
> A short worked example.

> <span class="admonition-kind" data-kind="admonition"></span>
>
> **Notice**
>
> Generic admonition kind.

Callout with a fenced block inside:

> <span class="admonition-kind" data-kind="note"></span>
>
> **Note**
>
> Run:
>
> ```shell
> $ nix --version
> nix (Nix) 2.11.0
> ```

Callout with a list:

> <span class="admonition-kind" data-kind="tip"></span>
>
> **Tip**
>
> Checklist:
>
> - Install Nix
> - Open a **new** terminal
> - Run `nix --version`

Legacy strong-title callout (no `admonition-kind` span):

> **Note**
>
> Styled when the first child is a strong title.

## Inline code and kbd

<span id="inline-code"></span>

Paths and flags must read LTR inside RTL paragraphs: `/nix/store`, `~/.config/nix/nix.conf`, `--extra-experimental-features`, `pkgs.hello`.

Keyboard-ish chips often use backticks in this app (`Ctrl+E`, `Ctrl+K`); HTML kbd when present:

Press <kbd>Ctrl</kbd>+<kbd>E</kbd> in dev to edit.

Mixed punctuation: use `foo.bar` and `a/b/c` next to Persian or English words.

## Fenced code blocks

<span id="fenced-code"></span>

### Nix

```nix
{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  packages = [
    pkgs.hello
    pkgs.cowsay
  ];
}
```

### Shell / bash

```shell
$ curl -L https://nixos.org/nix/install | sh -s -- --daemon
$ nix --version
```

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "hello from bash"
```

### Shell session

```shell-session
$ nix-env -iA nixpkgs.hello
installing 'hello-2.12.1'
$ hello
Hello, world!
```

### Diff

```diff
--- a/flake.nix
+++ b/flake.nix
@@ -1,5 +1,6 @@
 {
   description = "demo";
+  # added line
 }
```

### JSON

```json
{
  "name": "example",
  "version": 1,
  "nested": { "ok": true }
}
```

### Text / plain

```text
/nix/store/b6gvzjyb2pg0…-firefox-33.1
```

### Unlabeled fence

```
plain fence without a language tag
line two
```

### Nested backticks in prose about fences

To write a fence in docs, open with three backticks and a language id such as `nix`.

## Tables

<span id="tables"></span>

| Flag | Meaning | Default |
| --- | --- | --- |
| `max-jobs` | Parallel derivations | `1` |
| `cores` | Cores per job | `0` (all) |
| `NIX_BUILD_CORES` | Env override | from `cores` |

Alignment demo:

| Left | Center | Right |
| :--- | :---: | ---: |
| a | b | c |
| longer cell | mid | 42 |

## Thematic breaks

<span id="hr"></span>

Above the rule.

---

Below the rule.

## Highlight mark

<span id="mark"></span>

Nix is a <mark>purely functional package manager</mark>. Highlights stay as HTML `<mark>` for mdsvex (Ctrl+H in the in-page editor).

## Hub cards

<span id="hub-cards"></span>

Site-specific HTML used on nix.dev hubs (preserved by the editor HTML→MD path):

<div class="nd-hub-cards" data-no-panel>
  <a class="nd-hub-card" href="/pages/nix-dev/tutorials" data-no-panel="1">
    <span class="nd-hub-card__title">Tutorials</span>
    <span class="nd-hub-card__desc">Lessons to get started</span>
  </a>
  <a class="nd-hub-card" href="/pages/nix-dev/guides" data-no-panel="1">
    <span class="nd-hub-card__title">Guides</span>
    <span class="nd-hub-card__desc">How-to recipes</span>
  </a>
  <a class="nd-hub-card" href="/pages/nix-dev/reference" data-no-panel="1">
    <span class="nd-hub-card__title">Reference</span>
    <span class="nd-hub-card__desc">Precise technical detail</span>
  </a>
  <a class="nd-hub-card" href="/pages/nix-dev/concepts" data-no-panel="1">
    <span class="nd-hub-card__title">Concepts</span>
    <span class="nd-hub-card__desc">History and ideas</span>
  </a>
</div>

## Mixed sample (Persian context)

<span id="mixed"></span>

When the page is RTL, English identifiers must stay LTR: install with `curl -L https://nixos.org/nix/install | sh`, then check `nix --version`. Store paths look like `/nix/store/…-hello-2.12.1`.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **Warning**
>
> Do not put secrets under a path that gets copied into the store, for example `./secrets/token`.


## Man-page patterns (from nix-shell)

<span id="manpage"></span>

Patterns taken from `/pages/nix-manual/command-ref/nix-shell` (including `#env-NIX_BUILD_SHELL`). Kept as published on the site so rendering and bugs stay visible.

### Multi-line synopsis

<span id="synopsis"></span>

Man-page command synopsis must **not** be multi-line Markdown prose (lines merge into one paragraph and backticks pair wrongly). Correct form: a fenced `text` block (same as the `nix-shell` page):

```text
nix-shell
  [--arg name value]
  [--argstr name value]
  [{--attr | -A} attrPath]
  [--command cmd]
  [--run cmd]
  [--exclude regexp]
  [--pure]
  [--keep name]
  {{--packages | -p} {packages | expressions} … | [path]}
```

Outside fences, braces still need Svelte escapes: `{'{'}` and `{'}'}`.

### Italic placeholders next to flags

<span id="placeholders"></span>

- `--command` *cmd* — run *cmd* in an interactive shell.
- `--run` *cmd* — same as `--command`, but non-interactive.
- `--exclude` *regexp* — skip dependencies whose store path matches *regexp*.
- `--keep` *name* — keep environment variable *name* under `--pure`.

### Inline code inside a fragment link

<span id="code-in-link"></span>

See also [`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL) and [`NIX_PATH`](#named-heading).

### HTML entities: angle brackets and escaped span id

<span id="html-entities"></span>

Prose with entity form of a Nix path: shell comes from `&lt;nixpkgs&gt;` on `NIX_PATH`.

Inside backticks (as often published): `` `&lt;nixpkgs&gt;` `` versus raw in a fence:

```shell
$ nix-shell '<nixpkgs>' --attr pan
```

Escaped span id wrapping a linked identifier (publish shape around env vars):

- &lt;span id="env-NIX_BUILD_SHELL"&gt;[`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL)&lt;/span&gt;

  Shell used to start the interactive environment.
  Defaults to `bash` from `bashInteractive` in `&lt;nixpkgs&gt;`, else `bash` on `PATH`.

### Callouts nested under a list item

<span id="nested-callouts"></span>

- &lt;span id="env-DEMO"&gt;[`DEMO_VAR`](#env-DEMO)&lt;/span&gt;

  Description of the variable.

  > **Note**
  >
  > Nested note under a list item (strong title only, no `admonition-kind` span).

  > **Example**
  >
  > Nested example callout under the same list item.

### Broken fence-in-callout (published shape)

<span id="broken-fence-callout"></span>

How some manual pages currently ship nested code (open fence not fully inside the quote):

> **Example**
>
> This callout may not wrap the fence cleanly:
>

```nix
  > #!/usr/bin/env -S nix-shell --pure
  > let
  >   pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/854fdc68881791812eddd33b2fed94b954979a8e.tar.gz") {};
  > in
  > pkgs.mkShell {
  >   buildInputs = pkgs.bashInteractive;
  > }
  > ```

### Extra fence languages (shebang examples)

<span id="extra-langs"></span>

#### Python

```python
#! /usr/bin/env nix-shell
#! nix-shell -i python3 --packages python3 python3Packages.prettytable

import prettytable
print("hello")
```

#### Perl

```perl
#! /usr/bin/env nix-shell
#! nix-shell -i perl
#! nix-shell --packages perl

use strict;
print "hello\n";
```

#### Haskell

```haskell
#! /usr/bin/env nix-shell
#! nix-shell -i runghc --packages 'haskellPackages.ghcWithPackages (ps: [ps.tagsoup])'

main = putStrLn "hello"
```

### Indented code block (not fenced)

<span id="indented-code"></span>

Four-space indent (no triple backticks):

    #! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/0672315759b3e15e2121365f067c1c8c56bb4722.tar.gz

### Correct nested fence under a callout (for contrast)

<span id="correct-nested-fence"></span>

> **Note**
>
> Prefer this shape when the fence is fully quoted:
>
> ```shell
> $ nix-shell '<nixpkgs>' --attr pan --pure
> ```

---

End of kitchen sink. If something renders wrong here, fix CSS/mdsvex before touching every doc page.
