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
