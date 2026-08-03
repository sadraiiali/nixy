# 8.3.4.5. nix-env --rollback

## نام

`nix-env --rollback` - تنظیم پروفایل کاربر روی نسل قبلی

## خلاصه دستور

```text
nix-env --rollback
```

## توضیحات
این عملیات به نسل «قبلی» پروفایل فعال، یعنی بالاترین شماره‌ی نسلِ کوچک‌تر از نسل فعلی (در صورت وجود) سوییچ می‌کند. این دستور صرفاً یک پوشش (wrapper) کاربردی و راحت دورِ `--list-generations` و `--switch-generation` است.

## مثال‌ها
```shell
$ nix-env --rollback
switching from generation 92 to 91
```

```shell
$ nix-env --rollback
error: no generation older than the current (91) exists
```
