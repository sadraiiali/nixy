# <a id="sec-ibus-typing-booster"></a> ibus-engines.typing-booster

این بسته یک روش تکمیل خودکار مبتنی بر ibus برای افزایش سرعت تایپ است.

## <a id="sec-ibus-typing-booster-activate"></a> فعال‌سازی موتور

برای فعال‌سازی `typing-booster` لازم است IBus بر همین اساس پیکربندی شود. این پیکربندی به مدیر میزکار در حال استفاده بستگی دارد. برای دریافت دستورالعمل‌های تفصیلی، لطفاً به [مستندات بالادستی](https://mike-fabian.github.io/ibus-typing-booster/) مراجعه کنید.

در NixOS، پیش از سفارشی‌سازی محیط میزکار خود برای استفاده از `typing-booster`، باید `ibus` را همراه با موتورهای مورد نظر صراحتاً فعال کنید. این کار با استفاده از ماژول `ibus` امکان‌پذیر است:

```nix
{ pkgs, ... }:
{
  i18n.inputMethod = {
    enable = true;
    type = "ibus";
    ibus.engines = with pkgs.ibus-engines; [ typing-booster ];
  };
}
```

## <a id="sec-ibus-typing-booster-customize-hunspell"></a> استفاده از دیکشنری‌های سفارشی hunspell

موتور IBus برای پشتیبانی از تکمیل

```nix
ibus-engines.typing-booster.override {
  langs = [
    "de-at"
    "en-gb"
  ];
}
```

_نکته: هر زبانی که به `langs` پاس داده می‌شود، باید نام یک صفت در `pkgs.hunspellDicts` باشد._

## <a id="sec-ibus-typing-booster-emoji-picker"></a> انتخاب‌کننده ایموجی توکار

بسته `ibus-engines.typing-booster` شامل برنامه‌ای به نام `emoji-picker` است. برای نمایش درست همه ایموجی‌ها، به یک فونت ویژه مانند `noto-fonts-color-emoji` نیاز است:

در NixOS، می‌توان آن را با استفاده از عبارت زیر نصب کرد:

```nix
{ pkgs, ... }:
{
  fonts.packages = with pkgs; [ noto-fonts-color-emoji ];
}
```
