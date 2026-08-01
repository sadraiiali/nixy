# npmHooks.npmInstallHook {#npm-install-hook}

قلابی برای نصب `node_modules` برای بسته‌های npm.
برای پروژه‌های اجرایی npm، پوشاننده (wrapper) ایجاد نمی‌کند.
عمدتاً برای یک محیط چندزبانه ساخته شده است.

## نمونه‌ها {#npm-install-hook-snippet}

[](#npm-build-hook-example-snippet)

## متغیرهای کنترل‌کننده `npmInstallHook` {#npm-install-hook-variables}

### متغیرهای اختصاصی `npmInstallHook` {#npm-install-hook-exclusive-variables}

#### `dontNpmPrune` {#npm-install-hook-dont-prune}

اینکه آیا دستور {command}`npm prune` روی `node_modules` اجرا شود یا خیر.
مقدار پیش‌فرض `true` است.

#### `npmInstallFlags` {#npm-install-hook-prune-flags}

پرچم‌هایی که هنگام فراخوانی {command}`npm prune` به `node_modules` بسته منتقل می‌شوند.
مقدار پیش‌فرض `--omit=dev --no-save` است که قابل تغییر نیست.

#### `dontNpmInstall` {#npm-install-hook-dont}

فعال بودن یا نبودن `npmInstallHook` را کنترل می‌کند.
مقدار پیش‌فرض `true` است، بنابراین قلاب اجرا خواهد شد.

### متغیرهای پشتیبانی‌شده {#npm-install-hook-honored-variables}

متغیرهای زیر توسط `npmInstallHook` پشتیبانی می‌شوند.

- [`npmWorkspace`](#javascript-buildNpmPackage-npmWorkspace)
- [`npmFlags`](#javascript-buildNpmPackage-npmFlags)
