# <a id="sec-pkgs-ociTools"></a> pkgs.ociTools

`pkgs.ociTools` مجموعه‌ای از توابع برای ایجاد باندل‌های زمان اجرای کنتینر طبق [مشخصات زمان اجرای OCI v1.0.0](https://github.com/opencontainers/runtime-spec/blob/v1.0.0/spec.md) است.
این مجموعه هیچ فرضی در مورد اجراکننده کنتینری که برای اجرای کنتینر ایجادشده انتخاب می‌کنید، ندارد.

مجموعه توابع موجود در `pkgs.ociTools` در حال حاضر [مشخصات تصویر OCI](https://github.com/opencontainers/image-spec) را مدیریت نمی‌کند.

در یک نگاه کلی، یک پیاده‌سازی OCI یک تصویر OCI را بارگیری کرده و سپس آن تصویر را در یک باندل سیستم‌فایل زمان اجرای OCI استخراج (unpack) می‌کند.
در این مرحله، باندل زمان اجرای OCI توسط یک زمان اجرای OCI اجرا خواهد شد.
`pkgs.ociTools` ابزارهایی را برای ایجاد باندل‌های زمان اجرای OCI فراهم می‌کند.

## <a id="ssec-pkgs-ociTools-buildContainer"></a> buildContainer

این تابع یک کنتینر زمان اجرای OCI (شامل یک `config.json` و یک پوشه سیستم‌فایل ریشه) می‌سازد که یک دستور واحد را در داخل خود اجرا می‌کند.
انبار نیکس (Nix store) کنتینر شامل تمام وابستگی‌های ارجاع‌داده‌شده توسط دستور داده‌شده خواهد بود.

این تابع فرض می‌کند که کنتینر روی پلتفرم‌های POSIX اجرا خواهد شد و پیکربندی‌ها را (مانند کاربری که فرآیند را اجرا می‌کند یا برخی mountها) طبق این فرض تنظیم می‌کند.
به همین دلیل، کنتینر ساخته‌شده با `buildContainer` بدون اعمال تغییرات در پیکربندی کنتینر، روی Windows یا سایر پلتفرم‌های غیر POSIX کار نخواهد کرد.
این تغییرات توسط `buildContainer` پشتیبانی نمی‌شوند.

برای پلتفرم‌های `linux`، تابع `buildContainer` همچنین فضاهای نام زیر را پیکربندی می‌کند (ببینید: `unshare(1)`) تا کنتینر OCI را از فضای نام سراسری ایزوله کند:
PID، شبکه، mount، IPC و UTS.

توجه داشته باشید که هیچ فضای نام کاربری ساخته نمی‌شود، بدین معنی که قادر به اجرای کنتینر نخواهید بود مگر اینکه کاربر `root` باشید.

### <a id="ssec-pkgs-ociTools-buildContainer-inputs"></a> Inputs

`buildContainer` منتظر آرگومانی با صفت‌های زیر است:

`args` (لیست رشته)

: مجموعه‌ای از آرگومان‌ها را برای اجرا در داخل کنتینر مشخص می‌کند.
  هر بسته‌ای که توسط `args` ارجاع داده شود، در داخل کنتینر در دسترس قرار خواهد گرفت.

`mounts` (مجموعه ویژگی؛ _اختیاری_)

: mountهای اضافی را مشخص می‌کند که زمان اجرا باید در اختیار کنتینر قرار دهد.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> همان‌طور که در [مسئله ۲۹۰۸۷۹#](https://github.com/NixOS/nixpkgs/issues/290879) توضیح داده شده است، این صفت در حال حاضر نادیده گرفته می‌شود.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> تابع `buildContainer` شامل حداقل مجموعه‌ای از سیستم‌فایل‌های لازم جهت mount شدن در کنتینر است و این مجموعه را نمی‌توان با صفت `mounts` تغییر داد.

  _مقدار پیش‌فرض:_ `{'{'}'{'{'}'{'}'}{'{'}'{'}'}'{'}'}`.

`readonly` (بولی؛ _اختیاری_)

: اگر `true` باشد، سیستم‌فایل ریشه کنتینر را به صورت فقط‌خواندنی تنظیم می‌کند.

  _مقدار پیش‌فرض:_ `false`.

`os` **منسوخ‌شده**

: سیستم‌عاملی را که سیستم‌فایل کنتینر بر پایه آن است مشخص می‌کند.
  در صورت مشخص شدن، مقدار آن باید از [مشخصات پیکربندی تصویر OCI](https://github.com/opencontainers/image-spec/blob/main/config.md#properties) پیروی کند.
  طبق مشخصات پیوند داده شده، تمام مقادیر ممکن برای `$GOOS` در [مستندات Go](https://go.dev/doc/install/source#environment) باید معتبر باشند، اما معمولاً یکی از مقادیر `darwin` یا `linux` خواهد بود.

  _مقدار پیش‌فرض:_ `"linux"`.

`arch` **منسوخ‌شده**

: برای مشخص کردن معماری‌ای استفاده می‌شود که باینری‌ها در سیستم‌فایل کنتینر برای آن کامپایل شده‌اند.
  در صورت مشخص شدن، مقدار آن باید از [مشخصات پیکربندی تصویر OCI](https://github.com/opencontainers/image-spec/blob/main/config.md#properties) پیروی کند.
  طبق مشخصات لینک‌شده، تمام مقادیر ممکن برای `$GOARCH` در [مستندات Go](https://go.dev/doc/install/source#environment) باید معتبر باشند، اما معمولاً یکی از مقادیر `386`، `amd64`، `arm` یا `arm64` خواهد بود.

  _مقدار پیش‌فرض:_ `x86_64`.

### <a id="ssec-pkgs-ociTools-buildContainer-examples"></a> مثال‌ها

<a id="ex-ociTools-buildContainer-bash"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # ایجاد یک کنتینر زمان اجرای OCI که `bash` را اجرا می‌کند
>
> این مثال از `ociTools.buildContainer` برای ایجاد یک کنتینر ساده استفاده می‌کند که `bash` را اجرا می‌کند.
>

> ```nix
> {
>   ociTools,
>   lib,
>   bash,
> }:
> ociTools.buildContainer {
>   args = [ (lib.getExe bash) ];
>
>   readonly = false;
> }
> ```
>
> به‌عنوان مثالی از نحوهٔ اجرای کنتینر تولیدشده توسط این بسته، از `runc` برای راه‌اندازی کنتینر استفاده خواهیم کرد.
> هر ابزار دیگری که از کنتینرهای OCI پشتیبانی کند را نیز می‌توان به جای آن به کار برد.
>

> ```shell
> $ nix-build
> (some output removed for clarity)
> /nix/store/7f9hgx0arvhzp2a3qphp28rxbn748l25-join
>
> $ cd /nix/store/7f9hgx0arvhzp2a3qphp28rxbn748l25-join
> $ nix-shell -p runc
> [nix-shell:/nix/store/7f9hgx0arvhzp2a3qphp28rxbn748l25-join]$ sudo runc run ocitools-example
> help
> GNU bash, version 5.2.26(1)-release (x86_64-pc-linux-gnu)
> (some output removed for clarity)
> ```
