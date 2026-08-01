(ref-pinning-nixpkgs)=

# سنجاق کردن Nixpkgs

مشخص کردن عبارت‌های Nix راه دور، مانند آنچه توسط Nixpkgs ارائه شده‌است، به روش‌های مختلفی انجام‌پذیر است:

- [متغیر محیطی `$NIX_PATH`](/pages/nix-manual/command-ref/env-common#env-NIX_PATH)
- [گزینه `-I`](/pages/nix-manual/command-ref/opt-common#opt-I) در اکثر دستورات مانند `nix-build`، `nix-shell` و غیره.
- [`fetchurl`](/pages/nix-manual/language/builtins-prefix#builtins-fetchurl)، [`fetchTarball`](/pages/nix-manual/language/builtins-prefix#builtins-fetchTarball)، [`fetchGit`](/pages/nix-manual/language/builtins-prefix#builtins-fetchGit) یا [دریافت‌کننده‌های Nixpkgs](https://nixos.org/manual/nixpkgs/stable/#chap-pkgs-fetchers) در عبارت‌های Nix

## مقادیر ممکن URL

- مسیر فایل محلی:
```
  ./path/to/expression.nix
  ```

استفاده از `./.` بدین معناست که عبارت در یک فایل `default.nix` در پوشه جاری قرار دارد.

- سنجاق‌شده به یک کامیت خاص:
```
  https://github.com/NixOS/nixpkgs/archive/eabc38219184cc3e04a974fe31857d8e0eac098d.tar.gz
  ```

- استفاده از آخرین نسخه کانال، به این معنا که تمام تست‌ها با موفقیت پشت سر گذاشته شده‌اند:
```
  http://nixos.org/channels/nixos-22.11/nixexprs.tar.xz
  ```

- سینتکس خلاصه برای کانال‌ها:
```
  channel:nixos-22.11
  ```

- استفاده از جدیدترین نسخه کانال، میزبانی‌شده توسط GitHub:
```
  https://github.com/NixOS/nixpkgs/archive/nixos-22.11.tar.gz
  ```

- استفاده از آخرین کامیت روی شاخه‌ی انتشار، اما هنوز آزمایش‌نشده:
```
  https://github.com/NixOS/nixpkgs/archive/release-21.11.tar.gz
  ```

## مثال‌ها

-
```shell-session
  $ nix-build -I ~/dev
  ```

-
```shell-session
  $ nix-build -I nixpkgs=http://nixos.org/channels/nixos-22.11/nixexprs.tar.xz
  ```

-
```shell-session
  $ nix-build -I nixpkgs=channel:nixos-22.11
  ```

-
```shell-session
  $ NIX_PATH=nixpkgs=http://nixos.org/channels/nixos-22.11/nixexprs.tar.xz nix-build
  ```

-
```shell-session
  $ NIX_PATH=nixpkgs=channel:nixos-22.11 nix-build
  ```

- در زبان Nix:
```nix
  let
    pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-22.11.tar.gz") {};
  in pkgs.stdenv.mkDerivation { ... }
  ```

## یافتن کامیت‌ها و نسخه‌های خاص

سایت [status.nixos.org](https://status.nixos.org/) موارد زیر را فراهم می‌کند:

- آخرین کامیت‌های تست‌شده برای هر نسخه - هنگام سنجاق کردن Nixpkgs به کامیت‌های خاص از آن استفاده کنید.
- فهرست کانال‌های نسخه‌ی فعال - هنگام پیگیری آخرین نسخه‌های کانال از آن استفاده کنید.

ف فهرست کامل کانال‌ها در [nixos.org/channels](https://nixos.org/channels) در دسترس است.

:::{tip}
اطلاعات بیشتر درباره‌ی نسخه‌های Nixpkgs و NixOS: [](channel-branches)
:::

