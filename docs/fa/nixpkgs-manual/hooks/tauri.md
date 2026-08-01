# cargo-tauri.hook {#tauri-hook}

[Tauri](https://tauri.app/) چارچوبی برای ساخت برنامه‌های دسکتاپ کوچک‌تر، سریع‌تر و امن‌تر با فرانت‌اند وب است.

در Nixpkgs، `cargo-tauri.hook` فازهای پیش‌فرض ساخت و نصب را بازنشانی می‌کند.

## قطعه‌کد نمونه {#tauri-hook-example-code-snippet}

```nix
{
  lib,
  stdenv,
  rustPlatform,
  fetchNpmDeps,
  cargo-tauri,
  glib-networking,
  nodejs,
  npmHooks,
  openssl,
  pkg-config,
  webkitgtk_4_1,
  wrapGAppsHook4,
}:

rustPlatform.buildRustPackage (finalAttrs: {
  # ...

  cargoHash = "...";

  # Assuming our app's frontend uses `npm` as a package manager
  npmDeps = fetchNpmDeps {
    name = "${finalAttrs.pname}-${finalAttrs.version}-npm-deps";
    inherit (finalAttrs) src;
    hash = "...";
  };

  nativeBuildInputs = [
    # Pull in our main hook
    cargo-tauri.hook

    # Setup npm
    nodejs
    npmHooks.npmConfigHook

    # Make sure we can find our libraries
    pkg-config
  ]
  ++ lib.optionals stdenv.hostPlatform.isLinux [ wrapGAppsHook4 ];

  buildInputs = lib.optionals stdenv.hostPlatform.isLinux [
    glib-networking # Most Tauri apps need networking
    openssl
    webkitgtk_4_1
  ];

  # Set our Tauri source directory
  cargoRoot = "src-tauri";
  # And make sure we build there too
  buildAndTestSubdir = finalAttrs.cargoRoot;

  # ...
})
```

## متغیرهای کنترل‌کننده cargo-tauri {#tauri-hook-variables-controlling}

### متغیرهای اختصاصی Tauri {#tauri-hook-exclusive-variables}

#### `tauriBuildFlags` {#tauri-build-flags}

پرچم‌های ارسال‌شده به `cargo tauri build` را کنترل می‌کند.

#### `tauriBundleType` {#tauri-bundle-type}

[نوع باندل](https://tauri.app/v1/guides/building/) برای ساخت.

#### `dontTauriBuild` {#dont-tauri-build}

استفاده از `tauriBuildHook` را غیرفعال می‌کند.

#### `dontTauriFixup` {#dont-tauri-fixup}

فاز پیش از اصلاح (pre fixup) مربوط به `tauriFixupHook` را غیرفعال می‌کند.

#### `dontTauriInstall` {#dont-tauri-install}

استفاده از `tauriInstallPostBuildHook` و `tauriInstallHook` را غیرفعال می‌کند.

### متغیرهای پشتیبانی‌شده {#tauri-hook-honored-variables}

همراه با موارد موجود در [](#compiling-rust-applications-with-cargo)، متغیرهای زیر که توسط `cargoBuildHook` و `cargoInstallHook` استفاده می‌شوند، توسط قلاب راه‌اندازی cargo-tauri نیز پشتیبانی می‌شوند.

- `buildAndTestSubdir`
- `cargoBuildType`
- `cargoBuildNoDefaultFeatures`
- `cargoBuildFeatures`
