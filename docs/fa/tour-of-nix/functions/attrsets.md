# توابع: آرگومان‌های مجموعه‌های ویژگی

> درس **۹** از ۳۵ · مسیر `functions/attrsets`

هنگام ارسال یک `attribute set` به یک `function`، می‌توانید مقادیر پیش‌فرضی را تنظیم کنید.

با انجام این کار، می‌توان تابع را بدون آن پارامتر فراخوانی کرد و آن را اختیاری ساخت.

**نکته:** یک مقدار پیش‌فرض با علامت '؟' تعریف می‌شود.

اکنون:

* `function` به نام `func` را به گونه‌ای تغییر دهید که **foobar** به عنوان **'foobar'** ارزیابی شود.

## کد اولیه

```nix
let
  f = "f";
  o = "o";
  b = "b";
  func = {a ? f, b , c }: a+b+c; #only modify this line!
in
rec {
  foo = func {b="o"; c=o;}; #must evaluate to "foo"
  bar = func {a=b; c="r";}; #must evaluate to "bar"
  foobar = func {a=foo;b=bar;}; #must evaluate to "foobar"
}
```

## راه‌حل

```nix
let
  f = "f";
  o = "o";
  b = "b";
  func = {a ? f, b ? "a", c ? ""}: a+b+c; #Only modify this line! 
in
rec {
  foo = func {b="o"; c=o;}; #should be foo
  bar = func {a=b; c="r";}; #should be bar
  foobar = func {a=foo;b=bar;}; #should be foobar
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=4Cfk41ylC2E&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=functions/attrsets) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
