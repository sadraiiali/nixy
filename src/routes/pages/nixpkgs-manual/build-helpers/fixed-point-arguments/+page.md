# <a id="chap-build-helpers-finalAttrs"></a> آرگومان‌های نقطه ثابت کمک‌رسان‌های ساخت

`stdenv.mkDerivation` همچنین به جای یک مجموعه ویژگی ساده، یک [تابع نقطه ثابت](#function-library-lib.fixedPoints.fix) را می‌پذیرد:

```nix
{
  stdenv,
  fetchurl,
}:
stdenv.mkDerivation (finalAttrs: {
  pname = "hello";
  version = "2.12";

  src = fetchurl {
    url = "mirror://gnu/hello/hello-${finalAttrs.version}.tar.gz";
    hash = "sha256-...";
  };
})
```

ورودی تابع، که طبق مرسوم `finalAttrs` نامیده می‌شود، وضعیت نهایی مجموعه ویژگی است. در اینجا `src` به جای تکرار رشته نسخه، `finalAttrs.version` را می‌خواند. گفته می‌شود یک کمک‌رسان ساخت مانند این، **آرگومان‌های نقطه ثابت** را می‌پذیرد.

صفاتی که از طریق `finalAttrs` به یکدیگر ارجاع می‌دهند، هنگام تغییر هر یک از آن‌ها با [`overrideAttrs`](#sec-pkg-overrideAttrs) درست باقی می‌مانند، زیرا همگی به مقادیر نهایی محاسبات نقطه ثابت دسترسی دارند.

`rec` نمی‌تواند این کار را انجام دهد: خودارجاعی‌های آن در زمان تعریف مجموعه ثابت می‌شوند و بازنشانی‌های بعدی را نادیده می‌گیرند.
برای سازوکار زیرین، [مجموعه‌های بازگشتی](/pages/nix-manual/language/syntax#recursive-sets) را ببینید.

## <a id="sec-build-helper-extendMkDerivation"></a> تعریف یک کمک‌رسان ساخت با `lib.extendMkDerivation`

از [`lib.customisation.extendMkDerivation`](#function-library-lib.customisation.extendMkDerivation) برای تعریف یک کمک‌رسان ساخت با پشتیبانی از نقطه ثابت بر اساس یک کمک‌رسان موجود استفاده کنید.
آرگومان `extendDrvArgs` آن، یک اورلی صفات شبیه به [`&lt;pkg&gt;.overrideAttrs`](#sec-pkg-overrideAttrs) می‌گیرد.

علاوه بر بازنشانی، `lib.extendMkDerivation` از `excludeDrvArgNames` نیز پشتیبانی می‌کند تا در صورت تمایل، برخی از آرگومان‌ها را در آرگومان‌های نقطه ثابت ورودی از انتقال به کمک‌رسان ساخت پایه (که به صورت `constructDrv` مشخص می‌شود) مستثنی کند.

<a id="ex-build-helpers-extendMkDerivation"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # مثال `mkLocalDerivation` - یک کمک‌رسان ساخت روی `mkDerivation`
>
> یک کمک‌رسان ساخت به نام `mkLocalDerivation` تعریف کنید که به‌طور پیش‌فرض بدون استفاده از جایگزین‌ها به‌صورت محلی عمل ساخت را انجام دهد.
>
> از `lib.extendMkDerivation` استفاده کنید:
>

> ```nix
> {
>   lib,
>   stdenv,
> }:
> lib.extendMkDerivation {
>   constructDrv = stdenv.mkDerivation;
>   excludeDrvArgNames = [
>     # Don't pass specialArg into mkDerivation.
>     "specialArg"
>   ];
>   extendDrvArgs =
>     finalAttrs:
>     {
>       preferLocalBuild ? true,
>       allowSubstitute ? false,
>       specialArg ? (_: false),
>       ...
>     }@args:
>     {
>       # Arguments to pass
>       inherit preferLocalBuild allowSubstitute;
>       # Some expressions involving specialArg
>       greeting = if specialArg "hi" then "hi" else "hello";
>     };
> }
> ```

برای اعمال تغییرات اضافی روی درایویشن حاصل، `transformDrv` را به `lib.extendMkDerivation` پاس دهید:

```nix
lib.customisation.extendMkDerivation { transformDrv = drv: /...; }
```

ایجاد یک derivation پوشش‌دهنده در اطراف یک derivation دیگر با استفاده از `transformDrv`

پوشش‌دهنده به آرگومان‌های اصلی دسترسی دارد.

<a id="ex-build-helpers-extendMkDerivation-transformDrv-wrapper"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # تعریف یک کمک‌رسان ساخت سفارشی که بارگیری و ساخت را انجام می‌دهد
>

> ```nix
> {
>   lib,
>   stdenvNoCC,
>   cacert,
>   configure-example,
>   download-example,
> }:
>
> lib.extendMkDerivation {
>   constructDrv = stdenvNoCC.mkDerivation;
>
>   excludeDrvArgNames = [
>     "bar"
>   ];
>
>   extendDrvArgs =
>     finalAttrs:
>     {
>       bar,
>       foo,
>       hash ? "",
>       ...
>     }@args:
>     {
>       inherit hash;
>       nativeBuildInputs = args.nativeBuildInputs or [ ] ++ [
>         cacert
>         download-example
>       ];
>       buildPhase = ''
>         runHook preBuild
>         download-example --foo="$foo" --out="$out"
>         runHook postBuild
>       '';
>       impureEnvVars = lib.fetchers.proxyImpureEnvVars;
>       outputHash = if finalAttrs.hash != "" then finalAttrs.hash else lib.fakeHash;
>       outputHashFormat = "recursive";
>       passthru = args.passthru or { } // {
>         inherit bar;
>       };
>     };
>
>   transformDrv =
>     unwrapped:
>     stdenvNoCC.mkDerivation (finalAttrs: {
>       name = finalAttrs.src.name + "-wrapped";
>       src = unwrapped;
>       nativeBuildInputs = [
>         configure-example
>       ];
>       inherit (unwrapped) bar;
>       buildPhase = ''
>         runHook preBuild
>         configure-example --bar="$bar"
>         runHook postBuild
>       '';
>     });
> }
> ```
