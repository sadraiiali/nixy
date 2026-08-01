# <a id="bootable-iso-image"></a> ساخت یک تصویر ISO قابل بوت

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> اگر نیاز دارید تصاویری برای یک پلتفرم متفاوت بسازید، به بخش [کامپایل متقاطع](https://github.com/nix-community/nixos-generators#user-content-cross-compiling) مراجعه کنید.

ممکن است متوجه شوید که یک تصویر نصب رسمی فاقد برخی از پشتیبانی‌های سخت‌افزاری است.

راه‌حل این است که فایل `myimage.nix` را ایجاد کنید تا با استفاده از ISO نصب مینیمال، به جدیدترین هسته (kernel) اشاره کند:

```nix
{ pkgs, modulesPath, lib, ... }: {
  imports = [
    "${modulesPath}/installer/cd-dvd/installation-cd-minimal.nix"
  ];

  # use the latest Linux kernel
  boot.kernelPackages = pkgs.linuxPackages_latest;

  # Needed for https://github.com/NixOS/nixpkgs/issues/58959
  boot.supportedFilesystems = lib.mkForce [ "btrfs" "reiserfs" "vfat" "f2fs" "xfs" "ntfs" "cifs" ];
}
```

یک تصویر ISO با پیکربندی بالا تولید کنید:

```shell
$ NIX_PATH=nixpkgs=https://github.com/NixOS/nixpkgs/archive/74e2faf5965a12e8fa5cff799b1b19c6cd26b0e3.tar.gz nix-shell -p nixos-generators --run "nixos-generate --format iso --configuration ./myimage.nix -o result"
```

با جایگزین کردن `sdX` با نام دستگاه خود، تصویر جدید را روی حافظه USB خود کپی کنید:

```shell
$ dd if=result/iso/*.iso of=/dev/sdX status=progress
$ sync
```

## گام‌های بعدی

- نگاهی به این [فهرست فرمت‌های پشتیبانی‌شده توسط مولدها](https://github.com/nix-community/nixos-generators#user-content-supported-formats) بیندازید تا ارائه‌دهنده ابری یا فناوری مجازی‌سازی خود را پیدا کنید.
- نگاهی به [راهنمای جایگزین برای ایجاد یک دیسک زنده (Live CD) NixOS](https://wiki.nixos.org/wiki/Creating_a_NixOS_live_CD) بیندازید.
