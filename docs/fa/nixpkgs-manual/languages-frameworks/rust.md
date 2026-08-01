# Rust {#rust}

برای نصب کامپایلر Rust و cargo، عبارت زیر را قرار دهید

```nix
{
  environment.systemPackages = [
    rustc
    cargo
  ];
}
```

در `configuration.nix` خود وارد کنید یا با `nix-shell -p rustc cargo` آن‌ها را در دسترس قرار دهید.

برای نسخه‌های دیگر مانند ساخت‌های

```nix
{
  lib,
  fetchFromGitHub,
  rustPlatform,
}:

rustPlatform.buildRustPackage (finalAttrs: {
  pname = "ripgrep";
  version = "14.1.1";

  src = fetchFromGitHub {
    owner = "BurntSushi";
    repo = "ripgrep";
    tag = finalAttrs.version;
    hash = "sha256-gyWnahj1A+iXUQlQ1O1H1u7K5euYQOld9qWm99Vjaeg=";
  };

  cargoHash = "sha256-9atn5qyBDy4P6iUoHFhg+TV6Ur71fiah4oTJbBMeEy4=";

  meta = {
    description = "Fast line-oriented regex search tool, similar to ag and ack";
    homepage = "https://github.com/BurntSushi/ripgrep";
    license = lib.licenses.unlicense;
    maintainers = [ ];
  };
})
```

`buildRustPackage` به یک صفت (attribute) `cargoHash` نیاز دارد که بر روی تمام سورس‌های crate این بسته محاسبه می‌شود.

::: {.warning}
`cargoSha256` پیش از این منسوخ شده‌است و به نفع `cargoHash` که از هش‌های [SRI](https://www.w3.org/TR/SRI/) پشتیبانی می‌کند، حذف خواهد شد.

اگر هنوز از `cargoSha256` استفاده می‌کنید، می‌توانید به‌سادگی آن را با `cargoHash` جایگزین کرده و هش را مجدداً محاسبه کنید، یا هش sha256 اصلی را با استفاده از `nix-hash --to-sri --type sha256 "<original sha256>"` به هش SRI تبدیل نمایید.
:::

```nix
{ cargoHash = "sha256-l1vL2ZdtDRxSGvP0X/l3nMw8+6WF67KPutJEzUROjg8="; }
```

اگر این روش کارساز نبود، می‌توانید به کپی کردن فایل `Cargo.lock` به داخل Nixpkgs
و درون‌ریزی آن طبق آنچه در [بخش بعدی](#importing-a-cargo.lock-file) توصیف شده متوسل شوید.

هر دو نوع هش هنگام مشارکت در Nixpkgs مجاز هستند.
هش Cargo با قرار دادن یک چک‌سام ساختگی در
عبارت و یک بار ساخت بسته به دست می‌آید. سپس می‌توان چک‌سام درست را
از ساخت شکست‌خورده برداشت کرد. یک هش ساختگی می‌تواند برای

```nix
{ cargoHash = lib.fakeHash; }
```

طبق دستورالعمل‌های راهنمای روش‌های برتر [کتاب Cargo](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html)، برنامه‌های Rust همواره باید فایل `Cargo

```nix
rustPlatform.buildRustPackage (finalAttrs: {
  pname = "broot";
  version = "1.2.0";

  src = fetchCrate {
    inherit (finalAttrs) pname version;
    hash = "sha256-aDQA4A5mScX9or3Lyiv/5GyAehidnpKKE0grhbP1Ctc=";
  };

  cargoHash = "sha256-iDYh52rj1M5Uupvbx2WeDd/jvQZ+2A50V5rp5e2t7q4=";
  cargoDepsName = finalAttrs.pname;

  # ...
})
```

### درون‌ریزی یک فایل `Cargo.lock` {#importing-a-cargo.lock-file}

استفاده از یک هش وندورشده (`cargoHash`) هنگام

```nix
rustPlatform.buildRustPackage {
  pname = "myproject";
  version = "1.0.0";

  cargoLock = {
    lockFile = ./Cargo.lock;
  };

  # ...
}
```

این کار وابستگی‌ها را با استفاده از درایویشن‌های با خروجی ثابت از lockfile مشخص‌شده دریافت می‌کند.

یک نکته این است که `Cargo.lock` را نمی‌توان در `patchPhase` پچ کرد، زیرا این فاز پس از دریافت وابستگی‌ها اجرا می‌شود. اگر

```nix
rustPlatform.buildRustPackage {
  pname = "myproject";
  version = "1.0.0";

  cargoLock =
    let
      fixupLockFile = path: f (builtins.readFile path);
    in
    {
      lockFileContents = fixupLockFile ./Cargo.lock;
    };

  # ...
}
```

اگر مخزن سورس بالادست فاقد فایل `Cargo.lock` باشد، باید یک فایل به `src` اضافه کنید، زیرا این کار برای ساخت یک بسته Rust ضروری است. تنظیم `cargoLock.lockFile` یا `cargoLock.lockFileContents` به صورت خودکار یک فایل `Cargo.lock` به `src` اضافه نمی‌کند. یک راهکار ساده، استفاده از موارد زیر است:

```nix
{
  postPatch = ''
    ln -s ${./Cargo.lock} Cargo.lock
  '';
}
```

هش خروجی هر وابستگی که از یک منبع git استفاده می‌کند باید در صفت (attribute) `outputHashes` مشخص شود. برای مثال:

```nix
rustPlatform.buildRustPackage {
  pname = "myproject";
  version = "1.0.0";

  cargoLock = {
    lockFile = ./Cargo.lock;
    outputHashes = {
      "finalfusion-0.14.0" = "17f4bsdzpcshwh74w5z119xjy2if6l2wgyjy56v621skr2r8y904";
    };
  };

  # ...
}
```

اگر برای یک وابستگی git یک هش خروجی تعیین نکنید، ساخت بسته با شکست مواجه شده و به شما اطلاع می‌دهد که کدام crate باید اضافه شود. برای پیدا کردن هش درست، ابتدا

```nix
rustPlatform.buildRustPackage {
  pname = "myproject";
  version = "1.0.0";

  cargoLock = {
    lockFile = ./Cargo.lock;
    allowBuiltinFetchGit = true;
  };

  # ...
}
```

### ویژگی‌های Cargo {#cargo-features}

می‌توانید ویژگی‌های پیش‌فرض را با استفاده از `buildNoDefaultFeatures` غیرفعال کنید، و ویژگی‌های اضافی را با `buildFeatures` اضافه کنید.

اگر می‌خواهید از ویژگی‌های متفاوتی برای فاز بررسی استفاده کنید، می‌توانید از `checkNoDefaultFeatures` و `checkFeatures` استفاده کنید. این گزینه‌ها تنها به `cargo test` ارسال می‌شوند و نه به `cargo build`. در صورت تنظیم نشدن، به طور پیش‌فرض همان مقادیر `buildNoDefaultFeatures` و `buildFeatures` خواهند بود.

برای مثال:

```nix
rustPlatform.buildRustPackage {
  pname = "myproject";
  version = "1.0.0";

  buildNoDefaultFeatures = true;
  buildFeatures = [
    "color"
    "net"
  ];

  # disable network features in tests
  checkFeatures = [ "color" ];

  # ...
}
```

### کامپایل متقاطع {#cross-compilation}

به‌طور پیش‌فرض، بسته‌های Rust درست مانند هر بستهٔ دیگری برای پلتفرم هاست کامپایل می‌شوند. مقدار `--target` ارسال‌شده به ابزارهای Rust از روی همین پلتفرم محاسبه می‌شود.
به‌طور پیش‌فرض، این فرآیند `stdenv.hostPlatform.config` را دریافت کرده و مولفه‌هایی را که تفاوت آن‌ها شناخته‌شده‌است جایگزین می‌کند. اما روش‌هایی برای سفارشی‌سازی این آرگومان وجود دارد:

 - برای انتخاب یک تارگت متفاوت بر اساس نام، `stdenv.hostPlatform.rust.
```nix
   import <nixpkgs> {
     crossSystem = (import <nixpkgs/lib>).systems.examples.armhf-embedded // {
       rust.rustcTargetSpec = "thumbv7em-none-eabi";
     };
   }
   ```

نتیجه زیر را خواهد داشت:
```shell
   --target thumbv7em-none-eabi
   ```

- برای ارسال یک تارگت کاملاً سفارشی، `stdenv.hostPlatform.rust.rustcTargetSpec` را با مسیر فایل JSON مشخصات تارگت سفارشی تعریف کنید.

   توجه داشته باشید که برخی ابزارها مانند Cargo و برخی کریت‌ها مانند `cc` از نام فایل JSON تارگت استفاده می‌کنند. بنابراین، مستقیماً از `./path/to/target-spec.json` استفاده نکنید، زیرا توسط Nix تغییر نام داده خواهد شد. در عوض، آن را در یک پوشه قرار دهید و از `"${./path/to/dir}/target-spec.json"` استفاده کنید. این پوشه باید تنها شامل همین یک فایل باشد تا از تغییرات غیرمرتبط که باعث ساخت‌های مجدد غیرضروری می‌شوند جلوگیری شود.

   برای مثال:
```nix
   import <nixpkgs> {
     crossSystem = {
       config = "mips64el-unknown-linux-gnuabi64";
       # gcc = ...; # Config for C compiler omitted
       rust.rustcTargetSpec = "${./rust}/mips64el_mips3-unknown-linux-gnuabi64.json";
     };
   }
   ```

منجر به نتیجه زیر خواهد شد:
```shell
   --target /nix/store/...-rust/mips64el_mips3-unknown-linux-gnuabi64.json
   ```

### اجرای تست‌های بسته {#running-package-tests}

هنگام استفاده از `buildRustPackage`، فاز `checkPhase` به صورت پیش‌فرض فعال است و `cargo test` را روی بسته‌ای که باید ساخته شود اجرا می‌کند. برای اطمینان از اینکه کدهای منبع را دو بار کامپایل نکنیم و فرآورده‌های ساخت که در زمان اجرا استفاده خواهند شد را واقعاً تست کنیم، تست‌ها به صورت پیش‌فرض در حالت `release` اجرا خواهند شد.

با این حال، در برخی موارد مجموعه تست یک

```nix
rustPlatform.buildRustPackage {
  # ...
  checkType = "debug";
}
```

لطفاً توجه داشته باشید که کد در اینجا دو بار کامپایل خواهد شد: یک بار در حالت `release` برای `buildPhase`، و بار دیگر در حالت `debug` برای `checkPhase`.

پرچم‌های تست، برای نمونه `--package foo`، می‌توانند از طریق صفت (

```nix
rustPlatform.buildRustPackage {
  # ...
  checkFlags = [
    # reason for disabling test
    "--skip=example::tests:example_test"
  ];
}
```

#### استفاده از `cargo-nextest` {#using-cargo-nextest}

تست‌ها را می‌توان با تنظیم `useNextest = true` به کمک [cargo-nextest](https://github.com/nextest-rs/nextest) اجرا کرد. همان گزینه‌ها همچنان اعمال می‌شوند، اما nextest مجموعه متفاوتی از آرگومان‌ها را می‌پذیرد و ممکن است لازم باشد تنظیمات برای سازگاری با cargo-nextest تطبیق داده شوند.

```nix
rustPlatform.buildRustPackage {
  # ...
  useNextest = true;
}
```

#### تنظیم `test-threads` {#setting-test-threads}

`buildRustPackage` به طور پیش‌فرض از نخ‌های تست موازی استفاده می‌کند،
گاهی ممکن است غیرفعال کردن آن ضروری باشد تا تست‌ها به صورت متوالی اجرا شوند.

```nix
rustPlatform.buildRustPackage {
  # ...
  dontUseCargoParallelTests = true;
}
```

### ساخت یک بسته در حالت `debug` {#building-a-package-in-debug-mode}

به‌طور پیش‌فرض، `buildRustPackage` از حالت `release` برای ساخت‌ها استفاده می‌کند. اگر لازم است یک بسته در حالت `debug` ساخته شود، می‌توان آن را به این صورت پیکربندی کرد:

```nix
rustPlatform.buildRustPackage {
  # ...
  buildType = "debug";
}
```

در این سناریو، `checkPhase` نیز در حالت `debug` اجرا خواهد شد.

### روال‌های سفارشی `build`/`install` {#custom-buildinstall-procedures}

برخی بسته‌ها ممکن

```nix
rustPlatform.buildRustPackage {
  # ...
  cargoPatches = [
    # a patch file to add/update Cargo.lock in the source code
    ./add-Cargo.lock.patch
  ];
}
```

### کامپایل کردن بسته‌های غیر Rust که شامل کد Rust هستند {#compiling-non-rust-packages-that-include-rust-code}

چندین بسته غیر Rust از کد Rust برای بخش‌های حساس به عملکرد یا امنیت استفاده می‌کنند. `rustPlatform` چند تابع و قلاب (hook) را ارائه می‌دهد که می‌توان از آن‌ها برای یکپارچه‌سازی Cargo در بسته‌های غیر Rust استفاده کرد.

#### تأمین محلی (Vendoring) وابستگی‌ها {#vendoring-of-dependencies}

از آنجا که دسترسی به شبکه در ساخت‌های ایزوله شده (Sandboxed) مجاز نیست، وابستگی‌های crate مربوط به Rust باید با استفاده از یک دریافت‌کننده به دست آیند

```nix
{
  cargoDeps = rustPlatform.fetchCargoVendor {
    inherit src;
    hash = "sha256-BoHIN/519Top1NUBjpB/oEMqi86Omt3zTQcXFWqrek0=";
  };
}
```

صفت `src` الزامی است، همین‌طور هشی که از طریق یکی از صفت‌های `hash` مشخص می‌شود. صفت‌های اختیاری زیر نیز می‌توانند استفاده شوند:

* `name`: نامی که برای فایل

```nix
{ cargoDeps = rustPlatform.importCargoLock { lockFile = ./Cargo.lock; }; }
```

اگر فایل `Cargo.lock` شامل وابستگی‌های git باشد، هش‌های خروجی آن‌ها باید مشخص شوند، چرا که از طریق فایل قفل در دسترس نیستند. برای مثال:

```nix
{
  cargoDeps = rustPlatform.importCargoLock {
    lockFile = ./Cargo.lock;
    outputHashes = {
      "rand-0.8.3" = "0ya2hia3cn31qa8894s3av2s8j5bjwb6yq92k0jsnlx7jid0jwqa";
    };
  };
}
```

یو کد منبع"
- "building" -> "ساخت" / "در حال ساخت"

Everything strictly follows rules and glossary requirements.
اگر یک هش خروجی برای یک وابستگی git مشخص نکنید، ساخت `cargoDeps` با شکست مواجه شده و به شما اطلاع می‌دهد که کدام کریت (crate) باید اضافه شود. برای یافتن هش درست، می‌توانید ابتدا از `lib.fakeSha25

```nix
{
  fetchFromGitHub,
  buildPythonPackage,
  cargo,
  rustPlatform,
  rustc,
  setuptools-rust,
}:

buildPythonPackage rec {
  pname = "tokenizers";
  version = "0.10.0";

  src = fetchFromGitHub {
    owner = "huggingface";
    repo = "tokenizers";
    tag = "python-v${version}";
    hash = "sha256-rQ2hRV52naEf6PvRsWVCTN7B1oXAQGmnpJw4iIdhamw=";
  };

  cargoDeps = rustPlatform.fetchCargoVendor {
    inherit
      pname
      version
      src
      sourceRoot
      ;
    hash = "sha256-RO1m8wEd5Ic2M9q+zFHeCJWhCr4Sv3CEWd08mkxsBec=";
  };

  sourceRoot = "${src.name}/bindings/python";

  nativeBuildInputs = [
    cargo
    rustPlatform.cargoSetupHook
    rustc
    setuptools-rust
  ];

  # ...
}
```

در برخی پروژه‌ها، crate مربوط به Rust در پوشه اصلی کد منبع Python قرار ندارد. در چنین مواردی، می‌توان از صفت (attribute) `cargoRoot` برای مشخص کردن پوشه crate نسبت به `sourceRoot` استفاده کرد. در مثال زیر، همان‌طور که در صفت (attribute) `cargoRoot` مشخص شده، crate در `src/rust` قرار دارد. توجه داشته باشید که باید `cargoRoot` را به `fetchCargoVendor` نیز پاس دهید.

```nix
{
  buildPythonPackage,
  fetchPypi,
  rustPlatform,
  setuptools-rust,
  openssl,
}:

buildPythonPackage rec {
  pname = "cryptography";
  version = "3.4.2"; # Also update the hash in vectors.nix

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-xGDilsjLOnls3MfVbGKnj80KCUCczZxlis5PmHzpNcQ=";
  };

  cargoDeps = rustPlatform.fetchCargoVendor {
    inherit
      pname
      version
      src
      cargoRoot
      ;
    hash = "sha256-ctUt8maCjnGddKPf+Ii++wKsAXA1h+JM6zKQNXXwJqQ=";
  };

  cargoRoot = "src/rust";

  # ...
}
```

#### بستهٔ Python با استفاده از `maturin` {#python-package-using-maturin}

بسته‌های Python که از [Maturin](https://github.com/PyO3/maturin) استفاده می‌کنند می‌توانند با `fetchCargoVendor`، `cargoSetupHook` و `maturinBuildHook` ساخته شوند. برای نمونه، درایویشن (جزئی) زیر بسته Python به نام `retworkx` را می‌سازد. از `fetchCargoVendor` و `cargoSetupHook` برای دریافت و آماده‌سازی وابستگی‌های crate استفاده می‌شود. از `maturinBuildHook` نیز برای انجام فرآیند ساخت استفاده می‌شود.

```nix
{
  lib,
  buildPythonPackage,
  rustPlatform,
  fetchFromGitHub,
}:

buildPythonPackage rec {
  pname = "retworkx";
  version = "0.6.0";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "Qiskit";
    repo = "retworkx";
    tag = version;
    hash = "sha256-11n30ldg3y3y6qxg3hbj837pnbwjkqw3nxq6frds647mmmprrd20=";
  };

  cargoDeps = rustPlatform.fetchCargoVendor {
    inherit pname version src;
    hash = "sha256-QsPCQhNZKYCAogQriQX6pBYQUDAIUsEdRX/63dAqTzg=";
  };

  nativeBuildInputs = with rustPlatform; [
    cargoSetupHook
    maturinBuildHook
  ];

  # ...
}
```

#### بسته Rust ساخته‌شده با `meson` {#rust-package-built-with-meson}

برخی پروژه‌ها، به‌ویژه برنامه‌های GNOME، به جای فراخوانی مستقیم Cargo، با سیستم ساخت Meson ساخته می‌شوند. استفاده از `rustPlatform.buildRustPackage` ممکن است برنامه اصلی را با موفقیت بسازد، اما فایل‌های مرتبط وجود نخواه

```nix
{
  lib,
  stdenv,
  fetchFromGitLab,
  meson,
  ninja,
  pkg-config,
  rustPlatform,
  rustc,
  cargo,
  wrapGAppsHook4,
  blueprint-compiler,
  libadwaita,
  libsecret,
  tinysparql,
}:

stdenv.mkDerivation (finalAttrs: {
  pname = "health";
  version = "0.95.0";

  src = fetchFromGitLab {
    domain = "gitlab.gnome.org";
    owner = "World";
    repo = "health";
    tag = finalAttrs.version;
    hash = "sha256-PrNPprSS98yN8b8yw2G6hzTSaoE65VbsM3q7FVB4mds=";
  };

  cargoDeps = rustPlatform.fetchCargoVendor {
    inherit (finalAttrs) pname version src;
    hash = "sha256-eR1ZGtTZQNhofFUEjI7IX16sMKPJmAl7aIFfPJukecg=";
  };

  nativeBuildInputs = [
    meson
    ninja
    pkg-config
    rustPlatform.cargoSetupHook
    rustc
    cargo
    wrapGAppsHook4
    blueprint-compiler
  ];

  buildInputs = [
    libadwaita
    libsecret
    tinysparql
  ];

  # ...
})
```

### کامپایل بستهٔ `wasm32-wasip1` {#compiling-wasm32-wasip1-package}

```nix
pkgsCross.wasm32-wasip1.callPackage (
  {
    fetchFromGitHub,
    rustPlatform,
    lld,
  }:
  rustPlatform.buildRustPackage (finalAttrs: {
    pname = "zellij-harpoon";
    version = "0.3.0";

    src = fetchFromGitHub {
      owner = "Nacho114";
      repo = "harpoon";
      tag = "v${finalAttrs.version}";
      hash = "sha256-JmYcbzxIF6qZs2/RKuspHqNpyDibGp9CVQJj47y/BOQ=";
    };

    cargoHash = "sha256-lsv5Wssakni18jif++fPo3Z5WyBtvPsGpWwG3abR7jQ=";

    # these two lines are currently required
    env.RUSTFLAGS = "-C linker=wasm-ld";
    nativeBuildInputs = [ lld ];
  })
) { }
```

## `buildRustCrate`: کامپایل کردن کریت‌های Rust با استفاده از Nix به جای Cargo {#compiling-rust-crates-using-nix-instead-of-cargo}

### عملکرد ساده {#simple-operation}

هنگام اجرا، `cargo build` فایلی به نام `Cargo.lock` تولید می‌کند که شامل نسخه‌های ثابت‌شدهٔ همهٔ وابستگی‌ها است. Nixpkgs شامل ابزاری به نام `crate2Nix` (`nix-shell -p crate2nix`) است که می‌توان از آن برای تبدیل یک `Cargo.lock` به یک عبارت نیکس (Nix expression) استفاده کرد.

```nix
with import <nixpkgs> { };
((import ./hello.nix).hello { }).override {
  crateOverrides = defaultCrateOverrides // {
    hello = attrs: { buildInputs = [ openssl ]; };
  };
}
```

در اینجا، انتظار می‌رود `crateOverrides` یک مجموعه ویژگی باشد که در آن کلید، نام crate بدون شماره نسخه و مقدار، یک تابع است. این تابع تمام صفات ارسال‌شده به `buildRustCrate` را به عنوان نخستین آرگومان دریافت می‌کند و مجموعه‌ای را برمی‌گرداند که شامل تمام صفاتی است که باید بازنویسی شوند.

برای موارد پیچیده‌تر، مانند زمانی که بخش‌هایی از derivation متعلق به crate به نسخه crate وابسته است، می‌توان آرگومان `attrs`

```nix
with import <nixpkgs> { };
((import ./hello.nix).hello { }).override {
  crateOverrides = defaultCrateOverrides // {
    hello =
      attrs:
      lib.optionalAttrs (lib.versionAtLeast attrs.version "1.0") {
        postPatch = ''
          substituteInPlace lib/zoneinfo.rs \
            --replace-fail "/usr/share/zoneinfo" "${tzdata}/share/zoneinfo"
        '';
      };
  };
}
```

موقعیت دیگر زمانی است که می‌خواهیم یک وابستگی تودرتو را بازنشانی کنیم. این کار در واقع دقیقاً به همان روش انجام می‌شود، چرا که پارامتر `crateOverrides` به وابستگی‌های crate فرستاده می‌شود. برای نمونه، جهت بازنشانی ورودی‌های ساخت برای crate مربوط به `libc` در مثال بالا، که در آن `libc` یک وابستگیِ crate اصلی است، می‌توانیم به این صورت عمل کنیم:

```nix
with import <nixpkgs> { };
((import hello.nix).hello { }).override {
  crateOverrides = defaultCrateOverrides // {
    libc = attrs: { buildInputs = [ ]; };
  };
}
```

### پیکربندی گزینه‌ها و فازها {#options-and-phases-configuration}

در واقع، بازنشانی‌های معرفی‌شده در بخش قبلی کلی‌تر هستند. پارامترهای متعدد دیگری نیز قابل بازنشانی هستند:

- نسخهٔ `rustc` استفاده‌شده برای کامپایل کردن کریت:
```nix
  (hello { }).override { rust = pkgs.rust; }
  ```

- این‌که ساخت در حالت release انجام شود یا حالت debug (به‌طور پیش‌فرض حالت release):
```nix
  (hello { }).override { release = false; }
  ```

- این‌که آیا دستورات ارسال‌شده به `rustc` هنگام ساخت چاپ شوند یا خیر
  (معادل `--verbose` در cargo:
```nix
  (hello { }).override { verbose = false; }
  ```

- آرگومان‌های اضافی برای ارسال به `rustc`:
```nix
  (hello { }).override { extraRustcOpts = "-Z debuginfo=2"; }
  ```

- آرگومان‌های اضافی پاس‌داده‌شده به `rustc` هنگامی که کریت یک proc-macro است، که جایگزین `extra
```nix
  (myProcMacro { }).override { extraRustcOptsForProcMacro = [ ]; }
  ```

- سقف سطح lint پاس‌داده‌شده به `rustc`. مقدار پیش‌فرض آن `null` است، که در صورت خالی بودن `lints` به طور خودکار به
```nix
  (hello { }).override { capLints = "warn"; }
  ```

- پیکربندی Lint مطابق با جدول `[lints]` در Cargo.toml. کلیدها نام ابزارها هستند (`rust`، `clippy`، `rust
```nix
  (hello { }).override {
    lints.rust = {
      unsafe_code = "forbid";
      unused = {
        level = "deny";
        priority = -1;
      };
    };
  }
  ```

- این‌که آیا کریت به جای `rustc` با `clippy-driver` کامپایل شود یا خیر.
  اسکریپت‌های ساخت (`build.rs`) از همان `rustc` ساده استفاده می‌کنند. مقدار پیش‌فرض `capLints` که
```nix
  (hello { }).override {
    useClippy = true;
    capLints = "warn";
    extraRustcOpts = [
      "-Dwarnings"
      "-Wclippy::all"
    ];
  }
  ```

هنگام استفاده از زنجیره ابزار Rust که `clippy-driver` اختصاصی خود را به همراه دارد (rust-overlay، Fenix)، آن را از طریق `clippy` ارسال کنید تا sysroot مطابقت داشته باشد:
```nix
  (hello { }).override {
    rust = myToolchain;
    clippy = myToolchain;
    useClippy = true;
    capLints = "warn";
  }
  ```

- فازها، درست مانند هر derivation دیگری، می‌توانند با استفاده از صفات زیر مشخص شوند: `preUnpack`، `postUnpack`، `prePatch`، `patches
```nix
  (hello { }).override {
    preConfigure = ''
      echo "pub const PATH=\"${hi.out}\";" >> src/path.rs"
    '';
  }
  ```

### راه‌اندازی `nix-shell` {#setting-up-nix-shell}

در بسیاری از مواقع می‌خواهید کد را از داخل `nix-shell` توسعه دهید

```nix
with import <nixpkgs> { };

stdenv.mkDerivation {
  name = "rust-env";
  nativeBuildInputs = [
    rustc
    cargo

    # Example Build-time Additional Dependencies
    pkg-config
  ];
  buildInputs = [
    # Example Run-time Additional Dependencies
    openssl
  ];

  # Set Environment Variables
  RUST_BACKTRACE = 1;
}
```

اکنون باید بتوانید موارد زیر را اجرا کنید:

```ShellSession
$ nix-shell --pure
$ cargo build
$ cargo test
```

## استفاده از زنجیره‌ابزارهای Rust نگه‌داری‌شده توسط جامعهٔ کاربری {#using-community-maintained-rust-toolchains}

::: {.note}
پروژه‌های زیر نمی‌توانند در Nixpkgs استفاده شوند، زیرا [Import From Derivation](https://nixos.org/manual/nix/unstable/language/import-from-derivation) (IFD) در Nixpkgs مجاز نیست.
برای بسته‌بندی مواردی که به Rust nightly نیاز دارند، گاهی می‌توان از `RUSTC_BOOT

```nix
with import <nixpkgs> { };
let
  fenix = callPackage (fetchFromGitHub {
    owner = "nix-community";
    repo = "fenix";
    # commit from: 2023-03-03
    rev = "e2ea04982b892263c4d939f1cc3bf60a9c4deaa1";
    hash = "sha256-AsOim1A8KKtMWIxG+lXh5Q4P2bhOZjoUhFWJ1EuZNNk=";
  }) { };
in
mkShell {
  name = "rust-env";
  nativeBuildInputs = [
    # Note: to use stable, just replace `default` with `stable`
    fenix.default.toolchain

    # Example Build-time Additional Dependencies
    pkg-config
  ];
  buildInputs = [
    # Example Run-time Additional Dependencies
    openssl
  ];

  # Set Environment Variables
  RUST_BACKTRACE = 1;
}
```

این را در `shell.nix` ذخیره کنید، سپس اجرا کنید:

```ShellSession
$ rustc --version
rustc 1.69.0-nightly (13471d3b2 2023-03-02)
```

تو ببینید در حال استفاده از nightly هستید.

اورلی Rust مربوط به Oxalica مثال‌های کامل‌تری از `shell.nix` (و کامپایل متقاطع) را در [

```nix
with import <nixpkgs> {
  overlays = [
    (import (fetchTarball "https://github.com/oxalica/rust-overlay/archive/master.tar.gz"))
  ];
};
let
  rustPlatform = makeRustPlatform {
    cargo = rust-bin.selectLatestNightlyWith (toolchain: toolchain.default);
    rustc = rust-bin.selectLatestNightlyWith (toolchain: toolchain.default);
  };

in
rustPlatform.buildRustPackage (finalAttrs: {
  pname = "ripgrep";
  version = "14.1.1";

  src = fetchFromGitHub {
    owner = "BurntSushi";
    repo = "ripgrep";
    tag = finalAttrs.version;
    hash = "sha256-gyWnahj1A+iXUQlQ1O1H1u7K5euYQOld9qWm99Vjaeg=";
  };

  cargoHash = "sha256-9atn5qyBDy4P6iUoHFhg+TV6Ur71fiah4oTJbBMeEy4=";

  # Tests require network access. Skipping.
  doCheck = false;

  meta = {
    description = "Fast line-oriented regex search tool, similar to ag and ack";
    homepage = "https://github.com/BurntSushi/ripgrep";
    license = with lib.licenses; [
      mit
      unlicense
    ];
    maintainers = with lib.maintainers; [ ];
  };
})
```

برای امتحان کردن آن قطعه‌کد، مراحل زیر را دنبال کنید:
1. قطعه‌کد بالا را با نام `default.nix` در آن پوشه ذخیره کنید
2. با cd وارد آن پوشه شوید و `nix

```nix
(
  final: prev: # lib.optionalAttrs prev.stdenv.targetPlatform.isAarch64
  {
    rust_1_72 = lib.updateManyAttrsByPath [
      {
        path = [
          "packages"
          "stable"
        ];
        update =
          old:
          old.overrideScope (
            final: prev: {
              rustc-unwrapped = prev.rustc-unwrapped.overrideAttrs (_: {
                src = lib.cleanSource /git/scratch/rust;
                # do *not* put passthru.isReleaseTarball=true here
              });
            }
          );
      }
    ] prev.rust_1_72;
  })
```

اگر مشکلی که در حال عیب‌یابی آن هستید فقط هنگام کامپایل متقاطع بروز می‌کند، می‌توانید `lib.optionalAttrs` را در مثال بالا از حالت کامنت خارج کرده و `isA

```bash
git bisect {good,bad}  # depending on result of last build
git submodule update --init
CARGO_NET_OFFLINE=false cargo vendor \
  --sync ./src/tools/cargo/Cargo.toml \
  --sync ./src/tools/rust-analyzer/Cargo.toml \
  --sync ./compiler/rustc_codegen_cranelift/Cargo.toml \
  --sync ./src/bootstrap/Cargo.toml
nix-build $NIXPKGS -A package-broken-by-rust-changes
```

بالا (`git submodule update --init` و `cargo vendor`) به دسترسی به شبکه نیاز دارند، بنابراین متأسفانه نمی‌توان آن‌ها را از داخل درایویشن `
