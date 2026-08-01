# گزینه‌ها

گزینه‌های زیر برای تمام عملیات‌های `nix-store` مجاز هستند، اما ممکن است همیشه تأثیری نداشته باشند.

- <span id="opt-add-root">[`--add-root`](#opt-add-root)</span> *path*

  باعث می‌شود نتیجه‌ی یک realization (`--realise` و `--force-realise`) به عنوان ریشه‌ی جمع‌کننده‌ی زباله ثبت شود. *path* به عنوان یک پیوند نمادین (symlink) به مسیر انبار حاصل ایجاد خواهد شد. علاوه بر این، یک پیوند نمادین با نامی منحصربه‌فرد به *path* در `/nix/var/nix/gcroots/auto/` ایجاد خواهد شد. برای نمونه،
```console
  $ nix-store --add-root /home/eelco/bla/result --realise ...

  $ ls -l /nix/var/nix/gcroots/auto
  lrwxrwxrwx    1 ... 2005-03-13 21:10 dn54lcypm8f8... -> /home/eelco/bla/result

  $ ls -l /home/eelco/bla/result
  lrwxrwxrwx    1 ... 2005-03-13 21:10 /home/eelco/bla/result -> /nix/store/1r11343n6qd4...-f-spot-0.0.10
  ```

بنابراین، هنگامی که `/home/eelco/bla/result` حذف می‌شود، ریشه جمع‌آوری زباله (garbage collection) در پوشه `auto` به یک پیوند نمادین (symlink) معلق تبدیل شده و توسط جمع‌کننده‌ی زباله (garbage collector) نادیده گرفته خواهد شد.

> **هشدار**
>
> توجه داشته باشید که جابه‌جا کردن یا تغییر نام ریشه‌های جمع‌آوری زباله (garbage collection) امکان‌پذیر نیست، زیرا پیوند نمادین (symlink) موجود در پوشه `auto` همچنان به مکان قبلی اشاره خواهد کرد.

اگر نتایج متعددی وجود داشته باشد، با شماره‌گذاری ترتیبی پیوندهای نمادین (symlink) فراتر از مورد اول، چندین پیوند نمادین (symlink) ایجاد خواهد شد (به عنوان مثال، `foo`، `foo-2`، `foo-3` و غیره).

