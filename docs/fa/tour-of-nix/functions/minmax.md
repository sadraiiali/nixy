# توابع: نخستین تابع شما!

> درس **۸** از ۳۵ · مسیر `functions/minmax`

کارهایی که باید انجام دهید:

* توابع `min` و `max` را با استفاده از ساختار `if () then X else Y` پیاده‌سازی کنید.

**نکته:** این توابع از قبل وجود دارند و از طریق `lib.min` و `lib.max` قابل دسترسی هستند (در این تمرین از `lib.min` و `lib.max` استفاده نکنید، بلکه آن‌ها را خودتان پیاده‌سازی کنید).
 
**آزمایش‌ها:** 

* اگر یک فراخوانی بازگشتی پایان‌ناپذیر به تابع `min` ایجاد کنید چه اتفاقی می‌افتد؟
* اکنون، به جای فراخوانی پیاده‌سازی `min` و `max` خودتان، از `lib.min` و `lib.max` استفاده کنید. 

  در واقع پرسش این است: برای استفاده از `lib` چه چیزی باید اضافه شود؟
* در نهایت مقایسه کنید: min/max با این آرگومان‌ها: ۹ و ۱-؛ چگونه می‌توانید کاری کنید که اعداد منفی هم به درست کار کنند؟

## کد شروع

```nix
let
  min = XX #modify these
  max = XX #two lines only
in
{
  ex0 = min 5 3;
  ex1 = max 9 4;
}
```

## راه حل

```nix
let
  min = x: y: if x < y then x else y;
  max = x: y: if x > y then x else y;
in
{
  ex0 = min 5 3;
  ex1 = max 9 4;
}
# make stdenv.lib available
# with import <nixpkgs> { };
# {
#   # finally make use of it
#   ex0 = stdenv.lib.min 9 (-1);
#   ex1 = stdenv.lib.max 9 (-1);
# }
# you need to use () precedence to not compute (9 -1) algebraic expression instead.
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=XD5si5Tz8QU&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=functions/minmax) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
