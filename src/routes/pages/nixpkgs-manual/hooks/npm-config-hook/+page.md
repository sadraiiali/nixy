# <a id="npm-config-hook"></a> npmHooks.npmConfigHook

هوک برای پیکربندی بسته‌هایی که از npm استفاده می‌کنند.
اصالتاً برای یک محیط چندزبانه ساخته شده است.

## <a id="npm-config-hook-snippet"></a> نمونه‌ها

[](#npm-build-hook-example-snippet)

## <a id="npm-config-hook-variables"></a> متغیرهای کنترل‌کننده `npmConfigHook`

### <a id="npm-config-hook-exclusive-variables"></a> متغیرهای اختصاصی `npmConfigHook`

#### <a id="npm-config-hook-deps"></a> `npmDeps`

درایویشنی که شامل وابستگی‌های بسته npm است.
معمولاً با `fetchNpmDeps` ساخته می‌شود.
این صفت الزامی است، در غیر این صورت هوک فرآیند ساخت را متوقف خواهد کرد.

#### <a id="npm-config-hook-writable-cache"></a> `makeCacheWritable`

اینکه آیا کش وابستگی‌ها پیش از نصب وابستگی‌ها قابل نوشتن شود یا خیر.
این گزینه را تنظیم نکنید مگر اینکه npm تلاش کند در پوشه کش بنویسد.

#### <a id="npm-config-hook-install-flags"></a> `npmInstallFlags`

پرچم‌هایی که جهت نصب وابستگی‌ها در محیط ساخت به فراخوانی `npm ci` پاس داده می‌شوند.
مقدار پیش‌فرض `--ignore-scripts` است که قابل حذف نیست.
این متغیر هیچ کنترلی روی `npmInstallHook` ندارد.

#### <a id="npm-config-hook-rebuild-flags"></a> `npmRebuildFlags`

پرچم‌هایی که پس از نصب وابستگی‌ها در محیط، به دستور `npm rebuild` پاس داده می‌شوند.

### <a id="npm-config-hook-honored-variables"></a> متغیرهای پذیرفته‌شده

متغیرهای زیر توسط `npmConfigHook` پشتیبانی و رعایت می‌شوند.

- [`npmWorkspace`](#javascript-buildNpmPackage-npmWorkspace)
- [`npmFlags`](#javascript-buildNpmPackage-npmFlags)
- `npmRoot`
