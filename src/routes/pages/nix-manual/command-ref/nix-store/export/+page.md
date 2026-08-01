# 8.3.3.6. nix-store --export

## نام

`nix-store --export` - صادر کردن مسیرهای انبار به یک آرشیو نیکس [Nix Archive]

## خلاصه دستور

`nix-store` `--export` *paths…*

## توضیحات

عملیات `--export`، صورت سریالی‌شده‌ای از [اشیاء انبار](/pages/nix-manual/glossary#gloss-store-object) داده‌شده را در خروجی استاندارد می‌نویسد؛ با این فرمت می‌توان آن‌ها را با استفاده از [`nix-store --import`](/pages/nix-manual/command-ref/nix-store/import) به یک [انبار Nix](/pages/nix-manual/store) دیگر وارد کرد.

> **هشدار**
>
> این دستور [بستار](/pages/nix-manual/glossary#gloss-closure) مسیرهای انبار مشخص‌شده را تولید *نمی‌کند*.
> تلاش برای وارد کردن شیء انباری که به مسیرهای انبار ناموجود در انبار هدف Nix اشاره می‌کند، با شکست مواجه خواهد شد.
>
> برای به‌دست آوردن بستار یک مسیر انبار، از [`nix-store --query`](/pages/nix-manual/command-ref/nix-store/query) استفاده کنید.

این دستور با [`nix-store --dump`](/pages/nix-manual/command-ref/nix-store/dump) متفاوت است؛ دستور دوم یک [آرشیو نیکس](/pages/nix-manual/glossary#gloss-nar) تولید می‌کند که شامل مجموعه [ارجاعات](/pages/nix-manual/glossary#gloss-reference) یک مسیر انبار داده‌شده *نیست*.

> **نکته**
>
> برای انتقال کارآمد بستارها به ماشین‌های راه دور از طریق SSH، از [`nix-copy-closure`](/pages/nix-manual/command-ref/nix-copy-closure) استفاده کنید.

[Nix Archive]: /pages/nix-manual/store/file-system-object/content-address#serial-nix-archive
## مثال‌ها
> **مثال**
>
> استقرار GNU Hello روی یک ماشین ایزوله از شبکه (Air-gapped) از طریق حافظه فلش USB.
>
> نوشتن بستار روی دستگاه بلوکی در ماشینی که به اینترنت متصل است:
>

```shell
> [alice@itchy]$ storePath=$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)
> [alice@itchy]$ nix-store --export $(nix-store --query --requisites $storePath) | sudo dd of=/dev/usb
> ```
>
> خواندن closure از روی بلاک‌دیوایس روی ماشینی بدون اتصال به اینترنت:
>

```shell
> [bob@scratchy]$ hello=$(sudo dd if=/dev/usb | nix-store --import | tail -1)
> [bob@scratchy]$ $hello/bin/hello
> Hello, world!
> ```
