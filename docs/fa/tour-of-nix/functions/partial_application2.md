# کاربرد جزئی II

> درس **14** / 35 · مسیر `functions/partial_application2`

همان‌طور که دیده‌ایم، توابع را می‌توان با یک `attribute set` فراخوانی کرد. این یک نمونه رایج دیگر از کاربرد جزئی است، بنابراین آن را حل کنید!

آرگومان‌های `attribute set` را کامل کنید:

  * مقدار A باید به 'HappyFunctionsAreCalled' ارزیابی شود.

## کد شروع

```nix
let
  arguments = {a="Happy"; b="Awesome";};

  func = {a, b}: {d, b, c}: a+b+c+d;
in
{
  A = func arguments XXX #only modify this line
}
```

## راه‌حل

```nix
let
  arguments = {a="Happy"; b="Awesome";};

  func = {a, b}: {d, b, c}: a+b+c+d;
in
{
  A = func arguments {d="Called"; b = "Functions"; c="Are";};
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=WaiIcgidSgs&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=functions/partial_application2) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
