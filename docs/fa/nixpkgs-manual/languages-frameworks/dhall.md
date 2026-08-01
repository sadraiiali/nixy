# Dhall {#sec-language-dhall}

پشتیبانی Nixpkgs از Dhall، فرض را بر آشنایی نسبی با پشتیبانی زبانی Dhall برای درون‌ریزی عبارت‌های Dhall می‌گذارد که اسناد آن در اینجا آمده است:

* [`dhall-lang.org` - نصب بسته‌ها](https://docs.dhall-lang.org/tutorials/Language-Tour.html#installing-packages)

## درون‌ریزی‌های راه دور {#ssec-dhall-remote-imports}

‏Nixpkgs پشتیبانی Dhall از درون‌ریزی‌های راه دور را با استفاده از بررسی‌های یکپارچگی معنایی Dhall کنار می‌زند. به طور خاص، هر درون‌ریزی Dhall می‌تواند توسط یک بررسی یکپارچگی مانند زیر محافظت شود:

```dhall
https://prelude.dhall-lang.org/v20.1.0/package.dhall
  sha256:26b0ef498663d269e4dc6a82b0ee289ec565d683ef4c00d0ebdd25333a5a3c98
```

… و اگر درون‌ریزی در کش ذخیره شده باشد، مفسر درون‌ریزی را به جای دریافت از URL، از کش بارگذاری می‌کند.

Nixpkgs از این ترفند برای افزودن تمام وابستگی‌های یک عبارت Dhall به کش استفاده می‌کند تا مفسر Dhall هرگز نیازی به رفع شناسه (resolve) هیچ URL راه دوری نداشته باشد. در واقع، Nixpkgs هنگام بسته‌بندی عبارت‌های Dhall، از یک مفسر Dhall که درون‌ریزی‌های راه دور آن غیرفعال شده استفاده می‌کند تا اعمال کند که مفسر هرگز یک درون‌ریزی راه دور را پردازش نکند. این بدان معناست که Nixpkgs تنها زمانی از ساخت عبارت‌های Dhall پشتیبانی می‌کند که تمام درون‌ریزی‌های راه دور آن‌ها توسط بررسی‌های تمامیت معنایی محافظت شده باشند.

Nixpkgs به جای درون‌ریزی‌های راه دور، از Nix برای دریافت کد Dhall راه دور استفاده می‌کند. به عنوان مثال، بسته Dhall مربوط به Prelude از `pkgs.fetchFromGitHub` برای دریافت مخزن `dhall-lang` حاوی Prelude استفاده می‌کند. اتکای انحصاری به Nix برای دریافت کد Dhall تضمین می‌کند که بسته‌های Dhall ساخته‌شده با استفاده از Nix خالص باقی بمانند و همچنین هنگام ساخت در یک محیط ایزوله رفتار مناسبی داشته باشند.

## بسته‌بندی یک عبارت Dhall از صفر {#ssec-dhall-packaging-expression}

ما می‌توانیم نحوه یکپارچه‌سازی Dhall در Nixpkgs را با شروع از عبارت ناچیز و ساده Dhall زیر که دارای یک وابستگی (Prelude) است، نشان دهیم:

```dhall
-- ./true.dhall

let Prelude = https://prelude.dhall-lang.org/v20.1.0/package.dhall

in  Prelude.Bool.not False
```

همان‌طور که نوشته شده، این عبارت را نمی‌توان با استفاده از Nixpkgs ساخت زیرا از درون‌ریزی Prelude با یک بررسی یکپارچگی معنایی محافظت نمی‌کند؛ بنابراین نخستین گام، منجمد کردن عبارت با استفاده از `dhall freeze` است، به این صورت:

```ShellSession
$ dhall freeze --inplace ./true.dhall
```

… که به ما می‌دهد:

```dhall
-- ./true.dhall

let Prelude =
      https://prelude.dhall-lang.org/v20.1.0/package.dhall
        sha256:26b0ef498663d269e4dc6a82b0ee289ec565d683ef4c00d0ebdd25333a5a3c98

in  Prelude.Bool.not False
```

برای بسته‌بندی آن عبارت، یک فایل `./true.nix` حاوی مشخصات زیر برای بسته Dhall ایجاد می‌کنیم:

```nix
# ./true.nix

{ buildDhallPackage, Prelude }:

buildDhallPackage {
  name = "true";
  code = ./true.dhall;
  dependencies = [ Prelude ];
  source = true;
}
```

… و با گنجاندن آن بسته Dhall در سلسله‌مراتب `pkgs.dhallPackages` با استفاده از یک اورلی، ساخت را به پایان می‌رسانیم، به این صورت:

```nix
# ./example.nix

let
  nixpkgs = fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/94b2848559b12a8ed1fe433084686b2a81123c99.tar.gz";
    hash = "sha256-B4Q3c6IvTLg3Q92qYa8y+i4uTaphtFdjp+Ir3QQjdN0=";
  };

  dhallOverlay = self: super: { true = self.callPackage ./true.nix { }; };

  overlay = self: super: {
    dhallPackages = super.dhallPackages.override (old: {
      overrides = self.lib.composeExtensions (old.overrides or (_: _: { })) dhallOverlay;
    });
  };

  pkgs = import nixpkgs {
    config = { };
    overlays = [ overlay ];
  };

in
pkgs
```

… که سپس می‌توانیم با استفاده از این دستور آن را بسازیم:

```ShellSession
$ nix build --file ./example.nix dhallPackages.true
```

## محتویات یک بسته Dhall {#ssec-dhall-package-contents}

بسته بالا درخت پوشه زیر را تولید می‌کند:

```ShellSession
$ tree -a ./result
result
├── .cache
│   └── dhall
│       └── 122027abdeddfe8503496adeb623466caa47da5f63abd2bc6fa19f6cfcb73ecfed70
├── binary.dhall
└── source.dhall
```

… که در آن:

* `source.dhall` شامل نتیجه‌ی تفسیر بسته Dhall ما است:
```ShellSession
  $ cat ./result/source.dhall
  True
  ```

* زیرپوشه `.cache` شامل یک محصول کش باینری است که همان نتیجه‌ی `source.dhall` را رمزگذاری می‌کند:
```ShellSession
  $ dhall decode < ./result/.cache/dhall/122027abdeddfe8503496adeb623466caa47da5f63abd2bc6fa19f6cfcb73ecfed70
  True
  ```

* `binary.dhall` شامل یک عبارت Dhall است که دریافت و رمزگشایی همان محصول کش را مدیریت می‌کند:
```ShellSession
  $ cat ./result/binary.dhall
  missing sha256:27abdeddfe8503496adeb623466caa47da5f63abd2bc6fa19f6cfcb73ecfed70
  $ cp -r ./result/.cache .cache

  $ chmod -R u+w .cache

  $ XDG_CACHE_HOME=.cache dhall --file ./result/binary.dhall
  True
  ```

فایل `source.dhall` تنها برای بسته‌هایی وجود دارد که `source = true;` را مشخص کرده باشند. به طور پیش‌فرض، بسته‌های Dhall فایل `source.dhall` را حذف می‌کنند تا هنگامی که منحصراً به عنوان وابستگی‌ها استفاده می‌شوند، در فضای دیسک صرفه‌جویی شود. به عنوان مثال، اگر بسته Prelude را بسازیم، این بسته تنها حاوی کدگذاری باینری عبارت خواهد بود:

```ShellSession
$ nix build --file ./example.nix dhallPackages.Prelude

$ tree -a result
result
├── .cache
│   └── dhall
│       └── 122026b0ef498663d269e4dc6a82b0ee289ec565d683ef4c00d0ebdd25333a5a3c98
└── binary.dhall

2 directories, 2 files
```

معمولاً، شما فقط `source = true;` را برای عبارت Dhall سطح بالای مورد نظر (مانند بسته Dhall نمونه‌ی ما `true.nix`) مشخص می‌کنید. با این حال، اگر تمایل دارید `source = true` را برای همه بسته‌های Dhall مشخص کنید، می‌توانید اورلی Dhall را به این شکل اصلاح کنید:

```nix
{
  dhallOverrides = self: super: {
    # Enable source for all Dhall packages
    buildDhallPackage = args: super.buildDhallPackage (args // { source = true; });

    true = self.callPackage ./true.nix { };
  };
}
```

… و اکنون Prelude حاوی نتیجهٔ کاملاً رمزگشایی‌شدهٔ تفسیر Prelude خواهد بود:

```ShellSession
$ nix build --file ./example.nix dhallPackages.Prelude

$ tree -a result
result
├── .cache
│   └── dhall
│       └── 122026b0ef498663d269e4dc6a82b0ee289ec565d683ef4c00d0ebdd25333a5a3c98
├── binary.dhall
└── source.dhall

$ cat ./result/source.dhall
{ Bool =
  { and =
      \(_ : List Bool) ->
        List/fold Bool _ Bool (\(_ : Bool) -> \(_ : Bool) -> _@1 && _) True
  , build = \(_ : Type -> _ -> _@1 -> _@2) -> _ Bool True False
  , even =
      \(_ : List Bool) ->
        List/fold Bool _ Bool (\(_ : Bool) -> \(_ : Bool) -> _@1 == _) True
  , fold =
      \(_ : Bool) ->
…
```

## توابع بسته‌بندی {#ssec-dhall-packaging-functions}

ما پیش از این مثالی از استفاده از `buildDhallPackage` برای ایجاد یک بسته Dhall از یک فایل منفرد را دیدیم، اما بیشتر بسته‌های Dhall از بیش از یک فایل تشکیل شده‌اند و دو ابزار مشتق‌شده وجود دارند که ممکن است هنگام بسته‌بندی فایل‌های متعدد مفیدتر بیابید:

* `buildDhallDirectoryPackage` - ساخت یک بسته Dhall از یک پوشه محلی

* `buildDhallGitHubPackage` - ساخت یک بسته Dhall از یک مخزن GitHub

تابع `buildDhallPackage` پایین‌ترین سطح از توابع است و آرگومان‌های زیر را می‌پذیرد:

* `name`: نام derivation

* `dependencies`: وابستگی‌های Dhall جهت ساخت و کش کردن پیش از موعد

* `code`: عبارت سطح بالا برای ساخت جهت این بسته

  توجه داشته باشید که فیلد `code` یک عبارت دلخواه Dhall را می‌پذیرد. شما تنها به یک فایل محدود نیستید.

* `source`: مقدار آن را برابر `true` قرار دهید تا نتیجهٔ رمزگشایی‌شده به عنوان `source.dhall` در فرآوردهٔ ساخت گنجانده شود، به قیمت مصرف فضای دیسک بیشتر

* `documentationRoot`: اگر می‌خواهید `dhall-docs` مستندات را زیر زیرپوشهٔ `docs` از فرآوردهٔ ساخت تولید کند، آن را روی پوشهٔ ریشهٔ بسته تنظیم کنید

تابع `buildDhallDirectoryPackage` یک تابع سطح بالاتر است که بر اساس `buildDhallPackage` پیاده‌سازی شده و آرگومان‌های زیر را می‌پذیرد:

* `name`: مشابه `buildDhallPackage`

* `dependencies`: مشابه `buildDhallPackage`

* `source`: مشابه `buildDhallPackage`

* `src`: پوشه‌ای حاوی کد Dhall که می‌خواهید به یک بسته Dhall تبدیل کنید

* `file`: فایل سطح بالا (به‌طور پیش‌فرض `package.dhall`) که نقطهٔ ورود به باقی بسته است

* `document`: مقدار آن را برابر `true` قرار دهید تا مستندات برای بسته تولید شود

تابع `buildDhallGitHubPackage` تابع سطح بالا دیگری است که بر اساس `buildDhallPackage` پیاده‌سازی شده و آرگومان‌های زیر را می‌پذیرد:

* `name`: مشابه `buildDhallPackage`

* `dependencies`: مشابه `buildDhallPackage`

* `source`: مشابه `buildDhallPackage`

* `owner`: مالک مخزن

* `repo`: نام مخزن

* `rev`: ریویژن (یا شاخه، یا تگ) مورد نظر

* `directory`: زیرپوشه‌ای از مخزن Git جهت بسته‌بندی (اگر پوشه‌ای غیر از ریشهٔ مخزن باشد)

* `file`: فایل سطح بالا (به‌طور پیش‌فرض `${directory}/package.dhall`) که نقطهٔ ورود به باقی بسته است

* `document`: مقدار آن را برابر `true` قرار دهید تا مستندات برای بسته تولید شود

علاوه بر این، `buildDhallGitHubPackage` همان آرگومان‌های `fetchFromGitHub` مانند `hash` یا `fetchSubmodules` را می‌پذیرد.

## `dhall-to-nixpkgs` {#ssec-dhall-dhall-to-nixpkgs}

می‌توانید از ابزار خط فرمان `dhall-to-nixpkgs` برای خودکارسازی بسته‌بندی کد Dhall استفاده کنید. برای مثال:

```ShellSession
$ nix-shell -p haskellPackages.dhall-nixpkgs nix-prefetch-git
[nix-shell]$ dhall-to-nixpkgs github https://github.com/Gabriella439/dhall-semver.git
{ buildDhallGitHubPackage, Prelude }:
  buildDhallGitHubPackage {
    name = "dhall-semver";
    githubBase = "github.com";
    owner = "Gabriella439";
    repo = "dhall-semver";
    rev = "2d44ae605302ce5dc6c657a1216887fbb96392a4";
    fetchSubmodules = false;
    hash = "sha256-n0nQtswVapWi/x7or0O3MEYmAkt/a1uvlOtnje6GGnk=";
    directory = "";
    file = "package.dhall";
    source = false;
    document = false;
    dependencies = [ (Prelude.overridePackage { file = "package.dhall"; }) ];
    }
```

:::{.note}
`nix-prefetch-git` به فراخوانی `nix-shell -p` در بالا اضافه شده است، زیرا برای کارکرد `dhall-to-nixpkgs` باید در `$PATH` قرار داشته باشد.
:::

این ابزار به‌طور خودکار درون‌ریزی‌های راه دور را تشخیص داده و آن‌ها را به وابستگی‌های بسته تبدیل می‌کند. همچنین می‌توانید از این ابزار روی پوشه‌های محلی Dhall نیز استفاده کنید:

```ShellSession
$ dhall-to-nixpkgs directory ~/proj/dhall-semver
{ buildDhallDirectoryPackage, Prelude }:
  buildDhallDirectoryPackage {
    name = "proj";
    src = ~/proj/dhall-semver;
    file = "package.dhall";
    source = false;
    document = false;
    dependencies = [ (Prelude.overridePackage { file = "package.dhall"; }) ];
    }
```

### درون‌ریزی‌های راه دور به عنوان درایویشن‌های با خروجی ثابت {#ssec-dhall-remote-imports-as-fod}

`dhall-to-nixpkgs` قابلیت دریافت و ساخت درون‌ریزی‌های راه دور را به عنوان درایویشن‌های با خروجی ثابت با استفاده از بررسی یکپارچگی Dhall آن‌ها دارد. این روش گاهی از بسته‌بندی دستی همهٔ درون‌ریزی‌های راه دور آسان‌تر است.

از این قابلیت می‌توان به صورت زیر استفاده کرد:

```ShellSession
$ dhall-to-nixpkgs directory --fixed-output-derivations ~/proj/dhall-semver
{ buildDhallDirectoryPackage, buildDhallUrl }:
  buildDhallDirectoryPackage {
    name = "proj";
    src = ~/proj/dhall-semver;
    file = "package.dhall";
    source = false;
    document = false;
    dependencies = [
      (buildDhallUrl {
        url = "https://prelude.dhall-lang.org/v17.0.0/package.dhall";
        hash = "sha256-ENs8kZwl6QRoM9+Jeo/+JwHcOQ+giT2VjDQwUkvlpD4=";
        dhallHash = "sha256:10db3c919c25e9046833df897a8ffe2701dc390fa0893d958c3430524be5a43e";
        })
      ];
    }
```

در اینجا، وابستگی `Prelude` مربوط به `dhall-semver` به جای اینکه به عنوان یک آرگومان تابع پاس داده شود، با استفاده از تابع کمک‌رسان `buildDhallUrl` دریافت و ساخته می‌شود.

## بازنشانی نسخه‌های وابستگی {#ssec-dhall-overriding-dependency-versions}

فرض کنید عبارت نمونه‌ی `true.dhall` خود را طوری تغییر دهیم که به نسخه قدیمی‌تری از Prelude (19.0.0) وابسته باشد:

```dhall
-- ./true.dhall

let Prelude =
      https://prelude.dhall-lang.org/v19.0.0/package.dhall
        sha256:eb693342eb769f782174157eba9b5924cf8ac6793897fc36a31ccbd6f56dafe2

in  Prelude.Bool.not False
```

اگر سعی کنیم آن عبارت را مجدداً بسازیم، فرآیند ساخت شکست خواهد خورد:

```ShellSession
$ nix build --file ./example.nix dhallPackages.true
builder for '/nix/store/0f1hla7ff1wiaqyk1r2ky4wnhnw114fi-true.drv' failed with exit code 1; last 10 log lines:

  Dhall was compiled without the 'with-http' flag.

  The requested URL was: https://prelude.dhall-lang.org/v19.0.0/package.dhall


  4│       https://prelude.dhall-lang.org/v19.0.0/package.dhall
  5│         sha256:eb693342eb769f782174157eba9b5924cf8ac6793897fc36a31ccbd6f56dafe2

  /nix/store/rsab4y99h14912h4zplqx2iizr5n4rc2-true.dhall:4:7
[1 built (1 failed), 0.0 MiB DL]
error: build of '/nix/store/0f1hla7ff1wiaqyk1r2ky4wnhnw114fi-true.drv' failed
```

… زیرا Prelude پیش‌فرض انتخاب‌شده توسط بازبینی `94b2848559b12a8ed1fe433084686b2a81123c99` از Nixpkgs، نسخه 20.1.0 است که بررسی تمامیت یکسانی با نسخه 19.0.0 ندارد. این بدان معناست که نسخه 19.0.0 ذخیره‌شده در حافظهٔ پنهان نیست و مفسر مجاز نیست به درون‌ریزی URL بازگردد.

با این حال، می‌توانیم با استفاده از `dhall-to-nixpkgs` نسخه پیش‌فرض Prelude را بازنشانی کنیم تا یک بسته Dhall برای Prelude مورد نظر خود ایجاد کنیم:

```ShellSession
$ dhall-to-nixpkgs github https://github.com/dhall-lang/dhall-lang.git \
    --name Prelude \
    --directory Prelude \
    --rev v19.0.0 \
    > Prelude.nix
```

… و سپس ارجاع به آن بسته در overlay Dhall خود، یا با بازنشانی سراسری Prelude برای تمامی بسته‌ها، به این صورت:

```nix
{
  dhallOverrides = self: super: {
    true = self.callPackage ./true.nix { };

    Prelude = self.callPackage ./Prelude.nix { };
  };
}
```

… یا بازنشانی گزینشی وابستگی Prelude فقط برای بسته `true`، به این صورت:

```nix
{
  dhallOverrides = self: super: {
    true = self.callPackage ./true.nix {
      Prelude = self.callPackage ./Prelude.nix { };
    };
  };
}
```

## بازنشانی‌ها {#ssec-dhall-overrides}

شما می‌توانید هر یک از آرگومان‌های `buildDhallGitHubPackage` یا `buildDhallDirectoryPackage` را با استفاده از صفت (attribute) `overridePackage` یک بسته بازنشانی کنید.
برای نمونه، فرض کنید می‌خواهیم `source = true` را تنها برای Prelude به صورت انتخابی فعال کنیم. می‌توانیم این کار را به شکل زیر انجام دهیم:

```nix
{
  dhallOverrides = self: super: {
    Prelude = super.Prelude.overridePackage { source = true; };

    # ...
  };
}
```

[semantic-integrity-checks]: https://docs.dhall-lang.org/tutorials/Language-Tour.html#installing-packages
