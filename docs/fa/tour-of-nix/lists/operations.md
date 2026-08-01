# فهرست‌ها

> درس **20** / 35 · مسیر `lists/operations`

برای یادگیری نحو پایه، هر XX را در مجموعه ویژگی با مقادیر موجود در محدوده let جایگزین کنید.

این کار را انجام دهید:

 * هر تمرین باید به true ارزیابی شود.

## کد اولیه

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  list = [2 "4" true false {a = 27;} false 3];
  f = x: isString x;
  s = "foobar";
in
{
  #replace all X, everything should evaluate to true
  ex00 = isList X;
#  ex01 = elemAt list 2 == X;
#  ex02 = length list == X;
#  ex03 = last list == X;
#  ex04 = filter f list == [ XX ];
#  ex05 = head list == X;
#  ex06 = tail list == [ XXX ];
#  ex07 = remove true list == [ XXX ];
#  ex08 = toList s == [ XXX ];
#  ex09 = take 3 list == [ XXX ];
#  ex10 = drop 4 list == [ XXX ];
#  ex11 = unique list == [ XXX ];
#  ex12 = list ++ ["x" "y"] == [ XXX ];
}
```

## راه‌حل

```nix
with import <nixpkgs> { };
with stdenv.lib;
let
  list = [2 "4" true false {a = 27;} false 3];
  f = x: isString x;
  s = "foobar";
in
{
  #replace all X, everything should evaluate to true
  ex00 = isList list;
  ex01 = elemAt list 2 == true;
  ex02 = length list == 7;
  ex03 = last list == 3;
  ex04 = filter f list == ["4"];
  ex05 = head list == 2;
  ex06 = tail list == ["4" true false {a = 27;} false 3];
  ex07 = remove true list == [2 "4" false {a = 27;} false 3];
  ex08 = toList s == [s];
  ex09 = take 3 list == [2 "4" true];
  ex10 = drop 4 list == [{a = 27;} false 3];
  ex11 = unique list == [2 "4" true false {a = 27;} 3];
  ex12 = list ++ ["x" "y"] == [2 "4" true false {a = 27;} false 3 "x" "y"];
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=yUfMxGs1AZQ&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=lists/operations) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
