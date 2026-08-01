---
myst:
  html_meta:
    "description lang=en": "Installing NixOS on a Raspberry Pi"
    "keywords": "Raspberry Pi, rpi, NixOS, installation, image, tutorial"
---

# نصب NixOS روی یک رسبری پای (Raspberry Pi)

این آموزش فرض می‌کند که شما یک [رسبری پای ۴ مدل B با ۴ گیگابایت رم (Raspberry Pi 4 Model B with 4GB RAM)](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) دارید.

پیش از شروع این آموزش، مطمئن شوید که تمام [سخت‌افزار لازم](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/1) را در اختیار دارید:

- کابل/آدابتور HDMI.
- کارت حافظه اس‌دی (SD) با ظرفیت ۸ گیگابایت یا بیشتر.
- کارت‌خوان اس‌دی (چنانچه سیستم شما اسلات اس‌دی ندارد).
- کابل برق برای رسبری پای خود.
- صفحه کلید USB.

:::{note}
این آموزش برای رسبری پای 4B نوشته شده‌است. استفاده از مدل‌های پشتیبانی‌شده‌ی قبلی مانند 3B یا 3B+ با اعمال برخی تغییرات در این آموزش امکان‌پذیر است.
:::

## راه‌اندازی (بوت) تصویر زنده NixOS

:::{note}
راه‌اندازی از روی USB ممکن است نیازمند ارتقای سفت‌افزار EEPROM باشد. این آموزش برای جلوگیری از چنین مشکلاتی، از یک کارت حافظه اس‌دی برای بوت استفاده می‌کند.
:::

برای آماده‌سازی تصویر AArch64 روی دستگاه دیگری که نیکس (Nix) را دارد، دستورات زیر را اجرا کنید:

```shell-session
$ nix-shell -p wget zstd

[nix-shell:~]$ wget https://hydra.nixos.org/build/226381178/download/1/nixos-sd-image-23.11pre500597.0fbe93c5a7c-aarch64-linux.img.zst
[nix-shell:~]$ unzstd -d nixos-sd-image-23.11pre500597.0fbe93c5a7c-aarch64-linux.img.zst
[nix-shell:~]$ dmesg --follow
```

:::{note}
شما می‌توانید یک تصویر به‌روز را از [Hydra](https://hydra.nixos.org/job/nixos/trunk-combined/nixos.sd_image.aarch64-linux) بارگیری کنید؛
برای این کار روی آخرین ساخت موفق (که با علامت تیک سبز مشخص شده‌است) کلیک کرده و پیوند مربوط به تصویر فرآورده‌ی ساخت را کپی کنید.
:::

:::{note}
اگر روی سیستمی هستید که امکان استفاده از آن وجود دارد، شاید راحت‌تر باشد که برای فلش کردن تصویر روی کارت حافظه اس‌دی خود از نرم‌افزاری مانند [Etcher](https://www.balena.io/etcher/) استفاده کنید.
:::

ترمینال شما باید پیام‌های هسته (kernel) را با دریافت آن‌ها چاپ کند.

کارت حافظه اس‌دی خود را متصل کنید و ترمینال باید دستگاه اختصاص‌یافته به آن، برای مثال `/dev/sdX` را چاپ کند.

برای متوقف کردن دستور `dmesg --follow`، کلیدهای <kbd>Ctrl</kbd>+<kbd>C</kbd> را فشار دهید.

با جایگزین کردن `sdX` با نام دستگاه خود در دستور زیر، NixOS را روی کارت حافظه اس‌دی خود کپی کنید:

```console
[nix-shell:~]$ sudo dd if=nixos-sd-image-23.11pre500597.0fbe93c5a7c-aarch64-linux.img of=/dev/sdX bs=4096 conv=fsync status=progress
```

پس از خروج از آن دستور، **کارت حافظه اس‌دی را به Raspberry Pi خود منتقل کرده و آن را روشن کنید**.

باید با یک شل تازه مواجه شوید.

در صورتی که تصویر بوت نشد، ارزش دارد که [سفت‌افزار را به‌روزرسانی کرده](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#bootloader_update_stable) و تصویر را دوباره بوت کنید.

## دریافت اتصال اینترنت

دستور `sudo -i` را اجرا کنید تا یک شل روت برای ادامه این آموزش دریافت کنید.

در این مرحله به اتصال اینترنت نیاز خواهید داشت. اگر می‌توانید از کابل اترنت استفاده کنید، آن را متصل کرده و به بخش بعدی بروید.

اگر به وای‌فای متصل می‌شوید، دستور `ip link` را اجرا کنید تا نام رابط شبکه بی‌سیم خود را پیدا کنید. به دنبال رابطی بگردید که با `wl` شروع می‌شود (معمولاً `wlan0`).

مقادیر `SSID` و `passphrase` را با اطلاعات احراز هویت وای‌فای خود جایگزین کرده و اجرا کنید:
```shell-session
# wpa_supplicant -B -i wlan0 -c <(wpa_passphrase 'SSID' 'passphrase') &
```

صبر کنید تا `wpa_supplicant` اتصال را برقرار کند. سپس برای فعال‌سازی دسترسی به اینترنت، یک آدرس IP ایستا اختصاص دهید. عبارت `192.168.1.X` را با یک آدرس IP آزاد در شبکه خود و `192.168.1.1` را با آدرس درگاه (gateway) روتر خود جایگزین کنید:
```shell-session
# ip addr add 192.168.1.X/24 dev wlan0
# ip route add default via 192.168.1.1
```

اکنون می‌توانید `dhcpcd` را بارگذاری و اجرا کنید تا یک آدرس آی‌پی (IP) مناسب به دست آورید:
```shell-session
# nix-shell -p dhcpcd
# dhcpcd wlan0
```

پس از چند ثانیه، اتصال را با اجرای دستور زیر بررسی کنید:
```shell-session
# host nixos.org
```

اگر وضوح DNS با موفقیت انجام شود، شما به اینترنت دسترسی دارید و می‌توانید به بخش بعدی بروید.

در صورتی که دچار خطای تایپی شده‌اید، `pkill wpa_supplicant` را اجرا کرده و از سر نو شروع کنید.

## به‌روزرسانی سفت‌افزار

برای بهره‌مندی از به‌روزرسانی‌ها و رفع اشکال‌های ارائه‌شده توسط سازنده، کار را با به‌روزرسانی سفت‌افزار Raspberry Pi آغاز می‌کنیم:

```shell-session
# nix-shell -p raspberrypi-eeprom
# mount /dev/disk/by-label/FIRMWARE /mnt
# BOOTFS=/mnt FIRMWARE_RELEASE_STATUS=stable rpi-eeprom-update -d -a
```

## نصب و پیکربندی NixOS

اکنون NixOS را با پیکربندی خودمان نصب می‌کنیم؛ در اینجا یک کاربر `guest` ایجاد کرده و daemon اس‌اس‌اچ (SSH) را فعال می‌کنیم.

در عبارت `let` زیر، مقدار متغیرهای `SSID` و `SSIDpassword` را به مقادیر `SSID` و `passphrase` که در مراحل قبل استفاده کردید تغییر دهید:

```nix
{ config, pkgs, lib, ... }:

let
  user = "guest";
  password = "guest";
  SSID = "mywifi";
  SSIDpassword = "mypassword";
  interface = "wlan0";
  hostname = "myhostname";
in {

  boot = {
    kernelPackages = pkgs.linuxKernel.packages.linux_rpi4;
    initrd.availableKernelModules = [ "xhci_pci" "usbhid" "usb_storage" ];
    loader = {
      grub.enable = false;
      generic-extlinux-compatible.enable = true;
    };
  };

  fileSystems = {
    "/" = {
      device = "/dev/disk/by-label/NIXOS_SD";
      fsType = "ext4";
      options = [ "noatime" ];
    };
  };

  networking = {
    hostName = hostname;
    wireless = {
      enable = true;
      networks."${SSID}".psk = SSIDpassword;
      interfaces = [ interface ];
    };
  };

  environment.systemPackages = with pkgs; [ vim ];

  services.openssh.enable = true;

  users = {
    mutableUsers = false;
    users."${user}" = {
      isNormalUser = true;
      password = password;
      extraGroups = [ "wheel" ];
    };
  };

  hardware.enableRedistributableFirmware = true;
  system.stateVersion = "23.11";
}
```

برای صرفه‌جویی در وقت جهت تایپ کردن کل پیکربندی، آن را بارگیری کنید:

```shell-session
# curl -L https://tinyurl.com/tutorial-nixos-install-rpi4 > /etc/nixos/configuration.nix
```

:::{note}
اعتبارنامه‌هایی که در یک پیکربندی NixOS می‌نویسید، هنگام ساخته شدن آن پیکربندی، به‌صورت متن ساده در `/nix/store` شما ذخیره خواهند شد.

اگر **نمی‌خواهید** این اتفاق بیفتد، می‌توانید اعتبارنامه‌های خود را در یک کنسول وارد کنید یا از یکی از راهکارهای جامعه‌ی کاربری برای رازهای رمزگذاری‌شده استفاده کنید.
:::

به دلیل نحوه طراحی `nixos-sd-image`، در این مرحله NixOS در واقع *از پیش نصب شده‌است*، بنابراین ما فقط نیاز داریم با پیکربندی جدید خود `nixos-rebuild` را اجرا کنیم:

```shell-session
# nixos-rebuild boot
# reboot
```

اگر سیستم شما بالا نیامد، قدیمی‌ترین پیکربندی را از منوی بوت (boot loader) انتخاب کنید تا به تصویر زنده بازگشته و از نو شروع کنید.

## اعمال تغییرات

سیستم بالا آمد، تبریک می‌گوییم.

برای اعمال تغییرات بیشتر در پیکربندی، [گزینه‌های NixOS را جستجو کنید](https://search.nixos.org/options)، فایل `/etc/nixos/configuration.nix` را ویرایش کرده و سیستم خود را به‌روزرسانی کنید:

```shell-session
$ sudo -i
# nixos-rebuild switch
```

## گام‌های بعدی

- هنگامی که یک سیستم‌عامل کاری در اختیار داشتید، سعی کنید آن را با دستور `nixos-rebuild switch --upgrade` ارتقا دهید تا نسخه‌های بسته‌ی به‌روزتری را نصب کنید، و اگر چیزی دچار خرابی شد، به پیکربندی قدیمی‌تر بازگردانی (rollback) کنید.
- برای فعال‌سازی شتاب‌دهی سخت‌افزاری جهت تجربه‌ی یک میزکار گرافیکی دلپذیر، ماژول [`nixos-hardware`](https://github.com/nixos/nixos-hardware) را به پیکربندی خود اضافه کنید:
```nix
  imports = [
    "${fetchTarball "https://github.com/NixOS/nixos-hardware/tarball/master"}/raspberry-pi/4"
  ];
  ```

توصیه می‌کنیم مرجع را روی `nixos-hardware` سنجاق کردن Nixpkgs کنید: [](ref-pinning-nixpkgs)

- برای تنظیم گزینه‌های راه‌انداز بوت (Boot Loader) که بر سخت‌افزار تأثیر می‌گذارند، [گزینه‌های `config.txt` را ببینید](https://www.raspberrypi.org/documentation/configuration/config-txt/). می‌توانید با اجرای دستور `mount /dev/disk/by-label/FIRMWARE /mnt` و باز کردن مسیر `/mnt/config.txt` این گزینه‌ها را تغییر دهید.

