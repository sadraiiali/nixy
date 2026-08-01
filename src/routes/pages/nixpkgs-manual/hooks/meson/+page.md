# <a id="meson"></a> Meson

[Meson](https://mesonbuild.com/) یک سیستم فراساخت متن‌باز است که با هدف سریع و کاربرپسند بودن طراحی شده است.

در Nixpkgs، ابزار meson همراه با یک setup hook ارائه می‌شود که فازهای پیکربندی، بررسی و نصب را بازنویسی می‌کند.

ابزار meson به عنوان یک سیستم فراساخت، به یک بخش سمت سرور (Backend) همراه نیاز دارد. در بافتار Nixpkgs، بک‌اند همراه معمول [Ninja](#ninja) است که یک setup hook ارائه می‌دهد که فازهای ساخت (Build) و نصب مبتنی بر ninja را ثبت می‌کند.

## <a id="meson-variables-controlling"></a> متغیرهای کنترل‌کننده Meson

### <a id="meson-exclusive-variables"></a> متغیرهای اختصاصی Meson

#### <a id="meson-flags"></a> `mesonFlags`

پرچم‌های پاس‌داده‌شده به `meson setup` را در طول فاز پیکربندی کنترل می‌کند.

#### <a id="meson-build-dir"></a> `mesonBuildDir`

پوشه‌ای که Meson فایل‌های میانجی را در آن قرار می‌دهد.

تنظیم این گزینه می‌تواند برای دیباگ (اشکال‌زدایی) ساخت‌های متعدد Meson در حالی که در همان پوشه کد منبع هستید مفید باشد، برای مثال، هنگام ساخت برای پلتفرم‌های مختلف.
مقادیر متفاوت برای هر ساخت، از تداخل فرآورده‌های ساخت با یکدیگر جلوگیری می‌کند.
این تنظیم هنگام اجرای ساخت در یک derivation ایزوله شده (Sandboxed)، هیچ اثر ملموسی ندارد.

مقدار پیش‌فرض `build` است.

#### <a id="meson-wrap-mode"></a> `mesonWrapMode`

کدام مقدار به عنوان [`-Dwrap_mode=`](https://mesonbuild.com/Builtin-options.html#core-options) پاس داده می‌شود.
در Nixpkgs، مقدار پیش‌فرض `nodownload` است، به طوری که هیچ زیرپروژه‌ای دریافت نخواهد شد (زیرا دسترسی به شبکه در طول استقرار (deployment) در Nixpkgs از قبل غیرفعال شده است).

نکته: Meson امکان پیش-بارگذاری زیرپروژه‌هایی را که در غیر این صورت دریافت می‌شدند، فراهم می‌کند.

#### <a id="meson-build-type"></a> `mesonBuildType`

کدام مقدار به عنوان [`--buildtype`](https://mesonbuild.com/Builtin-options.html#core-options) به `meson setup` در طول فاز پیکربندی پاس داده می‌شود. در Nixpkgs، مقدار پیش‌فرض `plain` است.

#### <a id="meson-auto-features"></a> `mesonAutoFeatures`

کدام مقدار به عنوان [`-Dauto_features=`](https://mesonbuild.com/Builtin-options.html#core-options) به `meson setup` در طول فاز پیکربندی پاس داده می‌شود. در Nixpkgs، مقدار پیش‌فرض `enabled` است، به این معنی که هر ویژگی که توسط اسکریپت‌های meson به عنوان "auto" اعلام شده باشد، فعال خواهد شد.

#### <a id="meson-check-flags"></a> `mesonCheckFlags`

پرچم‌های پاس‌داده‌شده به `meson test` را در طول فاز بررسی کنترل می‌کند.

#### <a id="meson-install-flags"></a> `mesonInstallFlags`

پرچم‌های پاس‌داده‌شده به `meson install` را در طول فاز نصب کنترل می‌کند.

#### <a id="meson-install-tags"></a> `mesonInstallTags`

فهرستی از برچسب‌های نصب که به گزینه خط فرمان Meson یعنی [`--tags`](https://mesonbuild.com/Installing.html#installation-tags) در طول فاز نصب پاس داده می‌شود.

نکته: `mesonInstallTags` باید فهرستی از رشته‌ها باشد که به یک رشته جداشده با ویرگول که برای `--tags` قابل تشخیص است تبدیل می‌شود.
مثال: `mesonInstallTags = [ "emulator" "assembler" ];` به `--tags emulator,assembler` تبدیل خواهد شد.

#### <a id="dont-use-meson-configure"></a> `dontUseMesonConfigure`

وقتی روی true تنظیم شود، از `mesonConfigurePhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

#### <a id="dont-use-meson-check"></a> `dontUseMesonCheck`

وقتی روی true تنظیم شود، از `mesonCheckPhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

#### <a id="dont-use-meson-install"></a> `dontUseMesonInstall`

وقتی روی true تنظیم شود، از `mesonInstallPhase` از‌پیش‌تعریف‌شده استفاده نمی‌کند.

### <a id="meson-honored-variables"></a> متغیرهای مورد پذیرش

متغیرهای زیر که معمولاً توسط `stdenv.mkDerivation` استفاده می‌شوند، توسط setup hook مربوط به Meson پذیرفته می‌شوند.

- `prefixKey`
- `enableParallelBuilding`
- `enableParallelChecking`
