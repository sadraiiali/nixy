# <a id="chap-overrides"></a> بازنشانی

گاهی اوقات شخص می‌خواهد بخش‌هایی از `nixpkgs` را بازنشانی کند، برای مثال صفات درایویشن‌ها یا نتایج در

```nix
pkgs.foo.override {
  arg1 = val1;
  arg2 = val2; # ...
}
```

همچنین امکان دسترسی به آرگومان‌های قبلی وجود دارد.

```nix
pkgs.foo.override (previous: {
  arg1 = previous.arg1; # ...
})
```

```nix
import pkgs.path {
  overlays = [ (self: super: { foo = super.foo.override { barSupport = true; }; }) ];
}
```

```nix
{
  mypkg = pkgs.callPackage ./mypkg.nix {
    mydep = pkgs.mydep.override {
      # ...
    };
  };
}
```

Nixpkgs یعنی `pkgs` را شامل می‌شود.

Paragraph 5:
نمونه‌های استفاده:

Let's double-check terms in Glossary:
- `derivation` -> `derivation /`

```nix
{
  helloBar = pkgs.hello.overrideAttrs (
    finalAttrs: previousAttrs: { pname = previousAttrs.pname + "-bar"; }
  );
}
```

در مثال بالا، "-bar" به صفت (attribute) `pname` اضافه می‌شود، در حالی که تمام صفات دیگر از بسته اصلی `hello` حفظ خواهند شد.

آرگومان ``

```nix
{ helloWithDebug = pkgs.hello.overrideAttrs { separateDebugInfo = true; }; }
```

در مثال بالا، صفت (attribute) `separateDebugInfo` بازنویسی می‌شود تا مقدار آن true باشد، در نتیجه اطلاعات دیباگ (اشکال‌زدایی) برای `helloWithDebug` ساخته می‌شود.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توجه داشته باشید که `separateDebugInfo` تنها توسط تابع `stdenv.mkDerivation` پردازش می‌شود، نه توسط derivation خام و تولیدشده‌ی Nix. بنابراین، استفاده از `overrideDerivation` در این مورد کار نخواهد کرد، زیرا تنها صفات derivation نهایی را بازنویسی می‌کند. به همین دلیل است که `overrideAttrs` باید در (تقریباً) همه موارد بر `overrideDerivation` ترجیح داده شود؛ یعنی امکان استفاده از `stdenv.mkDerivation` برای پردازش آرگومان‌های ورودی را فراهم می‌سازد،
>

> ```nix
> {
>   mySed = pkgs.gnused.overrideDerivation (oldAttrs: {
>     name = "sed-4.2.2-pre";
>     src = fetchurl {
>       url = "ftp://alpha.gnu.org/gnu/sed/sed-4.2.2-pre.tar.bz2";
>       hash = "sha256-MxBJRcM2rYzQYwJ5XKxhXTQByvSg5jZc5cSHEZoB2IY=";
>     };
>     patches = [ ];
>   });
> }
> ```
>
> / آرگومان
> - override -> بازنویسی / بازنشانی (overriding -> بازنشانی / بازنویسی)
>
> Let's review formatting:
> - Preserve `*before*` -> `*پیش از*`
> - Preserve
>

> ```nix
> {
>   f =
>     { a, b }:
>     {
>       result = a + b;
>     };
>   c = lib.makeOverridable f {
>     a = 1;
>     b = 2;
>   };
> }
> ```
>
> متغیر `c` مقدار تابع `f` است که با برخی آرگومان‌های پیش‌فرض اعمال شده است. از این رو در این مثال، مقدار `c.result` برابر با `3` است.
>
> با این حال، متغیر `c` دارای برخی توابع اضافی نیز هست، مانند
