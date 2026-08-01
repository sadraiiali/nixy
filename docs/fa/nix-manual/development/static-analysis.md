# تحلیل ایستا

نیکس برای تحلیل ایستای کد C++ از [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) استفاده می‌کند.
این کار به شناسایی اشکال‌ها، اعمال استانداردهای کدنویسی و حفظ کیفیت کد کمک می‌کند.

## اجرای محلی clang-tidy

برای اجرای clang-tidy روی کل پایگاه‌کد در شل توسعه:

```console
$ nix develop .#native-clangStdenv
$ configurePhase
$ meson compile -C build clang-tidy
```

این کار تمامی فایل‌های کدهای منبع C++ را تحلیل کرده و هرگونه هشدار را گزارش می‌کند.

برای اعمال خودکار اصلاحات مربوط به هشدارهای خاص:

```console
$ meson compile -C build clang-tidy-fix
```

> **هشدار**
>
> پیش از کامیت کردن، تغییرات را بررسی کنید، زیرا اصلاحات خودکار ممکن است همیشه درست نباشند.

## ادغام CI

ابزار clang-tidy به‌طور خودکار در هر پول ریکوئست (pull request) از طریق GitHub Actions اجرا می‌شود.
کار CI عبارت `.#hydraJobs.clangTidy.x86_64-linux` را می‌سازد که کارهای زیر را انجام می‌دهد:

1. تمام کامپوننت‌ها را در حالت دیباگ (برای کامپایل سریع‌تر) می‌سازد.
2. ابزار clang-tidy را روی هر کامپوننت اجرا می‌کند.
3. اگر هرگونه هشداری پیدا شود، با خطا مواجه می‌شود (هشدارها به‌عنوان خطا در نظر گرفته می‌شوند).

## پیکربندی

پیکربندی clang-tidy در فایل `.clang-tidy` در ریشه مخزن قرار دارد (که یک پیوند نمادین از `nix-meson-build-support/common/clang-tidy/.clang-tidy` است).

### سرکوب هشدارها

اگر یک هشدار مثبت کاذب (false positive) باشد، می‌توانید آن را به چندین روش سرکوب کنید:

1. **سرکوب درون‌خطی** (برای موارد خاص ترجیح داده می‌شود):
```cpp
   // NOLINTBEGIN(bugprone-some-check)
   ... code ...
   // NOLINTEND(bugprone-some-check)
   ```
یا برای یک خط تکی:
```cpp
   int x = something(); // NOLINT(bugprone-some-check)
   ```

2. **فایل پیکربندی** (برای غیرفعال‌سازی در سطح کل پروژه):
   این بررسی را به فهرست غیرفعال‌شده در `.clang-tidy` اضافه کنید:
```yaml
   Checks:
     - -bugprone-some-check  # Reason for disabling
   ```

3. **بررسی گزینه‌ها** (برای پیکربندی رفتار بررسی):
```yaml
   CheckOptions:
     bugprone-reserved-identifier.AllowedIdentifiers: '__some_identifier'
   ```

### افزودن بررسی‌های جدید

برای فعال کردن بررسی‌های اضافی:

1. فایل `nix-meson-build-support/common/clang-tidy/.clang-tidy` را ویرایش کنید.
2. بررسی مورد نظر را به فهرست `Checks` اضافه کنید.
3. ابزار `clang-tidy` را به صورت محلی اجرا کنید تا تأثیر آن را ببینید.
4. هرگونه هشدار جدید را برطرف کنید یا در صورت نیاز، زیرمجموعه بررسی‌های خاصی را غیرفعال کنید.

## افزونه سفارشی clang-tidy

پروژه Nix شامل زیرساختی برای بررسی‌های سفارشی `clang-tidy` در پوشهٔ `src/clang-tidy-plugin/` است.
این بررسی‌ها می‌توانند الگوهای کدنویسی مخصوص Nix را اعمال کنند که توسط بررسی‌های استاندارد `clang-tidy` پوشش داده نمی‌شوند.

برای افزودن یک بررسی سفارشی جدید:

1. پیاده‌سازی بررسی را در `src/clang-tidy-plugin/` اضافه کنید.
2. آن را در `nix-clang-tidy-checks.cc` ثبت کنید.
3. آن را در فایل `.clang-tidy` با پیشوند `nix-` فعال کنید.
