# پیاده‌سازی مجدد: catAttrs

> درس **34** / ۳۵ · مسیر `reimplementation/catAttrs`

تابع `catAttrs` را بنویسید.

 `catAttrs "a" [{a = 1;} {b = 0;} {a = 2;}]; => [ 1 2 ]`

مجموعه ویژگی‌هایی که شامل ویژگی نام‌برده نباشند، نادیده گرفته می‌شوند.

 **نکته:** می‌توانید از تابع توکار `concatLists` استفاده کنید.

 **نکته:** سمت راست عملگر `? operator` دارای همان سینتکس تخصیص در مجموعه ویژگی‌ها است (یعنی `{foo=42;}` و `{"foo" = 42;}`)

 **هشدار:** این کار دشوار است!

## کد شروع

```nix
with import <nixpkgs> { };
let
  list = [["a"] ["b"] ["c"]];
  
  attrList = [{a = 1;} {b = 0;} {a = 2;}];
  catAttrs = XXX
in
rec {
  example = builtins.concatLists list; #is [ "a" "b" "c" ]
  result = catAttrs "a" attrList; #should be [1 2] 
}
```

## راه‌حل

```nix
with import <nixpkgs> { };
let
  list = [["a"] ["b"] ["c"]];

  attrList = [{a = 1;} {b = 0;} {a = 2;}];
  catAttrs = name: List: builtins.concatLists (map (x: if x ? ${name} then [x.${name}] else []) List);
in
rec {
  example = builtins.concatLists list; #is [ "a" "b" "c" ]
  result = catAttrs "a" attrList; #should be [1 2] 
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=x57JiHKo7Ec&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=reimplementation/catAttrs) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
