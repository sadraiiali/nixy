# سلام دنیا

> درس **۳** از ۳۵ · مسیر `introduction/helloworld`

یک مقدمه ساده بر `Strings` در Nix:

* عبارت `String` را به "Hello World" کامل کنید، تمام 'X'ها را با
صفات یا `Strings` جایگزین کنید.

## عبارت‌های Let

عبارت let از اجزای زیر تشکیل شده‌است:

    let <bindings> in <body>

اتصالات (bindings) مجموعه‌ای از تعاریف هستند که با نقطه‌ویرگول از هم جدا شده‌اند.

**نکته:** در Nix می‌توانید از سازه‌ی `let` برای اتصال یک `value` به یک
`attribute` و همچنین یک `function` استفاده کنید. سپس در `<body>` می‌توانید
به `bound values`، حتی چندین بار ارجاع دهید.

اطلاعات بیشتر در [Nix by example part1](https://medium.com/@MrJamesFisher/nix-by-example-a0063a1a4c55#8310) نوشته‌ی James Fisher.

## کد شروع

```nix
let 
  h = "Hello";
  w = "World";
in
{
  helloWorld = h + X + X;
}
```

## راه‌حل

```nix
let 
  h = "Hello";
  w = "World";
in
{
  helloWorld = h + " " + w;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=p0ZB03Br3lM&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=introduction/helloworld) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
