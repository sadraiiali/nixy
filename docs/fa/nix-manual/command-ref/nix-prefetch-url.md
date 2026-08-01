# نام

`nix-prefetch-url` - کپی کردن یک فایل از یک URL به انبار و چاپ هش آن

# خلاصه دستور

`nix-prefetch-url` *url* [*hash*]
  [`--type` *hashAlgo*]
  [`--print-path`]
  [`--unpack`]
  [`--name` *name*]

# توضیحات

دستور `nix-prefetch-url` فایل ارجاع‌داده‌شده توسط URL یعنی *url* را بارگیری می‌کند، هش رمزنگاری‌شده آن را چاپ می‌کند و آن را در انبار Nix کپی می‌کند.
نام فایل در انبار به صورت `hash-baseName` است که در آن *baseName* تمام بخش‌هایی است که پس از آخرین اسلش در *url* می‌آید.

این دستور صرفاً برای راحتی نویسندگان عبارت‌های Nix فراهم شده‌است. اغلب، یک عبارت Nix برخی از توزیع‌های سورس را از شبکه با استفاده از عبارت `fetchurl` موجود در Nixpkgs دریافت می‌کند. با این حال، `fetchurl` نیازمند یک هش رمزنگاری‌شده‌است. اگر هش را نمی‌دانید، باید ابتدا فایل را بارگیری کنید، و سپس هنگام ساخت عبارت Nix خود، `fetchurl` دوباره آن را بارگیری خواهد کرد. از آنجا که `fetchurl` از همان نام فایل بارگیری‌شده‌ی `nix-prefetch-url` استفاده می‌کند، می‌توان از بارگیری تکراری جلوگیری کرد.

اگر *hash* مشخص شود، در صورتی که انبار Nix از پیش حاوی فایلی با همان هش و نام پایه باشد، بارگیری انجام نمی‌شود.
در غیر این صورت، فایل بارگیری می‌شود و اگر هش واقعی فایل با هش مشخص‌شده مطابقت نداشته باشد، خطایی اعلام می‌شود.

این دستور هش را روی خروجی استاندارد چاپ می‌کند.
هش با استفاده از [Nix32](@docroot@/protocols/nix32.md) چاپ می‌شود، مگر اینکه `--type md5` مشخص شده باشد؛
در این صورت با استفاده از base-16 چاپ می‌شود.
علاوه بر این، اگر از گزینه `--print-path` استفاده شود،
مسیر فایل بارگیری‌شده در انبار Nix نیز چاپ خواهد شد.

# گزینه‌ها

- `--type` *hashAlgo*

  از الگوریتم هش رمزنگاری‌شده‌ی مشخص‌شده استفاده کنید،
  که می‌تواند یکی از موارد `blake3`، `md5`، `sha1`، `sha256` و `sha512` باشد.
  پیش‌فرض `sha256` است.

- `--print-path`

  مسیر انبار فایل بارگیری‌شده را روی خروجی استاندارد چاپ کنید.

- `--unpack`

  بایگانی را استخراج کنید (که باید یک تاربال یا فایل زیپ باشد) و نتیجه را به انبار Nix اضافه کنید. هش حاصل را می‌توان با توابعی مانند `fetchzip` یا `fetchFromGitHub` متعلق به Nixpkgs استفاده کرد.

- `--executable`

  بیت اجرایی را روی فایل بارگیری‌شده تنظیم کنید.

- `--name` *name*

  نام فایل را در انبار Nix بازنویسی کنید. به‌طور پیش‌فرض، این نام `hash-basename` است که در آن *basename* آخرین مؤلفه‌ی *url* است.
  بازنویسی نام زمانی ضروری است که *basename* شامل کاراکترهایی باشد که در مسیرهای انبار Nix مجاز نیستند.

# مثال‌ها

```console
$ nix-prefetch-url ftp://ftp.gnu.org/pub/gnu/hello/hello-2.10.tar.gz
0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i
```

```console
$ nix-prefetch-url --print-path mirror://gnu/hello/hello-2.10.tar.gz
0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i
/nix/store/8alrpdaasjd1x6g1fczchmzbpqm936a3-hello-2.10.tar.gz
```

```console
$ nix-prefetch-url --unpack --print-path https://github.com/NixOS/patchelf/archive/0.8.tar.gz
079agjlv0hrv7fxnx9ngipx14gyncbkllxrp9cccnh3a50fxcmy7
/nix/store/19zrmhm3m40xxaw81c8cqm6aljgrnwj2-0.8.tar.gz
```
