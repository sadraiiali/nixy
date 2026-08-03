# 8.6.1. nix.conf

> Source: [/pages/nix-manual/command-ref/conf-file-prefix](/pages/nix-manual/command-ref/conf-file)

## <a id="name"></a> Name
`nix.conf` - Nix configuration file

## <a id="description"></a> Description
Nix supports a variety of configuration settings, which are read from configuration files or taken as command line flags.

## <a id="configuration-file"></a> Configuration file

By default Nix reads settings from the following places, in that order:

1. The system-wide configuration file `sysconfdir/nix/nix.conf` (i.e. `/etc/nix/nix.conf` on most systems), or `$NIX_CONF_DIR/nix.conf` if [`NIX_CONF_DIR`](/pages/nix-manual/command-ref/env-common#env-NIX_CONF_DIR) is set. 
 Values loaded in this file are not forwarded to the Nix daemon.
The client assumes that the daemon has already loaded them.
2. If [`NIX_USER_CONF_FILES`](/pages/nix-manual/command-ref/env-common#env-NIX_USER_CONF_FILES) is set, then each path separated by `:` will be loaded in reverse order. 
 Otherwise it will look for `nix/nix.conf` files in `XDG_CONFIG_DIRS` and [`XDG_CONFIG_HOME`](/pages/nix-manual/command-ref/env-common#env-XDG_CONFIG_HOME).
If unset, `XDG_CONFIG_DIRS` defaults to `/etc/xdg`, and `XDG_CONFIG_HOME` defaults to `$HOME/.config` as per [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).
3. If [`NIX_CONFIG`](/pages/nix-manual/command-ref/env-common#env-NIX_CONFIG) is set, its contents are treated as the contents of a configuration file.

### <a id="file-format"></a> File format

Configuration files consist of `name = value` pairs, one per line.
Comments start with a `#` character.

Example:

```
keep-outputs = true       # Nice for developers
keep-derivations = true   # Idem
```

Other files can be included with a line like `include &lt;path&gt;`, where `&lt;path&gt;` is interpreted relative to the current configuration file.
A missing file is an error unless `!include` is used instead.

A configuration setting usually overrides any previous value.
However, for settings that take a list of items, you can prefix the name of the setting by `extra-` to *append* to the previous value.

For instance,

```
substituters = a b
extra-substituters = c d
```

defines the `substituters` setting to be `a b c d`.

Unknown option names are not an error, and are simply ignored with a warning.

## <a id="command-line-flags"></a> Command line flags

Configuration options can be set on the command line, overriding the values set in the configuration file:

- Every configuration setting has corresponding command line flag (e.g. `--max-jobs 16`).
Boolean settings do not need an argument, and can be explicitly disabled with the `no-` prefix (e.g. `--keep-failed` and `--no-keep-failed`). 
 Unknown option names are invalid flags (unless there is already a flag with that name), and are rejected with an error.
- The flag `--option &lt;name&gt; &lt;value&gt;` is interpreted exactly like a `&lt;name&gt; = &lt;value&gt;` in a setting file. 
 Unknown option names are ignored with a warning.

The `extra-` prefix is supported for settings that take a list of items (e.g. `--extra-trusted users alice` or `--option extra-trusted-users alice`).

## <a id="integer-settings"></a> Integer settings

Settings that have an integer type support the suffixes `K`, `M`, `G`
and `T`. These cause the specified value to be multiplied by 2^10,
2^20, 2^30 and 2^40, respectively. For instance, `--min-free 1M` is
equivalent to `--min-free 1048576`.

# <a id="available-settings"></a> Available settings

- <a id="conf-abort-on-warn"></a><a id="conf-abort-on-warn"></a>`abort-on-warn` 
 If set to true, [`builtins.warn`](/pages/nix-manual/language/builtins-prefix#builtins-warn) throws an error when logging a warning. 
 This will give you a stack trace that leads to the location of the warning. 
 This is useful for finding information about warnings in third-party Nix code when you can not start the interactive debugger, such as when Nix is called from a non-interactive script. See `debugger-on-warn`. 
 Currently, a stack trace can only be produced when the debugger is enabled, or when evaluation is aborted. 
 This option can be enabled by setting `NIX_ABORT_ON_WARN=1` in the environment. 
 **Default:** `false`
- <a id="conf-accept-flake-config"></a><a id="conf-accept-flake-config"></a>`accept-flake-config` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`flakes` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-flakes)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = flakes
> accept-flake-config = ...
> ```
 Whether to accept Nix configuration settings from a flake without prompting. 
 **Default:** `false`
- <a id="conf-access-tokens"></a><a id="conf-access-tokens"></a>`access-tokens` 
 Access tokens used to access protected GitHub, GitLab, or
other locations requiring token-based authentication. 
 Access tokens are specified as a string made up of
space-separated `host=token` values. The specific token
used is selected by matching the `host` portion against the
"host" specification of the input. The `host` portion may
contain a path element which matches against the prefix
URL for the input. (eg: `github.com/org=token`). The actual use
of the `token` value is determined by the type of resource
being accessed: 
 
 Example `~/.config/nix/nix.conf`: 
```
access-tokens = github.com=23ac...b289 gitlab.mycompany.com=PAT:A123Bp_Cd..EfG gitlab.com=OAuth2:1jklw3jk
```
 Example `~/code/flake.nix`: 
```
input.foo = {
 type = "gitlab";
 host = "gitlab.mycompany.com";
 owner = "mycompany";
 repo = "pro";
};
```
 This example specifies three tokens, one each for accessing
github.com, gitlab.mycompany.com, and gitlab.com. 
 The `input.foo` uses the "gitlab" fetcher, which might
requires specifying the token type along with the token
value. 
 **Default:** *empty*
  - Github: the token value is the OAUTH-TOKEN string obtained
as the Personal Access Token from the Github server (see
https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps).
  - Gitlab: the token value is either the OAuth2 token or the
Personal Access Token (these are different types tokens
for gitlab, see
https://docs.gitlab.com/12.10/ee/api/README.html#authentication).
The `token` value should be `type:tokenstring` where
`type` is either `OAuth2` or `PAT` to indicate which type
of token is being specified.
- <a id="conf-allow-dirty"></a><a id="conf-allow-dirty"></a>`allow-dirty` 
 Whether to allow dirty Git/Mercurial trees. 
 **Default:** `true`
- <a id="conf-allow-dirty-locks"></a><a id="conf-allow-dirty-locks"></a>`allow-dirty-locks` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`flakes` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-flakes)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = flakes
> allow-dirty-locks = ...
> ```
 Whether to allow dirty inputs (such as dirty Git workdirs)
to be locked via their NAR hash. This is generally bad
practice since Nix has no way to obtain such inputs if they
are subsequently modified. Therefore lock files with dirty
locks should generally only be used for local testing, and
should not be pushed to other users. 
 **Default:** `false`
- <a id="conf-allow-import-from-derivation"></a><a id="conf-allow-import-from-derivation"></a>`allow-import-from-derivation` 
 By default, Nix allows [Import from Derivation](/pages/nix-manual/language/import-from-derivation). 
 With this option set to `false`, Nix throws an error when evaluating an expression that uses this feature,
even when the required store object is readily available.
This ensures that evaluation doesn't require any builds to take place,
regardless of the state of the store. 
 **Default:** `true`
- <a id="conf-allow-new-privileges"></a><a id="conf-allow-new-privileges"></a>`allow-new-privileges` 
 (Linux-specific.) By default, builders on Linux cannot acquire new
privileges by calling setuid/setgid programs or programs that have
file capabilities. For example, programs such as `sudo` or `ping`
should fail. (Note that in sandbox builds, no such programs are
available unless you bind-mount them into the sandbox via the
`sandbox-paths` option.) You can allow the use of such programs by
enabling this option. This is impure and usually undesirable, but
may be useful in certain scenarios (e.g. to spin up containers or
set up userspace network interfaces in tests). 
 **Default:** `false`
- <a id="conf-allow-symlinked-store"></a><a id="conf-allow-symlinked-store"></a>`allow-symlinked-store` 
 If set to `true`, Nix stops complaining if the store directory
(typically `/nix/store`) contains symlink components. 
 This risks making some builds "impure" because builders sometimes
"canonicalise" paths by resolving all symlink components. Problems
occur if those builds are then deployed to machines where /nix/store
resolves to a different location from that of the build machine. You
can enable this setting if you are sure you're not going to do that. 
 **Default:** `false`
- <a id="conf-allow-unsafe-native-code-during-evaluation"></a><a id="conf-allow-unsafe-native-code-during-evaluation"></a>`allow-unsafe-native-code-during-evaluation` 
 Enable built-in functions that allow executing native code. 
 In particular, this adds: 
 
 **Default:** `false`
  - `builtins.importNative` *path* *symbol* 
 Opens dynamic shared object (DSO) at *path*, loads the function with the symbol name *symbol* from it and runs it.
The loaded function must have the following signature: 
```
extern "C" typedef void (*ValueInitialiser) (EvalState & state, Value & v);
```
 The [Nix C++ API documentation](/pages/nix-manual/development/documentation#api-documentation) has more details on evaluator internals.
  - `builtins.exec` *arguments* 
 Execute a program, where *arguments* are specified as a list of strings, and parse its output as a Nix expression.
- <a id="conf-allowed-impure-host-deps"></a><a id="conf-allowed-impure-host-deps"></a>`allowed-impure-host-deps` 
 Which prefixes to allow derivations to ask for access to (primarily for Darwin). 
 **Default:** *empty*
- <a id="conf-allowed-uris"></a><a id="conf-allowed-uris"></a>`allowed-uris` 
 A list of URI prefixes to which access is allowed in restricted
evaluation mode. For example, when set to
`https://github.com/NixOS`, builtin functions such as `fetchGit` are
allowed to access `https://github.com/NixOS/patchelf.git`. 
 Access is granted when 
 
 **Default:** *empty*
  - the URI is equal to the prefix,
  - or the URI is a subpath of the prefix,
  - or the prefix is a URI scheme ended by a colon `:` and the URI has the same scheme.
- <a id="conf-allowed-users"></a><a id="conf-allowed-users"></a>`allowed-users` 
 A list of user names, separated by whitespace.
These users are allowed to connect to the Nix daemon. 
 You can specify groups by prefixing names with `@`.
For instance, `@wheel` means all users in the `wheel` group.
Also, you can allow all users by specifying `*`. 
 > **Note**
>
> Trusted users (set in `trusted-users`) can always connect to the Nix daemon. 
 **Default:** `*`
- <a id="conf-always-allow-substitutes"></a><a id="conf-always-allow-substitutes"></a>`always-allow-substitutes` 
 If set to `true`, Nix ignores the [`allowSubstitutes`](/pages/nix-manual/language/advanced-attributes) attribute in derivations and always attempt to use available substituters. 
 **Default:** `false`
- <a id="conf-auto-allocate-uids"></a><a id="conf-auto-allocate-uids"></a>`auto-allocate-uids` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`auto-allocate-uids` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-auto-allocate-uids)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = auto-allocate-uids
> auto-allocate-uids = ...
> ```
 Whether to select UIDs for builds automatically, instead of using the
users in `build-users-group`. 
 UIDs are allocated starting at 872415232 (0x34000000) on Linux and 56930 on macOS. 
 **Default:** `false`
- <a id="conf-auto-optimise-store"></a><a id="conf-auto-optimise-store"></a>`auto-optimise-store` 
 If set to `true`, Nix automatically detects files in the store
that have identical contents, and replaces them with hard links to
a single copy. This saves disk space. If set to `false` (the
default), you can still run `nix-store --optimise` to get rid of
duplicate files. 
 **Default:** `false`
- <a id="conf-bash-prompt"></a><a id="conf-bash-prompt"></a>`bash-prompt` 
 The bash prompt (`PS1`) in `nix develop` shells. 
 **Default:** *empty*
- <a id="conf-bash-prompt-prefix"></a><a id="conf-bash-prompt-prefix"></a>`bash-prompt-prefix` 
 Prefix prepended to the `PS1` environment variable in `nix develop` shells. 
 **Default:** *empty*
- <a id="conf-bash-prompt-suffix"></a><a id="conf-bash-prompt-suffix"></a>`bash-prompt-suffix` 
 Suffix appended to the `PS1` environment variable in `nix develop` shells. 
 **Default:** *empty*
- <a id="conf-build-dir"></a><a id="conf-build-dir"></a>`build-dir` 
 Override the `build-dir` store setting for all stores that have this setting. 
 See also the per-store [`build-dir`](/pages/nix-manual/store/types/local-store#store-local-store-build-dir) setting. 
 **Default:** ``
- <a id="conf-build-hook"></a><a id="conf-build-hook"></a>`build-hook` 
 The path to the helper program that executes remote builds. 
 Nix communicates with the build hook over `stdio` using a custom protocol to request builds that cannot be performed directly by the Nix daemon.
The default value is the internal Nix binary that implements remote building. 
 > **Important**
>
> Change this setting only if you really know what you’re doing. 
 **Default:** `nix __build-remote`
- <a id="conf-build-poll-interval"></a><a id="conf-build-poll-interval"></a>`build-poll-interval` 
 How often (in seconds) to poll for locks. 
 **Default:** `5`
- <a id="conf-build-users-group"></a><a id="conf-build-users-group"></a>`build-users-group` 
 This options specifies the Unix group containing the Nix build user
accounts. In multi-user Nix installations, builds should not be
performed by the Nix account since that would allow users to
arbitrarily modify the Nix store and database by supplying specially
crafted builders; and they cannot be performed by the calling user
since that would allow him/her to influence the build result. 
 Therefore, if this option is non-empty and specifies a valid group,
builds are performed under the user accounts that are a member
of the group specified here (as listed in `/etc/group`). Those user
accounts should not be used for any other purpose! 
 Nix never runs two builds under the same user account at the
same time. This is to prevent an obvious security hole: a malicious
user writing a Nix expression that modifies the build result of a
legitimate Nix expression being built by another user. Therefore it
is good to have as many Nix build user accounts as you can spare.
(Remember: uids are cheap.) 
 The build users should have permission to create files in the Nix
store, but not delete them. Therefore, `/nix/store` should be owned
by the Nix account, its group should be the group specified here,
and its mode should be `1775`. 
 If the build users group is empty, builds are performed under
the uid of the Nix process (that is, the uid of the caller if
`NIX_REMOTE` is empty, the uid under which the Nix daemon runs if
`NIX_REMOTE` is `daemon`). Obviously, this should not be used
with a nix daemon accessible to untrusted clients. 
 Defaults to `nixbld` when running as root, *empty* otherwise. 
 **Default:** *machine-specific*
- <a id="conf-builders"></a><a id="conf-builders"></a>`builders` 
 A semicolon- or newline-separated list of build machines. 
 In addition to the [usual ways of setting configuration options](/pages/nix-manual/command-ref/conf-file-prefix), the value can be read from a file by prefixing its absolute path with `@`. 
 > **Example**
>
> This is the default setting:
>
> ```
> builders = @/etc/nix/machines
> ```
 Each machine specification consists of the following elements, separated by spaces.
Only the first element is required.
To leave a field at its default, set it to `-`. 
 
 > **Example**
>
> Multiple builders specified on the command line:
>
> ```
> --builders 'ssh://mac x86_64-darwin ; ssh://beastie x86_64-freebsd'
> ```
 > **Example**
>
> This specifies several machines that can perform `i686-linux` builds:
>
> ```
> nix@scratchy.labs.cs.uu.nl i686-linux /home/nix/.ssh/id_scratchy 8 1 kvm
> nix@itchy.labs.cs.uu.nl i686-linux /home/nix/.ssh/id_scratchy 8 2
> nix@poochie.labs.cs.uu.nl i686-linux /home/nix/.ssh/id_scratchy 1 2 kvm benchmark
> ```
>
> However, `poochie` only builds derivations that have the attribute
>
> ```
> requiredSystemFeatures = [ "benchmark" ];
> ```
>
> or
>
> ```
> requiredSystemFeatures = [ "benchmark" "kvm" ];
> ```
>
> `itchy` cannot do builds that require `kvm`, but `scratchy` does support such builds.
> For regular builds, `itchy` is preferred over `scratchy` because it has a higher speed factor. 
 For Nix to use substituters, the calling user must be in the `trusted-users` list. 
 > **Note**
>
> A build machine must be accessible via SSH and have Nix installed.
> `nix` must be available in `$PATH` for the user connecting over SSH. 
 > **Warning**
>
> If you are building via the Nix daemon (default), the Nix daemon user account on the local machine (that is, `root`) requires access to a user account on the remote machine (not necessarily `root`).
>
> If you can’t or don’t want to configure `root` to be able to access the remote machine, set `store` to any [local store](/pages/nix-manual/store/types/local-store), e.g. by passing `--store /tmp` to the command on the local machine. 
 To build only on remote machines and disable local builds, set `max-jobs` to 0. 
 If you want the remote machines to use substituters, set `builders-use-substitutes` to `true`. 
 **Default:** *machine-specific*
  1. The URI of the remote store in the format `ssh://[username@]hostname[:port]`. 
 > **Example**
>
> `ssh://nix@mac` 
 For backward compatibility, `ssh://` may be omitted.
The hostname may be an alias defined in `~/.ssh/config`.
  2. A comma-separated list of [Nix system types](/pages/nix-manual/development/building#system-type).
If omitted, this defaults to the local platform type. 
 > **Example**
>
> `aarch64-darwin` 
 It is possible for a machine to support multiple platform types. 
 > **Example**
>
> `i686-linux,x86_64-linux`
  3. The SSH identity file to be used to log in to the remote machine.
If omitted, SSH uses its regular identities. 
 > **Example**
>
> `/home/user/.ssh/id_mac`
  4. The maximum number of builds that Nix executes in parallel on the machine.
Typically this should be equal to the number of CPU cores.
  5. The “speed factor”, indicating the relative speed of the machine as a positive integer.
If there are multiple machines of the right type, Nix prefers the fastest, taking load into account.
  6. A comma-separated list of supported system features. 
 A machine is only used to build a derivation if all the features in the derivation's [`requiredSystemFeatures`](/pages/nix-manual/language/advanced-attributes#adv-attr-requiredSystemFeatures) attribute are supported by that machine.
  7. A comma-separated list of required system features. 
 A machine is only used to build a derivation if all of the machine’s required features appear in the derivation’s [`requiredSystemFeatures`](/pages/nix-manual/language/advanced-attributes#adv-attr-requiredSystemFeatures) attribute.
  8. The (base64-encoded) public host key of the remote machine.
If omitted, SSH uses its regular `known_hosts` file. 
 The value for this field can be obtained via `base64 -w0`.
- <a id="conf-builders-use-substitutes"></a><a id="conf-builders-use-substitutes"></a>`builders-use-substitutes` 
 If set to `true`, Nix instructs remote build machines to use their own `substituters` if available. 
 It means that remote build hosts fetch as many dependencies as possible from their own substituters (e.g, from `cache.nixos.org`) instead of waiting for the local machine to upload them all.
This can drastically reduce build times if the network connection between the local machine and the remote build host is slow. 
 **Default:** `false`
- <a id="conf-commit-lock-file-summary"></a><a id="conf-commit-lock-file-summary"></a>`commit-lock-file-summary` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`flakes` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-flakes)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = flakes
> commit-lock-file-summary = ...
> ```
 The commit summary to use when committing changed flake lock files. If
empty, the summary is generated based on the action performed. 
 **Default:** *empty* 
 **Deprecated alias:** `commit-lockfile-summary`
- <a id="conf-compress-build-log"></a><a id="conf-compress-build-log"></a>`compress-build-log` 
 If set to `true` (the default), build logs written to
`/nix/var/log/nix/drvs` are compressed on the fly using bzip2.
Otherwise, they are not compressed. 
 **Default:** `true` 
 **Deprecated alias:** `build-compress-log`
- <a id="conf-connect-timeout"></a><a id="conf-connect-timeout"></a>`connect-timeout` 
 The timeout (in seconds) for establishing connections in the
binary cache substituter. It corresponds to `curl`’s
`--connect-timeout` option. A value of 0 means no limit. 
 **Default:** `15`
- <a id="conf-cores"></a><a id="conf-cores"></a>`cores` 
 Sets the value of the `NIX_BUILD_CORES` environment variable in the [invocation of the `builder` executable](/pages/nix-manual/store/building#builder-execution) of a derivation.
The `builder` executable can use this variable to control its own maximum amount of parallelism. 
 
FIXME(@fricklerhandwerk): I don't think this should even be mentioned here.
A very generic example using `derivation` and `xargs` may be more appropriate to explain the mechanism.
Using `mkDerivation` as an example requires being aware of that there are multiple independent layers that are completely opaque here.
 
 For instance, in Nixpkgs, if the attribute `enableParallelBuilding` for the `mkDerivation` build helper is set to `true`, it passes the `-j$`flag to GNU Make. 
 If set to`0`, nix will detect the number of CPU cores and pass this number via `NIX_BUILD_CORES`. 
 > **Note**
>
> The number of parallel local Nix build jobs is independently controlled with the `max-jobs` setting. 
 **Default:** `0` 
 **Deprecated alias:** `build-cores`
- <a id="conf-debugger-on-trace"></a><a id="conf-debugger-on-trace"></a>`debugger-on-trace` 
 If set to true and the `--debugger` flag is given, the following functions
enter the debugger like [`builtins.break`](/pages/nix-manual/language/builtins-prefix#builtins-break): 
 
 This is useful for debugging warnings in third-party Nix code. 
 **Default:** `false`
  - [`builtins.trace`](/pages/nix-manual/language/builtins-prefix#builtins-trace)
  - [`builtins.traceVerbose`](/pages/nix-manual/language/builtins-prefix#builtins-traceVerbose) 
if `trace-verbose` is set to true.
  - [`builtins.warn`](/pages/nix-manual/language/builtins-prefix#builtins-warn)
- <a id="conf-debugger-on-warn"></a><a id="conf-debugger-on-warn"></a>`debugger-on-warn` 
 If set to true and the `--debugger` flag is given, [`builtins.warn`](/pages/nix-manual/language/builtins-prefix#builtins-warn)
will enter the debugger like [`builtins.break`](/pages/nix-manual/language/builtins-prefix#builtins-break). 
 This is useful for debugging warnings in third-party Nix code. 
 Use `debugger-on-trace` to also enter the debugger on legacy warnings that are logged with [`builtins.trace`](/pages/nix-manual/language/builtins-prefix#builtins-trace). 
 **Default:** `false`
- <a id="conf-diff-hook"></a><a id="conf-diff-hook"></a>`diff-hook` 
 Absolute path to an executable capable of diffing build
results. The hook is executed if `run-diff-hook` is true, and the
output of a build is known to not be the same. This program is not
executed to determine if two results are the same. 
 The diff hook is executed by the same user and group who ran the
build. However, the diff hook does not have write access to the
store path just built. 
 The diff hook program receives three parameters: 
 
 The stderr and stdout output from the diff hook isn't displayed
to the user. Instead, it prints to the nix-daemon's log. 
 When using the Nix daemon, `diff-hook` must be set in the `nix.conf`
configuration file, and cannot be passed at the command line. 
 **Default:** ``
  1. A path to the previous build's results
  2. A path to the current build's results
  3. The path to the build's derivation
  4. The path to the build's scratch directory. This directory
exists only if the build was run with `--keep-failed`.
- <a id="conf-download-attempts"></a><a id="conf-download-attempts"></a>`download-attempts` 
 The number of times Nix attempts to download a file before giving up. 
 **Default:** `5`
- <a id="conf-download-buffer-size"></a><a id="conf-download-buffer-size"></a>`download-buffer-size` 
 The size of Nix's internal download buffer in bytes during `curl` transfers. If data is
not processed quickly enough to exceed the size of this buffer, downloads may stall.
The default is 1048576 (1 MiB). 
 **Default:** `1048576`
- <a id="conf-download-speed"></a><a id="conf-download-speed"></a>`download-speed` 
 Specify the maximum transfer rate in kilobytes per second you want
Nix to use for downloads. 
 **Default:** `0`
- <a id="conf-eval-attrset-update-layer-rhs-threshold"></a><a id="conf-eval-attrset-update-layer-rhs-threshold"></a>`eval-attrset-update-layer-rhs-threshold` 
 Tunes the maximum size of an attribute set that, when used
as a right operand in an [attribute set update expression](/pages/nix-manual/language/operators#update),
uses a more space-efficient linked-list representation of attribute sets. 
 Setting this to larger values generally leads to less memory allocations,
but may lead to worse evaluation performance. 
 A value of `0` disables this optimization completely. 
 This is an advanced performance tuning option and typically should not be changed.
The default value is chosen to balance performance and memory usage. On 32 bit systems
where memory is scarce, the default is a large value to reduce the amount of allocations. 
 **Default:** `16`
- <a id="conf-eval-cache"></a><a id="conf-eval-cache"></a>`eval-cache` 
 Whether to use the flake evaluation cache.
Certain commands won't have to evaluate when invoked for the second time with a particular version of a flake.
Intermediate results are not cached. 
 **Default:** `true`
- <a id="conf-eval-profile-file"></a><a id="conf-eval-profile-file"></a>`eval-profile-file` 
 Specifies the file where evaluation profile is saved. 
 **Default:** `nix.profile`
- <a id="conf-eval-profiler"></a><a id="conf-eval-profiler"></a>`eval-profiler` 
 Enables evaluation profiling. The following modes are supported: 
 
 Use `eval-profile-file` to specify where the profile is saved. 
 See [Using the `eval-profiler`](/pages/nix-manual/advanced-topics/eval-profiler). 
 **Default:** `disabled`
  - `flamegraph` stack sampling profiler. Outputs folded format, one line per stack (suitable for `flamegraph.pl` and compatible tools).
- <a id="conf-eval-profiler-frequency"></a><a id="conf-eval-profiler-frequency"></a>`eval-profiler-frequency` 
 Specifies the sampling rate in hertz for sampling evaluation profilers.
Use `0` to sample the stack after each function call.
See `eval-profiler`. 
 **Default:** `99`
- <a id="conf-eval-system"></a><a id="conf-eval-system"></a>`eval-system` 
 This option defines
[`builtins.currentSystem`](/pages/nix-manual/language/builtins-prefix#builtins-currentSystem)
in the Nix language if it is set as a non-empty string.
Otherwise, if it is defined as the empty string (the default), the value of the
`system` 
configuration setting is used instead. 
 Unlike `system`, this setting does not change what kind of derivations can be built locally.
This is useful for evaluating Nix code on one system to produce derivations to be built on another type of system. 
 **Default:** *empty*
- <a id="conf-experimental-features"></a><a id="conf-experimental-features"></a>`experimental-features` 
 Experimental features that are enabled. 
 Example: 
```
experimental-features = nix-command flakes
```
 The following experimental features are available: 
 
 Experimental features are [further documented in the manual](/pages/nix-manual/development/experimental-features). 
 **Default:** *empty*
  - [`auto-allocate-uids`](/pages/nix-manual/development/experimental-features#xp-feature-auto-allocate-uids)
  - [`blake3-hashes`](/pages/nix-manual/development/experimental-features#xp-feature-blake3-hashes)
  - [`ca-derivations`](/pages/nix-manual/development/experimental-features#xp-feature-ca-derivations)
  - [`cgroups`](/pages/nix-manual/development/experimental-features#xp-feature-cgroups)
  - [`configurable-impure-env`](/pages/nix-manual/development/experimental-features#xp-feature-configurable-impure-env)
  - [`daemon-trust-override`](/pages/nix-manual/development/experimental-features#xp-feature-daemon-trust-override)
  - [`dynamic-derivations`](/pages/nix-manual/development/experimental-features#xp-feature-dynamic-derivations)
  - [`external-builders`](/pages/nix-manual/development/experimental-features#xp-feature-external-builders)
  - [`fetch-closure`](/pages/nix-manual/development/experimental-features#xp-feature-fetch-closure)
  - [`fetch-tree`](/pages/nix-manual/development/experimental-features#xp-feature-fetch-tree)
  - [`flakes`](/pages/nix-manual/development/experimental-features#xp-feature-flakes)
  - [`git-hashing`](/pages/nix-manual/development/experimental-features#xp-feature-git-hashing)
  - [`impure-derivations`](/pages/nix-manual/development/experimental-features#xp-feature-impure-derivations)
  - [`local-overlay-store`](/pages/nix-manual/development/experimental-features#xp-feature-local-overlay-store)
  - [`mounted-ssh-store`](/pages/nix-manual/development/experimental-features#xp-feature-mounted-ssh-store)
  - [`nix-command`](/pages/nix-manual/development/experimental-features#xp-feature-nix-command)
  - [`parse-toml-timestamps`](/pages/nix-manual/development/experimental-features#xp-feature-parse-toml-timestamps)
  - [`pipe-operators`](/pages/nix-manual/development/experimental-features#xp-feature-pipe-operators)
  - [`read-only-local-store`](/pages/nix-manual/development/experimental-features#xp-feature-read-only-local-store)
  - [`recursive-nix`](/pages/nix-manual/development/experimental-features#xp-feature-recursive-nix)
  - [`verified-fetches`](/pages/nix-manual/development/experimental-features#xp-feature-verified-fetches)
- <a id="conf-external-builders"></a><a id="conf-external-builders"></a>`external-builders` 
 Helper programs that execute derivations. 
 The program is passed a JSON document that describes the build environment as the final argument.
The JSON document looks like this: 
 {'{'}
"args": [
"-e",
"/nix/store/vj1c3wf9…-source-stdenv.sh",
"/nix/store/shkw4qm9…-default-builder.sh"
],
"builder": "/nix/store/s1qkj0ph…-bash-5.2p37/bin/bash",
"env": {'{'}
"HOME": "/homeless-shelter",
"builder": "/nix/store/s1qkj0ph…-bash-5.2p37/bin/bash",
"nativeBuildInputs": "/nix/store/l31j72f1…-version-check-hook",
"out": "/nix/store/2yx2prgx…-hello-2.12.2"
…
{'}'},
"inputPaths": [
"/nix/store/14dciax3…-glibc-2.32-54-dev",
"/nix/store/1azs5s8z…-gettext-0.21",
…
],
"outputs": {'{'}
"out": "/nix/store/2yx2prgx…-hello-2.12.2"
{'}'},
"realStoreDir": "/nix/store",
"storeDir": "/nix/store",
"system": "aarch64-linux",
"tmpDir": "/private/tmp/nix-build-hello-2.12.2.drv-0/build",
"tmpDirInSandbox": "/build",
"topTmpDir": "/private/tmp/nix-build-hello-2.12.2.drv-0",
"version": 1
{'}'} 
 **Default:** *empty*
- <a id="conf-extra-platforms"></a><a id="conf-extra-platforms"></a>`extra-platforms` 
 System types of executables that can be run on this machine. 
 Nix only builds a given [store derivation](/pages/nix-manual/glossary#gloss-store-derivation) locally when its `system` attribute equals any of the values specified here or in the `system` option. 
 Setting this can be useful to build derivations locally on compatible machines: 
 
 Build systems usually detect the target platform to be the current physical system and therefore produce machine code incompatible with what may be intended in the derivation.
You should design your derivation's `builder` accordingly and cross-check the results when using this option against natively-built versions of your derivation. 
 **Default:** *machine-specific*
  - `i686-linux` executables can be run on `x86_64-linux` machines (set by default)
  - `x86_64-darwin` executables can be run on macOS `aarch64-darwin` with Rosetta 2 (set by default where applicable)
  - `armv6` and `armv5tel` executables can be run on `armv7`
  - some `aarch64` machines can also natively run 32-bit ARM code
  - `qemu-user` may be used to support non-native platforms (though this
may be slow and buggy)
- <a id="conf-fallback"></a><a id="conf-fallback"></a>`fallback` 
 If set to `true`, Nix falls back to building from source if a
binary substitute fails. This is equivalent to the `--fallback`
flag. The default is `false`. 
 **Default:** `false` 
 **Deprecated alias:** `build-fallback`
- <a id="conf-filter-syscalls"></a><a id="conf-filter-syscalls"></a>`filter-syscalls` 
 Whether to prevent certain dangerous system calls, such as
creation of setuid/setgid files or adding ACLs or extended
attributes. Only disable this if you're aware of the
security implications. 
 **Default:** `true`
- <a id="conf-flake-registry"></a><a id="conf-flake-registry"></a>`flake-registry` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`flakes` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-flakes)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = flakes
> flake-registry = ...
> ```
 Path or URI of the global flake registry. 
 When empty, disables the global flake registry. 
 **Default:** `https://channels.nixos.org/flake-registry.json`
- <a id="conf-fsync-metadata"></a><a id="conf-fsync-metadata"></a>`fsync-metadata` 
 If set to `true`, changes to the Nix store metadata (in
`/nix/var/nix/db`) are synchronously flushed to disk. This improves
robustness in case of system crashes, but reduces performance. The
default is `true`. 
 **Default:** `true`
- <a id="conf-fsync-store-paths"></a><a id="conf-fsync-store-paths"></a>`fsync-store-paths` 
 Whether to call `fsync()` on store paths before registering them, to
flush them to disk. This improves robustness in case of system crashes,
but reduces performance. The default is `false`. 
 **Default:** `false`
- <a id="conf-gc-reserved-space"></a><a id="conf-gc-reserved-space"></a>`gc-reserved-space` 
 Amount of reserved disk space for the garbage collector. 
 **Default:** `8388608`
- <a id="conf-hashed-mirrors"></a><a id="conf-hashed-mirrors"></a>`hashed-mirrors` 
 A list of web servers used by `builtins.fetchurl` to obtain files by
hash. Given a hash algorithm *ha* and a base-16 hash *h*, Nix tries to
download the file from *hashed-mirror*/*ha*/*h*. This allows files to
be downloaded even if they have disappeared from their original URI.
For example, given an example mirror `http://tarballs.nixos.org/`,
when building the derivation 
```
builtins.fetchurl {
 url = "https://example.org/foo-1.2.3.tar.xz";
 sha256 = "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae";
}
```
 Nix will attempt to download this file from
`http://tarballs.nixos.org/sha256/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae`
first. If it is not available there, it tries the original URI. 
 **Default:** *empty*
- <a id="conf-http-connections"></a><a id="conf-http-connections"></a>`http-connections` 
 The maximum number of parallel TCP connections used to fetch
files from binary caches and by other downloads. It defaults
to 25. 0 means no limit. 
 **Default:** `25` 
 **Deprecated alias:** `binary-caches-parallel-connections`
- <a id="conf-http2"></a><a id="conf-http2"></a>`http2` 
 Whether to enable HTTP/2 support. 
 **Default:** `true`
- <a id="conf-id-count"></a><a id="conf-id-count"></a>`id-count` 
 The number of UIDs/GIDs to use for dynamic ID allocation. 
 **Default:** `8388608`
- <a id="conf-ignore-try"></a><a id="conf-ignore-try"></a>`ignore-try` 
 If set to true, ignore exceptions inside 'tryEval' calls when evaluating Nix expressions in
debug mode (using the --debugger flag). By default the debugger pauses on all exceptions. 
 **Default:** `false`
- <a id="conf-ignored-acls"></a><a id="conf-ignored-acls"></a>`ignored-acls` 
 A list of ACLs that should be ignored, normally Nix attempts to
remove all ACLs from files and directories in the Nix store, but
some ACLs like `security.selinux` or `system.nfs4_acl` can't be
removed even by root. Therefore it's best to just ignore them. 
 **Default:** `security.csm security.selinux system.nfs4_acl`
- <a id="conf-impersonate-linux-26"></a><a id="conf-impersonate-linux-26"></a>`impersonate-linux-26` 
 Whether to impersonate a Linux 2.6 machine on newer kernels. 
 **Default:** `false` 
 **Deprecated alias:** `build-impersonate-linux-26`
- <a id="conf-impure-env"></a><a id="conf-impure-env"></a>`impure-env` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`configurable-impure-env` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-configurable-impure-env)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = configurable-impure-env
> impure-env = ...
> ```
 A list of items, each in the format of: 
 
 If the user is trusted (see `trusted-users` option), when building
a fixed-output derivation, environment variables set in this option
is passed to the builder if they are listed in [`impureEnvVars`](/pages/nix-manual/language/advanced-attributes#adv-attr-impureEnvVars). 
 This option is useful for, e.g., setting `https_proxy` for
fixed-output derivations and in a multi-user Nix installation, or
setting private access tokens when fetching a private repository. 
 **Default:** *empty*
  - `name=value` : Set environment variable `name` to `value` .
- <a id="conf-json-log-path"></a><a id="conf-json-log-path"></a>`json-log-path` 
 A file or unix socket to which JSON records of Nix's log output are
written, in the same format as `--log-format internal-json`
(without the `@nix ` prefixes on each line).
Concurrent writes to the same file by multiple Nix processes are not supported and
may result in interleaved or corrupted log records. 
 **Default:** ``
- <a id="conf-keep-build-log"></a><a id="conf-keep-build-log"></a>`keep-build-log` 
 If set to `true` (the default), Nix writes the build log of a
derivation (i.e. the standard output and error of its builder) to
the directory `/nix/var/log/nix/drvs`. The build log can be
retrieved using the command `nix-store -l path`. 
 **Default:** `true` 
 **Deprecated alias:** `build-keep-log`
- <a id="conf-keep-derivations"></a><a id="conf-keep-derivations"></a>`keep-derivations` 
 If `true` (default), the garbage collector keeps the derivations
from which non-garbage store paths were built. If `false`, they are
deleted unless explicitly registered as a root (or reachable from
other roots). 
 Keeping derivation around is useful for querying and traceability
(e.g., it allows you to ask with what dependencies or options a
store path was built), so by default this option is on. Turn it off
to save a bit of disk space (or a lot if `keep-outputs` is also
turned on). 
 **Default:** `true` 
 **Deprecated alias:** `gc-keep-derivations`
- <a id="conf-keep-env-derivations"></a><a id="conf-keep-env-derivations"></a>`keep-env-derivations` 
 If `false` (default), derivations are not stored in Nix user
environments. That is, the derivations of any build-time-only
dependencies may be garbage-collected. 
 If `true`, when you add a Nix derivation to a user environment, the
path of the derivation is stored in the user environment. Thus, the
derivation isn't garbage-collected until the user environment
generation is deleted (`nix-env --delete-generations`). To prevent
build-time-only dependencies from being collected, you should also
turn on `keep-outputs`. 
 The difference between this option and `keep-derivations` is that
this one is "sticky": it applies to any user environment created
while this option was enabled, while `keep-derivations` only applies
at the moment the garbage collector is run. 
 **Default:** `false` 
 **Deprecated alias:** `env-keep-derivations`
- <a id="conf-keep-failed"></a><a id="conf-keep-failed"></a>`keep-failed` 
 Whether to keep temporary directories of failed builds. 
 **Default:** `false`
- <a id="conf-keep-going"></a><a id="conf-keep-going"></a>`keep-going` 
 Whether to keep building derivations when another build fails. 
 **Default:** `false`
- <a id="conf-keep-outputs"></a><a id="conf-keep-outputs"></a>`keep-outputs` 
 If `true`, the garbage collector keeps the outputs of
non-garbage derivations. If `false` (default), outputs are
deleted unless they are GC roots themselves (or reachable from other
roots). 
 In general, outputs must be registered as roots separately. However,
even if the output of a derivation is registered as a root, the
collector still deletes store paths that are used only at build
time (e.g., the C compiler, or source tarballs downloaded from the
network). To prevent it from doing so, set this option to `true`. 
 **Default:** `false` 
 **Deprecated alias:** `gc-keep-outputs`
- <a id="conf-lint-absolute-path-literals"></a><a id="conf-lint-absolute-path-literals"></a>`lint-absolute-path-literals` 
 Controls handling of absolute path literals (paths starting with `/`) and home path literals (paths starting with `~/`). 
 
 It is true that some files are more difficult to reference with relative paths,
because they would require lots of `../../..` upward traversing to reach them.
But firstly, it is probably not a good idea to reference these files ---
such paths often make Nix expressions less portable and reproducible,
as they depend on the file system layout of the machine evaluating the expression. 
 Secondly, with pure evaluation mode, most such files are prohibited to access anyway,
whether by absolute or relative paths.
In that case, enabling this lint in fatal mode is less disruptive,
because the paths pure eval allows are usually not the ones that would be ergonomically expressed with absolute paths anyway. 
 **Default:** `ignore`
  - `ignore` : Ignore without warning (default)
  - `warn` : Emit a warning about non-portability
  - `fatal` : Treat as a parse error
- <a id="conf-lint-short-path-literals"></a><a id="conf-lint-short-path-literals"></a>`lint-short-path-literals` 
 Controls handling of relative path literals that don't start with `./` or `../`. 
 
 For example, with this setting set to `warn` or `fatal`, `foo/bar` would
suggest using `./foo/bar` instead. 
 This is useful for improving code readability and making path literals
more explicit. 
 **Default:** `ignore`
  - `ignore` : Ignore without warning (default)
  - `warn` : Emit a warning suggesting to use `./` prefix
  - `fatal` : Treat as a parse error
- <a id="conf-lint-url-literals"></a><a id="conf-lint-url-literals"></a>`lint-url-literals` 
 Controls handling of unquoted URLs as part of the Nix language syntax.
The Nix language allows for URL literals, like so: 
```
$ nix repl
nix-repl> http://foo
"http://foo"
```
 Setting this to `warn` or `fatal` will cause the Nix parser to
warn or throw an error when encountering a URL literal: 
```
$ nix repl --lint-url-literals fatal
nix-repl> http://foo
error: URL literal 'http://foo' is deprecated
 at «string»:1:1:

 1| http://foo
 | ^
```
 Unquoted URLs are being deprecated and their usage is discouraged. 
 The reason is that, as opposed to path literals, URLs have no
special properties that distinguish them from regular strings, URLs
containing query parameters have to be quoted anyway, and unquoted URLs
may confuse external tooling. 
 **Default:** `ignore`
- <a id="conf-log-lines"></a><a id="conf-log-lines"></a>`log-lines` 
 The number of lines of the tail of the log to show if a build fails. 
 **Default:** `25`
- <a id="conf-max-build-log-size"></a><a id="conf-max-build-log-size"></a>`max-build-log-size` 
 This option defines the maximum number of bytes that a builder can
write to its stdout/stderr. If the builder exceeds this limit, it's
killed. A value of `0` (the default) means that there is no limit. 
 **Default:** `0` 
 **Deprecated alias:** `build-max-log-size`
- <a id="conf-max-call-depth"></a><a id="conf-max-call-depth"></a>`max-call-depth` 
 The maximum function call depth to allow before erroring. 
 **Default:** `10000`
- <a id="conf-max-free"></a><a id="conf-max-free"></a>`max-free` 
 When a garbage collection is triggered by the `min-free` option, it
stops as soon as `max-free` bytes are available. The default is
infinity (i.e. delete all garbage). 
 **Default:** `9223372036854775807`
- <a id="conf-max-jobs"></a><a id="conf-max-jobs"></a>`max-jobs` 
 Maximum number of jobs that Nix tries to build locally in parallel. 
 The special value `auto` causes Nix to use the number of CPUs in your system.
Use `0` to disable local builds and directly use the remote machines specified in `builders`.
This doesn't affect derivations that have [`preferLocalBuild = true`](/pages/nix-manual/language/advanced-attributes#adv-attr-preferLocalBuild), which are always built locally. 
 > **Note**
>
> The number of CPU cores to use for each build job is independently determined by the `cores` setting. 
 TODO(@fricklerhandwerk): would be good to have those shorthands for common options as part of the specification 
 The setting can be overridden using the `--max-jobs` (`-j`) command line switch. 
 **Default:** `1` 
 **Deprecated alias:** `build-max-jobs`
- <a id="conf-max-silent-time"></a><a id="conf-max-silent-time"></a>`max-silent-time` 
 This option defines the maximum number of seconds that a builder can
go without producing any data on standard output or standard error.
This is useful (for instance in an automated build system) to catch
builds that are stuck in an infinite loop, or to catch remote builds
that are hanging due to network problems. It can be overridden using
the `--max-silent-time` command line switch. 
 The value `0` means that there is no timeout. This is also the
default. 
 **Default:** `0` 
 **Deprecated alias:** `build-max-silent-time`
- <a id="conf-max-substitution-jobs"></a><a id="conf-max-substitution-jobs"></a>`max-substitution-jobs` 
 This option defines the maximum number of substitution jobs that Nix
tries to run in parallel. The default is `16`. The minimum value
one can choose is `1` and lower values are interpreted as `1`. 
 **Default:** `16` 
 **Deprecated alias:** `substitution-max-jobs`
- <a id="conf-min-free"></a><a id="conf-min-free"></a>`min-free` 
 When free disk space in `/nix/store` drops below `min-free` during a
build, Nix performs a garbage-collection until `max-free` bytes are
available or there is no more garbage. A value of `0` (the default)
disables this feature. 
 **Default:** `0`
- <a id="conf-min-free-check-interval"></a><a id="conf-min-free-check-interval"></a>`min-free-check-interval` 
 Number of seconds between checking free disk space. 
 **Default:** `5`
- <a id="conf-nar-buffer-size"></a><a id="conf-nar-buffer-size"></a>`nar-buffer-size` 
 Maximum size of NARs before spilling them to disk. 
 **Default:** `33554432`
- <a id="conf-narinfo-cache-meta-ttl"></a><a id="conf-narinfo-cache-meta-ttl"></a>`narinfo-cache-meta-ttl` 
 The TTL in seconds for caching binary cache metadata (i.e.
`/nix-cache-info`). This determines how long information about a
binary cache (such as its store directory, priority, and whether it
wants mass queries) is considered valid before being refreshed. 
 **Default:** `604800`
- <a id="conf-narinfo-cache-negative-ttl"></a><a id="conf-narinfo-cache-negative-ttl"></a>`narinfo-cache-negative-ttl` 
 The TTL in seconds for negative lookups.
If a store path is queried from a substituter but was not found, a negative lookup is cached in the local disk cache database for the specified duration. 
 Set to `0` to force updating the lookup cache. 
 To wipe the lookup cache completely: 
```
$ rm $HOME/.cache/nix/binary-cache-v*.sqlite*
# rm /root/.cache/nix/binary-cache-v*.sqlite*
```
 **Default:** `3600`
- <a id="conf-narinfo-cache-positive-ttl"></a><a id="conf-narinfo-cache-positive-ttl"></a>`narinfo-cache-positive-ttl` 
 The TTL in seconds for positive lookups. If a store path is queried
from a substituter, the result of the query is cached in the
local disk cache database including some of the NAR metadata. The
default TTL is a month, setting a shorter TTL for positive lookups
can be useful for binary caches that have frequent garbage
collection, in which case having a more frequent cache invalidation
would prevent trying to pull the path again and failing with a hash
mismatch if the build isn't reproducible. 
 **Default:** `2592000`
- <a id="conf-netrc-file"></a><a id="conf-netrc-file"></a>`netrc-file` 
 If set to an absolute path to a `netrc` file, Nix uses the HTTP
authentication credentials in this file when trying to download from
a remote host through HTTP or HTTPS. Defaults to
`$NIX_CONF_DIR/netrc`. 
 The `netrc` file consists of a list of accounts in the following
format: 
```
machine my-machine
login my-username
password my-password
```
 For the exact syntax, see [the `curl`
documentation](https://ec.haxx.se/usingcurl-netrc.html). 
 > **Note**
>
> This must be an absolute path, and `~` is not resolved. For
> example, `~/.netrc` won't resolve to your home directory's
> `.netrc`. 
 **Default:** `/dummy/netrc`
- <a id="conf-nix-path"></a><a id="conf-nix-path"></a>`nix-path` 
 List of search paths to use for [lookup path](/pages/nix-manual/language/constructs/lookup-path) resolution.
This setting determines the value of
[`builtins.nixPath`](/pages/nix-manual/language/builtins-prefix#builtins-nixPath) and can be used with [`builtins.findFile`](/pages/nix-manual/language/builtins-prefix#builtins-findFile). 
 
 If the respective paths are accessible, the default values are: 
 
 These files are set up by the [Nix installer](/pages/nix-manual/installation/installing-binary).
See [`NIX_STATE_DIR`](/pages/nix-manual/command-ref/env-common#env-NIX_STATE_DIR) for details on the environment variable. 
 > **Note**
>
> If [restricted evaluation](/pages/nix-manual/command-ref/conf-file-prefix#conf-restrict-eval) is enabled, the default value is empty.
>
> If pure evaluation is enabled, `builtins.nixPath` *always* evaluates to the empty list `[ ]`. 
 **Default:** *machine-specific*
  - The configuration setting is overridden by the [`NIX_PATH`](/pages/nix-manual/command-ref/env-common#env-NIX_PATH) 
environment variable.
  - `NIX_PATH` is overridden by [specifying the setting as the command line flag](/pages/nix-manual/command-ref/conf-file-prefix#command-line-flags) `--nix-path` .
  - Any current value is extended by the [`-I` option](/pages/nix-manual/command-ref/opt-common#opt-I) or `--extra-nix-path` .
  - `$HOME/.nix-defexpr/channels` 
 The [user channel link](/pages/nix-manual/command-ref/files/default-nix-expression#user-channel-link), pointing to the current state of [channels](/pages/nix-manual/command-ref/files/channels) for the current user.
  - `nixpkgs=$NIX_STATE_DIR/profiles/per-user/root/channels/nixpkgs` 
 The current state of the `nixpkgs` channel for the `root` user.
  - `$NIX_STATE_DIR/profiles/per-user/root/channels` 
 The current state of all channels for the `root` user.
- <a id="conf-nix-shell-always-looks-for-shell-nix"></a><a id="conf-nix-shell-always-looks-for-shell-nix"></a>`nix-shell-always-looks-for-shell-nix` 
 Before Nix 2.24, [`nix-shell`](/pages/nix-manual/command-ref/nix-shell) would only look at `shell.nix` if it was in the working directory - when no file was specified. 
 Since Nix 2.24, `nix-shell` always looks for a `shell.nix`, whether that's in the working directory, or in a directory that was passed as an argument. 
 You may set this to `false` to temporarily revert to the behavior of Nix 2.23 and older. 
 Using this setting is not recommended.
It will be deprecated and removed. 
 **Default:** `true`
- <a id="conf-nix-shell-shebang-arguments-relative-to-script"></a><a id="conf-nix-shell-shebang-arguments-relative-to-script"></a>`nix-shell-shebang-arguments-relative-to-script` 
 Before Nix 2.24, relative file path expressions in arguments in a `nix-shell` shebang were resolved relative to the working directory. 
 Since Nix 2.24, `nix-shell` resolves these paths in a manner that is relative to the [base directory](/pages/nix-manual/glossary#gloss-base-directory), defined as the script's directory. 
 You may set this to `false` to temporarily revert to the behavior of Nix 2.23 and older. 
 Using this setting is not recommended.
It will be deprecated and removed. 
 **Default:** `true`
- <a id="conf-plugin-files"></a><a id="conf-plugin-files"></a>`plugin-files` 
 A list of plugin files to be loaded by Nix. Each of these files is
dlopened by Nix. If they contain the symbol `nix_plugin_entry()`,
this symbol is called. Alternatively, they can affect execution
through static initialization. In particular, these plugins may construct
static instances of RegisterPrimOp to add new primops or constants to the
expression language, RegisterStoreImplementation to add new store
implementations, RegisterCommand to add new subcommands to the `nix`
command, and RegisterSetting to add new nix config settings. See the
constructors for those types for more details. 
 Warning! These APIs are inherently unstable and may change from
release to release. 
 Since these files are loaded into the same address space as Nix
itself, they must be DSOs compatible with the instance of Nix
running at the time (i.e. compiled against the same headers, not
linked to any incompatible libraries). They should not be linked to
any Nix libraries directly, as those are already available at load
time. 
 If an entry in the list is a directory, all files in the directory
are loaded as plugins (non-recursively). 
 **Default:** *empty*
- <a id="conf-post-build-hook"></a><a id="conf-post-build-hook"></a>`post-build-hook` 
 Optional. The path to a program to execute after each build. 
 This option is only settable in the global `nix.conf`, or on the
command line by trusted users. 
 When using the nix-daemon, the daemon executes the hook as `root`.
If the nix-daemon is not involved, the hook runs as the user
executing the nix-build. 
 
 The program executes with no arguments. The program's environment
contains the following environment variables: 
 
 **Default:** *empty*
  - The hook executes after an evaluation-time build.
  - The hook does not execute on substituted paths.
  - The hook's output always goes to the user's terminal.
  - If the hook fails, the build succeeds but no further builds
execute.
  - The hook executes synchronously, and blocks other builds from
progressing while it runs.
  - `DRV_PATH`
The derivation for the built paths. 
 Example:
`/nix/store/5nihn1a7pa8b25l9zafqaqibznlvvp3f-bash-4.4-p23.drv`
  - `OUT_PATHS`
Output paths of the built derivation, separated by a space
character. 
 Example:
`/nix/store/l88brggg9hpy96ijds34dlq4n8fan63g-bash-4.4-p23-dev /nix/store/vch71bhyi5akr5zs40k8h2wqxx69j80l-bash-4.4-p23-doc /nix/store/c5cxjywi66iwn9dcx5yvwjkvl559ay6p-bash-4.4-p23-info /nix/store/scz72lskj03ihkcn42ias5mlp4i4gr1k-bash-4.4-p23-man /nix/store/a724znygmd1cac856j3gfsyvih3lw07j-bash-4.4-p23`.
- <a id="conf-pre-build-hook"></a><a id="conf-pre-build-hook"></a>`pre-build-hook` 
 If set, the path to a program that can set extra derivation-specific
settings for this system. This is used for settings that can't be
captured by the derivation model itself and are too variable between
different versions of the same system to be hard-coded into nix. 
 The hook is passed the derivation path and, if sandboxes are
enabled, the sandbox directory. It can then modify the sandbox and
send a series of commands to modify various settings to stdout. The
currently recognized commands are: 
 
 **Default:** *empty*
  - `extra-sandbox-paths` 
 
Pass a list of files and directories to be included in the
sandbox for this build. One entry per line, terminated by an
empty line. Entries have the same format as `sandbox-paths` .
- <a id="conf-preallocate-contents"></a><a id="conf-preallocate-contents"></a>`preallocate-contents` 
 Whether to preallocate files when writing objects with known size. 
 **Default:** `false`
- <a id="conf-print-missing"></a><a id="conf-print-missing"></a>`print-missing` 
 Whether to print what paths need to be built or downloaded. 
 **Default:** `true`
- <a id="conf-pure-eval"></a><a id="conf-pure-eval"></a>`pure-eval` 
 Pure evaluation mode ensures that the result of Nix expressions is fully determined by explicitly declared inputs, and not influenced by external state: 
 
 **Default:** `false`
  - Restrict file system and network access to files specified by cryptographic hash
  - Disable impure constants:
    - [`builtins.currentSystem`](/pages/nix-manual/language/builtins-prefix#builtins-currentSystem)
    - [`builtins.currentTime`](/pages/nix-manual/language/builtins-prefix#builtins-currentTime)
    - [`builtins.nixPath`](/pages/nix-manual/language/builtins-prefix#builtins-nixPath)
    - [`builtins.storePath`](/pages/nix-manual/language/builtins-prefix#builtins-storePath)
- <a id="conf-require-drop-supplementary-groups"></a><a id="conf-require-drop-supplementary-groups"></a>`require-drop-supplementary-groups` 
 Following the principle of least privilege,
Nix attempts to drop supplementary groups when building with sandboxing. 
 However this can fail under some circumstances.
For example, if the user lacks the `CAP_SETGID` capability.
Search `setgroups(2)` for `EPERM` to find more detailed information on this. 
 If you encounter such a failure, setting this option to `false` enables you to ignore it and continue.
But before doing so, you should consider the security implications carefully.
Not dropping supplementary groups means the build sandbox is less restricted than intended. 
 This option defaults to `true` when the user is root
(since `root` usually has permissions to call setgroups)
and `false` otherwise. 
 **Default:** `false`
- <a id="conf-require-sigs"></a><a id="conf-require-sigs"></a>`require-sigs` 
 If set to `true` (the default), any non-content-addressed path added
or copied to the Nix store (e.g. when substituting from a binary
cache) must have a signature by a trusted key. A trusted key is one
listed in `trusted-public-keys`, or a public key counterpart to a
private key stored in a file listed in `secret-key-files`. 
 Set to `false` to disable signature checking and trust all
non-content-addressed paths unconditionally. 
 (Content-addressed paths are inherently trustworthy and thus
unaffected by this configuration option.) 
 **Default:** `true`
- <a id="conf-restrict-eval"></a><a id="conf-restrict-eval"></a>`restrict-eval` 
 If set to `true`, the Nix evaluator doesn't allow access to any
files outside of
[`builtins.nixPath`](/pages/nix-manual/language/builtins-prefix#builtins-nixPath),
or to URIs outside of
[`allowed-uris`](/pages/nix-manual/command-ref/conf-file-prefix#conf-allowed-uris). 
 **Default:** `false`
- <a id="conf-run-diff-hook"></a><a id="conf-run-diff-hook"></a>`run-diff-hook` 
 If true, enable the execution of the `diff-hook` program. 
 When using the Nix daemon, `run-diff-hook` must be set in the
`nix.conf` configuration file, and cannot be passed at the command
line. 
 **Default:** `false`
- <a id="conf-sandbox"></a><a id="conf-sandbox"></a>`sandbox` 
 If set to `true`, builds are performed in a *sandboxed
environment*, i.e., they're isolated from the normal file system
hierarchy and only see their dependencies in the Nix store,
the temporary build directory, private versions of `/proc`,
`/dev`, `/dev/shm` and `/dev/pts` (on Linux), and the paths
configured with the `sandbox-paths` option. This is useful to
prevent undeclared dependencies on files in directories such as
`/usr/bin`. In addition, on Linux, builds run in private PID,
mount, network, IPC and UTS namespaces to isolate them from other
processes in the system (except that fixed-output derivations do
not run in private network namespace to ensure they can access the
network). 
 Currently, sandboxing only work on Linux and macOS. The use of a
sandbox requires that Nix is run as root (so you should use the
"build users" feature to perform the actual builds under different
users than root). 
 If this option is set to `relaxed`, then fixed-output derivations
and derivations that have the `__noChroot` attribute set to `true`
do not run in sandboxes. 
 The default is `true` on Linux and `false` on all other platforms. 
 **Default:** `true` 
 **Deprecated alias:** `build-use-chroot`, `build-use-sandbox`
- <a id="conf-sandbox-build-dir"></a><a id="conf-sandbox-build-dir"></a>`sandbox-build-dir` 
 *Linux only* 
 The build directory inside the sandbox. 
 This directory is backed by `build-dir` on the host. 
 **Default:** `/build`
- <a id="conf-sandbox-dev-shm-size"></a><a id="conf-sandbox-dev-shm-size"></a>`sandbox-dev-shm-size` 
 *Linux only* 
 This option determines the maximum size of the `tmpfs` filesystem
mounted on `/dev/shm` in Linux sandboxes. For the format, see the
description of the `size` option of `tmpfs` in mount(8). The default
is `50%`. 
 **Default:** `50%`
- <a id="conf-sandbox-fallback"></a><a id="conf-sandbox-fallback"></a>`sandbox-fallback` 
 Whether to disable sandboxing when the kernel doesn't allow it. 
 **Default:** `true`
- <a id="conf-sandbox-paths"></a><a id="conf-sandbox-paths"></a>`sandbox-paths` 
 A list of paths bind-mounted into Nix sandbox environments. You can
use the syntax `target=source` to mount a path in a different
location in the sandbox; for instance, `/bin=/nix-bin` mounts
the path `/nix-bin` as `/bin` inside the sandbox. If *source* is
followed by `?`, then it is not an error if *source* does not exist;
for example, `/dev/nvidiactl?` specifies that `/dev/nvidiactl`
only be mounted in the sandbox if it exists in the host filesystem. 
 If the source is in the Nix store, then its closure is added to
the sandbox as well. 
 Depending on how Nix was built, the default value for this option
may be empty or provide `/bin/sh` as a bind-mount of `bash`. 
 **Default:** *empty* 
 **Deprecated alias:** `build-chroot-dirs`, `build-sandbox-paths`
- <a id="conf-secret-key-files"></a><a id="conf-secret-key-files"></a>`secret-key-files` 
 A whitespace-separated list of files containing secret (private)
keys. These are used to sign locally-built paths. They can be
generated using `nix-store --generate-binary-cache-key`. The
corresponding public key can be distributed to other users, who
can add it to `trusted-public-keys` in their `nix.conf`. 
 **Default:** *empty*
- <a id="conf-show-trace"></a><a id="conf-show-trace"></a>`show-trace` 
 Whether Nix should print out a stack trace in case of Nix
expression evaluation errors. 
 **Default:** `false`
- <a id="conf-ssl-cert-file"></a><a id="conf-ssl-cert-file"></a>`ssl-cert-file` 
 The path of a file containing CA certificates used to
authenticate `https://` downloads. Nix by default uses
the first of the following files that exists: 
 
 The path can be overridden by the following environment
variables, in order of precedence: 
 
 **Default:** *machine-specific*
  1. `/etc/ssl/certs/ca-certificates.crt`
  2. `/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt`
  1. `NIX_SSL_CERT_FILE`
  2. `SSL_CERT_FILE`
- <a id="conf-stalled-download-timeout"></a><a id="conf-stalled-download-timeout"></a>`stalled-download-timeout` 
 The timeout (in seconds) for receiving data from servers
during download. Nix cancels idle downloads after this
timeout's duration. 
 **Default:** `300`
- <a id="conf-start-id"></a><a id="conf-start-id"></a>`start-id` 
 The first UID and GID to use for dynamic ID allocation. 
 **Default:** `872415232`
- <a id="conf-store"></a><a id="conf-store"></a>`store` 
 The [URL of the Nix store](/pages/nix-manual/store/types#store-url-format)
to use for most operations.
See the
[Store Types](/pages/nix-manual/store/types)
section of the manual for supported store types and settings. 
 **Default:** `auto`
- <a id="conf-substitute"></a><a id="conf-substitute"></a>`substitute` 
 If set to `true` (default), Nix uses binary substitutes if
available. This option can be disabled to force building from
source. 
 **Default:** `true` 
 **Deprecated alias:** `build-use-substitutes`
- <a id="conf-substituters"></a><a id="conf-substituters"></a>`substituters` 
 A list of [URLs of Nix stores](/pages/nix-manual/store/types#store-url-format) to be used as substituters, separated by whitespace.
A substituter is an additional [store](/pages/nix-manual/glossary#gloss-store) from which Nix can obtain [store objects](/pages/nix-manual/store/store-object) instead of building them. 
 Substituters are tried based on their priority value, which each substituter can set independently.
Lower value means higher priority.
The default is `https://cache.nixos.org`, which has a priority of 40. 
 At least one of the following conditions must be met for Nix to use a substituter: 
 
 In addition, each store path should be trusted as described in `trusted-public-keys` 
 **Default:** `https://cache.nixos.org/` 
 **Deprecated alias:** `binary-caches`
  - The substituter is in the `trusted-substituters` list
  - The user calling Nix is in the `trusted-users` list
- <a id="conf-sync-before-registering"></a><a id="conf-sync-before-registering"></a>`sync-before-registering` 
 Whether to call `sync()` before registering a path as valid. 
 **Default:** `false`
- <a id="conf-system"></a><a id="conf-system"></a>`system` 
 The system type of the current Nix installation.
Nix only builds a given [store derivation](/pages/nix-manual/glossary#gloss-store-derivation) locally when its `system` attribute equals any of the values specified here or in `extra-platforms`. 
 The default value is set when Nix itself is compiled for the system it will run on.
The following system types are widely used, as Nix is actively supported on these platforms: 
 
 In general, you do not have to modify this setting.
While you can force Nix to run a Darwin-specific `builder` executable on a Linux machine, the result would obviously be wrong. 
 This value is available in the Nix language as
[`builtins.currentSystem`](/pages/nix-manual/language/builtins-prefix#builtins-currentSystem)
if the
`eval-system`
configuration option is set as the empty string. 
 **Default:** `x86_64-linux`
  - `x86_64-linux`
  - `x86_64-darwin`
  - `i686-linux`
  - `aarch64-linux`
  - `aarch64-darwin`
  - `armv6l-linux`
  - `armv7l-linux`
- <a id="conf-system-features"></a><a id="conf-system-features"></a>`system-features` 
 A set of system “features” supported by this machine. 
 This complements the `system` and `extra-platforms` configuration options and the corresponding [`system`](/pages/nix-manual/language/derivations#attr-system) attribute on derivations. 
 A derivation can require system features in the [`requiredSystemFeatures` attribute](/pages/nix-manual/language/advanced-attributes#adv-attr-requiredSystemFeatures), and the machine to build the derivation must have them. 
 System features are user-defined, but Nix sets the following defaults: 
 
 **Default:** *machine-specific*
  - `apple-virt` 
 Included on Darwin if virtualization is available.
  - `kvm` 
 Included on Linux if `/dev/kvm` is accessible.
  - `nixos-test`, `benchmark`, `big-parallel` 
 These historical pseudo-features are always enabled for backwards compatibility, as they are used in Nixpkgs to route Hydra builds to specific machines.
  - `ca-derivations` 
 Included by default if the [`ca-derivations` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-ca-derivations) is enabled. 
 This system feature is implicitly required by derivations with the [`__contentAddressed` attribute](/pages/nix-manual/language/advanced-attributes#adv-attr-__contentAddressed).
  - `recursive-nix` 
 Included by default if the [`recursive-nix` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-recursive-nix) is enabled.
  - `uid-range` 
 On Linux, Nix can run builds in a user namespace where they run as root (UID 0) and have 65,536 UIDs available.
This is primarily useful for running containers such as `systemd-nspawn` inside a Nix build. For an example, see [`tests/systemd-nspawn/nix`](https://github.com/NixOS/nix/blob/67bcb99700a0da1395fa063d7c6586740b304598/tests/systemd-nspawn.nix). 
 Included by default on Linux if the `auto-allocate-uids` setting is enabled.
- <a id="conf-tarball-ttl"></a><a id="conf-tarball-ttl"></a>`tarball-ttl` 
 The number of seconds a downloaded tarball is considered fresh. If
the cached tarball is stale, Nix checks whether it is still up
to date using the ETag header. Nix downloads a new version if
the ETag header is unsupported, or the cached ETag doesn't match. 
 Setting the TTL to `0` forces Nix to always check if the tarball is
up to date. 
 Nix caches tarballs in `$XDG_CACHE_HOME/nix/tarballs`. 
 Files fetched via `NIX_PATH`, `fetchGit`, `fetchMercurial`,
`fetchTarball`, and `fetchurl` respect this TTL. 
 **Default:** `3600`
- <a id="conf-timeout"></a><a id="conf-timeout"></a>`timeout` 
 This option defines the maximum number of seconds that a builder can
run. This is useful (for instance in an automated build system) to
catch builds that are stuck in an infinite loop but keep writing to
their standard output or standard error. It can be overridden using
the `--timeout` command line switch. 
 The value `0` means that there is no timeout. This is also the
default. 
 **Default:** `0` 
 **Deprecated alias:** `build-timeout`
- <a id="conf-trace-function-calls"></a><a id="conf-trace-function-calls"></a>`trace-function-calls` 
 If set to `true`, the Nix evaluator traces every function call.
Nix prints a log message at the "vomit" level for every function
entrance and function exit. 
```
function-trace entered undefined position at 1565795816999559622
function-trace exited undefined position at 1565795816999581277
function-trace entered /nix/store/.../example.nix:226:41 at 1565795253249935150
function-trace exited /nix/store/.../example.nix:226:41 at 1565795253249941684
```
 The `undefined position` means the function call is a builtin. 
 Use the `contrib/stack-collapse.py` script distributed with the Nix
source code to convert the trace logs in to a format suitable for
`flamegraph.pl`. 
 **Default:** `false`
- <a id="conf-trace-import-from-derivation"></a><a id="conf-trace-import-from-derivation"></a>`trace-import-from-derivation` 
 By default, Nix allows [Import from Derivation](/pages/nix-manual/language/import-from-derivation). 
 When this setting is `true`, Nix logs a warning indicating that it performed such an import.
This option has no effect if `allow-import-from-derivation` is disabled. 
 **Default:** `false`
- <a id="conf-trace-verbose"></a><a id="conf-trace-verbose"></a>`trace-verbose` 
 Whether `builtins.traceVerbose` should trace its first argument when evaluated. 
 **Default:** `false`
- <a id="conf-trust-tarballs-from-git-forges"></a><a id="conf-trust-tarballs-from-git-forges"></a>`trust-tarballs-from-git-forges` 
 If enabled (the default), Nix considers tarballs from
GitHub and similar Git forges to be locked if a Git revision
is specified,
e.g. `github:NixOS/patchelf/7c2f768bf9601268a4e71c2ebe91e2011918a70f`.
This requires Nix to trust that the provider returns the
correct contents for the specified Git revision. 
 If disabled, such tarballs are only considered locked if a
`narHash` attribute is specified,
e.g. `github:NixOS/patchelf/7c2f768bf9601268a4e71c2ebe91e2011918a70f?narHash=sha256-PPXqKY2hJng4DBVE0I4xshv/vGLUskL7jl53roB8UdU%3D`. 
 **Default:** `true`
- <a id="conf-trusted-public-keys"></a><a id="conf-trusted-public-keys"></a>`trusted-public-keys` 
 A whitespace-separated list of public keys. 
 At least one of the following condition must be met
for Nix to accept copying a store object from another
Nix store (such as a substituter): 
 
 **Default:** `cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=` 
 **Deprecated alias:** `binary-cache-public-keys`
  - the store object has been signed using a key in the trusted keys list
  - the `require-sigs` option has been set to `false`
  - the store URL is configured with `trusted=true`
  - the store object is [content-addressed](/pages/nix-manual/glossary#gloss-content-addressed-store-object)
- <a id="conf-trusted-substituters"></a><a id="conf-trusted-substituters"></a>`trusted-substituters` 
 A list of [Nix store URLs](/pages/nix-manual/store/types#store-url-format), separated by whitespace.
These are not used by default, but users of the Nix daemon can enable them by specifying `substituters`. 
 Unprivileged users (those set in only `allowed-users` but not `trusted-users`) can pass as `substituters` only those URLs listed in `trusted-substituters`. 
 **Default:** *empty* 
 **Deprecated alias:** `trusted-binary-caches`
- <a id="conf-trusted-users"></a><a id="conf-trusted-users"></a>`trusted-users` 
 A list of user names, separated by whitespace.
These users will have additional rights when connecting to the Nix daemon, such as the ability to specify additional substituters, or to import unsigned realisations or unsigned input-addressed store objects. 
 You can also specify groups by prefixing names with `@`.
For instance, `@wheel` means all users in the `wheel` group. 
 > **Warning**
>
> Adding a user to `trusted-users` is essentially equivalent to giving that user root access to the system.
> For example, the user can access or replace store path contents that are critical for system security. 
 **Default:** `root`
- <a id="conf-upgrade-nix-store-path-url"></a><a id="conf-upgrade-nix-store-path-url"></a>`upgrade-nix-store-path-url` 
 Used by `nix upgrade-nix`, the URL of the file that contains the
store paths of the latest Nix release. 
 **Default:** `https://github.com/NixOS/nixpkgs/raw/master/nixos/modules/installer/tools/nix-fallback-paths.nix`
- <a id="conf-use-case-hack"></a><a id="conf-use-case-hack"></a>`use-case-hack` 
 Whether to enable a macOS-specific hack for dealing with file name case collisions. 
 **Default:** `false`
- <a id="conf-use-cgroups"></a><a id="conf-use-cgroups"></a>`use-cgroups` 
 Whether to execute builds inside cgroups.
This is only supported on Linux. 
 Cgroups are required and enabled automatically for derivations
that require the `uid-range` system feature. 
 **Default:** `false`
- <a id="conf-use-registries"></a><a id="conf-use-registries"></a>`use-registries` 
 > **Warning**
>
> This setting is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To change this setting, make sure the
> [`flakes` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-flakes)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = flakes
> use-registries = ...
> ```
 Whether to use flake registries to resolve flake references. 
 **Default:** `true`
- <a id="conf-use-sqlite-wal"></a><a id="conf-use-sqlite-wal"></a>`use-sqlite-wal` 
 Whether SQLite should use WAL mode. 
 **Default:** `true`
- <a id="conf-use-xdg-base-directories"></a><a id="conf-use-xdg-base-directories"></a>`use-xdg-base-directories` 
 If set to `true`, Nix conforms to the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) for files in `$HOME`.
The environment variables used to implement this are documented in the [Environment Variables section](/pages/nix-manual/command-ref/env-common). 
 > **Warning**
> This changes the location of some well-known symlinks that Nix creates, which might break tools that rely on the old, non-XDG-conformant locations. 
 In particular, the following locations change: 
 | Old | New |
| --- | --- |
| `~/.nix-profile` | `$XDG_STATE_HOME/nix/profile` |
| `~/.nix-defexpr` | `$XDG_STATE_HOME/nix/defexpr` |
| `~/.nix-channels` | `$XDG_STATE_HOME/nix/channels` | 
 If you already have Nix installed and are using [profiles](/pages/nix-manual/package-management/profiles) or [channels](/pages/nix-manual/command-ref/nix-channel), you should migrate manually when you enable this option.
If `$XDG_STATE_HOME` is not set, use `$HOME/.local/state/nix` instead of `$XDG_STATE_HOME/nix`.
This can be achieved with the following shell commands: 
```
nix_state_home=${XDG_STATE_HOME-$HOME/.local/state}/nix
mkdir -p $nix_state_home
mv $HOME/.nix-profile $nix_state_home/profile
mv $HOME/.nix-defexpr $nix_state_home/defexpr
mv $HOME/.nix-channels $nix_state_home/channels
```
 **Default:** `false`
- <a id="conf-user-agent-suffix"></a><a id="conf-user-agent-suffix"></a>`user-agent-suffix` 
 String appended to the user agent in HTTP requests. 
 **Default:** *empty*
- <a id="conf-warn-dirty"></a><a id="conf-warn-dirty"></a>`warn-dirty` 
 Whether to warn about dirty Git/Mercurial trees. 
 **Default:** `true`
- <a id="conf-warn-large-path-threshold"></a><a id="conf-warn-large-path-threshold"></a>`warn-large-path-threshold` 
 Warn when copying a path larger than this number of bytes to the Nix store
(as determined by its NAR serialisation).
Default is 0, which disables the warning.
Set it to 1 to warn on all paths. 
 **Default:** `0`
- <a id="conf-warn-short-path-literals"></a><a id="conf-warn-short-path-literals"></a>`warn-short-path-literals` 
 Deprecated. Use `lint-short-path-literals`` = warn` instead. 
 **Default:** `false`
