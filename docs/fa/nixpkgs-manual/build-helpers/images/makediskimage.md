# `<nixpkgs/nixos/lib/make-disk-image.nix>` {#sec-make-disk-image}

`<nixpkgs/nixos/lib/make-disk-image.nix>` تابعی برای ایجاد _تصویر دیسک_ در فرمت‌های متعدد است: raw، QCOW2 (QEMU)، QCOW2-Compressed (نسخه فشرده‌شده)، VDI (VirtualBox)، VPC (VirtualPC).

این تابع می‌تواند تصاویر را به دو روش ایجاد کند:

- با استفاده از `cptofs` بدون هیچ ماشین مجازی برای ایجاد یک تصویر دیسک انبار Nix،
- با استفاده از یک ماشین مجازی برای ایجاد یک نصب کامل NixOS.

هنگام آزمایش بخش‌های راه‌اندازی اولیه (بوت) یا چرخه حیات NixOS مانند یک راه‌انداز بوت (Boot Loader) یا چند نسل مختلف، استفاده از نصب کامل سیستم NixOS ضروری است.
در حالی که برای بسیاری از سرورهای وب و برنامه‌ها، کار با یک تصویر دیسک که فقط شامل انبار Nix است امکان‌پذیر می‌باشد که ساخت آن سریع‌تر است.

تست‌های NixOS نیز هنگام آماده‌سازی ماشین مجازی (VM) از این تابع استفاده می‌کنند. روش `cptofs` زمانی استفاده می‌شود که `virtualisation.useBootLoader` برابر با false (مقدار پیش‌فرض) باشد. در غیر این صورت از روش دوم استفاده می‌شود.

## ویژگی‌ها {#sec-make-disk-image-features}

برای مرجع، کد منبع امضای تابع را جهت مستندات مربوط به آرگومان‌ها مطالعه کنید: <https://github.com/NixOS/nixpkgs/blob/master/nixos/lib/make-disk-image.nix>.
ویژگی‌ها بسته به اینکه یک تصویر فقط-انبار-Nix یا یک تصویر کامل NixOS را انتخاب کنید، در بخش‌های مختلفی تقسیم‌بندی شده‌اند.

### عمومی {#sec-make-disk-image-features-common}

- پیکربندی دلخواه NixOS
- اندازه دیسک خودکار یا محدودشده: پارامتر `diskSize`؛ هنگام قرار داشتن `diskSize` روی حالت `auto` می‌توان `additionalSpace` را برای افزودن مقدار ثابتی از فضای دیسک تنظیم کرد
- چیدمان‌های متعدد جدول پارتیشن: EFI، legacy، legacy + GPT، hybrid، none از طریق پارامتر `partitionTableType`
- الگوهای متغیرها و سفت‌افزارهای OVMF یا EFI قابل سفارشی‌سازی هستند
- نوع سیستم‌فایل ریشه (`fsType`) به هر آنچه که `mkfs.${fsType}` در طول عملیات موجود باشد قابل سفارشی‌سازی است
- برچسب سیستم‌فایل ریشه قابل سفارشی‌سازی است؛ اگر یک تصویر انبار Nix باشد پیش‌فرض `nix-store` و در غیر این صورت `nixpkgs/nixos` است
- کد دلخواه پس از تولید تصویر دیسک با `postVM` قابل اجراست
- نسخه جاری Nixpkgs می‌تواند به عنوان یک کانال در تصویر دیسک تحقق یابد، که با به‌روزرسانی کدهای منبع، هش تصویر تغییر خواهد کرد
- مسیرهای انبار اضافی را می‌توان از طریق `additionalPaths` ارائه داد

### تصویر کامل NixOS {#sec-make-disk-image-features-full-image}

- محتوای دلخواه همراه با مجوزها را می‌توان با استفاده از `contents` در سیستم‌فایل مقصد قرار داد
- یک فایل `/etc/nixpkgs/nixos/configuration.nix` را می‌توان از طریق `configFile` ارائه داد
- راه‌اندازهای بوت پشتیبانی می‌شوند
- متغیرهای EFI را می‌توان در طول تولید تصویر تغییر داد و نتیجه در `$out` ارائه می‌شود
- اندازه پارتیشن بوت زمانی که جدول پارتیشن `efi` یا `hybrid` باشد

### درباره بازتولیدپذیری بیت‌به‌بیت {#sec-make-disk-image-features-reproducibility}

تصاویر **قطعی نیستند**. در صورت امکان لطفا برای رفع این مسئله تلاش کنید. منابع غیرقطعی بودن عبارتند از (فهرست کامل نیست):

- نصب راه‌انداز بوت (Boot Loader) دارای برچسب‌های زمانی است
- پایگاه‌داده انبار Nix در SQLite شامل زمان‌های ثبت است
- فایل `/etc/shadow` دارای ترتیبی غیرقطعی است

پرچم `deterministic` برای تلاش در جهت دست‌یابی به بیشترین میزان قطعی بودن در دسترس است.

## استفاده {#sec-make-disk-image-usage}

برای تولید تصویری که فقط شامل انبار Nix است:
```nix
let
  pkgs = import <nixpkgs> { };
  lib = pkgs.lib;
  make-disk-image = import <nixpkgs/nixos/lib/make-disk-image.nix>;
in
make-disk-image {
  inherit pkgs lib;
  config = { };
  additionalPaths = [ ];
  format = "qcow2";
  onlyNixStore = true;
  partitionTableType = "none";
  installBootLoader = false;
  touchEFIVars = false;
  diskSize = "auto";
  additionalSpace = "0M"; # Defaults to 512M.
  copyChannel = false;
}
```

برخی از آرگومان‌ها را می‌توان نادیده گرفت؛ آن‌ها صرفاً برای روشن شدن مثال به صورت صریح آورده شده‌اند.

ساخت این derivation یک تصویر دیسک QCOW2 ارائه می‌دهد که تنها شامل انبار نیکس (Nix store) و اطلاعات ثبت آن است.

برای تولید یک تصویر دیسک نصب NixOS همراه با UEFI و راه‌انداز بوت (Boot Loader) نصب‌شده:
```nix
let
  pkgs = import <nixpkgs> { };
  lib = pkgs.lib;
  make-disk-image = import <nixpkgs/nixos/lib/make-disk-image.nix>;
  evalConfig = import <nixpkgs/nixos/lib/eval-config.nix>;
in
make-disk-image {
  inherit pkgs lib;
  inherit
    (evalConfig {
      modules = [
        {
          fileSystems."/" = {
            device = "/dev/vda";
            fsType = "ext4";
            autoFormat = true;
          };
          boot.grub.device = "/dev/vda";
        }
      ];
    })
    config
    ;
  format = "qcow2";
  onlyNixStore = false;
  partitionTableType = "legacy+gpt";
  installBootLoader = true;
  touchEFIVars = true;
  diskSize = "auto";
  additionalSpace = "0M"; # Defaults to 512M.
  copyChannel = false;
  memSize = 2048; # Qemu VM memory size in MiB (1024*1024 bytes). Defaults to 1024M.
}
```
