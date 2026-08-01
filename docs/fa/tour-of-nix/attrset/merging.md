# مجموعه ویژگی‌ها: ادغام

جوخه **۱۸** / ۳۵ · مسیر `attrset/merging`

از آنجا که برنامه‌نویسی در Nix سراسر دربارهٔ `attribute sets` است، مهم است
که بدانید چگونه می‌توان آن‌ها را با استفاده از عملگر `//` `merge` کرد.

    l = {a="A"; b="B";} // {a="aaa"};

ارزیابی خواهد شد به:

    l = {a="aaa"; b="B";};
    
زیرا `set` متأخر، صفات `set` متقدم را بازنویسی می‌کند.

اکنون:

* هر تمرین `ex00, ex01, ...` باید به همان مقداری ارزیابی شود که با آن مقایسه شده‌است، کافی است پس از زدن دکمهٔ «run» خروجی را ببینید.

## کد شروع

```nix
let
  x = { a="bananas"; b= "pineapples"; };
  y = { a="kakis"; c ="grapes"; };
  z = { a="raspberrys"; c= "oranges"; };

  func = {a, b, c ? "another secret ingredient"}: "A drink with: " + 
    a + ", " + b + " and " + c;
in
rec {
  ex00=func ( x );  
  # hit 'run', you need the output to solve this!
  #ex01=func (y // X );  
  #ex02=func (x // { X="lychees";});
  #ex03=func (X // x // z);
}
```

## راه حل

```nix
with import <nixpkgs> { };
let
  x = { a="bananas"; b= "pineapples"; };
  y = { a="kakis"; c ="grapes"; };
  z = { a="raspberrys"; c= "oranges"; };

  func = {a, b, c ? "another secret ingredient"}: "A drink with: " + 
    a + ", " + b + " and " + c;
in
rec {
  ex00=func (x);  
  ex01=func (y // x );  
  ex02=func (x // { c="lychees";});
  ex03=func (z // x // z);
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=55HXT8Xxh1Q&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=attrset/merging) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
