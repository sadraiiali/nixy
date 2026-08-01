# پیاده‌سازی مجدد: reverseList

> درس **۳۰** از ۳۵ · مسیر `reimplementation/reverselist`

از `fold` برای پیاده‌سازی تابع `reverseList` استفاده کنید.

**نکته:** شما عملاً تابع `lib.reverseList` را پیاده‌سازی می‌کنید.
تابع شما باید دقیقاً به همان شکل رفتار کند!

## کد شروع

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  reverseList = lib.fold XXX;
in
rec {
  example = lib.reverseList listOfNumbers;
  result = reverseList listOfNumbers;
}
```

## راه‌حل

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  reverseList = lib.fold (e: acc: acc ++ [ e ]) [];
in
rec {
  example = lib.reverseList listOfNumbers;
  result = reverseList listOfNumbers;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=LApNEuzt9Is&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=reimplementation/reverselist) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
