# Octave {#sec-octave}

## مقدمه {#ssec-octave-introduction}

Octave یک زبان برنامه‌نویسی و محیط علمی ماژولار است.
اکثر بسته‌های پشتیبانی‌شده توسط Octave از [

```ShellSession
$ nix-build -A octavePackages.symbolic
```

برای نصب آن در پروفایل کاربر خود، این دستور را از ریشه مخزن اجرا کنید:

```ShellSession
$ nix-env -f. -iA octavePackages.symbolic
```

شما می‌توانید با استفاده از تابع پاس‌داده‌شده‌ی `withPackages`، Octave را همراه با بسته‌ها بسازید.

```ShellSession
$ nix-shell -p 'octave.withPackages (ps: with ps; [ symbolic ])'
```

این کار در یک فایل `shell.nix` نیز کار خواهد کرد.

```nix
{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  nativeBuildInputs = with pkgs; [ (octave.withPackages (opkgs: with opkgs; [ symbolic ])) ];
}
```

due to Octave maintaining a text-based database about which packages are installed where.`
        *   این موضوع به این دلیل است که Octave یک پایگاه داده متنی از اینکه چه بسته‌هایی در کجا نصب شده‌اند نگهداری می‌کند.

    *   `To this end, when all the requested packages have been built, the Octave package and all its add-on packages are put together into an environment, similar to Python.`
        *   به

1. نخست، تمام باینری‌های Octave به‌گونه‌ای پوشانده می‌شوند که متغیر محیطی `OCTAVE_SITE_INITFILE` روی فایلی در `$out` تنظیم شود؛ این کار برای اینکه Octave بتواند
