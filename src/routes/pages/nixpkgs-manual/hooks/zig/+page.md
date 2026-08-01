# <a id="zig"></a> Zig

[Zig](https://ziglang.org/) یک زبان برنامه‌نویسی با هدف عام و زنجیره ابزار برای نگهداری نرم‌افزارهای مقاوم، بهینه و قابل استفاده مجدد است.

در Nixpkgs، `zig` فازهای پیش‌فرض ساخت، بررسی و نصب را بازنشانی می‌کند.

## <a id="zig-example-code-snippet"></a> قطعه کد نمونه

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

## <a id="zig-variables-controlling"></a> متغیرهای کنترل‌کننده zig

### <a id="zig-exclusive-variables"></a> متغیرهای اختصاصی `zig`

متغیرهای زیر اختصاصی `zig` هستند.

#### <a id="dont-use-zig-configure"></a> `dontUseZigConfigure`

استفاده از `zigConfigurePhase` را غیرفعال می‌کند.

#### <a id="dont-use-zig-build"></a> `dontUseZigBuild`

استفاده از `zigBuildPhase` را غیرفعال می‌کند.

#### <a id="dont-use-zig-check"></a> `dontUseZigCheck`

استفاده از `zigCheckPhase` را غیرفعال می‌کند.

#### <a id="dont-use-zig-install"></a> `dontUseZigInstall`

استفاده از `zigInstallPhase` را غیرفعال می‌کند.

#### <a id="dont-set-zig-default-flags"></a> `dontSetZigDefaultFlags`

استفاده از مجموعه‌ای از پرچم‌های پیش‌فرض را هنگام انجام ساخت‌های zig غیرفعال می‌کند.

### <a id="zig-similar-variables"></a> متغیرهای مشابه

متغیرهای زیر مشابه معادل‌های خود در `stdenv.mkDerivation` هستند.

| متغیر `zig` | معادل `stdenv.mkDerivation` |
|---------------------|-----------------------------------|
| `zigBuildFlags`     | `buildFlags`                      |
| `zigCheckFlags`     | `checkFlags`                      |
| `zigInstallFlags`   | `installFlags`                    |

### <a id="zig-variables-honored"></a> متغیرهای پشتیبانی‌شده توسط zig

متغیرهای زیر که معمولاً در `stdenv.mkDerivation` استفاده می‌شوند، توسط `zig` رعایت می‌شوند.

- `prefixKey`
- `dontAddPrefix`
