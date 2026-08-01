# <a id="install-nix"></a> نصب Nix
پیش‌نیازها:
 - پیش از نصب، ممکن است ابتدا لازم باشد `xz-utils` یا ابزارهای مشابه را برای استخراج فایل tarball باینری Nix (`.tar.xz`) که از طریق اسکریپت‌های زیر بارگیری می‌شود، نصب کنید.

**لینوکس**
نصب Nix از طریق [نصب چندکاربره] توصیه شده:

```shell
$ curl -L https://nixos.org/nix/install | sh -s -- --daemon
```

در آرچ لینوکس (Arch Linux)، به عنوان روشی جایگزین می‌توانید [Nix را از طریق `pacman` نصب کنید](https://wiki.archlinux.org/title/Nix#Installation).

در فدورا (Fedora)، می‌توانید [Nix را از طریق `dnf` نصب کنید](https://src.fedoraproject.org/rpms/nix).

**macOS**
Nix را از طریق [نصب چندکاربره] توصیه‌شده نصب کنید:

```shell
$ curl -L https://nixos.org/nix/install | sh
```

> <span class="admonition-kind" data-kind="important"></span>
>
> **مهم**
>
> **به‌روزرسانی به macOS 15 Sequoia**
>
> اگر اخیراً به macOS 15 Sequoia به‌روزرسانی کرده‌اید و خطای زیر را دریافت می‌کنید:

> ```shell
> error: the user '_nixbld1' in the group 'nixbld' does not exist
> ```
> هنگام اجرای دستورات Nix، برای راهنمایی جهت اصلاح نصب خود بدون نیاز به نصب مجدد، به مسئلهٔ گیت‌هاب [NixOS/nix#10892](https://github.com/NixOS/nix/issues/10892) مراجعه کنید.

**ویندوز (WSL2)**
Nix را از طریق [نصب تک‌کاربره] توصیه شده نصب کنید:

```shell
$ curl -L https://nixos.org/nix/install | sh -s -- --no-daemon
```

با این حال، اگر [پشتیبانی سیستمد] را فعال کرده‌اید، Nix را از طریق [نصب چندکاربره] توصیه شده نصب کنید:

```shell
$ curl -L https://nixos.org/nix/install | sh -s -- --daemon
```

[پشتیبانی systemd]: https://learn.microsoft.com/en-us/windows/wsl/wsl-config#systemd-support

**Docker**
یک شل Docker با Nix را راه‌اندازی کنید:

```shell
$ docker run -it nixos/nix
```

یا یک شل Docker همراه با Nix که یک پوشه `workdir` را ارائه می‌دهد، راه‌اندازی کنید:

```shell
$ mkdir workdir
$ docker run -it -v $(pwd)/workdir:/workdir nixos/nix
```

مثال `workdir` از بالا را می‌توان برای شروع توسعه و برنامه‌نویسی روی Nixpkgs نیز به کار برد:

```shell
$ git clone git@github.com:NixOS/nixpkgs
$ docker run -it -v $(pwd)/nixpkgs:/nixpkgs nixos/nix
bash-5.1# nix-build -I nixpkgs=/nixpkgs -A hello
bash-5.1# find ./result # this symlink points to the build package
```

## تأیید نصب

با باز کردن **یک ترمینال جدید** و تایپ دستور زیر، نصب را بررسی کنید:

```shell
$ nix --version
nix (Nix) 2.11.0
```

[نصب چندکاربره]: /pages/nix-manual/installation/multi-user
[نصب تک‌کاربره]: /pages/nix-manual/installation/single-user
