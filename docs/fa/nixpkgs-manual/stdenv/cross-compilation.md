# کامپایل متقاطع {#chap-cross}

## مقدمه {#sec-cross-intro}

«کامپایل متقاطع» به معنای کامپایل کردن یک برنامه روی یک ماشین برای نوع دیگری از ماشین است. یک کاربرد معمول کامپایل متقاطع، کامپایل کردن برنامه‌ها برای دستگاه

```nix
{
  stdenv,
  fooDep,
  barDep,
  ...
}:
{
  # ...stdenv.buildPlatform...
}
```

نت‌های لیست‌سفیدشده است. این را می‌توان به صورت مستقیم مشخص کرد، یا در واقع از `config` تجزیه نمود. برای بازنمایی دقیق به `lib.systems.parse` مراجعه کنید.

Block 11:
`libc`

: This is a string identifying the standard C library used. Valid identifiers include "glibc" for GNU libc, "libSystem" for Darwin's Libsystem, and "uclibc" for

: این گزاره‌ها در `lib.systems.inspect` تعریف شده‌اند و به هر پلتفرم اضافه شده‌اند. آن‌ها نسبت به موارد موجود در `stdenv` برتری دارند زیرا کاربر را مجبور می‌کنند درباره‌ی پلتفرمی که در حال بررسی آن است صریح باشد. لطفاً به جای آن‌ها از این موارد استفاده کنید.

`platform`

: این بخش، صریحاً بگویم، محل انباشت تنظیمات آنی (ad-hoc) است (یک مجموعه ویژگی است). برای مشاهده نمونه‌ها به `lib.systems.platforms` مراجعه کنید

انواع وابستگی، روابطی را که یک بسته با هر یک از وابستگی‌های متعدی (transitive) خود دارد، توصیف می‌کنند. می‌توانید این‌طور تصور کنید که یک یا چند نوع وابستگی را به هر یک از پارامترهای رسمی در بالای فایل `.nix` یک بسته، و همچنین به همه‌ی پارامترهای رسمی *آن‌ها* و الی آخر نسبت می‌دهید. در مقابل، سه‌تایی‌هایی مانند `(foo

* `g++` اجازه استفاده از کد اسمبلر درون‌خطی را می‌دهد، بنابراین به دسترسی به نسخه‌ای از اسمبلر `gas` وابسته است. این یک وابستگی "host→ target" با سه‌تایی `(foo, bar, baz)` خواهد بود.

* `g++` (و `gcc`) شامل یک کتاب

```nix
stdenv.mkDerivation {
  # ...
  doCheck = stdenv.hostPlatform.emulatorAvailable buildPackages;
  checkPhase = ''
    ${stdenv.hostPlatform.emulator buildPackages} ./my-binary --self-test
  '';
}
```

برای اجرای یک باینری کامپایل متقاطع‌شده در خارج از محیط ایزوله (sandbox) Nix، آن را بسازید و شبیه‌ساز را از یک شل (Shell) فراخوانی کنید. این روش همچنین راهی سریع برای تأیید جدول توزیع بالاست:

```ShellSession
$ nix-build '<nixpkgs>' -A pkgsCross.aarch64-multiplatform.hello # Should be available in cache.nixos.org
```

برای دریافت مسیر یک شبیه‌ساز، با داشتن یک `crossSystem.config` (مثلاً با `aarch64-linux`):

```ShellSession
$ nix-instantiate --eval --strict -E \
    '(import <nixpkgs> { crossSystem.config = "aarch64-unknown-linux-gnu"; }).stdenv.hostPlatform.emulator (import <nixpkgs> {})'
"/nix/store/.../bin/qemu-aarch64"
```

و به‌طور خاص برای `aarch64-linux` و بسیاری از پلتفرم‌های دیگر، همه‌ی آن‌ها در بسته‌ی `qemu` در دسترس هستند؛ به این معنی که می‌توانید به سادگی اجرا کنید:

```ShellSession
$ nix-shell -p qemu --run 'qemu-aarch64 ./result/bin/hello'
Hello, world!
```

همین الگو برای مقاصد دیگر نیز با جایگزین کردن صفت (attribute) `pkgsCross.*` و بسته شبیه‌ساز (به عنوان مثال `wine` برای `

```nix
{ makeFlags = [ "CC=${stdenv.cc.targetPrefix}cc" ]; }
```

طول بکشد) ممکن است دشوار باشد. Nixpkgs یک [مجموعه‌کار مربوط به کامپایل متقاطع در Hydra](https://hydra.nixos.org/jobset/n

```ShellSession
$ nix-build '<nixpkgs>' -A pkgsCross.raspberryPi.hello
```

#### چه می‌شود اگر سیستم ساخت بسته‌ی شما نیاز به ساخت یک برنامه C برای اجرا در محیط ساخت داشته باشد؟ {#cross-qa-build-c-program-in-build-environment}

موارد زیر را به فراخوانی `mkDerivation` خود اضافه کنید.

```nix
{ depsBuildBuild = [ buildPackages.stdenv.cc ]; }
```

#### مجموعه تست بسته‌ام به اجرای کد پلتفرم میزبان نیاز دارد. {#cross-testsuite-runs-host-code}

موارد زیر را به فراخوانی `mkDerivation` خود اضافه کنید.

```nix
{ doCheck = stdenv.buildPlatform.canExecute stdenv.hostPlatform; }
```

#### بسته‌ای که از Meson استفاده می‌کند نیاز دارد باینری‌های پلتفرم میزبان را در طول ساخت اجرا کند. {#cross-meson-runs-host-code}

`mesonEmulatorHook` را مشروط بر اینکه باینری‌های هدف قابل اجرا باشند، به `nativeBuildInputs` اضافه کنید.

برای مثال:

```nix
{
  nativeBuildInputs = [
    meson
  ]
  ++ lib.optionals (!stdenv.buildPlatform.canExecute stdenv.hostPlatform) [ mesonEmulatorHook ];
}
```

نمونه‌ای از خطایی که این اقدام آن را برطرف می‌کند.

`[Errno 8] Exec format error: './gdk3-scan'`

```nix
{
  buildInputs = lib.optionals (stdenv.hostPlatform.libc == "glibc") [ stdenv.cc.libc.static ];
}
```

مثال‌هایی از خطاهایی که این مورد برطرف می‌کند:

`cannot find -lm: No such file or directory`

`cannot find -lc: No such file or directory`

::: {.note}
در زمان نگارش این مطلب، فرض بر این است که این مشکل تنها در `glibc` رخ می‌دهد، زیرا کتابخانه‌های ایستا (static) را به خروجی متفاوتی تقسیم می‌کند.

::: {.note}
ممکن است بخواهید استفاده از `stdenvAdapters.makeStatic` یا `pkgsStatic` یا پلتفرمی با `isStatic = true` را بررسی کنید.

## کامپایل متقاطع بسته‌ها {#sec-cross-usage}

Nixpkgs را می‌توان تنها با `localSystem` نمونه‌سازی کرد که در این حالت کامپایل متقاطع انجام نمی‌شود و همه‌چیز توسط همان سیستم و برای آن ساخته می‌شود؛ یا همچنین

```ShellSession
$ nix-build '<nixpkgs>' --arg crossSystem '(import <nixpkgs/lib>).systems.examples.fooBarBaz' -A whatever
```

::: {.note}
در نهایت مایلیم این نمونه‌های پلتفرم را به یک سهولت غیرضروری تبدیل کنیم تا

```ShellSession
$ nix-build '<nixpkgs>' --arg crossSystem '{ config = "<arch>-<os>-<vendor>-<abi>"; }' -A whatever
```

در اکثر قریب به اتفاق موارد کار می‌کند. مشکل امروز، وابستگی‌ها به انواع دیگری از پیکربندی است که مقادیر پیش‌فرض مناسبی برای آن‌ها ارائه نشده است. ما به مثال‌ها متکی هستیم تا به شکلی خام، آن پارامترهای پیکربندی را از طرف کاربر به طریقی کم‌وبیش عاقلانه تنظیم کنیم. موضوع [\#34274](https://github.com/NixOS/nixpkgs/issues/34274) این مشکل را همراه با علت اصلی آن در گزینه‌های پیکربندی کهنه و نامناسب پیگیری می‌کند.
:::

اگرچه هر کسی آزاد است که هر دو پارامتر را به‌طور کامل ارسال کند، منطق زیادی برای پر کردن فیلدهای مفقود وجود دارد. همان‌طور که

برای `pkgsBuildHost` ،`pkgsHostTarget` و `pkgsTargetTarget` بازتعریف شده‌اند. استفاده از آن‌ها برای نشان دادن اینکه فقط پلتفرم میزبان آن‌ها اهمیت دارد، پذیرفته‌شده و حتی توصیه می‌شود. یعنی هرجا هر یک از `pkgsBuild*` کارساز باشد، از `buildPackages` استفاده کنید، و زمانی که هر یک از `pkgsTarget*` کافی باشد (اگر چیزی بیش از فقط `

برای کارکرد درست این روند، ما شش مجموعه بسته‌ی `pkgs<theirHost><theirTarget>` را به یکدیگر پیوند می‌دهیم (splice می‌کنیم) و کاری می‌کنیم که `callPackage` آرگومان‌هایش را در واقع از آن دریافت کند. این موضوع در حال حاضر در `pkgs/top-level/splice.nix` پیاده‌
```
(native, native, native, foreign, foreign)
```

اگر تصور کنید که خودارجاعی‌های اشباع‌کننده در انتها با مراحل بی‌نهایت جایگزین شوند و سپس آن سه‌تایی‌های پلتفرم روی هم قرار گیرند، در نهایت به یک چندتایی بی‌نهایت می‌رسید:
```
(native..., native, native, native, foreign, foreign, foreign...)
```
2:
::: {.note}
If one explores Nixpkgs, they will see derivations with names like `gccCross`. Such `*Cross` derivations is a holdover from before we properly distinguished between the host and target platforms، the derivation with “Cross” in the name covered the `build = host != target` case, while the other covered the `host = target`, with build platform the same
