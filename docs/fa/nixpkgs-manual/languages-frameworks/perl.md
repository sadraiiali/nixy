# Perl {#sec-language-perl}

## اجرای برنامه‌های Perl در شل {#ssec-perl-running}

هنگام اجرای یک اسکریپت Perl، ممکن است با خطایی مانند `./myscript.pl: bad interpreter: /usr/bin/perl: no such file or directory` مواجه شوید. این اتفاق زمانی می‌افتد که اسکریپت انتظار دارد Perl در `/usr/bin/perl` نصب شده باشد، که هنگام استفاده از Perl از Nixpkgs این‌طور نیست. می‌توانید با تغییر سطر اول به شکل زیر، اسکریپت را برطرف کنید:

```perl
#!/usr/bin/env perl
```

تا نصب Perl از متغیر محیطی `PATH` گرفته شود، یا Perl مستقیماً با:

```ShellSession
$ perl ./myscript.pl
```

هنگامی که اسکریپت از یک کتابخانه Perl استفاده می‌کند که به صورت سراسری نصب نشده است، ممکن است با خطایی مانند `Can't locate DB_File.pm in @INC (you may need to install the DB_File module)` مواجه شوید. در این صورت، می‌توانید از `nix-shell` برای راه‌اندازی یک شل آنی (ad-hoc) به همراه آن کتابخانه نصب‌شده استفاده کنید، برای نمونه:

```ShellSession
$ nix-shell -p perl perlPackages.DBFile --run ./myscript.pl
```

اگر همیشه از اسکریپت در محیط‌هایی استفاده می‌کنید که `nix-shell` در دسترس است، می‌توانید فراخوانی `nix-shell` را به این شکل در شبانگ قرار دهید:

```perl
#!/usr/bin/env nix-shell
#! nix-shell -i perl -p perl perlPackages.DBFile
```

## بسته‌بندی برنامه‌های Perl {#ssec-perl-packaging}

Nixpkgs تابع `buildPerlPackage` را ارائه می‌دهد؛ یک تابع عمومی سازنده بسته برای هر بسته Perl که دارای یک `Makefile.PL` استاندارد باشد. این تابع در [pkgs/development/

```nix
{
  ClassC3 = buildPerlPackage rec {
    pname = "Class-C3";
    version = "0.21";
    src = fetchurl {
      url = "mirror://cpan/authors/id/F/FL/FLORA/Class-C3-${version}.tar.gz";
      hash = "sha256-/5GE5xHT0uYGOQxroqj6LMU7CtKn2s6vMVoSXxL4iK4=";
    };
  };
}
```

به استفاده از `mirror://cpan/` و همچنین `pname` و `version` در تعریف URL دقت کنید تا مطمئن شوید صفت `pname` با سورس واقعی که در حال بارگیری آن هستیم سازگار است. بسته‌های Perl در `all-packages.nix` از طریق متغیر `perlPackages` در دسترس قرار می‌گیرند. برای نمونه، اگر بسته‌ای دارید که به `ClassC3` نیاز دارد، معمولاً این‌گونه می‌نویسید:

```nix
{
  foo = import ../path/to/foo.nix {
    inherit
      stdenv
      fetchurl # ...
      ;
    inherit (perlPackages) ClassC3;
  };
}
```

در `all-packages.nix`. می‌توانید ساخت یک بسته Perl را به صورت زیر تست کنید:

```ShellSession
$ nix-build -A perlPackages.ClassC3
```

برای نصب آن با `nix-env` در عوض: `nix-env -f. -iA perlPackages.ClassC3`.

بنابراین `buildPerlPackage` چه کاری انجام می‌دهد؟ موارد

```nix
{
  buildPerlPackage,
  fetchurl,
  db,
}:

buildPerlPackage rec {
  pname = "BerkeleyDB";
  version = "0.36";

  src = fetchurl {
    url = "mirror://cpan/authors/id/P/PM/PMQS/BerkeleyDB-${version}.tar.gz";
    hash = "sha256-4Y+HGgGQqcOfdiKcFIyMrWBEccVNVAMDBWZlFTMorh8=";
  };

  preConfigure = ''
    echo "LIB = ${db.out}/lib" > config.in
    echo "INCLUDE = ${db.dev}/include" >> config.in
  '';
}
```

وابستگی‌ها به سایر بسته‌های Perl را می‌توان در صفات `buildInputs` و `propagatedBuildInputs` مشخص کرد. اگر موردی منحصراً یک وابستگی زمان ساخت است، از `buildInputs` استفاده کنید؛ اگر (همچنین) یک وابستگی زمان اجرا است، از `propagatedBuildInputs

```nix
{
  ClassC3Componentised = buildPerlPackage rec {
    pname = "Class-C3-Componentised";
    version = "1.0004";
    src = fetchurl {
      url = "mirror://cpan/authors/id/A/AS/ASH/Class-C3-Componentised-${version}.tar.gz";
      hash = "sha256-ASO9rV/FzJYZ0BH572Fxm2ZrFLMZLFATJng1NuU4FHc=";
    };
    propagatedBuildInputs = [
      ClassC3
      ClassInspector
      TestException
      MROCompat
    ];
  };
}
```

### تولید از CPAN {#ssec-generation-from-CPAN}

عبارت‌های Nix برای بسته‌های Perl می‌توانند (تقریباً) به طور خودکار از CPAN تولید شوند. این کار توسط برنامه `nix-generate-from-cpan` انجام می‌شود که می‌توان آن را به صورت زیر نصب کرد:

```ShellSession
$ nix-env -f "<nixpkgs>" -iA nix-generate-from-cpan
```

برای استفاده از آخرین نسخه، `<nixpkgs>` را با مسیر کلونی از nixpkgs جایگزین کنید.

این برنامه نام یک ماژول Perl را

```ShellSession
$ nix-generate-from-cpan XML::Simple
  XMLSimple = buildPerlPackage rec {
    pname = "XML-Simple";
    version = "2.22";
    src = fetchurl {
      url = "mirror://cpan/authors/id/G/GR/GRANTM/XML-Simple-2.22.tar.gz";
      hash = "sha256-uUUO8i6pZErl1q2ghtxDAPoQW+BQogMOvU79KMGY60k=";
    };
    propagatedBuildInputs = [ XMLNamespaceSupport XMLSAX XMLSAXExpat ];
    meta = {
      description = "API for simple XML files";
      license = with lib.licenses; [ artistic1 gpl1Plus ];
    };
  };
```

ور غیرمستقیم) یک ماژول بومی را درون‌ریزی کند. در این حالت، باید یک استاب (stub) برای آن ماژول بسازید که `Makefile.PL` را
