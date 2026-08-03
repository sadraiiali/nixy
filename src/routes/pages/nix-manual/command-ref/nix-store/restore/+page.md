# 8.3.3.17. nix-store --restore

## نام

دستور `nix-store --restore` - استخراج یک آرشیو نیکس

## خلاصه‌دستور

```text
nix-store --restore path
```

## توضیحات

عملیات `--restore` یک [آرشیو نیکس (NAR)][Nix Archive] را در *path* استخراج می‌کند، که مسیر مورد نظر نباید از‌پیش‌موجود باشد. آرشیو از ورودی استاندارد خوانده می‌شود.

[Nix Archive]: /pages/nix-manual/store/file-system-object/content-address#serial-nix-archive
