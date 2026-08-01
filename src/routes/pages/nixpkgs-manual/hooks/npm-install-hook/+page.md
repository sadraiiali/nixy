# <a id="npm-install-hook"></a> npmHooks.npmInstallHook

قلابی برای نصب `node_modules` برای بسته‌های npm.
برای پروژه‌های اجرایی npm، پوشاننده (wrapper) ایجاد نمی‌کند.
عمدتاً برای یک محیط چندزبانه ساخته شده است.

## <a id="npm-install-hook-snippet"></a> نمونه‌ها

[](#npm-build-hook-example-snippet)

## <a id="npm-install-hook-variables"></a> متغیرهای کنترل‌کننده `npmInstallHook`

### <a id="npm-install-hook-exclusive-variables"></a> متغیرهای اختصاصی `npmInstallHook`

#### <a id="npm-install-hook-dont-prune"></a> `dontNpmPrune`

اینکه آیا دستور `npm prune` روی `node_modules` اجرا شود یا خیر.
مقدار پیش‌فرض `true` است.

#### <a id="npm-install-hook-prune-flags"></a> `npmInstallFlags`

پرچم‌هایی که هنگام فراخوانی `npm prune` به `node_modules` بسته منتقل می‌شوند.
مقدار پیش‌فرض `--omit=dev --no-save` است که قابل تغییر نیست.

#### <a id="npm-install-hook-dont"></a> `dontNpmInstall`

فعال بودن یا نبودن `npmInstallHook` را کنترل می‌کند.
مقدار پیش‌فرض `true` است، بنابراین قلاب اجرا خواهد شد.

### <a id="npm-install-hook-honored-variables"></a> متغیرهای پشتیبانی‌شده

متغیرهای زیر توسط `npmInstallHook` پشتیبانی می‌شوند.

- [`npmWorkspace`](#javascript-buildNpmPackage-npmWorkspace)
- [`npmFlags`](#javascript-buildNpmPackage-npmFlags)
