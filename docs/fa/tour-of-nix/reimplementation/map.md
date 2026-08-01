# تاشو (Fold): پیاده‌سازی 'map'

> درس **31** از 35 · مسیر `reimplementation/map`

از `fold` برای نوشتن تابع `map` خود استفاده کنید.

**نکته:** آن خطای کوچک عمدی است، آن را اصلاح کنید!

## کد شروع

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  myMap = XXX fold XXX; 
in
rec {
  #your map should create the same result as the standard map function
  example = map (x: builtins.div x 2) listOfNumbers; 
  result = myMap (x: builtins.div x 2) listOfNumbers;
}
```

## راه حل

```nix
with import <nixpkgs> { };
let
  listOfNumbers = [2 4 6 9 27];
  myMap = op: list: lib.fold (x: y: [(op x)] ++ y) [] list; 
in
rec {
  #your map should create the same result as the standard map function
  example = map (x: builtins.div x 2) listOfNumbers; 
  result = myMap (x: builtins.div x 2) listOfNumbers;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=RZuWUn_QHnQ&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=reimplementation/map) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
