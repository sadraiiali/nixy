# 8.3.1. nix-build

## نام

`nix-build` - ساخت یک عبارت Nix

## خلاصه دستور

```text
nix-build [paths…]
  [--arg name value]
  [--argstr name value]
  [{--attr | -A} attrPath]
  [--no-out-link]
  [--dry-run]
  [{--out-link | -o} outlink]
```

## رفع ابهام
این صفحه راهنما دستور `nix-build` را توصیف می‌کند که با دستور `nix build` متفاوت است. برای مستندات مربوط به مورد دوم، دستور `nix build --help` را اجرا کنید یا `man nix3-build` را ببینید.

## توضیحات
دستور `nix-build` درایویشن‌های توصیف‌شده توسط عبارت‌های Nix در *paths* را می‌سازد. اگر ساخت موفقیت‌آمیز باشد، یک پیوند نمادین (symlink) به نتیجه در پوشه فعلی قرار می‌دهد. پیوند نمادین `result` نام دارد. اگر چندین عبارت Nix وجود داشته باشد، یا عبارت‌های Nix به چندین درایویشن ارزیابی شوند، چندین پیوند نمادین با شماره‌گذاری ترتیبی ایجاد می‌شوند (`result`، `result-2` و غیره).

اگر هیچ *paths* مشخص نشده باشد، آنگاه `nix-build` از فایل `default.nix` در پوشه فعلی (در صورت وجود) استفاده خواهد کرد.

اگر عنصری از *paths* با `http://` یا `https://` شروع شود، به عنوان URL یک فایل تاربال (tarball) تفسیر می‌شود که بارگیری شده و در یک مکان موقت استخراج می‌شود. فایل تاربال باید شامل یک پوشه سطح بالا منفرد باشد که حداقل حاوی فایلی به نام `default.nix` باشد.

دستور `nix-build` اساساً پوششی پیرامون
[`nix-instantiate`](/pages/nix-manual/command-ref/nix-instantiate) (برای ترجمه یک عبارت Nix سطح بالا به یک [store derivation] سطح پایین) و [`nix-store --realise`](/pages/nix-manual/command-ref/nix-store/realise) (برای ساخت store derivation) است.

[store derivation]: /pages/nix-manual/glossary#gloss-store-derivation
> **هشدار**
>
> نتیجه ساخت به‌طور خودکار به عنوان ریشه جمع‌کننده‌ی زباله (garbage collector) نیکس ثبت می‌شود. این ریشه با حذف یا تغییر نام پیوند نمادین `result` به‌طور خودکار ناپدید می‌شود. بنابراین نام پیوند نمادین را تغییر ندهید.

## گزینه‌ها
همه گزینه‌هایی که در اینجا ذکر نشده‌اند، به [`nix-store --realise`](/pages/nix-manual/command-ref/nix-store/realise) منتقل می‌شوند، به جز `--arg` و `--attr` / `-A` که به [`nix-instantiate`](/pages/nix-manual/command-ref/nix-instantiate) منتقل می‌شوند.

- <span id="opt-no-out-link">[`--no-out-link`](#opt-no-out-link)</span>

  یک پیوند نمادین به مسیر خروجی ایجاد نکنید. توجه داشته باشید که در نتیجه، خروجی به ریشه‌ای از جمع‌کننده‌ی زباله تبدیل نمی‌شود و بنابراین ممکن است توسط `nix-store --gc` حذف شود.

- <span id="opt-dry-run">[`--dry-run`](#opt-dry-run)</span>

  نشان دهید چه مسیرهای انباری (store paths) ساخته یا بارگیری خواهند شد.

- <span id="opt-out-link">[`--out-link`](#opt-out-link)</span> / `-o` *outlink*

  نام پیوند نمادین به مسیر خروجی ایجاد شده را از `result` به *outlink* تغییر دهید.

## مثال‌ها
```shell
$ nix-build '<nixpkgs>' --attr firefox
store derivation is /nix/store/qybprl8sz2lc...-firefox-1.5.0.7.drv
/nix/store/d18hyl92g30l...-firefox-1.5.0.7

$ ls -l result
lrwxrwxrwx  ...  result -> /nix/store/d18hyl92g30l...-firefox-1.5.0.7

$ ls ./result/bin/
firefox  firefox-config
```

اگر یک درایویشن (derivation) دارای خروجی‌های متعددی باشد، `nix-build` خروجی پیش‌فرض (اولین خروجی) را خواهد ساخت. همچنین می‌توانید تمام خروجی‌ها را بسازید:

```shell
$ nix-build '<nixpkgs>' --attr openssl.all
```

این کار یک پیوند نمادین (symlink) برای هر خروجی با نام `result-outputname` ایجاد می‌کند.
اگر نام خروجی `out` باشد، پسوند حذف می‌شود. بنابراین اگر `openssl` دارای
خروجی‌های `out`، `bin` و `man` باشد، دستور `nix-build` پیوندهای نمادین
`result`، `result-bin` و `result-man` را ایجاد خواهد کرد. همچنین امکان ساخت یک
خروجی خاص وجود دارد:

```shell
$ nix-build '<nixpkgs>' --attr openssl.man
```

این کار یک پیوند نمادین (symlink) به نام `result-man` ایجاد خواهد کرد.

ساخت یک عبارت نیکس (Nix expression) ارائه‌شده در خط فرمان:

```shell
$ nix-build --expr 'with import <nixpkgs> { }; runCommand "foo" { } "echo bar > $out"'
$ cat ./result
bar
```

ساخت بسته GNU Hello از آخرین نسخهٔ (Revision) شاخهٔ master از مجموعه‌ی بسته‌های نیکس (Nixpkgs):

```shell
$ nix-build https://github.com/NixOS/nixpkgs/archive/master.tar.gz --attr hello
```
