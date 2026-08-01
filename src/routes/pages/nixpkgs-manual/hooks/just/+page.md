# <a id="just-hook"></a> `just`

این قلاب راه‌اندازی (setup hook) تلاش می‌کند از [اجراکننده دستور `just`](https://just.systems/man/en/) برای ساخت، بررسی و نصب بسته استفاده کند. این قلاب به صورت پیش‌فرض `buildPhase` ،`checkPhase` و `installPhase` را بازنویسی می‌کند.

<a id="just-hook-justFlags"></a> متغیر `justFlags` می‌تواند روی فهرستی از رشته‌ها تنظیم شود تا پرچم‌های اضافی که به تمامی فراخوانی‌های `just` ارسال می‌شوند را اضافه کند.

## <a id="just-hook-buildPhase"></a> `buildPhase`

این فاز تلاش می‌کند `just` را با [دستورالعمل پیش‌فرض](https://just.systems/man/en/the-default-recipe.html) فراخوانی کند.

<a id="just-hook-dontUseJustBuild"></a> این رفتار را می‌توان با تنظیم `dontUseJustBuild` روی `true` غیرفعال کرد.

## <a id="just-hook-checkPhase"></a> `checkPhase`

این فاز در صورت در دسترس بودن، تلاش می‌کند دستورالعمل `just test` را فراخوانی کند. این رفتار را می‌توان با تنظیم `checkTarget` روی یک رشته بازنویسی کرد.

<a id="just-hook-dontUseJustCheck"></a> این رفتار را می‌توان با تنظیم `dontUseJustCheck` روی `true` غیرفعال کرد.

## <a id="just-hook-installPhase"></a> `installPhase`

این فاز تلاش می‌کند دستورالعمل `just install` را فراخوانی کند.

<a id="just-hook-dontUseJustInstall"></a> این رفتار را می‌توان با تنظیم `dontUseJustInstall` روی `true` غیرفعال کرد.
