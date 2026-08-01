# پیاده‌سازی مجدد: attrVals

> درس **۳۲** / ۳۵ · مسیر `reimplementation/attrVals`

پیاده‌سازی خودتان از تابع `attrVals` را بنویسید.

این تابع یک لیست از `attribute names` و یک `attribute set` را دریافت می‌کند. این تابع مقادیر هر `attribute name` را برمی‌گرداند.

**نکته**: به یاد داشته باشید که عبارت `attrSet ? "a"` مقدار `true` و عبارت `attrSet ? "j"` مقدار `false` را برمی‌گرداند!

**نکته**: به یاد داشته باشید که عبارت `key = "a"; attrSet.${key}` مقدار `1` را برمی‌گرداند!

### مقایسه `attrVals` با `attrValues`:

* `attrVals` -> با داشتن یک لیست از نام‌ها، مقادیر آن‌ها را از مجموعه استخراج کرده و لیستی از آن‌ها را برمی‌گرداند.

 `attrVals ["a" "b" "c"] attrSet; => باید [1 2 3] باشد`

* `attrValues` -> تمام مقادیر موجود در مجموعه داده‌شده را استخراج کرده و لیستی از آن‌ها را برمی‌گرداند.

 `attrValues attrSet; => [1 2 3 4]`

**هشدار:** این کار دشوار است!

## کد اولیه

```nix
with import <nixpkgs> { };
let
  attrSet = {c = 3; a = 1; b = 2; d=4;};

  #tips: use the map function and access the attribute values 
  attrVals = XXX;

in
rec {

  solution = attrVals ["a" "b" "c"] attrSet; #should be [1 2 3]
}
```

## راه حل

```nix

with import <nixpkgs> { };
let
  attrSet = {c = 3; a = 1; b = 2; d=4;};
  attrVals = kys: se: lib.fold (el: c: if se ? "${el}" then [(se.${el})] ++ c else c) [] kys;

in
rec {

  solution = attrVals ["a" "b" "c"] attrSet; #should be [1 2 3]
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=CQAeAyRX1zs&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=reimplementation/attrVals) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
