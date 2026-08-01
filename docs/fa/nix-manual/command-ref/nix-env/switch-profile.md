# Name

`nix-env --switch-profile` - تنظیم پروفایل کاربر روی پروفایل مشخص‌شده

# Synopsis

`nix-env` {`--switch-profile` | `-S`} *path*

# Description

این عملیات، *path* را به عنوان پروفایل فعلی کاربر تنظیم می‌کند. یعنی، پیوند نمادین `~/.nix-profile` به گونه‌ای تنظیم می‌شود که به *path* اشاره کند.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# Examples

```console
$ nix-env --switch-profile ~/my-profile
```
