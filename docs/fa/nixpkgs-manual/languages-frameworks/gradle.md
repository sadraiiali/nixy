# Gradle {#gradle}

Gradle یک ابزار ساخت محبوب برای Java/Kotlin است. خود Gradle در حال حاضر ابزارهایی برای بازتولیدپذیر کردن تفکیک وابستگی‌ها ارائه نمی‌دهد، بنابراین Nixpkgs دارای یک پروکسی طراحی‌شده برای رهگیری درخواست‌های وب Gradle است تا وابستگی‌ها را ثبت کند تا بتوان آن‌ها را به روشی بازتولیدپذیر بازیابی نمود.

## ساخت یک بسته Gradle {#building-a-gradle-package}

در ادامه نحوه‌ی شکل‌گیری یک derivation معمولی آمده است:

```nix
stdenv.mkDerivation (finalAttrs: {
  pname = "pdftk";
  version = "3.3.3";

  src = fetchFromGitLab {
    owner = "pdftk-java";
    repo = "pdftk";
    tag = "v${finalAttrs.version}";
    hash = "sha256-ciKotTHSEcITfQYKFZ6sY2LZnXGChBJy0+eno8B3YHY=";
  };

  nativeBuildInputs = [
    gradle
    makeWrapper
  ];

  # if the package has dependencies, mitmCache must be set
  mitmCache = gradle.fetchDeps {
    inherit (finalAttrs) pname;
    data = ./deps.json;
  };

  # this is required for using mitm-cache on Darwin
  __darwinAllowLocalNetworking = true;

  gradleFlags = [ "-Dfile.encoding=utf-8" ];

  # defaults to "assemble"
  gradleBuildTask = "shadowJar";

  # will run the gradleCheckTask (defaults to "test")
  doCheck = true;

  installPhase = ''
    mkdir -p $out/{bin,share/pdftk}
    cp build/libs/pdftk-all.jar $out/share/pdftk

    makeWrapper ${lib.getExe jre} $out/bin/pdftk \
      --add-flags "-jar $out/share/pdftk/pdftk-all.jar"

    cp ${finalAttrs.src}/pdftk.1 $out/share/man/man1
  '';

  meta.sourceProvenance = with lib.sourceTypes; [
    fromSource
    binaryBytecode # mitm cache
  ];
})
```

برای به‌روزرسانی (یا مقداردهی اولیه) وابستگی‌ها، اسکریپت به‌روزرسانی را از طریق چیزی مانند `$(nix-build -A <pname>.mitmCache.

```nix
{
  lib,
  stdenv,
  gradle,
  # ...
  pdftk,
}:

stdenv.mkDerivation (finalAttrs: {
  # ...
  mitmCache = gradle.fetchDeps {
    pkg = pdftk;
    data = ./deps.json;
  };
})
```

این به شما امکان می‌دهد هر یک از آرگومان‌های `pkg` مورد استفاده برای اسکریپت به‌روزرسانی را `override` کنید (برای مثال، `pkg = pdftk.override { enableSomeFlag = true };`).

روش دوم استفاده از `finalAttrs.finalPackage` به این صورت است:

```nix
stdenv.mkDerivation (finalAttrs: {
  # ...
  mitmCache = gradle.fetchDeps {
    pkg = finalAttrs.finalPackage;
    data = ./deps.json;
  };
})
```
derivation / اشتقاق ساخت` where appropriate, or just `derivation` when referring to concept/code). Wait, let's keep `derivation` or `derivation / اشتقاق ساخت`. "درایویشن‌های pkg" or "derivation این pkg". Let's write `derivation` or `derivation / اشتق

آن true است. اگر ساخت به دلایل مبهمی با شکست مواجه شد، مقدار آن را روی false تنظیم کنید.

- `dontUseGradleConfigure` / `dontUseGradleBuild` / `dontUseGradleCheck` \- force disable the Gradle setup hook for certain phases.
  - `dontUseGradleConfigure` / `dontUseGradleBuild` / `dontUse
