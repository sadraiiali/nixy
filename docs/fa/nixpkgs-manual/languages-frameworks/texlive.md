، بلکه باید در یک محیط سرهم‌بندی شوند." -> "بسته‌ها را نمی‌توان به‌طور مستقیم استفاده کرد، بلکه باید در یک محیط گردآوری شوند."
"
```nix
  texliveSmall.withPackages (
    ps: with ps; [
      collection-langkorean
      algorithms
      cm-super
    ]
  )
  ```
تابع `withPackages` را می‌توان چندین بار برای افزودن بسته‌های بیشتر فراخوانی کرد.

  - **نکته.** در Nixpkgs، بسته‌ها فقط باید از محیط‌های پیش‌ساخته به عنوان
```nix
  texliveBasic.withPackages (
    ps: with ps; [
      texdoc # recommended package to navigate the documentation
      perlPackages.LaTeXML.tex # tex files of LaTeXML, omit binaries
      cm-super
      cm-super.texdoc # documentation of cm-super
    ]
  )
  ```

- بسته‌ها را می‌توان با ارسال یک بسته جدید با همان `pname` به `.withPackages` بازنشانی کرد. برای نمونه، عبارت زیر Asymptote را با نسخه‌ای از Nixpkgs که معمولاً به‌روزتر است جایگزین می‌کند:
```nix
  texliveMedium.withPackages (ps: [ asymptote ])
  ```

- برای مستثنی کردن یک بسته از یک مجموعه، از یک بازنشانی خالی به‌صورت زیر استفاده کنید:
```nix
  texliveBasic.withPackages (
    ps: with ps; [
      collection-bibtexextra
      { pname = "bib2gls"; }
    ]
  )
  ```

- برای افزودن مستندات همه بسته‌ها در محیط، از موارد زیر استفاده کنید:
```nix
  texliveSmall.overrideAttrs { withDocs = true; }
  ```
این کار را می‌توان قبل یا بعد از فراخوانی `withPackages` اعمال کرد. پارامتر `withSources` تمام کانتینرهای سورس را اضافه می‌کند.

- تمام بسته‌های توزیع‌شده توسط TeX Live، که شامل اکثر بخش‌های CTAN است، در دسترس هستند و می‌توان آن‌ها را زیر `texlive.pkgs` یافت:
```ShellSession
  $ nix repl
  nix-repl> :l <nixpkgs>
  nix-repl> texlive.pkgs.[TAB]
  ```
این‌ها درایویشن‌هایی با خروجی‌های `out`، `tex`، `texdoc`، `texsource`، `tlpkg`، `man` و `info` هستند. امکان نصب آن‌ها خارج از `texlive.withPackages` وجود ندارد، اما برای مصارف دیگر در دسترس هستند. برای نمونه، جهت بسته‌بندی مجدد یک فونت، از
```nix
  stdenvNoCC.mkDerivation (finalAttrs: {
    src = texlive.pkgs.iwona;
    dontUnpack = true;

    inherit (finalAttrs.src) pname version;

    installPhase = ''
      runHook preInstall
      install -Dm644 $src/fonts/opentype/nowacki/iwona/*.otf -t $out/share/fonts/opentype
      runHook postInstall
    '';
  })
  ```

- See `biber`, `iwona` for complete examples.
"برای نمونه‌های کامل، `biber` و `iwona` را ببینید."

- "derivation" -> derivation / اشتقاق ساخت
Glossary entry: derivation ->

```nix
with import <nixpkgs> { };

let
  foiltex = stdenvNoCC.mkDerivation {
    pname = "latex-foiltex";
    version = "2.1.4b";

    outputs = [
      "tex"
      "texdoc"
    ];
    passthru.tlDeps = ps: [ ps.latex ];

    srcs = [
      (fetchurl {
        url = "http://mirrors.ctan.org/macros/latex/contrib/foiltex/foiltex.dtx";
        hash = "sha256-/2I2xHXpZi0S988uFsGuPV6hhMw8e0U5m/P8myf42R0=";
      })
      (fetchurl {
        url = "http://mirrors.ctan.org/macros/latex/contrib/foiltex/foiltex.ins";
        hash = "sha256-KTm3pkd+Cpu0nSE2WfsNEa56PeXBaNfx/sOO2Vv0kyc=";
      })
    ];

    unpackPhase = ''
      runHook preUnpack

      for _src in $srcs; do
        cp "$_src" $(stripHash "$_src")
      done

      runHook postUnpack
    '';

    nativeBuildInputs = [
      (texliveSmall.withPackages (
        ps: with ps; [
          cm-super
          hypdoc
          latexmk
        ]
      ))
      writableTmpDirAsHomeHook # Need a writable $HOME for latexmk
    ];

    # multiple-outputs.sh fails if $out is not defined
    preHook = ''
      out="''${tex-}"
    '';

    dontConfigure = true;

    buildPhase = ''
      runHook preBuild

      # Generate the style files
      latex foiltex.ins

      # Generate the documentation
      latexmk -pdf foiltex.dtx

      runHook postBuild
    '';

    installPhase = ''
      runHook preInstall

      path="$tex/tex/latex/foiltex"
      mkdir -p "$path"
      cp *.{cls,def,clo,sty} "$path/"

      path="$texdoc/doc/tex/latex/foiltex"
      mkdir -p "$path"
      cp *.pdf "$path/"

      runHook postInstall
    '';

    meta = {
      description = "LaTeX2e class for overhead transparencies";
      license = lib.licenses.unfreeRedistributable;
      maintainers = with lib.maintainers; [ veprbl ];
      platforms = lib.platforms.all;
    };
  };

  latex_with_foiltex = texliveSmall.withPackages (_: [ foiltex ]);
in
runCommand "test.pdf" { nativeBuildInputs = [ latex_with_foiltex ]; } ''
  cat >test.tex <<EOF
  \documentclass{foils}

  \title{Presentation title}
  \date{}

  \begin{document}
  \maketitle
  \end{document}
  EOF
    pdflatex test.tex
    cp test.pdf $out
''
```

## کش فونت LuaLaTeX {#sec-language-texlive-lualatex-font-cache}

کش فونت برای LuaLaTeX در `$HOME` نوشته می‌شود.
بنابراین، لازم است که `$HOME` روی یک مسیر قابل نوشتن تنظیم شود، برای مثال [پیش از استفاده از LuaLaTeX در درایویشن‌های Nix](https://github.com/NixOS/nixpkgs/issues/180639):
```nix
runCommand "lualatex-hello-world" { buildInputs = [ texliveFull ]; } ''
  mkdir $out
  echo '\documentclass{article} \begin{document} Hello world \end{document}' > main.tex
  env HOME=$(mktemp -d) lualatex  -interaction=nonstopmode -output-format=pdf -output-directory=$out ./main.tex
''
```

به‌علاوه، [کش یک کاربر می‌تواند با انبار نیکس (Nix store) واگرا شود](https://github.com/NixOS
```ShellSession
luaotfload-tool --cache=erase --flush-lookups --force
```
