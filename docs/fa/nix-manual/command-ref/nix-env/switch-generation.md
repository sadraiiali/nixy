# نام

`nix-env --switch-generation` - تنظیم محیط کاربر روی نسل مشخصی از پروفایل

# خلاصه

`nix-env` {`--switch-generation` | `-G`} *generation*

# توضیحات

این عملیات، نسل شماره *generation* را به عنوان نسل فعلی پروفایل فعال تعیین می‌کند. به این معنا که اگر `profile` مسیر پروفایل فعال باشد، پیوند نمادین `profile` به گونه‌ای تنظیم می‌شود که به `profile-generation-link` اشاره کند؛ و آن خود نیز پیوند نمادینی است که به محیط کاربری واقعی در انبار Nix اشاره دارد.

اگر نسل مشخص‌شده وجود نداشته باشد، عملیات تعویض با شکست مواجه خواهد شد.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

```console
$ nix-env --switch-generation 42
switching from generation 50 to 42
```

