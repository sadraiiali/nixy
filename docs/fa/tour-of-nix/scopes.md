# محدوده‌بندی صفت‌ها در let/with

> درس **23** / 35 · مسیر `scopes`

این پرسش درباره‌ی محدوده‌ها (scopes) است. ساختار `let` همانند `with` به الزام صفت‌ها (attributes) می‌پردازد.

پرسش: مقدار `res` به چه چیزی اختصاص می‌یابد و چرا؟

راه حل: کد منبع مرتبط با دکمه‌ی «راهنما» را ببینید.

## کد اولیه

```nix
let
  x = 123;
  as = { a = "foo"; b = "bar"; x="234"; };
 
in with as; {
 res = x; # what value is res bound to?
}
```

## راه حل

```nix
{ res = 123; }
# In Nix, `let` bindings have HIGHER precedence than `with` bindings.
# Even though `as` contains `x = "234"` and we use `with as`, 
# the `x = 123` from the let expression takes priority.
#
# Scoping precedence (highest to lowest):
# 1. let bindings (explicit definitions)
# 2. function arguments
# 3. with bindings (implicit scope imports)
#
# This design is intentional to prevent `with` from accidentally shadowing
# your explicitly defined variables, which would be surprising and error-prone.
#
#See this example, why it makes sense:
#{ config, lib, pkgs, ... }:
#
#let
#  vim = pkgs.stdenv.mkDerivation { 
#     name = "vim-hack";
#     unpackPhase = "true"; 
#     installPhase = ''
#       mkdir -p $out/bin; 
#       echo '#!/bin/sh
#       echo hi' > $out/bin/vim1; 
#       chmod u+x $out/bin/vim1
#     '';
#     };
#in
#
#{
#  environment.systemPackages = with pkgs; [ vim ];
#  # Here, `vim` refers to the custom vim from `let`, NOT pkgs.vim
#  # This is safe and predictable: your explicit definitions always win
#}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=LPU7-hIGQQ0&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در نیکس](https://nixcloud.io/tour/?id=scopes) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
