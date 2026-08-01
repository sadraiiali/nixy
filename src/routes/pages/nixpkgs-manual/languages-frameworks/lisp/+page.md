(ad-hoc)

Translation:
رایج‌ترین روش برای استفاده از این کتابخانه، اجرای ورپرهای آنی (ad-hoc) به این صورت است:

Inline backticks line:
`` `nix-shell -p 'sbcl.withPackages (ps: with ps; [ alexandria ])`

```
$ sbcl
* (load (sb-ext:posix-getenv "ASDF"))
* (asdf:load-system 'alexandria)
```

همچنین می‌توان یک محیط `pkgs.mkShell` در `shell.nix`/`flake.nix` ایجاد کرد:

```nix
let
  sbcl' = sbcl.withPackages (ps: [ ps.alexandria ]);
in
mkShell { packages = [ sbcl' ]; }
```

اکنون می‌توان از چنین Lispی برای مثال جهت کامپایل کردن کدهای منبع استفاده کرد:

```nix
{
  buildPhase = ''
    runHook preBuild

    ${sbcl'}/bin/sbcl --load my-build-file.lisp

    runHook postBuild
  '';
}
```

## <a id="lisp-importing-packages-from-quicklisp"></a> درون‌ریزی بسته‌ها از Quicklisp

برای صرفه‌جویی در نوشتن عبارت‌های Nix، اسکریپتی وجود دارد که تمام بسته‌های توزیع‌شده توسط Quicklisp را در `imported.nix` درون‌ریزی می‌کند. این کار با پارس کردن فایل‌های `releases.txt` و `systems.txt` آن انجام می‌شود که هر چند ماه یک‌بار در [quicklisp.org](https://beta.quicklisp.org/dist/quicklisp.txt) منتشر می‌شوند.

فرآیند درون‌ریزی در پوشه `import` به صورت کد Common Lisp در سیستم ASDF با نام `org.lispbuilds.nix` پیاده‌سازی شده است. برای اجرای اسکریپت، می‌توان `ql-import.lisp`

```
cd pkgs/development/lisp-modules
nix-shell --run 'sbcl --script ql-import.lisp'
```

`sbcl` etc.) also export the `buildASDFSystem`
function, which is similar to `build-asdf-system` from `packages.nix`, but is
part of the public API.

Glossary check:
- derivations -> درایویشن‌ها
- function -> تابع

Translation:
## <a id="lisp-defining-packages-outside"></a> تعریف دستی بسته‌ها در خارج از Nixpkgs

درایویشن‌های Lisp (مانند

آرگومان‌های زیر را می‌پذیرد:

- `pname`: نام بسته
- `version`: نسخه بسته
- `src`: سورس بسته
- `patches`: پچ‌هایی که باید پیش از

```nix
let
  alexandria = sbcl.buildASDFSystem rec {
    pname = "alexandria";
    version = "1.4";
    src = fetchFromGitLab {
      domain = "gitlab.common-lisp.net";
      owner = "alexandria";
      repo = "alexandria";
      tag = "v${version}";
      hash = "sha256-1Hzxt65dZvgOFIljjjlSGgKYkj+YBLwJCACi5DZsKmQ=";
    };
  };
  sbcl' = sbcl.withOverrides (self: super: { inherit alexandria; });
in
sbcl'.pkgs.alexandria
```

## <a id="lisp-overriding-package-attributes"></a> بازنشانی صفات بسته

بسته‌ها تابع `overrideLispAttrs` را ارائه می‌دهند که می‌توان از آن برای ساخت یک بسته جدید با پارامترهای متفاوت استفاده کرد.

مثالی از بازنشانی `alexandria`:

```nix
sbcl.pkgs.alexandria.overrideLispAttrs (oldAttrs: rec {
  version = "1.4";
  src = fetchFromGitLab {
    domain = "gitlab.common-lisp.net";
    owner = "alexandria";
    repo = "alexandria";
    tag = "v${version}";
    hash = "sha256-1Hzxt65dZvgOFIljjjlSGgKYkj+YBLwJCACi5DZsKmQ=";
  };
})
```

### <a id="lisp-dealing-with-slashy-systems"></a> مدیریت سیستم‌های اسلش‌دار

سیستم‌های اسلش‌دار (ثانویه) نباید در

```nix
ecl.pkgs.alexandria.overrideLispAttrs (oldAttrs: {
  systems = oldAttrs.systems ++ [ "alexandria/tests" ];
  lispLibs = oldAttrs.lispLibs ++ [ ecl.pkgs.rt ];
})
```

برای اطلاع از نحوهٔ ادغام مجدد آن در `ecl.pkgs`، [بخش مربوطه](#lisp-including-external-pkg-in-scope) در مورد استفاده از

```
nix-shell -p 'sbcl.withPackages (ps: [ ps.alexandria ps.bordeaux-threads ])'
```

از چنین پوشاننده‌ای می‌توان به این صورت استفاده کرد:

```
$ sbcl
* (load (sb-ext:posix-getenv "ASDF"))
* (asdf:load-system 'alexandria)
* (asdf:load-system 'bordeaux-threads)
```

### <a id="lisp-loading-asdf"></a> بارگیری ASDF

برای گرفتن بهترین نتیجه، هنگام استفاده از روکش‌های (wrappers) تولیدشده توسط کتابخانه، از فراخوانی `(require 'asdf)` خودداری کنید.

به جای آن،

```nix
wrapLisp {
  pkg = clisp;
  faslExt = "fas";
  flags = [
    "-E"
    "UTF8"
  ];
}
```
