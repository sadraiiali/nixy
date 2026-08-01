# Swift {#swift}

کامپایلر Swift توسط بسته `swift` ارائه می‌شود:

```sh
# Compile and link a simple executable.
nix-shell -p swift --run 'swiftc -' <<< 'print("Hello world!")'
# Run it!
./main
```

بسته `swift` همچنین دستور `swift` را همراه با چند نکته ارائه می‌دهد:

- مدیر بسته‌های Swift (شناخته‌شده به عنوان SwiftPM) به‌صورت جداگانه در قالب `swiftpm` بسته‌بندی شده است. اگر به عملکردهایی مانند `swift build`، `swift run` یا `swift test` نیاز دارید، باید بسته `swiftpm` را نیز به کلوژر خود اضافه کنید.
- در Darwin، دستور `swift repl` نیازمند نصب Xcode است

```sh
cd /path/to/my/project
# Enter a Nix shell with the required tools.
nix-shell -p swift swiftpm swiftpm2nix
# First, make sure the workspace is up-to-date.
swift package resolve
# Now generate the Nix code.
swiftpm2nix
```

این کار فایل‌هایی را در پوشه `nix` ایجاد می‌کند که بخشی از عبارت Nix شما خواهند بود. گام بعدی، نوشتن آن عبارت است:

```nix
{
  stdenv,
  swift,
  swiftpm,
  swiftpm2nix,
  fetchFromGitHub,
}:

let
  # Pass the generated files to the helper.
  generated = swiftpm2nix.helpers ./nix;

in
stdenv.mkDerivation (finalAttrs: {
  pname = "myproject";
  version = "0.0.0";

  src = fetchFromGitHub {
    owner = "nixos";
    repo = "myproject";
    tag = finalAttrs.version;
    hash = "";
  };

  # Including SwiftPM as a nativeBuildInput provides a buildPhase for you.
  # This by default performs a release build using SwiftPM, essentially:
  #   swift build -c release
  nativeBuildInputs = [
    swift
    swiftpm
  ];

  # The helper provides a configure snippet that will prepare all dependencies
  # in the correct place, where SwiftPM expects them.
  configurePhase = ''
    runHook preConfigure

    ${generated.configure}

    runHook postConfigure
  '';

  installPhase = ''
    runHook preInstall

    # This is a special function that invokes swiftpm to find the location
    # of the binaries it produced.
    binPath="$(swiftpmBinPath)"
    # Now perform any installation steps.
    mkdir -p $out/bin
    cp $binPath/myproject $out/bin/

    runHook postInstall
  '';
})
```

### پرچم‌های ساخت سفارشی {#ssec-swiftpm-custom-build-flags}

اگر می‌خواهید پیکربندی متفاوتی نسبت به `release` بسازید:

```nix
{ swiftpmBuildConfig = "debug"; }
```

همچنین می‌توان پرچم‌های اضافی را به `swift build` ارسال کرد:

```nix
{ swiftpmFlags = [ "--disable-dead-strip" ]; }
```

`buildPhase` پیش‌فرض از قبل `-j` را برای ساخت موازی ارسال می‌کند.

اگر این دو گزینه سفارشی‌سازی کافی نیستند، `build

```nix
{ doCheck = true; }
```

این در واقع این دستور را اجرا می‌کند: `swift test -c release`

### پچ کردن وابستگی‌ها {#ssec-swiftpm-patching-dependencies}

در برخی موارد، ممکن است پچ کردن یک وابستگی SwiftPM ضروری باشد. وابستگی‌های SwiftPM در `.build/checkouts` قرار دارند، اما ابزار کمک‌رسان `swiftpm2nix` آن‌ها را به صورت پیوندهای نمادین (symlinks) به مسیرهای فقط-خواندنی `/nix/store` ارائه می‌دهد. برای پچ کردن آن‌ها، باید آن‌ها را قابل نوشتن کنیم.

تابع ویژه `swiftpmMakeMutable` برای جایگزین کردن پیوند نمادین (symlink) با یک نسخه قابل نوشتن در دسترس است:

```nix
{
  configurePhase = ''
    runHook preConfigure

    ${generated.configure}

    # Replace the dependency symlink with a writable copy.
    swiftpmMakeMutable swift-crypto
    # Now apply a patch.
    patch -p1 -d .build/checkouts/swift-crypto -i ${./some-fix.patch}

    runHook postConfigure
  '';
}
```

## ملاحظات برای ابزارهای ساخت سفارشی {#ssec-swift-considerations-for-custom-build-tools}

### پیوند دادن کتابخانه استاندارد {#ssec-swift-linking-the-standard-library}
