(attribute)
- builder -> سازنده (Builder)
- source code / source -> سورس / کد منبع
- keep Latin terms unchanged: `outputs`, `meta.outputsToInstall`, `bin`, `out`, `man`, `coreutils.info`, `dev`, `propagatedBuildOutputs`, `$outputBin`, `$outputLib`, `symlinkJoin`, `<nixpkgs/pkgs/build-support/setup-hooks/multiple

```nix
{
  outputs = [
    "bin"
    "dev"
    "out"
    "doc"
  ];
}
```

اغلب چنین یک خطی کافی است. به ازای هر خروجی، یک متغیر محیطی با همان نام به سازنده (Builder) ارسال می‌شود و شامل مسیر آن خروجی در انبار نیکس (Nix store) است. معمولاً شما می‌خواهید خروجی اصلی `out` را نیز داشته باشید، زیرا تمام فایل‌هایی را که به جای دیگری نرفته‌اند جذب می‌کند.

::: {.note}
یک رفتار ویژه برای خروجی

برای صفحات man بخش ۳ استفاده می‌شود که معمولاً در `share/man/man[0-9]/` قرار دارند. این موارد به‌طور پیش‌فرض به `devman` یا `$outputMan` می‌روند.

#### `$outputInfo` {#outputinfo}

برای صفحات info استفاده می‌شود که معمولاً در `share/info/` قرار دارند. این
