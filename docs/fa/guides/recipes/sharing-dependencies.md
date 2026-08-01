(sharing-dependencies)=
# وابستگی‌ها در شل توسعه

هنگام [بسته‌بندی نرم‌افزار در `default.nix`](packaging-tutorial)، احتمالاً می‌خواهید یک [محیط توسعه در `shell.nix`](declarative-reproducible-envs) داشته باشید تا بتوانید به راحتی با `nix-shell` یا [به‌طور خودکار با `direnv`](./direnv) وارد آن شوید.

چگونه می‌توان وابستگی‌های بسته را در `default.nix` با محیط توسعه در `shell.nix` به اشتراک گذاشت؟

## خلاصه

از [صفت `inputsFrom` در `pkgs.mkShellNoCC`](https://nixos.org/manual/nixpkgs/stable/#sec-pkgs-mkShell-attributes) استفاده کنید:

```nix
# default.nix
let
  pkgs = import <nixpkgs> {};
  myPackage = pkgs.callPackage ./package.nix {};
in
{
  inherit myPackage;
  shell = pkgs.mkShellNoCC {
    inputsFrom = [ myPackage ];
  };
}
```

صفت `shell` را در `shell.nix` درون‌ریزی کنید:

```nix
# shell.nix
(import ./.).shell
```

## مثال کامل

فرض کنید بستهٔ شما در `package.nix` تعریف شده‌است:

```nix
# package.nix
{ cowsay, runCommand }:
runCommand "cowsay-output" { buildInputs = [ cowsay ]; } ''
  cowsay Hello, Nix! > $out
''
```

در این مثال، `cowsay` با استفاده از `buildInputs` به عنوان یک وابستگی ساخت اعلام می‌شود.

علاوه بر این، فرض کنید پروژه شما در `default.nix` تعریف شده‌است:

```nix
# default.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
{
  myPackage = pkgs.callPackage ./package.nix {};
}
```

یک صفت (attribute) برای تعیین یک محیط به `default.nix` اضافه کنید:

```diff
 let
   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
   pkgs = import nixpkgs { config = {}; overlays = []; };
 in
 {
   myPackage = pkgs.callPackage ./package.nix {};
+  shell = pkgs.mkShellNoCC {
+  };
 }
```

صفت `myPackage` را به درون اتصال `let` منتقل کنید تا امکان استفاده مجدد از آن فراهم شود.
سپس وابستگی‌های بسته را با استفاده از [`inputsFrom`](https://nixos.org/manual/nixpkgs/stable/#sec-pkgs-mkShell-attributes) وارد محیط کنید:

```diff
 let
   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
   pkgs = import nixpkgs { config = {}; overlays = []; };
+  myPackage = pkgs.callPackage ./package.nix {};
 in
 {
-  myPackage = pkgs.callPackage ./package.nix {};
+  inherit myPackage;
   shell = pkgs.mkShellNoCC {
+    inputsFrom = [ myPackage ];
   };
 }
```

در نهایت، صفت `shell` را در فایل `shell.nix` درون‌ریزی کنید:

```nix
# shell.nix
(import ./.).shell
```

محیط توسعه را بررسی کنید، این محیط حاوی وابستگی ساخت `cowsay` است:

```console
$ nix-shell --pure
[nix-shell]$ cowsay shell.nix
```

## گام‌های بعدی

- [](pinning-nixpkgs)
- [](./direnv)
- [](python-dev-environment)
- [](packaging-tutorial)
