# 8.3.4.7. nix-env --set

## نام

`nix-env --set` - تنظیم پروفایل برای شامل شدن یک derivation مشخص

## خلاصه

`nix-env` `--set` *drvname*

## توصیف

عملیات `--set` نسل فعلی یک پروفایل را تغییر می‌دهد تا دقیقاً شامل derivation مشخص‌شده باشد و هیچ چیز دیگری در آن نباشد.

## مثال‌ها

مورد زیر پروفایلی را به‌روزرسانی می‌کند تا نسل فعلی آن فقط شامل Firefox باشد:

```shell
$ nix-env --profile /nix/var/nix/profiles/browser --set firefox
```
