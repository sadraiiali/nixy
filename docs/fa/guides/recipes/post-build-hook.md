(post-build-hooks)=
# راه‌اندازی قلاب‌های پس از ساخت

این راهنما نحوه استفاده از گزینه پیکربندی [`post-build-hook`](/pages/nix-manual/command-ref/conf-file-prefix#conf-post-build-hook) در Nix را برای بارگذاری خودکار فرآورده‌ی ساخت در یک [کش باینری سازگار با S3](/pages/nix-manual/store/types) نشان می‌دهد.

## نکات احتیاطی در پیاده‌سازی

این یک مثال ساده و کاربردی است، اما برای تمام موارد استفاده مناسب نیست.

برنامه قلاب پس از ساخت پس از هر بار ساخت اجرا می‌شود و حلقه ساخت را مسدود می‌کند.
اگر برنامه قلاب با خطا مواجه شود، حلقه ساخت متوقف می‌شود.

به طور مشخص، این پیاده‌سازی باعث می‌شود که وقتی اتصال شبکه کند یا غیرقابل اعتماد است، Nix کند یا غیرقابل استفاده شود.
یک پیاده‌سازی پیشرفته‌تر ممکن است مسیرهای انبار را به یک خدمت پس‌زمینه یا صف ارائه‌شده توسط کاربر منتقل کند تا پردازش مسیرهای انبار در خارج از حلقه ساخت انجام شود.

## پیش‌نیازها

این آموزش فرض می‌کند که شما یک [کش باینری سازگار با S3 پیکربندی کرده‌اید](/pages/nix-manual/store/types#authenticated-writes-to-your-s3-compatible-binary-cache) و پروفایل پیش‌فرض AWS کاربر `root` می‌تواند فایل‌ها را در باکت بارگذاری کند.

## راه‌اندازی کلید امضا

از [`nix-store --generate-binary-cache-key`](/pages/nix-manual/command-ref/nix-store/generate-binary-cache-key) برای ایجاد یک جفت کلید رمزنگاری‌شده استفاده کنید.
شما مسیرها را با کلید خصوصی امضا می‌کنید و کلید عمومی را برای تأیید اصالت مسیرها توزیع می‌کنید.

```console
$ nix-store --generate-binary-cache-key example-nix-cache-1 /etc/nix/key.private /etc/nix/key.public
$ cat /etc/nix/key.public
example-nix-cache-1:1/cKDz3QCCOmwcztD2eV6Coggp6rqc9DGjWv7C0G+rM=
```

[](custom-binary-cache) روی هر ماشینی که قرار است به باکت دسترسی داشته باشد.
برای مثال، آدرس URL کش را به [`substituters`](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters) و کلید عمومی را به [`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys) در فایل `nix.conf` اضافه کنید:

```
substituters = https://cache.nixos.org/ s3://example-nix-cache
trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= example-nix-cache-1:1/cKDz3QCCOmwcztD2eV6Coggp6rqc9DGjWv7C0G+rM=
```

ماشین‌هایی که برای کش ساخت انجام می‌دهند، باید اشتقاق ساخت را با استفاده از کلید خصوصی امضا کنند.
مسیر فایل حاوی کلید خصوصی که تازه تولید کرده‌اید، باید به تنظیم [`secret-key-files`](/pages/nix-manual/command-ref/conf-file-prefix#conf-secret-key-files) برای آن ماشین‌ها اضافه شود:

```
secret-key-files = /etc/nix/key.private
```

## پیاده‌سازی قلاب پس از ساخت

اسکریپت زیر را در `/etc/nix/upload-to-cache.sh` بنویسید:

```bash
#!/bin/sh
set -eu
set -f # disable globbing
export IFS=' '
echo "Uploading paths" $OUT_PATHS
exec nix copy --to "s3://example-nix-cache" $OUT_PATHS
```

متغیر `$OUT_PATHS` فهرستی از مسیرهای انبار Nix است که با فاصله از یکدیگر جدا شده‌اند.
در این حالت، ما انتظار داریم و می‌خواهیم که شل (shell) جداسازی کلمات را انجام دهد تا هر مسیر خروجی به عنوان آرگومان مجزایی برای `nix store sign` در نظر گرفته شود.
Nix تضمین می‌کند که مسیرها شامل هیچ فضایی (فاصله خالی) نخواهند بود، با این حال ممکن است یک مسیر انبار شامل کاراکترهای گلاب (glob) باشد.
دستور `set -f` قابلیت گلابینگ را در شل غیرفعال می‌کند.

مطمئن شوید که برنامه قلاب توسط کاربر `root` قابل اجرا باشد:

```console
# chmod +x /etc/nix/upload-to-cache.sh
```

## به‌روزرسانی پیکربندی Nix

گزینه پیکربندی [`post-build-hook`](/pages/nix-manual/command-ref/conf-file-prefix#conf-post-build-hook) را روی ماشین محلی تنظیم کنید تا قلاب پس از ساخت اجرا شود:

```
post-build-hook = /etc/nix/upload-to-cache.sh
```

سپس `nix-daemon` را روی تمام ماشین‌های درگیر راه‌اندازی مجدد (reboot) کنید، به عنوان مثال با

```
pkill nix-daemon
```

## تست

هر درایویشن را بسازید، برای مثال:

```console
$ nix-build -E '(import <nixpkgs> {}).writeText "example" (builtins.toString builtins.currentTime)'
this derivation will be built:
  /nix/store/s4pnfbkalzy5qz57qs6yybna8wylkig6-example.drv
building '/nix/store/s4pnfbkalzy5qz57qs6yybna8wylkig6-example.drv'...
running post-build-hook '/home/grahamc/projects/github.com/NixOS/nix/post-hook.sh'...
post-build-hook: Signing paths /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
post-build-hook: Uploading paths /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
/nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
```

برای بررسی اینکه قلاب اعمال شده‌است، مسیر را از انبار حذف کرده و تلاش کنید آن را از کش باینری جایگزین کنید:

```console
$ rm ./result
$ nix-store --delete /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
$ nix-store --realise /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
copying path '/nix/store/m8bmqwrch6l3h8s0k3d673xpmipcdpsa-example from 's3://example-nix-cache'...
warning: you did not specify '--add-root'; the result might be removed by the garbage collector
/nix/store/m8bmqwrch6l3h8s0k3d673xpmipcdpsa-example
```

## نتیجه‌گیری

شما Nix را به‌گونه‌ای پیکربندی کرده‌اید که به‌طور خودکار هر ساخت محلی را امضا کرده و روی یک کش باینری سازگار با S3 در راه دور بارگذاری کند.

پیش از استقرار این پیکربندی در محیط عملیاتی (production)، حتماً [نکات احتیاطی پیاده‌سازی](#implementation-caveats) را در نظر بگیرید.
