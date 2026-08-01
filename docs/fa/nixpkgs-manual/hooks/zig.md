# Zig {#zig}

[Zig](https://ziglang.org/) یک زبان برنامه‌نویسی با هدف عام و زنجیره ابزار برای نگهداری نرم‌افزارهای مقاوم، بهینه و قابل استفاده مجدد است.

در Nixpkgs، `zig` فازهای پیش‌فرض ساخت، بررسی و نصب را بازنشانی می‌کند.

## قطعه کد نمونه {#zig-example-code-snippet}

```nix
{
  lib,
  stdenv,
  zig,
}:

stdenv.mkDerivation {
  # . . .

  nativeBuildInputs = [ zig ];

  zigBuildFlags = [ "-Dman-pages=true" ];

  dontUseZigCheck = true;

  # . . .
}
```

## متغیرهای کنترل‌کننده zig {#zig-variables-controlling}

### متغیرهای اختصاصی `zig` {#zig-exclusive-variables}

متغیرهای زیر اختصاصی `zig` هستند.

#### `dontUseZigConfigure` {#dont-use-zig-configure}

استفاده از `zigConfigurePhase` را غیرفعال می‌کند.

#### `dontUseZigBuild` {#dont-use-zig-build}

استفاده از `zigBuildPhase` را غیرفعال می‌کند.

#### `dontUseZigCheck` {#dont-use-zig-check}

استفاده از `zigCheckPhase` را غیرفعال می‌کند.

#### `dontUseZigInstall` {#dont-use-zig-install}

استفاده از `zigInstallPhase` را غیرفعال می‌کند.

#### `dontSetZigDefaultFlags` {#dont-set-zig-default-flags}

استفاده از مجموعه‌ای از پرچم‌های پیش‌فرض را هنگام انجام ساخت‌های zig غیرفعال می‌کند.

### متغیرهای مشابه {#zig-similar-variables}

متغیرهای زیر مشابه معادل‌های خود در `stdenv.mkDerivation` هستند.

| متغیر `zig` | معادل `stdenv.mkDerivation` |
|---------------------|-----------------------------------|
| `zigBuildFlags`     | `buildFlags`                      |
| `zigCheckFlags`     | `checkFlags`                      |
| `zigInstallFlags`   | `installFlags`                    |

### متغیرهای پشتیبانی‌شده توسط zig {#zig-variables-honored}

متغیرهای زیر که معمولاً در `stdenv.mkDerivation` استفاده می‌شوند، توسط `zig` رعایت می‌شوند.

- `prefixKey`
- `dontAddPrefix`
