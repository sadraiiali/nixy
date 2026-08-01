# تست‌کننده‌ها {#chap-testers}

این فصل چند سازندهٔ آزمایش را توصیف می‌کند که در فضای نام `testers` در دسترس هستند.

## `hasPkgConfigModules` {#tester-hasPkgConfigModules}

<!-- نام انکر قدیمی جهت کارکرد درست پیوندها -->
[]{#tester-hasPkgConfigModule}
بررسی می‌کند که آیا یک بسته فهرست مشخصی از ماژول‌های `pkg-config` را در دسترس قرار می‌دهد یا خیر.
اگر آرگومان `moduleNames` حذف شود، `hasPkgConfigModules` از `meta.pkgConfigModules` استفاده خواهد کرد.

:::{.example #ex-haspkgconfigmodules-defaultvalues}

# بررسی اینکه ماژول‌های `pkg-config` با استفاده از مقادیر پیش‌فرض در دسترس قرار گرفته‌اند

```nix
{
  passthru.tests.pkg-config = testers.hasPkgConfigModules { package = finalAttrs.finalPackage; };

  meta.pkgConfigModules = [ "libfoo" ];
}
```

:::

:::{.example #ex-haspkgconfigmodules-explicitmodules}

# بررسی اینکه ماژول‌های `pkg-config` با استفاده از نام‌های صریح ماژول ارائه شده‌اند

```nix
{
  passthru.tests.pkg-config = testers.hasPkgConfigModules {
    package = finalAttrs.finalPackage;
    moduleNames = [ "libfoo" ];
  };
}
```

:::

## `hasCmakeConfigModules` {#tester-hasCmakeConfigModules}

بررسی می‌کند که آیا یک بسته فهرست داده‌شده‌ای از ماژول‌های `*config.cmake` را ارائه می‌دهد یا خیر.
توجه داشته باشید که `moduleNames` استفاده‌شده در `find_package` در cmake به بزرگ و کوچک بودن حروف حساس هستند.

:::{.example #ex-hascmakeconfigmodules}

# بررسی اینکه ماژول‌های `*config.cmake` با استفاده از نام‌های صریح ماژول در دسترس قرار گرفته‌اند

```nix
{
  passthru.tests.cmake-config = testers.hasCmakeConfigModules {
    package = finalAttrs.finalPackage;
    moduleNames = [ "Foo" ];
  };
}
```

:::

## `lycheeLinkCheck` {#tester-lycheeLinkCheck}

لینک‌های یک سایت ایستای بسته‌بندی‌شده را با [`بسته lychee`](https://search.nixos.org/packages?show=lychee&type=packages&query=lychee) بررسی کنید.

شما می‌توانید از Nix برای ساخت بازتولیدپذیر وب‌سایت‌های ایستا، مانند مستندات نرم‌افزار، استفاده کنید.
برخی بسته‌ها مستندات را در خروجی‌های `out` یا `doc` خود نصب می‌کنند، یا شاید یک بسته اختصاصی داشته باشید که در آن سایت ایستای خود را با اجرای یک مولد، مانند [Hugo](https://gohugo.io/) یا [mdBook](https://rust-lang.github.io/mdBook/)، در یک derivation بازتولیدپذیر کرده‌اید.

اگر سایت ایستایی دارید که امکان ساخت آن با Nix وجود دارد، می‌توانید از `lycheeLinkCheck` برای بررسی صحت ابرپیوندهای موجود در سایت خود استفاده کنید و این کار را به‌عنوان بخشی از جریان کاری Nix و ادغام مداوم (CI) خود انجام دهید.

:::{.example #ex-lycheelinkcheck}

# بررسی ابرپیوندها در مستندات `nix`

```nix
testers.lycheeLinkCheck { site = nix.doc + "/share/doc/nix/manual"; }
```

:::

### مقدار بازگشتی {#tester-lycheeLinkCheck-return}

این تست‌کننده بسته‌ای تولید می‌کند که خروجی‌های کاربردی تولید نمی‌کند، بلکه تنها در صورتی موفق می‌شود که ابرپیوندهای موجود در سایت شما درست باشند. لاگ ساخت، لینک‌های خراب را فهرست خواهد کرد.

این ابزار دارای دو حالت است:

- ساخت derivation / اشتقاق ساخت بازگردانده‌شده؛ فرآیند ساخت آن بررسی می‌کند که ابرپیوندهای داخلی درست باشند. این حالت در محیط ایزوله شده (Sandboxed) اجرا می‌شود، بنابراین ابرپیوندهای خارجی را بررسی نخواهد کرد، اما سریع و قابل اعتماد است.

- فراخوانی صفت (attribute) `.online` با [`nix run`](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-run) ([آزمایشی](https://nixos.org/manual/nix/stable/contributing/experimental-features#xp-feature-nix-command)). این حالت خارج از محیط ایزوله شده (Sandboxed) اجرا می‌شود و بررسی می‌کند که هر دو ابرپیوند داخلی و خارجی درست باشند.
  مثال:
```shell
  nix run nixpkgs#lychee.tests.ok.online
  ```

### ورودی‌ها {#tester-lycheeLinkCheck-inputs}

`site` (مسیر یا derivation) {#tester-lycheeLinkCheck-param-site}

: مسیر فایل‌ها برای بررسی.

`relocatable` (بولین، اختیاری) {#tester-lycheeLinkCheck-param-relocatable}

: آیا انتظار می‌رود وب‌سایت قابل جابه‌جایی باشد، یعنی از هر پیشوند مسیر URL قابل سرویس‌دهی باشد یا خیر.

  وقتی `true` باشد (پیش‌فرض)، پیوندهای نسبی نسبت به ریشه (که با `/` شروع می‌شوند) به عنوان خطا در نظر گرفته می‌شوند، زیرا هنگامی که سایت از یک زیرمسیر سرویس‌دهی شود یا از طریق URLهای `file://` باز شود، خراب می‌شوند.

  وقتی `false` باشد، پیوندهای نسبی نسبت به ریشه بر اساس پوشه `site` حل‌وفصل می‌شوند.

`remap` (مجموعه ویژگی، اختیاری) {#tester-lycheeLinkCheck-param-remap}

: یک مجموعه ویژگی که در آن نام صفات عبارت‌های منظم (regular expression) هستند.
  مقادیر باید رشته‌ها، درایویشن‌ها یا مقادیر مسیر باشند.

  در پیکربندی پیش‌فرض بررسی بازگردانده‌شده، URLهای خارجی تنها زمانی بررسی می‌شوند که صفت `.online` را اجرا کنید.

  با افزودن نگاشت‌های مجدد، می‌توانید با ارائه‌ی یک جایگزین از سیستم‌فایل، به‌صورت آفلاین درست بودن URLهای مربوط به منابع خارجی را بررسی کنید.

  پیش از بررسی وجود یک URL، عبارت‌های منظم منطبق شده و با مقادیر مربوط به خود جایگزین می‌شوند.

  مثال:
```nix
  {
    "https://nix\\.dev/manual/nix/[a-z0-9.-]*" = "${nix.doc}/share/doc/nix/manual";
    "https://nixos\\.org/manual/nix/(un)?stable" =
      "${emptyDirectory}/placeholder-to-disallow-old-nix-docs-urls";
  }
  ```

مسیرهای انبار در مقادیر صفت به صورت خودکار پیشوند `file://` می‌گیرند، زیرا lychee این را برای مسیرهای موجود در سیستم‌فایل نیاز دارد.
  اگر این مسئله ایجاد مشکل می‌کند، یا اگر نیاز دارید ترتیب انجام جایگزینی‌ها را کنترل کنید، به جای آن از `extraConfig.remap` استفاده کنید.

`extraConfig` (مجموعه صفت) {#tester-lycheeLinkCheck-param-extraConfig}

: پیکربندی اضافی برای ارسال به `lychee` در [فایل پیکربندی](https://github.com/lycheeverse/lychee/blob/master/lychee.example.toml) آن.
  این پیکربندی به‌طور خودکار به TOML [ترجمه می‌شود](https://nixos.org/manual/nixos/stable/index.html#sec-settings-nix-representable).

  مثال: `{ "include_verbatim" = true; }`

`extraArgs` (لیست رشته‌ها، اختیاری) {#tester-lycheeLinkCheck-param-extraArgs}

: آرگومان‌های خط فرمان اضافی برای ارسال به فراخوانی `lychee`.
  این آرگومان‌ها در هر دو حالت آفلاین (ساخت) و [`online`](#tester-lycheeLinkCheck-return) ارسال می‌شوند.

  مثال: `[ "--format" "json" ]`

`lychee` (derivation، اختیاری) {#tester-lycheeLinkCheck-param-lychee}

: بسته `lychee` برای استفاده.

## `shellcheck` {#tester-shellcheck}

اجرای فایل‌ها از طریق `shellcheck`، یک ابزار تحلیل ایستا برای اسکریپت‌های شل، که در صورت وجود هرگونه مشکل شکست می‌خورد.

:::{.example #ex-shellcheck}
# اجرای `testers.shellcheck`

یک اسکریپت تک

```nix
testers.shellcheck {
  name = "script";
  src = ./script.sh;
}
```

چند فایل

```nix
let
  inherit (lib) fileset;
in
testers.shellcheck {
  name = "nixbsd-activate";
  src = fileset.toSource {
    root = ./.;
    fileset = fileset.unions [
      ./lib.sh
      ./nixbsd-activate
    ];
  };
}
```

:::

### ورودی‌ها {#tester-shellcheck-inputs}

`name` (رشته، اختیاری)
: نام تست.
  در آینده `name` الزامی خواهد شد زیرا قابلیت ردگیری شکست‌های تست را به میزان زیادی بهبود می‌بخشد، اما در حال حاضر برای جلوگیری از شکستن استفاده‌های موجود، به‌صورت اختیاری باقی مانده است.
  مقدار پیش‌فرض آن `run-shellcheck` است.
  در صورت ارائه `name`، نام derivation تولیدشده توسط تست‌کننده برابر با `shellcheck-${name}` خواهد بود.

`src` (از نوع مسیر)
: مسیر اسکریپت(های) شل برای بررسی.
  این می‌تواند یک فایل تنها یا یک پوشه حاوی فایل‌های شل باشد.
  تمام فایل‌های موجود در `src` بررسی خواهند شد، بنابراین ممکن است بخواهید به جای کل یک پوشه، سورس مبتنی بر `fileset` را ارائه دهید.

### مقدار بازگشتی {#tester-shellcheck-return}

یک derivation که `shellcheck` را روی اسکریپت(های) داده‌شده اجرا می‌کند و در صورت عدم یافتن هیچ مشکلی، یک خروجی خالی تولید می‌کند.
اگر `shellcheck` هرگونه مشکلی پیدا کند، فرآیند ساخت (Build) با شکست مواجه خواهد شد.

## `shfmt` {#tester-shfmt}

اجرای فایل‌ها از طریق `shfmt` (یک فرمت‌کننده اسکریپت شل)، که در صورت تغییر فرمت هر یک از فایل‌ها با شکست مواجه می‌شود.

:::{.example #ex-shfmt}
# اجرای `testers.shfmt`

یک اسکریپت تنها

```nix
testers.shfmt {
  name = "script";
  src = ./script.sh;
}
```

چندین فایل

```nix
let
  inherit (lib) fileset;
in
testers.shfmt {
  name = "nixbsd";
  src = fileset.toSource {
    root = ./.;
    fileset = fileset.unions [
      ./lib.sh
      ./nixbsd-activate
    ];
  };
}
```

:::

### ورودی‌ها {#tester-shfmt-inputs}

`name` (رشته)
: نام تست.
  `name` الزامی است زیرا قابلیت پیگیری شکست‌های تست را به شکل قابل توجهی بهبود می‌بخشد.
  نام derivation تولیدشده توسط این تست‌کننده `shfmt-${name}` است.

`src` (مشابه مسیر / path-like)
: مسیر اسکریپت‌(های) شل جهت بررسی.
  این می‌تواند یک فایل تنها یا یک پوشه حاوی فایل‌های شل باشد.
  تمام فایل‌های موجود در `src` بررسی خواهند شد، بنابراین ممکن است بخواهید به جای کل یک پوشه، سورس مبتنی بر `fileset` ارائه دهید.

`indent` (عدد صحیح، اختیاری)
: تعداد فاصله‌ها برای تورفتگی.
  مقدار پیش‌فرض `2` است.
  مقدار `0` با تب (tab) تورفتگی ایجاد می‌کند.

### مقدار بازگشتی {#tester-shfmt-return}

یک derivation که `shfmt` را روی اسکریپت‌(های) داده‌شده اجرا می‌کند و در صورت موفقیت، خروجی خالی تولید می‌کند.
اگر `shfmt` هر چیزی را دوباره قالب‌بندی کند، ساخت (Build) با شکست مواجه خواهد شد.

## `testVersion` {#tester-testVersion}

بررسی می‌کند که خروجی حاصل از اجرای یک دستور، شامل رشتهٔ نسخهٔ مشخص‌شده به عنوان یک کلمهٔ کامل باشد.

نکته: این بررسِی‌ای است که شما به `passthru.tests` اضافه می‌کنید و عمدتاً توسط OfBorg اجرا می‌شود، اما در Hydra اجرا نمی‌شود. اگر می‌خواهید شکست در بررسی نسخه به‌طور کامل مانع ساخت (Build) شود، [`versionCheckHook`](#versioncheckhook) ابزاری است که به دنبال آن هستید (و برای ساخت‌های سریع توصیه می‌شود). انگیزهٔ افزودن هر یک از این بررسی‌ها عبارت است از:

- شناسایی خطاهای پیوند پویا (dynamic linking) و مواردی از این دست، و متغیرهای محیطی مفقود که باید از طریق بسته‌بندی (wrapping) اضافه شوند.
- حفاظت احتمالی در برابر ساخت اشتباهی یک نسخهٔ نادرست، به عنوان مثال هنگام استفاده از یک هش «قدیمی» در یک derivation با خروجی ثابت (fixed-output derivation).

به طور پیش‌فرض، دستوری که باید اجرا شود از صفت (attribute) داده‌شده برای `package` استنتاج می‌شود:
ابتدا `meta.mainProgram` بررسی می‌شود و در صورت عدم وجود، به `pname` یا `name` رجوع می‌کند.
آرگومان پیش‌فرض برای این دستور `--version` است و نسخه‌ای که باید بررسی شود نیز از صفت `package` داده‌شده استنتاج خواهد شد.

:::{.example #ex-testversion-hello}

# بررسی نسخهٔ یک برنامه با استفاده از تمام مقادیر پیش‌فرض

این نمونه دستور `hello --version` را اجرا می‌کند و سپس بررسی می‌کند که نسخهٔ بستهٔ `hello` در خروجی این دستور وجود داشته باشد.

```nix
{ passthru.tests.version = testers.testVersion { package = hello; }; }
```

:::

:::{.example #ex-testversion-different-commandversion}

# بررسی نسخه برنامه با استفاده از یک دستور مشخص و رشته نسخه مورد انتظار

این مثال دستور `leetcode -V` را اجرا کرده و سپس بررسی می‌کند که `leetcode 0.4.2` به عنوان یک کلمه کامل (جداشده با فاصله) در خروجی دستور وجود داشته باشد.
این بدان معناست که خروجی‌ای مانند "leetcode 0.4.21" در تست‌ها رد می‌شود و خروجی‌ای مانند "You're running leetcode 0.4.2" در تست‌ها قبول می‌شود.

یک کاربرد رایج صفت (attribute) `version` مشخص کردن `version = "v${version}"` است.

```nix
{
  version = "0.4.2";

  passthru.tests.version = testers.testVersion {
    package = leetcode-cli;
    command = "leetcode -V";
    version = "leetcode ${version}";
  };
}
```

:::

## `testBuildFailure` {#tester-testBuildFailure}

اطمینان حاصل کنید که یک ساخت (Build) با موفقیت انجام نمی‌شود. این قابلیت برای تست کردن تست‌کننده‌ها مفید است.

این تابع یک derivation همراه با یک بازنشانی (override) روی سازنده (Builder) برمی‌گرداند که اثرات زیر را دارد:

 - ناکام گذاشتن ساخت زمانی که سازنده اصلی با موفقیت به پایان می‌رسد
 - انتقال `$out` به `$out/result` در صورت وجود (با این فرض که `out` خروجی پیش‌فرض است)
 - ذخیره لاگ ساخت در `$out/testBuildFailure.log` (همچنین)

اگرچه `testBuildFailure` به گونه‌ای طراحی شده است که تغییرات در محیط سازنده اصلی را به حداقل برساند، اما برخی تغییرات کوچک اجتناب‌ناپذیر هستند:

 - فایل `$TMPDIR/testBuildFailure.log` موجود است. این فایل نباید حذف شود.
 - `stdout` و `stderr` به جای tty، یک پایپ (pipe) هستند. این موضوع می‌تواند بهبود یابد.
 - یک یا دو فرآیند اضافی در طول اجرای سازنده اصلی در محیط ایزوله (sandbox) حضور دارند.
 - هش‌های derivation و خروجی متفاوت هستند، اما غیرعادی نیستند.
 - این derivation شامل یک وابستگی به `buildPackages.bash` و `expect-failure.sh` است که طوری ساخته شده تا شامل یک وابستگی متعدی به `buildPackages.coreutils` و احتمالاً موارد بیشتری باشد.
   این موارد به `PATH` یا هر متغیر محیطی دیگری اضافه نمی‌شوند، بنابراین مشاهده آن‌ها باید دشوار باشد.

:::{.example #ex-testBuildFailure-showingenvironmentchanges}

# بررسی شکست خوردن یک ساخت، و تایید تغییرات ایجادشده در طول ساخت

```nix
runCommand "example"
  {
    failed = testers.testBuildFailure (
      runCommand "fail" { } ''
        echo ok-ish >$out
        echo failing though
        exit 3
      ''
    );
  }
  ''
    grep -F 'ok-ish' $failed/result
    grep -F 'failing though' $failed/testBuildFailure.log
    [[ 3 = $(cat $failed/testBuildFailure.exit) ]]
    touch $out
  ''
```

:::

## `testBuildFailure'` {#tester-testBuildFailurePrime}

این تستر قابلیت‌های ارائه‌شده توسط [`testers.testBuildFailure`](#tester-testBuildFailure) را در بر می‌گیرد تا با ساده‌سازی بررسی کد خروج سازنده و تایید وجود ورودی‌ها در لاگ مربوط به سازنده، نوشتن بررسی‌ها را آسان‌تر کند.
علاوه بر این، کاربران می‌توانند یک اسکریپت حاوی بررسی‌های تکمیلی مشخص کنند و از طریق متغیر `failed` به نتیجه‌ی اعمال `testers.testBuildFailure` دسترسی داشته باشند.

نکته: اگر هیچ‌یک از بررسی‌ها با شکست مواجه نشوند، این تستر یک خروجی خالی تولید کرده و با موفقیت خارج می‌شود؛ نیازی به اجرای `touch "$out"` در `script` نیست.

:::{.example #ex-testBuildFailurePrime-doc-example}

# بررسی شکست یک ساخت و تایید تغییرات ایجادشده در طول ساخت

با استفاده مجدد از مثال موجود در [`testers.testBuildFailure`](#ex-testBuildFailure-showingenvironmentchanges)، می‌توانیم ببینیم که چگونه بررسی‌های رایج ساده‌تر می‌شوند و نیاز به `runCommand` برطرف می‌شود:

```nix
testers.testBuildFailure' {
  drv = runCommand "doc-example" { } ''
    echo ok-ish >"$out"
    echo failing though
    exit 3
  '';
  expectedBuilderExitCode = 3;
  expectedBuilderLogEntries = [ "failing though" ];
  script = ''
    grep --silent -F 'ok-ish' "$failed/result"
  '';
}
```

:::

### ورودی‌ها {#tester-testBuildFailurePrime-inputs}

`drv` (derivation)

: derivation شکست‌خورده‌ای که باید با `testBuildFailure` پوشانده (wrap) شود.

`name` (رشته، اختیاری)

: نام تست.
  در صورت عدم ارائه، مقدار پیش‌فرض آن برابر با `testBuildFailure-${(testers.testBuildFailure drv).name}` خواهد بود.

`expectedBuilderExitCode` (عدد صحیح، اختیاری)

: کد خروج مورد انتظار از سازنده (builder) مربوط به `drv`.
  در صورت عدم ارائه، مقدار پیش‌فرض آن برابر با `1` است.

`expectedBuilderLogEntries` (آرایه‌ای از مقادیر رشته‌مانند، اختیاری)

: فهرستی از مقادیر رشته‌مانند که باید از طریق تطابق دقیق در لوگ سازنده (builder) پیدا شوند.
  در صورت عدم ارائه، مقدار پیش‌فرض آن برابر با `[ ]` است.

  نکته: الگوها و عبارت‌های منظم (regular expressions) پشتیبانی نمی‌شوند.

`script` (رشته، اختیاری)

: رشته‌ای شامل بررسی‌های اضافی جهت اجرا.
  در صورت عدم ارائه، مقدار پیش‌فرض آن برابر با `""` است.
  نتیجه‌ی `testers.testBuildFailure drv` از طریق متغیر `failed` در دسترس است.
  به عنوان مثال، لوگ سازنده (builder) در مسیر `"$failed/testBuildFailure.log"` قرار دارد.

### مقدار بازگشتی {#tester-testBuildFailurePrime-return}

تست‌کننده خروجی خالی تولید می‌کند و تنها زمانی موفق می‌شود که بررسی‌ها با استفاده از `expectedBuilderExitCode`، `expectedBuilderLogEntries` و `script` موفقیت‌آمیز باشند.

## `testEqualContents` {#tester-testEqualContents}

بررسی این‌که دو مسیر محتوای یکسانی دارند.

`assertion` (رشته)

: پیامی که قبل از مقایسه، بعد از `:Checking` چاپ می‌شود.

`expected` (مسیر یا مقداری قابل تبدیل به مسیر انبار)

: مسیر مربوط به محتوای مورد انتظار [شیء سیستم‌فایل]

`actual` (مقداری قابل تبدیل به مسیر انبار) <!-- path value is possible, but wrong in practice, but let's not bother readers with our predictions -->

: مسیر مربوط به محتوای واقعی شیء سیستم‌فایل جهت بررسی

`postFailureMessage` (رشته)

: پیامی که در صورت عدم تطابق دقیق محتوای شیء سیستم‌فایل در دو مسیر، در انتها چاپ می‌شود.

`checkMetadata` (بولین)

: این‌که آیا در صورت وجود تفاوت در متادیتا (مانند دسترسی‌ها یا مالکیت)، تست شکست بخورد یا خیر.
  مقدار پیش‌فرض `true` است.

:::{.example #ex-testEqualContents-toyexample}

# بررسی این‌که دو مسیر محتوای یکسانی دارند

```nix
testers.testEqualContents {
  assertion = "sed -e performs replacement";
  expected = writeText "expected" ''
    foo baz baz
  '';
  actual =
    runCommand "actual"
      {
        # not really necessary for a package that's in stdenv
        nativeBuildInputs = [ gnused ];
        base = writeText "base" ''
          foo bar baz
        '';
      }
      ''
        sed -e 's/bar/baz/g' $base >$out
      '';
  # if applicable
  postFailureMessage = ''
    The bar-baz replacer produced an unexpected result.
    If the new behavior is acceptable and validated against the bar-baz specification, run ./adopt-new-bar-baz-result.sh to adjust this test and require the new behavior.
  '';
}
```

:::

## `testEqualArrayOrMap` {#tester-testEqualArrayOrMap}

بررسی می‌کند که آرایه‌های Bash (از جمله آرایه‌های متناظر، که به آن‌ها "maps" گفته می‌شود) به‌درستی مقداردهی شده باشند.

از این می‌توان برای اطمینان از ثبت قلاب‌های راه‌اندازی به یک ترتیب مشخص، یا برای نوشتن تست‌های واحد برای توابع شل که آرایه‌ها را تغییر می‌دهند، استفاده کرد.

:::{.example #ex-testEqualArrayOrMap-test-function-add-cowbell}

# تست تابعی که مقداری را به یک آرایه اضافه می‌کند

```nix
testers.testEqualArrayOrMap {
  name = "test-function-add-cowbell";
  valuesArray = [
    "cowbell"
    "cowbell"
  ];
  expectedArray = [
    "cowbell"
    "cowbell"
    "cowbell"
  ];
  script = ''
    addCowbell() {
      local -rn arrayNameRef="$1"
      arrayNameRef+=( "cowbell" )
    }

    nixLog "appending all values in valuesArray to actualArray"
    for value in "''${valuesArray[@]}"; do
      actualArray+=( "$value" )
    done

    nixLog "applying addCowbell"
    addCowbell actualArray
  '';
}
```

:::

### ورودی‌ها {#tester-testEqualArrayOrMap-inputs}

نکته: به‌صورت داخلی، این تستر از `__structuredAttrs` برای مدیریت انتقال داده‌ها بین عبارت‌های Nix و متغیرهای شل استفاده می‌کند.
این امر این محدودیت را اعمال می‌کند که آرایه‌ها و «نگاشت‌ها» (maps) دارای مقادیری باشند که رشته‌مانند هستند.

نکته: حداقل یکی از موارد `expectedArray` یا `expectedMap` باید ارائه شود.

`name` (رشته)

: نام تست.

`script` (رشته)

: تنها وظیفه `script` مقداردهی به `actualArray` یا `actualMap` است (می‌تواند هر دو را مقداردهی کند).
  برای انجام این کار، `script` می‌تواند به متغیرهای شل زیر دسترسی داشته باشد:

  - `valuesArray` (در دسترس هنگامی که `valuesArray` به تستر ارائه شده باشد)
  - `valuesMap` (در دسترس هنگامی که `valuesMap` به تستر ارائه شده باشد)
  - `actualArray` (در دسترس هنگامی که `expectedArray` به تستر ارائه شده باشد)
  - `actualMap` (در دسترس هنگامی که `expectedMap` به تستر ارائه شده باشد)

  اگرچه هم `expectedArray` و هم `expectedMap` در طول اجرای `script` در اسکوپ قرار دارند، آن‌ها *نباید* از داخل `script` مورد دسترسی یا تغییر قرار گیرند.

`valuesArray` (آرایه‌ای از مقادیر رشته‌مانند، اختیاری)

: آرایه‌ای از مقادیر رشته‌مانند.
  این آرایه می‌تواند در داخل `script` استفاده شود.

`valuesMap` (مجموعه ویژگی از مقادیر رشته‌مانند، اختیاری)

: یک مجموعه ویژگی از مقادیر رشته‌مانند.
  این مجموعه ویژگی می‌تواند در داخل `script` استفاده شود.

`expectedArray` (آرایه‌ای از مقادیر رشته‌مانند، اختیاری)

: آرایه‌ای از مقادیر رشته‌مانند.
  به این آرایه *نباید* از داخل `script` دسترسی پیدا کرد یا آن را تغییر داد.
  در صورت ارائه، انتظار می‌رود `script` متغیر `actualArray` را مقداردهی کند.

`expectedMap` (مجموعه ویژگی از مقادیر رشته‌مانند، اختیاری)

: یک مجموعه ویژگی از مقادیر رشته‌مانند.
  به این مجموعه ویژگی *نباید* از داخل `script` دسترسی پیدا کرد یا آن را تغییر داد.
  در صورت ارائه، انتظار می‌رود `script` متغیر `actualMap` را مقداردهی کند.

### مقدار بازگشتی {#tester-testEqualArrayOrMap-return}

این تستر یک خروجی خالی تولید می‌کند و تنها زمانی موفق می‌شود که `expectedArray` و `expectedMap` در صورت غیر-نال بودن، به ترتیب با `actualArray` و `actualMap` مطابقت داشته باشند.
لوگ ساخت شامل تفاوت‌های مواجه‌شده خواهد بود.

## `testEqualDerivation` {#tester-testEqualDerivation}

بررسی می‌کند که دو بسته دقیقاً دستورالعمل‌های ساخت یکسانی تولید کنند.

این می‌تواند برای اطمینان از اینکه تفاوت خاصی در پیکربندی، مانند وجود یک اورلی، باعث عدم یافتن در کش (cache miss) نمی‌شود استفاده شود.

هنگامی که درایویشن‌ها برابر باشند، مقدار بازگشتی یک فایل خالی است.
در غیر این صورت، لوگ ساخت تفاوت را از طریق `nix-diff` توضیح می‌دهد.

:::{.example #ex-testEqualDerivation-hello}

# بررسی اینکه دو بسته derivation / اشتقاق ساخت یکسانی تولید می‌کنند

```nix
testers.testEqualDerivation "The hello package must stay the same when enabling checks." hello (
  hello.overrideAttrs (o: {
    doCheck = true;
  })
)
```

:::

## `invalidateFetcherByDrvHash` {#tester-invalidateFetcherByDrvHash}

از هش درایویشن برای باطل کردن خروجی از طریق نام، به منظور تست استفاده کنید.

نوع: `(a@{ name, ... } -> Derivation) -> a -> Derivation`

به طور معمول، درایویشن‌های با خروجی ثابت می‌توانند و باید فقط بر اساس هش خروجی‌شان کش شوند، اما برای تست می‌خواهیم هر بار که دریافت‌کننده تغییر می‌کند، دریافت مجدد انجام شود.

تغییرات در دریافت‌کننده در `drvPath` مشخص می‌شود، که هش نحوه دریافت است، نه یک مسیر انبار ثابت.
با درج این هش در نام، می‌توانیم مطمئن شویم که هر بار با تغییر دریافت‌کننده، دریافت‌کننده مجدداً اجرا می‌شود.

این کار بر این فرض استوار است که Nix آن‌قدر هوشمند نیست که برای بهینه‌سازی دریافت، از پایگاه داده محتویات انبار محلی خود مجدداً استفاده کند.

ممکن است متوجه شوید که نام «نمک‌زده» (salted) از فراخوانی عادی مشتق می‌شود، نه درایویشن نهایی.
`invalidateFetcherByDrvHash` باید تابع دریافت‌کننده را دو بار فراخوانی کند:
یک بار برای گرفتن هش درایویشن، و بار دیگر برای تولید درایویشن با خروجی ثابت نهایی.

:::{.example #ex-invalidateFetcherByDrvHash-nix}

# جلوگیری از استفاده مجدد Nix از خروجی یک دریافت‌کننده

```nix
{
  tests.fetchgit = testers.invalidateFetcherByDrvHash fetchgit {
    name = "nix-source";
    url = "https://github.com/NixOS/nix";
    rev = "9d9dbe6ed05854e03811c361a3380e09183f4f4a";
    hash = "sha256-7DszvbCNTjpzGRmpIVAWXk20P0/XTrWZ79KSOGLrUWY=";
  };
}
```

:::

## `runCommand` {#tester-runCommand}

`runCommand :: { name, script, stdenv ? stdenvNoCC, hash ? "...", ... } -> Derivation`

این یک پوشش (wrapper) حول `pkgs.runCommandWith` است که:
- یک derivation با خروجی ثابت تولید می‌کند و به دستور(ها) اجازه می‌دهد به شبکه دسترسی داشته باشند؛
- نام derivation را بر اساس ورودی‌های آن تغییر می‌دهد (سالت می‌زند)، تا اطمینان حاصل شود که با هر بار تغییر ورودی‌ها، دستور دوباره اجرا می‌شود.

این تابع صفت‌های زیر را می‌پذیرد:
- صفت `name` مربوط به derivation؛
- اسکریپت (`script`) که باید اجرا شود؛
- `stdenv`، محیط مورد استفاده، که به‌طور پیش‌فرض `stdenvNoCC` است؛
- `hash` خروجی derivation، که به‌طور پیش‌فرض هشِ یک فایل خالی است.
  مقدار `outputHashMode` مربوط به derivation به‌طور پیش‌فرض روی recursive تنظیم شده است، بنابراین `script` می‌تواند یک پوشه نیز در خروجی تولید کند.

تمام صفت‌های دیگر به [`mkDerivation`](#sec-using-stdenv) منتقل می‌شوند،
از جمله `nativeBuildInputs` برای تعیین وابستگی‌های در دسترس `script`.

:::{.example #ex-tester-runCommand-nix}

# اجرای یک دستور با دسترسی به شبکه

```nix
testers.runCommand {
  name = "access-the-internet";
  script = ''
    curl -o /dev/null https://example.com
    touch $out
  '';
  nativeBuildInputs = with pkgs; [
    cacert
    curl
  ];
}
```

:::

## `runNixOSTest` {#tester-runNixOSTest}

یک تابع کمکی که دقیقاً مانند `runTest` در NixOS رفتار می‌کند، با این تفاوت که این مجموعه بسته‌های Nixpkgs را به عنوان `pkgs` تست اختصاص می‌دهد و گزینه‌های `nixpkgs.*` را فقط‌خواندنی می‌کند.

اگر تست شما بخشی از مخزن Nixpkgs است، یا اگر به نقطه ورود عمومی‌تری نیاز دارید، [«فراخوانی یک تست» در راهنمای NixOS](https://nixos.org/manual/nixos/stable/index.html#sec-calling-nixos-tests) را ببینید.

:::{.example #ex-runNixOSTest-hello}

# اجرای یک تست NixOS با استفاده از `runNixOSTest`

```nix
pkgs.testers.runNixOSTest (
  { lib, ... }:
  {
    name = "hello";
    nodes.machine =
      { pkgs, ... }:
      {
        environment.systemPackages = [ pkgs.hello ];
      };
    testScript = ''
      machine.succeed("hello")
    '';
  }
)
```

:::

## `nixosTest` {#tester-nixosTest}

یک تست شبکه‌ای ماشین مجازی NixOS را با استفاده از این ارزیابی از Nixpkgs اجرا کنید.

نکته: این تابع در درجه اول برای استفاده خارجی است. خود NixOS مستقیماً از `make-test-python.nix` استفاده می‌کند. بسته‌های تعریف‌شده در Nixpkgs [تست‌های NixOS را از طریق `nixosTests` (به صورت جمع) مجدداً استفاده می‌کنند](#ssec-nixos-tests-linking).

این تابع تقریباً معادل تابع `import ./make-test-python.nix` از [راهنمای NixOS](https://nixos.org/nixos/manual/index.html#sec-nixos-tests) است، با این تفاوت که به جای اینکه به NixOS اجازه دهد Nixpkgs را از نو فراخوانی کند، از اعمال فعلی Nixpkgs (`pkgs`) استفاده می‌شود.

اگر یک ماشین تست نیاز به تنظیم گزینه‌های NixOS ذیل `nixpkgs` داشته باشد، تنها باید گزینه `nixpkgs.pkgs` را تنظیم کند.

### پارامتر {#tester-nixosTest-parameter}

یک [شبکه تست ماشین مجازی NixOS](https://nixos.org/nixos/manual/index.html#sec-nixos-tests)، یا مسیر منتهی به آن. مثال:

```nix
{
  name = "my-test";
  nodes = {
    machine1 =
      {
        lib,
        pkgs,
        nodes,
        ...
      }:
      {
        environment.systemPackages = [ pkgs.hello ];
        services.foo.enable = true;
      };
    # machine2 = ...;
  };
  testScript = ''
    start_all()
    machine1.wait_for_unit("foo.service")
    machine1.succeed("hello | foo-send")
  '';
}
```

### Result {#tester-nixosTest-result}

یک derivation که تست ماشین مجازی (VM) را اجرا می‌کند.

صفات قابل توجه:

 * `nodes`: پیکربندی‌های ارزیابی‌شده NixOS. برای دیباگ (اشکال‌زدایی) و بررسی پیکربندی مفید است.

 * `driverInteractive`: اسکریپتی که یک نشست تعاملی Python را در بافت `testScript` اجرا می‌کند.

## `modularServiceCompliance` {#tester-modularServiceCompliance}

مجموعه آزمایش تطابق برای ادغام‌های [سرویس مدولار](https://nixos.org/manual/nixos/unstable/#modular-services).

بررسی می‌کند که یک ادغام مدیر سرویس به درستی قرارداد قابل حمل سرویس‌های مدولار را مدیریت کند: `process.argv`، زیرسرویس‌ها، ادعاها (assertions) و هشدارها.

### Return value {#tester-modularServiceCompliance-return}

یک مجموعه صفت (attribute set) از درایویشن‌ها که تست‌ها را در طول ساخت (Build) خود انجام می‌دهند.

### Inputs {#tester-modularServiceCompliance-inputs}

`evalConfig` (تابع)

: `{ services } -> { config; checkDrv; }`.
  تابعی برای ارزیابی سرویس‌های داده‌شده در بافت کامل ادغام.
  این تابع برای بررسی‌های ارزیابی روی پیکربندی‌هایی که اجرا نخواهند شد فراخوانی می‌شود.
  - ورودی `services` یک attrset از پیکربندی‌های سرویس مدولار است. این‌ها باید عیناً استفاده شوند.
  - صفت خروجی `config` همان attrset حاصل از سرویس‌های ارزیابی‌شده است (به عنوان مثال، مقدار گزینه `system.services` در NixOS).
    این صفت باید در دسترس باشد حتی اگر `checkDrv` شکست بخورد.
  - صفت خروجی `checkDrv` یک derivation نماینده است که وجود و قابلیت ساخت (Build) آن اثبات می‌کند ارزیابی معتبر است (به عنوان مثال، `system.build.toplevel` در NixOS، اما ممکن است در مورد یک ادغام مدیر فرآیند دیگر مشخص‌تر باشد).
  - آزمایش‌کننده عمومی فقط `config` و `checkDrv` را می‌خواند. یک ادغام ممکن است صفات اضافی را برای بررسی‌های ارزیابی مخصوص به ادغام خود بازگرداند. چنین صفات اضافی اختیاری هستند.

`mkTest` (تابع)

: `{ name, services, testExe } -> derivation`.
  - ورودی `name` نام تست است که برای استفاده به عنوان نام derivation مناسب است.
  - ورودی `services` یک attrset از پیکربندی‌های سرویس مدولار است که با ساختار گزینه سرویس‌های ادغام مطابقت دارد.
  - ورودی `testExe` یک مسیر انبار (Nix store) به یک فایل اجرایی است که سرویس‌ها را تایید می‌کند.
  - خروجی: یک derivation که مدیر سرویس را با ورودی‌های پیکربندی ارائه‌شده اجرا کرده و سپس پس از شروع سرویس‌ها `testExe` را فراخوانی می‌کند. آن فایل اجرایی باید به `sharedDir` دسترسی داشته باشد.

`sharedDir` (رشته)

: مسیر یک پوشه که برای فرآیندهای سرویس قابل نوشتن و برای `testExe` قابل خواندن باشد.
  ادغام باید اطمینان حاصل کند که این پوشه در هنگام اجرای سرویس‌ها و `testExe` در دسترس است.

`callReload` (تابع)

: `path -> string`.
  با دریافت `path` نام یک سرویس (فهرست نام‌های سرویس از سرویس سطح بالا تا زیرسرویس هدف، به عنوان مثال `[ "reload" "inner" ]`)، یک دستور شل (Shell) بازمی‌گرداند که آن سرویس را مجدداً بارگذاری (reload) می‌کند.
  این دستور در `testExe` گنجانده شده و با دسترسی کافی برای بارگذاری مجدد سرویس اجرا می‌شود (به عنوان مثال به عنوان کاربر root در ماشین مجازی (VM) تست).
  هیچ دستور بارگذاری مجددی مستقل از مدیر وجود ندارد، بنابراین هر ادغامی باید این را ارائه دهد؛ ادغام، `path` را طبق قرارداد نام‌گذاری یونیت خود پیوند می‌دهد (مجموعه تست هیچ فرضی را در نظر نمی‌گیرد).
  در NixOS، این `path` با خط تیره به نام یونیت systemd با پسوند `.service` پیوند داده می‌شود، بنابراین دستور برابر است با `systemctl reload ${lib.concatStringsSep "-" path}.service` (یک سرویس سطح بالا یک مسیر تک‌عنصری `[ "svc" ]` -> `svc.service` است؛ یک زیرسرویس تو در تو `[ "parent" "child" ]` -> `parent-child.service`).

:::{.example #ex-modularServiceCompliance-nixos}

# فراخوانی مجموعه انطباق در NixOS

```nix
# In nixos/tests/all-tests.nix:
# modularServiceCompliance =
recurseIntoAttrs (
  pkgs.testers.modularServiceCompliance {
    sharedDir = "/tmp/modular-service-compliance";
    evalConfig =
      { services }:
      let
        machine = evalSystem (
          { ... }:
          {
            system.services = services;
            system.stateVersion = "25.05";
            fileSystems."/" = {
              device = "/test/dummy";
              fsType = "auto";
            };
            boot.loader.grub.enable = false;
          }
        );
      in
      {
        config = machine.config.system.services;
        checkDrv = machine.config.system.build.toplevel;
      };
    callReload = path: "systemctl reload ${lib.concatStringsSep "-" path}.service";
    mkTest =
      {
        name,
        services,
        testExe,
      }:
      runTest {
        _class = "nixosTest";
        inherit name;
        nodes.machine.system.services = services;
        testScript = ''
          machine.wait_for_unit("multi-user.target")
          machine.succeed("${testExe}")
        '';
      };
  }
)
```

:::

### موارد انطباق دستی {#tester-modularServiceCompliance-manual}

موارد انطباق زیر هنوز خودکار نشده‌اند و هنگام پیاده‌سازی یک یکپارچه‌سازی سرویس مدولار جدید باید به‌صورت دستی بررسی شوند.

- **گزاره‌های شرطی (assertions) ناموفق مانع از استقرار (deployment) می‌شوند.**
  سرویسی با `assertions = [{ assertion = false; message = "..."; }]` باید باعث شکست استقرار (deployment) شود.
  این سازوکار مختص یکپارچه‌سازی است (برای نمونه، NixOS ادعاها را در طول ارزیابی `system.build.toplevel` بررسی می‌کند).

- **هشدارها برای کاربر قابل مشاهده هستند.**
  سرویسی با `warnings = [ "..." ]` باید هشدار را به کاربر نمایش دهد.
  در NixOS این‌ها پیام‌های `builtins.warn` هستند که در طول ارزیابی صادر می‌شوند.

[file system object]: https://nix.dev/manual/nix/latest/store/file-system-object
