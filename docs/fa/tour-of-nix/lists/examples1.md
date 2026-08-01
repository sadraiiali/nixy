# فهرست‌ها و مجموعه‌های ویژگی

> درس **21** / 35 · مسیر `lists/examples1`

برای یادگیری نحو پایه، هر XX را در مجموعه ویژگی با مقادیر موجود در حوزه (scope) let جایگزین کنید.

هر تمرین باید به مقدار `true` ارزیابی شود.

## کد شروع

```nix
let
  attrSet = {x = "a"; y = "b"; b = {t = true; f = false;};};
  attrSet.c = 1;
  attrSet.d = 2;
  attrSet.e.f = "g";

  list1 = [attrSet.c attrSet.d];
  list2 = [attrSet.x attrSet.y];

in
{
  #List concatenation.
  ex0 = ["a" "b" 1 2] == XX ++ XX;
}
```

## راه‌حل

```nix
let
  attrSet = {x = "a"; y = "b"; b = {t = true; f = false;};};
  attrSet.c = 1;
  attrSet.d = 2;
  attrSet.e.f = "g";

  list1 = [attrSet.c attrSet.d];
  list2 = [attrSet.x attrSet.y];

in
{
  #List concatenation.
  ex0 = ["a" "b" 1 2] == list2 ++ list1;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=Qg4tM_ebCoU&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=lists/examples1) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
