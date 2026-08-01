---
myst:
  html_meta:
    "description lang=en": "Building and running Docker images"
    "keywords": "Docker, containers, Nix, reproducible, build, tutorial"
---

(nixos-docker-images)=
# ساخت و اجرای تصاویر داکر

[Docker](https://www.docker.com/) مجموعه‌ای از ابزارها و سرویس‌ها است که برای ساخت، مدیریت و استقرار کنتینرها استفاده می‌شود.

بسیاری از پلتفرم‌های ابری، میزبانی کنتینر مبتنی بر Docker را ارائه می‌دهند.
ایجاد کنتینرهای Docker یک وظیفه رایج هنگام ساخت نرم‌افزار بازتولیدپذیر است.
در این آموزش، شما یادمی‌گیرید چگونه با استفاده از Nix، کنتینرهای Docker بسازید.

## پیش‌نیازها

شما به نصب هم‌زمان Nix و [Docker](https://docs.docker.com/get-docker/) نیاز خواهید داشت.
Docker در `nixpkgs` موجود است، که روش ترجیحی برای نصب آن روی NixOS محسوب می‌شود.
با این حال، اگر روی توزیع لینوکس دیگری یا macOS هستید، می‌توانید از نصب بومی Docker در سیستم‌عامل خود نیز استفاده کنید.

## ساخت نخستین کنتینر

مجموعهٔ بسته‌های نیکس (Nixpkgs) ابزار `dockerTools` را برای ایجاد تصاویر داکر فراهم می‌کند:

```nix
{ pkgs ? import <nixpkgs> { }
, pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; }
}:

pkgs.dockerTools.buildImage {
  name = "hello-docker";
  config = {
    Cmd = [ "${pkgsLinux.hello}/bin/hello" ];
  };
}
```

:::{note}
اگر در حال اجرای **macOS** یا هر پلتفرم دیگری به جز `x86_64-linux` هستید، لازم است یکی از کارهای زیر را انجام دهید:

- [راه‌اندازی ساخت‌های توزیع‌شده](distributed-build-setup-tutorial) برای ساخت روی لینوکس
- [کامپایل متقاطع](cross-compilation) به لینوکس با جایگزین کردن `pkgsLinux.hello` با `pkgs.pkgsCross.musl64.hello`
:::

تابع `dockerTools.buildImage` را فراخوانی کرده و چند پارامتر به آن ارسال می‌کنیم:

- یک `name` برای تصویر خود
- بخش `config` شامل دستوری که باید پس از شروع به کار کنتینر اجرا شود (`Cmd`). در اینجا ما به بسته GNU hello از Nixpkgs ارجاع داده و فایل اجرایی آن را در کنتینر اجرا می‌کنیم.

این را در فایل `hello-docker.nix` ذخیره کرده و آن را بسازید:

```shell-session
$ nix-build hello-docker.nix
these derivations will be built:
  /nix/store/qpgdp0qpd8ddi1ld72w02zkmm7n87b92-docker-layer-hello-docker.drv
  /nix/store/m4xyfyviwbi38sfplq3xx54j6k7mccfb-runtime-deps.drv
  /nix/store/v0bvy9qxa79izc7s03fhpq5nqs2h4sr5-docker-image-hello-docker.tar.gz.drv
warning: unknown setting 'experimental-features'
building '/nix/store/qpgdp0qpd8ddi1ld72w02zkmm7n87b92-docker-layer-hello-docker.drv'...
No contents to add to layer.
Packing layer...
Computing layer checksum...
Finished building layer 'hello-docker'
building '/nix/store/m4xyfyviwbi38sfplq3xx54j6k7mccfb-runtime-deps.drv'...
building '/nix/store/v0bvy9qxa79izc7s03fhpq5nqs2h4sr5-docker-image-hello-docker.tar.gz.drv'...
Adding layer...
tar: Removing leading `/' from member names
Adding meta...
Cooking the image...
Finished.
/nix/store/y74sb4nrhxr975xs7h83izgm8z75x5fc-docker-image-hello-docker.tar.gz
```

برچسب تصویر (`y74sb4nrhxr975xs7h83izgm8z75x5fc`) به هش ساخت Nix اشاره دارد و تضمین می‌کند که تصویر داکر مربوط به ساخت Nix ما است.
مسیر انبار در آخرین خط خروجی به تصویر داکر اشاره دارد.

## اجرای کنتینر

برای کار با کنتینر، این تصویر را از پیوند نمادین پیش‌فرض `result` که توسط `nix-build` ایجاد شده‌است، به ریجستری تصویر داکر بارگذاری کنید:

```shell-session
$ docker load < result
Loaded image: hello-docker:y74sb4nrhxr975xs7h83izgm8z75x5fc
```

شما همچنین می‌توانید از مسیر انبار برای بارگذاری تصویر استفاده کنید تا از وابستگی به وجود `result` جلوگیری کنید:

```shell-session
$ docker load < /nix/store/y74sb4nrhxr975xs7h83izgm8z75x5fc-docker-image-hello-docker.tar.gz
Loaded image: hello-docker:y74sb4nrhxr975xs7h83izgm8z75x5fc
```

حتی راحت‌تر از آن، می‌توانید همه کارها را با یک دستور انجام دهید.
مزیت این روش این است که اگر تغییری وجود داشته باشد، `nix-build` تصویر را مجدداً می‌سازد و مسیر انبار جدید را به `docker load` ارسال می‌کند:

```shell-session
$ docker load < $(nix-build hello-docker.nix)
Loaded image: hello-docker:y74sb4nrhxr975xs7h83izgm8z75x5fc
```

اکنون که تصویر را در Docker بارگذاری کرده‌اید، می‌توانید آن را اجرا کنید:

```shell-session
$ docker run -t hello-docker:y74sb4nrhxr975xs7h83izgm8z75x5fc
Hello, world!
```

## کار با تصاویر داکر

مقدمه‌ای عمومی بر کار با تصاویر داکر بخشی از این آموزش نیست.
[مستندات رسمی داکر](https://docs.docker.com/) منبع بسیار بهتری برای این منظور است.

توجه داشته باشید که وقتی تصاویر داکر خود را با Nix می‌سازید، احتمالاً نیازی به نوشتن یک `Dockerfile` نخواهید داشت، زیرا Nix قابلیت‌های Dockerfile را در بوم‌سازگان داکر جایگزین می‌کند.
با این وجود، درک ساختار یک Dockerfile همچنان ممکن است برای فهمیدن نحوه جایگزینی هر یک از عملکردهای آن توسط Nix مفید باشد.
از سوی دیگر، بسته به مورد استفاده شما، استفاده از رابط خط فرمان داکر (CLI)، Docker Compose، Docker Swarm یا Docker Hub همچنان می‌تواند مرتبط باشد.

## گام‌های بعدی

- جزئیات بیشتر در مورد نحوه استفاده از `dockerTools` را می‌توانید در [مستندات مرجع](https://nixos.org/nixpkgs/manual/#sec-pkgs-dockerTools) پیدا کنید.
- شاید تمایل داشته باشید نمونه‌های بیشتری از [تصاویر داکر ساخته‌شده با Nix](https://github.com/NixOS/nixpkgs/blob/master/pkgs/build-support/docker/examples.nix) را مرور کنید.
- نگاهی به [Arion](https://docs.hercules-ci.com/arion/) بیندازید؛ یک ابزار پوششی برای `docker-compose` که پشتیبانی درجه‌یکی از Nix ارائه می‌دهد.
- ساخت تصاویر داکر در یک {ref}`CI با GitHub Actions <github-actions>`.
