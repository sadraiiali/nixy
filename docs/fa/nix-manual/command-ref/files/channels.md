## کانال‌ها

پوشه‌ای حاوی پیوندهای نمادین (symlinks) به کانال‌های Nix که توسط [`nix-channel`] مدیریت می‌شود:

- مسیر `$XDG_STATE_HOME/nix/profiles/channels` برای کاربران عادی
- مسیر `$NIX_STATE_DIR/profiles/per-user/root/channels` برای کاربر `root`

ابزار [`nix-channel`] برای ذخیره کانال‌ها از یک [پروفایل](@docroot@/command-ref/files/profiles.md) استفاده می‌کند.
این پروفایل شامل پیوندهای نمادین به محتویات آن کانال‌ها است.

## کانال‌های مشترک‌ شده

فهرست کانال‌های مشترک‌شده در مسیرهای زیر ذخیره می‌شود:

- `~/.nix-channels`
- مسیر `$XDG_STATE_HOME/nix/channels` اگر گزینه [`use-xdg-base-directories`] روی `true` تنظیم شده باشد

با فرمت زیر:

```
<url> <name>
...
```

[`nix-channel`]: @docroot@/command-ref/nix-channel.md
[`use-xdg-base-directories`]: @docroot@/command-ref/conf-file.md#conf-use-xdg-base-directories
