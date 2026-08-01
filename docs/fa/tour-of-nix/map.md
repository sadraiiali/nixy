# نگاشت

> درس **27** از ۳۵ · مسیر `map`

تابعی به نام `builtins.map` وجود دارد.

این `map-function` به این آرگومان‌ها نیاز دارد: یک `function` (تابع) و یک `list` (فهرست).
این تابع، تابع داده‌شده را روی هر عنصر از فهرست داده‌شده ارزیابی می‌کند.

در این مثال، از آن برای ضرب کردن
هر عدد در یک فهرست در عدد دو استفاده شده‌است.

وظیفه شما:

* از تابع نگاشت استفاده کنید تا هر `string` (رشته) در **bar** را با "bar" گسترش دهید.

**نکته:** می‌توانید `Strings` را به هر شکلی که می‌خواهید تغییر دهید.
لازم نیست خروجی آن‌ها 'foobar' باشد (و نباید هم باشد).

## کد شروع

```nix
let
  bar = ["bar" "foo" "bla"];
  numbers = [1 2 3 4];
in
{
  #multiplies every number by 2
  example = map (n: n * 2) numbers; 
  #complete this
#  foobar = map ( XXX ) XXX;
}
```

## راه‌حل

```nix
let
  bar = ["bar" "foo" "bla"];
  numbers = [1 2 3 4];
in
{
  #multiplies every number by 2
  example = map (n: n * 2) numbers; 
  #complete this
  foobar = map (x: x + "bar") bar;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=4fp-7_yz07I&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گردش در Nix](https://nixcloud.io/tour/?id=map) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
