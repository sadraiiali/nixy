# pkg-config {#sec-pkg-config}

*pkg-config* یک رابط یکپارچه برای اعلام و استعلام کتابخانه‌های C/C++ ساخته‌شده‌است.

Nixpkgs چندین امکان

```nix
{ pkg-config, testers, ... }:

stdenv.mkDerivation (finalAttrs: {
  # ...

  nativeBuildInputs = [
    pkg-config
    validatePkgConfig
  ];

  passthru.tests.pkg-config = testers.hasPkgConfigModules {
    package = finalAttrs.finalPackage;
    versionCheck = true;
  };

  meta = {
    # ...
    pkgConfigModules = [ "miniz" ];
  };
})
```

## دسترسی به بسته‌ها از طریق نام ماژول pkg-config {#sec-pkg-config-usage}

### در داخل Nixpkgs {#sec-pkg-config-usage-internal}

یک [قلاب را
