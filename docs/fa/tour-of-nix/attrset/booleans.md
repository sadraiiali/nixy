# مجموعه‌های ویژگی و مقادیر بولین

> درس **۱۹** از ۳۵ · مسیر `attrset/booleans`

برای یادگیری نحو پایه نیکس، هر مقدار XX را در مجموعه ویژگی با مقادیری از صفت `attrSet` که در محدوده let تعریف شده است، جایگزین کنید.

هر تمرین مجزا (`ex00, ex01, ...`) باید به `true` ارزیابی شود. 

**نکته:** علامت `#` را حذف کنید تا با پیشروی در تمرین‌ها، آن‌ها را از حالت کامنت خارج کنید.

برای جزئیات بیشتر درباره `attribute sets` به [مستندات نیکس](https://nixos.org/manual/nix/stable/language/values#attribute-set) مراجعه کنید.

## کد اولیه

```nix
let
  attrSet = {x = "a"; y = "b"; b = {t = true; f = false;};};
  attrSet.c = 1;
  attrSet.d = null;
  attrSet.e.f = "g";
in
rec {
  #boolean
  ex0 = attrSet.b.t;
  #equal
#  ex01 =  "a" == attrSet.XX; 
  #unequal 
#  ex02 = !("b" != attrSet.XX );
  #and/or/neg
#  ex03 = ex01 && !ex02 || ! attrSet.XX;
  #implication
#  ex04 = true -> attrSet.XX;
#  ex05 = attrSet.XX ? e;
}
```

## راه‌حل

```nix
let
  attrSet = {x = "a"; y = "b"; b = {t = true; f = false;};};
  attrSet.c = 1;
  attrSet.d = null;
  attrSet.e.f = "g";
in
rec {
  ex0 = attrSet.b.t;
  #equal
  ex01 = "a" == attrSet.x;
  #unequal 
  ex02 = !("b" != attrSet.y);
  #and/or/neg
  ex03 = ex01 && !ex02 || !attrSet.b.f;
  #implication
  ex04 = true -> attrSet.b.t;
  #contains attribute
  ex05 = attrSet ? e;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=BZACbPJg9Oo&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=attrset/booleans) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
