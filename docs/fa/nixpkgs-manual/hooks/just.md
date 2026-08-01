# `just` {#just-hook}

این قلاب راه‌اندازی (setup hook) تلاش می‌کند از [اجراکننده دستور `just`](https://just.systems/man/en/) برای ساخت، بررسی و نصب بسته استفاده کند. این قلاب به صورت پیش‌فرض `buildPhase` ،`checkPhase` و `installPhase` را بازنویسی می‌کند.

[]{#just-hook-justFlags} متغیر `justFlags` می‌تواند روی فهرستی از رشته‌ها تنظیم شود تا پرچم‌های اضافی که به تمامی فراخوانی‌های `just` ارسال می‌شوند را اضافه کند.

## `buildPhase` {#just-hook-buildPhase}

این فاز تلاش می‌کند `just` را با [دستورالعمل پیش‌فرض](https://just.systems/man/en/the-default-recipe.html) فراخوانی کند.

[]{#just-hook-dontUseJustBuild} این رفتار را می‌توان با تنظیم `dontUseJustBuild` روی `true` غیرفعال کرد.

## `checkPhase` {#just-hook-checkPhase}

این فاز در صورت در دسترس بودن، تلاش می‌کند دستورالعمل `just test` را فراخوانی کند. این رفتار را می‌توان با تنظیم `checkTarget` روی یک رشته بازنویسی کرد.

[]{#just-hook-dontUseJustCheck} این رفتار را می‌توان با تنظیم `dontUseJustCheck` روی `true` غیرفعال کرد.

## `installPhase` {#just-hook-installPhase}

این فاز تلاش می‌کند دستورالعمل `just install` را فراخوانی کند.

[]{#just-hook-dontUseJustInstall} این رفتار را می‌توان با تنظیم `dontUseJustInstall` روی `true` غیرفعال کرد.
