# udevCheckHook {#udevcheckhook}

derivation / اشتقاق ساخت `udevCheckHook` مقدار `udevCheckPhase` را به [`preInstallCheckHooks`](#ssec-installCheck-phase) اضافه می‌کند، که همه قوانین udev را در تمامی خروجی‌ها پیدا کرده و آن‌ها را با استفاده از `udevadm verify --resolve-names=never --no-style` راستی‌آزمایی می‌کند. این قلاب باید در هر بسته‌ای که دارای خروجی‌های قوانین udev است استفاده شود تا اطمینان حاصل شود که قوانین معتبر هستند و معتبر باقی می‌مانند.

این قلاب در `installCheckPhase` اجرا می‌شود و برای این‌که اثر داشته باشد نیازمند فعال بودن `doInstallCheck` است:
```nix
{
  lib,
  stdenv,
  udevCheckHook,
  # ...
}:

stdenv.mkDerivation (finalAttrs: {
  # ...

  nativeInstallCheckInputs = [ udevCheckHook ];
  doInstallCheck = true;

  # ...
})
```
توجه داشته باشید که برای [`buildPythonPackage`](#buildpythonpackage-function) و [`buildPythonApplication`](#buildpythonapplication-function)، گزینه‌ی `doInstallCheck` به‌طور پیش‌فرض فعال است.

تمام خروجی‌ها برای مسیرهای `/{etc,lib}/udev/rules.d` خود اسکن می‌شوند.
اگر هیچ خروجی قانونی یافت نشود، قلاب عملاً هیچ کاری انجام نمی‌دهد.

قلاب `udevCheckHook` یک وابستگی به `systemdMinimal` اضافه می‌کند.
این قلاب به‌طور داخلی مشروط به پشتیبانی `hostPlatform` از udev و توانایی `buildPlatform` برای اجرای `udevadm` است.
این قلاب در مواضعی که استفاده می‌شود، نیازی به بررسی‌های صریح پلتفرم ندارد.

این قلاب را می‌توان با استفاده از `dontUdevCheck` غیرفعال کرد، که این کار زمانی ضروری است که بخواهید در `installCheckPhase` روی بسته‌ای با خروجی‌های قانون udev خراب، وظیفه‌ی دیگری را اجرا کنید.
