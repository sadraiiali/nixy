# کمک‌رسان‌های ساخت ساده {#chap-trivial-builders}

Nixpkgs توابع پوششی متنوعی ارائه می‌دهد که به ساخت درایویشن‌های کاربردیِ رایج کمک می‌کنند.
مانند [`stdenv.mkDerivation`](#sec-using-stdenv)، هر یک از این کمک‌رسان‌های ساخت یک درایویشن ایجاد می‌کنند، اما آرگومان‌های ارسال‌شده متفاوت (معمولاً ساده‌تر) از آرگومان‌های مورد نیاز `stdenv.mkDerivation` هستند.

## `runCommandWith` {#trivial-builder-runCommandWith}

تابع `runCommandWith` یک درایویشن ساخته‌شده با استفاده از دستور (های) مشخص‌شده در یک محیط تعیین‌شده را بازمی‌گرداند.

این تابع، تابع پایه و زیرین تمام [گونه‌های `runCommand*`] است.
رفتار کلی آن از طریق یک مجموعه ویژگی که به عنوان آرگومان اول پاس داده می‌شود کنترل شده و اجازه می‌دهد `stdenv` به صورت آزادانه تعیین شود.

[گونه‌های `runCommand*`] زیر وجود دارند: `runCommand`، `runCommandCC` و `runCommandLocal`.

[گونه‌های `runCommand*`]: #trivial-builder-runCommand

### نوع {#trivial-builder-runCommandWith-Type}

```
runCommandWith :: {
  name :: name;
  stdenv? :: Derivation;
  runLocal? :: Bool;
  derivationArgs? :: { ... };
} -> String -> Derivation
```

### ورودی‌ها {#trivial-builder-runCommandWith-Inputs}

`name` (رشته)
: نام درایویشن، که Nix آن را به مسیر انبار (store path) الحاق خواهد کرد؛ بخش [`mkDerivation`](#sec-using-stdenv) را ببینید.

`runLocal` (بولین)
: اگر روی `true` تنظیم شود، این گزینه درایویشن را مجبور می‌کند که به‌صورت محلی ساخته شود و از [جایگزین‌ها][substitutes] یا ساخت‌های راه دور استفاده نکند.
    این ویژگی برای دستورات بسیار کم‌هزینه (زمان اجرای کمتر از ۱ ثانیه) در نظر گرفته شده است که می‌توان با اجتناب از رفت‌وبرگشت(های) شبکه سرعت اجرای آن‌ها را افزایش داد.
    تأثیر آن تنظیم [`preferLocalBuild = true`][preferLocalBuild] و [`allowSubstitutes = false`][allowSubstitutes] است.

   ::: {.note}
   این کار مانع استفاده از [جایگزین‌کننده‌ها][substituter] می‌شود، بنابراین تنها زمانی `runLocal` را تنظیم کنید (یا از `runCommandLocal` استفاده کنید) که اطمینان دارید کاربر همواره یک سازنده (Builder) برای `system` درایویشن خواهد داشت. این موضوع باید برای بیشتر موارد استفاده ساده صادق باشد
   (به عنوان مثال، فقط کپی کردن برخی فایل‌ها به یک مکان دیگر یا افزودن پیوندهای نمادین (symlinks))، زیرا در آنجا `system`
   معمولاً همان `builtins.currentSystem` است.
   :::

`stdenv` (درایویشن)
: [محیط استاندارد](#chap-stdenv) برای استفاده، که مقدار پیش‌فرض آن `pkgs.stdenv` است.

`derivationArgs` (مجموعه ویژگی)
: آرگومان‌های اضافی برای [`mkDerivation`](#sec-using-stdenv).

`buildCommand` (رشته)
: دستورات شل برای اجرا در سازنده (Builder) درایویشن.

    ::: {.note}
    شما باید یک فایل یا پوشه به نام `$out` ایجاد کنید تا Nix بتواند سازنده (Builder) را با موفقیت اجرا کند.
    :::

[allowSubstitutes]: https://nix.dev/manual/nix/latest/language/advanced-attributes.html#adv-attr-allowSubstitutes
[preferLocalBuild]: https://nix.dev/manual/nix/latest/language/advanced-attributes.html#adv-attr-preferLocalBuild
[substituter]: https://nix.dev/manual/nix/latest/glossary#gloss-substituter
[substitutes]: https://nix.dev/manual/nix/latest/glossary#gloss-substitute

::: {.example #ex-runcommandwith}
# فراخوانی `runCommandWith`

```nix
runCommandWith
  {
    name = "example";
    derivationArgs.nativeBuildInputs = [ cowsay ];
  }
  ''
    cowsay > $out <<EOMOO
    'runCommandWith' is a bit cumbersome,
    so we have more ergonomic wrappers.
    EOMOO
  ''
```

:::

## `runCommand` و `runCommandCC` {#trivial-builder-runCommand}

تابع `runCommand` یک derivation / اشتقاق ساخت را برمی‌گرداند که با استفاده از دستور (های) مشخص‌شده، در محیط `stdenvNoCC` ساخته شده‌است.

`runCommandCC` مشابه است، اما از محیط کامپایلر پیش‌فرض استفاده می‌کند. برای به حداقل رساندن وابستگی‌ها، `runCommandCC` تنها باید زمانی استفاده شود که دستور ساخت به یک کامپایلر C نیاز دارد.

`runCommandLocal` نیز مشابه `runCommand` است، اما derivation / اشتقاق ساخت را مجبور می‌کند که به‌صورت محلی ساخته شود. یادداشت در مورد `runLocal` را در [`runCommandWith`] ببینید.

[`runCommandWith`]: #trivial-builder-runCommandWith

### نوع {#trivial-builder-runCommand-Type}

```
runCommand      :: String -> AttrSet -> String -> Derivation
runCommandCC    :: String -> AttrSet -> String -> Derivation
runCommandLocal :: String -> AttrSet -> String -> Derivation
```

### ورودی {#trivial-builder-runCommand-Input}

اگرچه امضای نوع با [`runCommandWith`] تفاوت دارد، آرگومان‌های مجزا با نام یکسان، دارای نوع و معنی یکسانی خواهند بود:

`name` (رشته)
: نام derivation

`derivationArgs` (مجموعه ویژگی)
: پارامترهای اضافی پاس‌داده‌شده به [`mkDerivation`]

`buildCommand` (رشته)
: دستور (هایی) که برای ساخت derivation اجرا می‌شوند.

::: {.example #ex-runcommand-simple}
# فراخوانی `runCommand`

```nix
runCommand "my-example" { } ''
  echo My example command is running

  mkdir $out

  echo I can write data to the Nix store > $out/message

  echo I can also run basic commands like:

  echo ls
  ls

  echo whoami
  whoami

  echo date
  date
''
```
:::

::: {.note}
`runCommand name derivationArgs buildCommand` معادل است با
```nix
runCommandWith {
  inherit name derivationArgs;
  stdenv = stdenvNoCC;
} buildCommand
```

به همین ترتیب، `runCommandCC name derivationArgs buildCommand` معادل است با
```nix
runCommandWith { inherit name derivationArgs; } buildCommand
```
:::

## نوشتن فایل‌های متنی {#trivial-builder-text-writing}

Nixpkgs توابع زیر را برای تولید درایویشن‌هایی که فایل‌های متنی یا اسکریپت‌های قابل اجرا را در انبار نیکس (Nix store) می‌نویسند، ارائه می‌دهد.
این توابع برای ایجاد فایل‌ها از عبارت‌های Nix مفید هستند و همگی به عنوان پوشش‌های تسهیل‌کننده در اطراف `writeTextFile` پیاده‌سازی شده‌اند.

هر یک از این توابع باعث تولید یک درایویشن می‌شوند.
وقتی نتیجه‌ی هر یک از این توابع را با [درون‌گذاری رشته](https://nixos.org/manual/nix/stable/language/string-interpolation) یا [`toString`](https://nixos.org/manual/nix/stable/language/builtins#builtins-toString) به یک رشته تبدیل می‌کنید، به [مسیر انبار](https://nixos.org/manual/nix/stable/store/store-path) این درایویشن ارزیابی می‌شود.

::: {.note}
برخی از این توابع، فایل‌های حاصل را درون پوشه‌ای در داخل [خروجی درایویشن](https://nixos.org/manual/nix/stable/language/derivations#attr-outputs) قرار می‌دهند.
اگر نیاز دارید در جای دیگری از یک عبارت نیکس (Nix expression) به فایل‌های حاصل ارجاع دهید، مسیر آن‌ها را به مسیر انبارِ درایویشن الحاق کنید.

برای مثال، اگر مقصد فایل یک پوشه باشد:

```nix
{
  my-file = writeTextFile {
    name = "my-file";
    text = ''
      Contents of File
    '';
    destination = "/share/my-file";
  };
}
```

به یاد داشته باشید که هنگام استفاده از آن در جاهای دیگر، "/share/my-file" را به مسیر انبار حاصل اضافه کنید:

```nix
writeShellScript "evaluate-my-file.sh" ''
  cat ${my-file}/share/my-file
''
```
:::

### `makeDesktopItem` {#trivial-builder-makeDesktopItem}

یک [فایل دسکتاپ XDG](https://specifications.freedesktop.org/desktop-entry-spec/1.4/) را در انبار نیکس (Nix store) می‌نویسد.

این تابع معمولاً برای افزودن آیتم‌های دسکتاپ به یک بسته از طریق قلاب `copyDesktopItems` استفاده می‌شود.

`makeDesktopItem` از نسخه 1.4 مشخصات پیروی می‌کند.

#### ورودی‌ها {#trivial-builder-makeDesktopItem-inputs}

`makeDesktopItem` یک مجموعه ویژگی دریافت می‌کند که بیشتر مقادیر موجود در [مشخصات XDG](https://specifications.freedesktop.org/desktop-entry-spec/1.4/ar01s06.html) را می‌پذیرد.

تمام کلیدهای شناخته‌شده از مشخصات به استثنای فیلد "Hidden" پشتیبانی می‌شوند. کلیدها به قالب camelCase تبدیل می‌شوند، اما تناظر ۱:۱ با معادل خود در مشخصات دارند: `genericName`، `noDisplay`، `comment`، `icon`، `onlyShowIn`، `notShowIn`، `dbusActivatable`، `tryExec`، `exec`، `path`، `terminal`، `mimeTypes`، `categories`، `implements`، `keywords`، `startupNotify`، `startupWMClass`، `url`، `prefersNonDefaultGPU`.

فیلد "Version" به صورت هاردکدشده روی نسخه‌ای قرار دارد که `makeDesktopItem` در حال حاضر از آن پیروی می‌کند.

فیلدهای زیر یا ضروری هستند، یا نوع آن‌ها با مشخصات متفاوت است، یا دارای مقادیر پیش‌فرض خاصی هستند، یا فیلدهای اضافی پشتیبانی‌شده توسط `makeDesktopItem` هستند:

`name` (رشته)

: نام فایل دسکتاپ در انبار نیکس (Nix store).

`type` (رشته؛ _اختیاری_)

: مقدار پیش‌فرض: `"Application"`

`desktopName` (رشته)

: معادل فیلد "Name" در مشخصات است.

`actions` (لیستی از مجموعه‌های ویژگی؛ _اختیاری_)

: لیستی از مجموعه‌های ویژگی {name, exec?, icon?}

`extraConfig` (مجموعه ویژگی؛ _اختیاری_)

: جفت‌های کلید/مقدار اضافی که عیناً به فایل دسکتاپ اضافه می‌شوند. ویژگی‌ها باید دارای پیشوند 'X-' باشند.

#### مثال‌ها {#trivial-builder-makeDesktopItem-examples}

::: {.example #ex-makeDesktopItem}
# کاربرد ۱ `makeDesktopItem`

یک فایل دسکتاپ `/nix/store/<store path>/my-program.desktop` را در انبار نیکس (Nix store) می‌نویسد.

```nix
{ makeDesktopItem }:
makeDesktopItem {
  name = "my-program";
  desktopName = "My Program";
  genericName = "Video Player";
  noDisplay = false;
  comment = "Cool video player";
  icon = "/path/to/icon";
  onlyShowIn = [ "KDE" ];
  dbusActivatable = true;
  tryExec = "my-program";
  exec = "my-program --someflag";
  path = "/some/working/path";
  terminal = false;
  actions.example = {
    name = "New Window";
    exec = "my-program --new-window";
    icon = "/some/icon";
  };
  mimeTypes = [ "video/mp4" ];
  categories = [ "Utility" ];
  implements = [ "org.my-program" ];
  keywords = [
    "Video"
    "Player"
  ];
  startupNotify = false;
  startupWMClass = "MyProgram";
  prefersNonDefaultGPU = false;
  extraConfig.X-SomeExtension = "somevalue";
}
```

:::

::: {.example #ex2-makeDesktopItem}
# کاربرد ۲ `makeDesktopItem`

بسته `hello` را جهت افزودن یک آیتم دسکتاپ بازنشانی کنید.

```nix
{
  copyDesktopItems,
  hello,
  makeDesktopItem,
}:

hello.overrideAttrs {
  nativeBuildInputs = [ copyDesktopItems ];

  desktopItems = [
    (makeDesktopItem {
      name = "hello";
      desktopName = "Hello";
      exec = "hello";
    })
  ];
}
```

:::

### `writeTextFile` {#trivial-builder-writeTextFile}

یک فایل متنی را در انبار نیکس (Nix store) می‌نویسد.

`writeTextFile` یک مجموعه ویژگی با ویژگی‌های ممکن زیر را می‌پذیرد:

`name` (String)

: با نام استفاده‌شده در شناسه مسیر انبار نیکس (Nix store) مطابقت دارد.

`text` (String)

: محتوای فایل.

`executable` (Bool, _اختیاری_)

: بیت قابل اجرا (executable) را برای این فایل تنظیم می‌کند.

  پیش‌فرض: `false`

`destination` (String, _اختیاری_)

: یک زیرمسیر تحت مسیر خروجی derivation که فایل در آن قرار می‌گیرد.
  زیرپوشه‌ها هنگام تحقق (realise) derivation به طور خودکار ایجاد می‌شوند.

  به طور پیش‌فرض، خود مسیر انبار فایلی حاوی محتوای متنی خواهد بود.

  پیش‌فرض: `""`

`checkPhase` (String, _اختیاری_)

: دستوراتی که باید پس از تولید فایل اجرا شوند.

  پیش‌فرض: `""`

`meta` (Attribute set, _اختیاری_)

: متادیتای اضافی برای derivation.

  پیش‌فرض: `{}`

`allowSubstitutes` (Bool, _اختیاری_)

: آیا جایگزینی از یک کش باینری مجاز باشد یا خیر.
  به [`allowSubstitutes`](https://nixos.org/manual/nix/stable/language/advanced-attributes#adv-attr-allowSubstitutes) در فراخوانی زیرین `derivation` منتقل می‌شود.

  مقدار پیش‌فرض آن `false` است، زیرا فرض می‌شود اجرای فایل قابل اجرای ساده‌ی `builder` مربوط به derivation به صورت محلی سریع‌تر از عملیات شبکه‌ای است.
  اگر گام `checkPhase` سنگین است، آن را برابر true قرار دهید.

  پیش‌فرض: `false`

`preferLocalBuild` (Bool, _اختیاری_)

: آیا ساخت به صورت محلی ترجیح داده شود، حتی اگر [ماشین‌های ساخت راه دور](https://nixos.org/manual/nix/stable/command-ref/conf-file#conf-substituters) سریع‌تری در دسترس باشند.

  به [`preferLocalBuild`](https://nixos.org/manual/nix/stable/language/advanced-attributes#adv-attr-preferLocalBuild) در فراخوانی زیرین `derivation` منتقل می‌شود.

  مقدار پیش‌فرض آن به همان دلیلی که `allowSubstitutes` به طور پیش‌فرض `false` است، برابر `true` می‌باشد.

  پیش‌فرض: `true`

`derivationArgs` (Attribute set, _اختیاری_)

: آرگومان‌های اضافی برای ارسال به فراخوانی زیرین `stdenv.mkDerivation`.

  پیش‌فرض: `{}`

مسیر انبار حاصل شامل تغییراتی از نام خواهد بود و یک فایل است، مگر اینکه از `destination` استفاده شده باشد که در آن صورت یک پوشه خواهد بود.

::: {.example #ex-writeTextFile}
# کاربرد ۱ از `writeTextFile`

نوشتن `my-file` در `/nix/store/<store path>/some/subpath/my-cool-script` و قابل اجرا کردن آن.
همچنین اجرای یک بررسی روی فایل حاصل در یک `checkPhase` و ارائه مقادیر برای گزینه‌های کم‌کاربردتر.

```nix
writeTextFile {
  name = "my-cool-script";
  text = ''
    #!/bin/sh
    echo "This is my cool script!"
  '';
  executable = true;
  destination = "/some/subpath/my-cool-script";
  checkPhase = ''
    ${pkgs.shellcheck}/bin/shellcheck $out/some/subpath/my-cool-script
  '';
  meta = {
    license = pkgs.lib.licenses.cc0;
  };
  allowSubstitutes = true;
  preferLocalBuild = false;
}
```
:::

::: {.example #ex2-writeTextFile}
# کاربرد ۲ `writeTextFile`

رشته‌ی `Contents of File` را در `/nix/store/<store path>` بنویسید.
همچنین تابع کمکی [](#trivial-builder-writeText) را ببینید.

```nix
writeTextFile {
  name = "my-file";
  text = ''
    Contents of File
  '';
}
```
:::

::: {.example #ex3-writeTextFile}
# کاربرد ۳ `writeTextFile`

یک اسکریپت قابل اجرای `my-script` را در `/nix/store/<store path>/bin/my-script` می‌نویسد.
همچنین تابع کمک‌رسان [](#trivial-builder-writeScriptBin) را ببینید.

```nix
writeTextFile {
  name = "my-script";
  text = ''
    echo "hi"
  '';
  executable = true;
  destination = "/bin/my-script";
}
```
:::

### `writeText` {#trivial-builder-writeText}

نوشتن یک فایل متنی در انبار Nix

`writeText` آرگومان‌های زیر را می‌گیرد:

`name` (String)

: نامی که در مسیر انبار Nix استفاده می‌شود.

`text` (String)

: محتوای فایل.

مسیر انبار شامل این نام خواهد بود و یک فایل خواهد بود.

::: {.example #ex-writeText}
# استفاده از `writeText`

نوشتن رشته `Contents of File` در `/nix/store/<store path>`:

```nix
writeText "my-file" ''
  Contents of File
''
```
:::

این معادل است با:

```nix
writeTextFile {
  name = "my-file";
  text = ''
    Contents of File
  '';
}
```

### `writeTextDir` {#trivial-builder-writeTextDir}

نوشتن یک فایل متنی درون یک زیرپوشه از انبار نیکس (Nix store).

`writeTextDir` آرگومان‌های زیر را می‌پذیرد:

`path` (رشته)

: مقصد در مسیر انبار نیکس (Nix store) که فایل باید زیر آن ایجاد شود.

`text` (رشته)

: محتویات فایل.

مسیر انبار یک پوشه خواهد بود.

::: {.example #ex-writeTextDir}
# استفاده از `writeTextDir`

نوشتن رشته `Contents of File` در `/nix/store/<store path>/share/my-file`:

```nix
writeTextDir "share/my-file" ''
  Contents of File
''
```
:::

این معادل است با:

```nix
writeTextFile {
  name = "my-file";
  text = ''
    Contents of File
  '';
  destination = "/share/my-file";
}
```

### `writeScript` {#trivial-builder-writeScript}

یک فایل اسکریپت قابل اجرا را در انبار نیکس (Nix store) می‌نویسد.

`writeScript` آرگومان‌های زیر را می‌پذیرد:

`name` (رشته)

: نامی که در مسیر انبار نیکس (Nix store) استفاده می‌شود.

`text` (رشته)

: محتوای فایل.

فایل ایجادشده به عنوان قابل اجرا علامت‌گذاری می‌شود.
مسیر انبار شامل نام خواهد بود و یک فایل خواهد بود.

::: {.example #ex-writeScript}
# استفاده از `writeScript`

رشته `Contents of File` را در `/nix/store/<store path>` بنویسید و فایل را قابل اجرا کنید.

```nix
writeScript "my-file" ''
  Contents of File
''
```

این معادل است با:

```nix
writeTextFile {
  name = "my-file";
  text = ''
    Contents of File
  '';
  executable = true;
}
```
:::

### `writeScriptBin` {#trivial-builder-writeScriptBin}

اسکریپتی را درون یک زیرپوشه `bin` از پوشه‌ای در انبار نیکس (Nix store) می‌نویسد.
این کار جهت حفظ سازگاری با عرف بسته‌های نرم‌افزاری در قرار دادن فایل‌های اجرایی در زیرپوشه `bin` انجام می‌شود.

`writeScriptBin` آرگومان‌های زیر را می‌پذیرد:

`name` (String)

: نام مورد استفاده در مسیر انبار نیکس (Nix store) و درون فایل ایجادشده زیر مسیر انبار.

`text` (String)

: محتوای فایل.

فایل ایجادشده به عنوان قابل اجرا نشانه‌گذاری می‌شود.
محتوای فایل در مسیر `/nix/store/<store path>/bin/<name>` قرار خواهد گرفت.
مسیر انبار شامل نام خواهد بود و یک پوشه خواهد بود.

::: {.example #ex-writeScriptBin}
# استفاده از `writeScriptBin`

```nix
writeScriptBin "my-script" ''
  echo "hi"
''
```
:::

این معادل است با:

```nix
writeTextFile {
  name = "my-script";
  text = ''
    echo "hi"
  '';
  executable = true;
  destination = "/bin/my-script";
}
```

### `writeShellScript` {#trivial-builder-writeShellScript}

یک اسکریپت Bash را در انبار می‌نویسد.

`writeShellScript` آرگومان‌های زیر را می‌پذیرد:

`name` (String)

: نامی که در مسیر انبار نیکس (Nix store) استفاده می‌شود.

`text` (String)

: محتوای فایل.

فایل ایجادشده به‌صورت قابل اجرا نشانه‌گذاری می‌شود.
مسیر انبار شامل این نام خواهد بود و یک فایل خواهد بود.

این تابع تقریباً کاملاً مشابه [](#trivial-builder-writeScript) است، با این تفاوت که یک سطر [شبانگ (shebang)](https://en.wikipedia.org/wiki/Shebang_%28Unix%29) به ابتدای فایل اضافه می‌کند که به نسخه Bash مورد استفاده در Nixpkgs اشاره دارد.
<!-- this cannot be changed in practice, so there is no point pretending it's somehow generic -->

::: {.example #ex-writeShellScript}
# نحوه استفاده از `writeShellScript`

```nix
writeShellScript "my-script" ''
  echo "hi"
''
```
:::

این معادل است با:

```nix
writeTextFile {
  name = "my-script";
  text = ''
    #! ${pkgs.runtimeShell}
    echo "hi"
  '';
  executable = true;
}
```

### `writeShellScriptBin` {#trivial-builder-writeShellScriptBin}

نوشتن یک اسکریپت Bash در زیرپوشه "bin" مربوط به یک پوشه در انبار نیکس (Nix store).

`writeShellScriptBin` آرگومان‌های زیر را می‌گیرد:

`name` (رشته)

: نام استفاده‌شده در مسیر انبار نیکس (Nix store) و درون فایل تولیدشده زیر مسیر انبار.

`text` (رشته)

: محتویات فایل.

محتویات فایل در `/nix/store/<store path>/bin/<name>` قرار می‌گیرد.
مسیر انبار شامل نام خواهد بود و یک پوشه است.

این تابع ترکیبی از [](#trivial-builder-writeShellScript) و [](#trivial-builder-writeScriptBin) است.

::: {.example #ex-writeShellScriptBin}
# نحوه استفاده از `writeShellScriptBin`

```nix
writeShellScriptBin "my-script" ''
  echo "hi"
''
```
:::

این معادل است با:

```nix
writeTextFile {
  name = "my-script";
  text = ''
    #! ${pkgs.runtimeShell}
    echo "hi"
  '';
  executable = true;
  destination = "/bin/my-script";
}
```

## `concatTextFile`، `concatText`، `concatScript` {#trivial-builder-concatText}

این توابع، `files` را در قالب یک فایل واحد در انبار نیکس (Nix store) به یکدیگر متصل می‌کنند. این ویژگی برای فایل‌های پیکربندی که به صورت خطوط متنی ساختار یافته‌اند مفید است. `concatTextFile` یک مجموعه ویژگی دریافت می‌کند و انتظار دو آرگومان دارد: `name` و `files`. `name` متناظر با نام استفاده‌شده در مسیر انبار نیکس (Nix store) است. `files` شامل فایل‌هایی خواهد بود که قرار است به هم متصل شوند. همچنین می‌توانید `executable` را برابر با true قرار دهید تا بیت قابل اجرا برای این فایل تنظیم شود.
`concatText` و `concatScript` روکش‌های (wrapper) ساده‌ای روی `concatTextFile` هستند.

در ادامه چند نمونه آورده شده‌است:
```nix
# Writes my-file to /nix/store/<store path>
concatTextFile
  {
    name = "my-file";
    files = [
      drv1
      "${drv2}/path/to/file"
    ];
  }
  # See also the `concatText` helper function below.

  # Writes executable my-file to /nix/store/<store path>/bin/my-file
  concatTextFile
  {
    name = "my-file";
    files = [
      drv1
      "${drv2}/path/to/file"
    ];
    executable = true;
    destination = "/bin/my-file";
  }
  # Writes contents of files to /nix/store/<store path>
  concatText
  "my-file"
  [
    file1
    file2
  ]

  # Writes contents of files to /nix/store/<store path>
  concatScript
  "my-file"
  [
    file1
    file2
  ]
```

## `writeShellApplication` {#trivial-builder-writeShellApplication}

`writeShellApplication` شبیه به `writeShellScriptBin` و `writeScriptBin` است، اما از وابستگی‌های زمان اجرا با `runtimeInputs` پشتیبانی می‌کند.
یک اسکریپت شل قابل اجرا را در `/nix/store/<store path>/bin/<name>` می‌نویسد و نحو آن را با [`shellcheck`](https://github.com/koalaman/shellcheck) و گزینه `-n` در `bash` بررسی می‌کند.
برخی از گزینه‌های پایه Bash به طور پیش‌فرض تنظیم شده‌اند (`errexit` ،`nounset` و `pipefail`)، اما می‌توان آن‌ها را با `bashOptions` بازنشانی کرد.

آرگومان‌های اضافی را می‌توان با تنظیم `derivationArgs` به `stdenv.mkDerivation` ارسال کرد؛ توجه داشته باشید متغیرهایی که به این روش تنظیم می‌شوند، هنگام _ساخت_ اسکریپت شل مقداردهی می‌شوند، نه زمان اجرای آن.
متغیرهای محیطی زمان اجرا را می‌توان با آرگومان `runtimeEnv` تنظیم کرد.

`writeShellApplication` دارای آرگومان‌های زیر است:

`name` (String)

: نام اسکریپتی که باید نوشته شود.

`text` (String)

: متن اسکریپت شل، بدون شامل شدن shebang.

`runtimeInputs` (لیستی از درایویشن‌ها یا رشته‌ها، _اختیاری_)

: ورودی‌هایی که باید در زمان اجرا به `$PATH` اسکریپت شل اضافه شوند.

  هر عنصر می‌تواند یک derivation معمولی یا یک رشته شامل یک مسیر باشد که در این صورت پسوند `/bin` به آن اضافه می‌شود تا یک عبارت `PATH` ایجاد کند (برای اطلاعات بیشتر به [`lib.strings.makeBinPath`](#function-library-lib.strings.makeBinPath) مراجعه کنید).

`runtimeEnv` (مجموعه ویژگی، _اختیاری_)

: متغیرهای محیطی اضافی برای تنظیم در زمان اجرا.

`checkPhase` (رشته، _اختیاری_)

: `checkPhase` برای اجرا.

  مسیر اسکریپت به عنوان `$target` در `checkPhase` ارائه می‌شود.

  _رفتار پیش‌فرض:_ اجرای [`shellcheck`](https://github.com/koalaman/shellcheck) (روی پلتفرم‌های پشتیبانی‌شده) و `bash -n` (بررسی نحو بدون اجرای دستورات).

`excludeShellChecks` (لیستی از رشته‌ها، _اختیاری_)

: بررسی‌هایی که باید هنگام اجرای `shellcheck` مستثنی شوند.

  به عنوان مثال، `excludeShellChecks = [ "SC2016" ]` مانع از گزارش `SC2016` توسط `shellcheck` می‌شود، اما همچنان هرگونه مشکل دیگر را تشخیص می‌دهد.

  برای مشاهده لیست بررسی‌ها به [ویکی `shellcheck`](https://www.shellcheck.net/wiki/) مراجعه کنید.

`extraShellCheckFlags` (لیستی از رشته‌ها، _اختیاری_)

: پرچم‌های خط فرمان اضافی برای ارسال به `shellcheck`.

`bashOptions` (لیستی از رشته‌ها، _اختیاری_)

: گزینه‌های Bash برای فعال‌سازی با `set -o` در شروع اسکریپت.

  _پیش‌فرض:_ `[ "errexit" "nounset" "pipefail" ]` که به این معناست:
  1. شکست یک دستور در داخل لیست دستورات یا پایپ‌لاین باعث خروج اسکریپت می‌شود، مگر اینکه به عنوان یک شرط استفاده شده باشد (در داخل `while` ،`if` ،`&&` ،`||` و غیره)؛
  2. هرگونه تلاش برای گسترش یک متغیر تعریف‌نشده باعث خروج اسکریپت می‌شود.

`inheritPath` (بولی، _اختیاری_)

: آیا اسکریپت PATH را از محیط والد خود به ارث می‌برد یا خیر.

  _پیش‌فرض:_ `true`

`meta` (مجموعه ویژگی، _اختیاری_)

: آرگومان [`meta`](#chap-meta) مربوط به `stdenv.mkDerivation`

`passthru` (مجموعه ویژگی، _اختیاری_)

: آرگومان [`passthru`](#chap-passthru) مربوط به `stdenv.mkDerivation`

`derivationArgs` (مجموعه ویژگی، _اختیاری_)

: آرگومان‌های اضافی برای ارسال به [`stdenv.mkDerivation`](#chap-stdenv)

  ::: {.caution}
  برخی صفات derivation نیز به صورت داخلی تنظیم می‌شوند، بنابراین بازنشانی آن‌ها می‌تواند باعث بروز مشکلاتی شود.
  :::

::: {.example #ex-writeShellApplication}
# نحوه استفاده از `writeShellApplication`

برنامه شل زیر می‌تواند مستقیماً به `curl` ارجاع دهد، به جای اینکه نیاز باشد `${curl}/bin/curl` نوشته شود

```nix
writeShellApplication {
  name = "show-nixos-org";

  runtimeInputs = [
    curl
    w3m
  ];

  text = ''
    curl -s 'https://nixos.org' | w3m -dump -T text/html
  '';
}
```
:::

## `symlinkJoin` {#trivial-builder-symlinkJoin}

از این تابع می‌توان برای قرار دادن چندین درایویشن در یک ساختار پوشه یکسان استفاده کرد. نحوه کار آن به این صورت است که یک درایویشن جدید ایجاد کرده و پیوندهای نمادین (symlinks) را به هر یک از مسیرهای فهرست‌شده اضافه می‌کند. این تابع دو آرگومان دریافت می‌کند: `name` و `paths`. صفت `name` (یا به عنوان جایگزین، `pname` و `version`) نامی است که در مسیر انبار نیکس (Nix store) برای درایویشن ایجادشده استفاده می‌شود. `paths` فهرستی از مسیرها است که پیوند نمادین (symlink) داده خواهند شد. این مسیرها می‌توانند به درایویشن‌های انبار نیکس (Nix store) یا هر زیرپوشه‌ی موجود در آن‌ها اشاره داشته باشند.
در ادامه یک نمونه آورده شده‌است:
```nix
# adds symlinks of hello and stack to current build and prints "links added"
symlinkJoin {
  name = "myexample";
  paths = [
    pkgs.hello
    pkgs.stack
  ];
  postBuild = "echo links added";
}
```
این یک درایویشن با ساختار پوشه‌ای مانند زیر ایجاد می‌کند:
```
/nix/store/sglsr5g079a5235hy29da3mq3hv8sjmm-myexample
|-- bin
|   |-- hello -> /nix/store/qy93dp4a3rqyn2mz63fbxjg228hffwyw-hello-2.10/bin/hello
|   `-- stack -> /nix/store/6lzdpxshx78281vy056lbk553ijsdr44-stack-2.1.3.1/bin/stack
`-- share
    |-- bash-completion
    |   `-- completions
    |       `-- stack -> /nix/store/6lzdpxshx78281vy056lbk553ijsdr44-stack-2.1.3.1/share/bash-completion/completions/stack
    |-- fish
    |   `-- vendor_completions.d
    |       `-- stack.fish -> /nix/store/6lzdpxshx78281vy056lbk553ijsdr44-stack-2.1.3.1/share/fish/vendor_completions.d/stack.fish
...
```

## `writeClosure` {#trivial-builder-writeClosure}

با گرفتن فهرستی از [مسیرهای انبار](https://nixos.org/manual/nix/stable/glossary#gloss-store-path) (یا عبارت‌های رشته‌مانند قابل تبدیل به مسیرهای انبار)، [بستار](https://nixos.org/manual/nix/stable/glossary#gloss-closure) جمعی آن‌ها را در یک فایل متنی می‌نویسد.

نتیجه معادل خروجی `nix-store -q --requisites` است.

برای نمونه،

```nix
writeClosure [ (writeScriptBin "hi" "${hello}/bin/hello") ]
```

مسیر خروجی `/nix/store/<hash>-runtime-deps` را تولید می‌کند که شامل

```
/nix/store/<hash>-hello-2.10
/nix/store/<hash>-hi
/nix/store/<hash>-libidn2-2.3.0
/nix/store/<hash>-libunistring-0.9.10
/nix/store/<hash>-glibc-2.32-40
```

می‌توانید ببینید که این شامل `hi` (مسیر ورودی اصلی)،
`hello` که یک ارجاع مستقیم است، و همچنین
مسیرهای دیگری است که به‌طور غیرمستقیم برای اجرای `hello` مورد نیاز هستند.

## `writeDirectReferencesToFile` {#trivial-builder-writeDirectReferencesToFile}

مجموعه‌ی ارجاعات، یعنی وابستگی‌های مستقیم آن‌ها را در فایل خروجی می‌نویسد.

این خروجی معادل `nix-store -q --references` تولید می‌کند.

برای مثال،

```nix
writeDirectReferencesToFile (writeScriptBin "hi" "${hello}/bin/hello")
```

مسیر خروجی `/nix/store/<hash>-runtime-references` را تولید می‌کند که حاوی

```
/nix/store/<hash>-hello-2.10
```

اما هیچ‌یک از وابستگی‌های `hello`، زیرا آن‌ها به‌طور مستقیم توسط خروجی `hi` مورد ارجاع قرار نگرفته‌اند.
