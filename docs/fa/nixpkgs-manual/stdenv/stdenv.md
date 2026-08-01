Nixpkgs)، محیطی را برای ساخت بسته‌های یونیکس فراهم می‌کند که بسیاری از کارهای رایج ساخت را به طور خودکار انجام می‌دهد. در واقع، برای بسته‌های یونیکسی که از رابط ساخت استاند

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  src = fetchurl {
    url = "http://example.org/libfoo-1.2.3.tar.bz2";
    hash = "sha256-tWxU/LANbQE32my+9AXyt3nCT7NBVfJ45CX757EMT3Q=";
  };
}
```

` -> Nixpkgs
- `function argument` -> آرگومان تابع
- `version` -> نسخه

Ensure bold formatting is preserved:
**از زمان [RFC 0035

```nix
stdenv.mkDerivation (finalAttrs: {
  pname = "libfoo";
  version = "1.2.3";
  src = fetchurl {
    url = "http://example.org/libfoo-source-${finalAttrs.version}.tar.bz2";
    hash = "sha256-tWxU/LANbQE32my+9AXyt3nCT7NBVfJ45CX757EMT3Q=";
  };
})
```

بسیاری از بسته‌ها دارای وابستگی‌هایی هستند که در محیط استاندارد ارائه نشده‌اند. معمولاً کافی است آن وابستگی‌ها را در صفت `buildInputs` مشخص کنید:

```nix
stdenv.mkDerivation {
  pname = "libfoo";
  version = "1.2.3";
  # ...
  buildInputs = [
    libbar
    perl
    ncurses
  ];
}
```

این صفت (attribute) تضمین می‌کند که زیرپوشه‌های `bin` این بسته‌ها در طول ساخت (Build) در متغیر محیطی `PATH` ظاهر شوند، زیرپوشه‌های `include` آن‌ها توسط

```nix
stdenv.mkDerivation {
  pname = "fnord";
  version = "4.5";

  # ...

  buildPhase = ''
    runHook preBuild

    gcc foo.c -o foo

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cp foo $out/bin

    runHook postInstall
  '';
}
```

(به استفاده از رشته‌های متنی با سبک `''` توجه کنید که برای قطعه‌اسکریپت‌های بزرگ چندخطی بسیار کاربردی هستند، زیرا نیازی به اسکیپ کردن `"` و `\` ندارند و تورفتگی در آن‌ها به‌صورت هوشمندانه حذف می‌شود.)

صفات متعدد دیگری نیز برای سفارشی‌سازی ساخت وجود دارد. این صفات در [](#ssec-stdenv-attributes) فهرست شده‌اند.

اگرچه محیط استاندارد یک سازنده عمومی ارائه می‌دهد، شما همچنان می‌توانید اسکریپت ساخت اختصاصی خود را ارائه دهید:

```nix
stdenv.mkDerivation {
  pname = "libfoo";
  version = "1.2.3";
  # ...
  builder = ./builder.sh;
}
```

که در آن `stdenv` محیط را به طور خودکار آماده می‌کند (مثلاً با بازنشانی `PATH` و پر کردن آن از ورودی‌های ساخت). در صورت تمایل، می‌توانید از سازنده عمومی `stdenv` استفاده کنید:

```bash
buildPhase() {
  echo "... this is my custom build phase ..."
  gcc foo.c -o foo
}

installPhase() {
  mkdir -p $out/bin
  cp foo $out/bin
}

genericBuild
```

### ساخت یک بسته `stdenv` در `nix-shell` {#sec-building-stdenv-package-in-nix-shell}

برای ساخت یک بسته `stdenv` در یک [`nix-shell`](https://nixos.org/manual/nix/unstable/command-ref/nix-shell.html)، وارد یک شل شوید، [فازهایی](#sec-stdenv-phases) را که می‌خواهید بسازید پیدا کنید، سپس `genericBuild` را به صورت دستی فراخوانی کنید:

به یک پوشه خالی بروید، `nix-shell` را با بسته مورد نظر فراخوانی کنید، و از داخل شل، متغیرهای خروجی را روی یک پوشه قابل نوشتن تنظیم کنید:

```bash
cd "$(mktemp -d)"
nix-shell '<nixpkgs>' -A some_package
export out=$(pwd)/out
```

در ادامه، بخش‌های مورد نظر ساخت را فراخوانی کنید.
نخست، فازهایی را اجرا کنید که یک نسخهٔ کاری از کدهای منبع را تولید می‌کنند، که پوشه را برای شما به کدهای منبع تغییر خواهند داد:

```bash
phases="${prePhases[*]:-} unpackPhase patchPhase" genericBuild
```

سپس، فازهای بیشتری را تا رسیدن به خطا اجرا کنید.
اگر خطا در فاز ساخت یا بررسی باشد، فازهای زیر مورد نیاز خواهند بود:

```bash
phases="${preConfigurePhases[*]:-} configurePhase ${preBuildPhases[*]:-} buildPhase checkPhase" genericBuild
```

از این دستور برای اجرای تمامی فازهای نصب استفاده کنید:
```bash
phases="${preInstallPhases[*]:-} installPhase ${preFixupPhases[*]:-} fixupPhase installCheckPhase" genericBuild
```

یک فاز منفرد را می‌توان به تعداد دفعات لازم برای بررسی خطا به این صورت مجدداً اجرا کرد:

```bash
phases="buildPhase" genericBuild
```

برای تغییر یک [فاز](#sec-stdenv-phases)، ابتدا آن را با

```bash
echo "$buildPhase"
```

یا اگر آن خالی است، برای مثال، اگر از یک تابع استفاده می‌کند:

```bash
type buildPhase
```

در اینجا برسی کلی از رایج‌ترین آن‌ها آورده شده‌است.
        *   EN: `It should cover most use cases.`
        *   FA: این بخش باید اکثر موارد استفاده را پوشش دهد.

    *   **List 2:**
        *   EN: `Add dependencies to `nativeBuildInputs` if they are executed during the build:`
        *   FA: اگر وابستگی‌ها هنگام ساخت اجرا می‌شوند، آن‌ها را به `nativeBuild

وابستگی‌هایی که تنها برای اجرای تست‌ها مورد نیازند، به همین شکل به بومی (اجراشده در طول ساخت) و غیر بومی (اجراشده در زمان اجرا) دسته‌بندی می‌شوند:
```nix
stdenv.mkDerivation (finalAttrs: {
  pname = "solo5";
  version = "0.7.5";

  src = fetchurl {
    url = "https://github.com/Solo5/solo5/releases/download/v${finalAttrs.version}/solo5-v${finalAttrs.version}.tar.gz";
    hash = "sha256-viwrS9lnaU8sTGuzK/+L/PlMM/xRRtgVuK5pixVeDEw=";
  };

  nativeBuildInputs = [
    makeWrapper
    pkg-config
  ];

  buildInputs = [ libseccomp ];

  postInstall = ''
    substituteInPlace $out/bin/solo5-virtio-mkimage \
      --replace-fail "/usr/lib/syslinux" "${syslinux}/share/syslinux" \
      --replace-fail "/usr/share/syslinux" "${syslinux}/share/syslinux" \
      --replace-fail "cp " "cp --no-preserve=mode "

    wrapProgram $out/bin/solo5-virtio-mkimage \
      --prefix PATH : ${
        lib.makeBinPath [
          dosfstools
          mtools
          parted
          syslinux
        ]
      }
  '';

  doCheck = true;
  nativeCheckInputs = [
    util-linux
    qemu
  ];
  # `checkPhase` elided
})
```

گی‌های پایین‌دست قرار می‌گیرند.
این موضوع به‌ویژه برای زبان‌های تفسیری مفید است، جایی که همه وابستگی‌های متعدی (transitive) باید در همان محیط موجود باشند.
بنابراین، این روش برای زیرساخت پایتون در Nixpkgs استفاده می‌شود.

Blockquote note:
:::{.note}
Propagated dependencies should be used with care, because they obscure the actual build

```nix
with import <nixpkgs> { };
let
  bar = stdenv.mkDerivation {
    name = "bar";
    dontUnpack = true;
    # `hello` is also made available to dependents, such as `foo`
    propagatedBuildInputs = [ hello ];
    postInstall = "mkdir $out";
  };
  foo = stdenv.mkDerivation {
    name = "foo";
    dontUnpack = true;
    # `bar` is a direct dependency, which implicitly includes the propagated `hello`
    buildInputs = [ bar ];
    # The `hello` binary is available!
    postInstall = "hello > $out";
  };
in
foo
```
:::

انتشار وابستگی کامپایل متقاطع را در نظر می‌گیرد، به این معنی که وابستگی‌هایی که از مرزهای پلتفرم عبور می‌کنند به طور مناسب تنظیم می‌شوند.

برای تعیین قوانین دقیق انتشار وابستگی، ابتدا به هر وابستگی جفتی از مقادیر سه‌تایی (`-1` برای `build`، `0` برای `host` و `1` برای `target`) اختصاص می‌دهیم که نشان‌دهنده [

```
  h |   t  || i=-1 |  i=0 |  i=1
----|------||------|------|-----
 -1 |  -1  ||   x  |  -1  |  -1
 -1 |   0  ||   x  |  -1  |   0
 -1 |   1  ||   x  |  -1  |   1
  0 |   0  ||  -1  |   0  |   0
  0 |   1  ||  -1  |   0  |   1
  1 |   1  ||   0  |   1  |   x
```

:::

```
let mapOffset(h, t, i) = i + (if i <= 0 then h else t - 1)

propagated-dep(h0, t0, A, B)
propagated-dep(h1, t1, B, C)
h0 + h1 in {-1, 0, 1}
h0 + t1 in {-1, 0, 1}
-------------------------------------- Transitive property
propagated-dep(mapOffset(h0, t0, h1),
               mapOffset(h0, t0, t1),
               A, C)
```

```
let mapOffset(h, t, i) = i + (if i <= 0 then h else t - 1)

dep(h0, t0, A, B)
propagated-dep(h1, t1, B, C)
h0 + h1 in {-1, 0, 1}
h0 + t1 in {-1, 0, 1}
----------------------------- Take immediate dependencies' propagated dependencies
propagated-dep(mapOffset(h0, t0, h1),
               mapOffset(h0, t0, t1),
               A, C)
```

```
propagated-dep(h, t, A, B)
----------------------------- Propagated dependencies count as dependencies
dep(h, t, A, B)
```

ارائه توضیحی دربارهٔ این ساختار پیچیده لازم است. در حالت معمولِ `nativeBuildInputs` یا `buildInputs`، آفست هدفِ یک وابستگی، یکی بیشتر از آفست میزبان است: `t = h + 1`. این بدین معناست که:

```
let f(h, t, i) = i + (if i <= 0 then h else t - 1)
let f(h, h + 1, i) = i + (if i <= 0 then h else (h + 1) - 1)
let f(h, h + 1, i) = i + (if i <= 0 then h else h)
let f(h, h + 1, i) = i + h
```

اینجاست که مفهوم «شبیه به جمع» از مطالب بالا مطرح می‌شود: می‌توانیم به‌سادگی تمام جابه‌جایی‌های (offset) هاست را جمع کنیم تا جابه‌جایی هاستِ وابستگی متعدی (transitive dependency) را به دست آوریم. جابه‌جایی هدفِ وابستگی متعدی برابر با جابه‌جایی هاست + ۱ است، درست همان‌طور که در وابستگی‌های ترکیب‌شده برای ساخت این وابستگی متعدی وجود داشت؛ از آن می‌توان صرف‌نظر کرد چرا که اطلاعات جدیدی اضافه نمی‌کند.

به دلیل بررسی‌های محدوده، حالت‌های غیرمعمول عبارت‌اند از `h = t` (`depsBuildBuild` و غیره) و `h + 2 = t` (`depsBuildTarget`).

در حالت نخست، انگیزه استفاده از `mapOffset` این است که از آنجا که پلتفرم‌های هاست و هدف آن یکسان هستند، هیچ وابستگی متعدی از آن نباید بتواند جابه‌جاییِ بزرگ‌تری نسبت به جابه‌جایی‌های هدفِ کاهش‌یافته‌اش «کشف» کند. `mapOffset` به‌طور موثری تمام جابه‌جایی‌های وابستگی‌های متعدی آن را «فشرده» (squash

فهرستی از وابستگی‌ها که پلتفرم میزبان آن‌ها پلتفرم ساخت derivation جدید، و پلتفرم هدف آن‌ها پلتفرم میزبان derivation جدید است. این‌ها برنامه‌ها و کتابخانه‌هایی هستند که در زمان ساخت استفاده می‌شوند و اگر یک کامپایلر یا ابزار مشابه باشند، کدی تولید می‌کنند که در زمان اجرا اجرا می‌شود، یعنی ابزارهایی که برای ساخت derivation جدید استفاده می‌شوند. اگر وابستگی اهمیتی به پلتفرم هدف نمی‌دهد (یعنی یک کامپایلر یا ابزار مشابه نیست)، آن را به جای `depsBuildBuild` یا `depsBuildTarget` در اینجا قرار دهید. این بخش می‌توانست `depsBuildHost` نامیده شود، اما به دلیل تداوم تاریخی از `nativeBuildInputs` استفاده می‌شود.

از آنجایی که این بسته‌ها قادر به اجرا در زمان ساخت هستند، همان‌طور که در بالا توصیف شد به `PATH` اضافه می‌شوند. اما از آنجایی که اجرای این بسته‌ها تنها در آن زمان تضمین می‌شود، نباید به عنوان وابستگی‌های زمان اجرا باقی بمانند. این موضوع در حال حاضر اعمال نمی‌شود، اما ممکن است در آینده انجام شود.

##### `depsBuildTarget` {#var-stdenv-depsBuildTarget}

فهرستی از وابستگی‌ها که پلتفرم میزبان آن‌ها پلتفرم ساخت derivation جدید، و پلتفرم هدف آن‌ها پلتفرم هدف derivation جدید است. این‌ها برنامه‌هایی هستند که در زمان ساخت استفاده می‌شوند

این‌ها اغلب برنامه‌ها و کتابخانه‌هایی هستند که توسط derivation جدید در *زمان اجرا* استفاده می‌شوند، اما همیشه این‌طور نیست. به عنوان مثال، کد ماشین موجود در یک کتابخانه با پیوند ایستا (statically-linked) تنها در زمان اجرا استفاده می‌شود، اما derivation حاوی کتابخانه تنها در زمان ساخت مورد نیاز است. حتی در حالت پویا (dynamic) نیز ممکن است برای راضی کردن لینک‌کننده (linker)، به کتاب

ی خود تابع، به‌همراه هرگونه بازنشانیِ اعمال‌شده، هنگامی که تابع توسط هر فراخوانی `overrideAttrs` مجدداً فراخوانی می‌شود. برای مثال:

Let's double-check glossary and terminology:
- attributes -> صفات (attribute -> صفت (attribute))
- build -> ساخت (Build)
- builder -> سازنده (Builder

```nix
mkDerivation (finalAttrs: {
  pname = "hello";
  withFeature = true;
  configureFlags = lib.optionals finalAttrs.withFeature [ "--with-feature" ];
})
```

توجه داشته باشید که این بخش از کلیدواژهٔ `rec` برای استفادهٔ مجدد از `withFeature` در `configureFlags` استفاده نمی‌کند.
کلیدواژهٔ `rec` در سطح نحو عمل می‌کند و از بازنشانی (overriding) مطلع نیست.

در عوض

```nix
# `pkg` is the _original_ definition (for illustration purposes)
let
  pkg = mkDerivation (finalAttrs: {
    # ...

    # An example attribute
    packages = [ ];

    # `passthru.tests` is a commonly defined attribute.
    passthru.tests.simple = f finalAttrs.finalPackage;

    # An example of an attribute containing a function
    passthru.appendPackages =
      packages':
      finalAttrs.finalPackage.overrideAttrs (newSelf: super: { packages = super.packages ++ packages'; });

    # For illustration purposes; referenced as
    # `(pkg.overrideAttrs(x)).finalAttrs` etc in the text below.
    passthru.finalAttrs = finalAttrs;
    passthru.original = pkg;
  });
in
pkg
```

}

Translation 18:
##### `preConfigurePhases` {#var-stdenv-preConfigurePhases}

Text 19:
Additional phases executed just before the configure phase.

Translation 19:
فازهای اضافی که درست قبل از فاز پیکربندی اجرا می‌شوند.

Let's double-check all translations and glossary matching:
- `derivation` -> derivation / اشتقاق ساخت (or derivation in technical context

##### `preBuildPhases` {#var-stdenv-preBuildPhases}

فازهای اضافی که درست پیش از فاز ساخت اجرا می‌شوند.

##### `preInstallPhases` {#var-stdenv-preInstallPhases}

فازهای اضافی که درست پیش از فاز نصب اجرا می‌شوند.

##### `preFixupPhases` {#var-stdenv-preFixupPhases}

ف

در خط فرمان به `./configure` پاس داده می‌شود. با قرار دادن `dontAddPrefix` روی `true` این قابلیت را غیرفعال کنید.

##### `prefix` {#var-stdenv-prefix}

The prefix under which the package must be installed, passed via the `--prefix` option to the configure script. It defaults to `$out`.

فارسی:
پیشوندی که بسته باید تحت آن نصب شود و از طریق گزینه `--prefix` به اسکری

##### `prefixKey` {#var-stdenv-prefixKey}

کلیدی که هنگام مشخص کردن [`prefix`](#var-stdenv-prefix) نصب استفاده می‌شود. به طور پیش‌فرض، این مقدار روی `--prefix=` تنظیم شده‌است زیرا توسط اکثریت بسته‌ها استفاده می‌شود. بسته‌های دیگر ممکن است به `--prefix ` (همراه با یک فاصله در انتها) یا `PREFIX=` نیاز داشته باشند

```nix
{ makeFlags = [ "PREFIX=$(out)" ]; }
```

::: {.note}
پرچم‌ها در Bash درون گیومه قرار می‌گیرند، اما متغیرهای محیطی را می‌توان با استفاده از نحو make مشخص کرد.
:::

##### `makeFlagsArray` {#var-stdenv-makeFlagsArray}

یک آرایه شل شامل آرگومان‌های اضافی ارسال‌شده به `make`. اگر آرگومان‌ها حاوی فاصله باشند، باید به جای `makeFlags` از این استفاده کنید، برای مثال:

```nix
{
  preBuild = ''
    makeFlagsArray+=(CFLAGS="-O0 -g" LDFLAGS="-lfoo -lbar")
  '';
}
```

توجه داشته باشید که آرایه‌های شل را نمی‌توان از طریق متغیرهای محیطی منتقل کرد، بنابراین نمی‌توانید `makeFlagsArray` را در صفت (attribute) یک derivation / اشتقاق ساخت تنظیم کنید (زیرا آن‌ها از طریق متغیرهای محیطی منتقل می‌شوند): باید آن‌ها را در کد شل تعریف کنید.

##### `buildFlags` / `buildFlagsArray` {#var-stdenv-buildFlags}

فهرستی از رشته‌ها که به‌عنوان پرچم‌های اضافی به `make` منتقل می‌شوند. مانند `makeFlags` و `makeFlagsArray` است، اما فقط در فاز ساخت استفاده می‌شود. هرگونه تارگت ساخت باید به‌عنوان بخشی از `buildFlags` مشخص شود.

##### `preBuild` {#var-stdenv-preBuild}

قلابی که در ابتدای فاز ساخت اجرا می‌شود.

##### `postBuild` {#var-stdenv-postBuild}

```nix
{ doCheck = true; }
```

در درایویشن (derivation) برای فعال‌سازی بررسی‌ها. استثنا کامپایل متقاطع است. ساخت‌های کامپایل متقاطع‌شده هرگز تست‌ها را اجرا نمی‌کنند، صرف‌نظر از این‌که `doCheck` چگونه تنظیم شده باشد، زیرا برنامهٔ تازه‌ساخته‌شده روی پلتفرمی که

```nix
{ installTargets = "install-bin install-doc"; }
```

##### `stripAllFlags` {#var-stdenv-stripAllFlags}

Line 26:
Flags passed to the `strip` command applied to the files in the directories listed in `stripAllList`. Defaults to `-s -p` (i.e. `--strip-all --preserve-dates`).

Persian:
پرچم‌های پاس‌داده‌شده به دستور `strip` که روی فایل‌های موجود در پوشه‌های ذکرشده در `stripAllList` اعمال

##### `stripExclude` {#var-stdenv-stripExclude}

فهرستی از نام‌های فایل یا الگوهای مسیر برای جلوگیری از strip شدن. یک

```nix
stdenv.mkDerivation {
  # ...
  stripExclude = [ "*.rlib" ];
}
```

این مثال از strip شدن فایل‌های موجود در برخی مسیرها جلوگیری می‌کند:

```nix
stdenv.mkDerivation {
  # ...
  stripExclude = [ "lib/modules/*/build/*" ];
}
```

/ پیش‌فرض
- `output` -> خروجی

Check heading levels and attributes:
##### `dontPatchELF` {#var-stdenv-dontPatchELF}
##### `dontPatchShebangs` {#var-stdenv-dontPatchShebangs}
##### `dontPruneLibtool

```nix
{
  pkgs ? import <nixpkgs> {
    config = { };
    overlays = [
      (final: prev: {
        ncurses = prev.ncurses.overrideAttrs { separateDebugInfo = true; };
        readline = prev.readline.overrideAttrs { separateDebugInfo = true; };
      })
    ];
  },
}:
pkgs.mkShell {
  NIX_DEBUG_INFO_DIRS = pkgs.lib.makeSearchPathOutput "debug" "lib/debug" [
    pkgs.glibc
    pkgs.ncurses
    pkgs.openssl
    pkgs.readline
  ];

  packages = [
    pkgs.gdb
    pkgs.socat
  ];

  shellHook = ''
    gdb socat
  '';
}
```

**`environment variable`** -> متغیر محیطی (applied)
- **`shell`** -> شل (Shell) (applied)
- **`Nixpkgs`** -> Nixpkgs (applied)
- **`search path`** -> مسیر جستجو (

```nix
{ doInstallCheck = true; }
```

در derivation / اشتقاق ساخت برای فعال‌سازی بررسی‌های نصب. استثنا در این میان کامپایل متقاطع است. ساخت‌های کامپایل متقاطع‌شده صرف‌نظر از نحوه تنظیم `doInstallCheck` هرگز تست‌ها را اجرا نمی‌کنند، زیرا برنامهٔ تازه‌ساخته‌شده روی پلتفرمی که برای ساخت آن استفاده شده‌است، اجرا نخواهد شد.

##### `installCheck

```bash
# adds `FOOBAR=baz` to `$out/bin/foo`’s environment
makeWrapper $out/bin/foo $wrapperfile --set FOOBAR baz

# Prefixes the binary paths of `hello` and `git`
# and suffixes the binary path of `xdg-utils`.
# Be advised that paths often should be patched in directly
# (via string replacements or in `configurePhase`).
makeWrapper $out/bin/foo $wrapperfile \
  --prefix PATH : ${lib.makeBinPath [ hello git ]} \
  --suffix PATH : ${lib.makeBinPath [ xdg-utils ]}
```

بسته‌ها ممکن است انتظار داشته باشند یا نیاز داشته باشند که ابزارهای دیگری در زمان اجرا در دسترس باشند.
می‌توان از `makeWrapper` برای افزودن بسته‌ها به یک متغیر محیطی `PATH` محلی برای یک wrapper استفاده کرد.

از `--prefix` برای تنظیم صریح وابستگی‌ها در `PATH` استفاده کنید.

::: {.note
```nix
{
  postInstall = ''
    find "$out" -type f -exec remove-references-to -t ${stdenv.cc} '{}' +
  '';
}
```

### `runHook` \<hook\> {#fun-runHook}

اجرای \<hook\> و مقادیر موجود در آرایهٔ مرتبط با آن. نام آرایه با حذف عبارت `Hook` از انتهای \<hook\> و افزودن `Hooks` تعیین می‌شود.

برای مثال، `runHook postHook` قلاب `postHook` و تمام مقادیر موجود در آرایهٔ `postHooks` (در صورت وجود) را اجرا می‌کند.

### `substitute` \<infile\> \<outfile\> \<subs\> {#fun-substitute}

جایگزینی رشته‌ای را روی محتوای \<infile\> انجام داده و نتیجه را در \<outfile\> می‌نویسد. جایگزینی‌ها در \<subs\> به شکل زیر هستند:

#### `--replace-fail` \<s1\> \<s2\> {#fun-substitute-replace-fail}

جایگزینی هر بار وقوع رشتهٔ \<s1\> با \<s2\>.
در صورتی که هیچ تغییری ایجاد نشود، خطا خواهد داد.

#### `--replace-warn` \<s1\> \<s2\> {#fun-substitute-replace-warn}

جایگزینی هر بار وقوع رشتهٔ \<s1\> با \<s2\>.
در صورتی که هیچ تغ

```shell
substitute ./foo.in ./foo.out \
    --replace-fail /usr/bin/bar $bar/bin/bar \
    --replace-fail "a string containing spaces" "some other text" \
    --subst-var someVar
```

### `substituteInPlace` \<multiple files\> \<subs\> {#fun-substituteInPlace}

مانند `substitute` است، اما جایگزینی‌ها را به

```bash
#! @bash@/bin/sh
PATH=@coreutils@/bin
echo @foo@
```

و محیط شامل `bash=/nix/store/bmwp0q28cf21...-bash-3.2-p39` و `coreutils=/nix/store/68afga4khv0w...-coreutils-6.12` باشد، اما شامل متغیر `foo` نباشد، آن‌گاه خروجی برابر خواهد بود با

```bash
#! /nix/store/bmwp0q28cf21...-bash-3.2-p39/bin/sh
PATH=/nix/store/68afga4khv0w...-coreutils-6.12/bin
echo @foo@
```

به این معنی که هیچ جایگزینی برای متغیرهای تعریف‌نشده انجام نمی‌شود.

متغیرهای محیطی که با حرف بزرگ یا خط زیرین (underscore) شروع می‌شوند فیلتر می‌شوند تا از جای

```bash
# prints coreutils-8.24
stripHash "/nix/store/9s9r019176g7cvn2nvcw41gsp862y6b4-coreutils-8.24"
```

اگر می‌خواهید نتیجه را در متغیر دیگری ذخیره کنید، الگوی زیر ممکن است مفید باشد:

```bash
name="/nix/store/9s9r019176g7cvn2nvcw41gsp862y6b4-coreutils-8.24"
someVar=$(stripHash $name)
```

### `wrapProgram` \<executable\> \<makeWrapperArgs\> {#fun-wrapProgram}

یک تابع کاربردی برای `makeWrapper` که `<executable>` را با یک واسط (wrapper) که برنامه اصلی را اجرا می‌کند، جایگزین می‌کند. این تابع تمام آرگومان‌های مشابه `makeWrapper` را می‌پذیرد، به جز `--inherit-argv0` (که در پیاده‌سازی `makeBinaryWrapper` استفاده می‌شود) و `--argv0` (که توسط پیاده‌سازی‌های wrapper در هر دو `makeWrapper` و `makeBinaryWrapper` استفاده می‌شود).

اگر آن را چند بار اعمال کنید، فایل wrapper بازنویسی می‌شود و در نهایت با پوشش‌دهی دوگانه (double wrapping) مواجه خواهید شد که باید از آن اجتناب کرد.

### `prepend

```shellSession
$ configureFlags="--disable-static"
$ prependToVar configureFlags --disable-dependency-tracking --enable-foo
$ echo $configureFlags
--disable-dependency-tracking --enable-foo --disable-static
```

### `appendToVar` \<variableName\> \<elements...\> {#fun-appendToVar}

افزودن عناصر به یک متغیر.

مثال:

```shellSession
$ configureFlags="--disable-static"
$ appendToVar configureFlags --disable-dependency-tracking --enable-foo
$ echo $configureFlags
--disable-static --disable-dependency-tracking --enable-foo
```

جانبی)
    - Code elements in backticks preserved (`envBuildBuildHooks`, `n`, `n + 1`, `hostOffset`, `targetOffset`).
    - Anchors and markdowns intact (`## Package setup hooks {#ssec-setup-hooks}`, `*relative*`, `[by convention...]`).

    Let's refine paragraph 3:
    "به عنوان مثال، اگر یک مسیر derivation بیش از یک بار ذکر

```bash
addEnvHooks "$hostOffset" myBashFunction
```

*وجود* قلاب‌های آماده‌سازی (setup hooks) مدت‌هاست که مستند شده‌است و بسته‌های درون Nixpkgs مختارند از این مکانیزم استفاده کنند. با این حال، سایر بسته‌ها نباید به تغییر نکردن این مکانیزم‌ها بین نسخه‌های Nixpkgs اتکا کنند. به دلیل مشکلات موجود در این سیستم، الزام به پایدار بودن آن برای هر بازه زمانی فایده چندانی ندارد.

ابتدا، به بررسی برخی از قلاب‌های آماده‌سازی می‌پردازیم که بخشی از `stdenv` پیش‌فرض Nixpkgs هستند. این بدان معناست که آن‌ها برای هر بسته‌ای که با استفاده از `stdenv.mkDerivation` ساخته می‌شود اجرا می‌شوند، حتی با سازنده‌های (builders) سفارشی. برخی از آن‌ها مختص پلتفرم خاصی هستند، بنابراین ممکن است روی لینوکس اجرا شوند اما روی Darwin اجرا نشوند یا برعکس.

### `move-docs.sh` {#move-docs.sh}

این قلاب آماده‌سازی، هرگونه مستندات نصب‌شده را به زیرپوشه `/share` منتقل می‌کند. این موارد شامل پوشه‌های man، doc و info می‌شود. این امر برای برنامه‌های قدیمی که نحوه استفاده از زیرپوشه `share` را نمی‌دانند

```
patchShebangs [--build | --host] PATH...
```

##### پرچم‌ها {#patch-shebangs.sh-invocation-flags}

`--build`
: جستجوی دستورات موجود در زمان ساخت

`--host`
: جستجوی دستورات موجود در زمان اجرا

##### مثال‌ها {#patch-shebangs.sh-invocation-examples}

```sh
patchShebangs --host /nix/store/<hash>-hello-1.0/bin
```

```sh
patchShebangs --build configure
```

`#!/bin/sh` به `#!/nix/store/<hash>-some-bash/bin/sh` بازنویسی خواهد شد.

`#!/usr/bin/env` رفتار

```nix
stdenv.mkDerivation {
  # ...
  dontPatchShebangs = true;
  # ...
}
```

، آن را به متغیر محیطی `PATH` اضافه می‌کند. این امر تضمین می‌کند که برنامه‌های قابل اجرا که در `$out/bin` قرار دارند قابل دسترسی باشند.

Let's double-check glossary terms:
- build-time -> زمان ساخت
- build phase -> فازهای ساخت (in "one of the build phases" -> "یکی از فازهای ساخت")
- Nix store -> انبار نیکس (Nix store)

این قلاب به‌ویژه در طول آزمایش بسیار مفید است، زیرا به بسته‌ها اجازه می‌دهد تا فایل‌های اجرایی خود را بدون نیاز به تغییرات دستی در `PATH` پیدا کنند.

**نکته**: این قلاب به‌طور ویژه تنها برای پوشه `$out/bin` طراحی شده‌است و از مسیرهای دیگر مانند `$sourceRoot/bin` پشتیبانی نمی‌کند و آن‌ها را مدیریت ن

یک وظیفهٔ نهایی قلاب آماده‌سازی، تعریف تعدادی متغیر محیطی استاندارد است تا به سیستم‌های ساخت بگوید کدام فایل‌های اجرایی چه هدفی را برآورده می‌کنند. آن‌ها به‌گونه‌ای تعریف شده‌اند که فقط نام پایهٔ ابزارها باشند، با این فرض که باینری‌های Bintools Wrapper در مسیر قرار خواهند داشت. اولاً، این امر به بسته‌های بد نوشته‌شده

اگر فایل `${cc}/nix-support/cc-wrapper-hook` وجود داشته باشد، در انتهای [ورپر کامپایلر](#cc-wrapper) اجرا خواهد شد.
اگر فایل `${binutils}/nix-support/ld-wrapper-hook` وجود داشته باشد، در انتهای ورپر لینکر و پیش از اجرای لینکر اجرا می‌شود.
اگر فایل `${binutils}/nix-

```
/tmp/nix-build-zynaddsubfx-2.5.2.drv-0/zynaddsubfx-2.5.2/src/UI/guimain.cpp:571:28: error: format not a string literal and no format arguments [-Werror=format-security]
         printf(help_message);
                            ^
cc1plus: some warnings being treated as errors
```

#### `stackprotector` {#stackprotector}

گزینه‌های کامپایلر `-fstack-protector-strong --param ssp-buffer-size=4` را اضافه می‌کند. این کار بررسی‌های ایمنی را در برابر بازنویسی‌های پشته اضافه کرده و بسیاری از حملات احتمالی تزریق کد را به وضعیت‌های متوقف‌کننده (abort) تبدیل می‌کند. در بهترین حالت، این کار آسیب‌پذیری‌های تزریق کد را به محروم‌سازی از سرویس یا مواردی بی‌اهمیت تبدیل می‌کند (بسته به برنامه).

این گزینه باید برای خطاهایی مشابه موارد زیر خاموش یا برطرف شود:

```
bin/blib.a(bios_console.o): In function `bios_handle_cup':
/tmp/nix-build-ipxe-20141124-5cbdc41.drv-0/ipxe-5cbdc41/src/arch/i386/firmware/pcbios/bios_console.c:86: undefined reference to `__stack_chk_fail'
```

#### `fortify` {#fortify}

گزینه‌های کامپایلر `-O2 -D_FORTIFY_SOURCE=2` را اضافه می‌کند. در طول تولید کد، کامپایلر اطلاعات زیادی دربارهٔ اندازه‌های بافر (در صورت امکان) می‌داند و تلاش می‌کند فراخوانی‌های ناامن توابع بافر با طول نامحدود

```
malloc.c:404:15: error: return type is an incomplete type
malloc.c:410:19: error: storage size of 'ms' isn't known

strdup.h:22:1: error: expected identifier or '(' before '__extension__'

strsep.c:65:23: error: register name not specified for 'delim'

installwatch.c:3751:5: error: conflicting types for '__open_2'

fcntl2.h:50:4: error: call to '__open_missing_mode' declared with attribute error: open with O_CREAT or O_TMPFILE in second argument needs 3 arguments
```

غیرفعال‌سازی `fortify` مستلزم غیرفعال‌سازی `fortify3` نیز هست.

#### `fortify3` {#fortify3}

گزینه‌های کامپایلر `-O2 -D_FORT

```
ccbLfRgg.s: Assembler messages:
ccbLfRgg.s:33: Error: missing or invalid displacement expression `private_key_len@GOTOFF'
```

#### `strictoverflow` {#strictoverflow}

سرریز عدد صحیح علامت‌دار طبق استاندارد C، یک رفتار تعریف‌نشده‌است. اگر این اتفاق بیفتد، خطایی در برنامه محسوب می‌شود، چرا که برنامه باید پیش از وقوع سرریز آن را بررسی کند

```
intel_drv.so: undefined symbol: vgaHWFreeHWRec
```

#### `zerocallusedregs` {#zerocallusedregs}

گزینه کامپایلر `-fzero-call-used-regs=used-gpr` را اضافه می‌کند. این باعث می‌شود ثبات‌های با منظور عمومی (general-purpose registers) که قرارداد فراخوانی (calling convention) یک معماری آن‌ها را "call-used" می‌داند، هنگام بازگشت از تابع صفر شوند. این کار ساخت گجت‌های کاربردی

glossary: dependencies -> وابستگی‌ها)
- package -> بسته (matches)
- packages dependencies -> وابستگی‌های یک بسته (matches)
- system -> سیستم (matches)
- state -> وضعیت (matches)
- crash -> کرش (matches)
- build -> ساخت (matches)
- build errors -> خطاهای ساخت (

```
sorry, unimplemented: __builtin_clear_padding not supported for variable length aggregates
```

#### `glibcxxassertions` {#glibcxxassertions}

پرچم کامپایلر `-D_GLIBCXX_ASSERTIONS` را اضافه می‌کند. این پرچم تنها روی هدف‌های libstdc++ تأثیر دارد و هنگام تعریف شدن، بررسی‌های خطای اضافی را در قالب ادعاهای پیش‌شرط (precondition assertions) فعال می‌سازد؛ مانند بررسی محدوده (bounds checking) در رشته‌های C++ و بررسی اشاره‌گر تهی هنگام رازگشایی (dereferencing

-per-platform-wrapper]: هر ورپر (wrapper) یک پلتفرم منفرد را هدف قرار می‌دهد، بنابراین اگر باینری‌ها برای چند پلتفرم مورد نیاز باشند، باینری‌های زیرین باید چندین بار پوشش داده (wrap) شوند. از آنجا که این ویژگیِ خود ورپر است
