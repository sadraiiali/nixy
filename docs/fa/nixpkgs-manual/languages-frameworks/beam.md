# زبان‌های BEAM (Erlang، Elixir و LFE) {#sec-beam}

## مقدمه {#beam-introduction}

در این نوشتار و عبارت‌های Nix مرتبط، ما از واژه _BEAM_ برای توصیف محیط استفاده می‌کنیم. BEAM نام ماشین مجازی Erlang است و تا آنجا که به ما مربوط می‌شود، از دیدگاه بسته‌بندی، تمام زبان‌هایی که روی BEAM اجرا می‌شوند قابل تعویض هستند. آنچه تغییر می‌کند، مانند سیستم ساخت، برای کاربران هر بسته BEAM مشخص شفاف است، بنابراین تفاوتی میان آن‌ها قائل نمی‌شویم.

## نسخه‌های موجود و جدول زمان‌بندی منسوخ‌سازی {#available-versions-and-deprecations-schedule}

### Erlang OTP {#erlang}

Nixpkgs از Erlang بالادستی در [چرخه حیات پشتیبانی](https://erlang.org/download/otp_versions_tree.html) آن پیروی می‌کند و تا ۳ نسخه منتشرشده اخیر Erlang را در دسترس نگه می‌دارد. به دلیل زمان‌بندی انتشار بالادستی و NixOS، این امر ممکن است به معنای حذف قدیمی‌ترین نسخه پیش از خروج کامل آن از پشتیبانی توسط بالادستی باشد.

### Elixir {#elixir}

Nixpkgs از [برنامه رسمی منسوخ‌سازی Elixir](https://hexdocs.pm/elixir/compatibility-and-deprecations.html) پیروی می‌کند و تا ۵ نسخه منتشرشده اخیر Elixir را در دسترس نگه می‌دارد.

## ساختار {#beam-structure}

تمامی عبارت‌های مربوط به BEAM از طریق مجموعه‌بسته‌های سطح بالا در دسترس هستند. توصیه می‌شود برای اطمینان از سازگاری نسخه‌ها، با یک مجموعه‌بسته واحد کار کنید.

- `beamPackages` - نسخه پیش‌فرض OTP
- `beamMinimalPackages` - نسخه پیش‌فرض OTP، بدون wxwidgets، که حدود ۱ گیگابایت در اندازه closure صرفه‌جویی می‌کند

همچنین مجموعه‌بسته‌های مخصوص نسخه OTP نیز وجود دارند، برای مثال برای OTP 28:

- `beam28Packages`
- `beamMinimal28Packages`

در داخل هر مجموعه‌بسته موارد زیر قرار دارند:

- خود erlang (نسخه از مجموعه‌بسته گرفته می‌شود)
- مفسرها: elixir (نسخه‌های متعدد، مانند elixir_1_18) و lfe
- بسته‌ها: rebar3، hex، و غیره
- سازنده‌ها: mixRelease، buildRebar3، و غیره
- قلاب‌ها: برای ترکیب سازنده‌ها و بسته‌ها

برای استفاده از یک Elixir غیرپیش‌فرض، حفظ سازگاری مابقی مجموعه‌بسته بسیار مهم است، بنابراین توصیه می‌شود از `.extend` استفاده کنید. این کار اطمینان می‌دهد سازنده‌هایی مانند `mixRelease`، `fetchMixDeps` و `buildMix` همگی Elixir بازنشانی‌شده را دریافت می‌کنند:

```nix
let
  beamPackages = beam27Packages.extend (self: super: { elixir = self.elixir_1_18; });
in
beamPackages.mixRelease {
  # ...
}
```

## ابزارهای ساخت {#beam-build-tools}

### Rebar3 {#beam-build-tools-rebar3}

ما نسخه‌ای از Rebar3 را تحت `beamPackages.rebar3` ارائه می‌دهیم. همچنین یک تابع کمکی برای دریافت وابستگی‌های Rebar3 از یک lockfile تحت `beamPackages.fetchRebar3Deps` ارائه می‌کنیم.

ما همچنین نسخه‌ای از Rebar3 به همراه افزونه‌ها را تحت `beamPackages.rebar3WithPlugins` ارائه می‌دهیم. این بسته، تابعی است که دو آرگومان می‌گیرد: `plugins`، فهرستی از درایویشن‌های nix برای گنجاندن به عنوان افزونه (که تنها در صورت مشخص شدن در `rebar.config` بارگیری می‌شوند)، و `globalPlugins` که همیشه باید توسط rebar3 بارگیری شوند. مثال: `beamPackages.rebar3WithPlugins { globalPlugins = [beamPackages.pc]; }`.

هنگام افزودن یک افزونه جدید، مهم است که صفت `name` با اتمی که توسط rebar3 برای ارجاع به افزونه استفاده می‌شود یکسان باشد.

### Erlang.mk {#beam-build-tools-erlangmk}

Erlang.mk دقیقاً همان‌طور که انتظار می‌رود کار می‌کند. یک فرآیند خودراه‌اندازی (bootstrap) وجود دارد که باید اجرا شود و توسط درایویشن `buildErlangMk` پشتیبانی می‌شود.

### Mix {#beam-build-tools-mix}

برای برنامه‌های Elixir که از [mix release](https://hexdocs.pm/mix/Mix.Release.html) استفاده می‌کنند، از سازنده `mixRelease` برای ایجاد انتشار (release) استفاده کنید. برای جزئیات بیشتر به مثال‌ها مراجعه کنید.

همچنین یک تابع کمکی `buildMix` وجود دارد که رفتار آن به `buildErlangMk` و `buildRebar3` نزدیک‌تر است. تفاوت اصلی این است که `mixRelease` یک انتشار (release) ایجاد می‌کند، در حالی که `buildMix` فقط بسته را می‌سازد، که برای کتابخانه‌ها و سایر وابستگی‌ها مفیدتر است.

## نحوه نصب بسته‌های BEAM {#how-to-install-beam-packages}

برای استفاده از هر یک از این سازنده‌ها در محیط خود، با مسیر صفت آن‌ها تحت `beamPackages` (یا یک مجموعه بسته BEAM دیگر) به آن‌ها ارجاع دهید، مانند `beamPackages.rebar3`:

::: {.example #ex-beam-ephemeral-shell}
# شل زودگذر

```ShellSession
$ nix-shell -p beamPackages.rebar3
```
:::

::: {.example #ex-beam-declarative-shell}
# شل اعلانی (declarative)

```nix
let
  pkgs = import <nixpkgs> {
    config = { };
    overlays = [ ];
  };
in
pkgs.mkShell { packages = [ pkgs.beamPackages.rebar3 ]; }
```
:::

## بسته‌بندی برنامه‌های BEAM {#packaging-beam-applications}

### برنامه‌های Erlang {#packaging-erlang-applications}

#### بسته‌های Rebar3 {#rebar3-packages}

سازنده (Builder) `beamPackages.buildRebar3` می‌تواند برای ساخت یک derivation استفاده شود که نحوهٔ ساخت پروژهٔ Rebar3 را متوجه می‌شود.

#### بسته‌های Erlang.mk {#erlang-mk-packages}

Erlang.mk عملکردی مشابه Rebar3 دارد، با این تفاوت که به جای `beamPackages.buildRebar3` از `beamPackages.buildErlangMk` استفاده می‌کنیم.

اگر یک بسته نیاز به کامپایل کردن کد بومی از طریق مکانیسم کامپایل پورت Erlang.mk داشته باشد، `compilePorts = true;` را به derivation اضافه کنید.

### برنامه‌های Elixir {#packaging-elixir-applications}

#### بسته‌های Mix {#mix-packages}

از `beamPackages.mixRelease` برای ایجاد یک انتشار (release) به مفهوم mix استفاده می‌شود. وابستگی‌ها باید با `beamPackages.fetchMixDeps` دریافت شده و به آن پاس داده شوند.

#### mixRelease - نمونه Elixir Phoenix {#mix-release-elixir-phoenix-example}

۳ گام وجود دارد: وابستگی‌های فرانت‌اند (جاوااسکریپت)، وابستگی‌های بک‌اند (الیکسیر) و derivation نهایی که هر دوی آن‌ها را کنار هم قرار می‌دهد.

##### mixRelease - وابستگی‌های فرانت‌اند (جاوااسکریپت) {#mix-release-javascript-deps}

برای پروژه‌های Phoenix، در داخل Nixpkgs می‌توانید از `fetchYarnDeps` یا `buildNpmPackage` استفاده کنید. نمونه‌ای با `buildNpmPackage` را می‌توانید در [اینجا](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/pl/plausible/package.nix) و نمونه‌ای با `fetchYarnDeps` را در [اینجا](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/pi/pinchflat/package.nix) بیابید.

##### mixRelease - وابستگی‌های بک‌اند (mix) {#mix-release-mix-deps}

۲ روش برای بسته‌بندی وابستگی‌های بک‌اند وجود دارد: یا mix2nix به ازای هر وابستگی، یا استفاده از یک derivation با خروجی ثابت (FOD).

هنگام نوشتن یک پروژهٔ Elixir با هدف‌گیری `mixRelease`، می‌توانید استفاده از [deps_nix](https://github.com/code-supply/deps_nix) همراه با `mixNixDeps` را نیز مد نظر قرار دهید. ابزار `deps_nix` از وابستگی‌های git پشتیبانی می‌کند، اما قصد دارد مستقیماً به `mix.exs` پروژه اضافه شود.

##### mix2nix {#mix2nix}

ابزار `mix2nix` یک ابزار رابط خط فرمان (CLI) موجود در Nixpkgs است. این ابزار یک عبارت نیکس (Nix expression) از فایل `mix.lock` تولید می‌کند. این ابزار در سری ابزارهای 2nix کاملاً استاندارد است.

توجه داشته باشید که در حال حاضر mix2nix نمی‌تواند وابستگی‌های git موجود در فایل mix.lock را پردازش کند. اگر وابستگی‌های git دارید، می‌توانید آن‌ها را به صورت دستی اضافه کنید (به [این نمونه](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/pl/pleroma/package.nix) مراجعه کنید) یا از روش FOD استفاده کنید.

مزیت استفاده از mix2nix این است که Nix کل گراف وابستگی‌های شما را خواهد شناخت. هنگام به‌روزرسانی یک وابستگی، این امر باعث ساخت مجدد (Rebuild) کامل و بارگیری تمام وابستگی‌ها نخواهد شد، در حالی که FOD این کار را انجام می‌دهد.

گام‌های عملی:

- دستور `mix2nix > mix_deps.nix` را در مخزن بالادست (upstream) اجرا کنید.
- `mixNixDeps = with pkgs; import ./mix_deps.nix { inherit lib beamPackages; };` را به عنوان یک آرگومان به mixRelease پاس دهید.

اگر وابستگی‌های git وجود دارند:

- باید نسخه را به صورت مصنوعی در mix.exs ثابت کنید و mix.lock را با نسخهٔ ثابت دوباره تولید کنید (در مخزن بالادست). این کار به شما امکان می‌دهد `mix2nix > mix_deps.nix` را اجرا کنید.
- از فایل mix_deps.nix، وابستگی‌هایی که نسخه‌های git داشتند را حذف کنید و آن‌ها را به عنوان بازنویسی / بازنشانی (override) به تابع import پاس دهید.

```nix
{
  mixNixDeps = import ./mix.nix {
    inherit beamPackages lib;
    overrides = (
      final: prev: {
        # mix2nix does not support git dependencies yet,
        # so we need to add them manually
        prometheus_ex = beamPackages.buildMix rec {
          name = "prometheus_ex";
          version = "3.0.5";

          # Change the argument src with the git src that you actually need
          src = fetchFromGitLab {
            domain = "git.pleroma.social";
            group = "pleroma";
            owner = "elixir-libraries";
            repo = "prometheus.ex";
            rev = "a4e9beb3c1c479d14b352fd9d6dd7b1f6d7deee5";
            hash = "sha256-U17LlN6aGUKUFnT4XyYXppRN+TvUBIBRHEUsfeIiGOw=";
          };
          # you can re-use the same beamDeps argument as generated
          beamDeps = with final; [ prometheus ];
        };
      }
    );
  };
}
```

برای اینکه هش با src جدید Git شما مطابقت پیدا کند، لازم است فرآیند ساخت را یک بار اجرا کنید.

##### FOD {#fixed-output-derivation}

یک fixed output derivation وابستگی‌های mix را از اینترنت بارگیری می‌کند. برای تضمین بازتولیدپذیری، یک هش ارائه خواهد شد. توجه داشته باشید که mix نسبتاً بازتولیدپذیر است. تولید یک هش متفاوت در هر بار اجرا توسط یک FOD مشاهده نشده است (برخلاف npm که احتمال آن نسبتاً بالا است). برای نمونه استفاده از FOD، [akkoma](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/ak/akkoma/package.nix) را ببینید.

مراحل عملی

- با آرگومان زیر برای mixRelease شروع کنید

```nix
{
  mixFodDeps = fetchMixDeps {
    pname = "mix-deps-${pname}";
    inherit src version;
    hash = lib.fakeHash;
  };
}
```

اولین ساخت خطایی درباره مقدار هش خواهد داد، پس از آن می‌توانید آن را با مقدار پیشنهادی جایگزین کنید.

توجه داشته باشید که اگر پس از جایگزینی مقدار، Nix هش دیگری را پیشنهاد کند، به این معنی است که mix وابستگی‌ها را به صورت بازتولیدپذیر دریافت نمی‌کند. در این حالت یک FOD کار نخواهد کرد و مجبور خواهید بود از mix2nix استفاده کنید.

##### mixRelease - مثال {#mix-release-example}

ساختار فایل `default.nix` برای یک پروژه Phoenix به شکل زیر خواهد بود.

```nix
{
  # beam27Packages or beam29Packages is available if you need a particular version
  beamPackages,
}:
let
  pname = "your_project";
  version = "0.0.1";

  src = builtins.fetchgit {
    url = "ssh://git@github.com/your_id/your_repo";
    rev = "replace_with_your_commit";
  };

  # if using mix2nix you can use the mixNixDeps attribute
  mixFodDeps = beamPackages.fetchMixDeps {
    pname = "mix-deps-${pname}";
    inherit src version;
    # nix will complain and tell you the right value to replace this with
    hash = lib.fakeHash;
    mixEnv = ""; # default is "prod", when empty includes all dependencies, such as "dev", "test".
    # if you have build time environment variables add them here
    MY_ENV_VAR = "my_value";
  };
in
beamPackages.mixRelease {
  inherit
    src
    pname
    version
    mixFodDeps
    ;
  # if you have build time environment variables add them here
  MY_ENV_VAR = "my_value";

  postBuild = ''
    # for external task you need a workaround for the no deps check flag
    # https://github.com/phoenixframework/phoenix/issues/2690
    mix do deps.loadpaths --no-deps-check, phx.digest
    mix phx.digest --no-deps-check
  '';
}
```

راه‌اندازی نیازمند مراحل زیر است:

- اطلاعات محرمانه خود را به متغیرهای محیطی زمان اجرا منتقل کنید. برای اطلاعات بیشتر به [مستندات runtime.exs](https://hexdocs.pm/mix/Mix.Tasks.Release.html#module-runtime-configuration) مراجعه کنید. در یک ساخت تازه Phoenix، این به این معنی است که هر دو متغیر `DATABASE_URL` و `SECRET_KEY` باید به `runtime.exs` منتقل شوند.
- بسته به اینکه پروژه از npm یا yarn استفاده می‌کند، با استفاده از `fetchNpmDeps`/`buildNpmPackage` یا `fetchYarnDeps` یک عبارت نیکس (Nix expression) برای وابستگی‌های فرانت‌اند خود تولید کنید
- آن تغییرات را کامیت کرده و پوش کنید
- اکنون می‌توانید `nix-build .` را اجرا کنید
- برای اجرای نسخه انتشار، متغیر محیطی `RELEASE_TMP` را روی پوشه‌ای تنظیم کنید که برنامه‌تان دسترسی نوشتن به آن را دارد. از این پوشه برای ذخیره تنظیمات BEAM استفاده خواهد شد.

#### نمونه‌ای از ایجاد یک سرویس برای یک پروژه Elixir - Phoenix {#example-of-creating-a-service-for-an-elixir---phoenix-project}

برای ایجاد یک سرویس با نسخه انتشار خود، می‌توانید فایل `service.nix` را با موارد زیر به پروژه خود اضافه کنید

```nix
{
  config,
  pkgs,
  lib,
  ...
}:

let
  release = pkgs.callPackage ./default.nix { };
  release_name = "app";
  working_directory = "/home/app";
in
{
  systemd.services.${release_name} = {
    wantedBy = [ "multi-user.target" ];
    after = [
      "network.target"
      "postgresql.target"
    ];
    # note that if you are connecting to a postgres instance on a different host
    # postgresql.target should not be included in the requires.
    requires = [
      "network-online.target"
      "postgresql.target"
    ];
    description = "my app";
    environment = {
      # RELEASE_TMP is used to write the state of the
      # VM configuration when the system is running
      # it needs to be a writable directory
      RELEASE_TMP = working_directory;
      # can be generated in an elixir console with
      # Base.encode32(:crypto.strong_rand_bytes(32))
      RELEASE_COOKIE = "my_cookie";
      MY_VAR = "my_var";
    };
    serviceConfig = {
      Type = "exec";
      DynamicUser = true;
      WorkingDirectory = working_directory;
      # Implied by DynamicUser, but just to emphasize due to RELEASE_TMP
      PrivateTmp = true;
      ExecStart = ''
        ${release}/bin/${release_name} start
      '';
      ExecStop = ''
        ${release}/bin/${release_name} stop
      '';
      ExecReload = ''
        ${release}/bin/${release_name} restart
      '';
      Restart = "on-failure";
      RestartSec = 5;
    };
    unitConfig = {
      StartLimitBurst = 3;
      StartLimitInterval = 10;
    };
    # disksup requires bash
    path = [ pkgs.bash ];
  };

  # in case you have migration scripts or you want to use a remote shell
  environment.systemPackages = [ release ];
}
```

## نحوه توسعه {#how-to-develop}

### ایجاد یک شل {#creating-a-shell}

معمولاً، ما نیاز داریم یک فایل `shell.nix` ایجاد کنیم و توسعه‌ی خود را داخل محیط مشخص‌شده در آن انجام دهیم. کافی است نسخه Erlang خود و هر مفسر دیگری را نصب کنید، و سپس از ابزارهای ساخت معمولی خود استفاده کنید. به عنوان مثال، با Elixir:

```nix
{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
let
  # pin OTP via beam27Packages/beam28Packages/... and Elixir via .extend
  beamPackages = beam27Packages.extend (self: super: { elixir = self.elixir_1_18; });
in
mkShell { buildInputs = [ beamPackages.elixir ]; }
```

### استفاده از یک اورلی {#beam-using-overlays}

اگر برای تغییر برخی صفات یک derivation / اشتقاق ساخت نیاز به استفاده از یک اورلی دارید، به عنوان مثال اگر به یک رفع اشکال از نسخه‌ای نیاز دارید که هنوز در Nixpkgs در دسترس نیست، می‌توانید صفاتی مانند `version` (و `hash` مربوط به آن) را بازنشانی کرده و سپس از این اورلی در محیط توسعه خود استفاده کنید:

#### `shell.nix` {#beam-using-overlays-shell.nix}

```nix
let
  elixir_1_18_1_overlay = (
    self: super: {
      elixir_1_18 = super.elixir_1_18.override {
        version = "1.18.1";
        hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
      };
    }
  );
  pkgs = import <nixpkgs> { overlays = [ elixir_1_18_1_overlay ]; };
in
with pkgs;
mkShell { buildInputs = [ elixir_1_18 ]; }
```

#### پروژه Elixir - Phoenix {#elixir---phoenix-project}

در اینجا یک نمونه `shell.nix` آورده شده است.

```nix
with import <nixpkgs> { };

let
  # pin OTP via beam27Packages/beam28Packages/... and Elixir via .extend
  beamPackages = beam27Packages.extend (self: super: { elixir = self.elixir_1_18; });

  # define packages to install
  basePackages = [
    git
    beamPackages.elixir
    nodejs
    postgresql_14
    # formatting js file
    prettier
  ];

  inputs = basePackages ++ lib.optionals stdenv.hostPlatform.isLinux [ inotify-tools ];

  # define shell startup command
  hooks = ''
    # this allows mix to work on the local directory
    mkdir -p .nix-mix .nix-hex
    export MIX_HOME=$PWD/.nix-mix
    export HEX_HOME=$PWD/.nix-mix
    # make hex from Nixpkgs available
    # `mix local.hex` will install hex into MIX_HOME and should take precedence
    export MIX_PATH="${beamPackages.hex}/lib/erlang/lib/hex/ebin"
    export PATH=$MIX_HOME/bin:$HEX_HOME/bin:$PATH
    export LANG=C.UTF-8
    # keep your shell history in iex
    export ERL_AFLAGS="-kernel shell_history enabled"

    # postgres related
    # keep all your db data in a folder inside the project
    export PGDATA="$PWD/db"

    # phoenix related env vars
    export POOL_SIZE=15
    export DB_URL="postgresql://postgres:postgres@localhost:5432/db"
    export PORT=4000
    export MIX_ENV=dev
    # add your project env vars here, word readable in the nix store.
    export ENV_VAR="your_env_var"
  '';

in
mkShell {
  buildInputs = inputs;
  shellHook = hooks;
}
```

مقداردهی اولیه پروژه نیازمند گام‌های زیر است:

- ایجاد پوشه db با `initdb ./db` (داخل پوشه پروژه mix شما)
- ایجاد کاربر postgres با `createuser postgres -ds`
- ایجاد دیتابیس با `createdb db`
- راه‌اندازی نمونه postgres با `pg_ctl -l "$PGDATA/server.log" start`
- افزودن پوشه `/db` به فایل `.gitignore` خود
- می‌توانید سرور Phoenix خود را راه‌اندازی کرده و با `iex -S mix phx.server` یک شل دریافت کنید
