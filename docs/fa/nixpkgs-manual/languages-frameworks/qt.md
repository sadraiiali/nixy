# Qt {#sec-language-qt}

نوشتن عبارت‌های Nix برای کتابخانه‌ها و برنامه‌های Qt تا حد زیادی مشابه سایر نرم‌افزارهای C++ است.
این بخش فرض می‌کند که شما

```nix
{ stdenv, qt6 }:

stdenv.mkDerivation {
  pname = "myapp";
  version = "1.0";

  buildInputs = [ qt6.qtbase ];
  nativeBuildInputs = [ qt6.wrapQtAppsHook ];
}
```

در مورد Qt 5 نیز صدق می‌کند که در آن کتابخانه‌ها و ابزارها زیر `libsForQt5` قرار دارند.

هر بسته Qt باید `wrapQtAppsHook` را در `nativeBuildInputs`

```nix
{ stdenv, qt6 }:

stdenv.mkDerivation {
  # ...
  nativeBuildInputs = [ qt6.wrapQtAppsHook ];
  qtWrapperArgs = [ "--prefix PATH : /path/to/bin" ];
}
```

این ورودی‌ها به عنوان آرگومان به [wrapProgram](#fun-wrapProgram) پاس داده می‌شوند.

اگر به کنترل بیشتری بر فرآیند ایجاد wrapper نیاز دارید، `dontWrap

```nix
{
  stdenv,
  lib,
  wrapQtAppsHook,
}:

stdenv.mkDerivation {
  # ...
  nativeBuildInputs = [ wrapQtAppsHook ];
  dontWrapQtApps = true;
  preFixup = ''
    wrapQtApp "$out/bin/myapp" --prefix PATH : /path/to/bin
  '';
}
```

wrap نمی‌شوند، بنابراین همان‌طور که قبلاً اشاره شد باید آن‌ها را به‌صورت دستی wrap کنید.
یک نمونه از مواردی که همیشه لازم است این
