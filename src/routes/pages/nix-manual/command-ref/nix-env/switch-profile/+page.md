# 8.3.4.9. nix-env --switch-profile

## Name

`nix-env --switch-profile` - تنظیم پروفایل کاربر روی پروفایل مشخص‌شده

## Synopsis

```text
nix-env {--switch-profile | -S} path
```

## Description
این عملیات، *path* را به عنوان پروفایل فعلی کاربر تنظیم می‌کند. یعنی، پیوند نمادین `~/.nix-profile` به گونه‌ای تنظیم می‌شود که به *path* اشاره کند.

## Examples
```shell
$ nix-env --switch-profile ~/my-profile
```
