# مجموعه ویژگی‌ها: مثال‌های ۱

> درس **۱۵** از ۳۵ · مسیر `attrset/examples`

کاری کنید که تمام `ex0` تا `ex7` به مقدار درست ارزیابی شوند.

**نکته:** برای عملگر '?'، به <https://nixos.org/manual/nix/stable/language/operators#has-attribute> مراجعه کنید.

**نکته:** <https://nixos.org/manual/nix/stable/language/builtins.html#builtins-listToAttrs>

## کد اولیه

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attr = {a="a"; b = 1; c = true;};
  s = "b";
in
{
  #replace all X, everything should evaluate to true
  ex0 = isAttrs X;
#  ex1 = attr.a == X;
#  ex2 = attr.${s} == X;
#  ex3 = attrVals ["c" "b"] attr == [ XXX ];
#  ex4 = attrValues attr == [ XXX ];
#  ex5 = builtins.intersectAttrs attr {a="b"; d=234; c="";} 
#    == { X = X; X = X;};
#  ex6 = removeAttrs attr ["b" "c"] == { XXX };
#  ex7 = ! attr ? a == XXX;
}
```

## راه حل

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  attr = {a="a"; b = 1; c = true;};
  s = "b";
in
{
  #replace all X, everything should evaluate to true
  ex0 = isAttrs attr;
  ex1 = attr.a == "a";
  ex2 = attr.${s} == 1;
  ex3 = attrVals ["c" "b"] attr == [true 1];
  ex4 = attrValues attr == ["a" 1 true];
  ex5 = builtins.intersectAttrs attr {a="b"; d=234; c="";} == { a = "b"; c="";};
  ex6 = removeAttrs attr ["b" "c"] == {a = "a";};
  ex7 = ! attr ? a == false;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=GQO1HUV0A9E&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=attrset/examples) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
