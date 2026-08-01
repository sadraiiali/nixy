# مجموعه ویژگی‌ها: مثال‌های ۲

> درس **۱۶** از ۳۵ · مسیر `attrset/examples2`

باعث شوید `ex0` و `ex1` به مقدار درست ارزیابی شوند.

## کد اولیه

```nix
let
  list = [ { name = "foo"; value = 123; }
           { name = "bar"; value = 456; } ];
  string = ''{"x": [1, 2, 3], "y": null}'';
in 
{
  ex0 = builtins.listToAttrs list == { XXX };
  ex1 = builtins.fromJSON string == { XXX };
}
```

## راه‌حل

```nix
let
  list = [ { name = "foo"; value = 123; }
           { name = "bar"; value = 456; } ];
  string = ''{"x": [1, 2, 3], "y": null}'';
in 
{
  ex0 = builtins.listToAttrs list == {foo = 123; bar = 456;};
  ex1 = builtins.fromJSON string == {x = [1 2 3]; y = null;};
}
```

## ویدیو

[YouTube](https://www.youtube.com/watch?v=GQO1HUV0A9E&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [A tour of Nix](https://nixcloud.io/tour/?id=attrset/examples2) · [GitHub](https://github.com/nixcloud/tour_of_nix)
