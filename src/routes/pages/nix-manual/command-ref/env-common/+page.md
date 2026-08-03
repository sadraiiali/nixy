# 8.2. متغیرهای محیطی رایج

بیشتر دستورهای Nix متغیرهای محیطی زیر را تفسیر می‌کنند.

## متغیرهای محیطی پیکربندی

متغیرهای محیطی زیر بر نحوه بارگذاری پیکربندی Nix تأثیر می‌گذارند.
برای جزئیات کامل، مستندات [فایل پیکربندی](/pages/nix-manual/command-ref/conf-file#configuration-file) را ببینید.

- <span id="env-NIX_CONF_DIR">[`NIX_CONF_DIR`](#env-NIX_CONF_DIR)</span>

  پوشه پیکربندی سیستم را بازنویسی می‌کند.

- <span id="env-NIX_USER_CONF_FILES">[`NIX_USER_CONF_FILES`](#env-NIX_USER_CONF_FILES)</span>

  مکان‌های فایل پیکربندی کاربر را بازنویسی می‌کند.

- <span id="env-NIX_CONFIG">[`NIX_CONFIG`](#env-NIX_CONFIG)</span>

  تنظیمات پیکربندی را به‌صورت درون‌خطی فراهم می‌کند.

## متغیرهای محیطی تنظیمات انبار

- <span id="env-NIX_IGNORE_SYMLINK_STORE">[`NIX_IGNORE_SYMLINK_STORE`](#env-NIX_IGNORE_SYMLINK_STORE)</span>

  به‌طور معمول، پوشه انبار Nix (معمولاً `/nix/store`) اجازه ندارد شامل هیچ مؤلفه پیوند نمادینی (symlink) باشد. این کار برای جلوگیری از ساخت‌های «ناخالص» انجام می‌شود. سازنده‌ها گاهی اوقات با حل کردن تمام مؤلفه‌های پیوند نمادین، مسیرها را «استانداردسازی» می‌کنند. بنابراین، ساخت‌ها روی ماشین‌های مختلف (با تبدیل شدن `/nix/store` به مکان‌های مختلف) می‌توانند نتایج متفاوتی تولید کنند. این موضوع به‌طور کلی مشکلی ایجاد نمی‌کند، مگر زمانی که ساخت‌ها روی ماشین‌هایی مستقر شوند که در آن‌ها `/nix/store` به شکل متفاوتی حل می‌شود. اگر مطمئن هستید که چنین کاری انجام نخواهید داد، می‌توانید `NIX_IGNORE_SYMLINK_STORE` را روی `1` تنظیم کنید.

  توجه داشته باشید که اگر انبار Nix را پیوند نمادین (symlink) می‌کنید تا بتوانید آن را روی سیستم‌فایلی غیر از سیستم‌فایل ریشه قرار دهید، در لینوکس بهتر است از نقاط اتصال `bind` استفاده کنید، به عنوان مثال:

```shell
  $ mkdir /nix
  $ mount -o bind /mnt/otherdisk/nix /nix
  ```

برای جزئیات، به صفحهٔ راهنمای `mount 8` مراجعه کنید.

- <span id="env-NIX_STORE_DIR">[`NIX_STORE_DIR`](#env-NIX_STORE_DIR)</span>

  محل انبار Nix را بازنویسی می‌کند.
  در یونیکس، مقدار پیش‌فرض `/nix/store` است که در زمان کامپایل توسط گزینهٔ ساخت `libstore:store-dir` تعیین می‌شود.
  در ویندوز، هیچ تنظیماتی در زمان کامپایل وجود ندارد؛ مقدار پیش‌فرض `%PROGRAMDATA%\nix\store` است که در زمان اجرا با استفاده از [پوشهٔ شناخته‌شده‌ی `%PROGRAMDATA%`](#known-folders) تعیین می‌شود.

  به فصل [انواع انبار][Store Types] مراجعه کنید؛ هر انبار دارای یک تنظیمات `store` است که برای مقدار پیش‌فرض خود به این مورد ارجاع می‌دهد.

- <span id="env-NIX_LOG_DIR">[`NIX_LOG_DIR`](#env-NIX_LOG_DIR)</span>

  محل پوشهٔ گزارش‌های Nix را بازنویسی می‌کند.
  در یونیکس، مقدار پیش‌فرض `/nix/var/log/nix` است که در زمان کامپایل توسط گزینهٔ ساخت `log-dir` تعیین می‌شود.
  در ویندوز، هیچ تنظیماتی در زمان کامپایل وجود ندارد؛ مقدار پیش‌فرض `%PROGRAMDATA%\nix\log` است که در زمان اجرا با استفاده از [پوشهٔ شناخته‌شده‌ی `%PROGRAMDATA%`](#known-folders) تعیین می‌شود.

  [انبار محلی][Local Store]، [انبار دائم محلی][Local Daemon Store] و [انبار SSH آزمایشی با سیستم‌فایل مونت‌شده][Experimental SSH Store with filesystem mounted] دارای تنظیمات مختص‌به‌انبار هستند که این مورد را بازنویسی می‌کنند.

- <span id="env-NIX_STATE_DIR">[`NIX_STATE_DIR`](#env-NIX_STATE_DIR)</span>

  محل پوشهٔ وضعیت Nix را بازنویسی می‌کند.
  در یونیکس، مقدار پیش‌فرض `${'{'}localstatedir{'}'}/nix` است که در آن `localstatedir` یک گزینهٔ ساخت در زمان کامپایل است که به طور پیش‌فرض `/nix/var` می‌باشد.
  در ویندوز، هیچ تنظیماتی در زمان کامپایل وجود ندارد؛ مقدار پیش‌فرض `%PROGRAMDATA%\nix\state` است که در زمان اجرا با استفاده از [پوشهٔ شناخته‌شده‌ی `%PROGRAMDATA%`](#known-folders) تعیین می‌شود.

  [انبار محلی][Local Store]، [انبار دائم محلی][Local Daemon Store] و [انبار SSH آزمایشی با سیستم‌فایل مونت‌شده][Experimental SSH Store with filesystem mounted] دارای تنظیمات مختص‌به‌انبار هستند که این مورد را بازنویسی می‌کنند.

- <span id="env-NIX_DAEMON_SOCKET_PATH">[`NIX_DAEMON_SOCKET_PATH`](#env-NIX_DAEMON_SOCKET_PATH)</span>

  مسیر سوکت دامنه یونیکس مورد استفاده برای ارتباط با دائم (daemon) Nix را بازنویسی می‌کند.
  به طور پیش‌فرض `daemon-socket/socket` در داخل پوشه وضعیت است (نگاه کنید به [`NIX_STATE_DIR`](#env-NIX_STATE_DIR)).

  برای جزئیات درباره نحوه حل مسیر سوکت، به مستندات [انبار دائم محلی][Local Daemon Store] مراجعه کنید.

- <span id="env-TMPDIR">[`TMPDIR`](#env-TMPDIR)</span>

  از پوشه مشخص‌شده برای ذخیره فایل‌های موقت استفاده کنید. به طور خاص،
  این شامل پوشه‌های ساخت موقت می‌شود؛ این پوشه‌ها می‌توانند مقدار قابل توجهی
  از فضای دیسک را اشغال کنند. مقدار پیش‌فرض `/tmp` است.

- <span id="env-NIX_REMOTE">[`NIX_REMOTE`](#env-NIX_REMOTE)</span>

  تنظیمات [`store`](/pages/nix-manual/command-ref/conf-file#conf-store) را بازنویسی می‌کند.

[Store Types]: /pages/nix-manual/store/types
[store URL format]: /pages/nix-manual/store/types#store-url-format
[Local Store]: /pages/nix-manual/store/types/local-store
[Local Daemon Store]: /pages/nix-manual/store/types/local-daemon-store
[Experimental SSH Store with filesystem mounted]: /pages/nix-manual/store/types/experimental-ssh-store-with-filesystem-mounted
## تنظیمات ارزیاب زبان Nix

- <span id="env-NIX_SHOW_STATS">[`NIX_SHOW_STATS`](#env-NIX_SHOW_STATS)</span>

  اگر روی `1` تنظیم شود، Nix برخی آمارهای ارزیابی، مانند
  تعداد مقادیر تخصیص‌یافته را چاپ خواهد کرد.

- <span id="env-NIX_COUNT_CALLS">[`NIX_COUNT_CALLS`](#env-NIX_COUNT_CALLS)</span>

  اگر روی `1` تنظیم شود، Nix تعداد دفعات فراخوانی توابع را در طول
  ارزیابی عبارت Nix چاپ خواهد کرد. این کار برای تحلیل کارایی (profiling) عبارت‌های Nix شما مفید است.

- <span id="env-GC_INITIAL_HEAP_SIZE">[`GC_INITIAL_HEAP_SIZE`](#env-GC_INITIAL_HEAP_SIZE)</span>

اگر Nix به گونه‌ای پیکربندی شده باشد که از جمع‌کننده‌ی زباله Boehm استفاده کند، این متغیر اندازه اولیهٔ هیپ (heap) را بر حسب بایت تنظیم می‌کند. مقدار پیش‌فرض آن ۳۸۴ مگابایت (MiB) است. تنظیم کردن آن روی یک مقدار پایین، مصرف حافظه را کاهش می‌دهد، اما به دلیل سربار جمع‌آوری زباله (garbage collection)، زمان اجرا را افزایش خواهد داد.

- <span id="env-NIX_PATH">[`NIX_PATH`](#env-NIX_PATH)</span>

  فهرستی جداشده با دو نقطه (کولون) از ورودی‌های مسیر جستجو که برای حل [مسیرهای جستجو](/pages/nix-manual/language/constructs/lookup-path) استفاده می‌شوند.

  این متغیر محیطی، مقدار [تنظیم پیکربندی `nix-path`](/pages/nix-manual/command-ref/conf-file#conf-nix-path) را بازنویسی می‌کند.

  می‌توان آن را با استفاده از [گزینهٔ `-I`](/pages/nix-manual/command-ref/opt-common#opt-I) گسترش داد.

  > **مثال**
  >

> ```bash
> $ export NIX_PATH=/home/eelco/Dev:nixos-config=/etc/nixos
> ```

اگر `NIX_PATH` روی یک رشته‌ی خالی تنظیم شود، حل کردن مسیرهای جستجو همیشه با شکست مواجه خواهد شد.

> **مثال**
>

> ```bash
> $ NIX_PATH= nix-instantiate --eval '<nixpkgs>'
> error: file 'nixpkgs' was not found in the Nix search path (add it using $NIX_PATH or -I)
> ```

## پوشه‌های کاربر

Nix از **پیکربندی**، **وضعیت** و **کش** مختص هر کاربر پشتیبانی می‌کند.
متغیرهای محیطی زیر مکان این پوشه‌ها را بازنشانی می‌کنند:

- [پوشه پیکربندی کاربر]<a id="user-conf-dir"></a>: [`NIX_CONFIG_HOME`]<a id="env-NIX_CONFIG_HOME"></a>
- پوشه وضعیت کاربر: [`NIX_STATE_HOME`]<a id="env-NIX_STATE_HOME"></a>
- پوشه کش کاربر: [`NIX_CACHE_HOME`]<a id="env-NIX_CACHE_HOME"></a>

هنگامی که این موارد تنظیم نشده باشند، مقادیر پیش‌فرض به پلتفرم بستگی دارند:

- در سیستم‌های یونیکس، [پوشه‌های پایه XDG](#xdg-base-directories): `$XDG_CONFIG_HOME/nix`، `$XDG_STATE_HOME/nix`، `$XDG_CACHE_HOME/nix`
- در ویندوز، [پوشه‌های شناخته‌شده ویندوز](#known-folders): `%APPDATA%\nix\config`، `%LOCALAPPDATA%\nix\state`، `%LOCALAPPDATA%\nix\cache`

[`use-xdg-base-directories`]: /pages/nix-manual/command-ref/conf-file#conf-use-xdg-base-directories
به دلایل سازگاری با نسخه‌های پیشین، دستورات قدیمی Nix (مانند `nix-env`، `nix-channel`) برخلاف این پوشه‌ها، از فایل‌های نقطه‌ای (dotfiles) در `$HOME` استفاده می‌کنند، مگر اینکه [`use-xdg-base-directories`] فعال شده باشد.
[دستورات جدید Nix](/pages/nix-manual/command-ref/new-cli/nix) (آزمایشی) به‌طور پیش‌فرض از پوشه‌های مناسب استفاده می‌کنند.

هنگامی که [`use-xdg-base-directories`] فعال است، پوشه پیکربندی به شکل زیر تحلیل می‌شود:

1. متغیر `$NIX_CONFIG_HOME`، در صورتی که تعریف شده باشد
2. در غیر این صورت، مقدار پیش‌فرض پلتفرم (به‌عنوان‌مثال `$XDG_CONFIG_HOME/nix` در یونیکس)

همین روند برای پوشه‌های وضعیت و کش نیز برقرار است.

## متغیرهای محیطی متفرقه

- <span id="env-IN_NIX_SHELL">[`IN_NIX_SHELL`](#env-IN_NIX_SHELL)</span>

  نشانگری که مشخص می‌کند آیا محیط فعلی توسط `nix-shell` راه‌اندازی شده است یا خیر. این متغیر می‌تواند مقادیر `pure` یا `impure` داشته باشد.

## پیوست: قراردادهای مخصوص سیستم‌عامل

این اطلاعات مختص Nix نیستند، اما در بالا به آن‌ها ارجاع داده شده است.

### <a id="xdg-base-directories"></a> یونیکس: پوشه‌های پایه XDG

[مشخصات پوشه پایه XDG] مکان‌های استانداردی را برای فایل‌های پیکربندی، وضعیت و کش مختص کاربر در سیستم‌های یونیکس تعریف می‌کند.

[مشخصات پوشه پایه XDG]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

متغیرهای محیطی زیر مورد استفاده قرار می‌گیرند:

- [`XDG_CONFIG_HOME`]<a id="env-XDG_CONFIG_HOME"></a> (پیش‌فرض `~/.config`)
- [`XDG_STATE_HOME`]<a id="env-XDG_STATE_HOME"></a> (پیش‌فرض `~/.local/state`)
- [`XDG_CACHE_HOME`]<a id="env-XDG_CACHE_HOME"></a> (پیش‌فرض `~/.cache`)
- [`XDG_CONFIG_DIRS`]<a id="env-XDG_CONFIG_DIRS"></a> (پیش‌فرض `/etc/xdg`) — فهرستی جداشده با دونقطه از پوشه‌های پایه پیکربندی اضافی که پس از `XDG_CONFIG_HOME` جستجو می‌شوند

### <a id="known-folders"></a> ویندوز: پوشه‌های شناخته‌شده

در ویندوز، [پوشه‌های شناخته‌شده][windows-known-folders] مکان‌های استانداردی را برای داده‌های برنامه در ویندوز فراهم می‌کنند.

[windows-known-folders]: https://learn.microsoft.com/en-us/windows/win32/shell/known-folders

پوشه‌های مرتبط عبارتند از:

- [`%APPDATA%`]<a id="env-APPDATA"></a> — داده‌های برنامه رومینگ مختص هر کاربر
- [`%LOCALAPPDATA%`]<a id="env-LOCALAPPDATA"></a> — داده‌های برنامه محلی مختص هر کاربر
- [`%PROGRAMDATA%`]<a id="env-PROGRAMDATA"></a> — داده‌های برنامه در سطح سیستم
