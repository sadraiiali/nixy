# نخستین برنامه خود را بسته‌بندی کنید {#chap-first-package}

با انتخاب کمک‌رسان ساخت مربوط به زبان برنامه و تنظیم چند صفت، یک برنامه را با Nixpkgs بسته‌بندی کنید.

هر بوم‌سازگان زبانی، کمک‌رسان ساخت خاص خود را دارد.
برای دیدن مجموعه کامل، [](#chap-language-support) را ببینید.

## بسته‌بندی یک برنامه Go {#first-package-go}

`buildGoModule` برنامه‌های Go را که از ماژول‌های Go استفاده می‌کنند می‌سازد.

بسته را در `package.nix` بنویسید:

:::{.example #ex-first-package-go}

# بسته‌بندی `pet` با `buildGoModule`

```nix
# package.nix
{
  buildGoModule,
  fetchFromGitHub,
  lib,
}:
buildGoModule (finalAttrs: {
  pname = "pet";
  version = "0.3.4";

  src = fetchFromGitHub {
    owner = "knqyf263";
    repo = "pet";
    tag = "v${finalAttrs.version}";
    hash = "sha256-Gjw1dRrgM8D3G7v6WIM2+50r4HmTXvx0Xxme2fH9TlQ=";
  };

  vendorHash = "sha256-6hCgv2/8UIRHw1kCe3nLkxF23zE/7t5RDwEjSzX3pBQ=";

  meta = {
    description = "Simple command-line snippet manager, written in Go";
    homepage = "https://github.com/knqyf263/pet";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [ kalbasit ];
  };
})
```

:::

`buildGoModule` به `pname`، `version`، `src` و `vendorHash` نیاز دارد.

نسخه Nixpkgs را ثابت‌سازی کرده و بسته را از `default.nix` فراخوانی کنید:

```nix
# default.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz";
  pkgs = import nixpkgs { };
in
pkgs.callPackage ./package.nix { }
```

آن را بسازید:

```shell
$ nix-build ./default.nix
# or equivalent
$ nix-build
```

آن را اجرا کنید:

```shell
$ ./result/bin/pet --help
pet - Simple command-line snippet manager.
```

`vendorHash` وابستگی‌های دریافت‌شده را ثابت می‌کند.
برای یافتن مقدار آن:

1. `vendorHash` را روی یک رشته خالی `""` قرار دهید.
2. `nix-build` را اجرا کنید.
3. مقدار صحیح را از خطا کپی کرده و در `vendorHash` قرار دهید.

برای هر صفت (attribute) و موارد استفاده پیشرفته، [مرجع Go](#sec-language-go) را ببینید.
