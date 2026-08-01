# 8.3.3.9. nix-store --import

## نام

`nix-store --import` - وارد کردن [آرشیو نیکس] به انبار

[آرشیو نیکس]: /pages/nix-manual/store/file-system-object/content-address#serial-nix-archive
## خلاصه
`nix-store` `--import`

## توضیحات
عملیات `--import`، سریال‌سازی مجموعه‌ای از [اشیاء انبار](/pages/nix-manual/glossary#gloss-store-object) تولیدشده توسط [`nix-store --export`](/pages/nix-manual/command-ref/nix-store/export) را از ورودی استاندارد می‌خواند و آن اشیاء انبار را به [انبار Nix](/pages/nix-manual/store) مشخص‌شده اضافه می‌کند.
مسیرهایی که از پیش در انبار Nix هدف وجود دارند، نادیده گرفته می‌شوند.
اگر مسیری [به] مسیر دیگری که در انبار Nix هدف وجود ندارد، [ارجاع دهد](/pages/nix-manual/glossary#gloss-reference)، عملیات وارد کردن با شکست مواجه می‌شود.

> **نکته**
>
> برای انتقال کارآمد بسته‌های بسته (closures) به ماشین‌های راه دور از طریق SSH، از [`nix-copy-closure`](/pages/nix-manual/command-ref/nix-copy-closure) استفاده کنید.

## مثال‌ها
> **مثال**
>
> با داشتن یک بسته (closure) از GNU Hello به عنوان یک فایل:
>

```shell
> $ storePath="$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)"
> $ nix-store --export $(nix-store --query --requisites $storePath) > hello.closure
> ```
>
> بسته‌ی بسته (closure) را با استفاده از گزینه‌ی [`--store`](/pages/nix-manual/command-ref/conf-file#conf-store) به یک [انبار SSH راه دور](/pages/nix-manual/store/types/ssh-store) درون‌ریزی کنید:
>

```shell
> $ nix-store --import --store ssh://alice@itchy.example.org < hello.closure
> ```
