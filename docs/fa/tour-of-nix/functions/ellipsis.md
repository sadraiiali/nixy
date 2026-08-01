# توابع: الگوی @

> درس **10** / 35 · مسیر `functions/ellipsis`

## سه نقطه (Ellipsis)

همان‌طور که دیده‌ایم، توابع را می‌توان با یک `مجموعه ویژگی` فراخوانی کرد.
این `مجموعه ویژگی` باید شامل تمام `آرگومان‌های تابع` مورد نیاز باشد.

با این حال، چنین `مجموعه ویژگی` می‌تواند شامل صفات اضافی نیز باشد، اما باید `...` را به شکل زیر اضافه کنید:

    func2 = args@{a, b, c, ...}: a+b+c+args.d;

**نکته:** به `...` اصطلاحاً سه نقطه (ellipsis) گفته می‌شود.

## الگوی @

درون یک تابع، می‌توان به این `صفات` با استفاده از الگوی `@` دسترسی پیدا کرد.

اکنون `مجموعه ویژگی` آرگومان‌ها را کامل کنید:

  * **foo** باید به 'foo' ارزیابی شود
  * **foobar** باید به 'foobar' ارزیابی شود

## کد شروع

```nix
let
  arguments = {a="f"; b="o"; c=X; d=X;}; #only modify this line
  func = {a, b, c, ...}: a+b+c; 
  func2 = args@{a, b, c, ...}: a+b+c+args.d;
in
{
  #the argument d is not used 
  foo = func arguments;
  #now the argument d is used
  foobar = func2 arguments;
}
```

## راه‌حل

```nix
let
  arguments = {a="f"; b="o"; c="o"; d="bar";}; #only modify this line

  func = {a, b, c, ...}: a+b+c; 
  func2 = args@{a, b, c, ...}: a+b+c+args.d;
in
{
  #the argument d is not used 
  foo = func arguments;
  #now the argument d is used
  foobar = func2 arguments;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=4HE5hx8E_QA&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=functions/ellipsis) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
