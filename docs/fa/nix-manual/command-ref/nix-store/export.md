# نام

`nix-store --export` - صادر کردن مسیرهای انبار به یک آرشیو نیکس [Nix Archive]

## خلاصه دستور

`nix-store` `--export` *paths…*

## توضیحات

عملیات `--export`، صورت سریالی‌شده‌ای از [اشیاء انبار](@docroot@/glossary.md#gloss-store-object) داده‌شده را در خروجی استاندارد می‌نویسد؛ با این فرمت می‌توان آن‌ها را با استفاده از [`nix-store --import`](./import.md) به یک [انبار Nix](@docroot@/store/index.md) دیگر وارد کرد.

> **هشدار**
>
> این دستور [بستار](@docroot@/glossary.md#gloss-closure) مسیرهای انبار مشخص‌شده را تولید *نمی‌کند*.
> تلاش برای وارد کردن شیء انباری که به مسیرهای انبار ناموجود در انبار هدف Nix اشاره می‌کند، با شکست مواجه خواهد شد.
>
> برای به‌دست آوردن بستار یک مسیر انبار، از [`nix-store --query`](@docroot@/command-ref/nix-store/query.md) استفاده کنید.

این دستور با [`nix-store --dump`](./dump.md) متفاوت است؛ دستور دوم یک [آرشیو نیکس](@docroot@/glossary.md#gloss-nar) تولید می‌کند که شامل مجموعه [ارجاعات](@docroot@/glossary.md#gloss-reference) یک مسیر انبار داده‌شده *نیست*.

> **نکته**
>
> برای انتقال کارآمد بستارها به ماشین‌های راه دور از طریق SSH، از [`nix-copy-closure`](@docroot@/command-ref/nix-copy-closure.md) استفاده کنید.

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

> **مثال**
>
> استقرار GNU Hello روی یک ماشین ایزوله از شبکه (Air-gapped) از طریق حافظه فلش USB.
>
> نوشتن بستار روی دستگاه بلوکی در ماشینی که به اینترنت متصل است:
>
```shell-session
> [alice@itchy]$ storePath=$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)
> [alice@itchy]$ nix-store --export $(nix-store --query --requisites $storePath) | sudo dd of=/dev/usb
> ```
>
> خواندن closure از روی بلاک‌دیوایس روی ماشینی بدون اتصال به اینترنت:
>
```shell-session
> [bob@scratchy]$ hello=$(sudo dd if=/dev/usb | nix-store --import | tail -1)
> [bob@scratchy]$ $hello/bin/hello
> Hello, world!
> ```
