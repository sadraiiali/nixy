، محیط‌های Julia را همراه با بسته‌های اضافی بسازید.

Line 12:
This function accepts a list of strings representing Julia package names.
- function -> تابع
- package names -> نام‌های بسته

```nix
julia.withPackages [ "Plots" ]
```

آرگومان‌ها را می‌توان با استفاده از `.override` ارسال کرد.
برای مثال:

```nix
(julia.withPackages.override {
  precompile = false; # Turn off precompilation
})
  [ "Plots" ]
```

در اینجا یک روش خوب برای اجرای یک محیط Julia با یک دستور تک‌خطی شل آمده است:

```sh
nix-shell -p 'julia.withPackages ["Plots"]' --run julia
```

### آرگومان‌ها {#julia-withpackage-arguments}

* `precompile`: این‌که آیا `Pkg.precompile()` روی محیط تولیدشده اجرا شود یا خیر.

  این کار وارد کردن بسته‌ها را سریع‌تر می‌کند، اما ممکن است در برخی موارد با شکست مواجه شود.
  به عنوان مثال، یک مشکل بالادستی (upstream) در `Gtk.jl` وجود دارد که از کارکرد پیش‌کمپایل در محیط ایزوله (sandbox) ساخت Nix جلوگیری می‌کند، زیرا کد پیش‌کمپایل‌شده تلاش می‌کند به یک صفحه نمایش دسترسی پیدا کند.
  بسته‌هایی از این دست، اگر با `precompile=false` ساخته شوند و سپس پس از شروع محیط در صورت نیاز پیش‌کمپایل شوند، به خوبی کار خواهند کرد.

  پیش‌فرض: `true`

* `extraLibs`: وابستگی‌های کتابخانه‌ای اضافی که در `LD_LIBRARY_PATH` برای
