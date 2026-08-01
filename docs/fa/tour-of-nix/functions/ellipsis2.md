# توابع: الگوی @-بخش دوم

> درس **11** / 35 · مسیر `functions/ellipsis2`

`مجموعه ویژگی`‌ها می‌توانند حاوی صفت‌های اضافه‌ای باشند که بخشی از تعریف تابع نیستند.

در داخل یک تابع، به آن `صفت‌`ها می‌توان با استفاده از `الگوی @` دسترسی پیدا کرد.

**نکته:** عبارت `bargs@{a, b, ...}:` معادل `{a, b, ...}@bargs:` است.

اکنون خط آخر را کامل کنید: 

* نتیجه‌ی ارزیابی آن باید 'foobar' باشد.

نحوه‌ی استفاده از آن را در [nixpkgs/all-packages](https://github.com/NixOS/nixpkgs/blob/5a237aecb57296f67276ac9ab296a41c23981f56/pkgs/top-level/all-packages.nix#L16761) ببینید.

## کد اولیه

```nix
let
  func = {a, b, ...}@bargs: if a == "foo" then
    b + bargs.c else b + bargs.x + bargs.y;
in
{
  #complete next line so it evaluates to "foobar"
  foobar = func {a="bar"; XXX #ONLY EDIT THIS LINE
}
```

## راه حل

```nix
let
  func = {a, b, ...}@bargs: if a == "foo" then
    b + bargs.c else b + bargs.x + bargs.y;
in
{
  #complete next line so it evaluates to "foobar"
  foobar = func {a="bar"; b="foo"; x="bar"; y="";}; 
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=Rwcwcw169P8&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=functions/ellipsis2) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
