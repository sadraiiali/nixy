# wafHook {#waf-hook}

[Waf](https://waf.io) یک سیستم ساخت نرم‌افزار مبتنی بر پایتون است.

در Nixpkgs، `wafHook` فازهای پیش‌فرض پیکربندی، ساخت و نصب را بازنویسی می‌کند.

## متغیرهای کنترل‌کننده wafHook {#waf-hook-variables-controlling}

### متغیرهای اختصاصی `wafHook` {#waf-hook-exclusive-variables}

متغیرهای زیر اختصاصی `wafHook` هستند.

#### `wafPath` {#waf-path}

محل ابزار `waf`. مقدار پیش‌فرض آن `./waf` است تا پروژه‌های نرم‌افزاری که آن را مستقیماً درون درخت‌های کد منبع خود شامل شده‌اند پشتیبانی شوند.

اگر فایلی که `wafPath` به آن اشاره می‌کند وجود نداشته باشد، از `waf` ارائه‌شده توسط Nixpkgs استفاده خواهد شد.

#### `wafFlags` {#waf-flags}

پرچم‌های ارسال‌شده به ابزار waf را در طول فازهای ساخت و نصب کنترل می‌کند. برای تنظیمات مختص فازهای ساخت یا نصب، به ترتیب از `wafBuildFlags` یا `wafInstallFlags` استفاده کنید.

#### `dontUseWafConfigure` {#dont-use-waf-configure}

وقتی روی true تنظیم شود، از `wafConfigurePhase` ازپیش‌تعریف‌شده استفاده نمی‌کند.

#### `dontUseWafBuild` {#dont-use-waf-build}

وقتی روی true تنظیم شود، از `wafBuildPhase` ازپیش‌تعریف‌شده استفاده نمی‌کند.

#### `dontUseWafInstall` {#dont-use-waf-install}

وقتی روی true تنظیم شود، از `wafInstallPhase` ازپیش‌تعریف‌شده استفاده نمی‌کند.

### متغیرهای مشابه {#waf-hook-similar-variables}

متغیرهای زیر مشابه معادل‌های خود در `stdenv.mkDerivation` هستند.

| متغیر `wafHook`       | معادل `stdenv.mkDerivation` |
|-----------------------|-----------------------------------|
| `wafConfigureFlags`   | `configureFlags`                  |
| `wafConfigureTargets` | `configureTargets`                |
| `wafBuildFlags`       | `buildFlags`                      |
| `wafBuildTargets`     | `buildTargets`                    |
| `wafInstallFlags`     | `installFlags`                    |
| `wafInstallTargets`   | `installTargets`                  |

### متغیرهای مورد پشتیبانی {#waf-hook-honored-variables}

متغیرهای زیر که معمولاً توسط `stdenv.mkDerivation` استفاده می‌شوند، توسط `wafHook` نیز پشتیبانی می‌شوند.

- `prefixKey`
- `enableParallelBuilding`
- `enableParallelInstalling`
