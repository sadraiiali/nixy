# استفاده از Nix در داخل Docker

برای اجرای جدیدترین نسخه پایدار Nix با Docker، دستور زیر را اجرا کنید:

```console
$ docker run -ti docker.io/nixos/nix
Unable to find image 'docker.io/nixos/nix:latest' locally
latest: Pulling from docker.io/nixos/nix
5843afab3874: Pull complete
b52bf13f109c: Pull complete
1e2415612aa3: Pull complete
Digest: sha256:27f6e7f60227e959ee7ece361f75d4844a40e1cc6878b6868fe30140420031ff
Status: Downloaded newer image for docker.io/nixos/nix:latest
35ca4ada6e96:/# nix --version
nix (Nix) 2.3.12
35ca4ada6e96:/# exit
```

> اگر نسخه پیش‌انتشار جدیدتری می‌خواهید، می‌توانید از `ghcr.io/nixos/nix` استفاده کرده و آن‌ها را در https://github.com/nixos/nix/pkgs/container/nix مشاهده کنید.

# چه چیزی در تصویر داکر Nix گنجانده شده است؟

تصویر داکر رسمی با استفاده از `pkgs.dockerTools.buildLayeredImage` (و نه با `Dockerfile` که در تصاویر داکر مرسوم است) ساخته می‌شود. با این حال، همچنان می‌توانید مانند هر تصویر داکر دیگری، تصویر داکر سفارشی خود را بر پایه آن بنا کنید.

همچنین، این تصویر داکر بر پایه هیچ تصویر دیگری نیست و شامل حداقل مجموعه از وابستگی‌های زمان اجرا است که برای استفاده از Nix لازم هستند:

 - pkgs.nix
 - pkgs.bashInteractive
 - pkgs.coreutils-full
 - pkgs.gnutar
 - pkgs.gzip
 - pkgs.gnugrep
 - pkgs.which
 - pkgs.curl
 - pkgs.less
 - pkgs.wget
 - pkgs.man
 - pkgs.cacert.out
 - pkgs.findutils

# تصویر داکر با جدیدترین نسخه توسعه Nix

برای دریافت جدیدترین تصویری که توسط [Hydra](https://hydra.nixos.org) ساخته شده است، دستور زیر را اجرا کنید:

```console
$ curl -L https://hydra.nixos.org/job/nix/master/dockerImage.x86_64-linux/latest/download/1 | docker load
$ docker run -ti nix:2.5pre20211105
```

همچنین می‌توانید خودتان یک تصویر داکر را از کد منبع بسازید:

```console
$ nix build ./\#hydraJobs.dockerImage.x86_64-linux
$ docker load -i ./result/image.tar.gz
$ docker run -ti nix:2.5pre20211105
```

# تصویر داکر با Nix بدون دسترسی ویژه

اگر می‌خواهید Nix را درون یک کنتیر با کاربری غیر از `root` اجرا کنید، می‌توانید با مشخص کردن آرگومان‌های `uid`، `gid`، `uname` و `gname` برای `docker.nix`، تصویری با نصب تک‌کاربره غیررایوت (non-root) از Nix بسازید:

```console
$ nix build --file docker.nix \
    --arg uid 1000 \
    --arg gid 1000 \
    --argstr uname user \
    --argstr gname user \
    --argstr name nix-user \
    --out-link nix-user.tar.gz
$ docker load -i nix-user.tar.gz
$ docker run -ti nix-user
```
