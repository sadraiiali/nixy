# <a id="typst"></a> Typst

Typst را می‌توان برای شامل کردن بسته‌ها از [Typst Universe](https://typst.app/universe/) یا بسته‌های سفارشی پیکربندی کرد.

## <a id="typst-custom-environment"></a> محیط سفارشی

شما می‌توانید با استفاده از کد زیر، یک محیط Typst سفارشی همراه با مجموعه‌ای انتخاب‌شده از بسته‌های **

```nix
typst.withPackages (
  p: with p; [
    polylux_0_4_0
    cetz_0_3_0
  ]
)
```

برای گزینه‌های سفارشی‌سازی بیشتر، می‌توانید wrapper را مستقیماً فراخوانی کنید:

```nix
typst.wrapper {
  packages = p: [ ];
  fonts = [ ];
  extraWrapperArgs = [ ];
}
```

### <a id="typst-handling-outdated-package-hashes"></a> مدیریت هش‌های قدیمی بسته

از آنجا که **Typst Universe** راهکاری برای دریافت یک بسته با یک هش مشخص ارائه نمی‌کند، هش‌های بسته در `nixpkgs` ممکن است گاهی قدیمی شوند. برای برطرف کردن این مشکل، می‌توانید منبع بسته را با استفاده از روش زیر به‌صورت دستی بازنشانی کنید:

```nix
typst.withPackages.override
  (old: {
    typstPackages = old.typstPackages.overrideScope (
      _: previous: {
        polylux_0_4_0 = previous.polylux_0_4_0.overrideAttrs (oldPolylux: {
          src = oldPolylux.src.overrideAttrs { outputHash = YourUpToDatePolyluxHash; };
        });
      }
    );
  })
  (
    p: with p; [
      polylux_0_4_0
      cetz_0_3_0
    ]
  )
```

## <a id="typst-custom-packages"></a> بسته‌های سفارشی

`Nixpkgs` یک تابع کمکی به نام `buildTypstPackage` برای ساخت بسته‌های سفارشی Typst ارائه می‌دهد که می‌توان از آن‌ها در محیط Typst استفاده کرد. با این حال، تمام وابستگی‌های بسته سفارشی باید به طور صریح در `typstDeps` مشخص شوند.

در ادامه نحوه تعریف یک بسته سفارشی Typst آمده است:

```nix
{ buildTypstPackage, typstPackages }:

buildTypstPackage (finalAttrs: {
  pname = "my-typst-package";
  version = "0.0.1";
  src = ./.;
  typstDeps = with typstPackages; [ cetz_0_3_0 ];
})
```

### <a id="typst-package-scope-and-usage"></a> حوزه و نحوه استفاده از بسته

به‌طور پیش‌فرض، هر بسته سفارشی تحت حوزه `@preview` قرار می‌گیرد، همان‌طور که در زیر نشان داده شده است:

```typst
#import "@preview/my-typst-package:0.0.1": *
```

از آنجا که `@preview` برای بسته‌های **Typst Universe** در نظر گرفته شده است، توصیه می‌شود از این روش **تنها برای تغییرات موقت یا آزمایشی روی بسته‌های موجود** از **Typst Universe** استفاده کنید.

از سوی دیگر، **بسته‌های محلی** (بسته‌هایی که تحت حوزهٔ `@local` قرار دارند)، بخشی از محیط Typst محسوب **نمی‌شوند**. این بدان معناست که بسته‌های محلی در صورت نیاز باید به‌صورت دستی به کامپایلر Typst پیوند داده شوند.
