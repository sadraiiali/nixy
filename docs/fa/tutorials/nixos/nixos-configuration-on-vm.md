# <span id="nixos-vms"></span> ماشین‌های مجازی NixOS

یکی از مهم‌ترین ویژگی‌های NixOS، قابلیت پیکربندی سرتاسر سیستم به شکل اعلانی (declarative)، از جمله بسته‌هایی که باید نصب شوند، سرویس‌هایی که باید اجرا شوند و همچنین سایر تنظیمات و گزینه‌ها است.

پیکربندی‌های NixOS را می‌توان برای تست و استفاده از NixOS با استفاده از یک ماشین مجازی به کار برد که در مقایسه با نصب کامل روی سخت‌افزار واقعی (bare metal)، گزینه‌ای سبک‌تر محسوب می‌شود.

## چه چیزی خواهید آموخت؟

این آموزش به عنوان مقدمه‌ای بر ایجاد ماشین‌های مجازی NixOS عمل می‌کند. ماشین‌های مجازی ابزاری کاربردی برای آزمایش یا دیباگ (اشکال‌زدایی) پیکربندی‌های NixOS هستند.

## به چه چیزی نیاز دارید؟

- یک سیستم لینوکس با پشتیبانی از مجازی‌سازی
- (اختیاری) یک محیط گرافیکی برای اجرای یک ماشین مجازی گرافیکی
- یک [نصب Nix](https://nix.dev/install-nix) فعال
- دانش پایه‌ای از [زبان Nix](/pages/nix-dev/tutorials/nix-language)

> **مهم**
>
> یک پیکربندی NixOS یک تابع در زبان Nix است که از قرارداد [ماژول NixOS](https://nixos.org/manual/nixos/stable/index.html#sec-writing-modules) پیروی می‌کند. برای بررسی جامع سیستم ماژول، آموزش [module-system-deep-dive](/pages/nix-dev/tutorials/module-system/deep-dive) را مطالعه کنید.

## شروع از یک پیکربندی پیش‌فرض NixOS

> **نکته**
>
> این آموزش با ساختن `configuration.nix` شما از اصول اولیه شروع می‌کند و هر مرحله را توضیح می‌دهد. در صورت تمایل، می‌توانید مستقیماً به بخش [پیکربندی نمونه](#sample-nixos-config "بخشی در همین صفحه") بروید.

ما با یک `configuration.nix` حداقلی شروع می‌کنیم:

```nix
{ config, pkgs, ... }:

{
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  system.stateVersion = "24.05";
}
```

برای امکان ورود به سیستم، خطوط زیر را به مجموعه ویژگی بازگردانده‌شده اضافه کنید:

```nix
  users.users.alice = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
  };
```

علاوه بر این، باید یک رمز عبور برای این کاربر مشخص کنید. فقط به منظور نمایش، با افزودن گزینه‌ی `initialPassword` به پیکربندی کاربر، یک رمز عبور ناامن و به صورت متن ساده (Plain text) مشخص می‌کنید:

```nix
   initialPassword = "test";
```

ما دو برنامه سبک‌وزن را به عنوان مثال اضافه می‌کنیم:

```nix
  environment.systemPackages = with pkgs; [
    cowsay
    lolcat
  ];
```

> **هشدار**
>
> از گذرواژه‌های متنی ساده (plain text) در خارج از این مثال استفاده نکنید، مگر اینکه بدانید چه کار می‌کنید. برای جایگزین‌های امن‌تر، [`initialHashedPassword`](https://nixos.org/manual/nixos/stable/options.html#opt-users.extraUsers._name_.initialHashedPassword) یا [`ssh.authorizedKeys`](https://nixos.org/manual/nixos/stable/options.html#opt-users.extraUsers._name_.openssh.authorizedKeys.keys) را ببینید.

### <span id="sample-nixos-config"></span> پیکربندی نمونه

فایل کامل `configuration.nix` به شکل زیر است:

```nix
{ config, pkgs, ... }:
{
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  users.users.alice = {
    isNormalUser = true;
    extraGroups = [ "wheel" ]; # Enable ‘sudo’ for the user.
    initialPassword = "test";
  };

  environment.systemPackages = with pkgs; [
    cowsay
    lolcat
  ];

  system.stateVersion = "24.05";
}
```

## ایجاد یک ماشین مجازی مبتنی بر QEMU از روی یک پیکربندی NixOS

یک ماشین مجازی NixOS با استفاده از دستور `nix-build` ایجاد می‌شود:

```bash
$ nix-build '<nixpkgs/nixos>' -A vm -I nixpkgs=channel:nixos-24.05 -I nixos-config=./configuration.nix
```

این دستور صفت `vm` را از نسخه `nixos-24.05` از NixOS، با استفاده از پیکربندی NixOS مشخص‌شده در مسیر نسبی، می‌سازد.

**توضیح دقیق**

- آرگومان موقعیتی برای [`nix-build`](/pages/nix-manual/command-ref/nix-build) مسیری است به درایویشنی که باید ساخته شود. آن مسیر را می‌توان از [یک عبارت Nix که به یک derivation ارزیابی می‌شود](/pages/nix-dev/tutorials/nix-language) به دست آورد.
    
    کمک‌رسان ساخت ماشین مجازی در NixOS تعریف شده است که بخشی از [مخزن `nixpkgs`](https://github.com/NixOS/nixpkgs) است. بنابراین ما از [مسیر جستجو](/pages/nix-dev/tutorials/nix-language) `<nixpkgs/nixos>` استفاده می‌کنیم.
    
- [گزینه‌ی `-A`](/pages/nix-manual/command-ref/opt-common#opt-attr) صفت مورد نظر را برای انتخاب از عبارت Nix ارائه‌شده یعنی `<nixpkgs/nixos>` مشخص می‌کند.
    
    برای ساخت ماشین مجازی، ما صفت `vm` را همان‌طور که در [`nixos/default.nix`](https://github.com/NixOS/nixpkgs/blob/7c164f4bea71d74d98780ab7be4f9105630a2eba/nixos/default.nix#L19) تعریف شده است، انتخاب می‌کنیم.
    
- [گزینه‌ی `-I`](/pages/nix-manual/command-ref/opt-common#opt-I) ورودی‌ها را به مسیر جستجو اضافه می‌کند.
    
    در اینجا ما `nixpkgs` را طوری تنظیم می‌کنیم که به [نسخه خاصی از Nixpkgs](/pages/nix-dev/reference/pinning-nixpkgs) اشاره کند و `nix-config` را روی فایل `configuration.nix` در پوشه جاری تنظیم می‌کنیم.
    

## اجرای ماشین مجازی

دستور قبلی یک پیوند نمادین با نام `result` در پوشه کاری ایجاد کرد. این پیوند به پوشه‌ای اشاره دارد که حاوی ماشین مجازی است.

```bash
$ ls -R ./result
result:
bin  system

result/bin:
run-nixos-vm
```

ماشین مجازی را اجرا کنید:

```bash
$ QEMU_KERNEL_PARAMS=console=ttyS0 ./result/bin/run-nixos-vm -nographic; reset
```

این دستور به دلیل وجود `-nographic`، QEMU را در همین ترمینال اجرا خواهد کرد. گزینه‌ی `console=ttyS0` همچنین فرآیند راه‌اندازی (بوت) را نمایش می‌دهد که در صفحه‌ی ورود به کنسول به پایان می‌رسد.

با نام کاربری `alice` و رمز عبور `test` وارد شوید. بررسی کنید که برنامه‌ها طبق مشخصات واقعاً در دسترس هستند:

```bash
$ cowsay hello | lolcat
```

با خاموش کردن ماشین مجازی، از آن خارج شوید:

```bash
$ sudo poweroff
```

> **نکته**
>
> اگر فراموش کردید کاربر را به گروه `wheel` اضافه کنید یا پسوردی تعیین نکردید، ماشین مجازی را از یک ترمینال دیگر متوقف کنید:
>
> \`\`\`
>
> > **نکته**
> >
> > ```bash
> > $ sudo pkill qemu
> > ```
> >
> > اجرای ماشین مجازی یک فایل `nixos.qcow2` در پوشه فعلی ایجاد می‌کند. این فایل تصویر دیسک حاوی وضعیت پویای ماشین مجازی است. از آنجا که این فایل وضعیت اجراهای قبلی (مانند رمز عبور کاربر) را حفظ می‌کند، ممکن است در اشکال‌زدایی تداخل ایجاد کند.
> >
> > هرگاه پیکربندی را تغییر دادید، این فایل را حذف کنید:
> >
> > ```bash
> > $ rm nixos.qcow2
> > ```
> >
> > ## اجرای GNOME روی یک ماشین مجازی گرافیکی
> >
> > برای ایجاد یک ماشین مجازی با رابط کاربری گرافیکی، خطوط زیر را به پیکربندی اضافه کنید:
> >
> > ```nix
> > # Enable the X11 windowing system.
> > services.xserver.enable = true;
> >
> > # Enable the GNOME Desktop Environment.
> > services.xserver.displayManager.gdm.enable = true;
> > services.xserver.desktopManager.gnome.enable = true;
> > ```
> >
> > این سه خط، X11، مدیر نمایشگر GDM (برای امکان ورود به سیستم) و GNOME را به عنوان مدیر دسکتاپ فعال می‌کنند.
> >
> > > **راهنمایی**
> > >
> > > همچنین می‌توانید از ماژول `installation-cd-graphical-gnome.nix` برای تولید فایل پیکربندی از صفر استفاده کنید:
> > >
> > > ```bash
> > > nix-shell -I nixpkgs=channel:nixos-24.05 -p "$(cat <<EOF
> > > let
> > > pkgs = import <nixpkgs> { config = {}; overlays = []; };
> > > iso-config = pkgs.path + /nixos/modules/installer/cd-dvd/installation-cd-graphical-gnome.nix;
> > > nixos = pkgs.nixos iso-config;
> > > in nixos.config.system.build.nixos-generate-config
> > > EOF
> > >)"
> > > ```
> > >
> > > ```bash
> > > $ nixos-generate-config --dir ./
> > > ```
> > >
> > > فایل کامل `configuration.nix` به شکل زیر است:
> > >
> > > ```nix
> > > { config, pkgs, ... }:
> > > {
> > > boot.loader.systemd-boot.enable = true;
> > > boot.loader.efi.canTouchEfiVariables = true;
> > >
> > > services.xserver.enable = true;
> > >
> > > services.xserver.displayManager.gdm.enable = true;
> > > services.xserver.desktopManager.gnome.enable = true;
> > >
> > > users.users.alice = {
> > > isNormalUser = true;
> > > extraGroups = [ "wheel" ];
> > > initialPassword = "test";
> > > };
> > >
> > > system.stateVersion = "24.05";
> > > }
> > > ```
> > >
> > > برای دریافت خروجی گرافیکی، ماشین مجازی را بدون گزینه‌های خاص اجرا کنید:
> > >
> > > ```bash
> > > $ nix-build '<nixpkgs/nixos>' -A vm -I nixpkgs=channel:nixos-24.05 -I nixos-config=./configuration.nix
> > > $ ./result/bin/run-nixos-vm
> > > ```
> > >
> > > ## اجرای Sway به عنوان کامپوزیتور Wayland روی یک ماشین مجازی
> > >
> > > برای تغییر به یک کامپوزیتور Wayland، گزینه `services.xserver.desktopManager.gnome` را غیرفعال کرده و `programs.sway` را فعال کنید:
> > >
> > > **`configuration.nix`**
> > >
> > > ```diff
> > > - services.xserver.desktopManager.gnome.enable = true;
> > > + programs.sway.enable = true;
> > > ```
> > >
> > > > **نکته**
> > > >
> > > > اجرای ترکیب‌کننده‌های Wayland در یک ماشین مجازی ممکن است منجر به مشکلاتی با درایورهای نمایشگر مورد استفاده توسط QEMU شود. شما باید از میان درایورهای موجود، یکی را که با Sway سازگار است انتخاب کنید. برای مشاهده گزینه‌ها به [مستندات کاربر QEMU](https://www.qemu.org/docs/master/system/qemu-manpage.html) مراجعه کنید. یکی از گزینه‌ها درایور `virtio-vga` است: :::{'{'}'{'{'}'{'}'}'{'{'}'{'{'}'{'}'}'{'{'}'{'}'}'{'}'}
> > > >
> > > > ```bash
> > > > $ ./result/bin/run-nixos-vm -device virtio-vga
> > > > ```
> > > >
> > > > همچنین می‌توان آرگومان‌ها را به QEMU در فایل پیکربندی اضافه کرد:
> > > >
> > > > ```nix
> > > > { config, pkgs, ... }:
> > > > {
> > > > boot.loader.systemd-boot.enable = true;
> > > > boot.loader.efi.canTouchEfiVariables = true;
> > > >
> > > > services.xserver.enable = true;
> > > >
> > > > services.xserver.displayManager.gdm.enable = true;
> > > > programs.sway.enable = true;
> > > >
> > > > imports = [ <nixpkgs/nixos/modules/virtualisation/qemu-vm.nix> ];
> > > > virtualisation.qemu.options = [
> > > > "-device virtio-vga"
> > > > ];
> > > >
> > > > users.users.alice = {
> > > > isNormalUser = true;
> > > > extraGroups = [ "wheel" ];
> > > > initialPassword = "test";
> > > > };
> > > >
> > > > system.stateVersion = "24.05";
> > > > }
> > > > ```
> > >
> > > راهنمای NixOS دارای فصل‌هایی درباره‌ی [X11](https://nixos.org/manual/nixos/stable/#sec-x11) و [Wayland](https://nixos.org/manual/nixos/stable/#sec-wayland) است که مدیران پنجره جایگزین را فهرست می‌کنند.
> > >
> > > ## مراجع
> > >
> > > - [راهنمای NixOS: پیکربندی NixOS](https://nixos.org/manual/nixos/stable/index.html#ch-configuration).
> > > - [راهنمای NixOS: ماژول‌ها](https://nixos.org/manual/nixos/stable/index.html#sec-writing-modules).
> > > - [مرجع گزینه‌های راهنمای NixOS](https://nixos.org/manual/nixos/stable/options.html).
> > > - [راهنمای NixOS: تغییر پیکربندی](https://nixos.org/manual/nixos/stable/#sec-changing-config).
> > > - [کد منبع NixOS: قالب پیکربندی (`configuration template`) در `tools.nix`](https://github.com/NixOS/nixpkgs/blob/4e0525a8cdb370d31c1e1ba2641ad2a91fded57d/nixos/modules/installer/tools/tools.nix#L122-L226).
> > > - [کد منبع NixOS: صفت `vm` در `default.nix`](https://github.com/NixOS/nixpkgs/blob/master/nixos/default.nix).
> > > - [راهنمای Nix: `nix-build`](/pages/nix-manual/command-ref/nix-build).
> > > - [راهنمای Nix: گزینه‌های رایج خط فرمان](/pages/nix-manual/command-ref/opt-common).
> > > - [مستندات کاربری QEMU](https://www.qemu.org/docs/master/system/qemu-manpage.html) برای گزینه‌های زمان اجرای بیشتر
> > > - [جستجوی گزینه‌های NixOS: `virtualisation.qemu`](https://search.nixos.org/options?query=virtualisation.qemu) برای پیکربندی اعلانی ماشین مجازی
> > >
> > > ## گام‌های بعدی
> > >
> > > - [module-system-deep-dive](/pages/nix-dev/tutorials/module-system/deep-dive)
> > > - [integration-testing-vms](/pages/nix-dev/tutorials/nixos/integration-testing-using-virtual-machines)
> > > - [bootable-iso-image](/pages/nix-dev/tutorials/nixos/building-bootable-iso-image)
