# نام

`nix-env --install` - افزودن بسته‌ها به پروفایل کاربر

# خلاصه دستور

`nix-env` {`--install` | `-i`} *args…*
  [{`--prebuilt-only` | `-b`}]
  [{`--attr` | `-A`}]
  [`--from-expression`] [`-E`]
  [`--from-profile` *path*]
  [`--preserve-installed` | `-P`]
  [`--remove-all` | `-r`]
  [`--priority` *priority*]

# توضیحات

عملیات `--install` یک پروفایل جدید ایجاد می‌کند.
این عملیات بر اساس نسل فعلی [profile] فعال است، که مجموعه‌ای از [store paths] توصیف‌شده توسط *args* به آن اضافه می‌شوند.

[store paths]: @docroot@/store/store-path.md

آرگومان‌های *args* به روش‌های مختلفی به مسیرهای انبار نگاشت می‌شوند:

- به‌طور پیش‌فرض، *args* مجموعه‌ای از نام‌ها است که نمایانگر derivationها در [default Nix expression] هستند.
  این موارد [realised] شده و مسیرهای خروجی حاصل نصب می‌شوند.
  در صورتی که گزینه `--preserve-installed` مشخص نشده باشد، derivationهای در حال حاضر نصب‌شده‌ای که نامشان با نام derivation در حال افزودن برابر است، حذف خواهند شد.

  [derivation expression]: @docroot@/glossary.md#gloss-derivation-expression
  [default Nix expression]: @docroot@/command-ref/files/default-nix-expression.md
  [realised]: @docroot@/glossary.md#gloss-realise

  اگر چندین derivation مطابق با یک نام در *args* وجود داشته باشد که دارای نام یکسانی هستند (مثلاً `gcc-3.3.6` و `gcc-4.1.1`)، آنگاه derivation با بالاترین *priority* استفاده می‌شود. یک derivation می‌تواند با اعلام صفت `meta.priority` یک اولویت تعریف کند. این صفت باید یک عدد باشد که مقدار بالاتر نشان‌دهنده اولویت پایین‌تر است. اولویت پیش‌فرض `5` است.

  اگر چندین derivation منطبق با اولویت یکسان وجود داشته باشد، آنگاه derivation با بالاترین نسخه نصب خواهد شد.

  شما می‌توانید با مشخص کردن دقیق نسخه‌ها، نصب چندین derivation با نام یکسان را اجبار کنید. برای نمونه، دستور `nix-env --install gcc-3.3.6 gcc-4.1.1` هر دو نسخه GCC را نصب خواهد کرد (و احتمالاً باعث ایجاد تداخل در پروفایل کاربر خواهد شد!).

- اگر [`--attr`](#opt-attr) / `-A` مشخص شده باشد، آرگومان‌ها *مسیرهای صفت (attribute paths)* هستند که صفت‌ها را از [default Nix expression] انتخاب می‌کنند.
  این روش سریع‌تر از استفاده از نام‌های derivation بوده و بدون ابهام است.
  مسیرهای صفت بسته‌های موجود را با [`nix-env --query`](./query.md) نمایش دهید:
```console
  nix-env --query --available --attr-path
  ```

- اگر `--from-profile` به همراه *path* داده شود، *args* مجموعه‌ای از نام‌هاست که [store paths] نصب‌شده در پروفایل *path* را نشان می‌دهند. این یک روش آسان برای کپی کردن عناصر محیط کاربر از یک پروفایل به پروفایلی دیگر است.

- اگر `--from-expression` داده شود، *args* [Nix language functions](@docroot@/language/syntax.md#functions) هستند که با [default Nix expression] به عنوان تنها آرگومانشان فراخوانی می‌شوند.
  درایویشن‌های بازگردانده‌شده توسط آن فراخوانی‌های تابع، نصب می‌شوند.
  این امر اجازه می‌دهد تا درایویشن‌ها به روشی غیرقابل‌ابهام مشخص شوند، که اگر چندین درایویشن با نام یکسان وجود داشته باشد، ضروری است.

- اگر `--priority` به همراه *priority* داده شود، اولویت درایویشن‌هایی که در حال نصب هستند روی *priority* تنظیم می‌شود.
  از این قابلیت می‌توان برای بازنویسی اولویت درایویشن‌هایی که در حال نصب هستند استفاده کرد.
  این کار زمانی مفید است که *args* شامل [store paths] باشد که هیچ اطلاعات اولویتی ندارند.

- اگر *args* شامل [store paths] باشد که به [store derivations][store derivation] اشاره می‌کنند، آنگاه آن store derivations [realised] شده و مسیرهای خروجی حاصل نصب می‌شوند.

- اگر *args* شامل [store paths] باشد که به store derivations اشاره نمی‌کنند، آنگاه این موارد [realised] و نصب می‌شوند.

- به طور پیش‌فرض، تمام [outputs](@docroot@/language/derivations.md#attr-outputs) برای هر [store derivation] نصب می‌شوند.
  این رفتار را می‌توان با افزودن صفت `meta.outputsToInstall` روی درایویشن که زیرمجموعه‌ای از نام‌های خروجی را فهرست می‌کند، بازنویسی کرد.

  مثال:

  فایل `example.nix` یک درایویشن با دو خروجی `foo` و `bar` تعریف می‌کند که هر کدام شامل یک فایل هستند.
```nix
  # example.nix
  let
    pkgs = import <nixpkgs> {};
    command = ''
      ${pkgs.coreutils}/bin/mkdir -p $foo $bar
      echo foo > $foo/foo-file
      echo bar > $bar/bar-file
    '';
  in
  derivation {
    name = "example";
    builder = "${pkgs.bash}/bin/bash";
    args = [ "-c" command ];
    outputs = [ "foo" "bar" ];
    system = builtins.currentSystem;
  }
  ```

نصب از روی این عبارت نیکس باعث می‌شود فایل‌های هر دو خروجی در پروفایل فعلی ظاهر شوند.
```console
  $ nix-env --install --file example.nix
  installing 'example'
  $ ls ~/.nix-profile
  foo-file
  bar-file
  manifest.nix
  ```

افزودن `meta.outputsToInstall` به آن derivation باعث می‌شود که `nix-env` فقط فایل‌ها را از خروجی‌های مشخص‌شده نصب کند.
```nix
  # example-outputs.nix
  import ./example.nix // { meta.outputsToInstall = [ "bar" ]; }
  ```

  ```console
  $ nix-env --install --file example-outputs.nix
  installing 'example'
  $ ls ~/.nix-profile
  bar-file
  manifest.nix
  ```

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

# گزینه‌ها

- `--prebuilt-only` / `-b`

  فقط از درایویشن‌هایی استفاده کنید که برای آن‌ها یک جایگزین ثبت شده است؛ یعنی یک باینری پیش‌ساخته وجود دارد که می‌توان آن را به جای ساختن درایویشن بارگیری کرد. بنابراین، هیچ بسته‌ای از روی کد منبع ساخته نخواهد شد.

- `--preserve-installed` / `-P`

  درایویشن‌هایی را که نام آن‌ها با یکی از درایویشن‌های در حال نصب مطابقت دارد، حذف نکنید. معمولاً تلاش برای داشتن دو نسخه از یک بسته در یک نسل از یک پروفایل، به دلیل تداخل نام فایل بین دو نسخه، منجر به خطایی در ساخت آن نسل می‌شود. با این حال، این موضوع برای همه بسته‌ها صدق نمی‌کند.

- `--remove-all` / `-r`

  ابتدا تمام بسته‌های از‌پیش‌نصب‌شده را حذف کنید. این کار معادل اجرای اولیه `nix-env --uninstall '.*'` است، با این تفاوت که همه‌چیز در یک تراکنش واحد انجام می‌شود.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

برای نصب یک بسته با استفاده از یک مسیر صفت خاص از عبارت Nix فعال:

```console
$ nix-env --install --attr gcc40mips
installing `gcc-4.0.2'
$ nix-env --install --attr xorg.xorgserver
installing `xorg-server-1.2.0'
```

برای نصب نسخه مشخصی از `gcc` با استفاده از نام derivation:

```console
$ nix-env --install gcc-3.3.2
installing `gcc-3.3.2'
uninstalling `gcc-3.1'
```

استفاده از مسیر صفت (attribute path) برای انتخاب یک بسته ترجیح داده می‌شود، زیرا بسیار سریع‌تر است و هیچ‌گونه تداخل یا چند تطابق (multiple matches) رخ نخواهد داد.

توجه داشته باشید که نسخهٔ از‌پیش‌نصب‌شده حذف می‌شود، زیرا گزینهٔ `--preserve-installed` مشخص نشده بود.

برای نصب یک نسخهٔ دلخواه:

```console
$ nix-env --install gcc
installing `gcc-3.3.2'
```

برای نصب تمام درایویشن‌ها در عبارت نیکس (Nix expression) `foo.nix`:

```console
$ nix-env --file ~/foo.nix --install '.*'
```

برای کپی کردن مسیر انبار با نام نمادین `gcc` از یک پروفایل دیگر:

```console
$ nix-env --install --from-profile /nix/var/nix/profiles/foo gcc
```

برای نصب یک [derivation] مشخص (که معمولاً توسط `nix-instantiate` ایجاد می‌شود):

```console
$ nix-env --install /nix/store/8la6y31fmm6i4wfmby6avly1wf718xnj-gcc-3.4.3.drv
```

برای نصب یک مسیر خروجی خاص:

```console
$ nix-env --install /nix/store/y3cgx0xj1p4iv9x0pnnmdhr8iyg741vk-gcc-3.4.3
```

برای نصب از روی یک عبارت نیکس (Nix expression) که در خط فرمان مشخص شده است:

```console
$ nix-env --file ./foo.nix --install --expr \
    'f: (f {system = "i686-linux";}).subversionWithJava'
```

یعنی این عبارت به `(f: (f {system =
"i686-linux";}).subversionWithJava) (import ./foo.nix)` ارزیابی می‌شود؛ در نتیجه صفت `subversionWithJava` را از مجموعهٔ بازگردانده‌شده با فراخوانی تابع تعریف‌شده در `./foo.nix` انتخاب می‌کند.

یک اجرای آزمایشی (dry-run) به شما می‌گوید چه مسیرهایی بارگیری یا از روی کد منبع ساخته خواهند شد:

```console
$ nix-env --file '<nixpkgs>' --install --attr hello --dry-run
(dry run; not doing anything)
installing ‘hello-2.10’
this path will be fetched (0.04 MiB download, 0.19 MiB unpacked):
  /nix/store/ikwkxz4wwlp2g1428n7dy729cg1d9hin-hello-2.10
  ...
```

برای نصب Firefox از آخرین نسخه در کانال Nixpkgs/NixOS 14.12:

```console
$ nix-env --file https://github.com/NixOS/nixpkgs/archive/nixos-14.12.tar.gz --install --attr firefox
```
