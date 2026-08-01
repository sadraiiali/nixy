# استفاده از `post-build-hook`

# نکات هشداردهنده در پیاده‌سازی

در اینجا ما از قلاب پس از ساخت برای بارگذاری در یک کش باینری استفاده می‌کنیم. این یک مثال ساده و کاربردی است، اما برای تمام موارد استفاده مناسب نیست.

برنامه قلاب پس از ساخت پس از هر ساخت اجرا شده اجرا می‌شود و حلقه ساخت را مسدود می‌کند. اگر برنامه قلاب با خطا مواجه شود، حلقه ساخت خارج می‌شود.

به طور مشخص، این پیاده‌سازی باعث می‌شود که Nix در صورت کند یا غیرقابل‌اعتماد بودن اینترنت، کند یا غیرقابل‌استفاده شود.

یک پیاده‌سازی پیشرفته‌تر ممکن است مسیرهای انبار را به یک خدمت پس‌زمینه یا صف ارائه‌شده توسط کاربر منتقل کند تا پردازش مسیرهای انبار در خارج از حلقه ساخت انجام شود.

# پیش‌نیازها

این آموزش فرض می‌کند که شما یک [کش باینری سازگار با S3](@docroot@/command-ref/new-cli/nix3-help-stores.md#s3-binary-cache-store) را به عنوان یک [substituter](../command-ref/conf-file.md#conf-substituters) پیکربندی کرده‌اید و پروفایل پیش‌فرض AWS کاربر `root` می‌تواند به باکت (bucket) بارگذاری کند.

# راه‌اندازی کلید امضا

از دستور `nix-store --generate-binary-cache-key` برای ایجاد کلیدهای امضای عمومی و خصوصی خود استفاده کنید. ما مسیرها را با کلید خصوصی امضا می‌کنیم و کلید عمومی را برای تأیید اصالت مسیرها توزیع می‌کنیم.

```console
# nix-store --generate-binary-cache-key example-nix-cache-1 /etc/nix/key.private /etc/nix/key.public
# cat /etc/nix/key.public
example-nix-cache-1:1/cKDz3QCCOmwcztD2eV6Coggp6rqc9DGjWv7C0G+rM=
```

سپس [`nix.conf`](../command-ref/conf-file.md) را روی هر ماشینی که قرار است به کش دسترسی داشته باشد، به‌روزرسانی کنید.
URL کش را به [`substituters`](../command-ref/conf-file.md#conf-substituters) و کلید عمومی را به [`trusted-public-keys`](../command-ref/conf-file.md#conf-trusted-public-keys) اضافه کنید:

    substituters = https://cache.nixos.org/ s3://example-nix-cache
    trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= example-nix-cache-1:1/cKDz3QCCOmwcztD2eV6Coggp6rqc9DGjWv7C0G+rM=

ماشین‌هایی که برای کش ساخت (build) انجام می‌دهند باید درایویشن‌ها را با استفاده از کلید خصوصی امضا کنند.
روی آن ماشین‌ها، مسیر فایل کلید را به فیلد [`secret-key-files`](../command-ref/conf-file.md#conf-secret-key-files) در [`nix.conf`](../command-ref/conf-file.md) آن‌ها اضافه کنید:

    secret-key-files = /etc/nix/key.private

ما در مرحلهٔ بعد خدمت پس‌زمینه (daemon) Nix را مجدداً راه‌اندازی خواهیم کرد.

# پیاده‌سازی قلاب پس از ساخت (build hook)

اسکریپت زیر را در `/etc/nix/upload-to-cache.sh` بنویسید:

```bash
#!/bin/sh

set -eu
set -f # disable globbing
export IFS=' '

echo "Uploading paths" $OUT_PATHS
exec nix copy --to "s3://example-nix-cache" $OUT_PATHS
```

> **نکته**
>
> متغیر `$OUT_PATHS` یک فهرست جداشده با فاصله از مسیرهای انبار Nix است. در این حالت، ما انتظار داریم و می‌خواهیم که شل عملیات جداسازی کلمات را انجام دهد تا هر مسیر خروجی به عنوان یک آرگومان جداگانه برای `nix store sign` در نظر گرفته شود. Nix تضمین می‌کند که مسیرها حاوی هیچ فاصله (space) نیستند، با این حال ممکن است یک مسیر انبار حاوی کاراکترهای گلوب (glob) باشد. دستور `set -f` قابلیت گلوبینگ را در شل غیرفعال می‌کند.
> اگر می‌خواهید فایل `.drv` را نیز بارگذاری کنید، متغیر `$DRV_PATH` نیز برای اسکریپت تعریف شده‌است و دقیقاً مانند `$OUT_PATHS` کار می‌کند.

سپس مطمئن شوید که برنامه قلاب توسط کاربر `root` قابل‌اجرا است:

```console
# chmod +x /etc/nix/upload-to-cache.sh
```

# به‌روزرسانی پیکربندی Nix

فایل `/etc/nix/nix.conf` را ویرایش کنید تا با اضافه کردن قطعه‌کد پیکربندی زیر در انتهای آن، قلاب ما اجرا شود:

    post-build-hook = /etc/nix/upload-to-cache.sh

سپس، خدمت پس‌زمینه `nix-daemon` را راه‌اندازی مجدد کنید.

# تست

یک derivation را بسازید، برای مثال:

```console
$ nix-build --expr '(import <nixpkgs> {}).writeText "example" (builtins.toString builtins.currentTime)'
this derivation will be built:
  /nix/store/s4pnfbkalzy5qz57qs6yybna8wylkig6-example.drv
building '/nix/store/s4pnfbkalzy5qz57qs6yybna8wylkig6-example.drv'...
running post-build-hook '/home/grahamc/projects/github.com/NixOS/nix/post-hook.sh'...
post-build-hook: Signing paths /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
post-build-hook: Uploading paths /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
/nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
```

سپس مسیر را از انبار پاک کرده و تلاش کنید آن را از کش باینری جایگزین کنید:

```console
$ rm ./result
$ nix-store --delete /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
```

اکنون، مسیر را از کش کپی کنید:

```console
$ nix-store --realise /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
copying path '/nix/store/m8bmqwrch6l3h8s0k3d673xpmipcdpsa-example from 's3://example-nix-cache'...
warning: you did not specify '--add-root'; the result might be removed by the garbage collector
/nix/store/m8bmqwrch6l3h8s0k3d673xpmipcdpsa-example
```

# نتیجه‌گیری

اکنون ما یک نصب Nix داریم که به‌گونه‌ای پیکربندی شده‌است که به‌طور خودکار هر ساخت محلی را امضا کرده و به یک کش باینری راه دور بارگذاری می‌کند.

پیش از استقرار این پیکربندی در محیط عملیاتی (production)، حتماً [ملاحظات پیاده‌سازی](#implementation-caveats) را بررسی کنید.
