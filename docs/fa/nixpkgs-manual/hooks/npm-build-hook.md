# npmHooks.npmBuildHook {#npm-build-hook}

قلاب برای ساخت بسته‌هایی که از npm استفاده می‌کنند. می‌تواند در محیط‌های چندزبانه استفاده شود.

## مثال‌ها {#npm-build-hook-snippet}

:::{.example #npm-build-hook-example-snippet}

# استفاده از `npmHooks`

```nix
{
  stdenv,
  fetchFromGitHub,
  fetchNpmDeps,
  npmHooks,
  nodejsInstallExecutables,
  nodejsInstallManuals,
  nodejs,
}:
stdenv.mkDerivation (finalAttrs: {
  pname = "some-npm-project";
  version = "1.0";

  src = fetchFromGitHub {
    owner = "JohnNpm";
    repo = "SomeProject";
    tag = finalAttrs.version;
    hash = "...";
  };

  strictDeps = true;

  nativeBuildInputs = [
    nodejs
    nodejsInstallExecutables
    nodejsInstallManuals
    npmHooks.npmConfigHook
    npmHooks.npmBuildHook
    npmHooks.npmInstallHook
  ];

  npmBuildScript = "build";

  npmBuildFlags = [
    "--prod"
  ];

  npmFlags = [
    "--ignore-scripts"
  ];

  npmDeps = fetchNpmDeps {
    inherit (finalAttrs) src;
    hash = "...";
  };

  makeWrapperArgs = [
    "--set"
    "NODE_ENV"
    "production"
  ];

  meta = {
    description = "npm project";
  };
})
```
:::

## متغیرهای کنترل‌کننده `npmBuildHook` {#npm-build-hook-variables}

### متغیرهای اختصاصی `npmBuildHook` {#npm-build-hook-exclusive-variables}

#### `npmBuildScript` {#npm-build-hook-script}

اسکریپتی را که برای ساخت بسته npm درون فایل `package.json` اجرا می‌شود، کنترل می‌کند.
تنظیم آن الزامی است، معمولاً روی `build` قرار می‌گیرد، اما می‌تواند بین بسته‌های مختلف متفاوت باشد.

#### `npmBuildFlags` {#npm-build-hook-flags}

آرگومان‌های دستور {command}`npm run $npmBuildScript` را کنترل می‌کند.

#### `dontNpmBuild` {#npm-build-hook-dont}

در صورت فعال بودن، `npmBuildHook` را غیرفعال می‌کند.

### متغیرهای مورد پشتیبانی {#npm-build-hook-honored-variables}

متغیرهای زیر توسط `npmBuildHook` پشتیبانی می‌شوند:

- [`npmWorkspace`](#javascript-buildNpmPackage-npmWorkspace)
- [`npmFlags`](#javascript-buildNpmPackage-npmFlags)
