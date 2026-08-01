# عیب‌یابی

این صفحه مجموعه‌ای از نکات برای حل مشکلاتی است که ممکن است هنگام استفاده از Nix با آن‌ها مواجه شوید.

## اگر یک کش باینری از کار افتاده یا غیرقابل دسترس باشد، چه باید کرد؟

گزینه [`--option substitute false`](/pages/nix-manual/command-ref/conf-file-prefix#conf-substitute) را به دستورات Nix پاس دهید.

## چگونه Nix را مجبور کنیم تا دوباره بررسی کند که آیا چیزی در کش باینری وجود دارد یا خیر؟

Nix پیگیری می‌کند که چه مواردی در کش‌های باینری موجود است تا مجبور نباشد در هر دستور آن‌ها را استعلام کند.
این شامل پاسخ‌های منفی نیز می‌شود؛ یعنی اگر یک مسیر انبار مشخص قابل جایگزینی (substitute) نباشد.

گزینه [`--narinfo-cache-negative-ttl`](/pages/nix-manual/command-ref/conf-file-prefix#conf-narinfo-cache-negative-ttl) را برای تنظیم مهلت زمانی کش بر حسب ثانیه پاس دهید.

## چگونه خطای زیر را برطرف کنیم: `error: querying path in database: database disk image is malformed`

این یک [مسئله شناخته‌شده](https://github.com/NixOS/nix/issues/1353) است.
این کار را امتحان کنید:

```shell-session
$ sqlite3 /nix/var/nix/db/db.sqlite "pragma integrity_check"
```

که خطاها را در [پایگاه‌داده](/pages/nix-manual/glossary#gloss-nix-database) چاپ خواهد کرد.
اگر خطاها به دلیل مراجع مفقود باشند، دستور زیر ممکن است کارساز باشد:

```shell-session
$ mv /nix/var/nix/db/db.sqlite /nix/var/nix/db/db.sqlite-bkp
$ sqlite3 /nix/var/nix/db/db.sqlite-bkp ".dump" | sqlite3 /nix/var/nix/db/db.sqlite
```

## نحوه رفع مشکل: `error: current Nix store schema is version 10, but I only support 7`

این یک [مسئله شناخته‌شده](https://github.com/NixOS/nix/issues/1251) است.

این بدان معناست که استفاده از نسخه جدیدتری از Nix، طرح‌واره (schema) اسلای‌کی‌وی [پایگاه‌داده](/pages/nix-manual/glossary#gloss-nix-database) را ارتقا داده است، و سپس شما تلاش کرده‌اید از نسخه قدیمی‌تری از Nix استفاده کنید.

راه‌حل این است که از پایگاه‌داده خروجی (dump) بگیرید و از نسخه قدیمی Nix برای وارد کردن مجدد داده‌ها استفاده کنید:

```shell-session
$ /path/to/nix/unstable/bin/nix-store --dump-db > /tmp/db.dump
$ mv /nix/var/nix/db /nix/var/nix/db.toonew
$ mkdir /nix/var/nix/db
$ nix-store --load-db < /tmp/db.dump
```

## نحوه رفع مشکل: `writing to file: Connection reset by peer`

این ممکن است به این معنا باشد که شما در حال تلاش برای درون‌ریزی یک فایل یا پوشه بیش از حد بزرگ به [انبار نیکس](/pages/nix-manual/glossary#gloss-store) هستید، یا اینکه ماشین شما با کمبود منابعی مانند فضای دیسک یا رم (memory) مواجه شده است.

تلاش کنید اندازه پوشه مورد نظر برای درون‌ریزی را کاهش دهید، یا [جمع‌آوری زباله (garbage collection)](/pages/nix-manual/command-ref/nix-collect-garbage) را اجرا کنید.

## به‌روزرسانی macOS نصب Nix را خراب می‌کند

این یک [مسئله شناخته‌شده](https://github.com/NixOS/nix/issues/3616) است.
[نصب‌کننده](/pages/nix-manual/installation/installing-binary) Nix فایل `/etc/zshrc` را تغییر می‌دهد.
هنگامی که macOS به‌روزرسانی می‌شود، معمولاً دوباره `/etc/zshrc` را بازنویسی می‌کند.

به عنوان یک راه‌حل موقت، قطعه‌کد زیر را به انتهای `/etc/zshrc` اضافه کرده و شل را مجدداً راه‌اندازی کنید:

```bash
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
```
