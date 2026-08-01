# <a id="versioncheckhook"></a> versionCheckHook

این قلاب یک `versionCheckPhase` به [`preInstallCheckHooks`](#ssec-installCheck-phase) اضافه می‌کند که برنامه اصلی derivation را با آرگومان `--help` یا `--version` اجرا کرده و بررسی می‌کند که رشته `$`در آن خروجی یافت شود. اگر این بررسی شکست بخورد، کل ساخت با شکست مواجه خواهد شد. _(یک گزینه ملایم‌تر [`testers.testVersion`](#tester-testVersion) است.)_

نحوه استفاده از آن به این صورت است:

```nix
{
  lib,
  stdenv,
  versionCheckHook,
  # ...
}:

stdenv.mkDerivation (finalAttrs: {
  # ...

  nativeInstallCheckInputs = [ versionCheckHook ];
  doInstallCheck = true;

  # ...
})
```

توجه داشته باشید که برای [`buildPythonPackage`](#buildpythonpackage-function) و [`buildPythonApplication`](#buildpythonapplication-function)، `doInstallCheck` به طور پیش‌فرض فعال است.

این کار در یک محیط تمیز (با استفاده از `env --ignore-environment`) انجام می‌شود و خروجی‌های `stdout` و `stderr` دستور را برای یافتن رشته `$`بررسی می‌کند. خروجی دریافت‌شده را در لاگ ساخت به شما گزارش می‌دهد و اگر نتواند`$`را پیدا کند، ساخت با شکست مواجه خواهد شد.

متغیرهایی که این فاز کنترل می‌کند عبارت‌اند از:

-`dontVersionCheck`: افزودن این قلاب به [`preInstallCheckHooks`](#ssec-installCheck-phase) را غیرفعال می‌کند. زمانی مفید است که بخواهید توابع Bash قلاب را بارگذاری کنید، اما آن‌ها را به شیوهٔ دیگری اجرا نمایید.
- `versionCheckProgram`: مسیر کامل برنامه‌ای که باید رشته `$`را چاپ کند. به طور پیش‌فرض به ترتیب از اولین مقدار غیرخالی`$binary` در میان `$`و`$`استفاده می‌کند تا تقریباً`${'{'}'{'{'}'{'}'}placeholder "out"{'{'}'{'}'}'{'}'}/bin/$binary` را بسازد. مقدار `$`از`meta.mainProgram` می‌آید و معمولاً نیازی نیست به طور صریح تنظیم شود. هنگام تنظیم `versionCheckProgram`، استفاده مستقیم از `$out` کار نخواهد کرد، زیرا متغیرهای محیطی از این متغیر توسط قلاب بازگشایی نمی‌شوند. بنابراین استفاده از `placeholder "out"` اجتانب‌ناپذیر است.
- `versionCheckProgramArg`: آرگومانی که باید به `versionCheckProgram` پاس داده شود. در صورت تعریف‌نشدن، قلاب ابتدا `--version` و سپس `--help` را امتحان می‌کند. مثال‌ها: `version`، `-V`، `-v`.
- `versionCheckKeepEnvironment`: فهرستی از متغیرهای محیطی برای حفظ و پاس دادن به دستور. تنها متغیرهایی باید به این فهرست اضافه شوند که واقعاً برای کارکرد دستور نسخه مورد نیاز هستند. اگر امکان‌پذیر نیست که همه این متغیرهای محیطی را به طور صریح فهرست کنید، می‌توانید این پارامتر را روی مقدار خاص `"*"` تنظیم کنید تا پرچم `--ignore-environment` غیرفعال شده و در نتیجه تمام متغیرهای محیطی حفظ شوند.
- `preVersionCheck`: قلابی که پیش از انجام بررسی اجرا می‌شود.
- `postVersionCheck`: قلابی که پس از انجام بررسی اجرا می‌شود.

این بررسی فرض می‌کند که فایل اجرایی _خودکفا (hermetic)_ است. اگر متغیرهای محیطی مانند `PATH` یا `HOME` برای کارکرد برنامه مورد نیاز باشند، در حال حاضر [`testers.testVersion`](#tester-testVersion) جایگزین بهتری است.
