---
myst:
 html_meta:
 "description lang=en": "Cross compilation tutorial using Nix"
 "keywords": "Nix, cross compilation, cross-compile, Nix"
---

(cross-compilation)=

# کامپایل متقاطع

مجموعه‌ی بسته‌های نیکس (Nixpkgs) ابزارهایی را برای کامپایل متقاطع نرم‌افزار برای انواع سیستم‌های مختلف فراهم می‌کند.

## چه چیزهایی نیاز دارید؟

- تجربه استفاده از کامپایلرهای C
- دانش پایه از [زبان Nix](<reading-nix-language>)

## پلتفرم‌ها

هنگام کامپایل کردن کد، بین **پلتفرم ساخت (build platform)** که در آن فایل اجرایی *ساخته* می‌شود، و **پلتفرم میزبان (host platform)** که فایل اجرایی کامپایل‌شده روی آن *اجرا* می‌شود، تمایز وجود دارد [^id3].

**کامپایل بومی (Native compilation)** حالت خاصی است که در آن این دو پلتفرم یکسان هستند.
**کامپایل متقاطع** حالت عمومی است که در آن این دو پلتفرم یکسان نیستند.

کامپایل متقاطع زمانی مورد نیاز است که پلتفرم میزبان منابع محدودی (مانند پردازنده) داشته باشد یا دسترسی به آن برای توسعه آسان نباشد.

مجموعه‌ی بسته‌های نیکس (Nixpkgs) از پشتیبانی بسیار آزمایش‌شده‌ای برای کامپایل متقاطع برخوردار است.

[^id3]: اصطلاحات مربوط به پلتفرم‌های کامپایل متقاطع در میان سیستم‌های ساخت مختلف متفاوت است.
 ما تصمیم گرفته‌ایم از
 [اصطلاحات autoconf](https://www.gnu.org/software/autoconf/manual/autoconf-2.69/html_node/Hosts-and-Cross_002dCompilation.html) پیروی کنیم.

## پلتفرم هدف (target platform) چیست؟

مفهوم سومی برای پلتفرم وجود دارد که به آن **پلتفرم هدف** گفته می‌شود.

پلتفرم هدف مربوط به مواردی است که می‌خواهید یک باینری کامپایلر بسازید.
در چنین مواردی، شما کامپایلر را روی *پلتفرم ساخت* می‌سازید، آن را برای کامپایل کد روی *پلتفرم میزبان* اجرا می‌کنید، و فایل اجرایی نهایی را روی *پلتفرم هدف* اجرا می‌کنید.

از آنجا که این مورد به ندرت نیاز است، این آموزش فرض می‌کند که هدف با میزبان یکسان است.

## تعیین پیکربندی پلتفرم میزبان

پلتفرم ساخت به‌طور خودکار توسط Nix در طول فاز پیکربندی تعیین می‌شود.

بهترین راه برای تعیین پلتفرم میزبان، اجرای این دستور روی پلتفرم میزبان است:

```shell-session
$ $(nix-build '<nixpkgs>' -I nixpkgs=channel:nixos-23.11 -A gnu-config)/config.guess
aarch64-unknown-linux-gnu
```

در صورتی که این کار امکان‌پذیر نباشد (برای مثال، هنگامی که پلتفرم میزبان برای توسعه به راحتی در دسترس نیست)، پیکربندی پلتفرم باید به صورت دستی و از طریق الگوی زیر ساخته شود:

```
<cpu>-<vendor>-<os>-<abi>
```

این نمایش رشته‌ای به دلایل تاریخی در `nixpkgs` استفاده می‌شود.

توجه داشته باشید که `<vendor>` اغلب `unknown` است و `<abi>` اختیاری است.
همچنین هیچ شناسه منحصربه‌فردی برای یک پلتفرم وجود ندارد، برای مثال `unknown` و `pc` به جای یکدیگر قابل استفاده هستند (به همین دلیل است که اسکریپت `config.guess` نامیده می‌شود).

اگر نمی‌توانید Nix را نصب کنید، راهی برای اجرای `config.guess` (که معمولاً همراه با بسته autoconf ارائه می‌شود) از روی سیستم‌عاملی که قادر به اجرای آن روی هاست پلتفرم هستید، پیدا کنید.

برخی مثال‌های رایج دیگر از پیکربندی‌های پلتفرم:

- aarch64-apple-darwin14
- aarch64-pc-linux-gnu
- x86_64-w64-mingw32
- aarch64-apple-ios

:::{note}
سیستم‌عامل macOS/Darwin یک مورد خاص است، زیرا تمام بخش‌های سیستم‌عامل متن‌باز نیست.
کامپایل متقاطع تنها بین `aarch64-darwin` و `x86_64-darwin` امکان‌پذیر است.
پشتیبانی از `aarch64-darwin` اخیراً اضافه شده‌است، بنابراین کامپایل متقاطع به سختی آزمایش شده‌است.
:::

## انتخاب هاست پلتفرم با Nix

مجموعه‌ی بسته‌های نیکس (Nixpkgs) دارای مجموعه‌ای از هاست پلتفرم‌های ازپیش‌تعریف‌شده برای کامپایل متقاطع به نام `pkgsCross` است.

بررسی آن‌ها در `nix repl` امکان‌پذیر است:

:::{note}
[از نسخه 2.19 به بعد Nix](https://nix.dev/manual/nix/latest/release-notes/rl-2.19)، دستور `nix repl` به پرچم `-f` / `--file` نیاز دارد:
```shell-session
$ nix repl -f '<nixpkgs>' -I nixpkgs=channel:nixos-23.11
```
:::

```shell-session
$ nix repl '<nixpkgs>' -I nixpkgs=channel:nixos-23.11
Welcome to Nix 2.18.1. Type :? for help.

Loading '<nixpkgs>'...
Added 14200 variables.

nix-repl> pkgsCross.<TAB>
pkgsCross.aarch64-android pkgsCross.musl-power
pkgsCross.aarch64-android-prebuilt pkgsCross.musl32
pkgsCross.aarch64-darwin pkgsCross.musl64
pkgsCross.aarch64-embedded pkgsCross.muslpi
pkgsCross.aarch64-multiplatform pkgsCross.or1k
pkgsCross.aarch64-multiplatform-musl pkgsCross.pogoplug4
pkgsCross.aarch64be-embedded pkgsCross.powernv
pkgsCross.amd64-netbsd pkgsCross.ppc-embedded
pkgsCross.arm-embedded pkgsCross.ppc64
pkgsCross.armhf-embedded pkgsCross.ppc64-musl
pkgsCross.armv7a-android-prebuilt pkgsCross.ppcle-embedded
pkgsCross.armv7l-hf-multiplatform pkgsCross.raspberryPi
pkgsCross.avr pkgsCross.remarkable1
pkgsCross.ben-nanonote pkgsCross.remarkable2
pkgsCross.fuloongminipc pkgsCross.riscv32
pkgsCross.ghcjs pkgsCross.riscv32-embedded
pkgsCross.gnu32 pkgsCross.riscv64
pkgsCross.gnu64 pkgsCross.riscv64-embedded
pkgsCross.i686-embedded pkgsCross.scaleway-c1
pkgsCross.iphone32 pkgsCross.sheevaplug
pkgsCross.iphone32-simulator pkgsCross.vc4
pkgsCross.iphone64 pkgsCross.wasi32
pkgsCross.iphone64-simulator pkgsCross.x86_64-embedded
pkgsCross.mingw32 pkgsCross.x86_64-netbsd
pkgsCross.mingwW64 pkgsCross.x86_64-netbsd-llvm
pkgsCross.mmix pkgsCross.x86_64-unknown-redox
pkgsCross.msp430
```

این نام‌های صفت (attribute) برای بسته‌های کامپایل متقاطع طی زمان به‌نسبت آزادانه انتخاب شده‌اند.
آن‌ها معمولاً با رشته‌ی پیکربندی پلتفرم متناظر مطابقت ندارند.

می‌توانید رشته‌ی پلتفرم را از `pkgsCross.<platform>.stdenv.hostPlatform.config` بازیابی کنید:

```shell-session
nix-repl> pkgsCross.aarch64-multiplatform.stdenv.hostPlatform.config
"aarch64-unknown-linux-gnu"
```

اگر پلتفرم میزبان مورد نظر شما هنوز تعریف نشده‌است، لطفاً آن را به [پروژه اصلی مشارکت دهید](https://github.com/NixOS/nixpkgs/blob/master/lib/systems/examples.nix).

## مشخص کردن پلتفرم میزبان

مکانیزم راه‌اندازی کامپایل متقاطع به شکل زیر عمل می‌کند:

1. پیکربندی پلتفرم ساخت را بگیرید و آن را روی مجموعه بسته فعلی، که به طور قراردادی `pkgs` نامیده می‌شود، اعمال کنید.

 پلتفرم ساخت ضمنی در `pkgs = import <nixpkgs> {}` به عنوان سیستم فعلی در نظر گرفته می‌شود.
 این کار یک محیط ساخت `pkgs.stdenv` با تمام وابستگی‌های موجود برای کامپایل روی پلتفرم ساخت ایجاد می‌کند.

2. پیکربندی مناسب پلتفرم میزبان را روی تمام بسته‌های موجود در `pkgsCross` اعمال کنید.

 استفاده از `pkgs.pkgsCross.<host>.hello` بسته `hello` را تولید می‌کند که روی پلتفرم ساخت کامپایل شده‌است تا روی پلتفرم `<host>` اجرا شود.

چندین روش معادل برای دسترسی به بسته‌های هدف‌گذاری‌شده برای پلتفرم میزبان وجود دارد.

1. بسته پلتفرم میزبان را به صراحت از داخل محیط پلتفرم ساخت انتخاب کنید:
```nix
 let
 nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/release-23.11";
 pkgs = import nixpkgs {};
 in
 pkgs.pkgsCross.aarch64-multiplatform.hello
 ```

۲. هنگام درون‌ریزی `nixpkgs`، پلتفرم میزبان را به `crossSystem` ارسال کنید.
 این کار `nixpkgs` را به گونه‌ای پیکربندی می‌کند که تمام بسته‌های آن برای پلتفرم میزبان ساخته شوند:
```nix
 let
 nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/release-23.11";
 pkgs = import nixpkgs { crossSystem = { config = "aarch64-unknown-linux-gnu"; }; };
 in
 pkgs.hello
 ```

به‌طور معادل، می‌توانید پلتفرم هاست را به عنوان یک آرگومان به `nix-build` ارسال کنید:
```sh
 $ nix-build '<nixpkgs>' -I nixpkgs=channel:nixos-23.11 \
 --arg crossSystem '{ config = "aarch64-unknown-linux-gnu"; }' \
 -A hello
 ```

## کامپایل متقاطع برای نخستین بار

برای کامپایل متقاطع بسته‌ای مانند [hello](https://www.gnu.org/software/hello/)، صفت پلتفرم، در مورد ما `aarch64-multiplatform` را انتخاب کرده و دستور زیر را اجرا کنید:

```shell-session
$ nix-build '<nixpkgs>' -I nixpkgs=channel:nixos-23.11 \
 -A pkgsCross.aarch64-multiplatform.hello
...
/nix/store/1dx87l5rav8679lqigf9xxkb7wvh2m4k-hello-aarch64-unknown-linux-gnu-2.12.1
```

:::{note}
هش بسته در مسیر انبار با به‌روزرسانی‌های کانال تغییر می‌کند.
:::

برای یافتن نام صفت بسته‌ای که مایل به ساخت آن هستید، [بسته‌ها را جستجو کنید](https://search.nixos.org/packages).

## کامپایل متقاطع در دنیای واقعی برای یک مثال Hello World

مثال زیر یک برنامه Hello World را به عنوان فایل‌های اجرایی استاتیک برای پلتفرم‌های `armv6l-unknown-linux-gnueabihf` و `x86_64-w64-mingw32` (ویندوز) کامپایل متقاطع می‌کند و فایل اجرایی حاصل را با استفاده از [یک شبیه‌ساز](https://en.wikipedia.org/wiki/Emulator) اجرا می‌کند.

با فرض اینکه یک فایل `cross-compile.nix` داریم:

```nix
let
 nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/release-23.11";
 pkgs = import nixpkgs {};

 # Create a C program that prints Hello World
 helloWorld = pkgs.writeText "hello.c" ''
 #include <stdio.h>

 int main (void)
 {
 printf ("Hello, world!\n");
 return 0;
 }
 '';

 # A function that takes host platform packages
 crossCompileFor = hostPkgs:
 # Run a simple command with the compiler available
 hostPkgs.runCommandCC "hello-world-cross-test" {} ''
 # Wine requires home directory
 HOME=$PWD

 # Compile our example using the compiler specific to our host platform
 $CC ${helloWorld} -o hello

 # Run the compiled program using user mode emulation (Qemu/Wine)
 # buildPackages is passed so that emulation is built for the build platform
 ${hostPkgs.stdenv.hostPlatform.emulator hostPkgs.buildPackages} hello > $out

 # print to stdout
 cat $out
 '';
in {
 # Statically compile our example using the two platform hosts
 rpi = crossCompileFor pkgs.pkgsCross.raspberryPi;
 windows = crossCompileFor pkgs.pkgsCross.mingwW64;
}
```

اگر این مثال را بسازیم و هر دو derivation حاصل را چاپ کنیم، باید برای هر کدام عبارت "Hello, world!" را ببینیم:

```shell-session
$ cat $(nix-build cross-compile.nix)
Hello, world!
Hello, world!
```

## محیط توسعه با یک کامپایلر متقاطع

در {ref}`آموزش محیط‌های اعلامی و قابل بازتولید <declarative-reproducible-envs>`، بررسی کردیم که چگونه Nix به ما کمک می‌کند تا ابزارها و کتابخانه‌های سیستم را برای پروژه‌مان فراهم کنیم.

همچنین امکان فراهم کردن محیطی با یک کامپایلر پیکربندی‌شده برای **کامپایل متقاطع به باینری‌های استاتیک با استفاده از musl** نیز وجود دارد.

با فرض اینکه یک `shell.nix` داریم:

```nix
let
 nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/release-23.11";
 pkgs = (import nixpkgs {}).pkgsCross.aarch64-multiplatform;
in

# callPackage is needed due to https://github.com/NixOS/nixpkgs/pull/126844
pkgs.pkgsStatic.callPackage ({ mkShell, zlib, pkg-config, file }: mkShell {
 # these tools run on the build platform, but are configured to target the host platform
 nativeBuildInputs = [ pkg-config file ];
 # libraries needed for the host platform
 buildInputs = [ zlib ];
}) {}
```

و فایل `hello.c`:

```{code-block} c hello.c
#include <stdio.h>

int main (void)
{
 printf ("Hello, world!\n");
 return 0;
}
```

ما می‌توانیم آن را کامپایل متقاطع کنیم:

```shell-session
$ nix-shell --run '$CC hello.c -o hello' shell.nix
```

و تأیید کنید که aarch64 است:

```shell-session
$ nix-shell --run 'file hello' shell.nix
hello: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), statically linked, with debug_info, not stripped
```

## گام‌های بعدی

- [کش باینری رسمی](https://cache.nixos.org) تعداد محدودی از باینری‌ها را برای بسته‌هایی که کامپایل متقاطع شده‌اند دارد، بنابراین برای صرفه‌جویی در زمان کامپایل مجدد، {ref}`کش باینری و CI خود را با GitHub Actions پیکربندی کنید <github-actions>`.

- در حالی که بسیاری از کامپایلرها در Nixpkgs از کامپایل متقاطع پشتیبانی می‌کنند، همه آن‌ها چنین قابلیتی ندارند.

 علاوه بر این، پشتیبانی از کامپایل متقاطع کار ساده‌ای نیست و به دلیل ترکیبات مختلف احتمالی مواردی که باید تست شوند، ممکن است برخی از بسته‌ها ساخته نشوند.

 [توضیحات تفصیلی درباره‌ی نحوه پیاده‌سازی کامپایل متقاطع در Nix](https://nixos.org/manual/nixpkgs/stable/#chap-cross) می‌تواند در رفع آن مسائل کمک کند.

- جامعه‌ی کاربری Nix یک [اتاق اختصاصی در Matrix](https://matrix.to/#/#cross-compiling:nixos.org) برای دریافت کمک در زمینه کامپایل متقاطع دارد.
