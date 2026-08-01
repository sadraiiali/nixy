# نام

دستور `nix-store --serve` - ارائه انبار Nix محلی از طریق SSH

# خلاصه

دستور `nix-store` `--serve` [`--write`]

# توضیحات

عملکرد `--serve` دسترسی به انبار Nix را از طریق استاندارد ورودی (stdin) و استاندارد خروجی (stdout) فراهم می‌کند و به این منظور طراحی شده‌است که دسترسی به انبار Nix را برای یک کاربر محدود SSH فراهم کند.

پرچم‌های زیر در دسترس هستند:

- `--write`

  به کاربر متصل اجازه می‌دهد تا درخواست اشتقاق ساخت (realization of derivations) را بدهد. در عمل، از این قابلیت می‌توان برای وادار کردن هاست به عمل به عنوان یک سازنده راه دور استفاده کرد.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

برای تبدیل یک هاست به یک سرور ساخت، می‌توان از فایل `authorized_keys` برای اعطای دسترسی ساخت به یک کلید عمومی SSH خاص استفاده کرد:

```console
$ cat <<EOF >>/root/.ssh/authorized_keys
command="nice -n20 nix-store --serve --write" ssh-rsa AAAAB3NzaC1yc2EAAAA...
EOF
```

