# Steam {#sec-steam}

## Steam در Nix {#sec-steam-nix}

Steam به عنوان یک فایل `.deb` توزیع می‌شود، در حال حاضر فقط به صورت یک بسته i686 (بسته amd64 فقط حاوی مستندات است). هنگامی که استخراج می‌شود، اسکریپتی به نام `steam` دارد که در اوبونتو (توزیع هدف آن‌ها) در مسیر `/usr/bin` قرار می‌گیرد. وقتی این اسکریپت برای اولین بار اجرا می‌شود، برخی فایل‌ها را در پوشه خانه کاربر کپی می‌کند، که شامل اسکریپت دیگری است که در نهایت مسئول اجرای باینری steam است که آن هم در `$HOME` قرار دارد.

مشکلات و محدودیت‌های Nix:

- ما `/bin/bash` را نداریم و بسیاری از اسکریپت‌ها به آن اشاره می‌کنند. همین موضوع در مورد `/usr/bin/python` نیز صدق می‌کند.
- ما لودر پویا را در `/lib` نداریم.
- اسکریپت `steam.sh` موجود در `$HOME` قابل پچ کردن نیست، زیرا توسط steam بررسی و بازنویسی می‌شود.
- باینری steam قابل پچ کردن نیست، آن هم بررسی می‌شود.

رویکرد فعلی برای استقرار Steam در NixOS، ساخت یک محیط chroot سازگار با FHS است، همان‌طور که در [اینجا](https://sandervanderburg.blogspot.com/2013/09/composing-fhs-compatible-chroot.html) مستند شده‌است. این به ما اجازه
```ShellSession
  strace steam
  ```

تا ببینید چه چیزی باعث عدم اجرای Steam می‌شود.

- **استفاده از درایورهای FOSS Radeon یا nouveau (nvidia)**

  - Steam همراه
```
    steam.sh: line 713: 7842 Segmentation fault (core dumped)
    ```

. To use it, install the `steam-run` package and run the game with:`
        *   `chroot` سازگار با FHS که برای Steam استفاده می‌شود،

```
steam-run ./foo
```
