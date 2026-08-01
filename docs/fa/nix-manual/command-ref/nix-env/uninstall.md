# نام

`nix-env --uninstall` - حذف بسته‌ها از پروفایل کاربر

# خلاصه

`nix-env` {`--uninstall` | `-e`} *drvnames…*

# توضیحات

عملیات حذف (uninstall)، یک پروفایل کاربر جدید بر اساس نسل فعلی پروفایل فعال ایجاد می‌کند که در آن، مسیرهای انبار (store paths) مشخص‌شده توسط نام‌های نمادین *drvnames* حذف می‌شوند.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

```console
$ nix-env --uninstall gcc
$ nix-env --uninstall '.*' (remove everything)
```
