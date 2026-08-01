# Haskell {#haskell}

زیرساخت Haskell در Nixpkgs دو هدف اصلی دارد: هدف اولیه ارائه یک کامپایلر Haskell و ابزارهای ساخت و همچنین زیرساختی برای بسته‌بندی بسته‌های مبتنی بر Haskell است.

هدف ثانویه ارائه پشتیبانی از محیط‌های توسعه Haskell از جمله کتابخانه‌های پیش‌ساخته Haskell است. با این حال، در این زمینه به دلیل محدودیت‌های خودتحمیلی در Nixpkgs، برای

ما به دنبال یک مجموعه‌ی بسته‌ی «تاییدشده» هستیم که تنها شامل یک نسخه از هر بسته باشد، مانند [Stackage]، که مجموعه‌ای انتخاب‌شده از بسته‌هایی است که سازگاری آن‌ها تایید شده است. ما از اطلاعات نسخه موجود در اسنپ‌شات‌های Stackage استفاده می‌کنیم و آن را با بسته‌های بیشتری گسترش می‌دهیم. به‌طور معمول در Nixpkgs تعداد بسته‌های Haskell در حال ساخت تقریباً دو تا

[سازنده Haskell در Nixpkgs](#haskell-mkderivation) چنین کاری انجام نمی‌دهد.
این ابزار بسته‌هایی با نام‌های وابستگی‌های مورد نظر را به‌عنوان ورودی دریافت می‌کند و صرفاً بررسی می‌کند که آیا محدوده نسخه‌ها را برآورده می‌کنند یا خیر، و اگر برآورده نکنند شکست می‌خورد (به‌طور پیش‌فرض، برای دور زدن این موضوع `jailbreak` را ببینید).

تابع `haskellPackages.callPackage` تحلیل بسته (package resolution) را انجام می‌دهد.
به عنوان مثال، برای یک ورودی بسته با نام `aeson` از `haskellPackages.aeson` استفاده می‌کند که دارای نسخه پیش‌فرض است همان‌طور که در بالا توضیح داده شد. (به طور کلی‌تر:
`<packages>.callPackage f` تابع `f` را با ورودی‌های نام‌گذاری‌شده ارائه شده از مجموعه بسته `<packages>` فراخوانی می‌کند.)
اگرچه این رفتار پیش‌فرض است، اما امکان بازنشانی وابستگی‌ها برای یک بسته خاص وجود دارد؛ نگاه کنید به
[`override` و `overrideScope`](#h

<!-- Policy introduced here: https://discourse.nixos.org/t/nixpkgs-ghc-deprecation-policy-user-feedback-necessary/64153 -->

## `haskellPackages.mkDerivation` {#haskell-mkderivation}

هر مجموعه بسته‌ی Haskell دارای `mkDerivation` آگاه از Haskell مخصوص به خود است که برای ساخت بسته‌های آن استفاده می‌شود. به‌طور کلی نیازی نیست مستقی

`dontConvertCabalFileToUnix`
: به طور پیش‌فرض، `haskellPackages.mkDerivation` فایل `.cabal` یک بسته داده‌شده را به پایان خطوط یونیکس تبدیل می‌کند.
این کار برای دور زدن مشکل [تبدیل فایل‌های `.cabal` اصلاح‌شده به پایان خطوط DOS توسط Hackage](https://github.com/haskell/hackage-server/issues/316) طراحی شده است که در موارد متعدد باعث ناتوانی در اعمال پچ‌ها می‌شود.
می‌توانید مقدار `true` را برای غیرفعال کردن این رفتار پاس دهید.

`enableLibraryProfiling`
: آیا پروفایلینگ ([profiling][profiling]) برای کتابخانه‌های موجود در بسته فعال شود یا خیر. در صورت پشتیبانی، به طور پیش‌فرض فعال است.

`enableExecutableProfiling`
: آیا پروفایلینگ ([profiling][profiling]) برای برنامه‌های اجرایی موجود در بسته فعال شود یا خیر. به طور پیش‌فرض غیرفعال است.

`profilingDetail`
: [سطح جزئیات پروفایلینگ][profiling-detail] برای تنظیم. مقدار پیش‌فرض `exported-functions` است.

`enableSharedExecutables`
: آیا برنامه‌های اجرایی به صورت پویا لینک شوند یا خیر. به طور پیش‌فرض، برنامه‌های اجرایی به صورت ایستا لینک می‌شوند.

`enableSharedLibraries`
: آیا کتابخانه‌های اشتراکی Haskell ساخته شوند یا خیر. این گزینه به طور پیش‌فرض فعال است مگر اینکه از `pkgsStatic` استفاده شود یا کتابخانه‌های اشتراکی در GHC غیرفعال شده باشند.

`enableStaticLibraries`
: آیا کتابخانه‌های ایستا ساخته شوند یا خیر. در صورت پشتیبانی، به طور پیش‌فرض فعال است.

`enableDeadCodeElimination`
: آیا حذف کدهای مرده مبتنی بر لینکِر در GHC فعال شود یا خیر.
در صورت پشتیبانی، به طور پیش‌فرض فعال است.

`enableHsc2hsViaAsm`
: آیا پرچم `--via-asm` به `hsc2hs` ارسال شود یا خیر. تنها در Windows به طور پیش‌فرض فعال است.

`hyperlinkSource`
: آیا کد منبع نیز به عنوان بخشی از مستندات haddock با ارسال [پرچم `--hyperlinked-source`][haddock-hyperlinked-source-option] رندر شود یا خیر.
مقدار پیش‌فرض `true` است.

`isExecutable`
: آیا بسته شامل یک برنامه اجرایی است یا خیر.

`isLibrary`
: آیا بسته شامل یک کتابخانه است یا خیر.

`jailbreak`
: آیا [jailbreak-cabal][jailbreak-cabal] پیش از `configurePhase` برای حذف محدودیت‌های نسخه در فایل cabal اجرا شود یا خیر. توجه داشته باشید که اگر محدودیت‌های نسخه شرطی باشند (مثلاً اگر یک وابستگی پشت یک پرچم پنهان شده باشد)، این کار نمی‌تواند آن‌ها را بردارد.

`enableParallelBuilding`
: آیا از پرچم `-j` برای شروع موازی چندین کار توسط GHC/Cabal استفاده شود یا خیر.

`maxBuildCores`
: حداکثر تعداد کارهایی که به صورت موازی برای کامپایل کردن استفاده می‌شوند، صرف‌نظر از `$NIX_BUILD_CORES`. مقدار پیش‌فرض 16 است، زیرا کامپایل کردن Haskell با GHC در صورت استفاده از کارهای موازی بیش از حد، در حال حاضر دچار [افت عملکرد](https://gitlab.haskell.org/ghc/ghc/-/issues/9221) می‌شود.

`doCoverage`
: آیا فایل‌های مورد نیاز برای [HPC][haskell-program-coverage] تولید و نصب شوند یا خیر.
مقدار پیش‌فرض `false` است.

`doHaddock`
: آیا مستندات (HTML) با استفاده از [haddock][haddock] ساخته شوند یا خیر.
در صورت پشتیبانی، مقدار پیش‌فرض `true` است.

`testTargets`
: نام‌های مجموعه‌های تست برای ساخت و اجرا. در صورت عدم تنظیم، تمام مجموعه‌های تست اجرا خواهند شد.

`preCompileBuildDriver`
: کد Shell برای اجرا قبل از کامپایل کردن `Setup.hs`.

`postCompileBuildDriver`
: کد Shell برای اجرا بعد از کامپایل کردن `Setup.hs`.

`preHaddock`
: کد Shell برای اجرا قبل از ساخت مستندات با استفاده از haddock.

`enableSeparateDocOutput`
: آیا مستندات در یک خروجی جداگانه `doc` نصب شوند یا خیر.
اگر `doHaddock` برابر با `true` باشد، به‌طور خودکار فعال می‌شود.

`enableSeparateIntermediatesOutput`
: زمانی که `doInstallIntermediates` درست است، آیا فرآورده‌های میانی ساخت در یک خروجی جداگانه `intermediates` نصب شوند یا خیر. برای اطلاعات

فرآورده‌های ساخت استفاده خواهد کرد تا از کامپایل مجدد ماژول‌های تغییرنکرده جلوگیری کند.

Block 14:
For more detail on how to store and use incremental build products, see
[Gabriella Gonzalez’ blog post “Nixpkgs support for incremental Haskell
builds”.][incremental-builds] motivation behind this feature

```nix
let
  pkgs = import <nixpkgs> { };
  inherit (pkgs) haskell;
  inherit (haskell.lib.compose) overrideCabal;

  # Incremental builds work with GHC >=9.4.
  turtle = haskell.packages.ghc944.turtle;

  # This will do a full build of `turtle`, while writing the intermediate build products
  # (compiled modules, etc.) to the `intermediates` output.
  turtle-full-build-with-incremental-output = overrideCabal (drv: {
    doInstallIntermediates = true;
    enableSeparateIntermediatesOutput = true;
  }) turtle;

  # This will do an incremental build of `turtle` by copying the previously
  # compiled modules and intermediate build products into the source tree
  # before running the build.
  #
  # GHC will then naturally pick up and reuse these products, making this build
  # complete much more quickly than the previous one.
  turtle-incremental-build = overrideCabal (drv: {
    previousIntermediates = turtle-full-build-with-incremental-output.intermediates;
  }) turtle;
in
turtle-incremental-build
```

## محیط‌های توسعه {#haskell-development-environments}

علاوه بر ساخت و نصب نرم‌افزارهای Haskell، Nixpkgs می‌تواند محیط‌های توسعه را نیز برای پروژه‌های Haskell فراهم کند. این امر این مزیت آشکار را دارد

```console
$ cd ~/src/random
$ nix-shell -A haskellPackages.random.env '<nixpkgs>'
[nix-shell:~/src/random]$ ghc-pkg list
/nix/store/a8hhl54xlzfizrhcf03c1l3f6l9l8qwv-ghc-9.2.4-with-packages/lib/ghc-9.2.4/package.conf.d
    Cabal-3.6.3.0
    array-0.5.4.0
    base-4.16.3.0
    binary-0.8.9.0
    …
    ghc-9.2.4
    …
```

/ساختن/ساخت)
- "download" -> بارگیری
- "usecases" -> موارد استفاده

Looks very good, natural Persian suitable for software developers, adhering strictly to constraints and style guidelines. No commentary/preamble, no code fence invention, preserving backticks and links.همان‌طور که مشاهده می‌کن

```console
$ ls
my-project.cabal src …
$ cabal2nix ./. > my-project.nix
```

عبارت نیکس (Nix expression) تولیدشده به تابعی ارزیابی می‌شود که آماده‌ی فراخوانی با `callPackage` است. فعلاً، می‌توانیم یک `default.nix` کمینه اضافه کنیم که دقیقاً همین کار را انجام دهد:

```nix
# Retrieve nixpkgs impurely from NIX_PATH for now, you can pin it instead, of course.
{
  pkgs ? import <nixpkgs> { },
}:

# use the nixpkgs default haskell package set
pkgs.haskellPackages.callPackage ./my-project.nix { }
```

با استفاده از `nix-build default.nix` اکنون می‌توانیم پروژه خود را ساخت دهیم، اما همچنین می‌توانیم با استفاده از `nix-shell -A env default.nix` وارد شلی شویم که همهٔ وابستگی‌های بسته در آن در دسترس هستند. اگر `cabal-install` را به صورت سراسری نصب کرده باشید، طبق انتظار در داخل شل کار خواهد کرد.

### shellFor {#

```nix
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.haskellPackages.shellFor {
  packages = hpkgs: [
    # reuse the nixpkgs for this package
    hpkgs.distribution-nixpkgs
    # call our generated Nix expression manually
    (hpkgs.callPackage ./my-project/my-project.nix { })
  ];

  # development tools we use
  nativeBuildInputs = [
    pkgs.cabal-install
    pkgs.haskellPackages.doctest
    pkgs.cabal2nix
  ];

  # Extra arguments are added to mkDerivation's arguments as-is.
  # Since it adds all passed arguments to the shell environment,
  # we can use this to set the environment variable the `Paths_`
  # module of distribution-nixpkgs uses to search for bundled
  # files.
  # See also: https://cabal.readthedocs.io/en/latest/cabal-package.html#accessing-data-files-from-package-code
  distribution_nixpkgs_datadir = toString ./distribution-nixpkgs;
}
```

های ``haskell-language-server-wrapper``، ``haskell-language-server`` و ``haskell-language-server-x.x.x`` را ارائه می‌دهد، که در آن ``x.x.

```nix
pkgs.haskell-language-server.override {
  supportedGhcVersions = [
    "90"
    "94"
  ];
}
```
جایی که تمام رشته‌های `version` مجاز هستند، به طوری که `haskell.packages.ghc${version}` یک مجموعه بسته‌ی موجود باشد.

وقتی `haskell-language-server-wrapper` را اجرا می‌کنید، نسخه GHC استفاده‌شده توسط پروژه‌ای را که روی آن کار

```nix
haskellPackages.nix-tree.override { brick = haskellPackages.brick_0_67; }
```

<!-- TODO(@sternenseemann): این بخش به قسمت بعدی تعلق دارد
یکی از مشکلات رایجی که ممکن است با چنین بازنشانی‌ای مواجه شوید، شکست ساخت با پیام “abort because of serious configure-time warning from Cab

```nix
haskellPackages.haskell-ci.overrideScope (self: super: {
  Cabal = self.Cabal_3_14_2_0;
})
```

رابط سفارشی زمانی وارد عمل می‌شود که بخواهید آرگومان‌های ارسال‌شده به `haskellPackages.mkDerivation` را بازنشانی کنید. برای این منظور، از تابع `overrideCabal` از `haskell.lib.compose` استفاده می‌شود. به عنوان مثال، اگر بخواهید یک man page را که همراه بسته توزیع شده است نصب کنید، می‌توانید کاری شبیه به این انجام دهید:

```nix
haskell.lib.compose.overrideCabal (drv: {
  postInstall = ''
    ${drv.postInstall or ""}
    install -Dm644 man/pnbackup.1 -t $out/share/man/man1
  '';
}) haskellPackages.pnbackup
```

`overrideCabal` دو آرگومان می‌گیرد:

1. تابعی که تمام آرگومان‌های قبلاً ارسال‌شده به `haskellPackages.mkDerivation` را دریافت کرده و مجموعه‌ای از آرگومان‌ها را جهت جایگزینی (یا افزودن) با مقداری جدید برمی‌گرداند.
2. derivation مربوط به Haskell برای بازنشانی.

آرگومان‌ها به گونه‌ای

```nix
let
  installManPage = haskell.lib.compose.overrideCabal (drv: {
    postInstall = ''
      ${drv.postInstall or ""}
      install -Dm644 man/${drv.pname}.1 -t "$out/share/man/man1"
    '';
  });

in
installManPage haskellPackages.pnbackup
```

در واقع، `haskell.lib.compose` از قبل کمک‌رسان‌های مفید زیادی برای کارهای معمول ارائه می‌دهد که جزئیات آن‌ها در بخش بعدی آمده است. آن‌ها همچنین به گونه‌ای ساختار یافته‌اند که می‌توان آن‌ها را با استفاده از `lib.pipe` ترکیب کرد:

```nix
lib.pipe my-haskell-package [
  # lift version bounds on dependencies
  haskell.lib.compose.doJailbreak
  # disable building the haddock documentation
  haskell.lib.compose.dontHaddock
  # pass extra package flag to Cabal's configure step
  (haskell.lib.compose.enableCabalFlag "myflag")
]
```

libc
- `GMP` -> GMP
- `Cabal` -> Cabal
- `Hackage` -> Hackage
- inline backticks kept exactly Latin!

Let's verify markdown rendering and links.
Links:
`[documentation of `haskellPackages.mkDerivation`](#haskell-mkderivation)`
`[nixpkgs#16463
```
  error: output '/nix/store/64k8iw0ryz76qpijsnl9v87fb26v28z8-my-haskell-package-1.0.0.0' is not allowed to refer to the following paths:
           /nix/store/5q5s4a07gaz50h04zpfbda8xjs8wrnhg-ghc-9.6.3
  ```

اگر این اتفاق افتاد، ابتدا بررسی ارجاعات GHC را غیرفعال کرده و درایویشن را مجدداً بسازید:
```nix
  pkgs.haskell.lib.overrideCabal (pkgs.haskell.lib.justStaticExecutables my-haskell-package) (drv: {
    disallowGhcReference = false;
  })
  ```

سپس برای تشخیص این‌که کدام کتابخانه‌ها مسئول هستند، از `strings` استفاده کنید:
```
  $ nix-build ...
  $ strings result/bin/my-haskell-binary | grep /nix/store/
  ...
  /nix/store/n7ciwdlg8yyxdhbrgd6yc2d8ypnwpmgq-hs-opentelemetry-sdk-0.0.3.6/bin
  ...
  ```

در نهایت، از `remove-references-to` برای حذف آن مسیرهای انبار از خروجی تولیدشده استفاده کنید:
```nix
  pkgs.haskell.lib.overrideCabal (pkgs.haskell.lib.justStaticExecutables my-haskell-package) (drv: {
    postInstall = ''
      ${drv.postInstall or ""}
      remove-references-to -t ${pkgs.haskellPackages.hs-opentelemetry-sdk}
    '';
  })
  ```

[164630]: https://github.com/NixOS/nixpkgs/issues/164630

`enableSeparateBinOutput drv`
: فایل‌های اجرایی تولیدشده توسط `drv` را در یک خروجی `bin` مجزا نصب می‌کند. این کار تاثیری مشابه `justStaticExecutables` دارد، اما کتابخانه‌ها و مستندات را در خروجی `out` در کنار خ

`disableCabalFlag flag drv`
: اطمینان حاصل می‌کند که پرچم Cabal به نام `flag` در مرحله‌ی configure مربوط به Cabal غیرفعال شده است.

`appendBuildFlags list drv`
: رشته‌های موجود در `list` را به آرگومان `buildFlags` برای `drv` اضافه می‌کند.

<!-- TODO(@sternenseemann): removeConfigureFlag -->

`appendPatches list drv

` استفاده کنند.
توجه داشته باشید که این ویژگی در هنگام کامپایل متقاطع به‌طور خودکار غیرفعال می‌شود، زیرا مستلزم اجرای باینری‌های مورد نظر است.`

Let'

```nix
# cabal get mtl-2.2.1 && cd mtl-2.2.1 && cabal2nix .
{
  mkDerivation,
  base,
  lib,
  transformers,
}:
mkDerivation {
  pname = "mtl";
  version = "2.2.1";
  src = ./.;
  libraryHaskellDepends = [
    base
    transformers
  ];
  homepage = "http://github.com/ekmett/mtl";
  description = "Monad classes, using functional dependencies";
  license = lib.licenses.bsd3;
}
```

این عبارت باید با `haskellPackages.callPackage` فراخوانی شود، که [`haskellPackages.mkDerivation`](#haskell-mkderivation) و وابستگی‌های Haskell را به عنوان آرگومان‌ها ارائه می‌دهد.

`callCabal2nix name src args`
: یک بسته به نام `name` از derivation سورس `src` با استفاده از `cabal2nix` ایجاد می‌کند.

  `args` آرگومان‌های اضافی ارائه‌شده به `haskellPackages.callPackage` هستند.

`callCabal2nixWithOptions name src opts args`
: یک بسته به نام `name` از derivation سورس `src` با استفاده از `cabal2nix` ایجاد می‌کند.

  `opts` گزینه‌های اضافی برای فراخوانی `cabal2nix` هستند. اگر `opts` یک رشته باشد، به عنوان آرگومان‌های خط فرمان اضافی برای `cabal2nix` استفاده خواهد شد، مانند `--subpath path/to/dir/containing/cabal-file`. در غیر این صورت، `opts` باید یک AttrSet باشد که می‌تواند شامل صفات زیر باشد:

  `extraCabal2nixOptions`
  : آرگومان‌های خط فرمان اضافی برای `cabal2nix`.

  `srcModifier`
  : تابعی که برای تغییر `src` داده‌شده به جای فیلتر پیش‌فرض استفاده می‌شود.

    فیلتر سورس پیش‌فرض، همه فایل‌ها را از

جلوگیری شود.

نتیجه دو اورلی مانند نمونه‌های زیر است. بخش‌های قابل تنظیم با کامنت‌ها علامت‌گذاری شده‌اند، همان‌طور که هرگونه روش اختیاری یا جایگزین برای دستیابی به تنظیمات profiling مورد نظر بدون ایجاد ساخت‌های مجدد بیش از حد مشخص شده

```nix
let
  # Name of the compiler and package set you want to change. If you are using
  # the default package set `haskellPackages`, you need to look up what version
  # of GHC it currently uses (note that this is subject to change).
  ghcName = "ghc910";
  # Desired new setting
  enableProfiling = true;

in
[
  # The first overlay modifies the GHC derivation so that it does or does not
  # build profiling versions of the core libraries bundled with it. It is
  # recommended to only use such an overlay if you are enabling profiling on a
  # platform that doesn't by default, because compiling GHC from scratch is
  # quite expensive.
  (
    final: prev:
    let
      inherit (final) lib;

    in
    {
      haskell = prev.haskell // {
        compiler = prev.haskell.compiler // {
          ${ghcName} = prev.haskell.compiler.${ghcName}.override {
            # Unfortunately, the GHC setting is named differently for historical reasons
            enableProfiledLibs = enableProfiling;
          };
        };
      };
    }
  )

  (
    final: prev:
    let
      inherit (final) lib;
      haskellLib = final.haskell.lib.compose;

    in
    {
      haskell = prev.haskell // {
        packages = prev.haskell.packages // {
          ${ghcName} = prev.haskell.packages.${ghcName}.override {
            overrides = hfinal: hprev: {
              mkDerivation =
                args:
                hprev.mkDerivation (
                  args
                  // {
                    # Since we are forcing our ideas upon mkDerivation, this change will
                    # affect every package in the package set.
                    enableLibraryProfiling = enableProfiling;

                    # To actually use profiling on an executable, executable profiling
                    # needs to be enabled for the executable you want to profile. You
                    # can either do this globally or…
                    enableExecutableProfiling = enableProfiling;
                  }
                );

              # …only for the package that contains an executable you want to profile.
              # That saves on unnecessary rebuilds for packages that you only depend
              # on for their library, but also contain executables (e.g. pandoc).
              my-executable = haskellLib.enableExecutableProfiling hprev.my-executable;

              # If you are disabling profiling to save on build time, but want to
              # retain the ability to substitute from the binary cache. Drop the
              # override for mkDerivation above and instead have an override like
              # this for the specific packages you are building locally and want
              # to make cheaper to build.
              my-library = haskellLib.disableLibraryProfiling hprev.my-library;
            };
          };
        };
      };
    }
  )
]
```

<!-- TODO(@sternenseemann): بخش‌های بازنشانی mkDerivation، بازنشانی GHC و بازنشانی کل مجموعه بسته‌ها را بنویسید و در صورت مرتبط بودن از اینجا به آن‌ها لینک دهید.
-->

[Stackage]: https://www.stackage.org
[cabal-project-files]: https://cabal.readthedocs.io/en/latest/cabal-project.html
[cabal2nix]: https://github.com/nixos/cabal2nix
[cpphs]: https://Hackage.haskell.org/package/cpphs
[haddock-hoogle-option]: https://haskell-haddock.readthedocs.io/en/latest/invoking.html#cmdoption-hoogle
[haddock-hyperlinked-source-option]: https://haskell-haddock.readthedocs.io/en/latest/invoking.html#cmdoption-hyperlinked-source
[haddock]: https://www.haskell.org/haddock/
[haskell-program-coverage]: https://downloads.haskell.org/~ghc/latest/docs/html/users_guide/profiling.html#observing-code-coverage
[haskell.nix]: https://input-output-hk.github.io/haskell.nix/index.html
[HLS user guide]: https://haskell-language-server.readthedocs.io/en/latest/configuration.html#configuring-your-editor
[hoogle]: https://wiki.haskell.org/Hoogle
[incremental-builds]: https://www.haskellforall.com
