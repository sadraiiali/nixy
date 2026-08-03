# 8.3.3.3. nix-store --delete

## نام

`nix-store --delete` - حذف مسیرهای انبار

## خلاصه دستور

```text
nix-store --delete [--ignore-liveness] paths…
```

## توضیحات
عملکرد `--delete` مسیرهای انبار *paths* را از انبار Nix حذف می‌کند، اما تنها در صورتی که انجام این کار امن باشد؛ یعنی زمانی که مسیر از طریق هیچ‌یک از ریشه‌های جمع‌کننده‌ی زباله قابل دسترسی نباشد. این بدان معناست که شما تنها می‌توانید مسیرهایی را حذف کنید که توسط `nix-store --gc` نیز حذف می‌شوند. بنابراین، `--delete` نسخه هدایت‌شده‌تری از `--gc` است.

با گزینه `--ignore-liveness`، قابلیت دسترسی از ریشه‌ها نادیده گرفته می‌شود. با این حال، اگر مسیرهای دیگری در انبار وجود داشته باشند که به آن ارجاع دهند (یعنی به آن وابسته باشند)، آن مسیر همچنان حذف نخواهد شد.

## مثال
```shell
$ nix-store --delete /nix/store/gjak3al7lj61x4gj6rln4f5pc5v0f67n-mesa-6.4
0 bytes freed (0.00 MiB)
error: cannot delete path `/nix/store/gjak3al7lj61x4gj6rln4f5pc5v0f67n-mesa-6.4' since it is still alive
```
