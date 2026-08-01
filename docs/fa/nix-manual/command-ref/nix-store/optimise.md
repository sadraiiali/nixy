# نام

`nix-store --optimise` - کاهش میزان مصرف فضای دیسک

## خلاصه دستور

`nix-store` `--optimise`

## توضیحات

عملیات `--optimise` با پیدا کردن فایل‌های یکسان در انبار و اتصال سخت (hard-link) آن‌ها به یکدیگر، فضای دیسک اشغال‌شده توسط انبار Nix را کاهش می‌دهد. این کار معمولاً حجم انبار را در حدود ۲۵ تا ۳۵ درصد کاهش می‌دهد. تنها فایل‌های معمولی و پیوندهای نمادین به این روش به یکدیگر پیوند سخت داده می‌شوند. فایل‌ها زمانی یکسان در نظر گرفته می‌شوند که دارای سریال‌سازی [Nix Archive (NAR)][Nix Archive] یکسانی باشند: یعنی فایل‌های معمولی باید محتویات و دسترسی‌های یکسانی (قابل‌اجرا یا غیرقابل‌اجرا) داشته باشند و پیوندهای نمادین نیز باید دارای محتویات یکسانی باشند.

پس از اتمام کار، یا هنگامی که دستور متوقف می‌شود، گزارشی از میزان صرفه‌جویی به‌دست‌آمده در خروجی خطای استاندارد (standard error) چاپ می‌شود.

برای دریافت برخی اطلاعات درباره‌ی روند پیشرفت، از پرچم‌های `-vv` یا `-vvv` استفاده کنید.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

## مثال

```console
$ nix-store --optimise
hashing files in `/nix/store/qhqx7l2f1kmwihc9bnxs7rc159hsxnf3-gcc-4.1.1'
...
541838819 bytes (516.74 MiB) freed by hard-linking 54143 files;
there are 114486 files with equal contents out of 215894 files in total
```

[بایگانی نیکس]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive
