---
myst:
  html_meta:
    "description lang=en": "Packaging Existing Software With Nix"
    "keywords": "Nix, packaging"
---

(packaging-tutorial)=
# بسته‌بندی نرم‌افزارهای موجود با Nix

یکی از موارد استفاده اصلی Nix، حل مشکلات رایجی است که در بسته‌بندی نرم‌افزار با آن‌ها مواجه می‌شویم؛ مشکلاتی نظیر مشخص کردن و تهیه وابستگی‌ها.

در بلندمدت، Nix چنین مشکلاتی را کاهش می‌دهد.
اما هنگامی که *برای نخستین بار* یک نرم‌افزار موجود را با Nix بسته‌بندی می‌کنید، مواجهه با خطاهایی که نامفهوم به‌نظر می‌رسند امری رایج است.

## مقدمه

در این آموزش، شما نخستین [درایویشن‌های Nix](/pages/nix-manual/language/derivations) خود را برای بسته‌بندی نرم‌افزارهای C/C++ ایجاد خواهید کرد.
شما از [محیط استاندارد Nixpkgs](https://nixos.org/manual/nixpkgs/stable/#part-stdenv) (`stdenv`) بهره خواهید برد که بخش عمده‌ای از کارهای مربوطه را خودکارسازی می‌کند.

### چه چیزی خواهید آموخت؟

این آموزش با `hello` آغاز می‌شود؛ پیاده‌سازی برنامه‌ی «hello world» که تنها نیازمند وابستگی‌هایی است که از پیش توسط `stdenv` فراهم شده‌اند.
در ادامه، بسته‌های پیچیده‌تری را که دارای وابستگی‌های خاص خود هستند می‌سازید، که این امر به استفاده از ویژگی‌های اضافی درایویشن منجر می‌شود.

شما با پیام‌های خطای Nix، شکست‌های ساخت و مجموعه‌ای از مشکلات دیگر مواجه شده و آن‌ها را رفع خواهید کرد و در طول مسیر، تکنیک‌های اشکال‌زدایی تکرارپذیر خود را توسعه می‌دهید.

### به چه چیزهایی نیاز دارید؟

- آشنایی با شل یونیکس و ویرایشگرهای متن ساده
- باید در [خواندن زبان Nix](reading-nix-language) تسلط کافی داشته باشید. در صورت نیاز می‌توانید ابتدا به عقب بازگشته و آن آموزش را مرور کنید.

### چقدر زمان می‌برد؟

گذراندن دقیق تمام مراحل حدود ۶۰ دقیقه طول خواهد کشید.

## نخستین بسته شما

:::{note}
<!--
TODO: link to the Nix manual glossary entry once it's in a released build:
https://hydra.nixos.org/job/nix/master/build.x86_64-linux/latest/download/manual/glossary.html#package
-->
یک _بسته_ مفهومی است که تعریف آزادی دارد و به مجموعه‌ای از فایل‌ها و داده‌های دیگر یا به یک {term}`عبارت نیکس (Nix expression)` که نماینده‌ی چنین مجموعه‌ای پیش از تحقق یافتن آن است، اشاره دارد.
بسته‌ها در Nixpkgs دارای ساختار مرسومی هستند که امکان کشف آن‌ها در جستجوها و ترکیب‌شان را در محیط‌ها در کنار سایر بسته‌ها فراهم می‌کند.

برای اهداف این آموزش، یک «بسته» تابعی از زبان Nix است که به یک derivation ارزیابی خواهد شد.
این کار شما یا دیگران را قادر می‌سازد تا در نتیجه‌ی «بسته‌بندی نرم‌افزار موجود با Nix»، یک فرآوردهٔ ساخت برای استفاده‌ی عملی تولید کنید.
:::

برای شروع، این derivation اسکلت را در نظر بگیرید:

```nix
{ stdenv }:

stdenv.mkDerivation {	}
```

این تابعی است که یک مجموعه ویژگی شامل `stdenv` را دریافت کرده و یک derivation (که در حال حاضر کاری انجام نمی‌دهد) تولید می‌کند.

### یک تابع بسته

GNU Hello پیاده‌سازی برنامه‌ی «سلام دنیا» است که کد منبع آن [از سرور FTP پروژه‌ی گنو](https://ftp.gnu.org/gnu/hello/) قابل دسترس است.

برای شروع، یک صفت (attribute) به نام `pname` به مجموعه ارسالی به `mkDerivation` اضافه کنید.
هر بسته به یک نام و یک نسخه نیاز دارد و نیکس بدون وجود آن‌ها خطای `error: derivation name missing` را پرتاب خواهد کرد.

```diff

stdenv.mkDerivation {
+ pname = "hello";
+ version = "2.12.1";

```

سپس، یک وابستگی به آخرین نسخه `hello` اعلام کنید و به Nix دستور دهید تا از `fetchzip` برای بارگیری [آرشیو کد منبع](https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz) استفاده کند.

:::{note}
`fetchzip` می‌تواند علاوه بر فایل‌های زیپ، [آرشیوهای بیشتری](https://nixos.org/manual/nixpkgs/stable/#fetchurl) را نیز دریافت کند!
:::

هش تا پیش از بارگیری و استخراج آرشیو قابل‌شناسایی نیست.
اگر هش ارائه‌شده به `fetchzip` نادرست باشد، Nix خطا خواهد داد.
صفت `hash` را روی یک رشته‌ی خالی تنظیم کنید و سپس با استفاده از پیام خطای حاصل، هش صحیح را مشخص کنید:

```nix
# hello.nix
{
  stdenv,
  fetchzip,
}:

stdenv.mkDerivation {
  pname = "hello";
  version = "2.12.1";

  src = fetchzip {
    url = "https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz";
    sha256 = "";
  };
}
```

این فایل را در `hello.nix` ذخیره کنید و `nix-build` را اجرا کنید تا اولین خطای ساخت خود را مشاهده کنید:

```console
$ nix-build hello.nix
error: cannot evaluate a function that has an argument without a value ('stdenv')
       Nix attempted to evaluate a function as a top level expression; in
       this case it must have its arguments supplied either by default
       values, or passed explicitly with '--arg' or '--argstr'. See
       /pages/nix-manual/language/constructs#functions.

       at /home/nix-user/hello.nix:3:3:

            2| {
            3|   stdenv,
             |   ^
            4|   fetchzip,
```

مشکل: عبارت موجود در فایل `hello.nix` یک *تابع* است که تنها در صورتی خروجی مورد نظر خود را تولید می‌کند که آرگومان‌های صحیح به آن ارسال شوند.

### ساخت با `nix-build`

مجموعه‌ی `stdenv` از [`nixpkgs`](https://github.com/NixOS/nixpkgs/) در دسترس است که باید با یک عبارت Nix دیگر درون‌ریزی شود تا به عنوان یک آرگومان به این derivation ارسال گردد.

روش توصیه‌شده برای انجام این کار، ایجاد یک فایل `default.nix` در همان پوشه‌ی `hello.nix` با محتوای زیر است:

```nix
# default.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
{
  hello = pkgs.callPackage ./hello.nix { };
}
```

این به شما اجازه می‌دهد تا `nix-build -A hello` را اجرا کنید تا درایویشن موجود در `hello.nix` را محقق سازید، که مشابه قرار داد فعلی مورد استفاده در Nixpkgs است.

:::{note}
تابع `callPackage` به طور خودکار صفات را از `pkgs` به تابع داده‌شده منتقل می‌کند، در صورتی که آن‌ها با صفات مورد نیاز مجموعه ویژگی آرگومان آن تابع مطابقت داشته باشند.
در این حالت، `callPackage` مقادیر `stdenv` و `fetchzip` را به تابع تعریف‌شده در `hello.nix` تحویل خواهد داد.

آموزش [](./callpackage.md) به جزئیات نحوه عملکرد این موضوع می‌پردازد.
:::

اکنون دستور `nix-build` را با آرگومان جدید اجرا کنید:

```console
$ nix-build -A hello
error: hash mismatch in fixed-output derivation '/nix/store/pd2kiyfa0c06giparlhd1k31bvllypbb-source.drv':
         specified: sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
            got:    sha256-1kJjhtlsAkpNB7f6tZEs+dbKd8z7KoNHyDHEJ0tmhnc=
error: 1 dependencies of derivation '/nix/store/b4mjwlv73nmiqgkdabsdjc4zq9gnma1l-hello-2.12.1.drv' failed to build
```

### پیدا کردن هش فایل
همان‌طور که انتظار می‌رفت، هش نادرست فایل باعث بروز خطا شد و Nix به طور مفیدی هش صحیح را ارائه کرد.
در `hello.nix`، رشته‌ی خالی را با هش صحیح جایگزین کنید:

```nix
# hello.nix
{
  stdenv,
  fetchzip,
}:

stdenv.mkDerivation {
  pname = "hello";
  version = "2.12.1";

  src = fetchzip {
    url = "https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz";
    sha256 = "sha256-1kJjhtlsAkpNB7f6tZEs+dbKd8z7KoNHyDHEJ0tmhnc=";
  };
}
```

اکنون دستور قبلی را دوباره اجرا کنید:

```console
$ nix-build -A hello
this derivation will be built:
  /nix/store/rbq37s3r76rr77c7d8x8px7z04kw2mk7-hello.drv
building '/nix/store/rbq37s3r76rr77c7d8x8px7z04kw2mk7-hello.drv'...
...
configuring
...
configure: creating ./config.status
config.status: creating Makefile
...
building
... <many more lines omitted>
```
درایویشن با موفقیت ساخته شد.

خروجی کنسول نشان می‌دهد که `configure` فراخوانی شده است، که یک `Makefile` تولید کرد و سپس از آن برای ساخت پروژه استفاده شد.
در این مورد نیازی به نوشتن هیچ‌گونه دستورالعمل ساختی نبود زیرا سیستم ساخت `stdenv` مبتنی بر [GNU Autoconf](https://www.gnu.org/software/autoconf/) است که به‌طور خودکار ساختار پوشه پروژه را تشخیص داد.

### نتیجه ساخت
پوشه کاری خود را برای دیدن نتیجه بررسی کنید:

```console
$ ls
default.nix hello.nix  result
```

این `result` یک [پیوند نمادین (symlink)](https://en.wikipedia.org/wiki/Symbolic_link) به مکانی در انبار Nix (Nix store) است که شامل باینری ساخته‌شده است؛ می‌توانید `./result/bin/hello` را برای اجرای این برنامه فراخوانی کنید:

```console
$ ./result/bin/hello
Hello, world!
```

تبریک می‌گوییم، شما با موفقیت اولین برنامه خود را با Nix بسته‌بندی کردید!

در ادامه، قطعه نرم‌افزار دیگری را با وابستگی‌های خارج از `stdenv` بسته‌بندی خواهید کرد که چالش‌های جدیدی را پیش رو می‌گذارد و شما را ملزم به استفاده از ویژگی‌های بیشتری از `mkDerivation` می‌کند.

## بسته‌ای با وابستگی‌ها

اکنون برنامه دوم و تا حدودی پیچیده‌اتری را اضافه کنید: [`icat`](https://github.com/atextor/icat) (که تصاویر را در ترمینال شما رندر می‌کند).

با افزودن یک صفت جدید برای `icat`، فایل `default.nix` را از بخش قبلی تغییر دهید:

```nix
# default.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
{
  hello = pkgs.callPackage ./hello.nix { };
  icat = pkgs.callPackage ./icat.nix { };
}
```

فایل `hello.nix` را به یک فایل جدید به نام `icat.nix` کپی کنید، و صفات `pname` و `version` را در آن فایل به‌روزرسانی کنید:

```nix
# icat.nix
{
  stdenv,
  fetchzip,
}:

stdenv.mkDerivation {
  pname = "icat";
  version = "v0.5";

  src = fetchzip {
    # ...
  };
}
```

اکنون نوبت به بارگیری کد منبع می‌رسد.
مخزن اصلی `icat` روی [GitHub](https://github.com/atextor/icat) میزبانی می‌شود، بنابراین باید [دریافت‌کننده‌ی کد منبع](https://nixos.org/manual/nixpkgs/stable/#chap-pkgs-fetchers) قبلی را جایگزین کنید.
این بار، به جای `fetchzip` از [`fetchFromGitHub`](https://nixos.org/manual/nixpkgs/stable/#fetchfromgithub) استفاده کنید و مجموعه ویژگی‌های آرگومان تابع را متناسب با آن به‌روزرسانی کنید:

```nix
# icat.nix
{
  stdenv,
  fetchFromGitHub,
}:

stdenv.mkDerivation {
  pname = "icat";
  version = "v0.5";

  src = fetchFromGitHub {
    # ...
  };
}
```

### دریافت کد منبع از گیت‌هاب
در حالی که `fetchzip` به آرگومان‌های `url` و `sha256` نیاز داشت، آرگومان‌های بیشتری برای [`fetchFromGitHub`](https://nixos.org/manual/nixpkgs/stable/#fetchfromgithub) مورد نیاز است.

URL کد منبع `https://github.com/atextor/icat` است که خود دو آرگومان نخست را فراهم می‌کند:
- `owner`: نام حسابی که مخزن را کنترل می‌کند
```
  owner = "atextor";
  ```
- `repo`: نام مخزنی که باید دریافت شود
```
  repo = "icat";
  ```

برای یافتن [Git revision](https://git-scm.com/docs/revisions) مناسب (`rev`)، مانند هش کامیت Git یا تگ (مثلاً `v1.0`) که با نسخه‌ای که می‌خواهید دریافت کنید مطابقت داشته باشد، به [صفحه تگ‌ها](https://github.com/atextor/icat/tags) پروژه مراجعه کنید.

در این مورد، آخرین تگ انتشار `v0.5` است.

مانند مثال `hello`، باید یک هش نیز ارائه شود.
این بار، به جای استفاده از رشته‌ی خالی و اجازه دادن به `nix-build` برای اعلام هش درست در قالب یک خطا، می‌توانید از همان ابتدا هش درست را با دستور `nix-prefetch-url` دریافت کنید.

شما به هش SHA256 *محتویات* فایل تارباز (به جای هش خود فایل تارباز) نیاز دارید.
بنابراین آرگومان‌های `--unpack` و `--type sha256` را ارسال کنید:

```console
$ nix-prefetch-url --unpack https://github.com/atextor/icat/archive/refs/tags/v0.5.tar.gz --type sha256
path is '/nix/store/p8jl1jlqxcsc7ryiazbpm7c1mqb6848b-v0.5.tar.gz'
0wyy2ksxp95vnh71ybj1bbmqd5ggp13x3mk37pzr99ljs9awy8ka
```

هش صحیح را برای `fetchFromGitHub` تنظیم کنید:

```nix
# icat.nix
{
  stdenv,
  fetchFromGitHub,
}:

stdenv.mkDerivation {
  pname = "icat";
  version = "v0.5";

  src = fetchFromGitHub {
    owner = "atextor";
    repo = "icat";
    rev = "v0.5";
    sha256 = "0wyy2ksxp95vnh71ybj1bbmqd5ggp13x3mk37pzr99ljs9awy8ka";
  };
}
```

### وابستگی‌های گم‌شده

با اجرای `nix-build` تنها روی صفت جدید `icat`، اشکال کاملاً جدیدی گزارش می‌شود:

```console
$ nix-build -A icat
these 2 derivations will be built:
  /nix/store/86q9x927hsyyzfr4lcqirmsbimysi6mb-source.drv
  /nix/store/l5wz9inkvkf0qhl8kpl39vpg2xfm2qpy-icat.drv
...
error: builder for '/nix/store/l5wz9inkvkf0qhl8kpl39vpg2xfm2qpy-icat.drv' failed with exit code 2;
       last 10 log lines:
       >                  from /nix/store/hkj250rjsvxcbr31fr1v81cv88cdfp4l-glibc-2.37-8-dev/include/stdio.h:27,
       >                  from icat.c:31:
       > /nix/store/hkj250rjsvxcbr31fr1v81cv88cdfp4l-glibc-2.37-8-dev/include/features.h:195:3: warning: #warning "_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE" [8;;https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#index-Wcpp-Wcpp8;;]
       >   195 | # warning "_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE"
       >       |   ^~~~~~~
       > icat.c:39:10: fatal error: Imlib2.h: No such file or directory
       >    39 | #include <Imlib2.h>
       >       |          ^~~~~~~~~~
       > compilation terminated.
       > make: *** [Makefile:16: icat.o] Error 1
       For full logs, run 'nix log /nix/store/l5wz9inkvkf0qhl8kpl39vpg2xfm2qpy-icat.drv'.
```

یک خطای کامپایلر.
سورس `icat` از گیت‌هاب دریافت شد و Nix تلاش کرد آنچه را پیدا کرده است بسازد، اما کامپایل به دلیل یک وابستگی مفقود با شکست مواجه شد: هدر `imlib2`.

اگر [عبارت `imlib2` را در سایت search.nixos.org جستجو کنید](https://search.nixos.org/packages?query=imlib2)، متوجه خواهید شد که `imlib2` از‌پیش در Nixpkgs وجود دارد.

با اضافه کردن `imlib2` به آرگومان‌های تابع موجود در فایل `icat.nix`، این بسته را به محیط ساخت خود اضافه کنید.
سپس مقدار آن آرگومان یعنی `imlib2` را به فهرست `buildInputs` در `stdenv.mkDerivation` اضافه کنید:

```nix
# icat.nix
{
  stdenv,
  fetchFromGitHub,
  imlib2,
}:

stdenv.mkDerivation {
  pname = "icat";
  version = "v0.5";

  src = fetchFromGitHub {
    owner = "atextor";
    repo = "icat";
    rev = "v0.5";
    sha256 = "0wyy2ksxp95vnh71ybj1bbmqd5ggp13x3mk37pzr99ljs9awy8ka";
  };

  buildInputs = [ imlib2 ];
}
```

دوباره دستور `nix-build -A icat` را اجرا کنید و با خطای دیگری مواجه خواهید شد، اما این بار فرآیند کامپایل پیشرفت بیشتری می‌کند:

```console
$ nix-build -A icat
this derivation will be built:
  /nix/store/bw2d4rp2k1l5rg49hds199ma2mz36x47-icat.drv
...
error: builder for '/nix/store/bw2d4rp2k1l5rg49hds199ma2mz36x47-icat.drv' failed with exit code 2;
       last 10 log lines:
       >                  from icat.c:31:
       > /nix/store/hkj250rjsvxcbr31fr1v81cv88cdfp4l-glibc-2.37-8-dev/include/features.h:195:3: warning: #warning "_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE" [8;;https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#index-Wcpp-Wcpp8;;]
       >   195 | # warning "_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE"
       >       |   ^~~~~~~
       > In file included from icat.c:39:
       > /nix/store/4fvrh0sjc8sbkbqda7dfsh7q0gxmnh9p-imlib2-1.11.1-dev/include/Imlib2.h:45:10: fatal error: X11/Xlib.h: No such file or directory
       >    45 | #include <X11/Xlib.h>
       >       |          ^~~~~~~~~~~~
       > compilation terminated.
       > make: *** [Makefile:16: icat.o] Error 1
       For full logs, run 'nix log /nix/store/bw2d4rp2k1l5rg49hds199ma2mz36x47-icat.drv'.
```

شما می‌توانید چند هشدار را مشاهده کنید که باید در کد بالادستی اصلاح شوند.
اما نکته‌ی مهم برای این آموزش، خطای `fatal error: X11/Xlib.h: No such file or directory` است: یک وابستگی دیگر وجود ندارد.

## پیدا کردن بسته‌ها

تعیین منبع مناسب برای یک وابستگی در حال حاضر تا حدودی پیچیده است، زیرا نام بسته‌ها همیشه با نام کتابخانه‌ها یا برنامه‌ها مطابقت ندارند.

شما به فایل‌های هدر `Xlib.h` از بسته C مربوط به `X11` نیاز دارید.
درایویشن Nixpkgs برای این مورد `libX11` است که در مجموعه بسته `xorg` در دسترس قرار دارد.
چندین راه برای فهمیدن این موضوع وجود دارد:

### `search.nixos.org`

:::{tip}
ساده‌ترین راه برای پیدا کردن آنچه نیاز دارید، مراجعه به search.nixos.org/packages است.
:::

متأسفانه در این مورد، [جستجوی عبارت `x11`](https://search.nixos.org/packages?query=x11) نتایج نامرتبط بسیار زیادی تولید می‌کند، زیرا X11 همه‌جا حاضر است.
در نوار کناری سمت چپ، فهرستی از مجموعه‌های بسته وجود دارد و [انتخاب `xorg`](https://search.nixos.org/packages?buckets={%22package_attr_set%22%3A[%22xorg%22]%2C%22package_license_set%22%3A[]%2C%22package_maintainers_set%22%3A[]%2C%22package_platforms%22%3A[]}&query=x11) چیزی امیدوارکننده را نشان می‌دهد.

اگر تمام راه‌ها با شکست مواجه شدند، آشنایی با نحوه جستجوی کلمات کلیدی در [کد منبع Nixpkgs](https://github.com/nixos/nixpkgs) کمک‌کننده خواهد بود.

### جستجوی محلی کد

برای پیدا کردن تخصیص‌های نام در کد منبع، عبارت `"<keyword> ="` را جستجو کنید.
برای مثال، این‌ها نتایج جستجوی [`"x11 = "`](https://github.com/search?q=repo%3ANixOS%2Fnixpkgs+%22x11+%3D%22&type=code) یا [`"libx11 ="`](https://github.com/search?q=repo%3ANixOS%2Fnixpkgs+%22libx11+%3D%22&type=code) در گیت‌هاب هستند.

یا اینکه یک کلون از [مخزن Nixpkgs](https://github.com/nixos/nixpkgs) را دریافت کرده و کد را به صورت محلی جستجو کنید.

یک شل را راه‌اندازی کنید که ابزارهای مورد نیاز را در دسترس قرار دهد؛ ابزار `git` برای کنترل نسخه، و `rg` برای جستجوی کد (که توسط [بسته `ripgrep`](https://search.nixos.org/packages?show=ripgrep) فراهم شده است):
```console
$ nix-shell -p git ripgrep
[nix-shell:~]$
```

مخزن Nixpkgs بسیار بزرگ است.
برای جلوگیری از انتظار طولانی جهت کلون کامل، فقط آخرین نسخه را کلون کنید:

```console
[nix-shell:~]$ git clone https://github.com/NixOS/nixpkgs --depth 1
...
[nix-shell:~]$ cd nixpkgs/
```

برای محدود کردن نتایج، فقط پوشه‌ی `pkgs` را جستجو کنید که تمام دستورالعمل‌های بسته‌ها را در خود نگه می‌دارد:

```console
[nix-shell:~]$ rg "x11 =" pkgs
pkgs/tools/X11/primus/default.nix
21:  primus = if useNvidia then primusLib_ else primusLib_.override { nvidia_x11 = null; };
22:  primus_i686 = if useNvidia then primusLib_i686_ else primusLib_i686_.override { nvidia_x11 = null; };

pkgs/applications/graphics/imv/default.nix
38:    x11 = [ libGLU xorg.libxcb xorg.libX11 ];

pkgs/tools/X11/primus/lib.nix
14:    if nvidia_x11 == null then libGL

pkgs/top-level/linux-kernels.nix
573:    ati_drivers_x11 = throw "ati drivers are no longer supported by any kernel >=4.1"; # added 2021-05-18;
... <a lot more results>
```

از آنجا که `rg` به طور پیش‌فرض نسبت به بزرگی و کوچکی حروف حساس است،
برای اطمینان از اینکه چیزی را از دست نمی‌دهید، `-i` را اضافه کنید:

```
[nix-shell:~]$ rg -i "libx11 =" pkgs
pkgs/applications/version-management/monotone-viz/graphviz-2.0.nix
55:    ++ lib.optional (libX11 == null) "--without-x";

pkgs/top-level/all-packages.nix
14191:    libX11 = xorg.libX11;

pkgs/servers/x11/xorg/default.nix
1119:  libX11 = callPackage ({ stdenv, pkg-config, fetchurl, xorgproto, libpthreadstubs, libxcb, xtrans, testers }: stdenv.mkDerivation (finalAttrs: {

pkgs/servers/x11/xorg/overrides.nix
147:  libX11 = super.libX11.overrideAttrs (attrs: {
```

### جستجوی محلی derivation

برای جستجوی derivationها در خط فرمان، از `nix-locate` موجود در [`nix-index`](https://github.com/nix-community/nix-index) استفاده کنید.

### افزودن مجموعه‌ی بسته‌ها به عنوان وابستگی‌ها

مجموعه ویژگی ورودی درایویشن خود را با افزودن `xorg` کامل کرده و از `xorg.libX11` در `buildInputs` استفاده کنید:

```nix
# icat.nix
{
  stdenv,
  fetchFromGitHub,
  imlib2,
  xorg,
}:

stdenv.mkDerivation {
  pname = "icat";
  version = "v0.5";

  src = fetchFromGitHub {
    owner = "atextor";
    repo = "icat";
    rev = "v0.5";
    sha256 = "0wyy2ksxp95vnh71ybj1bbmqd5ggp13x3mk37pzr99ljs9awy8ka";
  };

  buildInputs = [ imlib2 xorg.libX11 ];
}
```

:::{note}
از آنجا که زبان Nix به‌صورت تنبل ارزیابی می‌شود، دسترسی تنها به `xorg.libX11` به این معنا است که محتویات باقی‌مانده‌ی مجموعه ویژگی `xorg` هرگز پردازش نمی‌شوند.
:::

## رفع خطاهای ساخت

دستور قبلی را دوباره اجرا کنید:

```console
$ nix-build -A icat
this derivation will be built:
  /nix/store/x1d79ld8jxqdla5zw2b47d2sl87mf56k-icat.drv
...
error: builder for '/nix/store/x1d79ld8jxqdla5zw2b47d2sl87mf56k-icat.drv' failed with exit code 2;
       last 10 log lines:
       >   195 | # warning "_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE"
       >       |   ^~~~~~~
       > icat.c: In function 'main':
       > icat.c:319:33: warning: ignoring return value of 'write' declared with attribute 'warn_unused_result' [8;;https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#index-Wunused-result-Wunused-result8;;]
       >   319 |                                 write(tempfile, &buf, 1);
       >       |                                 ^~~~~~~~~~~~~~~~~~~~~~~~
       > gcc -o icat icat.o -lImlib2
       > installing
       > install flags: SHELL=/nix/store/8fv91097mbh5049i9rglc73dx6kjg3qk-bash-5.2-p15/bin/bash install
       > make: *** No rule to make target 'install'.  Stop.
       For full logs, run 'nix log /nix/store/x1d79ld8jxqdla5zw2b47d2sl87mf56k-icat.drv'.
```

خطای مربوط به کمبود وابستگی برطرف شده است، اما اکنون مشکل دیگری وجود دارد: `make: *** No rule to make target 'install'.  Stop.`

### `installPhase`
ابزار `stdenv` به‌طور خودکار با فایل `Makefile` که همراه با `icat` ارائه شده است کار می‌کند.
خروجی کنسول نشان می‌دهد که مراحل `configure` و `make` بدون مشکل اجرا می‌شوند، بنابراین باینری `icat` با موفقیت در حال کامپایل شدن است.

خط زمانی رخ می‌دهد که `stdenv` تلاش می‌کند `make install` را اجرا کند.
فایل `Makefile` موجود در پروژه به طور اتفاقی فاقد هدف `install` است.
فایل `README` در مخزن `icat` تنها به استفاده از `make` برای ساخت ابزار اشاره می‌کند و مرحله‌ی نصب را به عهده‌ی کاربران می‌گذارد.

برای اضافه کردن این مرحله به درایویشن خود، از [`installPhase` attribute](https://nixos.org/manual/nixpkgs/stable/#ssec-install-phase) استفاده کنید.
این ویژگی حاوی فهرستی از رشته‌دستورات است که برای انجام عملیات نصب اجرا می‌شوند.

از آنجا که `make` با موفقیت به پایان می‌رسد، فایل اجرایی `icat` در پوشه‌ی ساخت موجود است.
شما فقط باید آن را از آنجا به پوشه‌ی خروجی کپی کنید.

در Nix، پوشه‌ی خروجی در متغیر `$out` ذخیره می‌شود.
این متغیر در [`builder` execution environment](/pages/nix-manual/language/derivations#builder-execution) مربوط به درایویشن قابل دسترس است.
یک پوشه‌ی `bin` درون پوشه‌ی `$out` ایجاد کنید و باینری `icat` را به آنجا کپی کنید:

```nix
# icat.nix
{
  stdenv,
  fetchFromGitHub,
  imlib2,
  xorg,
}:

stdenv.mkDerivation {
  pname = "icat";
  version = "v0.5";

  src = fetchFromGitHub {
    owner = "atextor";
    repo = "icat";
    rev = "v0.5";
    sha256 = "0wyy2ksxp95vnh71ybj1bbmqd5ggp13x3mk37pzr99ljs9awy8ka";
  };

  buildInputs = [ imlib2 xorg.libX11 ];

  installPhase = ''
    mkdir -p $out/bin
    cp icat $out/bin
  '';
}
```

### فازها و قلاب‌ها

درایویشن‌های `stdenv.mkDerivation` در Nixpkgs به [فازها](https://nixos.org/manual/nixpkgs/stable/#sec-stdenv-phases) مختلفی تقسیم می‌شوند.
هر فاز به منظور کنترل جنبه‌ای خاص از فرآیند ساخت در نظر گرفته شده است.

پیش‌تر مشاهده کردید که `stdenv.mkDerivation` انتظار داشت `Makefile` پروژه دارای یک هدف `install` باشد و در غیر این صورت با خطا مواجه شد.
برای رفع این مشکل، شما یک `installPhase` سفارشی تعریف کردید که حاوی دستورالعمل‌هایی برای کپی کردن باینری `icat` به محل خروجی صحیح، یعنی در واقع نصب آن بود.
تا آن نقطه، `stdenv.mkDerivation` به طور خودکار اطلاعات `buildPhase` را برای بستهٔ `icat` تعیین کرده بود.

در طول تحقق درایویشن، تعدادی تابع شل («قلاب‌ها» یا همان hooks در Nixpkgs) وجود دارند که ممکن است در هر فاز از درایویشن اجرا شوند.
قلاب‌ها کارهایی مانند تنظیم متغیرها، منبع‌یابی فایل‌ها، ایجاد پوشه‌ها و غیره را انجام می‌دهند.

این موارد مختص هر فاز هستند و هم قبل و هم بعد از اجرای آن فاز اجرا می‌شوند.
آن‌ها محیط ساخت را برای عملیات رایج در طول ساخت تغییر می‌دهند.

فراخوانی این قلاب‌ها را در فازهای درایویشنی که تعریف می‌کنید بگنجانید، حتی زمانی که مستقیماً از آن‌ها استفاده نمی‌کنید.
این کار بعدها [بازنشانی](https://nixos.org/manual/nixpkgs/stable/#chap-overrides) آسان بخش‌های خاصی از درایویشن را تسهیل می‌کند.
همچنین کد را مرتب نگه داشته و خواندن آن را ساده‌تر می‌کند.

`installPhase` خود را طوری تنظیم کنید که قلاب‌های مناسب را فراخوانی کند:

```nix
# icat.nix

# ...

  installPhase = ''
    runHook preInstall
    mkdir -p $out/bin
    cp icat $out/bin
    runHook postInstall
  '';

# ...

```

## یک ساخت موفق

اجرای مجدد دستور `nix-build -A icat` در نهایت کار دلخواه شما را به شکلی تکرارپذیر انجام خواهد داد.
دستور `ls` را در پوشه‌ی محلی فراخوانی کنید تا یک پیوند نمادین `result` را که به مسیری در انبار Nix اشاره می‌کند، بیابید:

```console
$ ls
default.nix hello.nix icat.nix result
```

دستور `result/bin/icat` همان فایل اجرایی است که پیش‌تر ساخته شد. موفقیت‌آمیز بود!

اجرای دستور `nix-build` (بدون مشخص کردن یک صفت) تمام صفات را به‌طور هم‌زمان می‌سازد.
اولین صفت (`hello`) در مسیر `result/bin/` ظاهر می‌شود، در حالی که دومین صفت (`icat`) در مسیر `result-2/bin/` قرار می‌گیرد.
افزودن صفات بیشتر، پیوندهای نمادین اضافی `result-n` را تولید می‌کند.

## منابع

- [راهنمای Nixpkgs - محیط استاندارد](https://nixos.org/manual/nixpkgs/unstable/#part-stdenv)

## گام‌های بعدی

- [](callpackage-tutorial)
- [](sharing-dependencies)
- [](automatic-direnv)
- [](python-dev-environment)
- [افزودن بسته‌های جدید خود به Nixpkgs](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md)
  - [](../contributing/how-to-contribute.md)
  - [](../contributing/how-to-get-help.md)
