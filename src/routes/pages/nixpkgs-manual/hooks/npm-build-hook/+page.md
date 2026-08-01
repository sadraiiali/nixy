# <a id="npm-build-hook"></a> npmHooks.npmBuildHook

قلاب برای ساخت بسته‌هایی که از npm استفاده می‌کنند. می‌تواند در محیط‌های چندزبانه استفاده شود.

## <a id="npm-build-hook-snippet"></a> مثال‌ها

<a id="npm-build-hook-example-snippet"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استفاده از `npmHooks`
>

> ```nix
> {
>   stdenv,
>   fetchFromGitHub,
>   fetchNpmDeps,
>   npmHooks,
>   nodejsInstallExecutables,
>   nodejsInstallManuals,
>   nodejs,
> }:
> stdenv.mkDerivation (finalAttrs: {
>   pname = "some-npm-project";
>   version = "1.0";
>
>   src = fetchFromGitHub {
>     owner = "JohnNpm";
>     repo = "SomeProject";
>     tag = finalAttrs.version;
>     hash = "...";
>   };
>
>   strictDeps = true;
>
>   nativeBuildInputs = [
>     nodejs
>     nodejsInstallExecutables
>     nodejsInstallManuals
>     npmHooks.npmConfigHook
>     npmHooks.npmBuildHook
>     npmHooks.npmInstallHook
>   ];
>
>   npmBuildScript = "build";
>
>   npmBuildFlags = [
>     "--prod"
>   ];
>
>   npmFlags = [
>     "--ignore-scripts"
>   ];
>
>   npmDeps = fetchNpmDeps {
>     inherit (finalAttrs) src;
>     hash = "...";
>   };
>
>   makeWrapperArgs = [
>     "--set"
>     "NODE_ENV"
>     "production"
>   ];
>
>   meta = {
>     description = "npm project";
>   };
> })
> ```

## <a id="npm-build-hook-variables"></a> متغیرهای کنترل‌کننده `npmBuildHook`

### <a id="npm-build-hook-exclusive-variables"></a> متغیرهای اختصاصی `npmBuildHook`

#### <a id="npm-build-hook-script"></a> `npmBuildScript`

اسکریپتی را که برای ساخت بسته npm درون فایل `package.json` اجرا می‌شود، کنترل می‌کند.
تنظیم آن الزامی است، معمولاً روی `build` قرار می‌گیرد، اما می‌تواند بین بسته‌های مختلف متفاوت باشد.

#### <a id="npm-build-hook-flags"></a> `npmBuildFlags`

آرگومان‌های دستور `npm run $npmBuildScript` را کنترل می‌کند.

#### <a id="npm-build-hook-dont"></a> `dontNpmBuild`

در صورت فعال بودن، `npmBuildHook` را غیرفعال می‌کند.

### <a id="npm-build-hook-honored-variables"></a> متغیرهای مورد پشتیبانی

متغیرهای زیر توسط `npmBuildHook` پشتیبانی می‌شوند:

- [`npmWorkspace`](#javascript-buildNpmPackage-npmWorkspace)
- [`npmFlags`](#javascript-buildNpmPackage-npmFlags)
