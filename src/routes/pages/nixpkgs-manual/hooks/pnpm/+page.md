# <a id="pnpm-build-hook"></a> pnpmBuildHook

[pnpm](https://pnpm.io/) یک مدیر بستهٔ سازگار با NPM است که بر افزایش سرعت مدیریت و کاهش فضای دیسک تمرکز دارد.

قلاب `pnpmBuildHook` در Nixpkgs، فاز ساخت پیش‌فرض را برای ساخت بسته‌هایی که از pnpm استفاده می‌کنند، بازنویسی می‌کند.

<a id="ex-pnpm-build-hook"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> ## <a id="pnpm-build-hook-code-snippet"></a> نمونه قطعه‌کد pnpmBuildHook
>

> ```nix
> {
>   lib,
>   stdenv,
>   fetchFromGitHub,
>   fetchPnpmDeps,
>   pnpmConfigHook,
>   pnpmBuildHook,
>   makeBinaryWrapper,
>   pnpm_10,
> }:
> let
>   pnpm = pnpm_10;
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "coolPackages";
>   version = "1.0";
>
>   src = fetchFromGitHub {
>     owner = "JaneCool";
>     repo = "coolpackage";
>     tag = finalAttrs.version;
>     hash = lib.fakeHash;
>   };
>
>   __structuredAttrs = true;
>   strictDeps = true;
>
>   pnpmDeps = fetchPnpmDeps {
>     inherit (finalAttrs) pname version src;
>     inherit pnpm;
>     fetcherVersion = 4;
>     hash = lib.fakeHash;
>   };
>
>   nativeBuildInputs = [
>     pnpmConfigHook
>     pnpmBuildHook
>     makeBinaryWrapper
>   ];
>
>   pnpmBuildScript = "build";
>   pnpmBuildFlags = [
>     "--mode"
>     "production"
>   ];
>   pnpmWorkspaces = [
>     "test"
>   ];
>
>   installPhase = ''
>     runHook preInstall
>
>     mkdir "$out"
>     cp -r dist/. "$out"
>
>     runHook postInstall
>   '';
>
>   meta = {
>     description = "very cool package that does cool things";
>     mainProgram = "cool";
>   };
> })
> ```

## <a id="pnpm-build-hook-variables"></a> متغیرهای کنترل‌کننده `pnpmBuildHook`

### <a id="pnpm-build-hook-exclusive-variables"></a> متغیرهای اختصاصی pnpm

#### <a id="pnpm-build-hook-script"></a> `pnpmBuildScript`

اسکریپت اجراشده برای ساخت بسته را کنترل می‌کند؛ به‌صورت پیش‌فرض این اسکریپت `build` است.

#### <a id="pnpm-build-hook-flags"></a> `pnpmFlags`

پرچم‌های استفاده‌شده برای همه فراخوانی‌های pnpm در تمام هوک‌های محلی این derivation / اشتقاق ساخت را کنترل می‌کند.

#### <a id="pnpm-build-hook-build-flags"></a> `pnpmBuildFlags`

پرچم‌های ارسال‌شده فقط به فراخوانی اسکریپت ساخت pnpm را کنترل می‌کند.

#### <a id="pnpm-build-hook-dont"></a> `dontPnpmBuild`

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

### <a id="pnpm-build-hook-honored-variables"></a> متغیرهای در نظر گرفته‌شده

متغیرهای زیر توسط `pnpmBuildHook` در نظر گرفته می‌شوند.

* [`pnpmRoot`](#javascript-pnpm-sourceRoot)
* [`pnpmWorkspaces`](#javascript-pnpm-workspaces)
