# نام

`nix-copy-closure` - کپی کردن شیءهای انبار به یا از یک ماشین راه دور از طریق SSH

# خلاصه

`nix-copy-closure`
  [`--to` | `--from` ]
  [`--gzip`]
  [`--include-outputs`]
  [`--use-substitutes` | `-s`]
  [`-v`]
  [_user_@]_machine_[:_port_] _paths_

# توضیحات

با داشتن _paths_ از یک ماشین، `nix-copy-closure` [closure](@docroot@/glossary.md#gloss-closure) آن مسیرها (یعنی تمام وابستگی‌های آن‌ها در انبار Nix) را محاسبه کرده و [store objects](@docroot@/glossary.md#gloss-store-object) موجود در آن closure را از طریق SSH به ماشینی دیگر کپی می‌کند.
این ابزار شیءهای انباری را که در حال حاضر روی ماشین دیگر موجود هستند، کپی نمی‌کند.

> **نکته**
>
> در حالی که انبار Nix مورد استفاده روی ماشین محلی را می‌توان در خط فرمان با گزینه [`--store`](@docroot@/command-ref/conf-file.md#conf-store) مشخص کرد، انبار Nix قابل دسترس روی ماشین راه دور تنها می‌تواند روی همان ماشین راه دور [پیکربندی استاتیک](@docroot@/command-ref/conf-file.md#configuration-file) شود.

از آنجا که `nix-copy-closure` تابع `ssh` را فراخوانی می‌کند، ممکن است لازم باشد با ماشین راه دور احراز هویت کنید.
در واقع، ممکن است از شما _دو بار_ درخواست احراز هویت شود؛ زیرا `nix-copy-closure` در حال حاضر دو بار به ماشین راه دور متصل می‌شود: بار اول برای دریافت مجموعه مسیرهای گمشده روی ماشین مقصد، و بار دوم برای ارسال دامپ آن مسیرها.
هنگام استفاده از احراز هویت کلید عمومی، می‌توانید با استفاده از `ssh-agent` از تایپ کردن عبارت عبور جلوگیری کنید.

# گزینه‌ها

- `--to`

  کپی کردن closure مربوط به _paths_ از یک انبار Nix قابل دسترس از ماشین محلی به انبار Nix روی _machine_ راه دور.
  این رفتار پیش‌فرض است.

- `--from`

  کپی کردن closure مربوط به _paths_ از انبار Nix روی _machine_ راه دور به انبار Nix مشخص‌شدهٔ ماشین محلی.

- `--gzip`

  فعال‌سازی فشرده‌سازی اتصال SSH.

- `--include-outputs`

  همچنین کپی کردن خروجی‌های [store derivation]هایی که در closure گنجانده شده‌اند.

  [store derivation]: @docroot@/glossary.md#gloss-store-derivation

- `--use-substitutes` / `-s`

  تلاش برای بارگیری شیءهای انبار مفقود روی مقصد از [substituters](@docroot@/command-ref/conf-file.md#conf-substituters).
  هر شیء انباری که نتواند روی مقصد جایگزین شود، همچنان به طور معمولی از مبدأ کپی می‌شود.
  این کار برای مثال زمانی مفید است که اتصال بین ماشین مبدأ و مقصد کند است، اما اتصال بین ماشین مقصد و `cache.nixos.org` (سرور کش باینری پیش‌فرض) سریع است.

{{#include ./opt-common.md}}

# متغیرهای محیطی

- `NIX_SSHOPTS`

  گزینه‌های اضافی که باید در خط فرمان به `ssh` پاس داده شوند.

{{#include ./env-common.md}}

# مثال‌ها

> **مثال**
>
> کپی کردن GNU Hello به همراه تمام وابستگی‌های آن به یک ماشین راه دور:
>
```shell-session
> $ storePath="$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)"
> $ nix-copy-closure --to alice@itchy.example.org "$storePath"
> copying 5 paths...
> copying path '/nix/store/h6q8sqsqfbd3252f9gixqn3z282wds7m-xgcc-13.2.0-libgcc' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/imnwvn96lw355giswsk36hx105j4wnpj-libunistring-1.1' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/85301indj7scg34spnfczkz72jgv8wa9-libidn2-2.3.7' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/ypwfsaljwhzw9iffiysxmxnhjj8v7np0-glibc-2.39-31' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/0dklv59zppdsqdvgf0qdvjgzcs5wbwxa-hello-2.12.1' to 'ssh://alice@itchy.example.org'...
> ```

> **مثال**
>
> کپی کردن GNU Hello از یک ماشین راه دور با استفاده از یک مسیر انبار شناخته‌شده و اجرای آن:
>
```shell-session
> $ storePath="$(nix-instantiate --eval --raw '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello.outPath)"
> $ nix-copy-closure --from alice@itchy.example.org "$storePath"
> $ "$storePath"/bin/hello
> Hello, world!
> ```
