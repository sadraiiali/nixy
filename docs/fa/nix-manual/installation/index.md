# نصب

این بخش نحوه نصب و پیکربندی Nix را برای استفاده‌ی بار اول شرح می‌دهد.

گزینه‌ی توصیه‌شده‌ی فعلی روی لینوکس و macOS، روش [چندکاربره](#multi-user) است.

## چندکاربره

این نصب اشتراک‌گذاری بهتر، ایزوله‌سازی بهبودیافته و امنیت بیشتری را نسبت به نصب تک‌کاربره ارائه می‌دهد.

این گزینه مستلزم یکی از موارد زیر است:

* لینوکس در حال اجرای systemd، با SELinux غیرفعال
* macOS

> **به‌روزرسانی به macOS 15 Sequoia**
>
> اگر اخیراً به macOS 15 Sequoia به‌روزرسانی کرده‌اید و در حال دریافت
```console
> error: the user '_nixbld1' in the group 'nixbld' does not exist
> ```
> هنگام اجرای دستورهای Nix، برای اطلاع از دستورالعمل‌های رفع مشکل نصب خود بدون نیاز به نصب مجدد، به مسئله‌ی گیت‌هاب [NixOS/nix#10892](https://github.com/NixOS/nix/issues/10892) مراجعه کنید.

```console
$ curl -L https://nixos.org/nix/install | sh -s -- --daemon
```

## تک‌کاربره

> حالت تک‌کاربره روی Mac پشتیبانی نمی‌شود.

> `warning: installing Nix as root is not supported by this script!`

این نصب نیازمندی‌های کمتری نسبت به نصب چندکاربره دارد، با این حال نمی‌تواند اشتراک‌گذاری، ایزوله‌سازی یا امنیت معادل را ارائه دهد.

این گزینه برای سیستم‌های بدون systemd مناسب است.

```console
$ curl -L https://nixos.org/nix/install | sh -s -- --no-daemon
```

## توزیع‌ها

جامعه‌ی کاربری Nix نصب‌کننده‌هایی را برای چندین توزیع نگهداری می‌کند.

آن‌ها را می‌توانید در مخزن [`nix-community/nix-installers`](https://github.com/nix-community/nix-installers) پیدا کنید.
