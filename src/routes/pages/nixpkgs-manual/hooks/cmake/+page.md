# <a id="cmake"></a> cmake

فاز پیکربندی پیش‌فرض را برای اجرای دستور CMake بازنویسی می‌کند.

به‌طور پیش‌فرض، ما از تولیدکننده Make در CMake استفاده می‌کنیم.
اما زمانی که Ninja نیز به عنوان یک `nativeBuildInput` در دسترس باشد، این قلاب راه‌اندازی (setup hook) آن را تشخیص داده و از تولیدکننده ninja استفاده می‌کند.

وابستگی‌ها به‌طور خودکار به `CMAKE_PREFIX_PATH` اضافه می‌شوند تا بسته‌ها به‌درستی توسط CMake تشخیص داده شوند.
برخی پرچم‌های اضافی نیز ارسال می‌شوند تا رفتاری مشابه بسته‌های مبتنی بر configure ارائه دهند.

به‌طور پیش‌فرض، ساخت موازی فعال است زیرا CMake تقریباً در همه‌جا از ساخت موازی پشتیبانی می‌کند.

می‌توانید رفتار این قلاب را با مقداردهی `configurePhase` به یک مقدار سفارشی یا با تنظیم `dontUseCmakeConfigure` غیرفعال کنید.

## <a id="cmake-variables-controlling"></a> متغیرهای کنترل‌کننده CMake

### <a id="cmake-exclusive-variables"></a> متغیرهای اختصاصی CMake

#### <a id="cmake-flags"></a> `cmakeFlags`

پرچم‌های ارسالی به `cmake setup` را در طول فاز پیکربندی کنترل می‌کند.

#### <a id="cmake-build-dir"></a> `cmakeBuildDir`

پوشه‌ای که CMake فایل‌های میانجی را در آن قرار می‌دهد.

تنظیم این متغیر می‌تواند برای دیباگ (اشکال‌زدایی) ساخت‌های متعدد CMake در همان پوشه کد منبع مفید باشد، برای مثال هنگام ساخت برای پلتفرم‌های مختلف.
مقادیر متفاوت برای هر ساخت از تداخل فرآورده‌های ساخت با یکدیگر جلوگیری می‌کند.
این تنظیم هنگام اجرای ساخت در یک derivation ایزوله شده (Sandboxed) هیچ اثر ملموسی ندارد.

مقدار پیش‌فرض `build` است.

#### <a id="cmake-build-type"></a> `cmakeBuildType`

نوع ساخت خروجی cmake.

به‌صورت داخلی پرچم cmake مربوط به `CMAKE_BUILD_TYPE` را مقداردهی می‌کند.

مقدار پیش‌فرض `Release` است.

#### <a id="dont-use-cmake-configure"></a> `dontUseCmakeConfigure`

هنگامی که روی true تنظیم شود، از `cmakeConfigurePhase` ازپیش‌تعریف‌شده استفاده نمی‌کند.

## <a id="cmake-ctest"></a> کنترل فراخوانی CTest

به‌طور پیش‌فرض تست‌ها توسط make در [`checkPhase`](#ssec-check-phase) یا توسط [ninja](#ninja) (اگر `ninja` در `nativeBuildInputs` در دسترس باشد) اجرا می‌شوند. تولیدکننده‌های Makefile و Ninja هدف `test` را تولید می‌کنند که در پشت صحنه `ctest` را فراخوانی می‌کند.
این امر ارسال آرگومان‌های اضافی به `ctest` را دشوار می‌سازد، بنابراین می‌توان با افزودن `ctestCheckHook` به `nativeCheckInputs` آن را مستقیماً در `checkPhase` فراخوانی کرد.

### <a id="cmake-ctest-variables"></a> متغیرهای CTest

#### <a id="cmake-ctest-disabled-tests"></a> `disabledTests`

امکان غیرفعال کردن اجرای فهرستی از تست‌ها را فراهم می‌کند. توجه داشته باشید که عبارت‌های باقاعده (regular expressions) توسط `disabledTests` پشتیبانی نمی‌شوند، اما می‌توان آن را با گزینه `--exclude-regex` ترکیب کرد.

#### <a id="cmake-ctest-flags"></a> `ctestFlags`

گزینه‌های اضافی که همراه با `checkFlags` به `ctest` ارسال می‌شوند.
