# vmTools {#sec-vm-tools}

مجموعه‌ای از ابزارهای مرتبط با ماشین مجازی (VM) که به ساخت برخی بسته‌ها در سناریوهای پیشرفته‌تر کمک می‌کنند.

## `vmTools.createEmptyImage` {#vm-tools-createEmptyImage}

قطعه‌اسکریپتی به زبان Bash که یک تصویر دیسک در `destination` ایجاد می‌کند.

### صفات {#vm-tools-createEmptyImage-attributes}

* `size`. اندازه دیسک به مگابایت (MiB).
* `fullName`. نامی که در `${destination}/nix-support/full-name` نوشته خواهد شد.
* `destination` (اختیاری، پیش‌فرض `$out`). محل نوشتن فایل‌های تصویر.

## `vmTools.runInLinuxVM` {#vm-tools-runInLinuxVM}

اجرای یک derivation در یک ماشین مجازی Linux (با استفاده از Qemu/KVM).
به‌طور پیش‌فرض، هیچ تصویر دیسکی وجود ندارد؛ سیستم‌فایل ریشه یک `tmpfs` است و انبار نیکس (Nix store) با هاست به اشتراک گذاشته می‌شود (از طریق [پروتکل 9P](https://wiki.qemu.org/Documentation/9p#9p_Protocol)).
بنابراین، هر derivation خالص (pure) در Nix باید بدون تغییر اجرا شود.

اگر ساخت با شکست مواجه شود و Nix با گزینه `-K/--keep-failed` اجرا شده باشد، اسکریپت `run-vm` در پوشه موقت ساخت باقی می‌ماند که به شما اجازه می‌دهد ماشین مجازی را بوت کرده و آن را به صورت تعاملی دیباگ (اشکال‌زدایی) کنید.

### صفات {#vm-tools-runInLinuxVM-attributes}

* `preVM` (اختیاری). دستور شل (Shell) که *پیش از* راه‌اندازی ماشین مجازی (یعنی روی هاست) ارزیابی می‌شود.
* `memSize` (اختیاری، پیش‌فرض `512`). میزان حافظه رم ماشین مجازی به مگابایت (MiB، یعنی ۱۰۲۴×۱۰۲۴ بایت).
* `diskImage` (اختیاری). یک تصویر سیستم‌فایل که به `/dev/sda` متصل می‌شود.
  توجه داشته باشید که در حال حاضر انتظار می‌رود این تصویر شامل یک سیستم‌فایل باشد، نه یک تصویر کامل دیسک دارای جدول پارتیشن و غیره.

### نمونه‌ها {#vm-tools-runInLinuxVM-examples}

ساخت derivation مربوط به hello در داخل یک ماشین مجازی:
```nix
{ pkgs }: with pkgs; with vmTools; runInLinuxVM hello
```

ساخت درون یک ماشین مجازی (VM) با حافظهٔ اضافی:
```nix
{ pkgs }:
with pkgs;
with vmTools;
runInLinuxVM (
  hello.overrideAttrs (_: {
    memSize = 1024;
  })
)
```

استفاده از ماشین مجازی (VM) با یک تصویر دیسک (به‌طور ضمنی `diskImage` را تنظیم می‌کند، [`vmTools.createEmptyImage`](#vm-tools-createEmptyImage) را ببینید):
```nix
{ pkgs }:
with pkgs;
with vmTools;
runInLinuxVM (
  hello.overrideAttrs (_: {
    preVM = createEmptyImage {
      size = 1024;
      fullName = "vm-image";
    };
  })
)
```

## `vmTools.extractFs` {#vm-tools-extractFs}

یک فایل را دریافت می‌کند، مانند یک ایزو (ISO)، و محتویات آن را در انبار (Store) استخراج می‌کند.

### صفات {#vm-tools-extractFs-attributes}

* `file`. مسیر فایلی که باید استخراج شود.
  توجه داشته باشید که در حال حاضر انتظار داریم تصویر شامل یک سیستم‌فایل باشد، نه یک تصویر دیسک کامل همراه با جدول پارتیشن و غیره.
* `fs` (اختیاری). سیستم‌فایل محتویات فایل.

### نمونه‌ها {#vm-tools-extractFs-examples}

محتویات یک فایل ایزو (ISO) را استخراج کنید:
```nix
{ pkgs }: with pkgs; with vmTools; extractFs { file = ./image.iso; }
```

## `vmTools.extractMTDfs` {#vm-tools-extractMTDfs}

مانند [](#vm-tools-extractFs)، اما از یک [Memory Technology Device (MTD)](https://en.wikipedia.org/wiki/Memory_Technology_Device) استفاده می‌کند.

## `vmTools.runInLinuxImage` {#vm-tools-runInLinuxImage}

مانند [](#vm-tools-runInLinuxVM)، اما به جای استفاده از `stdenv` از انبار نیکس (Nix store)، فرآیند ساخت را با استفاده از ابزارهای ارائه‌شده در `/bin`، `/usr/bin` و غیره از تصویر سیستم‌فایل مشخص‌شده اجرا می‌کند؛ که معمولاً سیستم‌فایلی شامل یک توزیع لینوکس مبتنی بر [FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) است.

## `vmTools.makeImageTestScript` {#vm-tools-makeImageTestScript}

تولید یک اسکریپت که می‌تواند برای اجرای یک نشست تعاملی در تصویر داده‌شده استفاده شود.

### Examples {#vm-tools-makeImageTestScript-examples}

ایجاد اسکریپتی برای اجرای یک ماشین مجازی (VM) Fedora 43:
```nix
{ pkgs }: pkgs.vmTools.makeImageTestScript pkgs.vmTools.diskImages.fedora43x86_64
```

یک اسکریپت برای اجرای یک ماشین مجازی (VM) اوبونتو 24.04 ایجاد کنید:
```nix
{ pkgs }: pkgs.vmTools.makeImageTestScript pkgs.vmTools.diskImages.ubuntu2404x86_64
```

## `vmTools.diskImageFuns` {#vm-tools-diskImageFuns}

مجموعه‌ای از توابع که مجموعه‌ای از‌پیش‌تعریف‌شده از تصاویر مینیمال توزیع‌های Linux را می‌سازند.

### تصاویر {#vm-tools-diskImageFuns-images}

* Fedora
  * `fedora42x86_64`
  * `fedora43x86_64`
* Rocky Linux
  * `rocky9x86_64`
  * `rocky10x86_64`
* AlmaLinux
  * `alma9x86_64`
  * `alma10x86_64`
* Oracle Linux
  * `oracle9x86_64`
* Amazon Linux
  * `amazon2023x86_64`
* Ubuntu
  * `ubuntu2204i386`
  * `ubuntu2204x86_64`
  * `ubuntu2404x86_64`
* Debian
  * `debian11i386`
  * `debian11x86_64`
  * `debian12i386`
  * `debian12x86_64`
  * `debian13i386`
  * `debian13x86_64`

### صفات {#vm-tools-diskImageFuns-attributes}

* `size` (اختیاری، مقدار پیش‌فرض `4096`). اندازه‌ی تصویر بر حسب MiB.
* `extraPackages` (اختیاری). فهرستی از نام بسته‌های اضافی از توزیع که باید در تصویر گنجانده شوند.

### مثال‌ها {#vm-tools-diskImageFuns-examples}

تصویر 8GiB شامل Firefox علاوه بر بسته‌های پیش‌فرض:
```nix
{ pkgs }:
pkgs.vmTools.diskImageFuns.ubuntu2404x86_64 {
  extraPackages = [ "firefox" ];
  size = 8192;
}
```

## `vmTools.diskImageExtraFuns` {#vm-tools-diskImageExtraFuns}

میانبری برای `vmTools.diskImageFuns.<attr> { extraPackages = ... }`.

## `vmTools.diskImages` {#vm-tools-diskImages}

میانبری برای `vmTools.diskImageFuns.<attr> { }`.
