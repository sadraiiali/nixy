تحت صفت‌های `tcl` و `tcl-X_Y` در دسترس هستند، که در آن `X_Y` نسخه Tcl است." -> "مفسرهای Tcl تحت صفت‌های `tcl` و `t

```
{ lib, fetchzip, mkTclDerivation, openssl }:

mkTclDerivation (finalAttrs: {
  pname = "tcltls";
  version = "1.7.22";

  src = fetchzip {
    url = "https://core.tcl-lang.org/tcltls/uv/tcltls-${finalAttrs.version}.tar.gz";
    hash = "sha256-TOouWcQc3MNyJtaAGUGbaQoaCWVe6g3BPERct/V65vk=";
  };

  buildInputs = [ openssl ];

  configureFlags = [
    "--with-ssl-dir=${openssl.dev}"
  ];

  meta = {
    homepage = "https://core.tcl-lang.org/tcltls/index";
    description = "OpenSSL / RSA-bsafe Tcl extension";
    maintainers = [ lib.maintainers.agbrooks ];
    license = lib.licenses.tcltk;
    platforms = lib.platforms.unix;
  };
})
```

ترجیح دهید.
نحوهٔ استفاده از آن در `pkgs/development/tcl-modules/by-name/README.md` مستند شده است.

تمام برنامه‌های Tcl در

```nix
{
  tclRequiresCheck = [
    "json"
    "doctools"
  ];
}
```

تقریباً به این صورت ترجمه می‌شود:

```nix
{
  preDist = ''
    TCLLIBPATH="$out/lib $TCLLIBPATH"
    tclsh <<<'exit [catch {package require json; package require doctools}]'
  '';
}
```

با این حال، این کار در فاز مجزای خود انجام می‌شود و به این‌که [`doCheck = true;`](#var-stdenv-doCheck) باشد یا خیر وابسته نیست.

این امر همچنین می‌تواند در بررسی این‌که بسته وجود بسته‌های به‌طور معمول موجود (برای مثال `tcllib`) را فرض نمی‌کند، مفید باشد.
