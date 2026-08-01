# <a id="chap-devShellTools"></a> ابزارهای کمکی شل توسعه

دستور `nix-shell` مفهوم محیط‌های شل زودگذر را برای مقاصد توسعه یا آزمایش رواج داده است.

با این حال، `nix-shell` تنها راه برای ایجاد چنین محیط‌هایی نیست و حتی خود `nix-shell` نیز می‌تواند به طور غیرمستقیم از این کتابخانه بهره‌مند شود.

این کتابخانه مجموعه‌ای از توابع را ارائه می‌دهد که به ایجاد چنین محیط‌هایی کمک می‌کنند.

## <a id="sec-devShellTools-valueToString"></a> `devShellTools.valueToString`

مقادیر Nix را به همان روشی که [تابع توکار `derivation`](/pages/nix-manual/language/derivations) انجام می‌دهد، به رشته تبدیل می‌کند.

> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> ## نمونه‌های استفاده از `valueToString`
>

> ```nix
> devShellTools.valueToString (builtins.toFile "foo" "bar")
> # => "/nix/store/...-foo"
> ```
>

> ```nix
> devShellTools.valueToString false
> # => ""
> ```

## <a id="sec-devShellTools-unstructuredDerivationInputEnv"></a> `devShellTools.unstructuredDerivationInputEnv`

تبدیل یک مجموعه از صفات derivation (همان‌طور که به [`derivation`] ارسال می‌شود) به مجموعه‌ای از متغیرهای محیطی که می‌توانند در یک اسکریپت شل استفاده شوند.
این تابع از `__structuredAttrs` پشتیبانی نمی‌کند، اما از `passAsFile` پشتیبانی می‌کند.

> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> ## نمونه استفاده از `unstructuredDerivationInputEnv`
>

> ```nix
> devShellTools.unstructuredDerivationInputEnv {
>   drvAttrs = {
>     name = "foo";
>     buildInputs = [
>       hello
>       figlet
>     ];
>     builder = bash;
>     args = [
>       "-c"
>       "${./builder.sh}"
>     ];
>   };
> }
> # => {
> #  name = "foo";
> #  buildInputs = "/nix/store/...-hello /nix/store/...-figlet";
> #  builder = "/nix/store/...-bash";
> #}
> ```
>
> توجه داشته باشید که `args` گنجانده نشده است، زیرا Nix آن را به محیط فرآیند سازنده (Builder) اضافه نمی‌کند.

## <a id="sec-devShellTools-derivationOutputEnv"></a> `devShellTools.derivationOutputEnv`

بخش‌های مرتبط یک derivation / اشتقاق ساخت را دریافت کرده و مجموعه‌ای از متغیرهای محیطی که در آن derivation وجود خواهند داشت را برمی‌گرداند.

> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> ## نمونه استفاده از `derivationOutputEnv`
>

> ```nix
> let
>   pkg = hello;
> in
> devShellTools.derivationOutputEnv {
>   outputList = pkg.outputs;
>   outputMap = pkg;
> }
> ```
