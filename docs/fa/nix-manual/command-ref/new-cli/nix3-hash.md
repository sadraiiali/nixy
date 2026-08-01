# nix hash - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-hash.html](@docroot@/command-ref/new-cli/nix3-hash.md)

> **Warning**
>
> This program is
> [**experimental**](https://nix.dev/manual/nix/2.34/development/experimental-features#xp-feature-nix-command)
> and its interface is subject to change.

# <a id="name"></a> Name

`nix hash` - compute and convert cryptographic hashes

# <a id="synopsis"></a> Synopsis

`nix hash` [*option*...] *subcommand*

where *subcommand* is one of the following:

**Available commands:**

- [`nix hash file`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-file) - print cryptographic hash of a regular file
- [`nix hash path`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-path) - print cryptographic hash of the NAR serialisation of a path
- [`nix hash to-base16`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-to-base16) - convert a hash to base-16 representation (deprecated, use `nix hash convert` instead)
- [`nix hash to-base32`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-to-base32) - convert a hash to base-32 representation (deprecated, use `nix hash convert` instead)
- [`nix hash to-base64`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-to-base64) - convert a hash to base-64 representation (deprecated, use `nix hash convert` instead)
- [`nix hash to-sri`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-to-sri) - convert a hash to SRI representation (deprecated, use `nix hash convert` instead)

**:**

- [`nix hash convert`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-hash-convert) - convert between hash formats

# <a id="options"></a> Options

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
- `--version`
Show version information.

> **Note**
>
> See [`man nix.conf`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#command-line-flags) for overriding configuration settings with command line flags.
