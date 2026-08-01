# <a id="sec-prefer-remote-fetch"></a> اورلی prefer-remote-fetch

`prefer-remote-fetch` یک اورلی است که کدهای منبع را روی یک سازنده راه دور بارگیری می‌کند. این ویژگی زمانی مفید است که ماشین ارزیابی‌کننده سرعت آپلود پایینی دارد، در حالی که سازنده می‌تواند کدهای منبع را سریع‌تر و به‌طور مستقیم دریافت کند. برای استفاده از آن، قطعه‌کد زیر را به عنوان یک اورلی جدید قرار دهید:

```nix
self: super: (super.prefer-remote-fetch self super)
```

یک نمونه پیکربندی کامل که اورلی را برای حساب کاربری خودتان تنظیم می‌کند می‌تواند به این صورت باشد

```ShellSession
$ mkdir ~/.config/nixpkgs/overlays/
$ cat > ~/.config/nixpkgs/overlays/prefer-remote-fetch.nix <<EOF
  self: super: super.prefer-remote-fetch self super
EOF
```
