(reproducible-scripts)=

# اسکریپت‌های تفسیری بازتولیدپذیر

در این آموزش، شما یاد خواهید گرفت که چگونه از Nix برای ایجاد و اجرای اسکریپت‌های تفسیری بازتولیدپذیر، که به عنوان اسکریپت‌های [shebang] نیز شناخته می‌شوند، استفاده کنید.

## الزامات

- یک {ref}`نصب Nix <install-nix>` فعال
- آشنایی با [Bash]

## یک اسکریپت ساده با وابستگی‌های غیربدیهی

اسکریپت زیر را در نظر بگیرید که محتوای XML یک URL را دریافت کرده، آن را به JSON تبدیل می‌کند و برای خوانایی بهتر قالب‌بندی می‌کند:

```bash
#! /bin/bash

curl https://github.com/NixOS/nixpkgs/releases.atom | xml2json | jq .
```

این برنامه به برنامه‌های `curl`، `xml2json` و `jq` نیاز دارد.
همچنین به مفسر `bash` نیاز دارد.
اگر هر یک از این وابستگی‌ها روی سیستمی که اسکریپت را اجرا می‌کند موجود نباشد، اسکریپت به‌صورت جزئی یا کلی با خطا مواجه خواهد شد.

با استفاده از Nix، می‌توانیم تمام وابستگی‌ها را به‌صورت صریح اعلام کنیم و اسکریپتی تولید کنیم که همیشه روی هر ماشینی که از Nix و بسته‌های مورد نیاز گرفته‌شده از Nixpkgs پشتیبانی می‌کند، اجرا شود.

## اسکریپت

خط [shebang] تعیین می‌کند که از چه برنامه‌ای برای اجرای یک اسکریپت تفسیری استفاده شود.

[Bash]: https://www.gnu.org/software/bash/
[shebang]: https://en.wikipedia.org/wiki/Shebang_(Unix)

ما از خط shebang به شکل `#!/usr/bin/env nix-shell` استفاده خواهیم کرد.

[`env`] برنامه‌ای است که در اکثر سیستم‌عامل‌های مدرن یونیکس‌مانند در مسیر سیستم‌فایلی `/usr/bin/env` در دسترس است.
این برنامه نام یک دستور را به عنوان آرگومان می‌گیرد و اولین فایل اجرایی با آن نام را که در پوشه‌های فهرست‌شده در متغیر محیطی `$PATH` پیدا کند، اجرا خواهد کرد.

[`env`]: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/env.html

ما از [`nix-shell` as a shebang interpreter] استفاده می‌کنیم.
این ابزار پارامترهای زیر را که برای مورد استفادهٔ ما مرتبط هستند می‌پذیرد:

- `-i` مشخص می‌کند که برای تفسیر بقیهٔ فایل از چه برنامه‌ای استفاده شود
- `--pure` بیشتر متغیرهای محیطی را هنگام اجرای اسکریپت حذف می‌کند
- `-p` بسته‌هایی را که باید در محیط مفسر حضور داشته باشند فهرست می‌کند
- `-I` [مسیر جستجوی ارجاع (ref-search-path)] را برای بسته‌ها به‌صورت صریح تنظیم می‌کند

جزئیات بیشتر دربارهٔ گزینه‌ها را می‌توانید در [مستندات مرجع `nix-shell`](/pages/nix-manual/command-ref/nix-shell#options) بیابید.

[`nix-shell` as a shebang interpreter]: /pages/nix-manual/command-ref/nix-shell#use-as-a--interpreter
[the search path]: /pages/nix-manual/command-ref/opt-common#opt-I

فایلی به نام `nixpkgs-releases.sh` با محتوای زیر ایجاد کنید:

```shell
#!/usr/bin/env nix-shell
#! nix-shell -i bash --pure
#! nix-shell -p bash cacert curl jq python3Packages.xmljson
#! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/2a601aafdc5605a5133a2ca506a34a3a73377247.tar.gz

curl https://github.com/NixOS/nixpkgs/releases.atom | xml2json | jq .
```

اولین خط یک shebang استاندارد است.
خطوط shebang اضافی یک ساختار مخصوص Nix هستند:

- با گزینه `-i`، برنامهٔ `bash` به عنوان مفسر برای بقیه فایل مشخص می‌شود.

- در این حالت، گزینهٔ `--pure` فعال می‌شود تا از استفادهٔ ضمنی اسکریپت از برنامه‌هایی که ممکن است از پیش روی سیستمی که اسکریپت روی آن اجرا می‌شود وجود داشته باشند، جلوگیری کند.

- گزینهٔ `-p` بسته‌های مورد نیاز برای اجرای اسکریپت را فهرست می‌کند.

 دستور `xml2json` توسط بستهٔ `python3Packages.xmljson` فراهم می‌شود، در حالی که `bash`، `jq` و `curl` توسط بسته‌هایی با همین نام فراهم می‌شوند.
بستهٔ `cacert` باید حضور داشته باشد تا احراز هویت SSL کار کند.

 :::{tip}
 برای پیدا کردن بسته‌هایی که برنامهٔ مورد نیاز شما را فراهم می‌کنند، از [search.nixos.org](https://search.nixos.org/packages) استفاده کنید.
 :::

- پارامتر `-I` به یک کامیت مشخص از Git در مخزن Nixpkgs اشاره دارد.

 این کار تضمین می‌کند که اسکریپت همیشه و در همه جا با دقیقاً نسخه‌های یکسانی از بسته‌ها اجرا خواهد شد.

اسکریپت را قابل اجرا کنید:
```console
 chmod +x nixpkgs-releases.sh
 ```

اجرای اسکریپت:

```console
./nixpkgs-releases.sh
```

## گام‌های نخستین

- {ref}`reading-nix-language` برای کسب اطلاعات دربارهٔ زبان Nix که برای اعلام بسته‌ها و پیکربندی‌ها استفاده می‌شود.
- {ref}`declarative-reproducible-envs` برای ایجاد محیط‌های شل بازتولیدپذیر با یک فایل پیکربندی اعلانی (declarative).
- [جمع‌آوری زباله (garbage collection)](/pages/nix-manual/package-management/garbage-collection) آزادسازی فضای ذخیره‌سازی اشغال‌شده توسط برنامه‌های ارائه‌شده از طریق Nix
