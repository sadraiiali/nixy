(automatic-direnv)=
# فعال‌سازی خودکار محیط با `direnv`

به‌جای فعال‌سازی دستی محیط برای هر پروژه، می‌توانید هر زمان که وارد پوشه پروژه می‌شوید یا فایل `shell.nix` درون آن را تغییر می‌دهید، یک [محیط‌های اعلامی و قابل بازتولید](declarative-reproducible-envs) را مجدداً بارگیری کنید.

1. [فراهم کردن امکان استفاده از nix-direnv](https://github.com/nix-community/nix-direnv)
2. [متصل کردن آن به شل خود](https://direnv.net/docs/hook.html)

برای مثال، یک فایل `shell.nix` با محتوای زیر بنویسید:

```nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    hello
  ];
}
```

از پوشه سطح بالا (top-level directory) پروژه خود، دستور زیر را اجرا کنید:

```shell-session
$ echo "use nix" > .envrc && direnv allow
```

دفعهٔ بعدی که ترمینال خود را باز کرده و وارد پوشهٔ سطح بالای پروژه خود شوید، `direnv` به طور خودکار شل تعریف‌شده در `shell.nix` را اجرا خواهد کرد.

```shell-session
$ cd myproject
$ which hello
/nix/store/1gxz5nfzfnhyxjdyzi04r86sh61y4i00-hello-2.12.1/bin/hello
```

ابزار `direnv` همچنین تغییرات فایل `shell.nix` را بررسی خواهد کرد.

افزودنی زیر را اعمال کنید:

```diff
 let
   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
   pkgs = import nixpkgs { config = {}; overlays = []; };
 in

 pkgs.mkShellNoCC {
   packages = with pkgs; [
     hello
   ];
+
+  shellHook = ''
+    hello
+  '';
 }
```

محیط در حال اجرا باید پس از اولین تعامل (اجرای هر دستور یا فشار دادن کلید `Enter`) خودش را مجدداً بارگذاری کند.

```shell-session
Hello, world!
```
