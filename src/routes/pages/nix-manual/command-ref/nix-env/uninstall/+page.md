# 8.3.4.10. nix-env --uninstall

## نام

`nix-env --uninstall` - حذف بسته‌ها از پروفایل کاربر

## خلاصه

```text
nix-env {--uninstall | -e} drvnames…
```

## توضیحات
عملیات حذف (uninstall)، یک پروفایل کاربر جدید بر اساس نسل فعلی پروفایل فعال ایجاد می‌کند که در آن، مسیرهای انبار (store paths) مشخص‌شده توسط نام‌های نمادین *drvnames* حذف می‌شوند.

## مثال‌ها
```shell
$ nix-env --uninstall gcc
$ nix-env --uninstall '.*' (remove everything)
```
