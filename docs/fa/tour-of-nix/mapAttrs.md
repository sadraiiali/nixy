# mapAttrs

> درس **28** / ۳۵ · مسیر `mapAttrs`

تابعی به نام `builtins.mapAttrs` وجود دارد که شبیه به `builtins.map` است.

تابع `mapAttrs` به این آرگومان‌ها نیاز دارد: یک `function` و یک `attrSet`.

این تابع، تابع ارائه‌شده را روی هر عنصر از مجموعه ویژگی داده‌شده ارزیابی می‌کند.

وظیفه شما:

 * در این تمرین، هر *مقدار* را در ۷ ضرب کنید.

مستندات: <https://nixos.org/manual/nix/stable/language/builtins.html#builtins-mapAttrs>

**نکته**: تابع mapAttrs توکار است اما در این نسخه قدیمی از تور وجود ندارد، به جای آن صرفاً از `lib.mapAttrs` استفاده کنید!

## کد شروع

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attrSet = { a = -2; b = 3; };
in 
{
  ex0 = lib.mapAttrs XXX
}
```

## راهحل

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attrSet = { a = -2; b = 3; };
in 
{
  ex0 = lib.mapAttrs (n: v: v * 7) attrSet;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=JYHTVORLGA0&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=mapAttrs) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
