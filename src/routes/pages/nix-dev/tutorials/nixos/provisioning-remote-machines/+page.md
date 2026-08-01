# <a id="provisioning-remote-machines-tutorial"></a> آموزش پیکربندی و آماده‌سازی ماشین‌های راه دور از طریق SSH

امکان جایگزینی هر نوع نصب لینوکس با یک پیکربندی NixOS روی سیستم‌های در حال اجرا با استفاده از [`nixos-anywhere`] و [`disko`] وجود دارد.

[`nixos-anywhere`]: https://nix-community.github.io/nixos-anywhere/
[`disko`]: https://github.com/nix-community/disko

## مقدمه

در این آموزش، یک پیکربندی NixOS را روی یک رایانه در حال اجرا مستقر می‌کنید.

### چه چیزی خواهید آموخت؟

شما یاد خواهید گرفت که چگونه:
- یک پیکربندی حداقلی NixOS با طرح‌بندی دیسک اعلانی و دسترسی SSH را مشخص کنید
- معتبر بودن یک پیکربندی را بررسی کنید
- یک پیکربندی NixOS را روی یک ماشین راه دور مستقر و به‌روزرسانی کنید

### به چه چیزی نیاز دارید؟

- آشنایی با [زبان Nix](/pages/nix-dev/tutorials/nix-language)
- آشنایی با [module-system-tutorial](/pages/nix-dev/tutorials/module-system)

برای یک نصب خودکار موفق، اطمینان حاصل کنید که *ماشین هدف* دارای شرایط زیر است:

- یک ماشین مجازی QEMU باشد که لینوکس را اجرا می‌کند
  - با پشتیبانی از [`kexec`](https://en.wikipedia.org/wiki/Kexec)
  - روی معماری مجموعه دستورالعمل (ISA) `x86-64` یا `aarch64`
  - با حداقل ۱ گیگابایت (GB) رم (RAM)

  این سیستم همچنین می‌تواند یک سیستم زنده (Live) بوت‌شده از USB باشد، مانند [نصب‌کننده NixOS](https://nixos.org/download/#download-nixos-accordion).

- آدرس IP به‌طور خودکار با DHCP پیکربندی شده باشد
  - امکان ورود به سیستم از طریق SSH را داشته باشید
  - با احراز هویت کلید عمومی (ترجیح داده می‌شود) یا رمز عبور
  - به عنوان کاربر `root` یا کاربر دیگری با دسترسی‌های `sudo`

*ماشین محلی* فقط به یک [نصب Nix](/pages/nix-dev/install-nix) فعال نیاز دارد.

ما در این آموزش به *ماشین هدف* `target-machine` می‌گوییم.
آن را با نام هاست یا آدرس IP واقعی جایگزین کنید.

## آماده‌سازی محیط

یک پوشه پروژه جدید ایجاد کنید و با شل (Shell) خود وارد آن شوید:

```shell
mkdir remote
cd remote
```

[تعیین وابستگی‌ها](/pages/nix-dev/guides/recipes/dependency-management) روی `nixpkgs`، `disko` و `nixos-anywhere`：

```shell
$ nix-shell -p npins
[nix-shell:remote]$ npins init
[nix-shell:remote]$ npins add github nix-community disko
[nix-shell:remote]$ npins add github nix-community nixos-anywhere
```

یک فایل جدید `shell.nix` ایجاد کنید که تمام ابزارهای موردنیاز را با استفاده از وابستگی‌های سنجاق‌شده فراهم می‌کند:

```nix
let
  sources = import ./npins;
  pkgs = import sources.nixpkgs {};
in

pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    npins
    nixos-anywhere
    nixos-rebuild
  ];
  shellHook = ''
    export NIX_PATH="nixpkgs=${sources.nixpkgs}:nixos-config=$PWD/configuration.nix"
  '';
}
```

اکنون از محیط موقت خارج شده و وارد محیط جدید مشخص‌شده شوید:

```shell
[nix-shell:remote]$ exit
$ nix-shell
```

این محیط شل آماده است تا از نسخه‌های خوش‌تعریف Nixpkgs به همراه `nixos-anywhere` و `nixos-rebuild` استفاده کند.

> <span class="admonition-kind" data-kind="important"></span>
>
> **مهم**
>
> تمام دستورات زیر را در این محیط اجرا کنید.

## ایجاد یک پیکربندی NixOS

پیکربندی جدید NixOS شامل پیکربندی عمومی سیستم و مشخصات چیدمان دیسک خواهد بود.

چیدمان دیسک در این مثال یک دیسک تکی را توصیف می‌کند که دارای یک رکورد راه‌اندازی اصلی [master boot record](https://en.wikipedia.org/wiki/Master_boot_record) (MBR) و پارتیشن سیستم [EFI system partition](https://en.wikipedia.org/wiki/EFI_system_partition) (ESP)، و یک سیستم‌فایل ریشه است که تمام فضای خالی باقی‌مانده را اشغال می‌کند.
این تنظیم هم روی سیستم‌های EFI و هم BIOS کار خواهد کرد.

یک فایل جدید به نام `single-disk-layout.nix` با مشخصات چیدمان دیسک ایجاد کنید:

```nix
{ ... }:

{
  disko.devices.disk.main = {
    type = "disk";
    content = {
      type = "gpt";
      partitions = {
        MBR = {
          priority = 0;
          size = "1M";
          type = "EF02";
        };
        ESP = {
          priority = 1;
          size = "500M";
          type = "EF00";
          content = {
            type = "filesystem";
            format = "vfat";
            mountpoint = "/boot";
          };
        };
        root = {
          priority = 2;
          size = "100%";
          content = {
            type = "filesystem";
            format = "ext4";
            mountpoint = "/";
          };
        };
      };
    };
  };
}
```

فایل `configuration.nix` را ایجاد کنید که تعریف طرح‌بندی دیسک را درون‌ریزی کرده و مشخص می‌کند کدام دیسک باید فرمت شود:

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> اگر شناسه دستگاه دیسک هدف را نمی‌دانید، تمام دستگاه‌های روی *ماشین هدف* را با دستور `lsblk` فهرست کنید:
>

> ```shell
> $ ssh target-machine lsblk
> NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
> sda      8:0    0   256G  0 disk
> ├─sda1   8:1    0 248.5G  0 part /nix/store
> │                                /
> └─sda2   8:2    0   7.5G  0 part [SWAP]
> sr0     11:0    1  1024M  0 rom
> ```
>
> در این مثال، نام دیسک `sda` است.
> مسیر بلاک دیسک (block device) به شکل `/dev/sda` خواهد بود.
> آن مقدار را برای بعد به خاطر بسپارید.

```nix
{ modulesPath, ... }:

let
  diskDevice = "/dev/sda";
  sources = import ./npins;
in
{
  imports = [
    (modulesPath + "/profiles/qemu-guest.nix")
    (sources.disko + "/module.nix")
    ./single-disk-layout.nix
  ];

  disko.devices.disk.main.device = diskDevice;

  boot.loader.grub = {
    devices = [ diskDevice ];
    efiSupport = true;
    efiInstallAsRemovable = true;
  };

  services.openssh.enable = true;

  users.users.root.openssh.authorizedKeys.keys = [
    "<your SSH key here>"
  ];

  system.stateVersion = "24.11";
}
```

> <span class="admonition-kind" data-kind="important"></span>
>
> **مهم**
>
> مسیر `/dev/sda` را با مسیر دستگاه بلوکی دیسک خود جایگزین کنید.
>
> رشته‌ی `&lt;your SSH key here&gt;` را با کلید عمومی SSH که می‌خواهید برای ورودهای آینده به عنوان کاربر `root` استفاده کنید، جایگزین کنید.

**توضیح تفصیلی**
متغیر `diskDevice` در بلوک `let` مسیر دستگاه بلوکی دیسک را تعریف می‌کند:

```nix
let
  diskDevice = "/dev/sda";
  sources = import ./npins;
in
```

این گزینه برای تعیین هدف پارتیشن‌بندی و فرمت‌بندی همان‌طور که در مشخصات طرح‌بندی دیسک توضیح داده شده است، استفاده می‌شود.
همچنین در پیکربندی راه‌انداز بوت استفاده می‌شود تا امکان راه‌اندازی آن هم روی سیستم‌های قدیمی BIOS و هم UEFI فراهم شود:

```nix
  disko.devices.disk.main.device = diskDevice;

  boot.loader.grub = {
    devices = [ diskDevice ];
    efiSupport = true;
    efiInstallAsRemovable = true;
  };
```

ماژول `qemu-guest.nix` این سیستم را برای اجرا در داخل یک ماشین مجازی QEMU سازگار می‌کند:

```nix
  imports = [
    (modulesPath + "/profiles/qemu-guest.nix")
    (sources.disko + "/module.nix")
    ./single-disk-layout.nix
  ];
```

بر اساس مشخصات طرح‌بندی دیسک، کتابخانه `disko` یک اسکریپت پارتیشن‌بندی و بخشی از پیکربندی NixOS را تولید می‌کند که پارتیشن‌ها را به همان نسبت در زمان بوت (ra'andazi) مونتاژ می‌کند.
خط اول کتابخانه را درون‌ریزی می‌کند و خط دوم طرح‌بندی دیسک را اعمال می‌کند:

```nix
  imports = [
    (modulesPath + "/profiles/qemu-guest.nix")
    (sources.disko + "/module.nix")
    ./single-disk-layout.nix
  ];
```

## تست چیدمان دیسک

بررسی کنید که چیدمان دیسک معتبر باشد:

```shell
nix-build -E "((import <nixpkgs> {}).nixos [ ./configuration.nix ]).installTest"
```

این دستور کل فرآیند نصب را با ساخت یک derivation در صفت `installTest` که توسط ماژول `disko` ارائه شده است، درون یک ماشین مجازی اجرا می‌کند.

## استقرار سیستم

برای استقرار سیستم، پیکربندی و اسکریپت قالب‌بندی دیسک مربوطه را ساخته و `nixos-anywhere` را با استفاده از نتایج اجرا کنید:

> <span class="admonition-kind" data-kind="important"></span>
>
> **مهم**
>
> مقدار `target-host` را با نام هاست یا آدرس IP *ماشین هدف* خود جایگزین کنید.

```shell
toplevel=$(nixos-rebuild build --no-flake)
diskoScript=$(nix-build -E "((import <nixpkgs> {}).nixos [ ./configuration.nix ]).diskoScript")
nixos-anywhere --store-paths "$diskoScript" "$toplevel" root@target-host
```

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> اگر احراز هویت با کلید عمومی را ندارید:
> متغیر محیطی `SSH_PASS` را روی رمز عبور خود تنظیم کنید و سپس پرچم `--env-password` را به دستور `nixos-anywhere` اضافه کنید.

اکنون ابزار `nixos-anywhere` به سیستم مقصد وارد می‌شود، دیسک را پارتیشن‌بندی، قالب‌بندی و متصل (mount) می‌کند و پیکربندی NixOS را نصب می‌کند.
سپس، سیستم را راه‌اندازی مجدد (Reboot) می‌کند.

## به‌روزرسانی سیستم

برای به‌روزرسانی سیستم، `npins` را اجرا کرده و پیکربندی را مجدداً مستقر کنید:

```shell
npins update nixpkgs
nixos-rebuild switch --no-flake --target-host root@target-host
```

ابزار `nixos-anywhere` دیگر مورد نیاز نیست، مگر اینکه بخواهید چیدمان دیسک را تغییر دهید.

# گام‌های بعدی

- [binary-cache-setup](/pages/nix-dev/tutorials/nixos/binary-cache-setup)
- [post-build-hooks](/pages/nix-dev/guides/recipes/post-build-hook)

## مراجع

- [`nixos-anywhere` project page][`nixos-anywhere`]
- [`disko` project repository][`disko`]
- [مجموعه‌ای از نمونه‌های چیدمان دیسک](https://github.com/nix-community/disko/tree/master/example)
