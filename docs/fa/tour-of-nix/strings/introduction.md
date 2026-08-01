# رشته‌ها

> درس **4** / 35 · مسیر `strings/introduction`

نیکس همچنین می‌تواند `Strings` را با استفاده از `${attribute}` درون‌گذاری کند که در آن `attribute` از یک محدوده let ارجاع داده می‌شود.

 * تمرین‌های ex0، ex1 و ex2 را طوری کامل کنید که هر کدام عبارت 'Hello World' را چاپ کنند.

## کد شروع

```nix
let 
  h = "Hello";
in
{
  ex0 = "${h} X";
  ex1 = "${h + X + X}";
  ex2 = ''${h + X + X}'';
}
```

## راه‌حل

```nix
let 
  h = "Hello";
in
{
  ex0 = "${h} World";
  ex1 = "${h + " " + "World"}";
  ex2 = ''${h + " " + "World"}'';
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=DX97PJpQLbI&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=strings/introduction) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
