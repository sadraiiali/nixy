# <a id="sec-pkg-config"></a> pkg-config

*pkg-config* یک رابط یکپارچه برای اعلام و استعلام کتابخانه‌های C/C++ ساخته‌شده است.

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

## <a id="sec-pkg-config-usage"></a> دسترسی به بسته‌ها از طریق نام ماژول pkg-config

### <a id="sec-pkg-config-usage-internal"></a> در داخل Nixpkgs

یک [قلاب را
