# ابزارهای کمکی شل توسعه {#chap-devShellTools}

دستور `nix-shell` مفهوم محیط‌های شل زودگذر را برای مقاصد توسعه یا آزمایش رواج داده‌است.
<!--
  ما باید سعی کنیم خود محصول را در راهنمای Nixpkgs مستند کنیم، نه فرآیند توسعه‌ی آن را،
  اما برای ارائه‌ی زمینه برای این کتابخانه باید *چیزی* گفته شود.
  این آینده‌نگرانه‌ترین جمله‌ای است که توانستم ارائه دهم، در حالی که خود Nix هنوز از این استفاده نمی‌کند.
  وضعیت فعلی صفت devShell مرتبط است: https://github.com/NixOS/nix/issues/7501
  -->
با این حال، `nix-shell` تنها راه برای ایجاد چنین محیط‌هایی نیست و حتی خود `nix-shell` نیز می‌تواند به طور غیرمستقیم از این کتابخانه بهره‌مند شود.

این کتابخانه مجموعه‌ای از توابع را ارائه می‌دهد که به ایجاد چنین محیط‌هایی کمک می‌کنند.

## `devShellTools.valueToString` {#sec-devShellTools-valueToString}

مقادیر Nix را به همان روشی که [تابع توکار `derivation`](https://nix.dev/manual/nix/2.23/language/derivations) انجام می‌دهد، به رشته تبدیل می‌کند.

:::{.example}
## نمونه‌های استفاده از `valueToString`

```nix
devShellTools.valueToString (builtins.toFile "foo" "bar")
# => "/nix/store/...-foo"
```

```nix
devShellTools.valueToString false
# => ""
```

:::

## `devShellTools.unstructuredDerivationInputEnv` {#sec-devShellTools-unstructuredDerivationInputEnv}

تبدیل یک مجموعه از صفات derivation (همان‌طور که به [`derivation`] ارسال می‌شود) به مجموعه‌ای از متغیرهای محیطی که می‌توانند در یک اسکریپت شل استفاده شوند.
این تابع از `__structuredAttrs` پشتیبانی نمی‌کند، اما از `passAsFile` پشتیبانی می‌کند.

:::{.example}
## نمونه استفاده از `unstructuredDerivationInputEnv`

```nix
devShellTools.unstructuredDerivationInputEnv {
  drvAttrs = {
    name = "foo";
    buildInputs = [
      hello
      figlet
    ];
    builder = bash;
    args = [
      "-c"
      "${./builder.sh}"
    ];
  };
}
# => {
#  name = "foo";
#  buildInputs = "/nix/store/...-hello /nix/store/...-figlet";
#  builder = "/nix/store/...-bash";
#}
```

توجه داشته باشید که `args` گنجانده نشده‌است، زیرا Nix آن را به محیط فرآیند سازنده (Builder) اضافه نمی‌کند.

:::

## `devShellTools.derivationOutputEnv` {#sec-devShellTools-derivationOutputEnv}

بخش‌های مرتبط یک derivation / اشتقاق ساخت را دریافت کرده و مجموعه‌ای از متغیرهای محیطی که در آن derivation وجود خواهند داشت را برمی‌گرداند.

:::{.example}
## نمونه استفاده از `derivationOutputEnv`

```nix
let
  pkg = hello;
in
devShellTools.derivationOutputEnv {
  outputList = pkg.outputs;
  outputMap = pkg;
}
```

:::
