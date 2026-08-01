# nix profile - Nix 2.34.9 Reference Manual

> Source: [https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-profile.html](@docroot@/command-ref/new-cli/nix3-profile.md)

> **Warning**
>
> This program is
> [**experimental**](https://nix.dev/manual/nix/2.34/development/experimental-features#xp-feature-nix-command)
> and its interface is subject to change.

# <a id="name"></a> Name

`nix profile` - manage Nix profiles

# <a id="synopsis"></a> Synopsis

`nix profile` [*option*...] *subcommand*

where *subcommand* is one of the following:

- [`nix profile add`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-add) - add a package to a profile
- [`nix profile diff-closures`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-diff-closures) - show the closure difference between each version of a profile
- [`nix profile history`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-history) - show all versions of a profile
- [`nix profile list`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-list) - list packages in the profile
- [`nix profile remove`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-remove) - remove packages from a profile
- [`nix profile rollback`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-rollback) - roll back to the previous version or a specified version of a profile
- [`nix profile upgrade`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-upgrade) - upgrade packages using their most recent flake
- [`nix profile wipe-history`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile-wipe-history) - delete non-current versions of a profile

# <a id="description"></a> Description

`nix profile` allows you to create and manage *Nix profiles*. A Nix
profile is a set of packages that can be installed and upgraded
independently from each other. Nix profiles are versioned, allowing
them to be rolled back easily.

# <a id="files"></a> Files

## <a id="profiles"></a> Profiles

A directory that contains links to profiles managed by [`nix-env`](https://nix.dev/manual/nix/2.34/command-ref/nix-env) and [`nix profile`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile):

- `$XDG_STATE_HOME/nix/profiles` for regular users
- `$NIX_STATE_DIR/profiles/per-user/root` if the user is `root`

A profile is a directory of symlinks to files in the Nix store.

### <a id="filesystem-layout"></a> Filesystem layout

Profiles are versioned as follows. When using a profile named *path*, *path* is a symlink to *path*`-`*N*`-link`, where *N* is the version of the profile.
In turn, *path*`-`*N*`-link` is a symlink to a path in the Nix store.
For example:

```
$ ls -l ~alice/.local/state/nix/profiles/profile*
lrwxrwxrwx 1 alice users 14 Nov 25 14:35 /home/alice/.local/state/nix/profiles/profile -> profile-7-link
lrwxrwxrwx 1 alice users 51 Oct 28 16:18 /home/alice/.local/state/nix/profiles/profile-5-link -> /nix/store/q69xad13ghpf7ir87h0b2gd28lafjj1j-profile
lrwxrwxrwx 1 alice users 51 Oct 29 13:20 /home/alice/.local/state/nix/profiles/profile-6-link -> /nix/store/6bvhpysd7vwz7k3b0pndn7ifi5xr32dg-profile
lrwxrwxrwx 1 alice users 51 Nov 25 14:35 /home/alice/.local/state/nix/profiles/profile-7-link -> /nix/store/mp0x6xnsg0b8qhswy6riqvimai4gm677-profile
```

Each of these symlinks is a root for the Nix garbage collector.

The contents of the store path corresponding to each version of the
profile is a tree of symlinks to the files of the installed packages,
e.g.

```
$ ll -R ~eelco/.local/state/nix/profiles/profile-7-link/
/home/eelco/.local/state/nix/profiles/profile-7-link/:
total 20
dr-xr-xr-x 2 root root 4096 Jan  1  1970 bin
-r--r--r-- 2 root root 1402 Jan  1  1970 manifest.nix
dr-xr-xr-x 4 root root 4096 Jan  1  1970 share

/home/eelco/.local/state/nix/profiles/profile-7-link/bin:
total 20
lrwxrwxrwx 5 root root 79 Jan  1  1970 chromium -> /nix/store/cyxny9d1zjb9l9103fr6j6kavp3bqjxf-chromium-86.0.4240.111/bin/chromium
lrwxrwxrwx 7 root root 87 Jan  1  1970 spotify -> /nix/store/w9182874m1bl56smps3m5zjj36jhp3rn-spotify-1.1.26.501.gbe11e53b-15/bin/spotify
lrwxrwxrwx 3 root root 79 Jan  1  1970 zoom-us -> /nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927/bin/zoom-us

/home/eelco/.local/state/nix/profiles/profile-7-link/share/applications:
total 12
lrwxrwxrwx 4 root root 120 Jan  1  1970 chromium-browser.desktop -> /nix/store/sqzyx2l85i6j2a77pnyvglh3bvzwmjjp-chromium-unwrapped-86.0.4240.111/share/applications/chromium-browser.desktop
lrwxrwxrwx 7 root root 110 Jan  1  1970 spotify.desktop -> /nix/store/w9182874m1bl56smps3m5zjj36jhp3rn-spotify-1.1.26.501.gbe11e53b-15/share/applications/spotify.desktop
lrwxrwxrwx 3 root root 107 Jan  1  1970 us.zoom.Zoom.desktop -> /nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927/share/applications/us.zoom.Zoom.desktop

…
```

Each profile version contains a manifest file:

- [`manifest.nix`](https://nix.dev/manual/nix/2.34/command-ref/files/manifest.nix) used by [`nix-env`](https://nix.dev/manual/nix/2.34/command-ref/nix-env).
- [`manifest.json`](https://nix.dev/manual/nix/2.34/command-ref/files/manifest.json) used by [`nix profile`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile) (experimental).

## <a id="user-profile-link"></a> User profile link

A symbolic link to the user's current profile:

- `~/.nix-profile`
- `$XDG_STATE_HOME/nix/profile` if [`use-xdg-base-directories`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-use-xdg-base-directories) is set to `true`.

By default, this symlink points to:

- `$XDG_STATE_HOME/nix/profiles/profile` for regular users
- `$NIX_STATE_DIR/profiles/per-user/root/profile` for `root`

The `PATH` environment variable should include `/bin` subdirectory of the profile link (e.g. `~/.nix-profile/bin`) for the user environment to be visible to the user.
The [installer](https://nix.dev/manual/nix/2.34/installation/installing-binary) sets this up by default, unless you enable [`use-xdg-base-directories`](https://nix.dev/manual/nix/2.34/command-ref/conf-file#conf-use-xdg-base-directories).

### <a id="profile-compatibility"></a> Profile compatibility

> **Warning**
>
> Once you have used [`nix profile`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile) you can no longer use [`nix-env`](https://nix.dev/manual/nix/2.34/command-ref/nix-env) without first deleting `$XDG_STATE_HOME/nix/profiles/profile`

Once you installed a package with [`nix profile`](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-profile), you get the following error message when using [`nix-env`](https://nix.dev/manual/nix/2.34/command-ref/nix-env):

```
$ nix-env -f '<nixpkgs>' -iA 'hello'
error: nix-env
profile '/home/alice/.local/state/nix/profiles/profile' is incompatible with 'nix-env'; please use 'nix profile' instead
```

To migrate back to `nix-env` you can delete your current profile:

> **Warning**
>
> This will delete packages that have been installed before, so you may want to back up this information before running the command.

```
 $ rm -rf "${XDG_STATE_HOME-$HOME/.local/state}/nix/profiles/profile"
```

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
