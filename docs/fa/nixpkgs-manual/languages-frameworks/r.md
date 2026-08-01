# R {#r}

## نصب {#installation}

با افزودن قطعه‌کد زیر به فایل `$HOME/.config/nixpkgs/config.nix` خود، یک محیط برای R تعریف کنید که شامل تمام کتابخانه‌های مورد استفاده شما باشد:

```nix
{
  packageOverrides =
    super:
    let
      self = super.pkgs;
    in
    {

      rEnv = super.rWrapper.override {
        packages = with self.rPackages; [
          devtools
          ggplot2
          reshape2
          yaml
          optparse
        ];
      };
    };
}
```

سپس می‌توانید از `nix-env -f "<nixpkgs>" -iA rEnv` برای نصب آن در پروفایل کاربر خود استفاده کنید. مجموعهٔ کتابخانه‌های در دسترس را می‌توان با اجرای دستور `nix-env -f "<nixpkgs>" -qaP -A rPackages` پیدا کرد. ستون اول از آن خروجی، همان نامی است که باید به `rWrapper` در قطعه

```nix
with import <nixpkgs> { };
{
  myProject = stdenv.mkDerivation {
    name = "myProject";
    version = "1";
    src = if lib.inNixShell then null else nix;

    buildInputs = with rPackages; [
      R
      ggplot2
      knitr
    ];
  };
}
```
و سپس `nix-shell .` را اجرا کنید تا وارد شلی شوید که این بسته‌ها در آن در دسترس هستند.

## RStudio {#rstudio}

برنامه RStudio از یک مجموعه استاندارد از بسته‌ها استفاده می‌کند و هرگونه محیط سفارشی R یا بسته‌های نصب‌شده‌ای را که ممکن است داشته باشید نادیده می‌گیرد. برای ایجاد یک محیط سفارشی، `rstudioWrapper` را ببینید که عملکردی مشابه `rWrapper` دارد:

```nix
{
  packageOverrides =
    super:
    let
      self = super.pkgs;
    in
    {

      rstudioEnv = super.rstudioWrapper.override {
        packages = with self.rPackages; [
          dplyr
          ggplot2
          reshape2
        ];
      };
    };
}
```

سپس مانند بالا، `nix-env -f "<nixpkgs>" -iA rstudioEnv` این را در پروفایل کاربر شما نصب خواهد کرد.

همچنین می‌توانید یک `shell.nix` خودمختار بدون نیاز به تغییر هیچ فایل پیکربندی ایجاد کنید:

```nix
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.rstudioWrapper.override {
  packages = with pkgs.rPackages; [
    dplyr
    ggplot2
    reshape2
  ];
}
```

اجرای `nix-shell` سپس شما را وارد محیطی معادل با محیط بالا می‌کند. اگر به بسته‌های اضافی نیاز دارید، کافی است آن‌ها را به فهرست اضافه کرده و دوباره وارد ش

```bash
nix-shell generate-shell.nix

Rscript generate-r-packages.R cran  > cran-packages.json.new
mv cran-packages.json.new cran-packages.json

Rscript generate-r-packages.R bioc  > bioc-packages.json.new
mv bioc-packages.json.new bioc-packages.json

Rscript generate-r-packages.R bioc-annotation > bioc-annotation-packages.json.new
mv bioc-annotation-packages.json.new bioc-annotation-packages.json

Rscript generate-r-packages.R bioc-experiment > bioc-experiment-packages.json.new
mv bioc-experiment-packages.json.new bioc-experiment-packages.json
```

`generate-r-packages.R <repo>` فایل `<repo>-packages.json` را می‌خواند، به همین دلیل این تغییر نام انجام شده‌است.

محتویات فایل تولیدشدهٔ `*-packages.json` برای ایجاد یک derivation بسته به ازای هر بسته R فهرست‌شده در فایل استفاده خواهد شد.

برخی از بسته‌ها برای مشخص کردن وابستگی‌های خارجی یا سایر پچ‌ها و الزامات خاص به بازنشانی‌ها نیاز دارند. این بازنشانی‌ها در فایل `pkgs/development/r-modules/default.nix` مشخص
