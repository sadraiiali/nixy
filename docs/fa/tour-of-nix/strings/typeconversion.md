# تبدیل عدد صحیح به رشته

> درس **۶** از ۳۵ · مسیر `strings/typeconversion`

درج `Strings` با استفاده از الگوی `${attribute}` به خوبی با `Strings` کار می‌کند. اما `${}` کارهای بیشتری می‌تواند انجام دهد. حتی می‌توانید توابع را در آن اجرا کنید.

از این قابلیت و تابع توکار `toString` استفاده کنید تا کد کار کند.

**نکته:** همچنین به <https://noogle.dev/> مراجعه کنید.

**نکته:** توابع توکار بیشتر را می‌توانید در [راهنمای Nix](https://nixos.org/manual/nix/stable/expressions/builtins.html#built-in-functions) پیدا کنید.

## کد اولیه

```nix
let 
  h = "Strings";
  v = 4;
in
{
  helloWorld = "${h} ${v} the win!";
}
```

## راه‌حل

```nix
let 
  h = "Strings";
  v = 4;
in
{
  helloWorld = "${h} ${toString v} the win!";
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=fyhPbWVCv_g&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=strings/typeconversion) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
