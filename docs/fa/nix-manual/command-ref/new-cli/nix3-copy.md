# nix copy - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-copy.html](@docroot@/command-ref/new-cli/nix3-copy.md)

> **Warning**
>
> This program is
> [**experimental**](https://nix.dev/manual/nix/2.34/development/experimental-features#xp-feature-nix-command)
> and its interface is subject to change.

# <a id="name"></a> Name

`nix copy` - copy paths between Nix stores

# <a id="synopsis"></a> Synopsis

`nix copy` [*option*...] *installables*...

# <a id="examples"></a> Examples

- Copy Firefox from the local store to a binary cache in `/tmp/cache`:
# nix copy --to file:///tmp/cache $(type -p firefox)

Note the `file://` - without this, the destination is a chroot
store, not a binary cache.
- Copy all store paths from a local binary cache in `/tmp/cache` to the local store:
# nix copy --all --from file:///tmp/cache
- Copy the entire current NixOS system closure to another machine via
SSH:
# nix copy --substitute-on-destination --to ssh://server /run/current-system

The `-s` flag causes the remote machine to try to substitute missing
store paths, which may be faster if the link between the local and
remote machines is slower than the link between the remote machine
and its substituters (e.g. `https://cache.nixos.org`).
- Copy a closure from another machine via SSH:
# nix copy --from ssh://server /nix/store/a6cnl93nk1wxnq84brbbwr6hxw9gp2w9-blender-2.79-rc2
- Copy Hello to a binary cache in an Amazon S3 bucket:
# nix copy --to s3://my-bucket?region=eu-west-1 nixpkgs#hello

or to an S3-compatible storage system:
# nix copy --to s3://my-bucket?region=eu-west-1&endpoint=example.com nixpkgs#hello

Note that this only works if Nix is built with AWS support.
- Copy a closure from `/nix/store` to the chroot store `/tmp/nix/nix/store`:
# nix copy --to /tmp/nix nixpkgs#hello --no-check-sigs
- Update the NixOS system profile to point to a closure copied from a
remote machine:
# nix copy --from ssh://server \
 --profile /nix/var/nix/profiles/system \
 /nix/store/r14v3km89zm3prwsa521fab5kgzvfbw4-nixos-system-foobar-24.05.20240925.759537f

# <a id="description"></a> Description

`nix copy` copies store path closures between two Nix stores. The
source store is specified using `--from` and the destination using
`--to`. If one of these is omitted, it defaults to the local store.

# <a id="options"></a> Options

- `--from` *store-uri*
URL of the source Nix store.
- `--no-check-sigs`
Do not require that paths are signed by trusted keys.
- `--out-link` / `-o` *path*
Create symlinks prefixed with *path* to the top-level store paths fetched from the source store.
- `--profile` *path*
The profile to operate on.
- `--stdin`
Read installables from the standard input. No default installable applied.
- `--substitute-on-destination` / `-s`
Whether to try substitutes on the destination store (only supported by SSH stores).
- `--to` *store-uri*
URL of the destination Nix store.

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

- `--all`
Apply the operation to every store path.
- `--derivation`
Operate on the [store derivation](https://nix.dev/manual/nix/2.34/glossary#gloss-store-derivation) rather than its outputs.
- `--expr` *expr*
Interpret [*installables*](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix#installables) as attribute paths relative to the Nix expression *expr*.
- `--file` / `-f` *file*
Interpret [*installables*](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix#installables) as attribute paths relative to the Nix expression stored in *file*. If *file* is the character -, then a Nix expression is read from standard input. Implies `--impure`.
- `--no-recursive`
Apply operation to specified paths only.

> **Note**
>
> See [`man nix.conf`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#command-line-flags) for overriding configuration settings with command line flags.
