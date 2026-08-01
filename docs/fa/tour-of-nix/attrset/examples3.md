# مجموعه ویژگی‌ها: مثال‌های ۳

> درس **۱۷** از ۳۵ · مسیر `attrset/examples3`

برای یادگیری نحو پایه، هر مقدار XX را در `rec scope` با مقادیر موجود در `let scope` جایگزین کنید.

اکنون:

* تمرین باید به true ارزیابی شود.

## کد اولیه

```nix
let
  attrSetBonus = {f = {add = (x: y: x + y);
                       mul = (x: y: x * y);};
                  n = {one = 1; two = 2;};};
in
rec {
  #Bonus: use only the attrSetBonus to solve this one
  exBonus = 5 == XX ( XX XX XX ) XX;
}
```

## راه حل

```nix
let
  attrSetBonus = {f = {add = (x: y: x + y);
                       mul = (x: y: x * y);};
                  n = {one = 1; two = 2;};};
in
rec {
  #Bonus: use only the attrSetBonus to solve this one
  exBonus = with attrSetBonus; 5 == f.add (f.mul n.two n.two) n.one ;
}
```

## ویدیو

[YouTube](https://www.youtube.com/watch?v=IbRyAUZ7aKw&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [A tour of Nix](https://nixcloud.io/tour/?id=attrset/examples3) · [GitHub](https://github.com/nixcloud/tour_of_nix)
