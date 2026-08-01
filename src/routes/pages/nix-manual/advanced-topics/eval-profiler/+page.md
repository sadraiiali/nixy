# 7.6. پروفایلر ارزیابی

ارزیاب Nix از [ارزیابی](/pages/nix-manual/language/evaluation)
[پروفایل‌سازی](&lt;https://en.wikipedia.org/wiki/Profiling_(computer_programming)&gt;)
سازگار با `flamegraph.pl` پشتیبانی می‌کند. این ابزار پروفایل‌سازی، پشته‌ی فراخوانی تابع nix را در فواصل زمانی منظم نمونه‌برداری می‌کند. این قابلیت را می‌توان با تنظیم
[`eval-profiler`](/pages/nix-manual/command-ref/conf-file#conf-eval-profiler)
فعال کرد:

```shell
$ nix-instantiate "<nixpkgs>" -A hello --eval-profiler flamegraph
```

فرکانس نمونه‌برداری پشته (stack sampling frequency) و مسیر فایل خروجی را می‌توان با گزینه‌های
[`eval-profile-file`](/pages/nix-manual/command-ref/conf-file#conf-eval-profile-file)
و [`eval-profiler-frequency`](/pages/nix-manual/command-ref/conf-file#conf-eval-profiler-frequency)
پیکربندی کرد. به‌طور پیش‌فرض، پروفایل جمع‌آوری‌شده در فایل `nix.profile` در دایرکتوری کاری فعلی ذخیره می‌شود.

پروفایل جمع‌آوری‌شده می‌تواند مستقیماً توسط `flamegraph.pl` مصرف شود:

```shell
$ flamegraph.pl nix.profile > flamegraph.svg
```

اطلاعات خط در پروفایل حاوی موقعیت مکان [محل فراخوانی](https://en.wikipedia.org/wiki/Call_site) و نام تابعی است که در حال فراخوانی است (در صورت وجود). برای مثال:

```
/nix/store/2q71fdvr4h33g9832hiriwnf20fn630l-source/pkgs/top-level/default.nix:167:5:primop import
```

در اینجا پرایموپ `import` در مسیر `/nix/store/2q71fdvr4h33g9832hiriwnf20fn630l-source/pkgs/top-level/default.nix:167:5` فراخوانی می‌شود.
