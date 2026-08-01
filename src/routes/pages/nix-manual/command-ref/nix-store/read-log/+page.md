# 8.3.3.14. nix-store --read-log

## نام

`nix-store --read-log` - چاپ گزارش ساخت (build log)

## خلاصه دستور
`nix-store` {'{'}'{'{'}'{'}'}`--read-log` | `-l`{'{'}'{'}'}'{'}'} *paths…*

## توصیف
عملیات `--read-log` گزارش ساخت مسیرهای انبار مشخص‌شده را روی خروجی استاندارد چاپ می‌کند. گزارش ساخت هر چیزی است که سازندهٔ یک derivation روی خروجی استاندارد و خطای استاندارد نوشته است. اگر یک مسیر انبار یک derivation نباشد، سازنده‌ی آن مسیر انبار مورد استفاده قرار می‌گیرد.

گزارش‌های ساخت در `/nix/var/log/nix/drvs` نگهداری می‌شوند. با این حال، هیچ تضمینی وجود ندارد که گزارش ساخت برای هر مسیر انبار خاصی در دسترس باشد. برای مثال، اگر مسیر به عنوان یک باینری پیش‌ساخته از طریق یک جایگزین (substitute) بارگیری شده باشد، گزارش آن در دسترس نخواهد بود.

## مثال
```shell
$ nix-store --read-log $(which ktorrent)
building /nix/store/dhc73pvzpnzxhdgpimsd9sw39di66ph1-ktorrent-2.2.1
unpacking sources
unpacking source archive /nix/store/p8n1jpqs27mgkjw07pb5269717nzf5f8-ktorrent-2.2.1.tar.gz
ktorrent-2.2.1/
ktorrent-2.2.1/NEWS
...
```
