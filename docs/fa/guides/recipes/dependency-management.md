(dependency-management-npins)=
# مدیریت خودکار منابع راه دور با `npins`

زبان Nix وابستگی‌های بین فایل‌هایی که Nix مدیریت می‌کند را توصیف می‌کند.
خود عبارت‌های Nix می‌توانند به منابع راه دور وابسته باشند و راه‌های مختلفی برای مشخص کردن مبدأ آن‌ها وجود دارد، همان‌طور که در [](pinning-nixpkgs) نشان داده شده است.

برای اتوماسیون بیشتر در زمینه مدیریت منابع راه دور، [`npins`](https://github.com/andir/npins/) را در پروژه خود راه‌اندازی کنید:

```shell-session
$ nix-shell -p npins --run "npins init --bare; npins add github nixos nixpkgs --branch nixos-23.11"
```

این دستور آخرین بازنگری از شاخه انتشار Nixpkgs 23.11 را دریافت خواهد کرد.
این دستور در پوشه جاری فایل `npins/sources.json` را تولید می‌کند که حاوی یک ارجاع سنجاق‌شده (Pinned) به بازنگری به‌دست‌آمده خواهد بود.
همچنین این دستور فایل `npins/default.nix` را ایجاد می‌کند که آن وابستگی‌ها را به عنوان یک مجموعه ویژگی (attribute set) در دسترس قرار می‌دهد.

فایل تولیدشده‌ی `npins/default.nix` را به عنوان مقدار پیش‌فرض برای آرگومان تابع موجود در `default.nix` درون‌ریزی کرده و از آن برای ارجاع به پوشه سورس Nixpkgs استفاده کنید:

```nix
{
  sources ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import sources.nixpkgs { inherit system; config = {}; overlays = []; },
}:
{
  package = pkgs.hello;
}
```

دستور `nix-build` تابع سطح بالا را با مجموعه ویژگی خالی `{}`, یا با صفت‌های ارسال‌شده از طریق [`--arg`](/pages/nix-manual/command-ref/nix-build#opt-arg) یا [`--argstr`](/pages/nix-manual/command-ref/nix-build#opt-argstr) فراخوانی می‌کند.
این الگو امکان [بازنشانی منابع با npins](overriding-sources-npins) را به صورت برنامه‌نویسی فراهم می‌کند.

برای اینکه `npins` در محیط توسعه‌ی پروژه شما به‌راحتی در دسترس باشد، آن را اضافه کنید:

```diff
 {
   sources ? import ./npins,
   system ? builtins.currentSystem,
   pkgs ? import sources.nixpkgs { inherit system; config = {}; overlays = []; },
 }:
-{
+rec {
   package = pkgs.hello;
+  shell = pkgs.mkShellNoCC {
+    inputsFrom = [ package ];
+    packages = with pkgs; [
+      npins
+    ];
+  };
 }
```

همچنین برای ورود راحت‌تر به آن محیط، یک `shell.nix` اضافه کنید:

```nix
(import ./. {}).shell
```

برای جزئیات بیشتر به [](./sharing-dependencies) مراجعه کنید و توجه داشته باشید که در اینجا باید یک مجموعه ویژگی خالی به عبارت درون‌ریزی‌شده ارسال کنید، زیرا `default.nix` اکنون شامل یک تابع است.

(overriding-sources-npins)=
## بازنشانی منابع

به عنوان یک مثال، از عبارت ایجادشده‌ی قبلی با نسخه‌ی قدیمی‌تری از Nixpkgs استفاده خواهیم کرد.

وارد محیط توسعه شوید، یک پوشه جدید بسازید و npins را با نسخه متفاوتی از Nixpkgs راه‌اندازی کنید:

```shell-session
$ nix-shell
[nix-shell]$ mkdir old
[nix-shell]$ cd old
[nix-shell]$ npins init --bare
[nix-shell]$ npins add github nixos nixpkgs --branch nixos-21.11
```

یک فایل `default.nix` در پوشه جدید ایجاد کنید تا فایل اصلی را با `sources` که تازه ایجاد کرده‌اید، درون‌ریزی کنید.

```nix
import ../default.nix { sources = import ./npins; }
```

این کار باعث می‌شود نسخه متفاوتی ساخته شود:

```shell-session
$ nix-build -A build
$ ./result/bin/hello --version | head -1
hello (GNU Hello) 2.10
```

منابع را همچنین می‌توان در خط فرمان بازنویسی کرد:

```shell-session
nix-build .. -A build --arg sources 'import ./npins'
```

## مهاجرت از `niv`

نسخه‌ی قبلی این راهنما استفاده از [`niv`](https://github.com/nmattia/niv/)، یک مدیر ثابت‌سازی نسخه (Pinning) مشابه که به زبان Haskell نوشته شده است را پیشنهاد می‌کرد.

اگر پروژه‌ای دارید که از `niv` استفاده می‌کند، می‌توانید تعاریف منابع راه دور را به `npins` درون‌ریزی کنید:

```shell-session
npins import-niv
```

:::{warning}
تمام ورودی‌های درون‌ریزی‌شده به‌روز خواهند لشد، بنابراین لزوماً به همان کامیت‌های قبلی اشاره نخواهند کرد.
:::

## مدیریت پیکربندی‌های NixOS

NixOS به‌طور پیش‌فرض برای یافتن `nixpkgs` از کانال‌ها استفاده می‌کند.
شما می‌توانید به جای آن، یک نسخه را با استفاده از `npins` از نقطه ورود `system.nix` (موجود از نسخه 26.05 به بعد) سنجاق کردن کنید:

```nix
let
  sources = import ./npins;
in
import "${sources.nixpkgs}/nixos" {
  configuration = ./configuration.nix;
}
```

پیش از NixOS 26.05، از `system.nix` استفاده کنید:

```bash
sudo NIX_PATH="nixos-config=configuration.nix:nixpkgs=$(nix-instantiate --raw --eval npins -A nixpkgs.outPath)" nixos-rebuild switch
```

اگر از npins به همراه `system.nix` استفاده می‌کنید، کانال‌ها را در پیکربندی خود غیرفعال کنید:

```nix
# configuration.nix
{
  # ...
  nix.channel.enable = false;
}
```

برای دردسترس قرار دادن چنین وابستگی‌های ثابت‌شده‌ای به عنوان [مسیرهای جستجو](https://nix.dev/tutorials/nix-language.html#lookup-paths) (مانند `<nixpkgs>`) در حین استفاده از پیکربندی NixOS، می‌توان از روش زیر استفاده کرد:

```nix
# configuration.nix
{ lib, ... }:
let
  sources = import ./npins;
in
{
  # ...
  nix.nixPath = lib.mapAttrsToList (k: v: "${k}=${v}") sources;
}
```

برای استفاده از [خط فرمان v3] و اجرای برنامه‌ها از وابستگی‌ها که بسته‌ها را از طریق یک [فلیک] ارائه می‌دهند، مانند `nix run nixpkgs#hello`، می‌توانید فلیک‌ها را فعال کرده و پین‌ها را به رجیستری فلیک اضافه کنید مانند:

```nix
# configuration.nix
{ lib, ... }:
let
  sources = import ./npins;
in
{
  # ...
  experimental-features = "nix-command flakes";
  nix.registry = lib.mapAttrs (_: path: {
    to = {
      type = "path";
      inherit path;
    };
  }) sources;
```

[خط فرمان نسخه ۳]: /pages/nix-manual/command-ref/experimental-commands
[فلیک]: https://nix.dev/concepts/flakes

## گام‌های بعدی

- برای کسب اطلاعات بیشتر، راهنمای توکار را بررسی کنید:
```shell-session
  npins --help
  ```

- برای جزئیات بیشتر و نمونه‌های روش‌های مختلف مشخص کردن منابع راه دور، به [](pinning-nixpkgs) مراجعه کنید.
