# نام

`nix-instantiate` - نمونه‌سازی درایویشن‌های انبار از عبارت‌های Nix

# خلاصه

`nix-instantiate`
  [`--parse` | `--eval` [`--strict`] [`--raw` | `--json` | `--xml`] ]
  [`--read-write-mode`]
  [`--arg` *name* *value*]
  [{`--attr`| `-A`} *attrPath*]
  [`--add-root` *path*]
  [`--expr` | `-E`]
  *files…*

`nix-instantiate` `--find-file` *files…*

# توضیحات

دستور `nix-instantiate` [درایویشن انبار]ها را از عبارت‌های (سطح‌بالای) Nix تولید می‌کند.
این دستور عبارت‌های Nix را در هر یک از *files* (که به‌طور پیش‌فرض *./default.nix* است) ارزیابی می‌کند. هر عبارت سطح‌بالایی باید به یک درایویشن، فهرستی از درایویشن‌ها، یا مجموعه‌ای از درایویشن‌ها ارزیابی شود. مسیرهای درایویشن‌های انبار حاصل روی خروجی استاندارد چاپ می‌شوند.

[درایویشن انبار]: @docroot@/glossary.md#gloss-store-derivation

اگر *files* کاراکتر `-` باشد، یک عبارت Nix از ورودی استاندارد خوانده خواهد شد.

# گزینه‌ها

- `--add-root` *path*

  [گزینه متناظر](./nix-store.md) را در `nix-store` ببینید.

- `--parse`

  فقط فایل‌های ورودی را تجزیه کرده و درخت‌های نحوی انتزاعی آن‌ها را به عنوان یک عبارت Nix روی خروجی استاندارد چاپ کنید.

- `--eval`

  فقط فایل‌های ورودی را تجزیه و ارزیابی کرده و مقادیر حاصل را روی خروجی استاندارد چاپ کنید.
  درایویشن‌های انبار سریال‌سازی و در انبار نوشته نمی‌شوند، بلکه فقط هش شده و دور انداخته می‌شوند.

  > **هشدار**
  >
  > این گزینه خروجی‌ای تولید می‌کند که می‌تواند به عنوان یک عبارت Nix تجزیه شود که هنگام ارزیابی، نتیجه‌ای متفاوت از عبارت ورودی تولید خواهد کرد.
  > برای مثال، این دو عبارت Nix با وجود داشتن معنای متفاوت، نتیجه یکسانی را چاپ می‌کنند:
  >
```console
  > $ nix-instantiate --eval --expr '{ a = {}; }'
  > { a = <CODE>; }
  > $ nix-instantiate --eval --expr '{ a = <CODE>; }'
  > { a = <CODE>; }
  > ```
>
> برای خروجی خوانا برای انسان، دستور `nix eval` (تجربی) اطلاعات بیشتری ارائه می‌دهد:
>
```console
  > $ nix-instantiate --eval --expr 'a: a'
  > <LAMBDA>
  > $ nix eval --expr 'a: a'
  > «lambda @ «string» :1:1»
  > ```
>
> برای خروجی قابل‌خواندن توسط ماشین، گزینه `--xml` خروجی صریح و بدون ابهامی تولید می‌کند:
>
```console
  > $ nix-instantiate --eval --xml --expr '{ foo = <CODE>; }'
  > <?xml version='1.0' encoding='utf-8'?>
  > <expr>
  >   <attrs>
  >     <attr column="3" line="1" name="foo">
  >       <unevaluated />
  >     </attr>
  >   </attrs>
  > </expr>
  > ```

- `--find-file`

  فایل‌های داده‌شده را در مسیر جستجوی Nix (همان‌طور که توسط متغیر محیطی `NIX_PATH` مشخص شده است) جستجو کنید. در صورت پیدا شدن، مسیرهای مطلق متناظر را روی خروجی استاندارد چاپ کنید. برای نمونه، اگر `NIX_PATH` برابر با `nixpkgs=/home/alice/nixpkgs` باشد، دستور `nix-instantiate --find-file nixpkgs/default.nix` مسیر `/home/alice/nixpkgs/default.nix` را چاپ خواهد کرد.

- `--strict`

  هنگامی که با `--eval` استفاده شود، عناصر فهرست و صفت‌ها را به‌صورت بازگشتی ارزیابی می‌کند. به‌طور عادی، چنین زیرعبارت‌هایی ارزیابی‌نشده باقی می‌مانند (زیرا زبان Nix تنبل است).

  > **هشدار**
  >
  > این گزینه می‌تواند باعث پایان‌ناپذیر شدن شود، زیرا ساختارهای داده‌ی تنبل می‌توانند به‌طور بی‌نهایت بزرگ باشند.

- `--raw`

  هنگامی که با `--eval` استفاده شود، نتیجه‌ی ارزیابی باید یک رشته باشد که به‌صورت کلام‌به‌کلام، بدون علامت نقل‌قول، فرار دادن (escaping) یا نویسه‌ی خط جدید در انتها چاپ می‌شود.

- `--json`

  هنگامی که با `--eval` استفاده شود، مقدار حاصل را به‌جای یک عبارت Nix، به‌عنوان یک نمایش JSON از درخت گرامر انتزاعی چاپ می‌کند.

- `--xml`

  هنگامی که با `--eval` استفاده شود، مقدار حاصل را به‌جای یک عبارت Nix، به‌عنوان یک نمایش XML از درخت گرامر انتزاعی چاپ می‌کند. طرح‌واره (schema) همان طرح‌واره‌ای است که توسط تابع توکار [`toXML`](../language/builtins.md) استفاده می‌شود.

- `--read-write-mode`

  هنگامی که با `--eval` استفاده شود، ارزیابی را در حالت خواندن/نوشتن انجام می‌دهد تا ویژگی‌های زبان nix که به آن نیاز دارند همچنان کار کنند (به‌قیمت نیاز به انجام اشتقاق ساخت برای هر درایویشن ارزیابی‌شده). اگر این گزینه فعال نباشد، ممکن است مسیرهای انبار ارزیابی‌نشده‌ای در خروجی نهایی وجود داشته باشد.

{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# مثال‌ها

[درایویشن انبار] را از یک عبارت Nix ایجاد کرده و با استفاده از `nix-store` آن‌ها را بسازید:

```console
$ nix-instantiate test.nix (instantiate)
/nix/store/cigxbmvy6dzix98dxxh9b6shg7ar5bvs-perl-BerkeleyDB-0.26.drv

$ nix-store --realise $(nix-instantiate test.nix) (build)
...
/nix/store/qhqk4n8ci095g3sdp93x7rgwyh9rdvgk-perl-BerkeleyDB-0.26 (output path)

$ ls -l /nix/store/qhqk4n8ci095g3sdp93x7rgwyh9rdvgk-perl-BerkeleyDB-0.26
dr-xr-xr-x 2 eelco users 4096 1970-01-01 01:00 lib
...
```

شما همچنین می‌توانید یک عبارت نیکس (Nix expression) را در خط فرمان بدهید:

```console
$ nix-instantiate --expr 'with import <nixpkgs> { }; hello'
/nix/store/j8s4zyv75a724q38cb0r87rlczaiag4y-hello-2.8.drv
```

این معادل است با:

```console
$ nix-instantiate '<nixpkgs>' --attr hello
```

تجزیه و ارزیابی عبارت‌های نیکس (Nix expression):

```console
$ nix-instantiate --parse --expr '1 + 2'
1 + 2
```

```console
$ nix-instantiate --eval --expr '1 + 2'
3
```

```console
$ nix-instantiate --eval --xml --expr '1 + 2'
<?xml version='1.0' encoding='utf-8'?>
<expr>
  <int value="3" />
</expr>
```

تفاوت بین ارزیابی غیرسخت و سخت:

```console
$ nix-instantiate --eval --xml --expr '{ x = {}; }'
<?xml version='1.0' encoding='utf-8'?>
<expr>
  <attrs>
    <attr column="3" line="1" name="x">
      <unevaluated />
    </attr>
  </attrs>
</expr>

$ nix-instantiate --eval --xml --strict --expr '{ x = {}; }'
<?xml version='1.0' encoding='utf-8'?>
<expr>
  <attrs>
    <attr column="3" line="1" name="x">
      <attrs>
      </attrs>
    </attr>
  </attrs>
</expr>
```
