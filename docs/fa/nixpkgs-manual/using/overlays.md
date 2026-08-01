برای پیکربندی سیستم NixOS و پیکربندی کاربر فراهم می‌کند: از همان فایل می‌توان به عنوان `overlays.nix` استفاده کرد و آن را به عنوان مقدار `nixpkgs.overlays` درون‌ریزی نمود.

## Defining overlays {#sec-overlays-definition}
## تعریف اورلای‌ها {#sec-overlays-definition}

Overlays are Nix functions which accept two arguments, conventionally called either `

```nix
final: prev:

{
  boost = prev.boost.override { python = final.python3; };
  rr = prev.callPackage ./pkgs/rr { stdenv = final.stdenv_32bit; };
}
```

)

    فورک AMD از کتابخانه BLIS، با صفت (attribute) `amd-blis`، نرم‌افزار BLIS را با بهینه‌سازی‌هایی برای پردازنده‌های مدرن AMD گسترش می‌دهد. تغییرات معمولاً پس از مدتی به پروژه بالادستی BLIS ارسال می‌شوند. با این حال، AMD BLIS معمولاً برخی بهبودهای عملکردی را روی پردازنده‌های AMD Zen ارائه می‌دهد. کتاب

های `blasProvider` و `lapackProvider` از پیاده‌سازی‌های متفاوتی استفاده کنند. این قابلیت می‌تواند برای انتخاب یک ارائه‌دهنده متفاوت به کار رود. ارائه‌دهندگان

```nix
final: prev:

{
  blas = prev.blas.override { blasProvider = final.mkl; };

  lapack = prev.lapack.override { lapackProvider = final.mkl; };
}
```

این اورلی از کتابخانه MKL شرکت Intel برای هر دو رابط BLAS و LAPACK استفاده می‌کند. توجه داشته باشید که همین کار در زمان اجرا با استفاده از `LD_LIBRARY_PATH` مربوط به `libblas.so.3` و `liblapack.so.3` نیز امکان‌پذیر است. برای مثال:

```ShellSession
$ LD_LIBRARY_PATH=$(nix-build -A mkl)/lib${LD_LIBRARY_PATH:+:}$LD_LIBRARY_PATH nix-shell -p octave --run octave
```

Intel MKL هنگام اجرا با چند پردازنده، به یک پیاده‌سازی `openmp` نیاز دارد. به‌طور پیش‌فرض، در صورتی که گزینه‌ی دیگری مشخص نشده باشد، `

```nix
final: prev:

{
  blas = prev.blas.override { blasProvider = final.lapack-reference; };

  lapack = prev.lapack.override { lapackProvider = final.lapack-reference; };
}
```

, and derivations need to specify an assertion to prevent this.
        *   برخی نرم‌افزارها با `ILP64` کار نمی‌کنند و درایویشن‌ها باید برای جلوگیری از این

```nix
{
  stdenv,
  blas,
  lapack,
  ...
}:

assert (!blas.isILP64) && (!lapack.isILP64);

stdenv.mkDerivation {
  # ...
}
```

### تعویض پیاده‌سازی MPI {#sec-overlays-alternatives-mpi}

تمام برنامه‌هایی که با پشتیبانی از [MPI](https://en.wikipedia.org/wiki/Message_

```nix
final: prev:

{
  mpi = final.mpich;
}
```
