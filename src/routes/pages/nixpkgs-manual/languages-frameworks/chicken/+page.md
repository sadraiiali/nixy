# <a id="sec-chicken"></a> CHICKEN

[CHICKEN](https://call-cc.org/) یک کامپایلر Scheme سازگار با [R⁵RS](https://schemers.org/Documents/Standards/R5RS/HTML/) است. این کامپایلر شامل یک حالت تعاملی و یک قالب بسته سفارشی به نام «eggs» است.

## <a id="sec-chicken-using"></a> استفاده از Eggs

Eggs توصیف‌شده در Nixpkgs در داخل مجموعه ویژگی `chickenPackages.chickenEggs` در دسترس هستند. افزودن یک egg به عنوان ورودی ساخت به روش معمول Nix انجام می‌شود. برای مثال، جهت افزودن پشتیبانی از [SRFI 189](https://srfi.schemers.org/srfi-189/srfi-189.html) در یک derivation، می‌توان این‌گونه نوشت:

```nix
{
  buildInputs = [
    chicken
    chickenPackages.chickenEggs.srfi-189
  ];
}
```

هم `chicken` و هم ایگ‌های (eggs) آن دارای یک قلاب راه‌اندازی (setup hook) هستند که متغیرهای محیطی `CHICKEN_INCLUDE_PATH` و `CHICKEN_REPOSITORY_PATH` را پیکربندی می‌کند.

## <a id="sec-chicken-updating-eggs"></a> به‌روزرسانی ایگ‌ها

Nixpkgs تنها زیرمجموعه‌ای از تمام ایگ‌های منتشرشده را می‌شناسد. این سیستم از [egg2nix](https://github.com/the-kenny/egg2nix) برای تولید یک مجموعه بسته از فهرستی از ایگ‌های موردنظر استفاده می‌کند.

این مجموعه بسته با اجرای دستورات شل (Shell) زیر بازتولید می‌شود:

```
$ nix-shell -p chickenPackages.egg2nix
$ cd pkgs/development/compilers/chicken/5/
$ egg2nix eggs.scm > eggs.nix
```

## <a id="sec-chicken-adding-eggs"></a> افزودن eggها

وقتی `egg2nix` را اجرا می‌کنیم، مجموعه‌ای از eggها با نسخه‌های سازگار با یکدیگر به دست می‌آوریم. این بدان معناست که وقتی eggهای جدیدی اضافه می‌کنیم، ممکن است لازم باشد eggهای موجود را به‌روزرسانی کنیم. برای جدا نگه داشتن این مراحل، قبل از افزودن eggهای بیشتر، دستورالعمل به‌روزرسانی eggها را دنبال کنید.

برای افزودن eggهای بیشتر، فایل `pkgs/development/compilers/chicken/5/eggs.scm` را ویرایش کنید.
بخش اول این فایل، eggهایی را فهرست می‌کند که خود `egg2nix` به آن‌ها نیاز دارد؛ تمام eggهای دیگر در بخش دوم قرار می‌گیرند. پس از ویرایش، دستورالعمل به‌روزرسانی eggها را دنبال کنید.

## <a id="sec-chicken-override-scope"></a> اسکوپ بازنشانی

بسته chicken و eggهای آن به‌ترتیب در یک اسکوپ قرار دارند. این بدان معناست که می‌توان این اسکوپ را بازنشانی کرد تا بر سایر بسته‌های موجود در آن تأثیر بگذارد.

این مثال نحوه استفاده از یک نسخه محلی `srfi-180` و اعمال تأثیر آن بر تمام eggهای دیگر را نشان می‌دهد:

```nix
let
  myChickenPackages = pkgs.chickenPackages.overrideScope (
    self: super: {
      # The chicken package itself can be overridden to affect the whole ecosystem.
      # chicken = super.chicken.overrideAttrs {
      #   src = ...
      # };

      chickenEggs = super.chickenEggs.overrideScope (
        eggself: eggsuper: {
          srfi-180 = eggsuper.srfi-180.overrideAttrs {
            # path to a local copy of srfi-180
            src = <...>;
          };
        }
      );
    }
  );
  # Here, `myChickenPackages.chickenEggs.json-rpc`, which depends on `srfi-180` will use
  # the local copy of `srfi-180`.
in
<...>
```
