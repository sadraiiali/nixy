# Meson {#meson}

[Meson](https://mesonbuild.com/) یک سیستم فراساخت متن‌باز است که با هدف سریع و کاربرپسند بودن طراحی شده است.

در Nixpkgs، ابزار meson همراه با یک setup hook ارائه می‌شود که فازهای پیکربندی، بررسی و نصب را بازنویسی می‌کند.

ابزار meson به عنوان یک سیستم فراساخت، به یک بخش سمت سرور (Backend) همراه نیاز دارد. در بافتار Nixpkgs، بک‌اند همراه معمول [Ninja](#ninja) است که یک setup hook ارائه می‌دهد که فازهای ساخت (Build) و نصب مبتنی بر ninja را ثبت می‌کند.

## متغیرهای کنترل‌کننده Meson {#meson-variables-controlling}

### متغیرهای اختصاصی Meson {#meson-exclusive-variables}

#### `mesonFlags` {#meson-flags}

پرچم‌های پاس‌داده‌شده به `meson setup` را در طول فاز پیکربندی کنترل می‌کند.

#### `mesonBuildDir` {#meson-build-dir}

پوشه‌ای که Meson فایل‌های میانجی را در آن قرار می‌دهد.

تنظیم این گزینه می‌تواند برای دیباگ (اشکال‌زدایی) ساخت‌های متعدد Meson در حالی که در همان پوشه کد منبع هستید مفید باشد، برای مثال، هنگام ساخت برای پلتفرم‌های مختلف.
مقادیر متفاوت برای هر ساخت، از تداخل فرآورده‌های ساخت با یکدیگر جلوگیری می‌کند.
این تنظیم هنگام اجرای ساخت در یک derivation ایزوله شده (Sandboxed)، هیچ اثر ملموسی ندارد.

مقدار پیش‌فرض `build` است.

#### `mesonWrapMode` {#meson-wrap-mode}

کدام مقدار به عنوان [`-Dwrap_mode=`](https://mesonbuild.com/Builtin-options.html#core-options) پاس داده می‌شود.
در Nixpkgs، مقدار پیش‌فرض `nodownload` است، به طوری که هیچ زیرپروژه‌ای دریافت نخواهد شد (زیرا دسترسی به شبکه در طول استقرار (deployment) در Nixpkgs از قبل غیرفعال شده است).

نکته: Meson امکان پیش-بارگذاری زیرپروژه‌هایی را که در غیر این صورت دریافت می‌شدند، فراهم می‌کند.

#### `mesonBuildType` {#meson-build-type}

کدام مقدار به عنوان [`--buildtype`](https://mesonbuild.com/Builtin-options.html#core-options) به `meson setup` در طول فاز پیکربندی پاس داده می‌شود. در Nixpkgs، مقدار پیش‌فرض `plain` است.

#### `mesonAutoFeatures` {#meson-auto-features}

کدام مقدار به عنوان [`-Dauto_features=`](https://mesonbuild.com/Builtin-options.html#core-options) به `meson setup` در طول فاز پیکربندی پاس داده می‌شود. در Nixpkgs، مقدار پیش‌فرض `enabled` است، به این معنی که هر ویژگی که توسط اسکریپت‌های meson به عنوان "auto" اعلام شده باشد، فعال خواهد شد.

#### `mesonCheckFlags` {#meson-check-flags}

پرچم‌های پاس‌داده‌شده به `meson test` را در طول فاز بررسی کنترل می‌کند.

#### `mesonInstallFlags` {#meson-install-flags}

پرچم‌های پاس‌داده‌شده به `meson install` را در طول فاز نصب کنترل می‌کند.

#### `mesonInstallTags` {#meson-install-tags}

فهرستی از برچسب‌های نصب که به گزینه خط فرمان Meson یعنی [`--tags`](https://mesonbuild.com/Installing.html#installation-tags) در طول فاز نصب پاس داده می‌شود.

نکته: `mesonInstallTags` باید فهرستی از رشته‌ها باشد که به یک رشته جداشده با ویرگول که برای `--tags` قابل تشخیص است تبدیل می‌شود.
مثال: `mesonInstallTags = [ "emulator" "assembler" ];` به `--tags emulator,assembler` تبدیل خواهد شد.

#### `dontUseMesonConfigure` {#dont-use-meson-configure}

وقتی روی true تنظیم شود، از `mesonConfigurePhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

#### `dontUseMesonCheck` {#dont-use-meson-check}

وقتی روی true تنظیم شود، از `mesonCheckPhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

#### `dontUseMesonInstall` {#dont-use-meson-install}

وقتی روی true تنظیم شود، از `mesonInstallPhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

### متغیرهای مورد پذیرش {#meson-honored-variables}

متغیرهای زیر که معمولاً توسط `stdenv.mkDerivation` استفاده می‌شوند، توسط setup hook مربوط به Meson پذیرفته می‌شوند.

- `prefixKey`
- `enableParallelBuilding`
- `enableParallelChecking`
