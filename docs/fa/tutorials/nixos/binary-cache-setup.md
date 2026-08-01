---
myst:
  html_meta:
    "description lang=en": "Setting up a binary cache for store objects"
    "keywords": "Nix, caching"
---

(setup-http-binary-cache)=
# راه‌اندازی کش باینری HTTP

یک کش باینری، [اشیای انبار Nix](/pages/nix-manual/store/store-object) پیش‌ساخته را ذخیره کرده و آن‌ها را از طریق شبکه در اختیار سایر ماشین‌ها قرار می‌دهد.
هر ماشینی که دارای یک انبار Nix باشد می‌تواند به عنوان یک کش باینری برای سایر ماشین‌ها عمل کند.

## مقدمه

در این آموزش، یک کش باینری Nix را راه‌اندازی می‌کنید که اشیای انبار را از یک ماشین NixOS از طریق HTTP یا HTTPS سرویس‌دهی می‌کند.

### چه چیزی خواهید آموخت؟

شما یاد خواهید گرفت که چگونه:
- کلیدهای امضا را برای کش خود راه‌اندازی کنید
- سرویس‌های مناسب را روی ماشین NixOS سرویس‌دهی‌کننده کش فعال کنید
- بررسی کنید که راه‌اندازی به درستی کار می‌کند

### به چه چیزهایی نیاز دارید؟

- یک [نصب Nix](<install-nix>) کاری روی ماشین محلی خود

- دسترسی SSH به یک ماشین NixOS برای استفاده به عنوان کش

- اگر با NixOS تازه آشنا شده‌اید، درباره‌ی [سیستم ماژول](module-system-tutorial) بیاموزید و اولین سیستم خود را با [](nixos-vms) پیکربندی کنید.

- (اختیاری) یک آی‌پی عمومی و دامین DNS

  اگر خودتان هاست را میزبانی نمی‌کنید، [هاست‌های سازگار با NixOS](https://wiki.nixos.org/wiki/NixOS_friendly_hosters) را در ویکی NixOS بررسی کنید.
  برای استقرار پیکربندی NixOS خود، آموزش [](provisioning-remote-machines-tutorial) را دنبال کنید.

برای یک کش در یک شبکه محلی، فرض می‌کنیم:
- نام هاست `cache` است (آن را با نام خود یا یک آدرس IP جایگزین کنید)
- هاست، اشیای انبار را از طریق HTTP روی پورت 80 سرویس‌دهی می‌کند (این حالت پیش‌فرض است)

برای یک کش با دسترسی عمومی، فرض می‌کنیم:
- نام دامنه `cache.example.com` است (آن را با نام خود جایگزین کنید)
- هاست، اشیای انبار را از طریق HTTPS روی پورت 443 سرویس‌دهی می‌کند (این حالت پیش‌فرض است)

### چقدر زمان خواهد برد؟

- ۲۵ دقیقه

## راه‌اندازی سرویس‌ها

برای ماشین NixOS که میزبان کش است، یک ماژول پیکربندی جدید در `binary-cache.nix` ایجاد کنید:

```{code-block} nix
{ config, ... }:

{
  services.nix-serve = {
    enable = true;
    secretKeyFile = "/var/secrets/cache-private-key.pem";
  };

  services.nginx = {
    enable = true;
    recommendedProxySettings = true;
    virtualHosts.cache = {
      locations."/".proxyPass = "http://${config.services.nix-serve.bindAddress}:${toString config.services.nix-serve.port}";
    };
  };

  networking.firewall.allowedTCPPorts = [
    config.services.nginx.defaultHTTPListenPort
  ];
}
```

گزینه‌های زیر [`services.nix-serve`] سرویس کش باینری را پیکربندی می‌کنند.

ابزار `nix-serve` از پروتکل‌های IPv6 یا SSL/HTTPS پشتیبانی نمی‌کند.
گزینه‌های [`services.nginx`] برای راه‌اندازی یک پروکسی استفاده می‌شوند که از IPv6 پشتیبانی کرده و درخواست‌های ارسالی به هاست‌نیم `cache` را مدیریت می‌کند.

[`services.nix-serve`]: https://search.nixos.org/options?query=services.nix-serve
[`services.nginx`]: https://search.nixos.org/options?query=services.nginx

:::{important}
یک [بخش HTTPS اختیاری](https-binary-cache) در انتهای این آموزش وجود دارد.
:::

ماژول جدید NixOS را به پیکربندی ماشین موجود اضافه کنید:

```{code-block} nix
{ config, ... }:

{
  imports = [
    ./binary-cache.nix
  ];

  # ...
}
```

از ماشین محلی خود، پیکربندی جدید را مستقر کنید:

```shell-session
nixos-rebuild switch --no-flake --target-host root@cache
```

:::{note}
daemon کش باینری خطاهایی را گزارش خواهد کرد زیرا هنوز هیچ فایل کلید محرمانه‌ای وجود ندارد.
:::

## تولید یک جفت کلید امضا

برای اطمینان از اصالت اشیاء انبار (store objects) موجود در کش، به یک جفت کلید خصوصی و عمومی نیاز دارید.

<!-- TODO: link to the remote builds tutorial for the case where store objects are signed after building them -->

برای تولید یک جفت کلید برای کش باینری، نام هاست نمونه `cache.example.com` را با هاست‌نیم خود جایگزین کنید:

```shell-session
nix-store --generate-binary-cache-key cache.example.com cache-private-key.pem cache-public-key.pem
```

فایل `cache-private-key.pem` توسط خدمت پس‌زمینه کش باینری برای امضای باینری‌ها در هنگام ارائه آن‌ها استفاده خواهد شد.
آن را در مسیری که در گزینه `services.nix-serve.secretKeyFile` روی ماشینی که میزبان کش است پیکربندی شده‌است، کپی کنید:

```shell-session
scp cache-private-key.pem root@cache:/var/secrets/cache-private-key.pem
```

تاکنون، خدمت پس‌زمینه (daemon) کش باینری به دلیل نبود فایل کلید مخفی در حلقه راه‌اندازی مجدد (restart loop) قرار داشت.
بررسی کنید که اکنون به درستی کار می‌کند:

```shell-session
ssh root@cache systemctl status nix-serve.service
```

:::{important}
[](custom-binary-cache) با استفاده از `cache-public-key.pem` روی ماشین محلی خود.
:::

## بررسی دسترسی

مراحل زیر بررسی می‌کنند که آیا همه چیز به درستی راه‌اندازی شده‌است یا خیر و ممکن است در شناسایی مشکلات کمک کنند.

### بررسی دسترسی عمومی

با پرس‌وجو از کش، بررسی کنید که آیا کش باینری، پروکسی معکوس و قوانین فایروال همان‌طور که در نظر گرفته شده‌اند کار می‌کنند یا خیر:

```shell-session
$ curl http://cache/nix-cache-info
StoreDir: /nix/store
WantMassQuery: 1
Priority: 30
```

### بررسی امضای شیء انبار

برای آزمایش اینکه آیا اشیاء انبار به درستی امضا شده‌اند یا خیر، متادیتا (فراطلاعات) یک درایویشن نمونه را بررسی کنید.
روی هاست کش باینری، بسته `hello` را بسازید و فایل `.narinfo` را از کش دریافت کنید:

```shell-session
$ hash=$(nix-build '<nixpkgs>' -A pkgs.hello | awk -F '/' '{print $4}' | awk -F '-' '{print $1}')
$ curl "http://cache/$hash.narinfo" | grep "Sig: "
...
Sig: cache.example.org:GyBFzocLAeLEFd0hr2noK84VzPUw0ArCNYEnrm1YXakdsC5FkO2Bkj2JH8Xjou+wxeXMjFKa0YP2AML7nBWsAg==
```

(https-binary-cache)=
### ارائه کش باینری از طریق HTTPS

اگر کش باینری به‌صورت عمومی قابل دسترسی باشد، می‌توان HTTPS را با استفاده از گواهی‌های SSL [Let's Encrypt](https://letsencrypt.org/) اعمال کرد.
فایل `binary-cache.nix` خود را مانند زیر ویرایش کنید و مطمئن شوید که URL و آدرس ایمیل نمونه را با اطلاعات خود جایگزین می‌کنید:

```{code-block} diff
   services.nginx = {
     enable = true;
     recommendedProxySettings = true;
-    virtualHosts.cache = {
+    virtualHosts."cache.example.com" = {
+      enableACME = true;
+      forceSSL = true;
       locations."/".proxyPass = "http://${config.services.nix-serve.bindAddress}:${toString config.services.nix-serve.port}";
     };
   };

+   security.acme = {
+     acceptTerms = true;
+     certs = {
+       "cache.example.com".email = "you@example.com";
+     };
+   };

   networking.firewall.allowedTCPPorts = [
     config.services.nginx.defaultHTTPListenPort
+    config.services.nginx.defaultSSLListenPort
   ];
```

برای استقرار این تغییرات، سیستم را بازسازی (rebuild) کنید:

```shell-session
nixos-rebuild switch --no-flake --target-host root@cache.example.com
```

## گام‌های بعدی

اگر کش باینری شما در حال حاضر یک [ماشین بیلد راه دور](/pages/nix-manual/advanced-topics/distributed-builds) است، تمام اشیاء انبار را در انبار Nix خود سرویس‌دهی خواهد کرد.

- [](custom-binary-cache) با استفاده از نام هاست کش باینری و کلید عمومی تولیدشده
- [](post-build-hooks) برای بارگذاری اشیاء انبار به کش باینری
- [](distributed-build-setup-tutorial)

برای صرفه‌جویی در فضای ذخیره‌سازی، لطفاً به صفات پیکربندی NixOS زیر مراجعه کنید:

- [`nix.gc`](https://search.nixos.org/options?query=nix.gc): گزینه‌ها برای جمع‌آوری زباله خودکار
- [`nix.optimise`](https://search.nixos.org/options?query=nix.optimise): گزینه‌ها برای بهینه‌سازی دوره‌ای انبار Nix

## جایگزین‌ها

- [`nix-serve-ng`](https://github.com/aristanetworks/nix-serve-ng): جایگزینی بی‌نقص و آماده برای `nix-serve` که به زبان Haskell نوشته شده‌است

- [انبار SSH](/pages/nix-manual/store/types)، [انبار SSH تجربی](/pages/nix-manual/store/types) و [انبار کش باینری S3](/pages/nix-manual/store/types) نیز می‌توانند برای سرویس‌دهی یک کش استفاده شوند.
  ارائه‌دهندگان تجاری زیادی برای ذخیره‌سازی سازگار با S3 وجود دارند، برای مثال:
  - Amazon S3
  - Tigris
  - Cloudflare R2

- [attic](https://github.com/zhaofengli/attic): سرور کش باینری Nix پشتیبانی‌شده توسط یک ارائه‌دهنده ذخیره‌سازی سازگار با S3

- [Cachix](https://www.cachix.org): کش باینری Nix به عنوان یک سرویس

## مراجع

- [راهنمای Nix در انبار کش باینری HTTP](/pages/nix-manual/store/types)
- [`services.nix-serve` گزینه‌های ماژول][`services.nix-serve`]
- [`services.nginx` گزینه‌های ماژول][`services.nginx`]
