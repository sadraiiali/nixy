---
myst:
  html_meta:
    "keywords": "tutorial, declarative, shell, environment, developer, nix, nixpkgs"
---

(declarative-reproducible-envs)=
# محیط‌های شل اعلامی با `shell.nix`

## بررسی اجمالی

محیط‌های شل اعلامی به شما امکان می‌دهند که:

- دستورات Bash را به طور خودکار در طول فعال‌سازی محیط اجرا کنید
- متغیرهای محیطی را به طور خودکار تنظیم کنید
- تعاریف محیط را تحت کنترل نسخه قرار داده و آن‌ها را روی ماشین‌های دیگر بازتولید کنید

### چه چیزی خواهید آموخت؟

در آموزش {ref}`ad-hoc-envs`، یادگرفتید که چگونه با استفاده از `nix-shell -p` به روش دستوری (imperative) محیط‌های شل ایجاد کنید.
این کار زمانی که می‌خواهید بدون نصب دائم ابزارها به سرعت به آن‌ها دسترسی داشته باشید عالی است.
همچنین یادگرفتید که چگونه آن دستور را با نسخه‌ای خاص از Nixpkgs با استفاده از یک کامیت گیت به عنوان آرگومان اجرا کنید تا همان محیط قبلی بازآفرینی شود.

در این آموزش، بررسی خواهیم کرد که چگونه با استفاده از یک پیکربندی اعلانی (declarative) در یک {term}`فایل Nix`، محیط‌های شل بازتولیدپذیر ایجاد کنیم.
این فایل را می‌توان با هر کسی به اشتراک گذاشت تا همان محیط را روی ماشینی دیگر بازآفرینی کند.

### چقدر زمان می‌برد؟

۳۰ دقیقه

### به چه چیزهایی نیاز دارید؟

- آشنایی با شل یونیکس
- درک مقدماتی از [زبان Nix](reading-nix-language)

## ورود به یک شل موقت

فرض کنید محیطی می‌خواهیم که در آن `cowsay` و `lolcat` در دسترس باشند.
ساده‌ترین راه ممکن برای انجام این کار استفاده از دستور `nix-shell -p` است:

```
$ nix-shell -p cowsay lolcat
```

این دستور کار می‌کند، اما تعدادی معایب دارد:
- لازم است هر بار که وارد شل می‌شوید، عبارت `-p cowsay lolcat` را تایپ کنید.
- این روش به شکلی (ارگونومیک) اجازه نمی‌دهد سفارشی‌سازی‌های بیشتری روی محیط شل خود انجام دهید.

راه‌حل بهتر این است که محیط شل خود را از یک فایل `shell.nix` بسازیم.

## یک فایل `shell.nix` پایه‌ای

فایلی به نام `shell.nix` با محتوای زیر ایجاد کنید:

```nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    cowsay
    lolcat
  ];
}
```

::::{dropdown} توضیحات تفصیلی
ما از نسخه‌ای از [Nixpkgs سنجاق‌شده به یک شاخه انتشار](<ref-pinning-nixpkgs>) استفاده می‌کنیم.
اگر آموزش [](ad-hoc-envs) را دنبال کرده‌اید و نمی‌خواهید تمام وابستگی‌ها را دوباره بارگیری کنید، دقیقاً همان ریویژن (revision) مشخص‌شده در بخش [](towards-reproducibility) را تعیین کنید:

```nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/2a601aafdc5605a5133a2ca506a34a3a73377247";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
```

ما به طور صریح `config` و `overlays` را تنظیم می‌کنیم تا از بازنویسی سهوی آن‌ها توسط [global configuration](https://nixos.org/manual/nixpkgs/stable/#chap-packageconfig) جلوگیری کنیم.

تابع `mkShellNoCC` یک مجموعه صفت (attribute set) را به عنوان آرگومان می‌پذیرد.
در اینجا ما به آن یک صفت `packages` همراه با فهرستی شامل دو آیتم از مجموعه صفت `pkgs` می‌دهیم.

:::{Dropdown} نکته‌ی حاشیه‌ای درباره‌ی `mkShell`

دستورات `nix-shell` و `mkShell` در ابتدا به عنوان روشی برای ساخت یک محیط شل حاوی [tools needed to debug package builds](https://nixos.org/manual/nixpkgs/stable/#sec-tools-of-stdenv)، مانند Make یا GCC طراحی شدند.
فقط بعدها بود که استفاده از آن به عنوان یک روش عمومی برای ساخت محیط‌های موقت برای اهداف دیگر به طور گسترده‌ای رایج شد.
تابع `mkShellNoCC` محیطی از این دست تولید می‌کند، اما بدون زنجیره ابزار کامپایلر (compiler toolchain).

ممکن است با نمونه‌هایی از `mkShell` یا `mkShellNoCC` مواجه شوید که در عوض، بسته‌ها را به صفت‌های `buildInputs` یا `nativeBuildInputs` اضافه می‌کنند.
تابع `mkShellNoCC` یک [wrapper around `mkDerivation`](https://nixos.org/manual/nixpkgs/stable/#sec-pkgs-mkShell) است، بنابراین همان آرگومان‌های `mkDerivation` مانند `buildInputs` یا `nativeBuildInputs` را می‌پذیرد.
آرگومان صفت `packages` برای `mkShellNoCC` در واقع صرفاً یک نام مستعار (alias) برای `nativeBuildInputs` است.
:::
::::

با اجرای `nix-shell` در همان پوشه‌ای که فایل `shell.nix` قرار دارد، وارد محیط شوید:

:::{note}
اولین اجرای `nix-shell` روی این فایل ممکن است برای بارگیری تمام وابستگی‌ها کمی زمان ببرد.
:::

```console
$ nix-shell
[nix-shell]$ cowsay hello | lolcat
```

دستور `nix-shell` به طور پیش‌فرض به دنبال فایلی به نام `shell.nix` در پوشه جاری می‌گردد و یک محیط شل از روی عبارت نیکس (Nix expression) موجود در این فایل می‌سازد.
بسته‌های تعریف‌شده در صفت (attribute) `packages` در متغیر محیطی `$PATH` در دسترس خواهند بود.

## متغیرهای محیطی

ممکن است بخواهید هنگام ورود به محیط شل، برخی متغیرهای محیطی را به طور خودکار صادر (export) کنید.

متغیر `GREETING` را تنظیم کنید تا بتوان از آن در محیط شل استفاده کرد:

```diff
 let
   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
   pkgs = import nixpkgs { config = {}; overlays = []; };
 in

 pkgs.mkShellNoCC {
   packages = with pkgs; [
     cowsay
     lolcat
   ];

+  GREETING = "Hello, Nix!";
 }
```

هر صفت (attribute) که به `mkShellNoCC` پاس داده شود و جزو موارد رزروشده نباشد و مقدار آن بتواند به یک رشته تبدیل شود، به یک متغیر محیطی تبدیل خواهد شد.

آن را امتحان کنید.
با تایپ کردن `exit` یا فشردن کلیدهای `Ctrl`+`D` از شل خارج شوید، سپس دوباره آن را با `nix-shell` راه‌اندازی کنید.

```console
[nix-shell]$ echo $GREETING
```

:::{warning}
برخی از متغیرها در برابر تنظیم شدن به شکلی که در بالا توصیف شد، محافظت می‌شوند.

برای مثال، قالب اعلان شل (shell prompt) برای بیشتر شل‌ها توسط متغیر محیطی `PS1` تنظیم می‌شود، اما `nix-shell` از قبل این مورد را به طور پیش‌فرض تنظیم می‌کند و صفت `PS1` تعیین‌شده در آرگومان را نادیده خواهد گرفت.

اگر نیاز دارید این متغیرهای محیطی محافظت‌شده را بازنویسی کنید، طبق توصیف بخش بعدی، از صفت `shellHook` استفاده کنید.
:::

## دستورات راه‌اندازی

ممکن است بخواهید پیش از ورود به محیط شل تعاملی، برخی از دستورات شل را اجرا کنید.
این دستورات را می‌توان در صفت `shellHook` که توسط `mkShellNoCC` فراهم شده‌است، قرار داد.

برای چاپ یک سلام و احوالپرسی رنگی، `shellHook` را تنظیم کنید:

```diff
 let
   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.05";
   pkgs = import nixpkgs { config = {}; overlays = []; };
 in

 pkgs.mkShellNoCC {
   packages = with pkgs; [
     cowsay
     lolcat
   ];

   GREETING = "Hello, Nix!";
+
+  shellHook = ''
+    echo $GREETING | cowsay | lolcat
+  '';
 }
```

دوباره امتحان کنید.
با تایپ کردن `exit` یا فشردن کلیدهای `Ctrl`+`D` از شل خارج شوید، سپس آن را دوباره با `nix-shell` راه‌اندازی کنید تا تأثیر آن را مشاهده کنید.

## مراجع

- [مستندات `mkShell`](https://nixos.org/manual/nixpkgs/stable/#sec-pkgs-mkShell)
- مستندات [توابع و ابزارهای شل](https://nixos.org/manual/nixpkgs/stable/#ssec-stdenv-functions) در Nixpkgs
- [مستندات `nix-shell`](https://n.dev/manual/nix/stable/command-ref/nix-shell)

## گام‌های بعدی

- [](reading-nix-language)
- [](automatic-direnv)
- [](../../guides/recipes/sharing-dependencies.md)
- [](../../guides/recipes/dependency-management.md)
