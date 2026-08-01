# سیستم نوع‌داده (Typing system)

> درس **۲۴** / ۳۵ · مسیر `types`

زبان Nix از نوع‌داده‌ی پویا (dynamic typing) استفاده می‌کند و توابع توکار (`builtin`) برای بررسی نوع یک `binding` وجود دارند.

**نکته:** از این توابع استفاده کنید: `isBool`، 
`isInt`، 
`isString`، 
`isNull`، 
`isList`، 
`isAttrs` و 
`isFunction`.

این کار را انجام دهید:

* از میان `ex00, ex01, ...` عبور کنید و با توجه به `type`، مقدار X را با `isBool` جایگزین کنید.
* `ex04` را اصلاح کنید، مشکل چیست؟

**نکته:** `()` می‌تواند یا یک `function` باشد یا اولویت (`precedence`) را مشخص کند.

همچنین نگاه کنید به <https://nixos.org/manual/nix/stable/language/values>.

## کد اولیه

```nix
with import <nixpkgs> {};
with lib;
{
  ex00 = isAttrs {};
  #ex01 = isX "a"; 
  #ex02 = isX (-3); 
  #ex03 = isX (x: x);
  #ex04 = isX (x:x);
  #ex05 = isX ("x");
  #ex06 = isX null; 
  #ex07 = isX (y: y+1);
  #ex08 = isX [({z}: z) (x: x)];
  #ex09 = isX {a=[];};
  #ex10 = isX -10; # oh, what is that?
}
```

## راه‌حل

```nix
with import <nixpkgs> {};
with lib;
{
  ex00 = isAttrs {};
  ex01 = isString "a"; 
  ex02 = isInt (-3); 
  ex03 = isFunction (x: x);
  ex04 = isString (x:x); # this is because of url parsing: foo = http://bar.com;
  ex05 = isString ("x");
  ex06 = isNull null; 
  ex07 = isFunction (y: y+1);
  ex08 = isList [({z}: z) (x: x)];
  ex09 = isAttrs {a=[];};
  ex10 = isInt (-10); # () were missing
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=EsbiR4uwywo&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=types) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
