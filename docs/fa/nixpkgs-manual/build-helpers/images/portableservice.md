# pkgs.portableService {#sec-pkgs-portableService}

`pkgs.portableService` تابعی برای ایجاد [Portable Services](https://systemd.io/PORTABLE_SERVICES/) در یک تصویر دیسک خام `squashfs` با دسترسی فقط‌خواندنی و تغییرناپذیر است.
این قابلیت به شما امکان می‌دهد از Nix برای ساخت تصاویری استفاده کنید که روی بسیاری از توزیع‌های اخیر لینوکس قابل اجرا هستند.

::: {.note}
سرویس‌های قابل حمل از نسخه systemd 239 (منتشرشده در 2018-06-22) پشتیبانی می‌شوند.
:::

تصویر تولیدشده شامل ساختار سیستم‌فایل مورد نیاز مشخصات Portable Services به همراه بسته‌های ارائه‌شده به `portableService` و تمامی وابستگی‌های آن‌ها خواهد بود.
پس از تولید، تصویر با پسوند فایل `.raw` همان‌طور که در مشخصات الزامی شده‌است، در انبار نیکس (Nix store) قرار می‌گیرد.
برای درک نحوه استفاده از خروجی `portableService` به [](#ex-portableService-hello) مراجعه کنید.

## Inputs {#ssec-pkgs-portableService-inputs}

`portableService` انتظار یک آرگومان با صفات زیر را دارد:

`pname` (رشته)

: نام سرویس قابل حمل.
  تصویر تولیدشده طبق الگوی `$pname_$version.raw` نام‌گذاری خواهد شد که توسط مشخصات Portable Services پشتیبانی می‌شود.

`version` (رشته)

: نسخه سرویس قابل حمل.
  تصویر تولیدشده طبق الگوی `$pname_$version.raw` نام‌گذاری خواهد شد که توسط مشخصات Portable Services پشتیبانی می‌شود.

`units` (فهرستی از مجموعه‌های صفت)

: فهرستی از درایویشن‌ها برای فایل‌های یونیت systemd.
  هر درایویشن باید یک فایل منفرد تولید کند و نامی داشته باشد که با مقدار `pname` شروع شده و با پسوند نوع یونیت (مانند ".service"، ".socket"، ".timer" و غیره) پایان یابد.
  برای درک بهتر این محدودیت نام‌گذاری به [](#ex-portableService-hello) مراجعه کنید.

`description` (رشته یا پوچ؛ _اختیاری_)

: در صورت مشخص شدن، این مقدار به‌عنوان `PORTABLE_PRETTY_NAME` به فایل `/etc/os-release` در تصویر تولیدشده اضافه می‌شود.
  از این صفت می‌توان برای ارائه اطلاعات بیشتر به هر کسی که تصویر را بررسی می‌کند استفاده کرد.

  _مقدار پیش‌فرض:_ `null`.

`homepage` (رشته یا پوچ؛ _اختیاری_)

: در صورت مشخص شدن، این مقدار به‌عنوان `HOME_URL` به فایل `/etc/os-release` در تصویر تولیدشده اضافه می‌شود.
  از این صفت می‌توان برای ارائه اطلاعات بیشتر به هر کسی که تصویر را بررسی می‌کند استفاده کرد.

  _مقدار پیش‌فرض:_ `null`.

`symlinks` (فهرستی از مجموعه‌های صفت؛ _اختیاری_)

: فهرستی از مجموعه‌های صفت به فرمت `{object, symlink}`.
  به ازای هر عنصر در فهرست، `portableService` یک پیوند نمادین (symlink) در مسیر مشخص‌شده توسط `symlink` (نسبت به ریشه تصویر) ایجاد می‌کند که به `object` اشاره دارد.

  تمام بسته‌هایی که `object` به آن‌ها وابسته است و وابستگی‌های آن‌ها به‌طور خودکار درون تصویر کپی می‌شوند.

  از این قابلیت می‌توان برای ایجاد پیوندهای نمادین (symlinks) برای برنامه‌هایی استفاده کرد که وجود برخی فایل‌ها را به‌صورت سراسری فرض می‌کنند (برای مثال `/etc/ssl` یا `/bin/bash`).
  برای درک نحوه انجام این کار به [](#ex-portableService-symlinks) مراجعه کنید.

  _مقدار پیش‌فرض:_ `[]`.

`contents` (فهرستی از مجموعه‌های صفت؛ _اختیاری_)

: فهرستی از درایویشن‌های اضافی که باید به‌صورت دست‌نخورده در تصویر گنجانده شوند.
  این درایویشن‌ها مستقیماً در یک پوشه `/nix/store` درون تصویر قرار خواهند گرفت.

  _مقدار پیش‌فرض:_ `[]`.

`squashfsTools` (مجموعه صفت؛ _اختیاری_)

: به شما اجازه می‌دهد بسته‌ای را که {manpage}`mksquashfs(1)` را ارائه می‌دهد و به‌صورت داخلی توسط `portableService` استفاده می‌شود، بازنشانی کنید.

  _مقدار پیش‌فرض:_ `pkgs.squashfsTools`.

`squash-compression` (رشته؛ _اختیاری_)

: به‌عنوان گزینه فشرده‌سازی به {manpage}`mksquashfs(1)` پاس داده می‌شود که به‌صورت داخلی توسط `portableService` استفاده می‌شود.

  _مقدار پیش‌فرض:_ `"xz -Xdict-size 100%"`.

`squash-block-size` (رشته؛ _اختیاری_)

: به عنوان گزینه اندازه بلوک به {manpage}`mksquashfs(1)` ارسال می‌شود، که به‌صورت داخلی توسط `portableService` استفاده می‌شود.

  _مقدار پیش‌فرض:_ `"1M"`.

## مثال‌ها {#ssec-pkgs-portableService-examples}

[]{#ex-pkgs-portableService}
:::{.example #ex-portableService-hello}
# ساخت تصویر Portable Service

مثال زیر یک تصویر Portable Service همراه با یک یونیت سرویس که آن را اجرا می‌کند، با استفاده از بسته `hello` می‌سازد.

```nix
{
  lib,
  writeText,
  portableService,
  hello,
}:
let
  hello-service = writeText "hello.service" ''
    [Unit]
    Description=Hello world service

    [Service]
    Type=oneshot
    ExecStart=${lib.getExe hello}
  '';
in
portableService {
  pname = "hello";
  inherit (hello) version;
  units = [ hello-service ];
}
```

پس از ساخت بسته، تصویر تولیدشده را می‌توان از طریق {manpage}`portablectl(1)` روی یک سیستم بارگذاری کرد:

```shell
$ nix-build
(some output removed for clarity)
/nix/store/8c20z1vh7z8w8dwagl8w87b45dn5k6iq-hello-img-2.12.1

$ portablectl attach /nix/store/8c20z1vh7z8w8dwagl8w87b45dn5k6iq-hello-img-2.12.1/hello_2.12.1.raw
Created directory /etc/systemd/system.attached.
Created directory /etc/systemd/system.attached/hello.service.d.
Written /etc/systemd/system.attached/hello.service.d/20-portable.conf.
Created symlink /etc/systemd/system.attached/hello.service.d/10-profile.conf → /usr/lib/systemd/portable/profile/default/service.conf.
Copied /etc/systemd/system.attached/hello.service.
Created symlink /etc/portables/hello_2.12.1.raw → /nix/store/8c20z1vh7z8w8dwagl8w87b45dn5k6iq-hello-img-2.12.1/hello_2.12.1.raw.

$ systemctl start hello
$ journalctl -u hello
Feb 28 22:39:16 hostname systemd[1]: Starting Hello world service...
Feb 28 22:39:16 hostname hello[102887]: Hello, world!
Feb 28 22:39:16 hostname systemd[1]: hello.service: Deactivated successfully.
Feb 28 22:39:16 hostname systemd[1]: Finished Hello world service.

$ portablectl detach hello_2.12.1
Removed /etc/systemd/system.attached/hello.service.
Removed /etc/systemd/system.attached/hello.service.d/10-profile.conf.
Removed /etc/systemd/system.attached/hello.service.d/20-portable.conf.
Removed /etc/systemd/system.attached/hello.service.d.
Removed /etc/portables/hello_2.12.1.raw.
Removed /etc/systemd/system.attached.
```
:::

:::{.example #ex-portableService-symlinks}
# مشخص کردن پیوندهای نمادین (symlinks) هنگام ساخت تصویر Portable Service

برخی سرویس‌ها ممکن است انتظار داشته باشند فایل‌ها یا پوشه‌ها به صورت سراسری در دسترس باشند.
یک نمونه، سرویسی است که انتظار دارد به‌طور پیش‌فرض تمام گواهی‌های SSL معتبر در یک مکان مشخص وجود داشته باشند.

برای در دسترس قرار دادن موارد به صورت سراسری، باید هنگام استفاده از `portableService` صفت (attribute) `symlinks` را مشخص کنید.
بسته زیر بر پایه بسته موجود در [](#ex-portableService-hello) ساخته شده‌است تا `/etc/ssl` را به صورت سراسری در دسترس قرار دهد (این موضوع صرفاً جنبه توضیحی دارد، زیرا `hello` از `/etc/ssl` استفاده نمی‌کند).

```nix
{
  lib,
  writeText,
  portableService,
  hello,
  cacert,
}:
let
  hello-service = writeText "hello.service" ''
    [Unit]
    Description=Hello world service

    [Service]
    Type=oneshot
    ExecStart=${lib.getExe hello}
  '';
in
portableService {
  pname = "hello";
  inherit (hello) version;
  units = [ hello-service ];
  symlinks = [
    {
      object = "${cacert}/etc/ssl";
      symlink = "/etc/ssl";
    }
  ];
}
```
:::
