# کمک‌رسان‌های ساخت {#part-builders}

یک کمک‌رسان ساخت، تابعی است که درایویشن‌ها را تولید می‌کند.

:::{.warning}
این موضوع نباید با [`آرگومان builder` از دستور اولیه `derivation` در Nix](https://nixos.org/manual/nix/unstable/language/derivations.html) اشتباه گرفته شود که به فایل اجرایی تولیدکننده نتیجه ساخت اشاره دارد، یا با [سازنده راه دور](https://nixos.org/manual/nix/stable/advanced-topics/distributed-builds.html) که به یک ماشین راه دور اشاره می‌کند که می‌تواند چنین فایل اجرایی را اجرا کند.
:::

چنین تابعی معمولاً به‌منظور انتزاع‌سازی روی یک گردش کار معمول برای یک زبان برنامه‌نویسی یا چارچوب مشخص طراحی می‌شود.
این امر امکان اعلام دستورالعمل ساخت را با تنظیم تعداد محدودی از گزینه‌های مرتبط با مورد استفاده خاص، به جای استفاده مستقیم از تابع `derivation` فراهم می‌کند.

[`stdenv.mkDerivation`](#part-stdenv) پرکاربردترین کمک‌رسان ساخت است و به عنوان پایه‌ای برای بسیاری از کمک‌رسان‌های دیگر عمل می‌کند.
علاوه بر این، گزینه‌های مختلفی را برای سفارشی‌سازی بخش‌هایی از ساخت‌ها ارائه می‌دهد.

هیچ رابط یکپارچه‌ای برای کمک‌رسان‌های ساخت وجود ندارد.
[کمک‌رسان‌های ساخت ساده](#chap-trivial-builders) و [دریافت‌کننده‌ها](#chap-pkgs-fetchers) برای سهولت کار، انواع ورودی‌های مختلفی دارند.
[کمک‌رسان‌های ساخت مخصوص زبان یا چارچوب](#chap-language-support) معمولاً از سبک `stdenv.mkDerivation` پیروی می‌کنند که یک مجموعه ویژگی (attribute set) یا یک تابع نقطه-ثابت (fixed-point) دریافت‌کنندهٔ مجموعه ویژگی را می‌پذیرد.

```{=include=} chapters
build-helpers/fixed-point-arguments.chapter.md
build-helpers/fetchers.chapter.md
build-helpers/trivial-build-helpers.chapter.md
build-helpers/testers.chapter.md
build-helpers/dev-shell-tools.chapter.md
build-helpers/special.md
build-helpers/images.md
hooks/index.md
packages/index.md
```
