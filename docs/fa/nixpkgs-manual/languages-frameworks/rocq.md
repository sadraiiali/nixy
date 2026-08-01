# Rocq و بسته‌های rocq {#sec-language-rocq}

توجه داشته باشید که "The Rocq Prover" (به اختصار Rocq) نام جدید دستیار اثبات است که قبلاً با نام Coq شناخته می‌شد. درایویشن‌های `coq` و `coqPackages` در حال حاضر هم برای نسخه‌های قدیمی‌تر Coq و هم برای برخی از نسخه‌های Rocq در طول دورهٔ گذار تغییر نام باقی می‌مانند. در حالت

```nix
coq.withPackages (
  ps: with ps; [
    mathcomp
    bignums
  ]
)
```

اگر سرور `vsrocq-language-server` یا `rocq-lsp` را نصب می‌کنید، در صورتی که می‌خواهید بسته‌های Coq/Rocq شما را پیدا کنند، حتماً آن‌ها را به‌جای نصب جداگانه، به عنوان بخشی از عبارت `coq.withPackages` بالا فهرست کنید.

## مجموعه‌های ویژگی بسته‌های Rocq: `rocqPackages` {#rocq-packages-attribute-sets-rocqpackages}

روش توصیه‌شده برای تعریف یک derivation برای یک کتابخانه Rocq، استفاده از تابع `rocqPackages.mkRocqDerivation

* `pname` (اجباری) نام بسته‌است،
* `version` (اختیاری، با مقدار پیش‌فرض `null`)، نسخه‌ای است که باید دریافت و ساخته شود؛ این صفت بسته به نوع و الگوی آن به چند روش تفسیر می‌شود:
  * اگر یک رشتهٔ نسخهٔ منتشرشدهٔ شناخته‌شده باشد (مثلاً از صفت `release` در زیر)، انتشار مربوطه انتخاب می‌شود و صفت `version` در derivation حاصل روی این رشتهٔ انتشار تنظیم می‌شود،
  * اگر یک پیشوند majorMinor به صورت `"x.y"` از یک نسخهٔ منتشرشدهٔ شناخته‌شده باشد (طبق تعریف بالا)، آخرین نسخهٔ منتشرشدهٔ شناخته‌شده با الگوی `"x.y.z"` انتخاب می‌شود (بر اساس ترتیب تعیین‌شده توسط `versionAtLeast`)،
  * اگر یک مسیر یا رشته‌ای نمایندهٔ یک مسیر مطلق باشد (یعنی با `"/"` شروع

همچنین صفات استاندارد دیگر `mkDerivation` را دریافت می‌کند، آن‌ها به همان شکل اضافه می‌شوند، به جز `meta` که `meta` محاسبه‌شده به صورت خودکار را گسترش می‌دهد (که در آن `platform` همانند `rocq-core` است و صفحه خانگی به صورت خودکار محاسبه می‌شود).

در اینجا یک نمونه بسته ساده آورده شده‌است. این یک کتابخانه خالص Rocq است، در نتیجه به Rocq وابسته است. این کتابخانه بر پایه کتابخانه Mathematical Components ساخته می‌شود، بنابراین برخی درایویشن‌های `mathcomp` را نیز به عنوان `extraBuildInputs` دریافت می‌کند.

```nix
{
  lib,
  mkRocqDerivation,
  version ? null,
  rocq-core,
  mathcomp,
  mathcomp-finmap,
  mathcomp-bigenough,
}:

mkRocqDerivation {
  # namePrefix leads to e.g. `name = rocq-core9.1-mathcomp2.5.0-multinomials-2.4.0`
  namePrefix = [
    "rocq-core"
    "mathcomp"
  ];
  pname = "multinomials";
  owner = "math-comp";
  inherit version;
  defaultVersion =
    let
      case = rocq: mc: out: {
        cases = [
          rocq-core
          mc
        ];
        inherit out;
      };
    in
    with lib.versions;
    lib.switch
      [ rocq-core.rocq-version mathcomp.version ]
      [
        (case (range "8.18" "9.1") (range "2.1.0" "2.5.0") "2.4.0")
        (case (range "8.17" "9.0") (range "2.1.0" "2.3.0") "2.3.0")
      ]
      null;
  release = {
    "2.4.0".sha256 = "sha256-7zfIddRH+Sl4nhEPtS/lMZwRUZI45AVFpcC/UC8Z0Yo=";
    "2.3.0".sha256 = "sha256-usIcxHOAuN+f/j3WjVbPrjz8Hl9ac8R6kYeAKi3CEts=";
  };

  propagatedBuildInputs = [
    mathcomp.boot
    mathcomp.algebra
    mathcomp-finmap
    mathcomp.fingroup
    mathcomp-bigenough
  ];

  meta = {
    description = "Coq/SSReflect Library for Monoidal Rings and Multinomials";
    license = lib.licenses.cecill-c;
  };
}
```

## سه روش برای بازنشانی بسته‌های Rocq {#rocq-overriding-packages}

سه روش متمایز برای تغییر یک بسته Rocq با بازنشانی یکی از مقادیر آن وجود دارد: `.override` ،`overrideRocqDerivation` و `.overrideAttrs`. این بخش توضیح می‌دهد چه نوع مقادیری را می‌توان با هر یک از این روش‌ها بازنشانی کرد.

### `.override` {#rocq-override}

روش `.override` به شما امکان می‌دهد آرگومان‌های یک derivation مربوط به Rocq را تغییر دهید. در مورد بسته `multinomials` در بالا، `.override` به شما اجازه می‌دهد آرگومان‌هایی مانند `mkRocqDerivation

```nix
multinomials.override { mathcomp = my-special-mathcomp; }
```

در Nixpkgs، تمامی درایویشن‌های Rocq یک آرگومان `version` می‌گیرند. این آرگومان را می‌توان بازنشانی کرد تا به‌راحتی از نسخه دیگری استفاده شود:

```nix
rocqPackages.multinomials.override { version = "1.5.1"; }
```

برای مشاهده تمام قالب‌های مختلفی که احتمالاً می‌توانید به `version` پاس دهید و همچنین محدودیت‌های آن، به [](#rocq-packages-attribute-sets-rocqpackages) مراجعه کنید.

### `overrideRocqDerivation` {#rocq-overrideRocqDerivation}

تابع `overrideRocqDerivation` به شما امکان می‌دهد آرگومان‌های داده‌شده به `mkRocqDerivation` را به‌راحتی تغییر دهید. این آرگومان‌ها در [](#rocq-packages-attribute-sets-rocqpackages) توصیف شده‌اند.

برای نمونه، در ادامه نحوه افزودن محلی انتشار جدیدی از کتابخانه `multinomials` و تنظیم `defaultVersion` برای استفاده از این انتشار آمده‌است:

```nix
rocqPackages.lib.overrideRocqDerivation {
  defaultVersion = "2.0";
  release."2.0".hash = "sha256-czoP11rtrIM7+OLdMisv2EF7n/IbGuwFxHiPtg3qCNM=";
} rocqPackages.multinomials
```

### `.overrideAttrs` {#rocq-overrideAttrs}

`.overrideAttrs` به شما امکان می‌دهد آرگومان‌های فراخوانی زیرین `stdenv.mkDerivation` را بازنویسی کنید. به صورت

```nix
rocqPackages.multinomials.overrideAttrs (oldAttrs: {
  postInstall = oldAttrs.postInstall or "" + ''
    echo "you can do anything you want here"
  '';
})
```
