# 8.4.5. nix-hash

## نام

`nix-hash` - محاسبه هش رمزنگاری‌شده یک مسیر

## خلاصه
`nix-hash` [`--flat`] [`--base32`] [`--truncate`] [`--type` *hashAlgo*] *path…*

`nix-hash` [`--to-base16`|`--to-base32`|`--to-base64`|`--to-sri`] [`--type` *hashAlgo*] *hash…*

## توضیحات
دستور `nix-hash` هش رمزنگاری‌شده‌ی محتویات هر *path* را محاسبه کرده و آن را در خروجی استاندارد چاپ می‌کند. به‌طور پیش‌فرض، این دستور یک هش MD5 محاسبه می‌کند، اما سایر الگوریتم‌های هش نیز در دسترس هستند. هش محاسبه‌شده به صورت مبنای شانزده (هگزادسیمال) چاپ می‌شود. برای تولید هشی مشابه `nix-prefetch-url` باید چندین آرگومان را مشخص کنید، برای مشاهده‌ی یک مثال به بخش زیر مراجعه کنید.

هش روی یک *سری‌سازی* (serialisation) از هر مسیر محاسبه می‌شود: یک دامپ (dump) از درخت سیستم‌فایل که ریشه‌ی آن همان مسیر است. این امر به دایرکتوری‌ها و پیوندهای نمادین اجازه می‌دهد تا مانند فایل‌های معمولی هش شوند. این دامپ در قالب *[آرشیو نیکس (NAR)][Nix Archive]* است که توسط [`nix-store --dump`](/pages/nix-manual/command-ref/nix-store/dump) تولید می‌شود. بنابراین، `nix-hash path` همان هش رمزنگاری‌شده‌ای را نتیجه می‌دهد که دستور `nix-store --dump path | md5sum` تولید می‌کند.

[Nix Archive]: /pages/nix-manual/store/file-system-object/content-address#serial-nix-archive
## گزینه‌ها
- `--flat`

  چاپ هش رمزنگاری‌شده‌ی محتویات هر *path* فایل معمولی.
  به این معنا که به‌جای محاسبه‌ی هش [آرشیو نیکس (NAR)](/pages/nix-manual/store/file-system-object/content-address#serial-nix-archive) مربوط به *path*،
  صرفاً *path* را به‌همان شکلی که هست، [به‌طور مستقیم هش کن](/pages/nix-manual/store/file-system-object/content-address#serial-flat).
  این کار مستلزم آن است که *path* به‌جای دایرکتوری، به یک فایل معمولی ارجاع یابد.
  نتیجه با خروجی تولیدشده توسط دستورات گنو یعنی `md5sum` و `sha1sum` یکسان است.

- `--base16`

  چاپ هش در قالب نمایش هگزادسیمال (پیش‌فرض).

- `--base32`

  چاپ هش در قالب نمایش [Nix32](/pages/nix-manual/protocols/nix32) به‌جای هگزادسیمال.
  این قالب فشرده‌تر است و می‌توان آن را در عبارت‌های Nix (مانند فراخوانی‌های `fetchurl`) استفاده کرد.

- `--base64`

  مشابه `--base32`، اما چاپ هش در قالب نمایش [Base64](https://en.wikipedia.org/wiki/Base64) که نسبت به قالب Nix32 فشرده‌تر است.

- `--sri`

  چاپ هش در قالب [SRI](/pages/nix-manual/glossary#gloss-sri) با کدگذاری Base64.
  نوع الگوریتم هش در ابتدای رشته‌ی هش قرار می‌گیرد،
  و پس از آن یک خط تیره (-) و سپس بدنه‌ی هش Base64 می‌آید.

- `--truncate`

  کوتاه‌کردن هش‌های طولانی‌تر از ۱۶۰ بیت (مانند SHA-256) به ۱۶۰ بیت.

- `--type` *hashAlgo*

  استفاده از الگوریتم هش رمزنگاری‌شده‌ی مشخص‌شده که می‌تواند یکی از موارد `blake3`، `md5`، `sha1`، `sha256` و `sha512` باشد.

- `--to-base16`

  هیچ چیزی را هش نکن، بلکه نمایش هش [Nix32](/pages/nix-manual/protocols/nix32) یعنی *hash* را به هگزادسیمال تبدیل کن.

- `--to-base32`

  هیچ چیزی را هش نکن، بلکه نمایش هش هگزادسیمال یعنی *hash* را به [Nix32](/pages/nix-manual/protocols/nix32) تبدیل کن.

- `--to-base64`

  هیچ چیزی را هش نکن، بلکه نمایش هش هگزادسیمال یعنی *hash* را به Base64 تبدیل کن.

- `--to-sri`

  هیچ چیزی را هش نکن، بلکه نمایش هش هگزادسیمال یعنی *hash* را به SRI تبدیل کن.

## مثال‌ها
محاسبه‌ی هشی مشابه دستور `nix-prefetch-url`:

```shell
$ nix-prefetch-url file://<(echo test)
1lkgqb6fclns49861dwk9rzb6xnfkxbpws74mxnx01z9qyv1pjpj
$ nix-hash --type sha256 --flat --base32 <(echo test)
1lkgqb6fclns49861dwk9rzb6xnfkxbpws74mxnx01z9qyv1pjpj
```

محاسبه‌ی هش‌ها:

```shell
$ mkdir test
$ echo "hello" > test/world

$ nix-hash test/ (MD5 hash; default)
8179d3caeff1869b5ba1744e5a245c04

$ nix-store --dump test/ | md5sum (for comparison)
8179d3caeff1869b5ba1744e5a245c04  -

$ nix-hash --type sha1 test/
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6

$ nix-hash --type sha1 --base16 test/
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6

$ nix-hash --type sha1 --base32 test/
nvd61k9nalji1zl9rrdfmsmvyyjqpzg4

$ nix-hash --type sha1 --base64 test/
5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --type sha1 --sri test/
sha1-5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --type sha256 --flat test/
error: reading file `test/': Is a directory

$ nix-hash --type sha256 --flat test/world
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03
```

تبدیل بین هگزادسیمال، Nix32، Base64 و SRI:

```shell
$ nix-hash --type sha1 --to-base32 e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6
nvd61k9nalji1zl9rrdfmsmvyyjqpzg4

$ nix-hash --type sha1 --to-base16 nvd61k9nalji1zl9rrdfmsmvyyjqpzg4
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6

$ nix-hash --type sha1 --to-base64 e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6
5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --type sha1 --to-sri nvd61k9nalji1zl9rrdfmsmvyyjqpzg4
sha1-5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --to-base16 sha1-5P2Lpfe76upazon+ECVVNs1g2rY=
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6
```
