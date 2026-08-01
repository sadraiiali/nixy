# nix hash - Nix 2.34.9 Reference Manual

> Source: [/pages/nix-manual/command-ref/new-cli/nix3-hash](/pages/nix-manual/command-ref/new-cli/nix3-hash)

> **Warning** 
>
> This program is
> [**experimental**](/pages/nix-manual/development/experimental-features#xp-feature-nix-command)
> and its interface is subject to change.

# <a id="name"></a> Name

`nix hash` - compute and convert cryptographic hashes

# <a id="synopsis"></a> Synopsis

`nix hash` [*option*...] *subcommand*

where *subcommand* is one of the following:

**Available commands:**

- [`nix hash file`](/pages/nix-manual/command-ref/experimental-commands) - print cryptographic hash of a regular file
- [`nix hash path`](/pages/nix-manual/command-ref/experimental-commands) - print cryptographic hash of the NAR serialisation of a path
- [`nix hash to-base16`](/pages/nix-manual/command-ref/experimental-commands) - convert a hash to base-16 representation (deprecated, use `nix hash convert` instead)
- [`nix hash to-base32`](/pages/nix-manual/command-ref/experimental-commands) - convert a hash to base-32 representation (deprecated, use `nix hash convert` instead)
- [`nix hash to-base64`](/pages/nix-manual/command-ref/experimental-commands) - convert a hash to base-64 representation (deprecated, use `nix hash convert` instead)
- [`nix hash to-sri`](/pages/nix-manual/command-ref/experimental-commands) - convert a hash to SRI representation (deprecated, use `nix hash convert` instead)

**:**

- [`nix hash convert`](/pages/nix-manual/command-ref/experimental-commands) - convert between hash formats

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
> See [`man nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix#command-line-flags) for overriding configuration settings with command line flags.
