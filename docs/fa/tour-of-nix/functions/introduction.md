# توابع: مقدمه

> درس **۷** از ۳۵ · مسیر `functions/introduction`

در ادامه قصد داریم نگاهی به `functions` و نحوه تعریف و فراخوانی آن‌ها بیندازیم. فراموش نکنید که بین آرگومان‌های توابعی که می‌نویسید از فاصله (Space) استفاده کنید!

اکنون:

* یک `function` بنویسید که ۳ `Strings` را دریافت کرده و آن‌ها را با یکدیگر ترکیب کند.

**نکته:** الحاق رشته‌ها را می‌توان با استفاده از عملگر '+' انجام داد.

**نکته:** درباره نوشتن توابع در <https://nixos.org/manual/nix/stable/language/constructs#functions> مطالعه کنید.

**نکته:** توابع توکاری وجود دارند که همیشه می‌توانید از آن‌ها استفاده کنید؛ به <https://nixos.org/manual/nix/stable/language/builtins> مراجعه کنید.

## کد شروع

```nix
let
  f = "f";
  o = "o";
  func = a: b: c: XXX; 
in
{
  foo = func f o "o";
}
```

## راهحل

```nix
let
  f = "f";
  o = "o";
  func = a: b: c: a+b+c; 
in
{
  foo = func f o "o";
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=rKWJFfBr7cg&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=functions/introduction) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
