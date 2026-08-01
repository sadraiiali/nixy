# Idris {#idris}

## نصب Idris {#installing-idris}

ساده‌ترین راه برای به دست آوردن یک نسخه کارآمد idris، نصب صفت (attribute) `idris` است:

```ShellSession
$ nix-env -f "<nixpkgs>" -iA idris
```

با این حال، این کار تنها کتابخانه‌های `prelude` و `base` را فراهم می‌کند. برای نصب idris به همراه کتابخانه‌های اضافی، می‌توانید از تابع `idrisPackages.with-packages` استفاده کنید؛ به عنوان مثال در یک اورلی در `~/.config/nixpkgs/overlays/my-idris.nix`:

```nix
self: super: {
  myIdris =
    with self.idrisPackages;
    with-packages [
      contrib
      pruviloj
    ];
}
```

و سپس:

```ShellSession
$ # On NixOS
$ nix-env -iA nixos.myIdris
$ # On non-NixOS
$ nix-env -iA nixpkgs.myIdris
```

برای مشاهده همه بسته‌های موجود Idris:

```ShellSession
$ # On NixOS
$ nix-env -qaPA nixos.idrisPackages
$ # On non-NixOS
$ nix-env -qaPA nixpkgs.idrisPackages
```

به همین ترتیب، ورود به یک `nix-shell`:

```ShellSession
$ nix-shell -p 'idrisPackages.with-packages (with idrisPackages; [ contrib pruviloj ])'
```

## راه‌اندازی Idris با پشتیبانی از کتابخانه‌ها {#starting-idris-with-library-support}

برای دسترسی به این کتابخانه‌ها در idris، آن را به ازای هر کتابخانه با آرگومان `-p <library name>` فراخوانی کنید:

```ShellSession
$ nix-shell -p 'idrisPackages.with-packages (with idrisPackages; [ contrib pruviloj ])'
[nix-shell:~]$ idris -p contrib -p pruviloj
```

فهرستی از تمام بسته‌های موجود که باینری Idris به آن‌ها دسترسی دارد، از طریق `--listlibs` در دسترس است:

```ShellSession
$ idris --listlibs
00prelude-idx.ibc
pruviloj
base
contrib
prelude
00pruviloj-idx.ibc
00base-idx.ibc
00contrib-idx.ibc
```

## ساخت یک پروژه Idris با Nix {#building-an-idris-project-with-nix}

به‌عنوان مثالی از نحوهٔ ایجاد یک عبارت نیکس (Nix expression) برای یک بسته Idris، در ادامه عبارت مربوط به `idrisPackages.yaml` آورده شده است:

```nix
{
  lib,
  build-idris-package,
  fetchFromGitHub,
  contrib,
  lightyear,
}:
build-idris-package {
  name = "yaml";
  version = "2018-01-25";

  # This is the .ipkg file that should be built, defaults to the package name
  # In this case it should build `Yaml.ipkg` instead of `yaml.ipkg`
  # This is only necessary because the yaml packages ipkg file is
  # different from its package name here.
  ipkgName = "Yaml";
  # Idris dependencies to provide for the build
  idrisDeps = [
    contrib
    lightyear
  ];

  src = fetchFromGitHub {
    owner = "Heather";
    repo = "Idris.Yaml";
    rev = "5afa51ffc839844862b8316faba3bafa15656db4";
    hash = "sha256-h28F9EEPuvab6zrfeE+0k1XGQJGwINnsJEG8yjWIl7w=";
  };

  meta = {
    description = "Idris YAML lib";
    homepage = "https://github.com/Heather/Idris.Yaml";
    license = lib.licenses.mit;
    maintainers = [ lib.maintainers.brainrape ];
  };
}
```

با فرض اینکه این فایل با نام `yaml.nix` ذخیره شده باشد، با استفاده از روش زیر قابل ساخت است:

```ShellSession
$ nix-build -E '(import <nixpkgs> {}).idrisPackages.callPackage ./yaml.nix {}'
```

یا می‌توان از

```nix
with import <nixpkgs> { };

{
  yaml = idrisPackages.callPackage ./yaml.nix { };
}
```

در یک فایل دیگر (مثلاً `default.nix`) تا بتوانید آن را با

```ShellSession
$ nix-build -A yaml
```

## ارسال گزینه‌ها به دستورات `idris` {#passing-options-to-idris-commands}

تابع `build-idris-package` همچنین مقادیر ورودی اختیاری را برای تنظیم گزینه‌های اضافی جهت دستورات `idris` مورد استفاده ارائه می‌دهد.

به‌طور خاص، می‌توانید `idrisBuildOptions`، `idrisTestOptions`، `idrisInstallOptions` و `idrisDocOptions` را جهت ارائه گزینه‌های اضافی به دستور `idris` به ترتیب هنگام ساخت، تست، نصب و تولید مستندات برای بسته خود تنظیم کنید.

برای نمونه می‌توانید تنظیم کنید

```nix
build-idris-package {
  idrisBuildOptions = [
    "--log"
    "1"
    "--verbose"
  ];

  # ...
}
```

برای درخواست خروجی تفصیلی در طول فاز ساخت `idris`.
