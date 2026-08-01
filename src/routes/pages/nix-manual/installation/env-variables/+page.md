# 3.6. متغیرهای محیطی

برای استفاده از Nix، باید برخی از متغیرهای محیطی تنظیم شوند. به‌طور خاص، متغیر `PATH` باید شامل پوشه‌های `prefix/bin` و `~/.nix-profile/bin` باشد. پوشهٔ اول حاوی خود ابزارهای Nix است، در حالی که `~/.nix-profile` یک پیوند نمادین (symlink) به *محیط کاربر* فعلی (یک بستهٔ خودکار تولیدشده متشکل از پیوندهای نمادین به بسته‌های نصب‌شده) است. ساده‌ترین راه برای تنظیم متغیرهای محیطی مورد نیاز، گنجاندن فایل `prefix/etc/profile.d/nix.sh` در فایل `~/.profile` (یا موارد مشابه) است، مانند این:

```bash
source prefix/etc/profile.d/nix.sh
```

# `NIX_SSL_CERT_FILE`

اگر لازم است برای پشتیبانی از یک پروکسی مرد میانی با قابلیت رهگیری HTTPS، یک مجموعه گواهی (certificate bundle) سفارشی مشخص کنید، باید مسیر مجموعه گواهی را در متغیر محیطی `NIX_SSL_CERT_FILE` تعیین کنید.

اگر متغیر `NIX_SSL_CERT_FILE` را به صورت دستی مشخص نکنید، Nix مجموعه گواهی اختصاصی خود را نصب و استفاده خواهد کرد.

متغیر محیطی را تنظیم کرده و Nix را نصب کنید

```shell
$ export NIX_SSL_CERT_FILE=/etc/ssl/my-certificate-bundle.crt
$ curl -L https://nixos.org/nix/install | sh
```

در فایل‌های پروفایل و rc شل (به عنوان مثال، `/etc/bashrc`، `/etc/zshrc`)، خط زیر را اضافه کنید:

```bash
export NIX_SSL_CERT_FILE=/etc/ssl/my-certificate-bundle.crt
```

> **نکته**
>
> نباید ابتدا دستور export را اجرا کرده و سپس نصب را انجام دهید، زیرا نصب‌کننده Nix حضور پیکربندی Nix را تشخیص داده و متوقف خواهد شد.

اگر از daemon استفاده می‌کنید، باید موارد زیر را نیز به `/etc/nix/nix.conf` اضافه کنید:

```
ssl-cert-file = /etc/ssl/my-certificate-bundle.crt
```

## متغیرهای محیطی پروکسی

نصب‌کننده Nix دارای پردازش ویژه‌ای برای این متغیرهای محیطی مربوط به پروکسی است: `http_proxy`, `https_proxy`, `ftp_proxy`, `all_proxy`, `no_proxy`, `HTTP_PROXY`, `HTTPS_PROXY`, `FTP_PROXY`, `ALL_PROXY`, `NO_PROXY`.

اگر هر یک از این متغیرها هنگام اجرای نصب‌کننده Nix تنظیم شده باشند، نصب‌کننده یک فایل بازنویسی در مسیر `/etc/systemd/system/nix-daemon.service.d/override.conf` ایجاد خواهد کرد تا `nix-daemon` از آن‌ها استفاده کند.
