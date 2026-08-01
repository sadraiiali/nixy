# 8.6.3. کانال‌ها

## کانال‌ها

پوشه‌ای حاوی پیوندهای نمادین (symlinks) به کانال‌های Nix که توسط [`nix-channel`] مدیریت می‌شود:

- مسیر `$XDG_STATE_HOME/nix/profiles/channels` برای کاربران عادی
- مسیر `$NIX_STATE_DIR/profiles/per-user/root/channels` برای کاربر `root`

ابزار [`nix-channel`] برای ذخیره کانال‌ها از یک [پروفایل](/pages/nix-manual/command-ref/files/profiles) استفاده می‌کند.
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

[`nix-channel`]: /pages/nix-manual/command-ref/nix-channel
[`use-xdg-base-directories`]: /pages/nix-manual/command-ref/conf-file#conf-use-xdg-base-directories
