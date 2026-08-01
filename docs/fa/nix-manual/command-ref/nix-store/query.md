# نام

`nix-store --query` - نمایش اطلاعات درباره مسیرهای انبار

# خلاصه

`nix-store` {`--query` | `-q`}
  {`--outputs` | `--requisites` | `-R` | `--references` | `--referrers` |
  `--referrers-closure` | `--deriver` | `-d` | `--valid-derivers` |
  `--graph` | `--tree` | `--binding` *name* | `-b` *name* | `--hash` |
  `--size` | `--roots`}
  [`--use-output`] [`-u`] [`--force-realise`] [`-f`]
  *paths…*

# توضیحات

عملیات `--query` اطلاعات مختلفی را درباره مسیرهای انبار نمایش می‌دهد. پرس‌وجوها در ادامه شرح داده شده‌اند. حداکثر یک پرس‌وجو را می‌توان مشخص کرد. پرس‌وجوی پیش‌فرض `--outputs` است.

مسیرهای *paths* همچنین می‌توانند پیوندهای نمادین از خارج از انبار Nix به انبار Nix باشند. در این صورت، پرس‌وجوی مورد نظر روی هدف پیوند نمادین اعمال می‌شود.

# گزینه‌های رایج پرس‌وجو

- `--use-output` / `-u`

  برای هر آرگومان ارسالی به پرس‌وجو که یک [درایویشن انبار] است، پرس‌وجو را به جای آن روی مسیر خروجی درایویشن اعمال کنید.

- `--force-realise` / `-f`

  ابتدا هر آرگومان پرس‌وجو را محقق (realise) کنید (ببینید [`nix-store --realise`](./realise.md)).

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

# پرس‌وجوها

- `--outputs`

  [مسیرهای خروجی] درایویشن‌های انبار *paths* را چاپ می‌کند. این‌ها همان مسیرهایی هستند که هنگام ساخت درایویشن تولید خواهند شد.

  [output paths]: @docroot@/glossary.md#gloss-output-path

- `--references`

  مجموعه [ارجاعات] مسیرهای انبار *paths*، یعنی وابستگی‌های بی‌واسطه آن‌ها را چاپ می‌کند. (برای *تمام* وابستگی‌ها، از `--requisites` استفاده کنید.)

  [references]: @docroot@/glossary.md#gloss-reference

- `--requisites` / `-R`

  مجموعه [*ملزومات*][requisite] (که بیشتر به عنوان [بسته closure] شناخته می‌شود) مسیرهای انبار *paths* را چاپ می‌کند.

  [requisite]: @docroot@/glossary.md#gloss-requisite
  [closure]: @docroot@/glossary.md#gloss-closure

  این پرس‌وجو یک گزینه دارد:

    - `--include-outputs`
      همچنین مسیرهای خروجی موجود از [درایویشن انبار]ها و بسته‌های closure آن‌ها را نیز شامل شود.

  از این پرس‌وجو می‌توان برای پیاده‌سازی انواع مختلف استقرار استفاده کرد. یک *استقرار از روی کد منبع* با توزیع closure یک درایویشن انبار به دست می‌آید. یک *استقرار باینری* با توزیع closure یک مسیر خروجی به دست می‌آید. یک *استقرار کش* (استقرار ترکیبی منبع/باینری، شامل باینری‌های وابستگی‌های مختص زمان ساخت) با توزیع closure یک درایویشن انبار و مشخص کردن گزینه `--include-outputs` به دست می‌آید.

- `--referrers`

  مجموعه [*ارجاع‌دهندگان*][referrer] مسیرهای انبار *paths* را چاپ می‌کند، یعنی مسیرهای انباری که در حال حاضر در انبار Nix وجود دارند و به یکی از *paths* ارجاع می‌دهند. توجه داشته باشید که برخلاف ارجاعات، مجموعه ارجاع‌دهندگان ثابت نیست؛ و با اضافه یا حذف شدن مسیرهای انبار می‌تواند تغییر کند.

  [referrer]: @docroot@/glossary.md#gloss-referrer

- `--referrers-closure`

  بسته closure مجموعه مسیرهای انبار *paths* را تحت [رابطه ارجاع‌دهندگان][referrer] چاپ می‌کند؛ یعنی تمام مسیرهای انباری که به طور مستقیم یا غیرمستقیم به یکی از *paths* ارجاع می‌دهند. این‌ها تمام مسیرهایی در انبار Nix هستند که در حال حاضر به *paths* وابسته‌اند.

  [referrer]: @docroot@/glossary.md#gloss-referrer

- `--deriver` / `-d`

چاپ [deriver]ی که برای ساخت مسیرهای انبار *paths* استفاده شده است. اگر مسیر فاقد deriver باشد (مثلاً یک فایل سورس باشد)، یا deriver آن ناشناخته باشد (مثلاً در سناریوی استقرار صرفاً باینری)، رشته‌ی `unknown-deriver` چاپ می‌شود.
تضمینی وجود ندارد که deriver بازگردانده‌شده در انبار محلی وجود داشته باشد، برای مثال زمانی که *paths* از یک کش باینری جایگزین (substituted) شده باشند.
برای دریافت تنها مسیرهای معتبر، به جای آن از `--valid-derivers` استفاده کنید.

[deriver]: @docroot@/glossary.md#gloss-deriver

- `--valid-derivers`

  مجموعه‌ای از فایل‌های derivation ( `.drv`) را چاپ می‌کند که فرض بر این است با ریلایز شدن (realized)، مسیرهای مذکور را تولید می‌کنند. ممکن است چیزی چاپ نکند، برای مثال برای مسیرهای سورس یا مسیرهایی که از یک کش باینری جایگزین شده‌اند.

- `--graph`

  گراف ارجاعات مسیرهای انبار *paths* را در قالب ابزار `dot` از [مجموعه Graphviz](http://www.graphviz.org/) شرکت AT\&T چاپ می‌کند. این قابلیت را می‌توان برای تجسم گراف‌های وابستگی استفاده کرد. برای به‌دست آوردن یک گراف وابستگی زمان ساخت، این گزینه را روی یک derivation انبار اعمال کنید. برای به‌دست آوردن یک گراف وابستگی زمان اجرا، آن را روی یک مسیر خروجی اعمال کنید.

- `--tree`

  گراف ارجاعات مسیرهای انبار *paths* را به صورت یک درخت متنی ASCII تو در تو چاپ می‌کند. ارجاعات بر اساس اندازه بسته (closure size) به ترتیب نزولی مرتب می‌شوند؛ این کار معمولاً درخت را مسطح‌تر کرده و خوانایی آن را افزایش می‌دهد. پرس‌وجو تنها زمانی وارد یک مسیر انبار می‌شود که برای اولین بار با آن روبه‌رو شود؛ این کار از رشد بیش از حد و انفجار نمایشی درخت گراف جلوگیری می‌کند.

- `--graphml`

  گراف ارجاعات مسیرهای انبار *paths* را در قالب فایل [GraphML](http://graphml.graphdrawing.org/) چاپ می‌کند. این قابلیت را می‌توان برای تجسم گراف‌های وابستگی استفاده کرد. برای به‌دست آوردن یک گراف وابستگی زمان ساخت، این گزینه را روی یک [store derivation] اعمال کنید. برای به‌دست آوردن یک گراف وابستگی زمان اجرا، آن را روی یک مسیر خروجی اعمال کنید.

- `--binding` *name* / `-b` *name*

  مقدار صفت *name* (یعنی متغیر محیطی) مربوط به [store derivation]های *paths* را چاپ می‌کند. نداشتن صفت مشخص‌شده توسط یک derivation، یک خطای محسوب می‌شود.

- `--hash`

  هش SHA-256 محتویات مسیرهای انبار *paths* را چاپ می‌کند (یعنی هش خروجی دستور `nix-store --dump` روی مسیرهای داده‌شده). از آنجا که این هش در پایگاه داده Nix ذخیره می‌شود، این یک عملیات سریع است.

- `--size`

  اندازه محتویات مسیرهای انبار *paths* را بر حسب بایت چاپ می‌کند؛ به بیان دقیق‌تر، اندازه خروجی `nix-store --dump` روی مسیرهای داده‌شده را چاپ می‌کند. توجه داشته باشید که فضای دیسک واقعی مورد نیاز برای مسیرهای انبار ممکن است بیشتر باشد، به‌ویژه در سیستم‌فایل‌هایی با اندازه‌های خوشه‌ای (cluster sizes) بزرگ.

- `--roots`

  ریشه‌های جمع‌کننده‌ی زباله (garbage collector) که مستقیماً یا غیرمستقیم به مسیرهای انبار *paths* اشاره می‌کنند را چاپ می‌کند.

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# مثال‌ها

چاپ کردن بسته (وابستگی‌های زمان اجرا) برنامه‌ی `svn` در محیط کاربر فعلی:

```console
$ nix-store --query --requisites $(which svn)
/nix/store/5mbglq5ldqld8sj57273aljwkfvj22mc-subversion-1.1.4
/nix/store/9lz9yc6zgmc0vlqmn2ipcpkjlmbi51vv-glibc-2.3.4
...
```

چاپ وابستگی‌های زمان ساخت `svn` عبارتند از:

```console
$ nix-store --query --requisites $(nix-store --query --deriver $(which svn))
/nix/store/y6qa66l9h0pw161crnlk6y16rdrcljx4-grep-2.5.1.tar.bz2.drv
/nix/store/z716h753s97jhnzvfank2srqbljswpgm-gcc-wrapper.sh
/nix/store/f39x0q73rjdyvzm93y9wrkfr6x39lb7f-glibc-2.3.4.drv
... lots of other paths ...
```

تفاوت این مثال با مثال قبلی در این است که ما بسته‌ی کامل (closure) مربوط به derivation (`-qd`) را درخواست می‌کنیم، نه بسته‌ی کامل مسیر خروجی حاوی `svn` را.

وابستگی‌های زمان ساخت را به صورت یک درخت نمایش دهید:

```console
$ nix-store --query --tree $(nix-store --query --deriver $(which svn))
/nix/store/7i5082kfb6yjbqdbiwdhhza0am2xvh6c-subversion-1.1.4.drv
+---/nix/store/vxnmkc8l8d2ijjha4xwhkfgx9vvc3q4c-builder.sh
+---/nix/store/rn9776dy82n5qrgz7xbcl1iw4vfkcrkk-bash-3.0.drv
|   +---/nix/store/x9j20hz6bln1crzn55qifk0bbsm8v5ac-bash
|   +---/nix/store/ajnn1mcm45wjvn0rlc22gvx2cwhjnazx-builder.sh
...
```

تمام مسیرهایی را که به همان کتابخانه `openssl` به عنوان `svn` وابسته هستند، نشان دهید:

```console
$ nix-store --query --referrers $(nix-store --query --binding openssl $(nix-store --query --deriver $(which svn)))
/nix/store/23ny9l9wixx21632y2wi4p585qhva1q8-sylpheed-1.0.0
/nix/store/5mbglq5ldqld8sj57273aljwkfvj22mc-subversion-1.1.4
/nix/store/dpmvp969yhdqs7lm2r1a3gng7pyq6vy4-subversion-1.1.3
/nix/store/l51240xqsgg8a7yrbqdx1rfzyv6l26fx-lynx-2.8.5
```

تمام مسیرهایی را نمایش دهید که مستقیماً یا غیرمستقیم به Glibc (کتابخانه C) استفاده‌شده توسط `svn` وابسته هستند:

```console
$ nix-store --query --referrers-closure $(ldd $(which svn) | grep /libc.so | awk '{print $3}')
/nix/store/034a6h4vpz9kds5r6kzb9lhh81mscw43-libgnomeprintui-2.8.2
/nix/store/15l3yi0d45prm7a82pcrknxdh6nzmxza-gawk-3.1.4
...
```

توجه داشته باشید که `ldd` دستوری است که کتابخانه‌های پویای استفاده‌شده توسط یک فایل اجرایی ELF را چاپ می‌کند.

تصویری از گراف وابستگی‌های زمان اجرا برای پروفایل کاربری فعلی بسازید:

```console
$ nix-store --query --graph ~/.nix-profile | dot -Tps > graph.ps
$ gv graph.ps
```

تمام ریشه‌های جمع‌کننده‌ی زباله (garbage collector) را نشان بده که به یک مسیر انبار اشاره می‌کنند که به `svn` وابسته است:

```console
$ nix-store --query --roots $(which svn)
/nix/var/nix/profiles/default-81-link
/nix/var/nix/profiles/default-82-link
/home/eelco/.local/state/nix/profiles/profile-97-link
```
