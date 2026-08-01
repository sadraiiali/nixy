# نام

`nix-store --import` - وارد کردن [آرشیو نیکس] به انبار

[آرشیو نیکس]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

# خلاصه

`nix-store` `--import`

# توضیحات

عملیات `--import`، سریال‌سازی مجموعه‌ای از [اشیاء انبار](@docroot@/glossary.md#gloss-store-object) تولیدشده توسط [`nix-store --export`](./export.md) را از ورودی استاندارد می‌خواند و آن اشیاء انبار را به [انبار Nix](@docroot@/store/index.md) مشخص‌شده اضافه می‌کند.
مسیرهایی که از پیش در انبار Nix هدف وجود دارند، نادیده گرفته می‌شوند.
اگر مسیری [به] مسیر دیگری که در انبار Nix هدف وجود ندارد، [ارجاع دهد](@docroot@/glossary.md#gloss-reference)، عملیات وارد کردن با شکست مواجه می‌شود.

> **نکته**
>
> برای انتقال کارآمد بسته‌های بسته (closures) به ماشین‌های راه دور از طریق SSH، از [`nix-copy-closure`](@docroot@/command-ref/nix-copy-closure.md) استفاده کنید.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

> **مثال**
>
> با داشتن یک بسته (closure) از GNU Hello به عنوان یک فایل:
>
```shell-session
> $ storePath="$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)"
> $ nix-store --export $(nix-store --query --requisites $storePath) > hello.closure
> ```
>
> بسته‌ی بسته (closure) را با استفاده از گزینه‌ی [`--store`](@docroot@/command-ref/conf-file.md#conf-store) به یک [انبار SSH راه دور](@docroot@/store/types/ssh-store.md) درون‌ریزی کنید:
>
```console
> $ nix-store --import --store ssh://alice@itchy.example.org < hello.closure
> ```

