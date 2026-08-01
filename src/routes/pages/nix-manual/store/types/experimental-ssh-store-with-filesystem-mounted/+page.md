# Experimental SSH Store with filesystem mounted - Nix 2.34.9 Reference Manual

> Source: [/pages/nix-manual/store/types/experimental-ssh-store-with-filesystem-mounted](/pages/nix-manual/store/types/experimental-ssh-store-with-filesystem-mounted)

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

## <a id="settings"></a> Settings

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
