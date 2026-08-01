# Idris2 {#sec-idris2}

هنگام توسعه با استفاده از Idris2، به‌طور پیش‌فرض کامپایلر Idris تنها حداقل کتابخانه‌های پشتیبانی را در محیط خود دارد. این بدان معناست که برای خواندن هیچ کتابخانه‌ای که به‌صورت سراسری نصب شده باشد، برای مثال در پوشه `$HOME`، تلاشی نخواهد کرد. روش توصیه‌شده برای استفاده از Idris2 این است که کامپایلر را در محیطی قرار دهید که این بسته‌ها را به ازای هر پروژه فراهم کند، برای مثال در یک devShell.

```nix
{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = [ (idris2.withPackages (p: [ p.idris2Api ])) ];
}
```
یا به عنوان جایگزین، اگر از Nix برای ساخت پروژه Idris2 استفاده می‌شود:

```nix
{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  inputsFrom = [ (pkgs.callPackage ./package.nix { }) ];
}
```

به طور پیش‌فرض، کامپایلر Idris2 ارائه‌شده توسط Nixpkgs بسته‌های نصب‌شده به صورت سراسری را نمی‌خواند و امکان نصب آن‌ها را نیز ندارد. اجرای `idris2 --

```nix
{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = [ (idris2.withPackages (p: [ p.idris2Api ])) ];
  shellHook = ''
    IDRIS2_PACKAGE_PATH="''${IDRIS2_PACKAGE_PATH:+$IDRIS2_PACKAGE_PATH}$HOME/.idris2"
  '';
}
```
قطعه‌کد زیر به Idris2 اجازه می‌دهد تا `idris2 --install` را با موفقیت اجرا کند:
```nix
{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = [ (idris2.withPackages (p: [ p.idris2Api ])) ];
  shellHook = ''
    IDRIS2_PREFIX="$HOME/.idris2"
  '';
}
```

- let's check dictionary: derivation -> derivation / اشتقاق ساخت)
Wait, glossary has:
derivation -> derivation / اشتقاق ساخت
derivations -> درایویشن‌ها

Let's check `derivation` in glossary:
`derivation` -> `
```nix
{ fetchFromGitHub, idris2Packages }:
let
  lspLibPkg = idris2Packages.buildIdris {
    ipkgName = "lsp-lib";
    src = fetchFromGitHub {
      owner = "idris-community";
      repo = "LSP-lib";
      rev = "main";
      hash = "sha256-EvSyMCVyiy9jDZMkXQmtwwMoLaem1GsKVFqSGNNHHmY=";
    };
    idrisLibraries = [ ];
  };
in
lspLibPkg.library { withSource = true; }
```

موارد بالا به یک derivation با نتایج کتابخانه نصب‌شده (به همراه کد منبع) منجر می‌شود.

یک نمونه کمی پیچیده‌تر از یک فایل اجرایی کاملاً بسته‌بندی‌شده، [`idris2-lsp`](https://github.com/idris-community/idris2-lsp) است که یک سرور زبان Idris2 بوده و از `LSP-lib` ذکرشده در بالا استفاده می‌کند.
```nix
{
  callPackage,
  fetchFromGitHub,
  idris2Packages,
}:

# Assuming the previous example lives in `lsp-lib.nix`:
let
  lspLib = callPackage ./lsp-lib.nix { };
  inherit (idris2Packages) idris2Api;
  lspPkg = idris2Packages.buildIdris {
    ipkgName = "idris2-lsp";
    src = fetchFromGitHub {
      owner = "idris-community";
      repo = "idris2-lsp";
      rev = "main";
      hash = "sha256-vQTzEltkx7uelDtXOHc6QRWZ4cSlhhm5ziOqWA+aujk=";
    };
    idrisLibraries = [
      idris2Api
      lspLib
    ];
  };
in
lspPkg.executable
```

مثال بالا از مقدار پیش‌فرض `withSource = false` برای `idris2Api` استفاده می‌کند، اما می‌توان آن را تغییر داد تا به جای آن با پاس دادن `(id

```nix
{
  idris2,
  devShell,
}:
let
  myIdris = idris2.withPackages (p: [ p.idris2Api ]);
in
devShell {
  packages = [ myIdris ];
}
```

این مسیر جستجو از مسیری که از قبل در محیط کاربر وجود دارد گسترش می‌یابد.
