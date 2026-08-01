# <a id="waf-hook"></a> wafHook

[Waf](https://waf.io) یک سیستم ساخت نرم‌افزار مبتنی بر پایتون است.

در Nixpkgs، `wafHook` فازهای پیش‌فرض پیکربندی، ساخت و نصب را بازنویسی می‌کند.

## <a id="waf-hook-variables-controlling"></a> متغیرهای کنترل‌کننده wafHook

### <a id="waf-hook-exclusive-variables"></a> متغیرهای اختصاصی `wafHook`

متغیرهای زیر اختصاصی `wafHook` هستند.

#### <a id="waf-path"></a> `wafPath`

محل ابزار `waf`. مقدار پیش‌فرض آن `./waf` است تا پروژه‌های نرم‌افزاری که آن را مستقیماً درون درخت‌های کد منبع خود شامل شده‌اند پشتیبانی شوند.

اگر فایلی که `wafPath` به آن اشاره می‌کند وجود نداشته باشد، از `waf` ارائه‌شده توسط Nixpkgs استفاده خواهد شد.

#### <a id="waf-flags"></a> `wafFlags`

پرچم‌های ارسال‌شده به ابزار waf را در طول فازهای ساخت و نصب کنترل می‌کند. برای تنظیمات مختص فازهای ساخت یا نصب، به ترتیب از `wafBuildFlags` یا `wafInstallFlags` استفاده کنید.

#### <a id="dont-use-waf-configure"></a> `dontUseWafConfigure`

وقتی روی true تنظیم شود، از `wafConfigurePhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

#### <a id="dont-use-waf-build"></a> `dontUseWafBuild`

وقتی روی true تنظیم شود، از `wafBuildPhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

#### <a id="dont-use-waf-install"></a> `dontUseWafInstall`

وقتی روی true تنظیم شود، از `wafInstallPhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

### <a id="waf-hook-similar-variables"></a> متغیرهای مشابه

متغیرهای زیر مشابه معادل‌های خود در `stdenv.mkDerivation` هستند.

| متغیر `wafHook`       | معادل `stdenv.mkDerivation` |
|-----------------------|-----------------------------------|
| `wafConfigureFlags`   | `configureFlags`                  |
| `wafConfigureTargets` | `configureTargets`                |
| `wafBuildFlags`       | `buildFlags`                      |
| `wafBuildTargets`     | `buildTargets`                    |
| `wafInstallFlags`     | `installFlags`                    |
| `wafInstallTargets`   | `installTargets`                  |

### <a id="waf-hook-honored-variables"></a> متغیرهای مورد پشتیبانی

متغیرهای زیر که معمولاً توسط `stdenv.mkDerivation` استفاده می‌شوند، توسط `wafHook` نیز پشتیبانی می‌شوند.

- `prefixKey`
- `enableParallelBuilding`
- `enableParallelInstalling`
