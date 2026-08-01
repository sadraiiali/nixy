# نام

`nix-env --set-flag` - اصلاح صفت‌های فراداده (meta attributes) بسته‌های نصب‌شده

# خلاصه دستور

`nix-env` `--set-flag` *name* *value* *drvnames*

# توضیحات

عملیات `--set-flag` امکان اصلاح صفت‌های فراداده (meta attributes) بسته‌های نصب‌شده را فراهم می‌کند. چندین صفت وجود دارد که اصلاح آن‌ها مفید است، زیرا روی رفتار `nix-env` یا اسکریپت ساخت محیط کاربر تأثیر می‌گذارند:

- صفت `priority` را می‌توان برای حل تضادهای نام فایل تغییر داد. اسکریپت ساخت محیط کاربر از صفت `meta.priority` در derivationها برای حل تضاد نام فایل‌ها بین بسته‌ها استفاده می‌کند. مقادیر اولویت پایین‌تر نشان‌دهنده اولویت بالاتر هستند. برای نمونه، بسته wrapper مربوط به GCC و بسته Binutils در Nixpkgs هر دو دارای فایلی به نام `bin/ld` هستند، بنابراین پیش‌تر اگر سعی می‌کردید هر دو را نصب کنید، با یک تضاد مواجه می‌شدید. اما از سوی دیگر، اکنون wrapper مربوط به GCC اولویت بالاتری نسبت به Binutils اعلام می‌کند، بنابراین فایل `bin/ld` مربوط به اولی در محیط کاربر پیوند نمادین (symlink) می‌شود.

- صفت `keep` را می‌توان روی `true` تنظیم کرد تا از ارتقا یا جایگزینی بسته جلوگیری شود. اگر می‌خواهید نسخه قدیمی‌تری از یک بسته را حفظ کنید، این کار مفید است.

- صفت `active` را می‌توان روی `false` تنظیم کرد تا بسته «غیرفعال» شود. یعنی هیچ پیوند نمادینی (symlink) به فایل‌های بسته ایجاد نخواهد شد، اما بسته همچنان بخشی از پروفایل باقی می‌ماند (بنابراین توسط جمع‌کنندهٔ زباله (garbage collector) جمع‌آوری نمی‌شود). این صفت را می‌توان مجدداً روی `true` تنظیم کرد تا بسته دوباره فعال شود.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

برای جلوگیری از ارتقای نسخه فعلی نصب‌شده‌ی Firefox:

```console
$ nix-env --set-flag keep true firefox
```

پس از این، `nix-env --upgrade ` از Firefox صرف‌نظر خواهد کرد.

برای غیرفعال کردن Firefox نصب‌شده‌ی فعلی و سپس نصب یک Firefox جدید، در حالی که نسخه قدیمی همچنان بخشی از پروفایل باقی می‌ماند:

```console
$ nix-env --query
firefox-2.0.0.9 (the current one)

$ nix-env --preserve-installed --install firefox-2.0.0.11
installing `firefox-2.0.0.11'
building path(s) `/nix/store/myy0y59q3ig70dgq37jqwg1j0rsapzsl-user-environment'
collision between `/nix/store/...-firefox-2.0.0.11/bin/firefox'
  and `/nix/store/...-firefox-2.0.0.9/bin/firefox'.
(i.e., can’t have two active at the same time)

$ nix-env --set-flag active false firefox
setting flag on `firefox-2.0.0.9'

$ nix-env --preserve-installed --install firefox-2.0.0.11
installing `firefox-2.0.0.11'

$ nix-env --query
firefox-2.0.0.11 (the enabled one)
firefox-2.0.0.9 (the disabled one)
```

برای اینکه فایل‌های موجود در `binutils` نسبت به فایل‌های موجود در `gcc` اولویت داشته باشند:

```console
$ nix-env --set-flag priority 5 binutils
$ nix-env --set-flag priority 10 gcc
```

