# pkgs.mkShell {#sec-pkgs-mkShell}

`pkgs.mkShell` یک `stdenv.mkDerivation` تخصصی‌شده است که هنگام استفاده با `nix-shell` (یا `nix develop`) برخی تکرارها را کاهش می‌دهد.

## نحوه استفاده {#sec-pkgs-mkShell-usage}

در ادامه یک نمونه استفاده متداول آورده شده است:

```nix
{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = [ pkgs.gnumake ];

  inputsFrom = [
    pkgs.hello
    pkgs.gnutar
  ];

  shellHook = ''
    export DEBUG=1
  '';
}
```

## صفات {#sec-pkgs-mkShell-attributes}

* `name` (پیش‌فرض: `nix-shell`). نام derivation را تنظیم می‌کند.
* `packages` (پیش‌فرض: `[]`). بسته‌های قابل اجرا را به محیط `nix-shell` اضافه می‌کند.
* `inputsFrom` (پیش‌فرض: `[]`). وابستگی‌های ساخت درایویشن‌های فهرست‌شده را به محیط `nix-shell` اضافه می‌کند.
* `shellHook` (پیش‌فرض: `""`). دستورات Bash که توسط `nix-shell` اجرا می‌شوند.

... تمام صفات `stdenv.mkDerivation`.

## گونه‌ها {#sec-pkgs-mkShell-variants}

`pkgs.mkShellNoCC` گونه‌ای است که به جای `stdenv` از `stdenvNoCC` به عنوان محیط پایه استفاده می‌کند. این ویژگی زمانی مفید است که به کامپایلر C در محیط شل نیازی نباشد.

## ساخت شل {#sec-pkgs-mkShell-building}

خروجی این derivation شامل یک فایل متنی خواهد بود که حاوی ارجاعی به تمام ورودی‌های ساخت است. این موضوع در ادغام مداوم (CI) کاربرد دارد، جایی که می‌خواهیم اطمینان حاصل کنیم هر derivation و وابستگی‌های آن به‌درستی ساخته می‌شوند؛ یا هنگام ایجاد یک ریشه GC تا وابستگی‌های ساخت جمع‌آوری زباله (garbage collection) نشوند.
