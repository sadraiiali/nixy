# <a id="setup-hook-check-phase-thread-limit"></a> checkPhaseThreadLimitHook

این قلاب، مقدار پیش‌فرض مجموعه‌ای از متغیرهای محیطی را که برای کنترل تعداد تردها شناخته می‌شوند، برابر با ۱ قرار می‌دهد. در غیر این صورت، بسیاری از این متغیرها به صورت پیش‌فرض روی `$(nproc)` تنظیم می‌شوند که اگر کارهای ساخت Nix و هسته‌های ساخت از قبل برای بهره‌برداری کامل از ظرفیت محاسباتی یک سازنده (Builder) بدون موازی‌سازی اضافی تنظیم شده باشند، باعث بیش‌بارگذاری سنگین روی ماشین‌های ساخت می‌شود.

در حال حاضر متغیرهای محیطی زیر را تنظیم می‌کند:
- [`OMP_NUM_THREADS`](https://www.openmp.org/spec-html/5.0/openmpse50.html)
- [`OPENBLAS_NUM_THREADS`](https://github.com/OpenMathLib/OpenBLAS/blob/e7b45174355edec1f04de1cabcf5ca6a98ea7fbc/USAGE.md#how-can-i-use-openblas-in-multi-threaded-applications)
- [`MKL_NUM_THREADS`](https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2023-0/mkl-domain-num-threads.html)
- [`BLIS_NUM_THREADS`](https://github.com/flame/blis/blob/b8b75b4e19459f5d618b57aa814ca38b1d82eb82/docs/Multithreading.md#specifying-multithreading)
- `VECLIB_MAXIMUM_THREADS`: فقط روی darwin تأثیر می‌گذارد، ببینید: [`man 7 Accelerate`](https://manp.gs/mac/7/Accelerate)
- [`NUMBA_NUM_THREADS`](https://numba.readthedocs.io/en/stable/reference/envvars.html#threading-control)
- [`NUMEXPR_NUM_THREADS`](https://numexpr.readthedocs.io/en/latest/user_guide.html#threadpool-configuration)

از متغیر محیطی `NIX_CHECK_PHASE_DEFAULT_NUM_THREADS` می‌توان برای بازنشانی حد پیش‌فرض تعداد تردها استفاده کرد.
از `dontLimitCheckPhaseThreads = true;` می‌توان برای غیرفعال کردن محدودسازی ترد در یک بسته خاص استفاده کرد.

این قلاب برای بازنشانی تعاریف ازپیش‌موجود متغیرهای محیطی تعداد ترد تلاشی نخواهد کرد.
