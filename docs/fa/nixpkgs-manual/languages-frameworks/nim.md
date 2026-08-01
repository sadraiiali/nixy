# Nim {#sec-language-nim}

کامپایلر Nim و یک تابع سازنده در دسترس هستند.
برنامه‌های Nim با استفاده از یک فایل lockfile و یکی از توابع `buildNimPackage` یا `buildNimSbom` ساخته می‌شوند.

## buildNimPackage {#buildNimPackage}

مثال زیر برنامه‌ای به زبان Nim را نشان می‌دهد که تنها به کتابخانه‌های Nim وابسته است:
```nix
{
  lib,
  buildNimPackage,
  fetchFromGitHub,
}:

buildNimPackage (finalAttrs: {
  pname = "ttop";
  version = "1.2.7";

  src = fetchFromGitHub {
    owner = "inv2004";
    repo = "ttop";
    tag = "v${finalAttrs.version}";
    hash = lib.fakeHash;
  };

  lockFile = ./lock.json;

  nimFlags = [ "-d:NimblePkgVersion=${finalAttrs.version}" ];
})
```

### پارامترهای `buildNimPackage` {#buildnimpackage-parameters}

تابع `buildNimPackage` یک مجموعه ویژگی از پارامترها را دریافت می‌کند که به `stdenv.mkDerivation` منتقل می‌شوند.
```sh
$ cd nixpkgs
$ nix build -f . ttop.src
$ nix run -f . nim_lk ./result | jq --sort-keys > pkgs/by-name/tt/ttop/lock.json
```

## buildNimSbom {#buildNimSbom}

یک جایگزین برای `buildNimPackage` عبارت است از `buildNimSbom` که بسته‌ها را از فایل‌های [
```nix
# pkgs/by-name/ni/nim_lk/package.nix
{
  lib,
  buildNimSbom,
  fetchFromSourcehut,
  openssl,
}:

buildNimSbom (finalAttrs: {
  src = fetchFromSourcehut {
    owner = "~ehmry";
    repo = "nim_lk";
    tag = finalAttrs.version;
    hash = lib.fakeHash;
  };
  buildInputs = [ openssl ];
}) ./sbom.json
```

### تولید SBOMها {#generating-nim-sboms}

ابزار [nim_lk](https://git.sr.ht/~ehmry/nim_lk) می‌تواند از متادیتای بستهٔ [

```nix
pkgs.nitter.overrideNimAttrs {
  # using a different source which has different dependencies from the standard package
  src = pkgs.fetchFromGitHub {
    # …
  };
  # new lock file generated from the source
  lockFile = ./custom-lock.json;
}
```

## بازنشانی‌های وابستگی lockfile {#nim-lock-overrides}

تابع `buildNimPackage` کتابخانه‌های مشخص‌شده توسط `lockFile` را با مجموعه ویژگی (
```nix
{
  lib,
  # …
  SDL2,
  # …
}:

{
  # …
  sdl2 =
    lockAttrs:
    {
      buildInputs ? [ ],
      ...
    }:
    {
      buildInputs = buildInputs ++ [ SDL2 ];
    };
  # …
}
```

حاشیه‌نویسی‌ها در مجموعه `nim-overrides.nix` توابعی هستند که دو آرگومان می‌گیرند و یک attrset جدید برمی‌گردانند تا روی بسته‌ای
```nix
{
  lib,
  buildNimPackage,
  nimOverrides,
  libressl,
}:

let
  buildNimPackage' = buildNimPackage.override {
    nimOverrides = nimOverrides.override { openssl = libressl; };
  };
in
buildNimPackage' (finalAttrs: {
  pname = "foo";
  # …
})
```

بازنشانی یک بسته به صورت خارجی:
```nix
{ pkgs }:
{
  foo = pkgs.foo.override {
    buildNimPackage = pkgs.buildNimPackage.override {
      nimOverrides = pkgs.nimOverrides.override { openssl = libressl; };
    };
  };
}
```
