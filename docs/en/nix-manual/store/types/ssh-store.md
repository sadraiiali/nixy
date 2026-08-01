# SSH Store - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/store/types/ssh-store.html](@docroot@/store/types/ssh-store.md)

# <a id="ssh-store"></a> SSH Store

**Store URL format**: `ssh://[username@]hostname[:port]`

This store type allows limited access to a remote store on another
machine via SSH.

## <a id="settings"></a> Settings

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
Priority of this store when used as a [substituter](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-substituters).
A lower value means a higher priority.
**Default:** `0`
- `remote-program`
Path to the `nix-store` executable on the remote machine.
**Default:** `nix-store`
- `remote-store`
[Store URL](https://nix.dev/manual/nix/2.34/store/types/#store-url-format)
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
