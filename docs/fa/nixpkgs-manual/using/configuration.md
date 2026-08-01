# پیکربندی سراسری {#chap-packageconfig}

Nix بر اساس متاداده‌های یک بسته، دارای پیش‌فرض‌های مشخصی درباره‌ی این است که کدام بسته‌ها می‌توانند یا نمی‌توانند نصب شوند.
به‌طور پیش‌فرض، اگر هر یک از معیارهای زیر برقرار باشد، Nix از نصب جلوگیری خواهد کرد:

- بسته خراب تلقی شود و مقدار `meta.broken` آن برابر با `true` تنظیم شده باشد.

- بسته برای اجرا روی سیستم موردنظر در نظر گرفته نشده باشد، زیرا هیچ‌یک از `meta.platforms` آن با سیستم داده‌شده مطابقت ندارد.

- مقدار `meta.license` بسته روی مجوزی تنظیم شده باشد که غیرآزاد محسوب می‌شود.

- بسته دارای آسیب‌پذیری‌های امنیتی شناخته‌شده باشد اما به دلیلی به‌روزرسانی نشده یا نمی‌تواند بشود، و فهرستی از مشکلات در `meta.knownVulnerabilities` بسته وارد شده باشد.

- مشکلاتی برای بسته‌ها وجود داشته باشد که باید تأیید و پذیرفته شوند، مانند إعلامیه‌های منسوخ‌شدن.

هر یک از این معیارها را می‌توان در پیکربندی Nixpkgs تغییر داد.

:::{.note}
همه این موارد در طول ارزیابی بررسی می‌شوند و این بررسی شامل هر بسته‌ای است که ارزیابی می‌شود.
به‌ویژه، تمام وابستگی‌های زمان ساخت بررسی می‌شوند.
:::

پیکربندی Nixpkgs یک کاربر در یک فایل پیکربندی مخصوص به خود کاربر در مسیر `~/.config/nixpkgs/config.nix` ذخیره می‌شود. برای مثال:

```nix
{ allowUnfree = true; }
```

:::{.caution}
نرم‌افزارهای غیرآزاد (Unfree) در ادغام مداوم (CI) مربوط به Nixpkgs تست یا ساخته نمی‌شوند و بنابراین در کش ذخیره نمی‌شوند.
اکثر مجوزهای غیرآزاد، اجرای نرم
```ShellSession
    $ export NIXPKGS_ALLOW_BROKEN=1
    ```

-   برای اجازه دادن دائمی به ساخت بسته‌های شکسته با نامی مشخص، می‌توانید `problems.handlers` مربوطه را به فایل پیکربندی کاربر
```nix
    {
      problems.handlers.hello.broken = "warn"; # or "ignore"
    }
    ```

- برای مجاز کردن دائمی ساخت همه بسته‌های خراب، می‌توانید `allowBroken = true;` را به فایل پیکربندی کاربر خود اضافه کنید، به این صورت:
```nix
    { allowBroken = true; }
    ```


## نصب بسته‌ها روی سیستم‌های پشتیبانی‌نشده {#sec-allow-unsupported-system}

همچنین دو روش برای تلاش جهت کامپایل کردن
```ShellSession
    $ export NIXPKGS_ALLOW_UNSUPPORTED_SYSTEM=1
    ```

- برای مجاز کردن دائمی ساخت بسته‌های پشتیبانی‌نشده، می‌توانید `allowUnsupportedSystem = true;` را به فایل پیکربندی کاربر خود اضافه کنید، مانند این:
```nix
    { allowUnsupportedSystem = true; }
    ```

تفاوت بین پشتیبانی‌نشدن یک بسته در برخی سیستم‌ها و خراب بودن آن، البته کمی مبهم است. اگر یک برنامه *باید* روی پلتفرم خاصی کار کند اما کار نمی‌کند، آن پلتفرم باید در
```ShellSession
    $ export NIXPKGS_ALLOW_UNFREE=1
    ```

- امکان مجاز کردن دائمی بسته‌های غیرآزاد به صورت مجزا، در حالی که بسته‌های غیرآزاد همچنان به طور پیش‌فرض مس
```nix
    { allowUnfreePredicate = (pkg: false); }
    ```

برای یک مثال کاربردی‌تر، مورد زیر را امتحان کنید. این پیکربندی تنها بسته‌های غیرآزاد با نام‌های roon-server و Visual Studio
```nix
    {
      allowUnfreePredicate =
        pkg:
        builtins.elem (lib.getName pkg) [
          "roon-server"
          "vscode"
        ];
    }
    ```

- همچنین امکان مجاز کردن و مسدود کردن پروانه‌هایی که به‌طور خاص قابل قبول یا غیرقابل قبول هستند، به ترتیب با استفاده از `allowlistedLicenses` و `blocklistedLicenses` وجود دارد.

    پیکربندی نمونه زیر، پروانه‌های `amd` و `wtfpl` را مجاز می‌کند:
```nix
    {
      allowlistedLicenses = with lib.licenses; [
        amd
        wtfpl
      ];
    }
    ```

پیکربندی نمونه زیر، مجوزهای `gpl3Only` و `agpl3Only` را در لیست سیاه قرار می‌دهد:
```nix
    {
      blocklistedLicenses = with lib.licenses; [
        agpl3Only
        gpl3Only
      ];
    }
    ```

github.com/NixOS/nixpkgs/blob/master/lib/licenses/licenses.nix) of the nixpkgs tree.`
->
`فهرست کاملی از مجوزها را
```ShellSession
    $ export NIXPKGS_ALLOW_INSECURE=1
    ```

-   امکان مجاز ساختن دائمی بسته‌های ناامن به‌صورت جداگانه وجود دارد، در حالی که همچنان سایر بسته‌های ناامن به‌طور پیش‌فرض با استفاده از گزینه پیکربندی `permittedInsecurePackages` در فایل پیکربندی کاربر مسدود می‌شوند.

    پیکربندی نمونه زیر اجازه نصب بسته ناامن فرضی `hello` نسخه `1.2.3` را می‌دهد:
```nix
    { permittedInsecurePackages = [ "hello-1.2.3" ]; }
    ```

- همچنین ساخت یک سیاست سفارشی در مورد بسته‌های ناامنی که مجاز یا غیرمجاز هستند، با بازنشانی گزینه پیکربندی `allowInsecurePredicate` امکان‌پذیر
```nix
    { allowInsecurePredicate = pkg: builtins.elem (lib.getName pkg) [ "ovftool" ]; }
    ```

structure strictly." Note indentation on first line: four spaces or indentation in input? Input has 4 spaces: `    Note that ...`. Let's preserve the indentation if present in original markdown.
3. No code fences invented.
4. Inline backticks unchanged (`permittedInsecurePackages`, `

```nix
{
  problems.matchers = [
    # Fail to build any packages which are about to be removed anyway
    {
      kind = "removal";
      handler = "error";
    }

    # Get warnings when using packages with no declared maintainers
    {
      kind = "maintainerless";
      handler = "warn";
    }

    # You deeply care about this package and want to absolutely know when it has any problems
    {
      package = "hello";
      handler = "error";
    }
  ];
}
```

تطبیق‌دهنده‌ها می‌توانند با یک یا چند مورد از نام بسته، نام مشکل یا نوع مشکل مطابقت داشته باشند.
اگر چند شرط وجود داشته باشد، برای انجام تطبیق باید همه

```nix
{
  packageOverrides = pkgs: rec {
    foo = pkgs.foo.override {
      # ...
    };
  };
}
```

## مرجع گزینه‌های `config` {#sec-config-options-reference}

صفات زیر را می‌توان در [`config`](#chap-packageconfig) پاس داد.

```{=include=} options
id-prefix: opt-
list-id: configuration-variable-list
source: ../config-options.json
```


## مدیریت اعلانی بسته‌ها {#sec-declarative-package-management}

### ساخت یک محیط {#sec-building-environment}

با استفاده از `packageOverrides` می‌توان بسته‌ها را به صورت اعلانی مدیریت کرد. این بدان معناست که می‌توانیم تمام بسته‌های مورد نظر خود را در یک عبارت نیکس (Nix expression) اعلانی فهرست کنیم. برای نمونه، جهت داشتن `aspell`، `bc`، `ffmpeg`، `coreutils`، `gdb`، `nix`، `emscripten`، `jq`، `nox` و `silver-searcher` می‌توانیم از موارد زیر در `~/.config/nixpkgs/config.nix` استفاده کنیم:

```nix
{
  packageOverrides =
    pkgs: with pkgs; {
      myPackages = pkgs.buildEnv {
        name = "my-packages";
        paths = [
          aspell
          bc
          coreutils
          gdb
          ffmpeg
          nix
          emscripten
          jq
          nox
          silver-searcher
        ];
      };
    };
}
```

برای نصب آن در محیط خود، می‌توانید صرفاً دستور `nix-env -iA nixpkgs.myPackages` را اجرا کنید. اگر می‌خواهید بسته‌هایی را که باید ساخته شوند از یک نسخه‌ی کاری `nixpkgs` بارگذاری کنید، کافی است `nix-env -f. -iA myPackages` را اجرا کنید. برای بررسی آنچه نصب شده است، فقط نگاهی به `~/.nix-profile/` بیندازید. می‌توانید ببینید که موارد زیادی نصب شده‌اند. برخی از این موارد مفید هستند و برخی دیگر خیر. بیایید به Nixpkgs بگوییم تنها مواردی را پیوند دهد که ما می‌خواهیم:

```nix
{
  packageOverrides =
    pkgs: with pkgs; {
      myPackages = pkgs.buildEnv {
        name = "my-packages";
        paths = [
          aspell
          bc
          coreutils
          gdb
          ffmpeg
          nix
          emscripten
          jq
          nox
          silver-searcher
        ];
        pathsToLink = [
          "/share"
          "/bin"
        ];
      };
    };
}
```

`pathsToLink` به Nixpkgs می‌گوید فقط مسیرهای فهرست‌شده را پیوند دهد که این کار موارد اضافی موجود در پروفایل را حذف می‌کند. `/bin` و `/share` پیش‌فرض‌های خوبی برای یک

```nix
{
  packageOverrides =
    pkgs: with pkgs; {
      myPackages = pkgs.buildEnv {
        name = "my-packages";
        paths = [
          aspell
          bc
          coreutils
          ffmpeg
          nix
          emscripten
          jq
          nox
          silver-searcher
        ];
        pathsToLink = [
          "/share/man"
          "/share/doc"
          "/bin"
        ];
        extraOutputsToInstall = [
          "man"
          "doc"
        ];
      };
    };
}
```

این امر مستندات مفیدی را برای استفاده از بسته‌هایمان در اختیار ما قرار می‌دهد. با این حال، اگر واقعاً می‌خواهیم آن manpageها توسط `man` شناسایی شوند، باید محیط خود را راه‌اندازی کنیم. این کار را نیز می‌توان درون عبارت‌های Nix مدیریت کرد.

```nix
{
  packageOverrides = pkgs: {
    myProfile = pkgs.writeText "my-profile" ''
      export PATH=$HOME/.nix-profile/bin:/nix/var/nix/profiles/default/bin:/sbin:/bin:/usr/sbin:/usr/bin
      export MANPATH=$HOME/.nix-profile/share/man:/nix/var/nix/profiles/default/share/man:/usr/share/man
    '';
    myPackages = pkgs.buildEnv {
      name = "my-packages";
      paths = with pkgs; [
        (runCommand "profile" { } ''
          mkdir -p $out/etc/profile.d
          cp ${myProfile} $out/etc/profile.d/my-profile.sh
        '')
        aspell
        bc
        coreutils
        ffmpeg
        man
        nix
        emscripten
        jq
        nox
        silver-searcher
      ];
      pathsToLink = [
        "/share/man"
        "/share/doc"
        "/bin"
        "/etc"
      ];
      extraOutputsToInstall = [
        "man"
        "doc"
      ];
    };
  };
}
```

برای اینکه این مورد به‌طور کامل کار کند، باید هنگام ورود به سیستم، این اسکریپت نیز سورس (source) شده باشد. سعی کنید چیزی شبیه به این را به فایل `~/.profile` خود اضافه کنید:

```ShellSession
#!/bin/sh
if [ -d "${HOME}/.nix-profile/etc/profile.d" ]; then
  for i in "${HOME}/.nix-profile/etc/profile.d/"*.sh; do
    if [ -r "$i" ]; then
      . "$i"
    fi
  done
fi
```

اکنون کافی است `. "${HOME}/.profile"` را اجرا کنید؛ سپس می‌توانید بارگیری صفحات man را از محیط خود آغاز کنید.

### راه‌اندازی GNU info {#sec-gnu-info-setup}

پیکربندی GNU info کمی پیچیده‌تر از صفحات man است. برای عملکرد صحیح، info نیاز دارد که یک پایگاه داده ایجاد شود. این کار با اعمال برخی تغییرات کوچک در اسکریپت‌های محیطی ما امکان‌پذیر است.

```nix
{
  packageOverrides = pkgs: {
    myProfile = pkgs.writeText "my-profile" ''
      export PATH=$HOME/.nix-profile/bin:/nix/var/nix/profiles/default/bin:/sbin:/bin:/usr/sbin:/usr/bin
      export MANPATH=$HOME/.nix-profile/share/man:/nix/var/nix/profiles/default/share/man:/usr/share/man
      export INFOPATH=$HOME/.nix-profile/share/info:/nix/var/nix/profiles/default/share/info:/usr/share/info
    '';
    myPackages = pkgs.buildEnv {
      name = "my-packages";
      paths = with pkgs; [
        (runCommand "profile" { } ''
          mkdir -p $out/etc/profile.d
          cp ${myProfile} $out/etc/profile.d/my-profile.sh
        '')
        aspell
        bc
        coreutils
        ffmpeg
        man
        nix
        emscripten
        jq
        nox
        silver-searcher
        texinfoInteractive
      ];
      pathsToLink = [
        "/share/man"
        "/share/doc"
        "/share/info"
        "/bin"
        "/etc"
      ];
      extraOutputsToInstall = [
        "man"
        "doc"
        "info"
      ];
      postBuild = ''
        if [ -x $out/bin/install-info -a -w $out/share/info ]; then
          shopt -s nullglob
          for i in $out/share/info/*.info $out/share/info/*.info.gz; do
              $out/bin/install-info $i $out/share/info/dir
          done
        fi
      '';
    };
  };
}
```

`postBuild` به Nixpkgs می‌گوید پس از ساخت محیط، دستوری را اجرا کند. در این حالت، `install-info` صفحات info نصب‌شده را به `dir` که گره ریشه پیش‌فرض GNU info است اضافه می‌کند. توجه داشته باشید که `texinfoInteractive` به محیط اضافه شده‌است تا دستور `install-info` را در دسترس قرار دهد.
