# ادعاها (Assertions)

> درس **25** از 35 · مسیر `assertions`

`Assertions` معمولاً برای بررسی برقرار بودن شرایط یا الزامات خاصی روی ویژگی‌ها و وابستگی‌ها یا میان آن‌ها استفاده می‌شوند. 

همچنین ببینید: <https://nixos.org/manual/nix/stable/language/constructs#assertions>.

### شکل ۱

    assert e1 || abort "e1 is true, so we abort with this error message";
    
    
که در آن `e1` عبارتی است که باید به یک مقدار `boolean` ارزیابی شود. 
اگر مقدار آن `true` ارزیابی شود، فراخوان `abort` اجرا خواهد شد.

### شکل ۲

    assert e1; e2

که در آن `e1` عبارتی است که باید به یک مقدار `boolean` ارزیابی شود. 
اگر مقدار آن `true` ارزیابی شود، `e2` بازگردانده می‌شود؛ در غیر این صورت، ارزیابی عبارت متوقف شده و یک ردپا (backtrace) چاپ می‌شود.

## کد شروع

```nix
with import <nixpkgs> {};
let
  func = x: y: assert (x==2) || abort "x has to be 2 or it won't work!"; x + y;
  n = "-5"; # only modify this line
in

assert (lib.isInt n) || abort "Type error since supplied argument is no int!";

rec {
  ex00 = func (n+3) 3;
}
```

## راه حل

```nix
with import <nixpkgs> {};
let
  func = x: y: assert (x==2) || abort "x has to be 2 or it won't work!"; x + y;
  n = -1;
in

assert (lib.isInt n) || abort "Type error since supplied argument is no int!";
assert (lib.isInt n) -> (n > -5);

rec {
  ex00 = func (n+3) 3;
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=g-qDaCr2rwQ&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=assertions) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
