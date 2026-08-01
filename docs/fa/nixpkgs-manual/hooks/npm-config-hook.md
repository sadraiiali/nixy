# npmHooks.npmConfigHook {#npm-config-hook}

هوک برای پیکربندی بسته‌هایی که از npm استفاده می‌کنند.
اصالتاً برای یک محیط چندزبانه ساخته شده است.

## نمونه‌ها {#npm-config-hook-snippet}

[](#npm-build-hook-example-snippet)

## متغیرهای کنترل‌کننده `npmConfigHook` {#npm-config-hook-variables}

### متغیرهای اختصاصی `npmConfigHook` {#npm-config-hook-exclusive-variables}

#### `npmDeps` {#npm-config-hook-deps}

درایویشنی که شامل وابستگی‌های بسته npm است.
معمولاً با `fetchNpmDeps` ساخته می‌شود.
این صفت الزامی است، در غیر این صورت هوک فرآیند ساخت را متوقف خواهد کرد.

#### `makeCacheWritable` {#npm-config-hook-writable-cache}

اینکه آیا کش وابستگی‌ها پیش از نصب وابستگی‌ها قابل نوشتن شود یا خیر.
این گزینه را تنظیم نکنید مگر اینکه npm تلاش کند در پوشه کش بنویسد.

#### `npmInstallFlags` {#npm-config-hook-install-flags}

پرچم‌هایی که جهت نصب وابستگی‌ها در محیط ساخت به فراخوانی {command}`npm ci` پاس داده می‌شوند.
مقدار پیش‌فرض `--ignore-scripts` است که قابل حذف نیست.
این متغیر هیچ کنترلی روی `npmInstallHook` ندارد.

#### `npmRebuildFlags` {#npm-config-hook-rebuild-flags}

پرچم‌هایی که پس از نصب وابستگی‌ها در محیط، به دستور {command}`npm rebuild` پاس داده می‌شوند.

### متغیرهای پذیرفته‌شده {#npm-config-hook-honored-variables}

متغیرهای زیر توسط `npmConfigHook` پشتیبانی و رعایت می‌شوند.

- [`npmWorkspace`](#javascript-buildNpmPackage-npmWorkspace)
- [`npmFlags`](#javascript-buildNpmPackage-npmFlags)
- `npmRoot`
