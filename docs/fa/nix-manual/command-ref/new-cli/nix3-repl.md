# nix repl - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-repl.html](@docroot@/command-ref/new-cli/nix3-repl.md)

> **Warning**
>
> This program is
> [**experimental**](https://nix.dev/manual/nix/2.34/development/experimental-features#xp-feature-nix-command)
> and its interface is subject to change.

# <a id="name"></a> Name

`nix repl` - start an interactive environment for evaluating Nix expressions

# <a id="synopsis"></a> Synopsis

`nix repl` [*option*...] *installables*...

# <a id="examples"></a> Examples

- Display all special commands within the REPL:
# nix repl
nix-repl> :?
- Evaluate some simple Nix expressions:
# nix repl

nix-repl> 1 + 2
3

nix-repl> map (x: x * 2) [1 2 3]
[ 2 4 6 ]
- Interact with Nixpkgs in the REPL:
# nix repl --file example.nix
Loading Installable ''...
Added 3 variables.

# nix repl --expr '{a={b=3;c=4;};}'
Loading Installable ''...
Added 1 variables.

# nix repl --expr '{a={b=3;c=4;};}' a
Loading Installable ''...
Added 1 variables.

# nix repl --extra-experimental-features 'flakes' nixpkgs
Loading Installable 'flake:nixpkgs#'...
Added 5 variables.

nix-repl> legacyPackages.x86_64-linux.emacs.name
"emacs-27.1"

nix-repl> :q

# nix repl --expr 'import <nixpkgs>{}'

Loading Installable ''...
Added 12439 variables.

nix-repl> emacs.name
"emacs-27.1"

nix-repl> emacs.drvPath
"/nix/store/lp0sjrhgg03y2n0l10n70rg0k7hhyz0l-emacs-27.1.drv"

nix-repl> drv = runCommand "hello" { buildInputs = [ hello ]; } "hello; hello > $out"

nix-repl> :b drv
this derivation produced the following outputs:
 out -> /nix/store/0njwbgwmkwls0w5dv9mpc1pq5fj39q0l-hello

nix-repl> builtins.readFile drv
"Hello, world!\n"

nix-repl> :log drv
Hello, world!

# <a id="description"></a> Description

This command provides an interactive environment for evaluating Nix
expressions. (REPL stands for 'read، eval، print loop'.)

On startup, it loads the Nix expressions named *files* and adds them
into the lexical scope. You can load addition files using the `:l <filename>` command, or reload all files using `:r`.

# <a id="options"></a> Options

- `--stdin`
Read installables from the standard input. No default installable applied.

## <a id="common-evaluation-options"></a> Common evaluation options

- `--arg` *name* *expr*
Pass the value *expr* as the argument *name* to Nix functions.
- `--arg-from-file` *name* *path*
Pass the contents of file *path* as the argument *name* to Nix functions.
- `--arg-from-stdin` *name*
Pass the contents of stdin as the argument *name* to Nix functions.
- `--argstr` *name* *string*
Pass the string *string* as the argument *name* to Nix functions.
- `--debugger`
Start an interactive environment if evaluation fails.
- `--eval-store` *store-url*
The [URL of the Nix store](https://nix.dev/manual/nix/2.34/store/types/#store-url-format)
to use for evaluation, i.e. to store derivations (`.drv` files) and inputs referenced by them.
- `--impure`
Allow access to mutable paths and repositories.
- `--include` / `-I` *path*
Add *path* to search path entries used to resolve [lookup paths](https://nix.dev/manual/nix/2.34/language/constructs/lookup-path)
This option may be given multiple times.
Paths added through `-I` take precedence over the [`nix-path` configuration setting](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-nix-path) and the [`NIX_PATH` environment variable](https://nix.dev/manual/nix/2.34/command-ref/env-common#env-NIX_PATH).
- `--override-flake` *original-ref* *resolved-ref*
Override the flake registries, redirecting *original-ref* to *resolved-ref*.

## <a id="common-flake-related-options"></a> Common flake-related options

- `--commit-lock-file`
Commit changes to the flake's lock file.
- `--inputs-from` *flake-url*
Use the inputs of the specified flake as registry entries.
- `--no-registries`
Don't allow lookups in the flake registries.

**DEPRECATED**
Use [`--no-use-registries`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-use-registries) instead.
- `--no-update-lock-file`
Do not allow any updates to the flake's lock file.
- `--no-write-lock-file`
Do not write the flake's newly generated lock file.
- `--output-lock-file` *flake-lock-path*
Write the given lock file instead of `flake.lock` within the top-level flake.
- `--override-input` *input-path* *flake-url*
Override a specific flake input (e.g. `dwarffs/nixpkgs`). The input path must not be empty. This implies `--no-write-lock-file`.
- `--recreate-lock-file`
Recreate the flake's lock file from scratch.

**DEPRECATED**
Use [`nix flake update`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-flake-update) instead.
- `--reference-lock-file` *flake-lock-path*
Read the given lock file instead of `flake.lock` within the top-level flake.
- `--update-input` *input-path*
Update a specific flake input (ignoring its previous entry in the lock file).

**DEPRECATED**
Use [`nix flake update`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-flake-update) instead.

## <a id="logging-related-options"></a> Logging-related options

- `--debug`
Set the logging verbosity level to 'debug'.
- `--log-format` *format*
Set the format of log output; one of `raw`, `internal-json`, `bar` or `bar-with-logs`.
- `--print-build-logs` / `-L`
Print full build logs on standard error.
- `--quiet`
Decrease the logging verbosity level.
- `--verbose` / `-v`
Increase the logging verbosity level.

## <a id="miscellaneous-global-options"></a> Miscellaneous global options

- `--help`
Show usage information.
- `--offline`
Disable substituters and consider all previously downloaded files up-to-date.
- `--option` *name* *value*
Set the Nix configuration setting *name* to *value* (overriding `nix.conf`).
- `--refresh`
Consider all previously downloaded files out-of-date.
- `--repair`
During evaluation, rewrite missing or corrupted files in the Nix store. During building, rebuild missing or corrupted store paths.
- `--version`
Show version information.

## <a id="options-that-change-the-interpretation-of-installables"></a> Options that change the interpretation of [installables](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix#installables)

- `--expr` *expr*
Interpret [*installables*](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix#installables) as attribute paths relative to the Nix expression *expr*.
- `--file` / `-f` *file*
Interpret [*installables*](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix#installables) as attribute paths relative to the Nix expression stored in *file*. If *file* is the character -, then a Nix expression is read from standard input. Implies `--impure`.

> **Note**
>
> See [`man nix.conf`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#command-line-flags) for overriding configuration settings with command line flags.
