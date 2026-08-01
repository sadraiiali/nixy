# تا کردن (Fold): مقدمه

> درس **29** / 35 · مسیر `fold/introduction`

### تمرین

وظیفه شما:

* `ex0`: از `fold` برای نوشتن تابعی استفاده کنید که تمام `strings`
با مقدار "a" را در یک `list` معنادار می‌شمارد

* `ex1`: از `fold` برای ضرب کردن هر عنصر در 2 و اضافه کردن [ 8 ] به آن استفاده کنید

### تابع fold (معروف به foldr)

`fold func init [x_1 x_2 ... x_n] == func x_1 (func x_2 ... (func x_n init))`

* `func`، یک `function` مانند `(el: container: container + el)`
* `init` به عنوان مقدار اولیه شروع

مثال‌های رشته‌ای:

* `lib.fold (el: c: el + c) "z" [ "a" "b" "c" ] => "abcz"`
* `lib.fold (el: c: c ++ [el]) [0] [1 2 3] => [ 0 3 2 1 ]`

### تابع foldl

`foldl func init [x_1 x_2 ... x_n] == func (... (func (func init x_1) x_2) ... x_n)`.

* `func`، یک `function` مانند `(container: el: container + el)`
* `init` به عنوان مقدار اولیه شروع

مثال‌های لیستی:

* `lib.foldl (c: el: el + c) "z" [ "a" "b" "c" ] => "cbaz"`
* `lib.foldl (c: el: c ++ [el]) [0] [1 2 3] => [ 0 1 2 3 ]`

**نکته:** به <https://nixos.org/manual/nixpkgs/stable/#chap-functions> مراجعه کنید، عبارت **lib.lists.foldr** را جستجو کنید

**نکته:** به <https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-repl> مراجعه کنید

## کد اولیه

```nix
with import <nixpkgs> { };
with lib;
let
  list = ["a" "b" "a" "c" "d" "a"];
  intList = [ 1 2 3 ];
  countA = XXX
  #mulB = XXX
in
rec {
  example = fold (x: y: x + y) "z" ["a" "b" "c"]; #is "abcz"
  ex0 = countA list; #should be 3
  #ex1 = mulB intList; #should be [ 2 4 6 8 ]
}
```

## راه‌حل

```nix
with import <nixpkgs> { };
with lib;
let
  list = ["a" "b" "a" "c" "d" "a"];
  intList = [ 1 2 3 ];
  countA = l: fold (el: c: if el == "a" then c + 1 else c) 0 l;
  mulB = l: fold (el: c: [(el * 2)] ++ c) [8] l;
in
rec {
  example = fold (x: y: x + y) "z" ["a" "b" "c"]; #is "abcz"
  ex0 = countA list; #should be 3
  ex1 = mulB intList; #should be [ 2 4 6 8 ]
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=TrUmPnKIKbI&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=fold/introduction) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
