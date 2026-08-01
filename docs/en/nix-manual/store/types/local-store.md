# Local Store - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/store/types/local-store.html](@docroot@/store/types/local-store.md)

# <a id="local-store"></a> Local Store

**Store URL format**: `local`, *root*

This store type accesses a Nix store in the local filesystem directly
(i.e. not via the Nix daemon). *root* is an absolute path that is
prefixed to other directories such as the Nix store directory. The
store pseudo-URL `local` denotes a store that uses `/` as its root
directory.

A store that uses a *root* other than `/` is called a *chroot
store*. With such stores, the store directory is "logically" still
`/nix/store`, so programs stored in them can only be built and
executed by `chroot`-ing into *root*. Chroot stores only support
building and running on Linux when [`mount namespaces`](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html) and [`user namespaces`](https://man7.org/linux/man-pages/man7/user_namespaces.7.html) are
enabled.

For example, the following uses `/tmp/root` as the chroot environment
to build or download `nixpkgs#hello` and then execute it:

```
# nix run --store /tmp/root nixpkgs#hello
Hello, world!
```

Here, the "physical" store location is `/tmp/root/nix/store`, and
Nix's store metadata is in `/tmp/root/nix/var/nix/db`.

It is also possible, but not recommended, to change the "logical"
location of the Nix store from its default of `/nix/store`. This makes
it impossible to use default substituters such as
`https://cache.nixos.org/`, and thus you may have to build everything
locally. Here is an example:

```
# nix build --store 'local?store=/tmp/my-nix/store&state=/tmp/my-nix/state&log=/tmp/my-nix/log' nixpkgs#hello
```

## <a id="settings"></a> Settings

- `build-dir`
The directory on the host, in which derivations' temporary build directories are created.
If not set, Nix will use the `builds` subdirectory of its configured state directory.
Note that builds are often performed by the Nix daemon, so its `build-dir` applies.
Nix will create this directory automatically with suitable permissions if it does not exist.
Otherwise its permissions must allow all users to traverse the directory (i.e. it must have `o+x` set, in unix parlance) for non-sandboxed builds to work correctly.
This is also the location where [`--keep-failed`](https://nix.dev/manual/nix/2.34/command-ref/opt-common#opt-keep-failed) leaves its files.
If Nix runs without sandbox, or if the platform does not support sandboxing with bind mounts (e.g. macOS), then the [`builder`](https://nix.dev/manual/nix/2.34/language/derivations#attr-builder)'s environment will contain this directory, instead of the virtual location [`sandbox-build-dir`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-sandbox-build-dir).

**Warning**
`build-dir` must not be set to a world-writable directory.
Placing temporary build directories in a world-writable place allows other users to access or modify build data that is currently in use.
This alone is merely an impurity, but combined with another factor this has allowed malicious derivations to escape the build sandbox.

See also the global [`build-dir`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-build-dir) setting.
**Default:** ``
- `ignore-gc-delete-failure`

**Warning**
This setting is part of an
[experimental feature](https://nix.dev/manual/nix/2.34/development/experimental-features).
To change this setting, make sure the
[`local-overlay-store` experimental feature](https://nix.dev/manual/nix/2.34/development/experimental-features#xp-feature-local-overlay-store)
is enabled.
For example, include the following in [`nix.conf`](https://nix.dev/manual/nix/2.34/command-ref/conf-file):
extra-experimental-features = local-overlay-store
ignore-gc-delete-failure = ...

Whether to ignore failures when deleting items with the garbage collector.
Normally the garbage collector will fail with an error if the nix daemon cannot delete a file, with this setting such errors will only be printed as warnings.
**Default:** `false`
- `log`
directory where Nix stores log files.
**Default:** `/nix/var/log/nix`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `read-only`
Allow this store to be opened when its [database](https://nix.dev/manual/nix/2.34/glossary#gloss-nix-database) is on a read-only filesystem.
Normally Nix attempts to open the store database in read-write mode, even for querying (when write access is not needed), causing it to fail if the database is on a read-only filesystem.
Enable read-only mode to disable locking and open the SQLite database with the [`immutable` parameter](https://www.sqlite.org/c3ref/open.html) set.

**Warning**
Do not use this unless the filesystem is read-only.
Using it when the filesystem is writable can cause incorrect query results or corruption errors if the database is changed by another process.
While the filesystem the database resides on might appear to be read-only, consider whether another user or system might have write access to it.

**Default:** `false`
- `real`
Physical path of the Nix store.
**Default:** `/nix/store`
- `require-sigs`
Whether store paths copied into this store should have a trusted signature.
**Default:** `true`
- `root`
Directory prefixed to all other paths.
**Default:** ``
- `state`
Directory where Nix stores state.
**Default:** `/dummy`
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-trusted-public-keys)
setting.
**Default:** `false`
- `use-roots-daemon`

**Warning**
This setting is part of an
[experimental feature](https://nix.dev/manual/nix/2.34/development/experimental-features).
To change this setting, make sure the
[`local-overlay-store` experimental feature](https://nix.dev/manual/nix/2.34/development/experimental-features#xp-feature-local-overlay-store)
is enabled.
For example, include the following in [`nix.conf`](https://nix.dev/manual/nix/2.34/command-ref/conf-file):
extra-experimental-features = local-overlay-store
use-roots-daemon = ...

Whether to request garbage collector roots from an external daemon.
When enabled, the garbage collector connects to a Unix domain socket
at [`<state-dir>`](https://nix.dev/manual/nix/2.34/store/types/local-store#store-option-state)`/gc-roots-socket/socket` to discover additional roots
that should not be collected. This is useful when the Nix daemon runs
without root privileges and cannot scan `/proc` for runtime roots.
The daemon can be started with [`nix store roots-daemon`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-store-roots-daemon).
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-substituters).
**Default:** `false`
