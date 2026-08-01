# پیاده‌سازی مجدد: attrValues

> درس **۳۳** از ۳۵ · مسیر `reimplementation/attrValues`

پیاده‌سازی خود را از تابع `attrValues` بنویسید.

 این تابع یک `مجموعه ویژگی` را به عنوان ورودی دریافت می‌کند و تمام مقادیر را
 مرتب‌شده بر اساس `صفت (attribute)` برمی‌گرداند.

 شما مجاز هستید از تابع توکار `attrNames`
 و تابع `attrVals` که در درس قبل پیاده‌سازی کردید،
 استفاده کنید.

### مقایسه `attrVals` با `attrValues`:

* `attrVals` -> با دریافت لیستی از نام‌ها، مقادیر آن‌ها را از مجموعه استخراج کرده و لیستی از آن‌ها را برمی‌گرداند

 `attrVals ["a" "b" "c"] attrSet; => should be [1 2 3]`

* `attrValues` -> تمام مقادیر موجود در مجموعه داده‌شده را استخراج کرده و لیستی از آن‌ها را برمی‌گرداند

 `attrValues attrSet; => [1 2 3 4]`

**هشدار:** این مرحله دشوار است!

## کد اولیه

```nix
with import <nixpkgs> { };
let
  attrSet = {c = 3; a = 1; b = 2;};

  attrValues = XXX;
in
rec {
  solution = attrValues attrSet; #should be [1 2 3]
}
```

## راهحل

```nix
with import <nixpkgs> { };
let
  attrSet = {c = 3; a = 1; b = 2;};

  attrValues = attrSet: lib.attrVals (builtins.attrNames attrSet) attrSet;
in
rec {
  solution = attrValues attrSet; #should be [1 2 3]
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=oikq0CBWR4w&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=reimplementation/attrValues) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
