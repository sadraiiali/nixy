# نام

دستور `nix-store --restore` - استخراج یک آرشیو نیکس

## خلاصه‌دستور

`nix-store` `--restore` *path*

## توضیحات

عملیات `--restore` یک [آرشیو نیکس (NAR)][Nix Archive] را در *path* استخراج می‌کند، که مسیر مورد نظر نباید از‌پیش‌موجود باشد. آرشیو از ورودی استاندارد خوانده می‌شود.

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
