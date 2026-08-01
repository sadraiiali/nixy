# اعمال جزئی (Partial application)

> درس **۱۳** / ۳۵ · مسیر `functions/partial_application`

**اعمال جزئی**: تابعی که تابع دیگری را برمی‌گرداند که ممکن است خودش تابع دیگری را برگرداند، اما هر تابع بازگشتی می‌تواند چندین پارامتر را بپذیرد.

بیایید نگاهی به `functions` و نحوه تعریف و فراخوانی آن‌ها بیندازیم:

* هر سوال را حل کنید: `ex00, ex01, ...` فقط با تغییر دادن X به یک
`value` از نوع `Int`

**نکته:** اگر پس از «اجرا» عبارت `ex03 = <LAMBDA>;` را دیدید، این یعنی
`ex03` به یک `function` متصل است.

## کد شروع

```nix
let
  b = 1;
  fu0 = (x: x);
  fu1 = (x: y: x + y) 4;
  fu2 = (x: y: (2 * x) + y);
in
rec {
  ex00 = fu0 X;     # must return 4
#  ex01 = (fu1) X;   # must return 5
#  ex02 = (fu2 X ) X; # must return 7
#  ex03 = (fu2 X );   # must return <LAMBDA>s
#  ex04 = ex03 X;    # must return 7
#  ex05 = (n: x: (fu2 x n)) X X; # must return 7
}
```

## راه‌حل

```nix
let
  b = 1;
  fu0 = (x: x);
  fu1 = (x: y: x + y) 4;
  fu2 = (x: y: (2 * x) + y);
in
rec {
  ex00 = fu0 4;     # must return 4
  ex01 = (fu1) 1;   # must return 5
  ex02 = (fu2 2) 3; # must return 7
  ex03 = (fu2 3);   # must return <LAMBDA>
  ex04 = ex03 1;    # must return 7
  ex05 = (n: x: (fu2 x n)) 3 2; # must return 7
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=ITaAmTWGQeE&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=functions/partial_application) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
