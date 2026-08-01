# Local Binary Cache Store - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/store/types/local-binary-cache-store.html](@docroot@/store/types/local-binary-cache-store.md)

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

## <a id="settings"></a> Settings

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
Priority of this store when used as a [substituter](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-substituters).
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
Optional [system features](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-system-features) available on the system this store uses to build derivations.
Example: `"kvm"`
**Default:** *machine-specific*
- `trusted`
Whether paths from this store can be used as substitutes
even if they are not signed by a key listed in the
[`trusted-public-keys`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-trusted-public-keys)
setting.
**Default:** `false`
- `want-mass-query`
Whether this store can be queried efficiently for path validity when used as a [substituter](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-substituters).
**Default:** `false`
- `write-nar-listing`
Whether to write a JSON file that lists the files in each NAR.
**Default:** `false`
