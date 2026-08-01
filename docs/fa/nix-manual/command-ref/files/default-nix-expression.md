## عبارت Nix پیش‌فرض

سورسِ [عبارت‌های نیکس (Nix expression)](@docroot@/glossary.md#gloss-nix-expression) که به طور پیش‌فرض توسط [`nix-env`] استفاده می‌شود:

- `~/.nix-defexpr`
- `$XDG_STATE_HOME/nix/defexpr` اگر [`use-xdg-base-directories`] روی مقدار `true` تنظیم شده باشد.

بارگذاری آن به صورت زیر انجام می‌شود:

- اگر عبارت پیش‌فرض یک فایل باشد، به عنوان یک عبارت Nix بارگذاری می‌شود.
- اگر عبارت پیش‌فرض یک پوشه حاوی یک فایل `default.nix` باشد، آن فایل `default.nix` به عنوان یک عبارت Nix بارگذاری می‌شود.
- اگر عبارت پیش‌فرض پوشه‌ای بدون فایل `default.nix` باشد، محتویات آن (هم فایل‌ها و هم زیرماژول‌ها/زیرپوشه‌ها) به عنوان عبارت‌های Nix بارگذاری می‌شوند.
  این عبارت‌ها در یک مجموعه ویژگی واحد ترکیب می‌شوند که هر عبارت تحت صفتی با همان نام فایل یا زیرپوشه اصلی قرار می‌گیرد.
  زیرپوشه‌های بدون فایل `default.nix` برای جستجوی عبارت‌های Nix بیشتر به صورت بازگشتی پیمایش می‌شوند، اما نام این پوشه‌های میانی به مسیرهای صفت عبارت Nix پیش‌فرض اضافه نمی‌شود.

سپس، عبارت حاصل به این صورت تفسیر می‌شود:

- اگر عبارت یک مجموعه ویژگی باشد، به عنوان عبارت Nix پیش‌فرض استفاده می‌شود.
- اگر عبارت یک تابع باشد، یک مجموعه خالی به عنوان آرگومان به آن ارسال می‌شود و مقدار بازگشتی به عنوان عبارت Nix پیش‌فرض استفاده می‌شود.

> **مثال**
>
> اگر عبارت پیش‌فرض شامل دو فایل `foo.nix` و `bar.nix` باشد، آنگاه عبارت Nix پیش‌فرض معادل خواهد بود با
>
```nix
> {
>   foo = import ~/.nix-defexpr/foo.nix;
>   bar = import ~/.nix-defexpr/bar.nix;
> }
> ```

فایل [`manifest.nix`](@docroot@/command-ref/files/manifest.nix.md) همیشه نادیده گرفته می‌شود.

دستور [`nix-channel`] یک پیوند نمادین (symlink) به [channels] کاربر فعلی در این پوشه قرار می‌دهد که همان [لینک کانال کاربر](#user-channel-link) است.
این کار باعث می‌شود تمام کانال‌های مشترک‌شده به عنوان صفت (attribute) در عبارت پیش‌فرض در دسترس باشند.

## لینک کانال کاربر

یک پیوند نمادین (symlink) که تضمین می‌کند [`nix-env`] می‌تواند [channels] کاربر فعلی را پیدا کند:

- `~/.nix-defexpr/channels`
- `$XDG_STATE_HOME/nix/defexpr/channels` اگر [`use-xdg-base-directories`] روی `true` تنظیم شده باشد.

این پیوند نمادین (symlink) به مسیرهای زیر اشاره می‌کند:

- `$XDG_STATE_HOME/nix/profiles/channels` برای کاربران معمولی
- `$NIX_STATE_DIR/profiles/per-user/root/channels` برای کاربر `root`

در یک نصب چندکاربره، ممکن است `~/.nix-defexpr/channels_root` را نیز داشته باشید که به کانال‌های کاربر root متصل می‌شود.

[`nix-channel`]: @docroot@/command-ref/nix-channel.md
[`nix-env`]: @docroot@/command-ref/nix-env.md
[`use-xdg-base-directories`]: @docroot@/command-ref/conf-file.md#conf-use-xdg-base-directories
[channels]: @docroot@/command-ref/files/channels.md
