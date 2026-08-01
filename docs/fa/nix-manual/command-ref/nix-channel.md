# نام

`nix-channel` - مدیریت کانال‌های نیکس (Nix channels)

# خلاصه‌دستور

`nix-channel` {`--add` url [*name*] | `--remove` *name* | `--list` | `--update` [*names…*] | `--list-generations` | `--rollback` [*generation*] }

# توصیف

کانال‌ها مکانیزمی برای ارجاع به عبارت‌های Nix راه دور و بازیابی راحت آخرین نسخه آن‌ها هستند.

اجزای متحرک کانال‌ها عبارتند از:
- کانال‌های رسمی فهرست‌شده در <https://channels.nixos.org>
- فهرست مختص کاربر از [کانال‌های مشترک‌شده](#subscribed-channels)
- [محتویات دانلودشده کانال](#channels)
- [مسیر جستجوی عبارت Nix](@docroot@/command-ref/conf-file.md#conf-nix-path)، تنظیم‌شده با [گزینه `-I`](#opt-I) یا [متغیر محیطی `NIX_PATH`](#env-NIX_PATH)

> **توجه**
>
> وضعیت یک کانال مشترک‌شده خارج از عبارت‌های Nixی است که به آن وابسته‌اند.
> این موضوع ممکن است بازتولیدپذیری را محدود کند.
>
> وابستگی به سایر عبارت‌های Nix را می‌توان به طور صریح با موارد زیر اعلام کرد:
> - [`fetchurl`](@docroot@/language/builtins.md#builtins-fetchurl)، [`fetchTarball`](@docroot@/language/builtins.md#builtins-fetchTarball)، یا [`fetchGit`](@docroot@/language/builtins.md#builtins-fetchGit) در عبارت‌های Nix
> - [گزینه `-I`](@docroot@/command-ref/opt-common.md#opt-I) در فراخوانی‌های خط فرمان

این دستور دارای عملیات زیر است:

- `--add` *url* \[*name*\]

  یک کانال با نام *name* واقع در *url* را به فهرست کانال‌های مشترک‌شده اضافه می‌کند.
  اگر *name* حذف شود، به طور پیش‌فرض آخرین جزء *url* در نظر گرفته می‌شود، در حالی که پسوندهای `-stable` یا `-unstable` از آن حذف شده‌اند.

  > **توجه**
  >
  > دستور `--add` به طور خودکار به‌روزرسانی را انجام نمی‌دهد.
  > از `--update` به طور صریح استفاده کنید.

  یک URL کانال باید به پوشه‌ای حاوی فایل `nixexprs.tar.gz` اشاره کند.
  در بالاترین سطح، آن فایل تاربال (tarball) باید حاوی یک پوشه منفرد با یک فایل `default.nix` باشد که به عنوان نقطه ورود کانال عمل می‌کند.

- `--remove` *name*

  کانال *name* را از فهرست کانال‌های مشترک‌شده حذف می‌کند.

- `--list`

  نام‌ها و URLهای تمام کانال‌های مشترک‌شده را در خروجی استاندارد چاپ می‌کند.

- `--update` \[*names*…\]

  عبارت‌های Nix مربوط به کانال‌های مشترک‌شده را دانلود کرده و یک نسل (generation) جدید ایجاد می‌کند.
  اگر هیچ کانالی مشخص نشده باشد، تمام کانال‌ها و در غیر این صورت فقط موارد موجود در *names* را به‌روزرسانی می‌کند.

  > **توجه**
  >
  > محتویات دانلودشده کانال کش می‌شوند.
  > برای تغییر مدت زمان اعتبار دانلودهای کش‌شده، از `--tarball-ttl` یا [گزینه پیکربندی `tarball-ttl`](@docroot@/command-ref/conf-file.md#conf-tarball-ttl) استفاده کنید.

- `--list-generations`

  فهرستی از تمام نسل‌های موجود فعلی برای پروفایل کانال را چاپ می‌کند.

  به همان شیوه کار می‌کند که
```
  nix-env --profile /nix/var/nix/profiles/per-user/$USER/channels --list-generations
  ```

- `--rollback` \[*نسخه*\]

  بازگردانی کانال‌ها به وضعیتی که قبل از آخرین فراخوانی `nix-channel --update` داشتند.
  به‌عنوان یک گزینه اختیاری، می‌توانید شماره *نسخه* (generation) خاصی از کانال را برای بازیابی مشخص کنید.

{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# فایل‌ها

دستور `nix-channel` روی فایل‌های زیر عمل می‌کند.

{{#include ./files/channels.md}}

# مثال‌ها

اشتراک در کانال Nixpkgs و اجرای `hello` از بسته GNU Hello:

```console
$ nix-channel --add https://channels.nixos.org/nixpkgs-unstable
$ nix-channel --list
nixpkgs https://channels.nixos.org/nixpkgs
$ nix-channel --update
$ nix-shell -p hello --run hello
hello
```

بازگردانی (rollback) به‌روزرسانی‌های کانال با استفاده از `--rollback`:

```console
$ nix-instantiate --eval '<nixpkgs>' --attr lib.version
"22.11pre296212.530a53dcbc9"

$ nix-channel --rollback
switching from generation 483 to 482

$ nix-instantiate --eval '<nixpkgs>' --attr lib.version
"22.11pre281526.d0419badfad"
```

حذف یک کانال (channel):

```console
$ nix-channel --remove nixpkgs
$ nix-channel --list
```
