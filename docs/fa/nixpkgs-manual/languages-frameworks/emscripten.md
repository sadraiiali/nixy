# Emscripten {#emscripten}

[Emscripten](https://github.com/kripken/emscripten): یک کامپایلر LLVM به JavaScript

اگر می‌خواهید همان‌طور که در Ubuntu و توزیع‌های مشابه عادت کرده‌اید، با `emcc`، `emconfigure` و `emmake` کار کنید،

```console
nix-shell -p emscripten
```

چند نکته که باید به آن‌ها توجه داشت:

* `export EMCC_DEBUG=2` برای دیباگ (اشکال‌زدایی) مفید است
* کش فرآورده‌ی ساخت در `~/.emscripten` گاهی مشکلاتی ایجاد می‌کند و لازم است هر از چند گاهی حذف شود

## مثال‌ها {#declarative-usage}

بیااید دو مثال متفاوت از `pkgs/top-level/emscripten-packages.nix` را ببینیم:

* `pkgs.zlib.override`
* `pkgs.buildEmscriptenPackage`

یک الزام خاص در `pkgs.buildEmscriptenPackage` مقدار `doCheck = true` است.
این به این معناست که هر بسته Emscripten مستلزم پیاده‌سازی یک [`checkPhase`](#ssec-check-phase) است.

* از `export EMCC_DEBUG=2` در داخل یک فاز استفاده کنید تا خروجی دیباگ (اشکال‌زدایی) با جزئیات بیشتری درباره‌ی ایراد پیش‌آمده دریافت کنید.
* کش موجود در `~/.emscripten` نیازمند تنظیم `HOME=$TMPDIR` در فازهای منفرد است.
  این کار کامپایل کردن را کندتر اما قطعی‌تر می‌سازد.

::: {.example #usage-1-pkgs.zlib.override}

# استفاده از `pkgs.zlib.override {}`

این مثال از `zlib` از Nixpkgs استفاده می‌کند، اما به جای کامپایل کردن **C** به **ELF**، به دلیل استفاده از `pkgs.zlib.override` و تغییر `stdenv` به `pkgs.emscriptenStdenv`، **C** را به **JavaScript** کامپایل می‌کند.

چندین تطبیق و هک اعمال شده‌است تا کار کند.
یک مزیت این است که وقتی `pkgs.zlib` به‌روزرسانی می‌شود، این بسته نیز به طور خودکار به‌روزرسانی خواهد شد.

```nix
(pkgs.zlib.override { stdenv = pkgs.emscriptenStdenv; }).overrideAttrs (old: {
  buildInputs = old.buildInputs ++ [ pkg-config ];
  # we need to reset this setting!
  env = (old.env or { }) // {
    NIX_CFLAGS_COMPILE = "";
  };

  configurePhase = ''
    # FIXME: Some tests require writing at $HOME
    HOME=$TMPDIR
    runHook preConfigure

    #export EMCC_DEBUG=2
    emconfigure ./configure --prefix=$out --shared

    runHook postConfigure
  '';

  dontStrip = true;
  outputs = [ "out" ];

  buildPhase = ''
    runHook preBuild

    emmake make

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    emmake make install

    runHook postInstall
  '';

  checkPhase = ''
    runHook preCheck

    echo "================= testing zlib using node ================="

    echo "Compiling a custom test"
    set -x
    emcc -O2 -s EMULATE_FUNCTION_POINTER_CASTS=1 test/example.c -DZ_SOLO \
    libz.so.${old.version} -I . -o example.js

    echo "Using node to execute the test"
    ${pkgs.nodejs}/bin/node ./example.js

    set +x
    if [ $? -ne 0 ]; then
      echo "test failed for some reason"
      exit 1;
    else
      echo "it seems to work! very good."
    fi
    echo "================= /testing zlib using node ================="

    runHook postCheck
  '';

  postPatch = pkgs.lib.optionalString pkgs.stdenv.hostPlatform.isDarwin ''
    substituteInPlace configure \
      --replace-fail '/usr/bin/libtool' 'ar' \
      --replace-fail 'AR="libtool"' 'AR="ar"' \
      --replace-fail 'ARFLAGS="-o"' 'ARFLAGS="-r"'
  '';
})
```

:::{.example #usage-2-pkgs.buildemscriptenpackage}

# استفاده از `pkgs.buildEmscriptenPackage {}`

این مثال `xmlmirror` شامل یک بسته Emscripten است که به‌طور کامل در همین بافت تعریف شده و از هیچ `pkgs.zlib.override` استفاده نمی‌کند.

```nix
pkgs.buildEmscriptenPackage {
  pname = "xmlmirror";
  version = "1.2.3";

  buildInputs = [
    pkg-config
    autoconf
    automake
    libtool
    gnumake
    libxml2
    nodejs
    openjdk
    json_c
  ];

  nativeBuildInputs = [
    pkg-config
    writableTmpDirAsHomeHook
    zlib
  ];

  src = pkgs.fetchgit {
    url = "https://gitlab.com/odfplugfest/xmlmirror.git";
    rev = "4fd7e86f7c9526b8f4c1733e5c8b45175860a8fd";
    hash = "sha256-i+QgY+5PYVg5pwhzcDnkfXAznBg3e8sWH2jZtixuWsk=";
  };

  configurePhase = ''
    runHook preConfigure

    rm -f fastXmlLint.js*
    # a fix for ERROR:root:For asm.js, TOTAL_MEMORY must be a multiple of 16MB, was 234217728
    # https://gitlab.com/odfplugfest/xmlmirror/issues/8
    sed -e "s/TOTAL_MEMORY=234217728/TOTAL_MEMORY=268435456/g" -i Makefile.emEnv
    # https://github.com/kripken/emscripten/issues/6344
    # https://gitlab.com/odfplugfest/xmlmirror/issues/9
    sed -e "s/\$(JSONC_LDFLAGS) \$(ZLIB_LDFLAGS) \$(LIBXML20_LDFLAGS)/\$(JSONC_LDFLAGS) \$(LIBXML20_LDFLAGS) \$(ZLIB_LDFLAGS) /g" -i Makefile.emEnv
    # https://gitlab.com/odfplugfest/xmlmirror/issues/11
    sed -e "s/-o fastXmlLint.js/-s EXTRA_EXPORTED_RUNTIME_METHODS='[\"ccall\", \"cwrap\"]' -o fastXmlLint.js/g" -i Makefile.emEnv

    runHook postConfigure
  '';

  buildPhase = ''
    runHook preBuild

    make -f Makefile.emEnv

    runHook postBuild
  '';

  outputs = [
    "out"
    "doc"
  ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/share
    mkdir -p $doc/share/${name}

    cp Demo* $out/share
    cp -R codemirror-5.12 $out/share
    cp fastXmlLint.js* $out/share
    cp *.xsd $out/share
    cp *.js $out/share
    cp *.xhtml $out/share
    cp *.html $out/share
    cp *.json $out/share
    cp *.rng $out/share
    cp README.md $doc/share/${name}

    runHook postInstall
  '';

  checkPhase = ''
    runHook preCheck

    runHook postCheck
  '';
}
```

:::

## دیباگ (اشکال‌زدایی) {#declarative-debugging}

از `nix-shell -I nixpkgs=/some/dir/nixpkgs -A emscriptenPackages.libz` استفاده کنید و از آنجا می‌توانید مراحل را تک‌به‌تک طی کنید. این کار، ساخت یک `unit test` خوب یا فهرست کردن فایل‌های پروژه را آسان می‌کند.

1. `nix-shell -I nixpkgs=/some/dir/nixpkgs -A emscriptenPackages.libz`
2. `cd /tmp/`
3. `unpackPhase`
4. cd libz-1.2.3
5. `configurePhase`
6. `buildPhase`
7. ... هک خوش بگذرد …
