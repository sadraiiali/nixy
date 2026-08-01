# بهترین روش‌ها

## URLها

سینتکس زبان Nix از URLهای بدون نقل‌قول پشتیبانی می‌کند، بنابراین می‌توان به جای `"https://example.com"` از `https://example.com` استفاده کرد.

[RFC 45](https://github.com/NixOS/rfcs/pull/45) برای منسوخ کردن URLهای بدون نقل‌قول پذیرفته شد و استدلال‌های متعددی را در این خصوص ارائه می‌دهد که چرا این ویژگی ضررش بیشتر از منفعتش است.

:::{tip}
همیشه برای URLها از نقل‌قول استفاده کنید.
:::

(rec-expression)=
## مجموعه ویژگی بازگشتی `rec { ... }`

دستور `rec` به شما اجازه می‌دهد تا به نام‌های درون همان مجموعه ویژگی ارجاع دهید.

مثال:

```{code-block} nix
:class: expression
rec {
  a = 1;
  b = a + 2;
}
```

```{code-block}
:class: value
{ a = 1; b = 3; }
```

یک اشتباه رایج، ایجاد یک خطای اشکال‌زدایی‌دشوار به نام `infinite recursion` (بازگشت بی‌نهایت) به هنگام پنهان‌سازی (shadowing) یک نام است.
ساده‌ترین مثال برای این حالت به شرح زیر است:

```{code-block} nix
let a = 1; in rec { a = a; }
```

:::{tip}
از `rec` اجتناب کنید. از `let ... in` استفاده کنید.

مثال:

```{code-block} nix
:class: expression
let
  a = 1;
in {
  a = a;
  b = a + 2;
}
```
:::

:::{tip}
خودارجاعی را می‌توان با نام‌گذاری صریح مجموعه ویژگی به دست آورد:

```{code-block} nix
:class: expression
let
  argset = {
    a = 1;
    b = argset.a + 2;
  };
in
  argset
```
:::

## حوزه‌های `with`

هنوز هم دیدن عبارت زیر در طبیعت (کدهای واقعی) رایج است:

```{code-block} nix
:class: expression
with (import <nixpkgs> {});

# ... lots of code
```

این کار تمام صفت‌های (attributes) عبارت درون‌ریزی‌شده را به محدوده (scope) عبارت فعلی می‌آورد.

این رویکرد دارای مشکلاتی است:

- تحلیل ایستا نمی‌تواند روی کد استدلال کند، زیرا برای اینکه ببیند چه نام‌هایی در محدوده (scope) قرار دارند، باید عملاً این فایل را ارزیابی کند.
- هنگامی که بیش از یک `with` استفاده می‌شود، دیگر مشخص نیست نام‌ها از کجا می‌آیند.
- قوانین محدوده (scoping) برای `with` بصری نیستند، برای جزئیات [این مسئله در Nix](https://github.com/NixOS/nix/issues/490) را ببینید.

:::{tip}
از `with` در بالای یک فایل Nix استفاده نکنید.
نام‌ها را به صورت صریح در یک عبارت `let` تخصیص دهید.

مثال:
:::{

```{code-block} nix
:class: expression
let
  pkgs = import <nixpkgs> {};
  inherit (pkgs) curl jq;
in

# ...
```
:::

امنیت دامنه‌های کوچک‌تر معمولاً چالش‌های کمتری ایجاد می‌کند، اما همچنان ممکن است به دلیل قوانین حاکم بر دامنه‌ها (scoping rules)، باعث بروز اتفاقات غیرمنتظره شود.

:::{tip}
اگر می‌خواهید کلاً از `with` اجتناب کنید، سعی کنید عبارت‌هایی به این شکل را جایگزین کنید

```{code-block} nix
:class: expression
buildInputs = with pkgs; [ curl jq ];
```

با موارد زیر:

```{code-block} nix
:class: expression
buildInputs = builtins.attrValues {
  inherit (pkgs) curl jq;
};
```
:::

(search-path)=
## مسیرهای جستجوی `<...>`

اغلب با نمونه‌کدهای زبان Nix مواجه خواهید شد که به `<nixpkgs>` اشاره می‌کنند.

`<...>` یک نحو (syntax) ویژه است که در [سال ۲۰۱۱ معرفی شد] تا دسترسی راحت به مقادیر حاصل از متغیر محیطی [`$NIX_PATH`] را فراهم کند.

[introduced in 2011]: https://github.com/NixOS/nix/commit/1ecc97b6bdb27e56d832ca48cdafd3dbb5185a04
[`$NIX_PATH`]: /pages/nix-manual/command-ref/env-common#env-NIX_PATH

این یعنی مقدار یک مسیر جستجو به وضعیت خارجی سیستم بستگی دارد.
هنگام استفاده از مسیرهای جستجو، یک عبارت Nix یکسان ممکن است نتایج متفاوتی تولید کند.

در بیشتر موارد، هنگام نصب Nix متغیر `$NIX_PATH` روی آخرین کانال تنظیم می‌شود، و بنابراین احتمالاً از یک ماشین تا ماشین دیگر متفاوت خواهد بود.

:::{note}
[کانال‌ها](/pages/nix-manual/command-ref/nix-channel) مکانیزمی برای ارجاع به عبارت‌های راه دور Nix و بازیابی آخرین نسخه آن‌ها هستند.
:::

وضعیت یک کانال مشترک، خارج از عبارت‌های Nixی است که به آن وابسته‌اند.
این وضعیت به راحتی روی ماشین‌های مختلف قابل انتقال نیست.
این موضوع ممکن است بازتولیدپذیری را محدود کند.

برای مثال، دو توسعه‌دهنده روی ماشین‌های مختلف احتمالاً `<nixpkgs>` را به نسخه‌های متفاوتی از مخزن {term}`Nixpkgs` ارجاع می‌دهند.
ممکن است ساخت‌ها برای یکی موفقیت‌آمیز باشد و برای دیگری با خطا مواجه شود که باعث سردرگمی می‌شود.

:::{tip}
با استفاده از روش‌های نشان‌داده‌شده در بخش [](pinning-nixpkgs)، وابستگی‌ها را به صورت صریح اعلام کنید.

به‌جز در مثال‌های مینیمال، از مسیرهای جستجو استفاده نکنید.
:::

برخی ابزارها انتظار دارند مسیر جستجو تنظیم شده باشد. در آن صورت:

::::{tip}
متغیر `$NIX_PATH` را روی یک مقدار مشخص در یک مکان مرکزی تحت کنترل نسخه تنظیم کنید.

:::{admonition} NixOS
در NixOS، متغیر `$NIX_PATH` را می‌توان به صورت دائم با گزینه [`nix.nixPath`](https://search.nixos.org/options?show=nix.nixPath) تنظیم کرد.
:::
::::

(nixpkgs-config)=
## پیکربندی بازتولیدپذیر Nixpkgs

برای دریافت سریع بسته‌ها جهت نمایش، از الگوی مختصر زیر استفاده می‌کنیم:

```nix
import <nixpkgs> {}
```

با این حال، حتی زمانی که `<nixpkgs>` طبق تصویر نشان داده‌شده در [](pinning-nixpkgs) جایگزین شود، ممکن است نتیجه همچنان کاملاً بازتولیدپذیر نباشد.
این به آن دلیل است که بنا به دلایل تاریخی، [عبارت سطح بالای Nixpkgs] به‌طور پیش‌فرض و به شکلی ناخالص برای به‌دست آوردن پارامترهای پیکربندی از سیستم‌فایل خوانش می‌کند.
سیستم‌هایی که فایل‌های مناسب در آن‌ها مقداردهی اولیه شده باشند، ممکن است در نهایت به نتایج متفاوتی برسند.

[Nixpkgs top-level expression]: https://github.com/NixOS/nixpkgs/blob/master/default.nix

این یک مشکل شناخته‌شده‌است که بدون شکستن پیکربندی‌های موجود قابل‌حل نیست.

:::{tip}
هنگام درون‌ریزی Nixpkgs، مقادیر [`config`](https://nixos.org/manual/nixpkgs/stable/#chap-packageconfig) و [`overlays`](https://nixos.org/manual/nixpkgs/stable/#chap-overlays) را به‌طور صریح تنظیم کنید:

```nix
import <nixpkgs> { config = {}; overlays = []; }
```
:::

این کاری است که ما در آموزش‌های خود انجام می‌دهیم تا اطمینان حاصل کنیم که مثال‌ها دقیقاً مطابق انتظار عمل خواهند کرد.
ما این کار را در مثال‌های مینیمال برای کاهش عوامل حواس‌پرتی رد می‌کنیم.

## به‌روزرسانی مجموعه‌های ویژگی تو در تو

[عملگر به‌روزرسانی مجموعه ویژگی](/pages/nix-manual/language/operators#update) دو مجموعه ویژگی را با هم ادغام می‌کند.

مثال:

```{code-block} nix
:class: expression
{ a = 1; b = 2; } // { b = 3; c = 4; }
```

```{code-block} nix
:class: value
{ a = 1; b = 3; c = 4; }
```

با این حال، نام‌های سمت راست اولویت دارند و به‌روزرسانی‌ها سطحی هستند.

مثال:

```{code-block} nix
:class: expression
{ a = { b = 1; }; } // { a = { c = 3; }; }
```

```{code-block} nix
:class: value
{ a = { c = 3; }; }
```

در اینجا، کلید `b` به طور کامل حذف شد، زیرا کل مقدار `a` جایگزین شد.

:::{tip}
از تابع Nixpkgs [`pkgs.lib.recursiveUpdate`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.attrsets.recursiveUpdate) استفاده کنید:

```{code-block} nix
:class: expression
let pkgs = import <nixpkgs> {}; in
pkgs.lib.recursiveUpdate { a = { b = 1; }; } { a = { c = 3;}; }
```

```{code-block} nix
:class: value
{ a = { b = 1; c = 3; }; }
```
:::

## مسیرهای کد منبع بازتولیدپذیر

```{code-block} nix
:class: expression
let pkgs = import <nixpkgs> {}; in

pkgs.stdenv.mkDerivation {
  name = "foo";
  src = ./.;
}
```

اگر فایل Nix حاوی این عبارت در `/home/myuser/myproject` باشد، آنگاه مسیر انبار `src` برابر با `/nix/store/<hash>-myproject` خواهد شد.

مشکل این است که اکنون ساخت شما دیگر بازتولیدپذیر نیست، زیرا به نام پوشه والد بستگی دارد.
این موضوع را نمی‌توان در کد منبع اعلام کرد و منجر به یک ناخالصی می‌شود.

اگر شخصی پروژه را در پوشه‌ای با نامی متفاوت بسازد، مسیر انبار متفاوتی برای `src` و هر چیز دیگری که به آن وابسته است دریافت خواهد کرد.
این امر می‌تواند دلیل ساخت‌های مجدد غیرضروری باشد.

:::{tip}
از [`builtins.path`](/pages/nix-manual/language/builtins-prefix#builtins-path) به همراه صفت `name` تنظیم‌شده روی یک مقدار ثابت استفاده کنید.

این کار نام نمادین مسیر انبار را به‌جای دایرکتوری کاری، از `name` استخراج خواهد کرد:

```{code-block} nix
:class: expression
let pkgs = import <nixpkgs> {}; in

pkgs.stdenv.mkDerivation {
  name = "foo";
  src = builtins.path { path = ./.; name = "myproject"; };
}
```
:::
