# nix help-stores - Nix 2.34.9 Reference Manual

> Source: [/pages/nix-manual/command-ref/new-cli/nix3-help-stores](/pages/nix-manual/command-ref/new-cli/nix3-help-stores)

> **Warning** 
>
> This program is
> [**experimental**](/pages/nix-manual/development/experimental-features#xp-feature-nix-command)
> and its interface is subject to change.

# <a id="name"></a> Name

`nix help-stores` - show help about store types and their settings

# <a id="synopsis"></a> Synopsis

`nix help-stores` [*option*...]

Nix supports different types of stores:

- Dummy Store
- Experimental Local Overlay Store
- Experimental SSH Store
- Experimental SSH Store with filesystem mounted
- HTTP Binary Cache Store
- Local Binary Cache Store
- Local Daemon Store
- Local Store
- S3 Binary Cache Store
- SSH Store

## <a id="store-url-format"></a> Store URL format

Stores are specified using a URL-like syntax. For example, the command

```
# nix path-info --store https://cache.nixos.org/ --json \
  /nix/store/1542dip9i7k4f24y6hqgd04hmvid9hr5-coreutils-9.1
```

fetches information about a store path in the HTTP binary cache
located at https://cache.nixos.org/, which is a type of store.

Store URLs can specify **store settings** using URL query strings,
i.e. by appending `?name1=value1&name2=value2&...` to the URL. For
instance,

```
--store ssh://machine.example.org?ssh-key=/path/to/my/key
```

tells Nix to access the store on a remote machine via the SSH
protocol, using `/path/to/my/key` as the SSH private key. The
supported settings for each store type are documented below.

The special store URL `auto` causes Nix to automatically select a
store as follows:

- Use the local store `/nix/store` if `/nix/var/nix`
is writable by the current user.
- Otherwise, if `/nix/var/nix/daemon-socket/socket` exists, connect
to the Nix daemon listening on that socket.
- Otherwise, on Linux only, use the local chroot store
`~/.local/share/nix/root`, which will be created automatically if it
does not exist.
- Otherwise, use the local store `/nix/store`.

# <a id="dummy-store"></a> Dummy Store

**Store URL format**: `dummy://`

This store type represents a store in memory.
Store objects can be read and written, but only so long as the store is open.
Once the store is closed, all data will be discarded.

It's useful when you want to use the Nix evaluator when no actual Nix store exists, e.g.

```
# nix eval --store dummy:// --expr '1 + 2'
```

## <a id="settings"></a> Settings

- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `read-only`
Make any sort of write fail instead of succeeding.
No additional memory will be used, because no information needs to be stored.
**Default:** `true`
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

# <a id="experimental-local-overlay-store"></a> Experimental Local Overlay Store

> **Warning**
>
> This store is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To use this store, make sure the
> [`local-overlay-store` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-local-overlay-store)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = local-overlay-store
> ```

**Store URL format**: `local-overlay`

This store type is a variation of the [local store] designed to leverage Linux's [Overlay Filesystem](https://docs.kernel.org/filesystems/overlayfs.html) (OverlayFS for short).
Just as OverlayFS combines a lower and upper filesystem by treating the upper one as a patch against the lower, the local overlay store combines a lower store with an upper almost-[local store].
("almost" because while the upper filesystems for OverlayFS is valid on its own, the upper almost-store is not a valid local store on its own because some references will dangle.)
To use this store, you will first need to configure an OverlayFS mountpoint appropriately as Nix will not do this for you (though it will verify the mountpoint is configured correctly).

### <a id="conceptual-parts-of-a-local-overlay-store"></a> Conceptual parts of a local overlay store

*This is a more abstract/conceptual description of the parts of a layered store, an authoritative reference.
For more "practical" instructions, see the worked-out example in the next subsection.*

The parts of a local overlay store are as follows:

- **Lower store**:

Specified with the `lower-store` setting.

This is any store implementation that includes a store directory as part of the native operating system filesystem.
For example, this could be a [local store], [local daemon store], or even another local overlay store.
The local overlay store never tries to modify the lower store in any way.
Something else could modify the lower store, but there are restrictions on this
Nix itself requires that this store only grow, and not change in other ways.
For example, new store objects can be added, but deleting or modifying store objects is not allowed in general, because that will confuse and corrupt any local overlay store using those objects.
(In addition, the underlying filesystem overlay mechanism may impose additional restrictions, see below.)
The lower store must not change while it is mounted as part of an overlay store.
To ensure it does not, you might want to mount the store directory read-only (which then requires the [read-only] parameter to be set to `true`).
  - **Lower store directory**:

Specified with `lower-store.real` setting.

This is the directory used/exposed by the lower store.
As specified above, Nix requires the local store can only grow not change in other ways.
Linux's OverlayFS in addition imposes the further requirement that this directory cannot change at all.
That means that, while any local overlay store exists that is using this store as a lower store, this directory must not change.
  - **Lower metadata source**:

Not directly specified.
A consequence of the `lower-store` setting, depending on the type of lower store chosen.

This is abstract, just some way to read the metadata of lower store [store objects](/pages/nix-manual/store/store-object).
For example it could be a SQLite database (for the [local store]), or a socket connection (for the [local daemon store]).
This need not be writable.
As stated above a local overlay store never tries to modify its lower store.
The lower store's metadata is considered part of the lower store, just as the store's [file system objects](/pages/nix-manual/store/file-system-object) that appear in the store directory are.
- **Upper almost-store**:

Not directly specified.
Instead the constituent parts are independently specified as described below.

This is almost but not quite just a [local store].
That is because taken in isolation, not as part of a local overlay store, by itself, it would appear corrupted.
But combined with everything else as part of an overlay local store, it is valid.
  - **Upper layer directory**:

Specified with `upper-layer` setting.

This contains additional [store objects](/pages/nix-manual/store/store-object)
(or, strictly speaking, their [file system objects](/pages/nix-manual/store/file-system-object) that the local overlay store will extend the lower store with).
  - **Upper store directory**:

Specified with the `real` setting.
This the same as the base local store setting, and can also be indirectly specified with the `root` setting.

This contains all the store objects from each of the two directories.
The lower store directory and upper layer directory are combined via OverlayFS to create this directory.
Nix doesn't do this itself, because it typically wouldn't have the permissions to do so, so it is the responsibility of the user to set this up first.
Nix can, however, optionally check that the OverlayFS mount settings appear as expected, matching Nix's own settings.
  - **Upper SQLite database**:

Not directly specified.
The location of the database instead depends on the `state` setting.
It is always `${'{'}'{'{'}'{'}'}state{'{'}'{'}'}'{'}'}/db`.

This contains the metadata of all of the upper layer [store objects](/pages/nix-manual/store/store-object) (everything beyond their file system objects), and also duplicate copies of some lower layer store object's metadata.
The duplication is so the metadata for the [closure](/pages/nix-manual/glossary#gloss-closure) of upper layer [store objects](/pages/nix-manual/store/store-object) can be found entirely within the upper layer.
(This allows us to use the same SQL Schema as the [local store]'s SQLite database, as foreign keys in that schema enforce closure metadata to be self-contained in this way.)

### <a id="example-filesystem-layout"></a> Example filesystem layout

Here is a worked out example of usage, following the concepts in the previous section.

Say we have the following paths:

- `/mnt/example/merged-store/nix/store`
- `/mnt/example/store-a/nix/store`
- `/mnt/example/store-b`

Then the following store URI can be used to access a local-overlay store at `/mnt/example/merged-store`:

```
local-overlay://?root=/mnt/example/merged-store&lower-store=/mnt/example/store-a&upper-layer=/mnt/example/store-b
```

The lower store directory is located at `/mnt/example/store-a/nix/store`, while the upper layer is at `/mnt/example/store-b`.

Before accessing the overlay store you will need to ensure the OverlayFS mount is set up correctly:

```
mount -t overlay overlay \
  -o lowerdir="/mnt/example/store-a/nix/store" \
  -o upperdir="/mnt/example/store-b" \
  -o workdir="/mnt/example/workdir" \
  "/mnt/example/merged-store/nix/store"
```

Note that OverlayFS requires `/mnt/example/workdir` to be on the same volume as the `upperdir`.

By default, Nix will check that the mountpoint as been set up correctly and fail with an error if it has not.
You can override this behaviour by passing `check-mount=false` if you need to.

## <a id="settings-1"></a> Settings

- `build-dir`
The directory on the host, in which derivations' temporary build directories are created.
If not set, Nix will use the `builds` subdirectory of its configured state directory.
Note that builds are often performed by the Nix daemon, so its `build-dir` applies.
Nix will create this directory automatically with suitable permissions if it does not exist.
Otherwise its permissions must allow all users to traverse the directory (i.e. it must have `o+x` set, in unix parlance) for non-sandboxed builds to work correctly.
This is also the location where [`--keep-failed`](/pages/nix-manual/command-ref/opt-common#opt-keep-failed) leaves its files.
If Nix runs without sandbox, or if the platform does not support sandboxing with bind mounts (e.g. macOS), then the [`builder`](/pages/nix-manual/language/derivations#attr-builder)'s environment will contain this directory, instead of the virtual location [`sandbox-build-dir`](/pages/nix-manual/command-ref/conf-file-prefix#conf-sandbox-build-dir).

**Warning**
`build-dir` must not be set to a world-writable directory.
Placing temporary build directories in a world-writable place allows other users to access or modify build data that is currently in use.
This alone is merely an impurity, but combined with another factor this has allowed malicious derivations to escape the build sandbox.

See also the global [`build-dir`](/pages/nix-manual/command-ref/conf-file-prefix#conf-build-dir) setting.
**Default:** ``
- `check-mount`
Check that the overlay filesystem is correctly mounted.
Nix does not manage the overlayfs mount point itself, but the correct
functioning of the overlay store does depend on this mount point being set up
correctly. Rather than just assume this is the case, check that the lowerdir
and upperdir options are what we expect them to be. This check is on by
default, but can be disabled if needed.
**Default:** `true`
- `ignore-gc-delete-failure`

**Warning**
This setting is part of an
[experimental feature](/pages/nix-manual/development/experimental-features).
To change this setting, make sure the
[`local-overlay-store` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-local-overlay-store)
is enabled.
For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
extra-experimental-features = local-overlay-store
ignore-gc-delete-failure = ...

Whether to ignore failures when deleting items with the garbage collector.
Normally the garbage collector will fail with an error if the nix daemon cannot delete a file, with this setting such errors will only be printed as warnings.
**Default:** `false`
- `log`
directory where Nix stores log files.
**Default:** `/nix/var/log/nix`
- `lower-store`
[Store URL](/pages/nix-manual/command-ref/new-cli/nix3-help-stores#store-url-format)
for the lower store. The default is `auto` (i.e. use the Nix daemon or `/nix/store` directly).
Must be a store with a store dir on the file system.
Must be used as OverlayFS lower layer for this store's store dir.
**Default:** *empty*
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `read-only`
Allow this store to be opened when its [database](/pages/nix-manual/glossary#gloss-nix-database) is on a read-only filesystem.
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
- `remount-hook`
Script or other executable to run when overlay filesystem needs remounting.
This is occasionally necessary when deleting a store path that exists in both upper and lower layers.
In such a situation, bypassing OverlayFS and deleting the path in the upper layer directly
is the only way to perform the deletion without creating a "whiteout".
However this causes the OverlayFS kernel data structures to get out-of-sync,
and can lead to 'stale file handle' errors; remounting solves the problem.
The store directory is passed as an argument to the invoked executable.
**Default:** *empty*
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
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `upper-layer`
Directory containing the OverlayFS upper layer for this store's store dir.
**Default:** *empty*
- `use-roots-daemon`

**Warning**
This setting is part of an
[experimental feature](/pages/nix-manual/development/experimental-features).
To change this setting, make sure the
[`local-overlay-store` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-local-overlay-store)
is enabled.
For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
extra-experimental-features = local-overlay-store
use-roots-daemon = ...

Whether to request garbage collector roots from an external daemon.
When enabled, the garbage collector connects to a Unix domain socket
at [`&lt;state-dir&gt;`](/pages/nix-manual/store/types/local-store#store-option-state)`/gc-roots-socket/socket` to discover additional roots
that should not be collected. This is useful when the Nix daemon runs
without root privileges and cannot scan `/proc` for runtime roots.
The daemon can be started with [`nix store roots-daemon`](/pages/nix-manual/command-ref/experimental-commands).
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

# <a id="experimental-ssh-store-with-filesystem-mounted"></a> Experimental SSH Store with filesystem mounted

> **Warning**
>
> This store is part of an
> [experimental feature](/pages/nix-manual/development/experimental-features).
>
> To use this store, make sure the
> [`mounted-ssh-store` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-mounted-ssh-store)
> is enabled.
> For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
>
> ```
> extra-experimental-features = mounted-ssh-store
> ```

**Store URL format**: `mounted-ssh-ng://[username@]hostname`

Experimental store type that allows full access to a Nix store on a remote machine,
and additionally requires that store be mounted in the local file system.

The mounting of that store is not managed by Nix, and must by managed manually.
It could be accomplished with SSHFS or NFS, for example.

The local file system is used to optimize certain operations.
For example, rather than serializing Nix archives and sending over the Nix channel,
we can directly access the file system data via the mount-point.

The local file system is also used to make certain operations possible that wouldn't otherwise be.
For example, persistent GC roots can be created if they reside on the same file system as the remote store:
the remote side will create the symlinks necessary to avoid race conditions.

## <a id="settings-2"></a> Settings

- `base64-ssh-public-host-key`
The public host key of the remote machine.
**Default:** *empty*
- `compress`
Whether to enable SSH compression.
**Default:** `false`
- `log`
directory where Nix stores log files.
**Default:** `/nix/var/log/nix`
- `max-connection-age`
Maximum age of a connection before it is closed.
**Default:** `4294967295`
- `max-connections`
Maximum number of concurrent connections to the Nix daemon.
**Default:** `1`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `real`
Physical path of the Nix store.
**Default:** `/nix/store`
- `remote-program`
Path to the `nix-daemon` executable on the remote machine.
**Default:** `nix-daemon`
- `remote-store`
[Store URL](/pages/nix-manual/store/types#store-url-format)
to be used on the remote machine. The default is `auto`
(i.e. use the Nix daemon or `/nix/store` directly).
**Default:** *empty*
- `root`
Directory prefixed to all other paths.
**Default:** ``
- `ssh-key`
Path to the SSH private key used to authenticate to the remote machine.
**Default:** *empty*
- `state`
Directory where Nix stores state.
**Default:** `/dummy`
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

# <a id="experimental-ssh-store"></a> Experimental SSH Store

**Store URL format**: `ssh-ng://[username@]hostname[:port]`

Experimental store type that allows full access to a Nix store on a
remote machine.

## <a id="settings-3"></a> Settings

- `base64-ssh-public-host-key`
The public host key of the remote machine.
**Default:** *empty*
- `compress`
Whether to enable SSH compression.
**Default:** `false`
- `max-connection-age`
Maximum age of a connection before it is closed.
**Default:** `4294967295`
- `max-connections`
Maximum number of concurrent connections to the Nix daemon.
**Default:** `1`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `remote-program`
Path to the `nix-daemon` executable on the remote machine.
**Default:** `nix-daemon`
- `remote-store`
[Store URL](/pages/nix-manual/store/types#store-url-format)
to be used on the remote machine. The default is `auto`
(i.e. use the Nix daemon or `/nix/store` directly).
**Default:** *empty*
- `ssh-key`
Path to the SSH private key used to authenticate to the remote machine.
**Default:** *empty*
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

# <a id="http-binary-cache-store"></a> HTTP Binary Cache Store

**Store URL format**: `http://...`, `https://...`

This store allows a binary cache to be accessed via the HTTP
protocol.

## <a id="settings-4"></a> Settings

- `compression`
NAR compression method. One of: `xz`, `bzip2`, `gzip`, `zstd`, `none`, `br`, `compress`, `grzip`, `lrzip`, `lz4`, `lzip`, `lzma` or `lzop`.
To use a particular compression method Nix has to be built with a version of libarchive that natively supports that compression algorithm.
**Default:** `xz`
- `compression-level`
The *preset level* to be used when compressing NARs.
The meaning and accepted values depend on the compression method selected.
`-1` specifies that the default compression level should be used.
**Default:** `-1`
- `index-debug-info`
Whether to index DWARF debug info files by build ID. This allows [`dwarffs`](https://github.com/edolstra/dwarffs) to
fetch debug info on demand
**Default:** `false`
- `local-nar-cache`
Path to a local cache of NARs fetched from this binary cache, used by commands such as `nix store cat`.
**Default:** ``
- `log-compression`
Compression method for `log/*` files. It is recommended to
use a compression method supported by most web browsers
(e.g. `brotli`).
**Default:** ``
- `ls-compression`
Compression method for `.ls` files.
**Default:** ``
- `narinfo-compression`
Compression method for `.narinfo` files.
**Default:** ``
- `parallel-compression`
Enable multi-threaded compression of NARs. This is currently only available for `xz` and `zstd`.
**Default:** `false`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `secret-key`
Path to the secret key used to sign the binary cache.
**Default:** *empty*
- `secret-keys`
List of comma-separated paths to the secret keys used to sign the binary cache.
**Default:** *empty*
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `tls-certificate`
Path to an optional TLS client certificate in PEM format.
**Default:** ``
- `tls-private-key`
Path to an optional TLS client certificate private key in PEM format.
**Default:** ``
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`
- `write-nar-listing`
Whether to write a JSON file that lists the files in each NAR.
**Default:** `false`

# <a id="local-binary-cache-store"></a> Local Binary Cache Store

**Store URL format**: `file://`*path*

This store allows reading and writing a binary cache stored in *path*
in the local filesystem. If *path* does not exist, it will be created.

For example, the following builds or downloads `nixpkgs#hello` into
the local store and then copies it to the binary cache in
`/tmp/binary-cache`:

```
# nix copy --to file:///tmp/binary-cache nixpkgs#hello
```

## <a id="settings-5"></a> Settings

- `compression`
NAR compression method. One of: `xz`, `bzip2`, `gzip`, `zstd`, `none`, `br`, `compress`, `grzip`, `lrzip`, `lz4`, `lzip`, `lzma` or `lzop`.
To use a particular compression method Nix has to be built with a version of libarchive that natively supports that compression algorithm.
**Default:** `xz`
- `compression-level`
The *preset level* to be used when compressing NARs.
The meaning and accepted values depend on the compression method selected.
`-1` specifies that the default compression level should be used.
**Default:** `-1`
- `index-debug-info`
Whether to index DWARF debug info files by build ID. This allows [`dwarffs`](https://github.com/edolstra/dwarffs) to
fetch debug info on demand
**Default:** `false`
- `local-nar-cache`
Path to a local cache of NARs fetched from this binary cache, used by commands such as `nix store cat`.
**Default:** ``
- `parallel-compression`
Enable multi-threaded compression of NARs. This is currently only available for `xz` and `zstd`.
**Default:** `false`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `secret-key`
Path to the secret key used to sign the binary cache.
**Default:** *empty*
- `secret-keys`
List of comma-separated paths to the secret keys used to sign the binary cache.
**Default:** *empty*
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`
- `write-nar-listing`
Whether to write a JSON file that lists the files in each NAR.
**Default:** `false`

# <a id="local-daemon-store"></a> Local Daemon Store

**Store URL format**: `daemon`, `unix://`*path*

This store type accesses a Nix store by talking to a Nix daemon
listening on the Unix domain socket *path*. The store pseudo-URL
`daemon` is equivalent to `unix:///nix/var/nix/daemon-socket/socket`.

## <a id="settings-6"></a> Settings

- `log`
directory where Nix stores log files.
**Default:** `/nix/var/log/nix`
- `max-connection-age`
Maximum age of a connection before it is closed.
**Default:** `4294967295`
- `max-connections`
Maximum number of concurrent connections to the Nix daemon.
**Default:** `1`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `real`
Physical path of the Nix store.
**Default:** `/nix/store`
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
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

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

## <a id="settings-7"></a> Settings

- `build-dir`
The directory on the host, in which derivations' temporary build directories are created.
If not set, Nix will use the `builds` subdirectory of its configured state directory.
Note that builds are often performed by the Nix daemon, so its `build-dir` applies.
Nix will create this directory automatically with suitable permissions if it does not exist.
Otherwise its permissions must allow all users to traverse the directory (i.e. it must have `o+x` set, in unix parlance) for non-sandboxed builds to work correctly.
This is also the location where [`--keep-failed`](/pages/nix-manual/command-ref/opt-common#opt-keep-failed) leaves its files.
If Nix runs without sandbox, or if the platform does not support sandboxing with bind mounts (e.g. macOS), then the [`builder`](/pages/nix-manual/language/derivations#attr-builder)'s environment will contain this directory, instead of the virtual location [`sandbox-build-dir`](/pages/nix-manual/command-ref/conf-file-prefix#conf-sandbox-build-dir).

**Warning**
`build-dir` must not be set to a world-writable directory.
Placing temporary build directories in a world-writable place allows other users to access or modify build data that is currently in use.
This alone is merely an impurity, but combined with another factor this has allowed malicious derivations to escape the build sandbox.

See also the global [`build-dir`](/pages/nix-manual/command-ref/conf-file-prefix#conf-build-dir) setting.
**Default:** ``
- `ignore-gc-delete-failure`

**Warning**
This setting is part of an
[experimental feature](/pages/nix-manual/development/experimental-features).
To change this setting, make sure the
[`local-overlay-store` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-local-overlay-store)
is enabled.
For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
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
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `read-only`
Allow this store to be opened when its [database](/pages/nix-manual/glossary#gloss-nix-database) is on a read-only filesystem.
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
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `use-roots-daemon`

**Warning**
This setting is part of an
[experimental feature](/pages/nix-manual/development/experimental-features).
To change this setting, make sure the
[`local-overlay-store` experimental feature](/pages/nix-manual/development/experimental-features#xp-feature-local-overlay-store)
is enabled.
For example, include the following in [`nix.conf`](/pages/nix-manual/command-ref/conf-file-prefix):
extra-experimental-features = local-overlay-store
use-roots-daemon = ...

Whether to request garbage collector roots from an external daemon.
When enabled, the garbage collector connects to a Unix domain socket
at [`&lt;state-dir&gt;`](/pages/nix-manual/store/types/local-store#store-option-state)`/gc-roots-socket/socket` to discover additional roots
that should not be collected. This is useful when the Nix daemon runs
without root privileges and cannot scan `/proc` for runtime roots.
The daemon can be started with [`nix store roots-daemon`](/pages/nix-manual/command-ref/experimental-commands).
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

# <a id="s3-binary-cache-store"></a> S3 Binary Cache Store

**Store URL format**: `s3://`*bucket-name*

This store allows reading and writing a binary cache stored in an AWS S3 (or S3-compatible service) bucket.
This store shares many idioms with the [HTTP Binary Cache Store](/pages/nix-manual/store/types/http-binary-cache-store).

For AWS S3, the binary cache URL for a bucket named `example-nix-cache` will be exactly [s3://example-nix-cache](/pages/nix-manual/command-ref/new-cli/s3:/example-nix-cache).
For S3 compatible binary caches, consult that cache's documentation.

### <a id="anonymous-reads-to-your-s3-compatible-binary-cache"></a> Anonymous reads to your S3-compatible binary cache

> If your binary cache is publicly accessible and does not require authentication,
> it is simplest to use the [HTTP Binary Cache Store] rather than S3 Binary Cache Store with
> [https://example-nix-cache.s3.amazonaws.com](https://example-nix-cache.s3.amazonaws.com) instead of [s3://example-nix-cache](/pages/nix-manual/command-ref/new-cli/s3:/example-nix-cache).

Your bucket will need a
[bucket policy](https://docs.aws.amazon.com/AmazonS3/v1/userguide/bucket-policies.html)
like the following to be accessible:

```
{
    "Id": "DirectReads",
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowDirectReads",
            "Action": [
                "s3:GetObject",
                "s3:GetBucketLocation",
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::example-nix-cache",
                "arn:aws:s3:::example-nix-cache/*"
            ],
            "Principal": "*"
        }
    ]
}
```

### <a id="authentication"></a> Authentication

Nix will use the
[default credential provider chain](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/credentials.html)
for authenticating requests to Amazon S3.

Note that this means Nix will read environment variables and files with different idioms than with Nix's own settings, as implemented by the AWS SDK.
Consult the documentation linked above for further details.

### <a id="authenticated-reads-to-your-s3-binary-cache"></a> Authenticated reads to your S3 binary cache

Your bucket will need a bucket policy allowing the desired users to perform the `s3:GetObject`, `s3:GetBucketLocation`, and `s3:ListBucket` actions on all objects in the bucket.
The anonymous policy given above can be updated to have a restricted `Principal` to support this.

### <a id="authenticated-writes-to-your-s3-compatible-binary-cache"></a> Authenticated writes to your S3-compatible binary cache

Your account will need an IAM policy to support uploading to the bucket:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UploadToCache",
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::example-nix-cache",
        "arn:aws:s3:::example-nix-cache/*"
      ]
    }
  ]
}
```

### <a id="examples"></a> Examples

With bucket policies and authentication set up as described above, uploading works via [`nix copy`](/pages/nix-manual/command-ref/new-cli/nix3-copy) (experimental).

- To upload with a specific credential profile for Amazon S3:
$ nix copy nixpkgs.hello \
 --to 's3://example-nix-cache?profile=cache-upload&region=eu-west-2'
- To upload to an S3-compatible binary cache:
$ nix copy nixpkgs.hello --to \
 's3://example-nix-cache?profile=cache-upload&scheme=https&endpoint=minio.example.com'

## <a id="settings-8"></a> Settings

- `addressing-style`
The S3 addressing style to use. `auto` (default) uses
virtual-hosted-style for standard AWS endpoints and path-style
for custom endpoints; bucket names containing dots automatically
fall back to path-style to avoid TLS certificate errors. `path`
forces path-style addressing (deprecated by AWS). `virtual`
forces virtual-hosted-style addressing (bucket names must not
contain dots).
**Default:** `auto`
- `compression`
NAR compression method. One of: `xz`, `bzip2`, `gzip`, `zstd`, `none`, `br`, `compress`, `grzip`, `lrzip`, `lz4`, `lzip`, `lzma` or `lzop`.
To use a particular compression method Nix has to be built with a version of libarchive that natively supports that compression algorithm.
**Default:** `xz`
- `compression-level`
The *preset level* to be used when compressing NARs.
The meaning and accepted values depend on the compression method selected.
`-1` specifies that the default compression level should be used.
**Default:** `-1`
- `endpoint`
The S3 endpoint to use. When empty (default), uses AWS S3 with
region-specific endpoints. For S3-compatible services such as
MinIO, set this to your service's endpoint.
**Default:** *empty*
- `index-debug-info`
Whether to index DWARF debug info files by build ID. This allows [`dwarffs`](https://github.com/edolstra/dwarffs) to
fetch debug info on demand
**Default:** `false`
- `local-nar-cache`
Path to a local cache of NARs fetched from this binary cache, used by commands such as `nix store cat`.
**Default:** ``
- `log-compression`
Compression method for `log/*` files. It is recommended to
use a compression method supported by most web browsers
(e.g. `brotli`).
**Default:** ``
- `ls-compression`
Compression method for `.ls` files.
**Default:** ``
- `multipart-chunk-size`
The size (in bytes) of each part in multipart uploads. Must be
at least 5 MiB (AWS S3 requirement). Larger chunk sizes reduce the
number of requests but use more memory. Default is 5 MiB.
**Default:** `5242880`
**Deprecated alias:** `buffer-size`
- `multipart-threshold`
The minimum file size (in bytes) for using multipart uploads.
Files smaller than this threshold will use regular PUT requests.
Default is 100 MiB. Only takes effect when multipart-upload is enabled.
**Default:** `104857600`
- `multipart-upload`
Whether to use multipart uploads for large files. When enabled,
files exceeding the multipart threshold will be uploaded in
multiple parts, which is required for files larger than 5 GiB and
can improve performance and reliability for large uploads.
**Default:** `false`
- `narinfo-compression`
Compression method for `.narinfo` files.
**Default:** ``
- `parallel-compression`
Enable multi-threaded compression of NARs. This is currently only available for `xz` and `zstd`.
**Default:** `false`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `profile`
The name of the AWS configuration profile to use. By default
Nix uses the `default` profile.
**Default:** `default`
- `region`
The region of the S3 bucket. If your bucket is not in
`us-east-1`, you should always explicitly specify the region
parameter.
**Default:** `us-east-1`
- `scheme`
The scheme used for S3 requests, `https` (default) or `http`. This
option allows you to disable HTTPS for binary caches which don't
support it.

**Note**
HTTPS should be used if the cache might contain sensitive
information.

**Default:** `https`
- `secret-key`
Path to the secret key used to sign the binary cache.
**Default:** *empty*
- `secret-keys`
List of comma-separated paths to the secret keys used to sign the binary cache.
**Default:** *empty*
- `storage-class`
The S3 storage class to use for uploaded objects. When not set (default),
uses the bucket's default storage class. Valid values include:

See AWS S3 documentation for detailed storage class descriptions and pricing:
https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html
**Default:** ``
  - STANDARD (default, frequently accessed data)
  - REDUCED\_REDUNDANCY (less frequently accessed data)
  - STANDARD\_IA (infrequent access)
  - ONEZONE\_IA (infrequent access, single AZ)
  - INTELLIGENT\_TIERING (automatic cost optimization)
  - GLACIER (archival with retrieval times in minutes to hours)
  - DEEP\_ARCHIVE (long-term archival with 12-hour retrieval)
  - GLACIER\_IR (instant retrieval archival)
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `tls-certificate`
Path to an optional TLS client certificate in PEM format.
**Default:** ``
- `tls-private-key`
Path to an optional TLS client certificate private key in PEM format.
**Default:** ``
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`
- `write-nar-listing`
Whether to write a JSON file that lists the files in each NAR.
**Default:** `false`

# <a id="ssh-store"></a> SSH Store

**Store URL format**: `ssh://[username@]hostname[:port]`

This store type allows limited access to a remote store on another
machine via SSH.

## <a id="settings-9"></a> Settings

- `base64-ssh-public-host-key`
The public host key of the remote machine.
**Default:** *empty*
- `compress`
Whether to enable SSH compression.
**Default:** `false`
- `log-fd`
file descriptor to which SSH's stderr is connected
**Default:** `-1`
- `max-connections`
Maximum number of concurrent SSH connections.
**Default:** `1`
- `path-info-cache-size`
Size of the in-memory store path metadata cache.
**Default:** `65536`
- `priority`
Priority of this store when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `remote-program`
Path to the `nix-store` executable on the remote machine.
**Default:** `nix-store`
- `remote-store`
[Store URL](/pages/nix-manual/store/types#store-url-format)
to be used on the remote machine. The default is `auto`
(i.e. use the Nix daemon or `/nix/store` directly).
**Default:** *empty*
- `ssh-key`
Path to the SSH private key used to authenticate to the remote machine.
**Default:** *empty*
- `store`
Logical location of the Nix store, usually
`/nix/store`. Note that you can only copy store paths
between stores if they have the same `store` setting.
**Default:** `/nix/store`
- `system-features`
Optional [system features](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters).
**Default:** `false`

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
