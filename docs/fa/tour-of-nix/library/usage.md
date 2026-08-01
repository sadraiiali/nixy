# دستورات inherit / import / with!

> درس **22** / 35 · مسیر `library/usage`

این ۳ کلیدواژه می‌توانند به راحتی باعث سردرگمی شوند. از آنجا که ما از آن‌ها به وفور در `A tour of Nix` استفاده می‌کنیم، باید آن‌ها را به درستی معرفی کنیم.

## عبارت With

یک عبارت با کلیدواژه with، مجموعه `set e1` را وارد محدوده lexical (محدوده واژگانی) `expression e2` می‌کند.

    let 
      as = { x = "foo"; y = "bar"; };
    in 
      with as; x + y

## عبارت Import

یک عبارت Nix را در مسیر فایل بارگذاری، تجزیه (parse) و بازمی‌گرداند.
دستور `import` سیستم ماژول Nix را پیاده‌سازی می‌کند: شما می‌توانید هر عبارت Nix (مانند یک مجموعه یا یک تابع) را در یک فایل جداگانه قرار دهید و از عبارت‌های Nix در فایل‌های دیگر آن را فراخوانی کنید.

    rec {
      x = 123;
      y = import ./foo.nix;
    }

## عبارت Inherit
کلیدواژه `inherit` باعث می‌شود که `attributes` مشخص‌شده به هر صفت همنامی که در محدوده (scope) فعلی وجود دارد، متصل شوند.

    let 
      x = 123; 
    in
    { 
      inherit x;
      y = 456;
    }
دستور `inherit` یک یا چند آرگومان می‌پذیرد.

این کار را انجام دهید:

* آن را به کار بیندازید!

## کد شروع

```nix
let 
  myImport = import <nixpkgs> {};
  x = 123; 
  as = { a = "foo"; b = "bar"; };
  
in with as; { 
  inherit x; #example
  #fix line below: we want a and b in this scope
  inherit X; 
  #also fix this line
  z = XXX.lib.isBool true;
}
```

## راه حل

```nix
let 
  myImport = import <nixpkgs> {};
  x = 123; 
  as = { a = "foo"; b = "bar"; };
  
in with as; { 
  inherit x;
  inherit a b;
  z = myImport.lib.isBool true;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=1XwNjrCVUvs&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [تور نیکس](https://nixcloud.io/tour/?id=library/usage) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
