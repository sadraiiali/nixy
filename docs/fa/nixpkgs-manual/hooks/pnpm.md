# pnpmBuildHook {#pnpm-build-hook}

[pnpm](https://pnpm.io/) یک مدیر بستهٔ سازگار با NPM است که بر افزایش سرعت مدیریت و کاهش فضای دیسک تمرکز دارد.

قلاب `pnpmBuildHook` در Nixpkgs، فاز ساخت پیش‌فرض را برای ساخت بسته‌هایی که از pnpm استفاده می‌کنند، بازنویسی می‌کند.

:::{.example #ex-pnpm-build-hook}
## نمونه قطعه‌کد pnpmBuildHook {#pnpm-build-hook-code-snippet}

```nix
{
  lib,
  stdenv,
  fetchFromGitHub,
  fetchPnpmDeps,
  pnpmConfigHook,
  pnpmBuildHook,
  makeBinaryWrapper,
  pnpm_10,
}:
let
  pnpm = pnpm_10;
in
stdenv.mkDerivation (finalAttrs: {
  pname = "coolPackages";
  version = "1.0";

  src = fetchFromGitHub {
    owner = "JaneCool";
    repo = "coolpackage";
    tag = finalAttrs.version;
    hash = lib.fakeHash;
  };

  __structuredAttrs = true;
  strictDeps = true;

  pnpmDeps = fetchPnpmDeps {
    inherit (finalAttrs) pname version src;
    inherit pnpm;
    fetcherVersion = 4;
    hash = lib.fakeHash;
  };

  nativeBuildInputs = [
    pnpmConfigHook
    pnpmBuildHook
    makeBinaryWrapper
  ];

  pnpmBuildScript = "build";
  pnpmBuildFlags = [
    "--mode"
    "production"
  ];
  pnpmWorkspaces = [
    "test"
  ];

  installPhase = ''
    runHook preInstall

    mkdir "$out"
    cp -r dist/. "$out"

    runHook postInstall
  '';

  meta = {
    description = "very cool package that does cool things";
    mainProgram = "cool";
  };
})
```
:::

## متغیرهای کنترل‌کننده `pnpmBuildHook` {#pnpm-build-hook-variables}

### متغیرهای اختصاصی pnpm {#pnpm-build-hook-exclusive-variables}

#### `pnpmBuildScript` {#pnpm-build-hook-script}

اسکریپت اجراشده برای ساخت بسته را کنترل می‌کند؛ به‌صورت پیش‌فرض این اسکریپت `build` است.

#### `pnpmFlags` {#pnpm-build-hook-flags}

پرچم‌های استفاده‌شده برای همه فراخوانی‌های pnpm در تمام هوک‌های محلی این derivation / اشتقاق ساخت را کنترل می‌کند.

#### `pnpmBuildFlags` {#pnpm-build-hook-build-flags}

پرچم‌های ارسال‌شده فقط به فراخوانی اسکریپت ساخت pnpm را کنترل می‌کند.

#### `dontPnpmBuild` {#pnpm-build-hook-dont}

اجرای خودکار `pnpmBuildHook` را غیرفعال می‌کند. فرآیند ساخت در صورت نیاز همچنان می‌تواند به‌صورت دستی اجرا شود، برای مثال:

```nix
{
  lib,
  rustPlatform,
  pnpmBuildHook,
  pnpmConfigHook,
  fetchPnpmDeps,
  emptyDirectory,
  pnpm_10,
}:
let
  pnpm = pnpm_10;
in
rustPlatform.buildRustPackage (finalAttrs: {
  pname = "super-fast-application";
  version = "1.0";

  src = emptyDirectory;

  cargoHash = lib.fakeHash;

  nativeBuildInputs = [
    pnpmBuildHook
    pnpmConfigHook
  ];

  pnpmDeps = fetchPnpmDeps {
    inherit (finalAttrs) pname version src;
    inherit pnpm;
    fetcherVersion = 4;
    hash = lib.fakeHash;
  };

  dontPnpmBuild = true;
  postBuild = ''
    pnpmBuildHook
  '';
})
```

### متغیرهای در نظر گرفته‌شده {#pnpm-build-hook-honored-variables}

متغیرهای زیر توسط `pnpmBuildHook` در نظر گرفته می‌شوند.

* [`pnpmRoot`](#javascript-pnpm-sourceRoot)
* [`pnpmWorkspaces`](#javascript-pnpm-workspaces)
