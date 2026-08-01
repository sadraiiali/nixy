# <a id="sec-generators"></a> مولدها
مولدها توابعی هستند که قالب‌های فایل را از ساختارهای داده Nix ایجاد می‌کنند، به عنوان مثال برای فایل‌های پیکربندی. مولدهایی برای `INI`، `JSON` و `YAML` در دسترس هستند.

تمام مولدها از یک واسط فراخوانی مشابه پیروی می‌کنند: `generatorName configFunctions data` که در آن `configFunctions` یک مجموعه ویژگی از توابع تعریف‌شده توسط کاربر است که بخش‌های تو در توی محتوا را قالب‌بندی می‌کنند. هر کدام دارای مقادیر پیش‌فرض مشترکی هستند، بنابراین اغلب نیازی به تنظیم دستی آن‌ها نیست. یک نمونه، `mkSectionName` از مولد `INI` است که به‌طور پیش‌فرض برابر با `(name: libStr.escape [ "[" "]" ] name)` است. این تابع نام یک بخش را دریافت کرده و آن را پاک‌سازی می‌کند. تابع پیش‌فرض `mkSectionName` کاراکترهای `[` و `]` را با بک‌اسلش گریزدهی (escape) می‌کند.

مولدها را می‌توان به‌دقت تنظیم کرد تا دقیقاً همان قالب فایل مورد نیاز برنامه/سرویس شما را تولید کنند. یک نمونه، یک قالب فایل INI است که از `: ` به عنوان جداکننده و رشته‌های `"yes"` و `"no"` به عنوان مقادیر بولین استفاده می‌کند و نیاز دارد تمام مقادیر رشته‌ای داخل گیومه قرار گیرند:

```nix
let
  inherit (lib) generators isString;

  customToINI = generators.toINI {
    # specifies how to format a key/value pair
    mkKeyValue = generators.mkKeyValueDefault {
      # specifies the generated string for a subset of nix values
      mkValueString =
        v:
        if v == true then
          ''"yes"''
        else if v == false then
          ''"no"''
        else if isString v then
          ''"${v}"''
        # and delegates all other values to the default generator
        else
          generators.mkValueStringDefault { } v;
    } ":";
  };

  # the INI file can now be given as plain old nix values
in
customToINI {
  main = {
    pushinfo = true;
    autopush = false;
    host = "localhost";
    port = 42;
  };
  mergetool = {
    merge = "diff3";
  };
}
```

این عبارت فایل INI زیر را به عنوان یک رشته Nix تولید خواهد کرد:

```INI
[main]
autopush:"no"
host:"localhost"
port:42
pushinfo:"yes"
str\:ange:"very::strange"

[mergetool]
merge:"diff3"
```

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> مسیرهای انبار نیکس (Nix store) را می‌توان با قرار دادن صفت (attribute) یک derivation / اشتقاق ساخت به این صورت به رشته‌ها تبدیل کرد: `"${'{'}'{'{'}'{'}'}drv{'{'}'{'}'}'{'}'}"`.

مستندات تفصیلی برای هر مولد را می‌توان در [اینجا](#sec-functions-library-generators) یافت.
