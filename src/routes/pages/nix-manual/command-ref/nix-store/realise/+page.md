# 8.3.3.15. nix-store --realise

## نام

`nix-store --realise` - ساخت یا دریافت اشیاء انبار

## خلاصه

```text
nix-store {--realise | -r} paths… [--dry-run]
```

## توضیحات
هر یک از *paths* به شرح زیر پردازش می‌شود:

- اگر مسیر به یک [store derivation] منتهی شود:
  1. اگر [معتبر] نباشد، خود فایل store derivation را جایگزین کنید.
  2. [output paths] آن را محقق (realise) کنید:
    - تلاش کنید [store objects] مرتبط با مسیرهای خروجی در [closure] مربوط به store derivation را از [substituters] دریافت کنید.
      - با [content-addressing derivations] (تجربی):
        مسیرهای خروجی برای محقق‌سازی را با پرس‌وجوی ورودی‌های محقق‌سازی مبتنی بر محتوا در [Nix database] تعیین کنید.
    - برای هر مسیر انباری که قابل جایگزینی نیست، اشیاء انبار مورد نیاز را تولید کنید:
      1. تمام خروجی‌های وابستگی‌های derivation را محقق کنید.
      2. فایل اجرایی [`builder`](/pages/nix-manual/language/derivations#attr-builder) مربوط به derivation را اجرا کنید.
         
- در غیر این صورت، و اگر مسیر از قبل معتبر نباشد: تلاش کنید [store objects] مرتبط در [closure] مسیر را از [substituters] دریافت کنید.

اگر هیچ جایگزینی موجود نباشد و هیچ store derivation ارائه نشده باشد، عملیات محقق‌سازی با شکست مواجه می‌شود.

[store paths]: /pages/nix-manual/store/store-path
[valid]: /pages/nix-manual/glossary#gloss-validity
[store derivation]: /pages/nix-manual/glossary#gloss-store-derivation
[output paths]: /pages/nix-manual/glossary#gloss-output-path
[store objects]: /pages/nix-manual/store/store-object
[closure]: /pages/nix-manual/glossary#gloss-closure
[substituters]: /pages/nix-manual/command-ref/conf-file#conf-substituters
[content-addressing derivations]: /pages/nix-manual/development/experimental-features#xp-feature-ca-derivations
[Nix database]: /pages/nix-manual/glossary#gloss-nix-database
مسیرهای حاصل در خروجی استاندارد چاپ می‌شوند.
برای آرگومان‌های غیر-derivation، خود آرگومان چاپ می‌شود.

## گزینه‌ها
- `--dry-run`

  توضیحی درباره بسته‌هایی که ساخته یا بارگیری می‌شوند را بدون انجام واقعی عملیات، روی خروجی خطای استاندارد (standard error) چاپ کند.

- `--ignore-unknown`

  اگر یک مسیر غیر-derivation جایگزینی نداشته باشد، آن را به‌طور بی‌صدا نادیده بگیرد.

- `--check`

  این گزینه به شما اجازه می‌دهد بررسی کنید که آیا یک derivation قطعی است یا خیر. این گزینه derivation مشخص‌شده را مجدداً می‌سازد و بررسی می‌کند که آیا نتیجه از نظر بیتی با خروجی‌های موجود یکسان است یا خیر، و در صورت عدم تطابق، خطایی را چاپ می‌کند. خروجی‌های derivation مشخص‌شده باید از قبل وجود داشته باشند. هنگامی که با `-K` استفاده می‌شود، اگر یک مسیر خروجی با خروجی متناظر از ساخت قبلی یکسان نباشد، مسیر خروجی جدید در `/nix/store/name.check.` باقی می‌ماند.

## مثال‌ها
این عملیات معمولاً برای ساخت [store derivation]هایی که توسط [`nix-instantiate`](/pages/nix-manual/command-ref/nix-instantiate) تولید شده‌اند، استفاده می‌شود:

```shell
$ nix-store --realise $(nix-instantiate ./test.nix)
/nix/store/6gwmy5jcnwdlz6aqqhksz863f1l8xc2w-aterm-2.3.1
```

این اساساً همان کاری است که [`nix-build`](/pages/nix-manual/command-ref/nix-build) انجام می‌دهد.

برای بررسی اینکه آیا یک derivation از‌پیش‌ساخته‌شده قطعی / reproducible از نظر نتیجه است یا خیر:

```shell
$ nix-build '<nixpkgs>' --attr hello --check -K
```

برای نمایش خروجی استاندارد و خطای استاندارد یک ساخت، از [`nix-store --read-log`](/pages/nix-manual/command-ref/nix-store/read-log) استفاده کنید:

```shell
$ nix-store --read-log $(nix-instantiate ./test.nix)
```
