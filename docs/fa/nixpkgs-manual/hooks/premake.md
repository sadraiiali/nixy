# Premake {#premake-hook}

این قلاب راه‌اندازی تلاش می‌کند بسته را با استفاده از [سیستم پیکربندی ساخت Premake](https://premake.github.io/) پیکربندی کند. این قلاب در صورت عدم وجود، به‌طور پیش‌فرض `configurePhase` را بازنویسی می‌کند.

[]{#premake-hook-premakefile} Premakefile مورد استفاده را می‌توان با تنظیم `premakefile` در derivation تعیین کرد.

[]{#premake-hook-premakeFlagsArray} پرچم‌های ارسالی به Premake را می‌توان با افزودن رشته‌ها به فهرست `premakeFlags` پیکربندی کرد.
