# OCaml {#sec-language-ocaml}

## راهنمای کاربر {#sec-language-ocaml-user-guide}

کتابخانه‌های OCaml در مجموعه صفات‌هایی به شکل `ocaml-ng.ocamlPackages_X_XX` در دسترس هستند که در آن X باید با نسخه کامپایلر مورد نظر جایگزین شود. به عنوان مثال، ocamlgraph کامپایل‌شده با OCaml 4.12 را می‌توان در `ocaml-ng.ocamlPackages_4_12.ocamlgraph` یافت. خود کامپایلر نیز در همین مجموعه و تحت نام `ocaml` قرار دارد.

اگر نسخه دقیق کامپایلر برایتان مهم نیست، `ocamlPackages` یک نام مستعار سطح بالا است که به نسخه جدیدی از OCaml اشاره می‌کند.

برنامه‌های OCaml معمولاً در سطح بالا در دسترس هستند، نه در داخل `ocamlPackages`. استثناهای مهم، ابزارهای ساخت هستند که باید با همان نسخه کامپایلری ساخته شوند
```nix
let
  pkgs = import <nixpkgs> { };
  # choose the ocaml version you want to use
  ocamlPackages = pkgs.ocaml-ng.ocamlPackages_4_12;
in
pkgs.mkShell {
  # build tools
  nativeBuildInputs = with ocamlPackages; [
    ocaml
    findlib
    pkgs.dune
    ocaml-lsp
  ];
  # dependencies
  buildInputs = with ocamlPackages; [ ocamlgraph ];
}
```

.version}/site-lib/`
- `$OCAMLPATH`
- `nix-shell`
- `buildDunePackage`
- `buildInputs`
- `propagatedBuildInputs`
- `minimalOCamlVersion`
- `fetchFromGitHub`
- `dune

```nix
{
  lib,
  fetchFromGitHub,
  buildDunePackage,
  ocaml,
  ocaml-syntax-shims,
  alcotest,
  result,
  bigstringaf,
  ppx_let,
}:

buildDunePackage (finalAttrs: {
  pname = "angstrom";
  version = "0.15.0";

  minimalOCamlVersion = "4.04";

  src = fetchFromGitHub {
    owner = "inhabitedtype";
    repo = "angstrom";
    tag = finalAttrs.version;
    hash = "sha256-MK8o+iPGANEhrrTc1Kz9LBilx2bDPQt7Pp5P2libucI=";
  };

  buildInputs = [ ocaml-syntax-shims ];

  propagatedBuildInputs = [
    bigstringaf
    result
  ];

  doCheck = lib.versionAtLeast ocaml.version "4.05";
  checkInputs = [
    alcotest
    ppx_let
  ];

  meta = {
    homepage = "https://github.com/inhabitedtype/angstrom";
    description = "OCaml parser combinators built for speed and memory efficiency";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ sternenseemann ];
  };
})
```

در اینجا مثال دوم آمده‌است، این بار با استفاده از یک آرشیو کد منبع که با `dune-release` تولید شده‌است. استفاده از این آرشیو در صورت در دسترس بودن اقدام مناسبی است، زیرا معمولاً شامل متغیرهای جایگزین‌شده‌ای مانند فیلد `%%VERSION%%` است. این کتابخانه به هیچ کتابخانه OCaml دیگری وابسته نیست و پس از ساخت آن هیچ تستی اجرا نمی‌شود.

```nix
{
  lib,
  fetchurl,
  buildDunePackage,
}:

buildDunePackage (finalAttrs: {
  pname = "wtf8";
  version = "1.0.2";

  minimalOCamlVersion = "4.02";

  src = fetchurl {
    url = "https://github.com/flowtype/ocaml-wtf8/releases/download/v${finalAttrs.version}/wtf8-v${finalAttrs.version}.tbz";
    hash = "sha256-d5/3KUBAWRj8tntr4RkJ74KWW7wvn/B/m1nx0npnzyc=";
  };

  meta = {
    homepage = "https://github.com/flowtype/ocaml-wtf8";
    description = "WTF-8 is a superset of UTF-8 that allows unpaired surrogates";
    license = lib.licenses.mit;
    maintainers = [ lib.maintainers.eqyiel ];
  };
})
```

اگر دو نسخهٔ متفاوت از یک کتابخانه به `buildInputs` اضافه شوند (که معمولاً به صورت متعدی و به دلیل `propagatedBuildInputs` رخ می‌دهد)، ساخت به طور خودکار با شکست مواجه خواهد شد. برای غیرفعال کردن این رفتار، `dontDetectOcamlConflicts` را روی true قرار دهید.
