# pkgs.dockerTools {#sec-pkgs-dockerTools}

`pkgs.dockerTools` مجموعه توابعی برای ایجاد و دستکاری تصاویر Docker بر اساس [مشخصات تصویر داکر نسخه ۱.۳.۱](https://github.com/moby/docker-image-spec/blob/v1.3.1/spec.md) است.
خود Docker برای انجام هیچ‌یک از عملیاتی که توسط این توابع انجام می‌شوند استفاده نمی‌شود.

## buildImage {#ssec-pkgs-dockerTools-buildImage}

این تابع یک تاربال مخزن (repository tarball) سازگار با Docker حاوی یک تصویر واحد می‌سازد.
به این ترتیب، نتیجه برای بارگذاری در Docker با دستور `docker image load` مناسب است (برای نحوه انجام این کار، [](#ex-dockerTools-buildImage) را ببینید).

این تابع یک لایه واحد برای تمام فایل‌ها (و وابستگی‌ها) که در آرگومان آن مشخص شده‌اند ایجاد می‌کند.
تنها وابستگی‌های جدیدی که در لایه‌های موجود قرار ندارند کپی خواهند شد.
اگر ترجیح می‌دهید چندین لایه برای فایل‌ها و وابستگی‌هایی که می‌خواهید به تصویر اضافه کنید ایجاد کنید، به جای آن [](#ssec-pkgs-dockerTools-buildLayeredImage) یا [](#ssec-pkgs-dockerTools-streamLayeredImage) را ببینید.

این تابع اجازه می‌دهد یک اسکریپت در طول فرآیند تولید لایه اجرا شود و رفتار سفارشی روی نتایج نهایی تصویر تاثیر بگذارد (مستندات صفات `runAsRoot` و `extraCommands` را ببینید).

تاربال مخزن حاصل، یک تصویر واحد را طبق آنچه توسط صفات `name` و `tag` مشخص شده‌است فهرست می‌کند.
به طور پیش‌فرض، آن تصویر از یک تاریخ ایجاد ثابت استفاده می‌کند (مستندات صفت (attribute) `created` را ببینید).
این ویژگی به `buildImage` اجازه می‌دهد تصاویر بازتولیدپذیر تولید کند.

:::{.tip}
هنگام اجرای تصویری که با `buildImage` ساخته شده‌است، ممکن است بسته به آنچه در تصویر گنجانده‌اید با خطاهای خاصی مواجه شوید، به‌ویژه اگر کار خود را با هیچ تصویر پایه‌ای شروع نکرده باشید.

اگر با خطاهایی مشابه `getProtocolByName: does not exist (no such protocol name: tcp)` مواجه شدید، ممکن است لازم باشد محتویات `pkgs.iana-etc` را در صفت (attribute) `copyToRoot` اضافه کنید.
به همین ترتیب، اگر با خطاهایی مشابه `Error_Protocol ("certificate has unknown CA",True,UnknownCa)` مواجه شدید، ممکن است لازم باشد محتویات `pkgs.cacert` را در صفت (attribute) `copyToRoot` اضافه کنید.
:::

### Inputs {#ssec-pkgs-dockerTools-buildImage-inputs}

`buildImage` انتخابی از یک آرگومان با صفات زیر را انتظار دارد:

`name` (String)

: نام تصویر تولیدشده.

`tag` (String یا Null؛ _اختیاری_)

: برچسب تصویر تولیدشده.
  اگر `null` باشد، هش derivation / اشتقاق ساخت Nix به عنوان برچسب استفاده خواهد شد.

  _مقدار پیش‌فرض:_ `null`.

`fromImage` (Path یا Null؛ _اختیاری_)

: تاربال مخزن مربوط به یک تصویر که قرار است به عنوان تصویر پایه برای تصویر تولیدشده استفاده شود.
  این فایل باید یک تصویر معتبر Docker باشد، مانند تصویری که توسط `docker image save` صادر شده‌است، یا تصویر دیگری که با توابع ابزاری `dockerTools` ساخته شده‌است.
  این را می‌توان معادل `FROM fromImage` در یک `Dockerfile` در نظر گرفت.
  مقدار `null` را می‌توان معادل `FROM scratch` دانست.

  در صورت مشخص شدن، لایه ایجادشده توسط `buildImage` به لایه‌های تعریف‌شده در تصویر پایه اضافه می‌شود و در نتیجه تصویری با حداقل دو لایه به دست می‌آید (یک یا چند لایه از تصویر پایه و لایه ایجادشده توسط `buildImage`).
  در غیر این صورت، تصویر حاصل فقط شامل لایه واحد ایجادشده توسط `buildImage` خواهد بود.

  :::{.note}
  تنها پیکربندی **Env** از تصویر پایه به ارث برده می‌شود.
  :::

  _مقدار پیش‌فرض:_ `null`.

`fromImageName` (String یا Null؛ _اختیاری_)

: برای مشخص کردن تصویر موجود در تاربال مخزن در صورتی که حاوی چند تصویر باشد استفاده می‌شود.
  مقدار `null` به این معنی است که `buildImage` از اولین تصویر موجود در مخزن استفاده خواهد کرد.

:::{.note}
  این گزینه باید همراه با `fromImageTag` استفاده شود. استفاده از `fromImageName` به تنهایی و بدون `fromImageTag` باعث می‌شود `buildImage` از اولین تصویر موجود در مخزن استفاده کند.
  :::

  _مقدار پیش‌فرض:_ `null`.

`fromImageTag` (رشته یا Null؛ _اختیاری_)

: برای مشخص کردن تصویر موجود در فایل tarball مخزن در صورتی که حاوی چند تصویر باشد، استفاده می‌شود.
  مقدار `null` به این معنی است که `buildImage` از اولین تصویر موجود در مخزن استفاده خواهد کرد.

  :::{.note}
  این گزینه باید همراه با `fromImageName` استفاده شود. استفاده از `fromImageTag` به تنهایی و بدون `fromImageName` باعث می‌شود `buildImage` از اولین تصویر موجود در مخزن استفاده کند.
  :::

  _مقدار پیش‌فرض:_ `null`.

`copyToRoot` (مسیر، فهرستی از مسیرها، یا Null؛ _اختیاری_)

: فایل‌هایی که باید به تصویر ایجادشده اضافه شوند.
  هر چیزی که به یک مسیر تبدیل شود (مانند یک derivation) نیز می‌تواند استفاده شود.
  این را می‌توان معادل `ADD contents/ /` در یک `Dockerfile` در نظر گرفت.

  _مقدار پیش‌فرض:_ `null`.

`keepContentsDirlinks` (بولین؛ _اختیاری_)

: هنگام اضافه کردن فایل‌ها به تصویر ایجادشده (طبق آنچه توسط `copyToRoot` مشخص شده)، این صفت کنترل می‌کند که آیا پیوندهای نمادین (symlinks) به پوشه‌ها حفظ شوند یا خیر.
  اگر `false` باشد، پیوندهای نمادین به پوشه‌ها تبدیل خواهند شد.
  رفتار این گزینه مانند `rsync -k` است زمانی که `keepContentsDirlinks` برابر `false` باشد، و مانند `rsync -K` است زمانی که `keepContentsDirlinks` برابر `true` باشد.

  _مقدار پیش‌فرض:_ `false`.

`runAsRoot` (رشته یا Null؛ _اختیاری_)

: یک اسکریپت Bash که با دسترسی root درون یک ماشین مجازی (VM) که شامل لایه‌های موجودِ تصویر پایه و لایه‌ی جدید تولیدشده است (از جمله فایل‌های حاصل از `copyToRoot`)، اجرا خواهد شد.
  این اسکریپت در پوشه کاری `/` اجرا می‌شود.
  این را می‌توان معادل `RUN ...` در یک `Dockerfile` در نظر گرفت.
  مقدار `null` به این معنی است که از این مرحله در فرآیند تولید تصویر صرف‌نظر خواهد شد.

  برای نحوه کار با این صفت به [](#ex-dockerTools-buildImage-runAsRoot) مراجعه کنید.

  :::{.caution}
  استفاده از این صفت مستلزم در دسترس بودن دستگاه `kvm` است؛ بخش [`system-features`](https://nixos.org/manual/nix/stable/command-ref/conf-file.html#conf-system-features) را ببینید.
  اگر دستگاه `kvm` در دسترس نیست، باید استفاده از [`buildLayeredImage`](#ssec-pkgs-dockerTools-buildLayeredImage) یا [`streamLayeredImage`](#ssec-pkgs-dockerTools-streamLayeredImage) را مد نظر قرار دهید.
  این توابع اجازه می‌دهند اسکریپت‌ها بدون دسترسی به دستگاه `kvm` با دسترسی root اجرا شوند.
  :::

  :::{.note}
  در زمانی که اسکریپتِ موجود در `runAsRoot` اجرا می‌شود، فایل‌هایی که مستقیماً در `copyToRoot` مشخص شده‌اند در ماشین مجازی (VM) حضور خواهند داشت، اما ممکن است وابستگی‌های آن‌ها هنوز آنجا نباشند.
  کپی کردن وابستگی‌های آن‌ها به درون تصویر ایجادشده، مرحله‌ای است که پس از پایان اجرای `runAsRoot` رخ می‌دهد.
  :::

  _مقدار پیش‌فرض:_ `null`.

`extraCommands` (رشته؛ _اختیاری_)

: یک اسکریپت Bash که قبل از نهایی شدن لایه‌ی ایجادشده توسط `buildImage` اجرا خواهد شد.
  این اسکریپت روی یک پوشه کاری (مبهم) اجرا می‌شود که پس از ایجاد لایه به `/` تبدیل خواهد شد.
  این گزینه مشابه `runAsRoot` است، با این تفاوت که اسکریپت مشخص‌شده در `extraCommands` با دسترسی root اجرا **نمی‌شود** و مستلزم ایجاد ماشین مجازی (VM) نیست.
  این اسکریپت صرفاً به عنوان بخشی از ساخت derivation ای اجرا می‌شود که خروجی آن لایه‌ی ایجادشده توسط `buildImage` است.

  برای نحوه کار با این صفت و تفاوت‌های ظریف آن نسبت به `runAsRoot` به [](#ex-dockerTools-buildImage-extraCommands) مراجعه کنید.

  _مقدار پیش‌فرض:_ `""`.

`config` (مجموعه ویژگی یا Null؛ _اختیاری_)

: برای مشخص کردن پیکربندی کنتینرهایی استفاده می‌شود که از تصویر تولیدشده راه‌اندازی خواهند شد.
  باید یک مجموعه ویژگی باشد، که هر صفت همان‌طور که در [مشخصات تصویر داکر v1.3.1](https://github.com/moby/docker-image-spec/blob/v1.3.1/spec.md#image-json-field-descriptions) فهرست شده، تعریف می‌شود.

  _مقدار پیش‌فرض:_ `null`.

`architecture` (رشته؛ _اختیاری_)

: برای مشخص کردن معماری تصویر استفاده می‌شود.
  این ویژگی برای ساخت‌های چندمعماری که نیازی به کامپایل متقاطع ندارند مفید است.
  در صورت مشخص شدن، مقدار آن باید از [مشخصات پیکربندی تصویر OCI](https://github.com/opencontainers/image-spec/blob/v1.1.1/config.md#properties) پیروی کند که همچنان باید با Docker سازگار باشد.
  بر اساس مشخصات لینک‌شده، تمامی مقادیر ممکن برای `$GOARCH` در [مستندات Go](https://go.dev/doc/install/source#environment) باید معتبر باشند، اما معمولاً یکی از مقادیر `386`، `amd64`، `arm` یا `arm64` خواهد بود.

  _مقدار پیش‌فرض:_ همان مقدار از `pkgs.go.GOARCH`.

`diskSize` (عدد؛ _اختیاری_)

: اندازه دیسک را بر حسب میبی‌بایت (۱۰۲۴x۱۰۲۴ بایت) ماشین مجازی مورد استفاده برای اجرای اسکریپت مشخص‌شده در `runAsRoot` کنترل می‌کند.
  اگر `runAsRoot` برابر با `null` باشد، این صفت نادیده گرفته می‌شود.

  _مقدار پیش‌فرض:_ 1024.

`buildVMMemorySize` (عدد؛ _اختیاری_)

: مقدار حافظه بر حسب میبی‌بایت (۱۰۲۴x۱۰۲۴ بایت) اختصاص‌یافته برای ماشین مجازی مورد استفاده برای اجرای اسکریپت مشخص‌شده در `runAsRoot` را کنترل می‌کند.
  اگر `runAsRoot` برابر با `null` باشد، این صفت نادیده گرفته می‌شود.

  _مقدار پیش‌فرض:_ 512.

`created` (رشته؛ _اختیاری_)

: زمان ایجاد تصویر تولیدشده را مشخص می‌کند.
  این مقدار باید یا تاریخ و زمان قالب‌بندی‌شده طبق [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) باشد یا `"now"`، که در این صورت `buildImage` از تاریخ جاری استفاده خواهد کرد.

  برای نحوه استفاده از `"now"` به [](#ex-dockerTools-buildImage-creatednow) مراجعه کنید.

  :::{.caution}
  استفاده از `"now"` به این معنی است که تصویر تولیدشده دیگر بازتولیدپذیر نخواهد بود (زیرا تاریخ هر بار که ساخته می‌شود تغییر خواهد کرد).
  :::

  _مقدار پیش‌فرض:_ `"1970-01-01T00:00:01Z"`.

`uid` (عدد؛ _اختیاری_)

: شناسه کاربر (uid) کاربری که مالک فایل‌های بسته‌بندی‌شده در لایه جدید ساخته‌شده توسط `buildImage` خواهد بود.

  _مقدار پیش‌فرض:_ 0.

`gid` (عدد؛ _اختیاری_)

: شناسه گروه (gid) گروهی که مالک فایل‌های بسته‌بندی‌شده در لایه جدید ساخته‌شده توسط `buildImage` خواهد بود.

  _مقدار پیش‌فرض:_ 0.

`compressor` (رشته؛ _اختیاری_)

: الگوریتم مورد استفاده برای فشرده‌سازی تصویر را انتخاب می‌کند.

  _مقدار پیش‌فرض:_ `"gz"`.\
  _مقادیر ممکن:_ `"none"`، `"gz"`، `"zstd"`.

`includeNixDB` (بولین؛ _اختیاری_)

: پایگاه داده Nix در تصویر را با وابستگی‌های `copyToRoot` پر می‌کند.
  هدف اصلی امکان استفاده از دستورات Nix در کنتینر است.

  :::{.caution}
  مراقب باشید زیرا این گزینه در ترکیب با `fromImage` به خوبی کار نمی‌کند. به ویژه در یک تصویر چندلایه، تنها مسیرهای Nix مربوط به تصویر پایینی در پایگاه داده خواهند بود.

  این گزینه همچنین از ثبت مسیرهای انبار که به عنوان وابستگی یکی از مقادیر دیگر وارد تصویر شده‌اند، اما وابستگی `copyToRoot` نیستند، غفلت می‌کند.
  :::

  _مقدار پیش‌فرض:_ `false`.

`meta` (مجموعه ویژگی)

: صفت `meta` مربوط به derivation نهایی، همانند `stdenv.mkDerivation`. صفات `description`، `maintainers` و هر صفت `meta` دیگری را می‌پذیرد.

`contents` **منسوخ‌شده**

: این صفت منسوخ شده‌است و به کاربران توصیه می‌شود به جای آن از `copyToRoot` استفاده کنند.

### خروجی‌های Passthru {#ssec-pkgs-dockerTools-buildImage-passthru-outputs}

`buildImage` چند صفت [`passthru`](#chap-passthru) تعریف می‌کند:

`buildArgs` (مجموعه ویژگی)

: آرگومان ارسال‌شده به خود `buildImage`.
  این ویژگی به شما امکان می‌دهد تمام صفت‌های مشخص‌شده در آرگومان را، همان‌طور که در بالا توضیح داده شد، بررسی کنید.

`layer` (مجموعه ویژگی)

: derivation مربوط به لایه‌ای که توسط `buildImage` ایجاد شده‌است.
  این ویژگی بررسی آسان‌تر محتواهای افزوده‌شده توسط `buildImage` در تصویر تولیدشده را امکان‌پذیر می‌سازد.

`imageTag` (رشته)

: برچسب (tag) تصویر تولیدشده.
  این مقدار زمانی مفید است که هیچ برچسبی در صفت‌های آرگومان `buildImage` مشخص نشده باشد، زیرا در این صورت یک برچسب خودکار استفاده خواهد شد.
  `imageTag` به شما اجازه می‌دهد مقدار برچسب استفاده‌شده در این حالت را بازیابی کنید.

### مثال‌ها {#ssec-pkgs-dockerTools-buildImage-examples}

:::{.example #ex-dockerTools-buildImage}
# ساخت یک تصویر Docker

بسته زیر یک تصویر Docker می‌سازد که فایل اجرایی `redis-server` از بسته `redis` را اجرا می‌کند.
این تصویر Docker دارای نام `redis` و برچسب `latest` خواهد بود.

```nix
{
  dockerTools,
  buildEnv,
  redis,
}:
dockerTools.buildImage {
  name = "redis";
  tag = "latest";

  copyToRoot = buildEnv {
    name = "image-root";
    paths = [ redis ];
    pathsToLink = [ "/bin" ];
  };

  runAsRoot = ''
    mkdir -p /data
  '';

  config = {
    Cmd = [ "/bin/redis-server" ];
    WorkingDir = "/data";
    Volumes = {
      "/data" = { };
    };
  };
}
```

نتیجه‌ی ساخت این بسته یک فایل `.tar.gz` است که می‌توان آن را در Docker بارگذاری کرد:

```shell
$ nix-build
(some output removed for clarity)
building '/nix/store/yw0adm4wpsw1w6j4fb5hy25b3arr9s1v-docker-image-redis.tar.gz.drv'...
Adding layer...
tar: Removing leading `/' from member names
Adding meta...
Cooking the image...
Finished.
/nix/store/p4dsg62inh9d2ksy3c7bv58xa851dasr-docker-image-redis.tar.gz

$ docker image load -i /nix/store/p4dsg62inh9d2ksy3c7bv58xa851dasr-docker-image-redis.tar.gz
(some output removed for clarity)
Loaded image: redis:latest
```
:::

:::{.example #ex-dockerTools-buildImage-runAsRoot}
# ساخت یک تصویر داکر با `runAsRoot`

بسته زیر یک تصویر داکر همراه با فایل اجرایی `hello` از بسته `hello` می‌سازد.
این بسته از `runAsRoot` برای ایجاد یک پوشه و یک فایل در داخل تصویر استفاده می‌کند.

این روش مشابه [](#ex-dockerTools-buildImage-extraCommands) عمل می‌کند، اما به جای `extraCommands` از `runAsRoot` استفاده می‌کند.

```nix
{
  dockerTools,
  buildEnv,
  hello,
}:
dockerTools.buildImage {
  name = "hello";
  tag = "latest";

  copyToRoot = buildEnv {
    name = "image-root";
    paths = [ hello ];
    pathsToLink = [ "/bin" ];
  };

  runAsRoot = ''
    mkdir -p /data
    echo "some content" > my-file
  '';

  config = {
    Cmd = [ "/bin/hello" ];
    WorkingDir = "/data";
  };
}
```
:::

:::{.example #ex-dockerTools-buildImage-extraCommands}
# ساخت یک تصویر Docker با `extraCommands`

بسته زیر یک تصویر Docker همراه با فایل اجرایی `hello` از بسته `hello` می‌سازد.
این بسته از `extraCommands` برای ایجاد یک پوشه و یک فایل درون تصویر استفاده می‌کند.

این روش همانند [](#ex-dockerTools-buildImage-runAsRoot) عمل می‌کند، اما به جای `runAsRoot` از `extraCommands` استفاده می‌کند.
توجه داشته باشید که با `extraCommands` نمی‌توانیم مستقیماً به `/` ارجاع دهیم و باید فایل‌ها و پوشه‌ها را به گونه‌ای بسازیم که گویی از قبل روی `/` هستیم.

```nix
{
  dockerTools,
  buildEnv,
  hello,
}:
dockerTools.buildImage {
  name = "hello";
  tag = "latest";

  copyToRoot = buildEnv {
    name = "image-root";
    paths = [ hello ];
    pathsToLink = [ "/bin" ];
  };

  extraCommands = ''
    mkdir -p data
    echo "some content" > my-file
  '';

  config = {
    Cmd = [ "/bin/hello" ];
    WorkingDir = "/data";
  };
}
```
:::

:::{.example #ex-dockerTools-buildImage-creatednow}
# ساخت تصویر Docker با تنظیم تاریخ ایجاد روی زمان جاری

توجه داشته باشید که استفاده از مقدار `"now"` در صفت (attribute) `created` بازتولیدپذیری را مختل خواهد کرد.

```nix
{
  dockerTools,
  buildEnv,
  hello,
}:
dockerTools.buildImage {
  name = "hello";
  tag = "latest";

  created = "now";

  copyToRoot = buildEnv {
    name = "image-root";
    paths = [ hello ];
    pathsToLink = [ "/bin" ];
  };

  config.Cmd = [ "/bin/hello" ];
}
```

پس از درون‌ریزی تاربال مخزن ایجادشده با Docker، رابط خط فرمان (CLI) آن تاریخی معقول را نمایش داده و تصاویر را طبق انتظار مرتب می‌کند:

```shell
$ docker image ls
REPOSITORY   TAG      IMAGE ID       CREATED              SIZE
hello        latest   de2bf4786de6   About a minute ago   25.2MB
```
:::

## buildLayeredImage {#ssec-pkgs-dockerTools-buildLayeredImage}

`buildLayeredImage` در لایه‌ی زیرین از [`streamLayeredImage`](#ssec-pkgs-dockerTools-streamLayeredImage) برای ساخت یک tarball مخزنِ فشرده‌شده و سازگار با Docker استفاده می‌کند.
در واقع، `buildLayeredImage` اسکریپت ایجادشده توسط `streamLayeredImage` را اجرا می‌کند تا تصویر فشرده‌شده را در انبار نیکس (Nix store) ذخیره کند.
`buildLayeredImage` از همان گزینه‌های `streamLayeredImage` پشتیبانی می‌کند؛ برای جزئیات بیشتر به [`streamLayeredImage`](#ssec-pkgs-dockerTools-streamLayeredImage) مراجعه کنید.

:::{.note}
با وجود نام مشابه، [`buildImage`](#ssec-pkgs-dockerTools-buildImage) کاملاً متفاوت از `buildLayeredImage` و `streamLayeredImage` عمل می‌کند.

اگرچه برخی از آرگومان‌ها ممکن است مرتبط به نظر برسند، اما نمی‌توان آن‌ها را به جای یکدیگر استفاده کرد.
:::

شما می‌توانید نتیجه‌ی این تابع را با دستور `docker image load` در Docker بارگذاری کنید.
برای مشاهده‌ی نحوه‌ی انجام این کار، [](#ex-dockerTools-buildLayeredImage-hello) را ببینید.

### نمونه‌ها {#ssec-pkgs-dockerTools-buildLayeredImage-examples}

:::{.example #ex-dockerTools-buildLayeredImage-hello}
# ساخت یک تصویر لایه‌ای Docker

بسته‌ی زیر یک تصویر لایه‌ای Docker می‌سازد که فایل اجرایی `hello` را از بسته‌ی `hello` اجرا می‌کند.
تصویر Docker دارای نام `hello` و برچسب `latest` خواهد بود.

```nix
{ dockerTools, hello }:
dockerTools.buildLayeredImage {
  name = "hello";
  tag = "latest";

  contents = [ hello ];

  config.Cmd = [ "/bin/hello" ];
}
```

نتیجه‌ی ساخت این بسته یک فایل `.tar.gz` است که می‌توان آن را در Docker بارگذاری کرد:

```shell
$ nix-build
(some output removed for clarity)
building '/nix/store/bk8bnrbw10nq7p8pvcmdr0qf57y6scha-hello.tar.gz.drv'...
No 'fromImage' provided
Creating layer 1 from paths: ['/nix/store/i93s7xxblavsacpy82zdbn4kplsyq48l-libunistring-1.1']
Creating layer 2 from paths: ['/nix/store/ji01n9vinnj22nbrb86nx8a1ssgpilx8-libidn2-2.3.4']
Creating layer 3 from paths: ['/nix/store/ldrslljw4rg026nw06gyrdwl78k77vyq-xgcc-12.3.0-libgcc']
Creating layer 4 from paths: ['/nix/store/9y8pmvk8gdwwznmkzxa6pwyah52xy3nk-glibc-2.38-27']
Creating layer 5 from paths: ['/nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1']
Creating layer 6 with customisation...
Adding manifests...
Done.
/nix/store/hxcz7snvw7f8rzhbh6mv8jq39d992905-hello.tar.gz

$ docker image load -i /nix/store/hxcz7snvw7f8rzhbh6mv8jq39d992905-hello.tar.gz
(some output removed for clarity)
Loaded image: hello:latest
```
:::

## streamLayeredImage {#ssec-pkgs-dockerTools-streamLayeredImage}

`streamLayeredImage` یک **اسکریپت** می‌سازد که هنگام اجرا، یک تاربال مخزن سازگار با Docker حاوی یک تصویر واحد را به خروجی استاندارد (stdout) استریم می‌کند و از چندین لایه برای بهبود اشتراک‌گذاری بین تصاویر استفاده می‌نماید.
این بدان معناست که `streamLayeredImage` یک تصویر را خروجی نمی‌دهد تا در انبار نیکس (Nix store) قرار گیرد، بلکه فقط اسکریپتی را می‌سازد که تصویر را تولید می‌کند؛ این امر باعث صرفه‌جویی در ورودی/خروجی (IO) و فضای دیسک/کش می‌شود، به‌ویژه در مورد تصاویر بزرگ.

می‌توانید نتیجه این تابع را با دستور `docker image load` در Docker بارگذاری کنید.
برای مشاهده نحوه انجام این کار، [](#ex-dockerTools-streamLayeredImage-hello) را ببینید.

برای این تابع، شما یک [مسیر انبار](https://nixos.org/manual/nix/stable/store/store-path) یا فهرستی از مسیرهای انبار را مشخص می‌کنید تا به تصویر اضافه شوند، و توابع به طور خودکار هرگونه وابستگی‌های آن مسیرها را در تصویر می‌گنجانند.
این تابع تلاش می‌کند به ازای هر شیء موجود در انبار نیکس (Nix store) که باید به تصویر اضافه شود، یک لایه ایجاد کند.
در صورتی که تعداد اشیاء قابل درج از تعداد لایه‌های موجود بیشتر باشد، تابع ["محبوب‌ترین"](https://github.com/NixOS/nixpkgs/tree/release-23.11/pkgs/build-support/references-by-popularity) اشیاء را در لایه‌های مجزای خود قرار می‌دهد و تمام اشیاء باقی‌مانده را در یک لایه واحد گروه‌بندی می‌کند.

یک لایه اضافی با پیوندهای نمادین (symlinks) به مسیرهای انباری که برای گنجانده شدن در تصویر مشخص کرده‌اید، ایجاد خواهد شد.
این پیوندهای نمادین با [`symlinkJoin`](#trivial-builder-symlinkJoin) ساخته می‌شوند، بنابراین در ریشه تصویر قرار خواهند گرفت.
برای درک نحوه چیدمان این پیوندهای نمادین در تصویر تولیدشده، [](#ex-dockerTools-streamLayeredImage-exploringlayers) را ببینید.

`streamLayeredImage` اجازه می‌دهد هنگام ایجاد لایه اضافی حاوی پیوندهای نمادین، اسکریپت‌هایی اجرا شوند تا رفتار سفارشی بتواند بر نتایج نهایی تصویر تأثیر بگذارد (به مستندات صفات `extraCommands` و `fakeRootCommands` مراجعه کنید).

تاربال مخزن حاصل، یک تصویر واحد را طبق آنچه توسط صفات `name` و `tag` مشخص شده‌است فهرست می‌کند.
به طور پیش‌فرض، آن تصویر از یک تاریخ ایجاد ایستا استفاده می‌کند (مستندات صفات `created` و `mtime` را ببینید).
این امر به تابع امکان می‌دهد تصاویر بازتولیدپذیر تولید کند.

### Inputs {#ssec-pkgs-dockerTools-streamLayeredImage-inputs}

`streamLayeredImage` یک آرگومان با صفات زیر دریافت می‌کند:

`name` (رشته / String)

: نام تصویر تولیدشده.

`tag` (رشته یا Null؛ _اختیاری_)

: تگ تصویر تولیدشده.
  اگر `null` باشد، هش derivation نیکس به عنوان تگ استفاده خواهد شد.

  _مقدار پیش‌فرض:_ `null`.

`fromImage`(مسیر یا Null؛ _اختیاری_)

: تاربال مخزن مربوط به تصویری که به عنوان پایه برای تصویر تولیدشده استفاده می‌شود.
  این باید یک تصویر معتبر Docker باشد، مانند تصویری که توسط `docker image save` صادر شده‌است، یا تصویر دیگری که با توابع کمکی `dockerTools` ساخته شده باشد.
  این را می‌توان معادل `FROM fromImage` در یک `Dockerfile` در نظر گرفت.
  مقدار `null` را می‌توان معادل `FROM scratch` در نظر گرفت.

  در صورت مشخص شدن، لایه‌های ایجادشده به لایه‌های تعریف‌شده در تصویر پایه اضافه خواهند شد.

  _مقدار پیش‌فرض:_ `null`.

`contents` (مسیر یا فهرستی از مسیرها؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-contents}

: پوشه‌هایی که محتوای آن‌ها به تصویر تولیدشده اضافه خواهد شد.
  مواردی که به مسیر تبدیل می‌شوند (مانند یک derivation) نیز قابل استفاده هستند.
  این را می‌توان معادل `ADD contents/ /` در یک `Dockerfile` در نظر گرفت.

تمام محتویات مشخص‌شده در `contents` به عنوان لایه نهایی در تصویر تولیدشده اضافه خواهند شد.
  آن‌ها به صورت پیوند به فایل‌های واقعی (به عنوان مثال، پیوند به مسیرهای انبار) اضافه می‌شوند.
  فایل‌های واقعی در لایه‌های قبلی اضافه خواهند شد.

  _مقدار پیش‌فرض:_ `[]`

`config` (مجموعه ویژگی یا مقدار تهی؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-config}

: برای مشخص کردن پیکربندی کانتینرهایی که از روی تصویر تولیدشده راه‌اندازی می‌شوند، استفاده می‌شود.
  باید یک مجموعه ویژگی باشد، به‌طوری که هر صفت همان‌طور که در [مشخصات تصویر Docker نسخه v1.3.0](https://github.com/moby/moby/blob/46f7ab808b9504d735d600e259ca0723f76fb164/image/spec/spec.md#image-json-field-descriptions) فهرست شده، باشد.

  اگر از هر بسته‌ای به‌طور مستقیم در `config` استفاده شود، آن بسته‌ها به‌طور خودکار در تصویر تولیدشده گنجانده می‌شوند.
  برای مشاهده یک نمونه، [](#ex-dockerTools-streamLayeredImage-configclosure) را ببینید.

  _مقدار پیش‌فرض:_ `null`.

`architecture` (رشته؛ _اختیاری_)

: برای مشخص کردن معماری تصویر استفاده می‌شود.
  این گزینه برای ساخت‌های چندمعماری که نیازی به کامپایل متقاطع ندارند مفید است.
  در صورت مشخص شدن، مقدار آن باید از [مشخصات پیکربندی تصویر OCI](https://github.com/opencontainers/image-spec/blob/main/config.md#properties) پیروی کند که همچنان باید با Docker سازگار باشد.
  طبق مشخصات پیوندشده، تمام مقادیر ممکن برای `$GOARCH` در [مستندات Go](https://go.dev/doc/install/source#environment) باید معتبر باشند، اما معمولاً یکی از مقادیر `386`، `amd64`، `arm` یا `arm64` خواهد بود.

  _مقدار پیش‌فرض:_ همان مقدار از `pkgs.go.GOARCH`.

`created` (رشته؛ _اختیاری_)

: زمان ایجاد تصویر تولیدشده را مشخص می‌کند.
  این تاریخ برای متاداده تصویر استفاده خواهد شد.
  این مقدار باید یک تاریخ و زمان قالب‌بندی‌شده طبق [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) یا `"now"` باشد، که در صورت انتخاب `"now"` از تاریخ فعلی استفاده می‌شود.

  :::{.caution}
  استفاده از `"now"` به این معنی است که تصویر تولیدشده دیگر بازتولیدپذیر نخواهد بود (زیرا تاریخ هر بار که ساخته می‌شود تغییر خواهد کرد).
  :::

  _مقدار پیش‌فرض:_ `"1970-01-01T00:00:01Z"`.

`mtime` (رشته؛ _اختیاری_)

: زمان مورد استفاده برای برچسب زمانی تغییر (modification timestamp) فایل‌ها در لایه‌های تصویر تولیدشده را مشخص می‌کند.
  این مقدار باید یک تاریخ و زمان قالب‌بندی‌شده طبق [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) یا `"now"` باشد، که در صورت انتخاب `"now"` از تاریخ فعلی استفاده می‌شود.

  :::{.caution}
  استفاده از یک تاریخ غیرثابت باعث می‌شود لایه‌های ساخته‌شده هر بار هش متفاوتی داشته باشند و از حذف داده‌های تکراری (deduplication) جلوگیری شود.
  استفاده از `"now"` همچنین به این معنی است که تصویر تولیدشده دیگر بازتولیدپذیر نخواهد بود (زیرا تاریخ هر بار که ساخته می‌شود تغییر خواهد کرد).
  :::

  _مقدار پیش‌فرض:_ `"1970-01-01T00:00:01Z"`.

`uid` (عدد؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-uid}
`gid` (عدد؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-gid}
`uname` (رشته؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-uname}
`gname` (رشته؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-gname}

: اعتبارنامه‌ها برای مالکیت انبار نیکس (Nix store).
  می‌تواند به مقادیری مانند `1000` / `1000` / `"user"` / `"user"` بازنویسی شود تا امکان ساخت کانتینری فراهم شود که در آن بتوان از Nix به عنوان یک کاربر بدون دسترسی ویژه در حالت تک‌کاربره استفاده کرد.

  _مقدار پیش‌فرض:_ `0` / `0` / `"root"` / `"root"`

`maxLayers` (عدد؛ _اختیاری_) []{#dockerTools-buildLayeredImage-arg-maxLayers}

: بیشترین تعداد لایه‌هایی که توسط تصویر تولیدشده استفاده خواهد شد.
  اگر یک `fromImage` مشخص شده باشد، تعداد لایه‌های استفاده‌شده توسط `fromImage` از `maxLayers` کسر خواهد شد تا اطمینان حاصل شود که تصویر تولیدشده حداکثر دارای `maxLayers` لایه خواهد بود.

  :::{.caution}
  بسته به ابزار/زمان اجرا (runtime) که تصویر در آن استفاده خواهد شد، ممکن است محدودیتی برای تعداد لایه‌هایی که یک تصویر می‌تواند داشته باشد وجود داشته باشد.
  برای Docker، [این موضوع در GitHub](https://github.com/docker/docs/issues/8230) را ببینید.
  :::

  _مقدار پیش‌فرض:_ 100.

`extraCommands` (String؛ _اختیاری_)

: یک اسکریپت Bash که در بافت (context) لایه‌ی ایجادشده با محتویات مشخص‌شده توسط `contents` اجرا خواهد شد.
  در زمانی که این اسکریپت اجرا می‌شود، تنها محتویاتی که مستقیماً توسط `contents` مشخص شده‌اند به عنوان پیوند در دسترس خواهند بود.

  _مقدار پیش‌فرض:_ `""`.

`fakeRootCommands` (String؛ _اختیاری_)

: یک اسکریپت Bash که در بافت لایه‌ی ایجادشده با محتویات مشخص‌شده توسط `contents` اجرا خواهد شد.
  در طول فرآیند تولید آن لایه، اگر اسکریپت در `extraCommands` مشخص شده باشد، ابتدا اجرا خواهد شد.
  پس از آن، وارد یک محیط {manpage}`fakeroot(1)` می‌شود.
  اسکریپت مشخص‌شده در `fakeRootCommands` درون محیط fakeroot اجرا می‌شود، و سپس لایه از دید فایل‌های داخل محیط fakeroot تولید می‌گردد.

  این ویژگی برای تغییر مالکان فایل‌های درون لایه (مثلاً با اجرای `chown`) یا انجام هرگونه عملیات دارای دسترسی ویژه مربوط به دستکاری فایل مفید است (به طور پیش‌فرض، مالک تمام فایل‌های درون لایه root خواهد بود و محیط ساخت دسترسی کافی برای انجام مستقیم عملیات‌های دارای دسترسی ویژه روی این فایل‌ها را ندارد).

  برای جزئیات بیشتر، صفحه راهنمای {manpage}`fakeroot(1)` را ببینید.

  :::{.caution}
  به دلیل نحوه کارکرد fakeroot، باینری‌های ایستا نمی‌توانند عملیات فایل دارای دسترسی ویژه را در `fakeRootCommands` انجام دهند، مگر اینکه `enableFakechroot` روی `true` تنظیم شده باشد.
  :::

  _مقدار پیش‌فرض:_ `""`.

`enableFakechroot` (Boolean؛ _اختیاری_)

: به طور پیش‌فرض، اسکریپت مشخص‌شده در `fakeRootCommands` فقط درون یک محیط fakeroot اجرا می‌شود.
  اگر `enableFakechroot` برابر با `true` باشد، پیش از اجرای اسکریپت در `fakeRootCommands` یک محیط chroot کامل‌تر با استفاده از [`proot`](https://proot-me.github.io/) ایجاد خواهد شد.
  فایل‌های موجود در انبار Nix در دسترس خواهند بود.
  این کار اجازه می‌دهد اسکریپت‌هایی که عملیات نصب را در `/` انجام می‌دهند، مطابق انتظار کار کنند.
  این را می‌توان معادل `RUN ...` در یک `Dockerfile` در نظر گرفت.

  _مقدار پیش‌فرض:_ `false`

`includeStorePaths` (Boolean؛ _اختیاری_)

: فایل‌های مشخص‌شده در `contents` درون لایه‌ها در تصویر تولیدشده قرار می‌گیرند.
  اگر `includeStorePaths` برابر با `false` باشد، فایل‌های واقعی در تصویر تولیدشده قرار نخواهند گرفت و در عوض فقط پیوندها به آن‌ها اضافه خواهند شد.
  تنظیم این گزینه روی `false` **توصیه نمی‌شود**، مگر اینکه ابزار دیگری برای درج مسیرهای انبار از طرق دیگر (مانند bind mount کردن انبار هاست) هنگام اجرای کنتینرها با تصویر تولیدشده داشته باشید.
  اگر هیچ ابزار اضافی ارائه ندهید، تصویر تولیدشده به درستی اجرا نخواهد شد.

  برای درک تأثیر تنظیم `includeStorePaths` روی `false`، بخش [](#ex-dockerTools-streamLayeredImage-exploringlayers) را ببینید.

  _مقدار پیش‌فرض:_ `true`

`includeNixDB` (Boolean؛ _اختیاری_)

: پایگاه داده nix را در تصویر با وابستگی‌های `copyToRoot` پر می‌کند.
  هدف اصلی، امکان استفاده از دستورات nix در کنتینر است.

:::{.caution}
  توجه داشته باشید که این گزینه همراه با `fromImage` به‌خوبی کار نمی‌کند. به‌ویژه، در یک تصویر چندلایه‌ای، تنها مسیرهای Nix مربوط به تصویر پایین‌تر در پایگاه داده وجود خواهند داشت.

  این کار همچنین ثبت مسیرهای انبار را که به عنوان وابستگی یکی از مقادیر دیگر وارد تصویر شده‌اند، اما وابستگی `copyToRoot` نیستند، ندیده می‌گیرد.
  :::

  _مقدار پیش‌فرض:_ `false`.

`meta` (مجموعه ویژگی)

: صفت `meta` در derivation حاصل، مانند `stdenv.mkDerivation`. گزینه‌های `description`، `maintainers` و هر صفت `meta` دیگری را می‌پذیرد.

`passthru` (مجموعه ویژگی؛ _اختیاری_)

: از این گزینه برای انتقال هر صفتی به عنوان [`passthru`](#chap-passthru) برای derivation حاصل استفاده کنید.

  _مقدار پیش‌فرض:_ `{}`

### خروجی‌های Passthru {#ssec-pkgs-dockerTools-streamLayeredImage-passthru-outputs}

`streamLayeredImage` همچنین صفت‌های [`passthru`](#chap-passthru) خود را تعریف می‌کند:

`imageTag` (رشته)

: تگ تصویر تولیدشده.
  این موضوع زمانی مفید است که هیچ تگی در صفت‌های آرگومان ورودی به تابع مشخص نشده باشد، زیرا در این صورت یک تگ خودکار استفاده خواهد شد.
  `imageTag` به شما اجازه می‌دهد مقدار تگ استفاده‌شده در این حالت را بازیابی کنید.

### مثال‌ها {#ssec-pkgs-dockerTools-streamLayeredImage-examples}

:::{.example #ex-dockerTools-streamLayeredImage-hello}
# استریم کردن یک تصویر لایه‌ای Docker

بسته زیر یک **اسکریپت** می‌سازد که هنگام اجرا، یک تصویر لایه‌ای Docker را که فایل اجرایی `hello` از بسته `hello` را اجرا می‌کند، استریم خواهد کرد.
تصویر Docker دارای نام `hello` و تگ `latest` خواهد بود.

```nix
{ dockerTools, hello }:
dockerTools.streamLayeredImage {
  name = "hello";
  tag = "latest";

  contents = [ hello ];

  config.Cmd = [ "/bin/hello" ];
}
```

نتیجه‌ی ساخت این بسته یک اسکریپت است.
اجرای این اسکریپت و هدایت خروجی آن به `docker image load` همان تصویری را به شما می‌دهد که در [](#ex-dockerTools-buildLayeredImage-hello) ساخته شده بود.
توجه داشته باشید که در این حالت، تصویر هرگز به انبار نیکس (Nix store) اضافه نمی‌شود، بلکه به‌طور مستقیم به Docker استریم می‌شود.

```shell
$ nix-build
(output removed for clarity)
/nix/store/wsz2xl8ckxnlb769irvq6jv1280dfvxd-stream-hello

$ /nix/store/wsz2xl8ckxnlb769irvq6jv1280dfvxd-stream-hello | docker image load
No 'fromImage' provided
Creating layer 1 from paths: ['/nix/store/i93s7xxblavsacpy82zdbn4kplsyq48l-libunistring-1.1']
Creating layer 2 from paths: ['/nix/store/ji01n9vinnj22nbrb86nx8a1ssgpilx8-libidn2-2.3.4']
Creating layer 3 from paths: ['/nix/store/ldrslljw4rg026nw06gyrdwl78k77vyq-xgcc-12.3.0-libgcc']
Creating layer 4 from paths: ['/nix/store/9y8pmvk8gdwwznmkzxa6pwyah52xy3nk-glibc-2.38-27']
Creating layer 5 from paths: ['/nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1']
Creating layer 6 with customisation...
Adding manifests...
Done.
(some output removed for clarity)
Loaded image: hello:latest
```
:::

:::{.example #ex-dockerTools-streamLayeredImage-exploringlayers}
# بررسی لایه‌ها در تصویری ساخته‌شده با `streamLayeredImage`

بسته زیر را در نظر بگیرید که یک تصویر Docker لایه‌ای را با بسته `hello` می‌سازد.

```nix
{ dockerTools, hello }:
dockerTools.streamLayeredImage {
  name = "hello";
  contents = [ hello ];
}
```

بسته `hello` به ۴ بسته دیگر وابسته است:

```shell
$ nix-store --query -R $(nix-build -A hello)
/nix/store/i93s7xxblavsacpy82zdbn4kplsyq48l-libunistring-1.1
/nix/store/ji01n9vinnj22nbrb86nx8a1ssgpilx8-libidn2-2.3.4
/nix/store/ldrslljw4rg026nw06gyrdwl78k77vyq-xgcc-12.3.0-libgcc
/nix/store/9y8pmvk8gdwwznmkzxa6pwyah52xy3nk-glibc-2.38-27
/nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1
```

این بدان معناست که تمامی این بسته‌ها در تصویر تولیدشده توسط `streamLayeredImage` گنجانده خواهند شد.
این کار هر بسته را در لایه‌ی مجزای خود قرار می‌دهد که در مجموع شامل ۵ لایه همراه با فایل‌های واقعی درون آن‌ها خواهد بود.
یک لایه‌ی نهایی تنها با پیوندهای نمادین (symlinks) برای بسته‌ی `hello` ایجاد خواهد شد.

تصویر تولیدشده دارای ساختار پوشه‌ی زیر خواهد بود (برخی از پوشه‌ها برای خوانایی بیشتر خلاصه شده‌اند):

```
├── bin
│   └── hello → /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1/bin/hello
├── nix
│   └── store
│       ├─⊕ 9y8pmvk8gdwwznmkzxa6pwyah52xy3nk-glibc-2.38-27
│       ├─⊕ i93s7xxblavsacpy82zdbn4kplsyq48l-libunistring-1.1
│       ├─⊕ ji01n9vinnj22nbrb86nx8a1ssgpilx8-libidn2-2.3.4
│       ├─⊕ ldrslljw4rg026nw06gyrdwl78k77vyq-xgcc-12.3.0-libgcc
│       └─⊕ zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1
└── share
    ├── info
    │   └── hello.info → /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1/share/info/hello.info
    ├─⊕ locale
    └── man
        └── man1
            └── hello.1.gz → /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1/share/man/man1/hello.1.gz
```

هر کدام از بسته‌های موجود در `/nix/store` از لایه‌ای در تصویر می‌آیند.
لایه نهایی پوشه‌های `/bin` و `/share` را اضافه می‌کند، اما آن‌ها تنها حاوی پیوندها به فایل‌های واقعی در `/nix/store` هستند.

اگر بسته ما مقدار `includeStorePaths` را برابر `false` تنظیم کند، در نهایت تنها لایه نهایی شامل پیوندها را خواهیم داشت، اما فایل‌های واقعی در تصویر وجود نخواهند داشت:

```nix
{ dockerTools, hello }:
dockerTools.streamLayeredImage {
  name = "hello";
  contents = [ hello ];
  includeStorePaths = false;
}
```

پس از ساخت این بسته، تصویر ساختار پوشه زیر را خواهد داشت:

```
├── bin
│   └── hello → /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1/bin/hello
└── share
    ├── info
    │   └── hello.info → /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1/share/info/hello.info
    ├─⊕ locale
    └── man
        └── man1
            └── hello.1.gz → /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1/share/man/man1/hello.1.gz
```

توجه داشته باشید که چگونه پیوندها به مسیرهای درون `/nix/store` اشاره می‌کنند، اما در خود تصویر گنجانده نشده‌اند.
به همین دلیل است که هنگام استفاده از `includeStorePaths` به ابزار اضافی نیاز دارید:
در غیر این صورت، کنتینری که از چنین تصویری ساخته شده باشد، هیچ‌یک از فایل‌های مورد نیاز خود برای اجرا را پیدا نخواهد کرد.
:::

::: {.example #ex-dockerTools-streamLayeredImage-configclosure}
# ساخت یک تصویر Docker لایه‌بندی‌شده با بسته‌ها مستقیماً در `config`

کلوژر `config` به‌طور خودکار در تصویر تولیدشده گنجانده می‌شود.
بسته زیر روشی فشرده‌تر برای ایجاد همان خروجی تولیدشده در [](#ex-dockerTools-streamLayeredImage-hello) را نشان می‌دهد.

```nix
{
  dockerTools,
  hello,
  lib,
}:
dockerTools.streamLayeredImage {
  name = "hello";
  tag = "latest";
  config.Cmd = [ "${lib.getExe hello}" ];
}
```
:::

[]{#ssec-pkgs-dockerTools-fetchFromRegistry}
## pullImage {#ssec-pkgs-dockerTools-pullImage}

این تابع مشابه دستور `docker image pull` است، به این معنی که می‌توان از آن برای دریافت (pull) یک تصویر Docker از یک مخزن ثبت (registry) که [Docker Registry HTTP API V2](https://distribution.github.io/distribution/spec/api/) را پیاده‌سازی می‌کند، استفاده کرد.
به‌طور پیش‌فرض، از مخزن ثبت `docker.io` استفاده می‌شود.

تصویر به صورت یک فایل tarball غیرفشرده و سازگار با Docker دانلود خواهد شد که برای استفاده با سایر توابع `dockerTools` مانند [`buildImage`](#ssec-pkgs-dockerTools-buildImage)، [`buildLayeredImage`](#ssec-pkgs-dockerTools-buildLayeredImage) و [`streamLayeredImage`](#ssec-pkgs-dockerTools-streamLayeredImage) مناسب است.

این تابع مستلزم مشخص کردن دو نوع متفاوت از هش‌ها/دایجست‌ها (digests) است:

- یکی از آن‌ها برای شناسایی یک تصویر منحصربه‌فرد در مخزن ثبت استفاده می‌شود (مستندات صفت (attribute) `imageDigest` را ببینید).
- دیگری توسط Nix استفاده می‌شود تا اطمینان حاصل شود که محتوای خروجی تغییر نکرده‌است (مستندات صفت (attribute) `sha256` را ببینید).

هر دو هش مورد نیاز هستند زیرا باید محتوایی را به‌طور منحصربه‌فرد در دو سیستم کاملاً متفاوت (مخزن ثبت Docker و انبار نیکس (Nix store)) شناسایی کنند، اما مقادیر آن‌ها یکسان نخواهد بود.
برای ابزاری که می‌تواند به جمع‌آوری این مقادیر کمک کند، [](#ex-dockerTools-pullImage-nixprefetchdocker) را ببینید.

### ورودی‌ها {#ssec-pkgs-dockerTools-pullImage-inputs}

`pullImage` انتظار یک آرگومان تنها با صفات زیر را دارد:

`imageName` (رشته)

: نام تصویری که باید دانلود شود، و همچنین نقطه پایانی (endpoint) مخزن ثبت را مشخص می‌کند.
  به‌طور پیش‌فرض، از مخزن ثبت `docker.io` استفاده می‌شود.
  برای مشخص کردن یک مخزن ثبت متفاوت، نقطه پایانی را پیش از `imageName` قرار دهید که با یک اسلش (`/`) جدا می‌شود.
  برای نحوه انجام این کار [](#ex-dockerTools-pullImage-differentregistry) را ببینید.

`imageDigest` (رشته)

: دایجست تصویری که باید دانلود شود را مشخص می‌کند.

  :::{.tip}
  **چرا نمی‌توانم تگی را برای دریافت (pull) مشخص کنم و در عوض باید از یک دایجست استفاده کنم؟ **

  تگ‌ها اغلب به‌روزرسانی می‌شوند تا به محتواهای متفاوت تصویر اشاره کنند.
  رایج‌ترین نمونه، تگ `latest` است که معمولاً هر زمان نسخه جدیدتری از تصویر در دسترس باشد به‌روزرسانی می‌شود.

  تگ تصویر برای تضمین عدم تغییر محتوای یک تصویر کافی نیست، اما یک دایجست این موضوع را تضمین می‌کند.
  ارائه یک دایجست کمک می‌کند اطمینان حاصل شود که حتی در صورت انتشار نسخه‌های جدیدتر یک تصویر، همچنان می‌توانید همان کد Nix را ساخت (Build) کنید و همان خروجی را دریافت کنید.
  :::

`sha256` (رشته)

: هش تصویر پس از دانلود آن.
  در درون، این به صفت (attribute) [`outputHash`](https://nixos.org/manual/nix/stable/language/advanced-attributes#adv-attr-outputHash) از derivation / اشتقاق ساخت حاصل منتقل می‌شود.
  این کار برای ارائه تضمین به Nix مبنی بر عدم تغییر محتوای تصویر لازم است، زیرا Nix از مقدار موجود در `imageDigest` پشتیبانی نمی‌کند.

`finalImageName` (رشته؛ _اختیاری_)

: نامی را مشخص می‌کند که پس از دانلود تصویر برای آن استفاده خواهد شد.
  این مورد فقط پس از دانلود تصویر اعمال می‌شود و برای شناسایی تصویر دانلود شونده در مخزن ثبت استفاده نمی‌شود.
  به جای آن از `imageName` استفاده کنید.

  _مقدار پیش‌فرض:_ همان مقداری که در `imageName` مشخص شده‌است.

`finalImageTag` (رشته؛ _اختیاری_)

: تگی را مشخص می‌کند که پس از دانلود تصویر برای آن استفاده خواهد شد.
  این مورد فقط پس از دانلود تصویر اعمال می‌شود و برای شناسایی تصویر دانلود شونده در مخزن ثبت استفاده نمی‌شود.

  _مقدار پیش‌فرض:_ `"latest"`.

`os` (رشته؛ _اختیاری_)

: سیستم‌عامل تصویری که باید دریافت شود را مشخص می‌کند.
  در صورت مشخص شدن، مقدار آن باید از [مشخصات پیکربندی تصویر OCI](https://github.com/opencontainers/image-spec/blob/main/config.md#properties) پیروی کند که همچنان باید با Docker سازگار باشد.
  طبق مشخصات پیوندشده، تمام مقادیر ممکن برای `$GOOS` در [مستندات Go](https://go.dev/doc/install/source#environment) باید معتبر باشند، اما معمولاً یکی از مقادیر `darwin` یا `linux` خواهد بود.

  _مقدار پیش‌فرض:_ `"linux"`.

`arch` (رشته؛ _اختیاری_)

: معماری تصویری که باید دریافت شود را مشخص می‌کند.
  در صورت مشخص شدن، مقدار آن باید از [مشخصات پیکربندی تصویر OCI](https://github.com/opencontainers/image-spec/blob/main/config.md#properties) پیروی کند که همچنان باید با Docker سازگار باشد.
  طبق مشخصات پیوندشده، تمام مقادیر ممکن برای `$GOARCH` در [مستندات Go](https://go.dev/doc/install/source#environment) باید معتبر باشند، اما معمولاً یکی از مقادیر `386`، `amd64`، `arm` یا `arm64` خواهد بود.

  _مقدار پیش‌فرض:_ همان مقدار `pkgs.go.GOARCH`.

`tlsVerify` (بولی؛ _اختیاری_)

: برای فعال یا غیرفعال کردن اعتبارسنجی گواهی‌نامه‌های اچ‌تی‌تی‌پی‌اس (HTTPS) و TLS هنگام ارتباط با مخزن Docker انتخاب‌شده استفاده می‌شود.
  تنظیم این گزینه روی `false` باعث می‌شود `pullImage` از طریق اچ‌تی‌تی‌پی (HTTP) به مخزن متصل شود.

  _مقدار پیش‌فرض:_ `true`.

`name` (رشته؛ _اختیاری_)

: نامی که برای خروجی در مسیر انبار نیکس (Nix store) استفاده می‌شود.

  _مقدار پیش‌فرض:_ مقداری مشتق‌شده از `finalImageName` و `finalImageTag` با جایگزینی برخی نمادها.
  توصیه می‌شود با مقدار پیش‌فرض به عنوان یک مقدار مبهم رفتار کنید.

### نمونه‌ها {#ssec-pkgs-dockerTools-pullImage-examples}

::: {.example #ex-dockerTools-pullImage-niximage}
# دریافت تصویر Docker مربوط به nixos/nix از مخزن پیش‌فرض

این نمونه، [تصویر `nixos/nix`](https://hub.docker.com/r/nixos/nix) را دریافت کرده و آن را در انبار نیکس (Nix store) ذخیره می‌کند.

```nix
{ dockerTools }:
dockerTools.pullImage {
  imageName = "nixos/nix";
  imageDigest = "sha256:b8ea88f763f33dfda2317b55eeda3b1a4006692ee29e60ee54ccf6d07348c598";
  finalImageName = "nix";
  finalImageTag = "2.19.3";
  hash = "sha256-zRwlQs1FiKrvHPaf8vWOR/Tlp1C5eLn1d9pE4BZg3oA=";
}
```
:::

::: {.example #ex-dockerTools-pullImage-differentregistry}
# دریافت تصویر Docker nixos/nix از یک رجیستری مشخص

این مثال [تصویر `coreos/etcd`](https://quay.io/repository/coreos/etcd) را از رجیستری `quay.io` دریافت می‌کند.

```nix
{ dockerTools }:
dockerTools.pullImage {
  imageName = "quay.io/coreos/etcd";
  imageDigest = "sha256:24a23053f29266fb2731ebea27f915bb0fb2ae1ea87d42d890fe4e44f2e27c5d";
  finalImageName = "etcd";
  finalImageTag = "v3.5.11";
  hash = "sha256-Myw+85f2/EVRyMB3axECdmQ5eh9p1q77FWYKy8YpRWU=";
}
```
:::

::: {.example #ex-dockerTools-pullImage-nixprefetchdocker}
# یافتن مقادیر دایجشت و هش برای استفاده در `dockerTools.pullImage`

از آنجا که [`dockerTools.pullImage`](#ssec-pkgs-dockerTools-pullImage) به دو هش متفاوت نیاز دارد، می‌توان ابزار `nix-prefetch-docker` را برای یافتن مقادیر این هش‌ها اجرا کرد.
این ابزار متنی را برای یک مجموعه ویژگی خروجی می‌دهد که می‌توانید آن را مستقیماً به `pullImage` پاس دهید.

```shell
$ nix run nixpkgs#nix-prefetch-docker -- --image-name nixos/nix --image-tag 2.19.3 --arch amd64 --os linux
(some output removed for clarity)
Writing manifest to image destination
-> ImageName: nixos/nix
-> ImageDigest: sha256:498fa2d7f2b5cb3891a4edf20f3a8f8496e70865099ba72540494cd3e2942634
-> FinalImageName: nixos/nix
-> FinalImageTag: latest
-> ImagePath: /nix/store/4mxy9mn6978zkvlc670g5703nijsqc95-docker-image-nixos-nix-latest.tar
-> ImageHash: 1q6cf2pdrasa34zz0jw7pbs6lvv52rq2aibgxccbwcagwkg2qj1q
{
  imageName = "nixos/nix";
  imageDigest = "sha256:498fa2d7f2b5cb3891a4edf20f3a8f8496e70865099ba72540494cd3e2942634";
  hash = "sha256-OEgs3uRPMb4Y629FJXAWZW9q9LqHS/A/GUqr3K5wzOA=";
  finalImageName = "nixos/nix";
  finalImageTag = "latest";
}
```

ارائه آرگومان‌های `--arch` و `--os` به `nix-prefetch-docker` جهت فیلتر کردن خروجی به یک تصویر واحد اهمیت دارد، در صورتی که چندین معماری و/یا سیستم‌عامل توسط نام تصویر و تگ‌های مشخص‌شده پشتیبانی شوند.
به طور پیش‌فرض، `nix-prefetch-docker` مقدار `os` را روی `linux` و `arch` را روی `amd64` تنظیم می‌کند.

برای مشاهده فهرستی از تمام آرگومان‌های پشتیبانی‌شده، دستور `nix-prefetch-docker --help` را اجرا کنید:
```shell
$ nix run nixpkgs#nix-prefetch-docker -- --help
(output removed for clarity)
```
:::

## exportImage {#ssec-pkgs-dockerTools-exportImage}

این تابع شبیه به دستور `docker container export` است، به این معنی که می‌توان از آن برای برون‌بری سیستم‌فایل یک تصویر به صورت یک آرشیو tarball فشرده‌نشده استفاده کرد.
تفاوت در این است که `docker container export` روی کنتینرها اعمال می‌شود، اما `dockerTools.exportImage` روی تصویرهای Docker اعمال می‌گردد.
آرشیو حاصل حاوی هیچ‌گونه متادیتای تصویر (مانند دستوری که با `docker container run` اجرا می‌شود) نخواهد بود و فقط محتویات سیستم‌فایل را شامل می‌شود.

شما می‌توانید از این تابع برای درون‌ریزی یک آرشیو در Docker با `docker image import` استفاده کنید.
برای درک نحوه انجام این کار، [](#ex-dockerTools-exportImage-importingDocker) را ببینید.

:::{.caution}
`exportImage` با استخراج تصویر داده‌شده در یک ماشین مجازی (VM) کار می‌کند.
به همین دلیل، استفاده از این تابع مستلزم در دسترس بودن دستگاه `kvm` است، [`system-features`](https://nixos.org/manual/nix/stable/command-ref/conf-file.html#conf-system-features) را ببینید.
:::

### ورودی‌ها {#ssec-pkgs-dockerTools-exportImage-inputs}

`exportImage` منتظر آرگومانی با صفات زیر است:

`fromImage` (مجموعه ویژگی یا رشته)

: فایل tarball مخزن تصویر که سیستم‌فایل آن برون‌بری خواهد شد.
  این باید یک تصویر معتبر Docker باشد، مانند تصویری که توسط `docker image save` برون‌بری شده‌است، یا تصویر دیگری که با توابع کمکی `dockerTools` ساخته شده‌است.

  اگر `name` مشخص نشده باشد، `fromImage` باید یک مجموعه ویژگی مربوط به یک derivation / اشتقاق ساخت باشد، یعنی نمی‌تواند مسری به یک tarball باشد.
  اگر `name` مشخص شده باشد، `fromImage` می‌تواند یک مجموعه ویژگی مربوط به یک derivation / اشتقاق ساخت یا صرفاً یک مسیر به یک tarball باشد.

  برای درک ارتباط بین `fromImage`، `name` و نام استفاده‌شده برای خروجی `exportImage`، بخش‌های [](#ex-dockerTools-exportImage-naming) و [](#ex-dockerTools-exportImage-fromImagePath) را ببینید.

`fromImageName` (رشته یا Null؛ _اختیاری_)

: برای مشخص کردن تصویر موجود در فایل tarball مخزن در صورتی که حاوی چند تصویر باشد، استفاده می‌شود.
  مقدار `null` به این معنی است که `exportImage` از اولین تصویر موجود در مخزن (Repository) استفاده خواهد کرد.

  :::{.note}
  این گزینه باید همراه با `fromImageTag` استفاده شود. استفاده از `fromImageName` به تنهایی و بدون `fromImageTag` باعث می‌شود که `exportImage` از اولین تصویر موجود در مخزن استفاده کند.
  :::

  _مقدار پیش‌فرض:_ `null`.

`fromImageTag` (رشته یا Null؛ _اختیاری_)

: برای مشخص کردن تصویر موجود در فایل tarball مخزن در صورتی که حاوی چند تصویر باشد، استفاده می‌شود.
  مقدار `null` به این معنی است که `exportImage` از اولین تصویر موجود در مخزن استفاده خواهد کرد.

  :::{.note}
  این گزینه باید همراه با `fromImageName` استفاده شود. استفاده از `fromImageTag` به تنهایی و بدون `fromImageName` باعث می‌شود که `exportImage` از اولین تصویر موجود در مخزن استفاده کند.
  :::

  _مقدار پیش‌فرض:_ `null`.

`diskSize` (عدد؛ _اختیاری_)

: اندازه‌ی دیسک (به مگابایت) ماشین مجازی (VM) استفاده‌شده برای استخراج تصویر را کنترل می‌کند.

  _مقدار پیش‌فرض:_ 1024.

`name` (رشته؛ _اختیاری_)

: نامی که برای خروجی در مسیر انبار نیکس (Nix store) استفاده می‌شود.

  _مقدار پیش‌فرض:_ مقدار `fromImage.name`.

### مثال‌ها {#ssec-pkgs-dockerTools-exportImage-examples}

:::{.example #ex-dockerTools-exportImage-hello}
# برون‌بری یک تصویر Docker با `dockerTools.exportImage`

این مثال ابتدا یک تصویر لایه‌ای را با [`dockerTools.buildLayeredImage`](#ssec-pkgs-dockerTools-buildLayeredImage) می‌سازد و سپس سیستم‌فایل آن را با `dockerTools.exportImage` برون‌بری می‌کند.

```nix
{ dockerTools, hello }:
dockerTools.exportImage {
  name = "hello";
  fromImage = dockerTools.buildLayeredImage {
    name = "hello";
    contents = [ hello ];
  };
}
```

هنگام ساخت بسته بالا، می‌توانیم ببینیم که لایه‌های تصویر Docker برای تولید خروجی نهایی استخراج می‌شوند:

```shell
$ nix-build
(some output removed for clarity)
Unpacking base image...
From-image name or tag wasn't set. Reading the first ID.
Unpacking layer 5731199219418f175d1580dbca05677e69144425b2d9ecb60f416cd57ca3ca42/layer.tar
tar: Removing leading `/' from member names
Unpacking layer e2897bf34bb78c4a65736510204282d9f7ca258ba048c183d665bd0f3d24c5ec/layer.tar
tar: Removing leading `/' from member names
Unpacking layer 420aa5876dca4128cd5256da7dea0948e30ef5971712f82601718cdb0a6b4cda/layer.tar
tar: Removing leading `/' from member names
Unpacking layer ea5f4e620e7906c8ecbc506b5e6f46420e68d4b842c3303260d5eb621b5942e5/layer.tar
tar: Removing leading `/' from member names
Unpacking layer 65807b9abe8ab753fa97da8fb74a21fcd4725cc51e1b679c7973c97acd47ebcf/layer.tar
tar: Removing leading `/' from member names
Unpacking layer b7da2076b60ebc0ea6824ef641978332b8ac908d47b2d07ff31b9cc362245605/layer.tar
Executing post-mount steps...
Packing raw image...
[    1.660036] reboot: Power down
/nix/store/x6a5m7c6zdpqz1d8j7cnzpx9glzzvd2h-hello
```

دستور زیر بخشی از محتویات خروجی را فهرست می‌کند تا تایید کند که ساختار آرشیو طبق انتظار است:

```shell
$ tar --exclude '*/share/*' --exclude 'nix/store/*/*' -tvf /nix/store/x6a5m7c6zdpqz1d8j7cnzpx9glzzvd2h-hello
drwxr-xr-x root/0            0 1979-12-31 16:00 ./
drwxr-xr-x root/0            0 1979-12-31 16:00 ./bin/
lrwxrwxrwx root/0            0 1979-12-31 16:00 ./bin/hello -> /nix/store/h92a9jd0lhhniv2q417hpwszd4jhys7q-hello-2.12.1/bin/hello
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/store/
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/store/05zbwhz8a7i2v79r9j21pl6m6cj0xi8k-libunistring-1.1/
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/store/ayg5rhjhi9ic73hqw33mjqjxwv59ndym-xgcc-13.2.0-libgcc/
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/store/h92a9jd0lhhniv2q417hpwszd4jhys7q-hello-2.12.1/
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/store/m59xdgkgnjbk8kk6k6vbxmqnf82mk9s0-libidn2-2.3.4/
dr-xr-xr-x root/0            0 1979-12-31 16:00 ./nix/store/p3jshbwxiwifm1py0yq544fmdyy98j8a-glibc-2.38-27/
drwxr-xr-x root/0            0 1979-12-31 16:00 ./share/
```
:::

:::{.example #ex-dockerTools-exportImage-importingDocker}
# وارد کردن آرشیو ساخته‌شده با `dockerTools.exportImage` در Docker

ما از همان بسته در [](#ex-dockerTools-exportImage-hello) استفاده کرده و آن را وارد Docker خواهیم کرد.

```nix
{ dockerTools, hello }:
dockerTools.exportImage {
  name = "hello";
  fromImage = dockerTools.buildLayeredImage {
    name = "hello";
    contents = [ hello ];
  };
}
```

ساخت و وارد کردن آن به Docker:

```shell
$ nix-build
(output removed for clarity)
/nix/store/x6a5m7c6zdpqz1d8j7cnzpx9glzzvd2h-hello
$ docker image import /nix/store/x6a5m7c6zdpqz1d8j7cnzpx9glzzvd2h-hello
sha256:1d42dba415e9b298ea0decf6497fbce954de9b4fcb2984f91e307c8fedc1f52f
$ docker image ls
REPOSITORY                              TAG                IMAGE ID       CREATED         SIZE
<none>                                  <none>             1d42dba415e9   4 seconds ago   32.6MB
```
:::

:::{.example #ex-dockerTools-exportImage-naming}
# بررسی نام‌گذاری خروجی با `dockerTools.exportImage`

در صورتی که `fromImage` یک derivation باشد، `exportImage` نیازی به صفت (attribute) `name` ندارد؛ به این معنی که عبارت زیر کار می‌کند:

```nix
{ dockerTools, hello }:
dockerTools.exportImage {
  fromImage = dockerTools.buildLayeredImage {
    name = "hello";
    contents = [ hello ];
  };
}
```

با این حال، از آنجا که خروجی [`dockerTools.buildLayeredImage`](#ssec-pkgs-dockerTools-buildLayeredImage) با `.tar.gz` به پایان می‌رسد، خروجی `exportImage` نیز با `.tar.gz` به پایان خواهد رسید، حتی اگر آرشیو ایجادشده با `exportImage` فشرده‌نشده باشد:

```shell
$ nix-build
(output removed for clarity)
/nix/store/by3f40xvc4l6bkis74l0fj4zsy0djgkn-hello.tar.gz
$ file /nix/store/by3f40xvc4l6bkis74l0fj4zsy0djgkn-hello.tar.gz
/nix/store/by3f40xvc4l6bkis74l0fj4zsy0djgkn-hello.tar.gz: POSIX tar archive (GNU)
```

اگر آرشیو واقعاً فشرده شده بود، خروجی `file` به این موضوع اشاره می‌کرد.
به همین دلیل، ممکن است هنگام استفاده از `exportImage` همراه با سایر توابع `dockerTools` تنظیم یک صفت `name` مناسب مهم باشد.
:::

:::{.example #ex-dockerTools-exportImage-fromImagePath}
# استفاده از `dockerTools.exportImage` با یک مسیر به عنوان `fromImage`

امکان استفاده از یک مسیر به عنوان مقدار صفت `fromImage` هنگام فراخوانی `dockerTools.exportImage` وجود دارد.
با این حال، هنگام انجام این کار، **باید** صفت `name` مشخص شود، در غیر این صورت هنگام ارزیابی کد Nix با خطا مواجه خواهید شد.

برای این مثال، فرض می‌کنیم یک تصویر تاربال Docker به نام `image.tar.gz` در همان پوشه‌ای که بسته ما تعریف شده‌است وجود دارد:

```nix
{ dockerTools }:
dockerTools.exportImage {
  name = "filesystem.tar";
  fromImage = ./image.tar.gz;
}
```

با ساخت این، خروجی مورد انتظار به دست خواهد آمد:

```shell
$ nix-build
(output removed for clarity)
/nix/store/w13l8h3nlkg0zv56k7rj0ai0l2zlf7ss-filesystem.tar
```

اگر صفت (attribute) `name` را مشخص نکنید، با یک خطای ارزیابی مواجه خواهید شد و بسته ساخته نخواهد شد.
:::

## کمک‌رسان‌های محیط {#ssec-pkgs-dockerTools-helpers}

هنگام ساخت تصاویر Docker با Nix، ممکن است بخواهید فایل‌های خاصی را اضافه کنید که نرم‌افزارِ در حال بسته‌بندی شما انتظار دارد به‌صورت سراسری در دسترس باشند.
نمونه‌های ساده آن ابزار `env` در مسیر `/usr/bin/env` یا گواهی‌های معتبر ریشه TLS/SSL هستند.
چنین فایل‌هایی به احتمال زیاد در صورت ساخت یک تصویر Docker از ابتدا با Nix شامل نخواهند شد، و همچنین ممکن است اگر از تصویر Docker دیگری شروع کنید که شامل آن‌ها نیست، باز هم وجود نداشته باشند.
کمک‌رسان‌های این بخش، بسته‌هایی هستند که برخی از این فایل‌های سراسریِ مورد نیاز معمول را فراهم می‌کنند.

اکثر این کمک‌رسان‌ها بسته هستند، به این معنی که باید آن‌ها را به فهرست محتوایی که قرار است در تصویر گنجانده شود اضافه کنید (این مورد بسته به تابعی که برای ساخت تصویر استفاده می‌کنید تغییر می‌کند).
[](#ex-dockerTools-helpers-buildImage) و [](#ex-dockerTools-helpers-buildLayeredImage) نحوه گنجاندن این بسته‌ها در توابع `dockerTools` که یک تصویر می‌سازند را نشان می‌دهند.
برای جزئیات بیشتر درباره‌ی نحوه کارکرد آن، مستندات مربوط به تابعی را که استفاده می‌کنید ببینید.

### usrBinEnv {#sssec-pkgs-dockerTools-helpers-usrBinEnv}

این بخش ابزار `env` را در مسیر `/usr/bin/env` فراهم می‌کند.
این قابلیت در حال حاضر با پیوند دادن به باینری `env` از بسته `coreutils` پیاده‌سازی شده‌است، اما یک جزئیات پیاده‌سازی محسوب می‌شود که ممکن است در آینده تغییر کند.

### binSh {#sssec-pkgs-dockerTools-helpers-binSh}

این گزینه یک پیوند `/bin/sh` به باینری `bash` از بسته `bash` ایجاد می‌کند.
به همین دلیل، از مواردی مانند اجرای تعاملی یک دستور درون یک کنتینر پشتیبانی می‌کند (به عنوان مثال با اجرای `docker container run -it <image_name>`).

### caCertificates {#sssec-pkgs-dockerTools-helpers-caCertificates}

این گزینه گواهی‌های ریشه معتبر TLS/SSL را از بسته `cacert` در چند مسیر مختلف اضافه می‌کند تا با باینری‌های ساخته‌شده برای توزیع‌های مختلف Linux سازگار باشد.
مسیرهایی که در حال حاضر استفاده می‌شوند عبارتند از:

- `/etc/ssl/certs/ca-bundle.crt`
- `/etc/ssl/certs/ca-certificates.crt`
- `/etc/pki/tls/certs/ca-bundle.crt`

[]{#ssec-pkgs-dockerTools-fakeNss}
### fakeNss {#sssec-pkgs-dockerTools-helpers-fakeNss}

این یک صادرات مجدد (re-export) از بسته `fakeNss` در Nixpkgs است.
ببینید: [](#sec-fakeNss).

### shadowSetup {#ssec-pkgs-dockerTools-shadowSetup}

این یک رشته حاوی اسکریپتی است که فایل‌های مورد نیاز برای کارکرد [`shadow`](https://github.com/shadow-maint/shadow) را (با استفاده از بسته `shadow` از Nixpkgs) آماده‌سازی می‌کند و متغیر `PATH` را تغییر می‌دهد تا همه ابزارهای آن در همان اسکریپت در دسترس باشند.
این رشته برای استفاده همراه با سایر توابع dockerTools در صفاتی که انتظار اسکریپت دارند در نظر گرفته شده‌است.
پس از اجرای اسکریپتِ موجود در `shadowSetup`، می‌توانید دستورات دیگری را اضافه کنید که از ابزارهای موجود در `shadow` استفاده می‌کنند؛ مانند افزودن کاربران و/یا گروه‌های اضافی.
برای درک بهتر نحوه استفاده از آن، [](#ex-dockerTools-shadowSetup-buildImage) و [](#ex-dockerTools-shadowSetup-buildLayeredImage) را ببینید.

`shadowSetup` به نتیجه‌ای مشابه [`fakeNss`](#sssec-pkgs-dockerTools-helpers-fakeNss) دست می‌یابد، اما علاوه بر راه‌اندازی فایل‌ها برای [PAM](https://en.wikipedia.org/wiki/Linux_PAM) و یک فایل {manpage}`login.defs(5)`، فقط یک کاربر `root` با مقادیر متفاوت برای پوشه خانه و شل مورد استفاده تنظیم می‌کند.

:::{.caution}
استفاده هم‌زمان از هر دو `fakeNss` و `shadowSetup` یا موجب شکست فرآیند ساخت شما می‌شود یا نتایج غیرمنتظره‌ای به بار می‌آورد.
بسته به مورد استفاده خود، تنها از یکی از `fakeNss` یا `shadowSetup` استفاده کنید و از به‌کارگیری هم‌زمان هر دو خودداری کنید.
:::

:::{.note}
هنگام استفاده همراه با [`buildLayeredImage`](#ssec-pkgs-dockerTools-buildLayeredImage) یا [`streamLayeredImage`](#ssec-pkgs-dockerTools-streamLayeredImage)، باید صفت (attribute) `enableFakechroot` را برابر با `true` قرار دهید، در غیر این صورت اسکریپت موجود در `shadowSetup` به‌درستی اجرا نخواهد شد.
بخش [](#ex-dockerTools-shadowSetup-buildLayeredImage) را ببینید.
:::

### نمونه‌ها {#ssec-pkgs-dockerTools-helpers-examples}

:::{.example #ex-dockerTools-helpers-buildImage}
# استفاده از کمک‌رسان‌های محیطی `dockerTools` با `buildImage`

این نمونه، کمک‌رسان [`binSh`](#sssec-pkgs-dockerTools-helpers-binSh) را به یک تصویر Docker پایه ساخته‌شده با [`dockerTools.buildImage`](#ssec-pkgs-dockerTools-buildImage) اضافه می‌کند.
این کمک‌رسان امکان ورود به یک شل (Shell) را در داخل کنتینر فراهم می‌سازد.
این، معادل `buildImage` برای [](#ex-dockerTools-helpers-buildLayeredImage) است.

```nix
{ dockerTools, hello }:
dockerTools.buildImage {
  name = "env-helpers";
  tag = "latest";

  copyToRoot = [
    hello
    dockerTools.binSh
  ];
}
```

پس از ساخت تصویر و بارگذاری آن در Docker، می‌توانیم یک کنتینر بر اساس آن ایجاد کرده و وارد یک شل در داخل کنتینر شویم.
این امر به وسیله‌ی `binSh` امکان‌پذیر شده‌است.

```shell
$ nix-build
(some output removed for clarity)
/nix/store/2p0i3i04cgjlk71hsn7ll4kxaxxiv4qg-docker-image-env-helpers.tar.gz
$ docker image load -i /nix/store/2p0i3i04cgjlk71hsn7ll4kxaxxiv4qg-docker-image-env-helpers.tar.gz
(output removed for clarity)
$ docker container run --rm -it env-helpers:latest /bin/sh
sh-5.2# help
GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)
(rest of output removed for clarity)
```
:::

:::{.example #ex-dockerTools-helpers-buildLayeredImage}
# استفاده از کمک‌رسان‌های محیطی `dockerTools` با `buildLayeredImage`

این مثال، کمک‌رسان [`binSh`](#sssec-pkgs-dockerTools-helpers-binSh) را به یک تصویر Docker پایه ساخته‌شده با [`dockerTools.buildLayeredImage`](#ssec-pkgs-dockerTools-buildLayeredImage) اضافه می‌کند.
این کمک‌رسان امکان ورود به یک شل (Shell) در داخل کنتینر را فراهم می‌کند.
این معادل `buildLayeredImage` برای [](#ex-dockerTools-helpers-buildImage) است.

```nix
{ dockerTools, hello }:
dockerTools.buildLayeredImage {
  name = "env-helpers";
  tag = "latest";

  contents = [
    hello
    dockerTools.binSh
  ];

  config = {
    Cmd = [ "/bin/hello" ];
  };
}
```

پس از ساخت تصویر و بارگذاری آن در Docker، می‌توانیم کنتینری بر اساس آن ایجاد کنیم و وارد یک شل (Shell) در داخل کنتینر شویم.
این امر توسط `binSh` امکان‌پذیر شده‌است.

```shell
$ nix-build
(some output removed for clarity)
/nix/store/rpf47f4z5b9qr4db4ach9yr4b85hjhxq-env-helpers.tar.gz
$ docker image load -i /nix/store/rpf47f4z5b9qr4db4ach9yr4b85hjhxq-env-helpers.tar.gz
(output removed for clarity)
$ docker container run --rm -it env-helpers:latest /bin/sh
sh-5.2# help
GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)
(rest of output removed for clarity)
```
:::

:::{.example #ex-dockerTools-shadowSetup-buildImage}
# استفاده از `dockerTools.shadowSetup` به همراه `dockerTools.buildImage`

این یک نمونه است که نحوه استفاده از `shadowSetup` به همراه `dockerTools.buildImage` را نشان می‌دهد.
توجه داشته باشید که اسکریپت اضافی در `runAsRoot` از `groupadd` و `useradd` استفاده می‌کند، که باینری‌های ارائه‌شده توسط بسته `shadow` هستند.
این باینری‌ها توسط اسکریپت `shadowSetup` به `PATH` اضافه می‌شوند، اما تنها برای مدت زمان اجرای `runAsRoot`.

```nix
{ dockerTools, hello }:
dockerTools.buildImage {
  name = "shadow-basic";
  tag = "latest";

  copyToRoot = [ hello ];

  runAsRoot = ''
    ${dockerTools.shadowSetup}
    groupadd -r hello
    useradd -r -g hello hello
    mkdir /data
    chown hello:hello /data
  '';

  config = {
    Cmd = [ "/bin/hello" ];
    WorkingDir = "/data";
  };
}
```
:::

:::{.example #ex-dockerTools-shadowSetup-buildLayeredImage}
# استفاده از `dockerTools.shadowSetup` همراه با `dockerTools.buildLayeredImage`

این همان کاری را انجام می‌دهد که [](#ex-dockerTools-shadowSetup-buildImage) انجام می‌دهد، اما به جای آن از `buildLayeredImage` استفاده می‌کند.

توجه داشته باشید که اسکریپت اضافی در `fakeRootCommands` از `groupadd` و `useradd` استفاده می‌کند، که باینری‌های ارائه‌شده توسط بسته `shadow` هستند.
این باینری‌ها توسط اسکریپت `shadowSetup` به `PATH` اضافه می‌شوند، اما فقط در طول مدت اجرای `fakeRootCommands`.

```nix
{ dockerTools, hello }:
dockerTools.buildLayeredImage {
  name = "shadow-basic";
  tag = "latest";

  contents = [ hello ];

  fakeRootCommands = ''
    ${dockerTools.shadowSetup}
    groupadd -r hello
    useradd -r -g hello hello
    mkdir /data
    chown hello:hello /data
  '';
  enableFakechroot = true;

  config = {
    Cmd = [ "/bin/hello" ];
    WorkingDir = "/data";
  };
}
```
:::

[]{#ssec-pkgs-dockerTools-buildNixShellImage-arguments}
## buildNixShellImage {#ssec-pkgs-dockerTools-buildNixShellImage}

`buildNixShellImage` در لایه‌ی زیرین از [`streamNixShellImage`](#ssec-pkgs-dockerTools-streamNixShellImage) استفاده می‌کند تا یک tarball از مخزنِ سازگار با Docker و فشرده‌شده برای تصویری بسازد که محیطی مشابه با اجرای `nix-shell` روی یک derivation / اشتقاق ساخت را آماده می‌کند.
در واقع، `buildNixShellImage` اسکریپت ایجادشده توسط `streamNixShellImage` را اجرا می‌کند تا تصویر فشرده‌شده را در انبار نیکس (Nix store) ذخیره نماید.

`buildNixShellImage` از همان گزینه‌های `streamNixShellImage` پشتیبانی می‌کند؛ برای جزئیات بیشتر به [`streamNixShellImage`](#ssec-pkgs-dockerTools-streamNixShellImage) مراجعه کنید.

[]{#ssec-pkgs-dockerTools-buildNixShellImage-example}
### مثال‌ها {#ssec-pkgs-dockerTools-buildNixShellImage-examples}

:::{.example #ex-dockerTools-buildNixShellImage-hello}
# ساخت یک تصویر Docker با `buildNixShellImage` به همراه محیط ساخت برای بسته `hello`

این مثال نحوه ساخت بسته `hello` را در داخل یک کانتینر Docker ساخته‌شده با `buildNixShellImage` نشان می‌دهد.
تصویر Docker تولیدشده نامی مانند `hello-<version>-env` و تگ `latest` خواهد داشت.
این مثال، معادل `buildNixShellImage` برای [](#ex-dockerTools-streamNixShellImage-hello) است.

```nix
{ dockerTools, hello }:
dockerTools.buildNixShellImage {
  drv = hello;
  tag = "latest";
}
```

نتیجه ساخت این بسته یک فایل `.tar.gz` است که می‌توان آن را در Docker بارگذاری کرد:

```shell
$ nix-build
(some output removed for clarity)
/nix/store/pkj1sgzaz31wl0pbvbg3yp5b3kxndqms-hello-2.12.1-env.tar.gz

$ docker image load -i /nix/store/pkj1sgzaz31wl0pbvbg3yp5b3kxndqms-hello-2.12.1-env.tar.gz
(some output removed for clarity)
Loaded image: hello-2.12.1-env:latest
```

پس از شروع یک کنتینر تعاملی، derivation را می‌توان با اجرای `buildDerivation` ساخت و خروجی آن را طبق انتظار اجرا کرد:

```shell
$ docker container run -it hello-2.12.1-env:latest
[nix-shell:~]$ buildDerivation
Running phase: unpackPhase
unpacking source archive /nix/store/pa10z4ngm0g83kx9mssrqzz30s84vq7k-hello-2.12.1.tar.gz
source root is hello-2.12.1
(some output removed for clarity)
Running phase: fixupPhase
shrinking RPATHs of ELF executables and libraries in /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1
shrinking /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1/bin/hello
checking for references to /build/ in /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1...
gzipping man pages under /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1/share/man/
patching script interpreter paths in /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1
stripping (with command strip and flags -S -p) in  /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1/bin

[nix-shell:~]$ $out/bin/hello
Hello, world!
```
:::

## streamNixShellImage {#ssec-pkgs-dockerTools-streamNixShellImage}

`streamNixShellImage` یک **اسکریپت** می‌سازد که با اجرا شدن، یک tarball مخزن سازگار با Docker از تصویری که محیطی مشابه اجرای `nix-shell` روی یک derivation برپا می‌کند را در stdout به صورت استریم پخش می‌کند.
این به این معنی است که `streamNixShellImage` تصویری در انبار نیکس (Nix store) خروجی نمی‌دهد، بلکه تنها اسکریپتی می‌سازد که تصویر را می‌سازد؛ این موضوع به ویژه در مورد تصاویر بزرگ باعث صرفه‌جویی در ورودی/خروجی (IO) و فضای دیسک/حافظه پنهان می‌شود.
برای درک نحوه بارگیری تصویر تولیدشده توسط این اسکریپت در Docker، بخش [](#ex-dockerTools-streamNixShellImage-hello) را ببینید.

محیط راه‌اندازی‌شده توسط `streamNixShellImage` تا حدی شبیه به سندباکس Nix است که معمولاً توسط `nix-build` استفاده می‌شود، با این تفاوت اصلی که دسترسی به اینترنت در آن مجاز است.
همچنین مانند یک `nix-shell` تعاملی رفتار می‌کند، مواردی مانند `shellHook` را اجرا می‌نماید (ببینید [](#ex-dockerTools-streamNixShellImage-addingShellHook)) و یک پرامپت تعاملی تنظیم می‌کند.
اگر derivation قابل ساخت باشد (یعنی بتوان از `nix-build` روی آن استفاده کرد)، اجرای `buildDerivation` در کانتینر، derivation را می‌سازد و تمام خروجی‌های آن در مسیرهای درست `/nix/store` که توسط متغیرهای محیطی مربوطه (مانند `$out`) اشاره شده‌اند، در دسترس خواهند بود.

::: {.caution}
محیط درون تصویر کاملاً با `nix-shell` یا `nix-build` مطابقت ندارد و مشخص شده‌است که این تابع برای درایویشن‌های با خروجی ثابت، درایویشن‌های آدرس‌دهی‌شده بر اساس محتوا، درایویشن‌های ناخالص و سایر انواع خاص درایویشن‌ها به‌درستی کار نمی‌کند.
:::

### Inputs {#ssec-pkgs-dockerTools-streamNixShellImage-inputs}

`streamNixShellImage` انتظار یک آرگومان با ویژگی‌های زیر را دارد:

`drv` (مجموعه ویژگی)

: همان derivation که محیط درون تصویر برای آن برپا خواهد شد.
  افزودن بسته‌ها به تصویر Docker با گسترش فهرست `nativeBuildInputs` این derivation امکان‌پذیر است.
  برای مشاهده نحوه انجام این کار، بخش [](#ex-dockerTools-streamNixShellImage-extendingBuildInputs) را ببینید.
  به همین ترتیب، می‌توانید اسکریپت راه‌اندازی اولیه تصویر را با گسترش `shellHook` توسعه دهید.
  بخش [](#ex-dockerTools-streamNixShellImage-addingShellHook) نحوه انجام این کار را نشان می‌دهد.

`name` (رشته؛ _اختیاری_)

: نام تصویر تولیدشده.

  _مقدار پیش‌فرض:_ مقدار `drv.name + "-env"`.

`tag` (رشته یا Null؛ _اختیاری_)

: تگ تصویر تولیدشده.
  اگر `null` باشد، هش nix derivation که تصویر Docker را می‌سازد به عنوان تگ استفاده خواهد شد.

  _مقدار پیش‌فرض:_ `null`.

`uid` (عدد؛ _اختیاری_)

: شناسه کاربر (User ID) برای اجرای کانتینر.
  این را می‌توان به عنوان کاربر ساخت `nixbld` در نظر گرفت.

  _مقدار پیش‌فرض:_ 1000.

`gid` (عدد؛ _اختیاری_)

: شناسه گروه (Group ID) برای اجرای کانتینر.
  این را می‌توان به عنوان گروه ساخت `nixbld` در نظر گرفت.

  _مقدار پیش‌فرض:_ 1000.

`homeDirectory` (رشته؛ _اختیاری_)

: پوشه خانه کاربری که کانتینر با آن در حال اجرا است.

  _مقدار پیش‌فرض:_ `/build`.

`shell` (رشته؛ _اختیاری_)

: مسیر باینری `bash` جهت استفاده به عنوان شل.
  این شل هنگام اجرای تصویر راه‌اندازی می‌شود.
  این را می‌توان معادل [متغیر محیطی](https://nixos.org/manual/nix/stable/command-ref/nix-shell.html#environment-variables) `NIX_BUILD_SHELL` برای {manpage}`nix-shell(1)` دانست.

  _مقدار پیش‌فرض:_ باینری `bash` از بسته `bash`.

`command` (رشته یا Null؛ _اختیاری_)

: در صورت تعیین شدن، این دستور در محیط derivation در یک شل تعاملی اجرا خواهد شد.
  در صورت تعیین دستور، یک فراخوانی به `exit` پس از آن اضافه می‌شود تا شل پس از اتمام اجرا خارج شود.
  این را می‌توان معادل گزینه `--command` در {manpage}`nix-shell(1)` دانست.

  _مقدار پیش‌فرض:_ `null`.

`run` (رشته یا Null؛ _اختیاری_)

: مشابه صفت `command` است، اما در عوض دستور را در یک شل غیرتعاملی اجرا می‌کند.
  در صورت تعیین دستور، یک فراخوانی به `exit` پس از آن اضافه می‌شود تا شل پس از اتمام اجرا خارج شود.
  این را می‌توان معادل گزینه `--run` در {manpage}`nix-shell(1)` دانست.

  _مقدار پیش‌فرض:_ `null`.

### مثال‌ها {#ssec-pkgs-dockerTools-streamNixShellImage-examples}

:::{.example #ex-dockerTools-streamNixShellImage-hello}
# ساخت یک تصویر Docker با `streamNixShellImage` همراه با محیط ساخت برای بسته `hello`

این مثال نحوه ساخت بسته `hello` را در داخل یک کانتینر Docker ساخته‌شده با `streamNixShellImage` نشان می‌دهد.
تصویر Docker تولیدشده نامی مانند `hello-<version>-env` و تگ `latest` خواهد داشت.
این مثال معادل `streamNixShellImage` از [](#ex-dockerTools-buildNixShellImage-hello) است.

```nix
{ dockerTools, hello }:
dockerTools.streamNixShellImage {
  drv = hello;
  tag = "latest";
}
```

نتیجه ساخت این بسته یک اسکریپت است.
اجرای این اسکریپت و هدایت خروجی آن به `docker image load` همان تصویری را به شما می‌دهد که در [](#ex-dockerTools-buildNixShellImage-hello) ساخته شده‌است.

```shell
$ nix-build
(some output removed for clarity)
/nix/store/8vhznpz2frqazxnd8pgdvf38jscdypax-stream-hello-2.12.1-env

$ /nix/store/8vhznpz2frqazxnd8pgdvf38jscdypax-stream-hello-2.12.1-env | docker image load
(some output removed for clarity)
Loaded image: hello-2.12.1-env:latest
```

پس از شروع یک کنتینر تعاملی، درایویشن را می‌توان با اجرای `buildDerivation` ساخت و خروجی مطابق انتظار قابل اجرا است:

```shell
$ docker container run -it hello-2.12.1-env:latest
[nix-shell:~]$ buildDerivation
Running phase: unpackPhase
unpacking source archive /nix/store/pa10z4ngm0g83kx9mssrqzz30s84vq7k-hello-2.12.1.tar.gz
source root is hello-2.12.1
(some output removed for clarity)
Running phase: fixupPhase
shrinking RPATHs of ELF executables and libraries in /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1
shrinking /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1/bin/hello
checking for references to /build/ in /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1...
gzipping man pages under /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1/share/man/
patching script interpreter paths in /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1
stripping (with command strip and flags -S -p) in  /nix/store/f2vs29jibd7lwxyj35r9h87h6brgdysz-hello-2.12.1/bin

[nix-shell:~]$ $out/bin/hello
Hello, world!
```
:::

:::{.example #ex-dockerTools-streamNixShellImage-extendingBuildInputs}
# افزودن بسته‌های اضافی به تصویر Docker ساخته‌شده با `streamNixShellImage`

این مثال نحوه افزودن بسته‌های اضافی به تصویری ساخته‌شده با `streamNixShellImage` را نشان می‌دهد.
در این حالت، ما بسته `cowsay` را اضافه می‌کنیم.
تصویر Docker تولیدشده نامی مانند `hello-<version>-env` و برچسب `latest` خواهد داشت.
این مثال از [](#ex-dockerTools-streamNixShellImage-hello) به عنوان نقطه شروع استفاده می‌کند.

```nix
{
  dockerTools,
  cowsay,
  hello,
}:
dockerTools.streamNixShellImage {
  tag = "latest";
  drv = hello.overrideAttrs (old: {
    nativeBuildInputs = old.nativeBuildInputs or [ ] ++ [ cowsay ];
  });
}
```

نتیجه‌ی ساخت این بسته اسکریپتی است که می‌توان آن را اجرا کرد و خروجی آن را به `docker image load` پایپ کرد تا تصویر تولیدشده بارگذاری شود.

```shell
$ nix-build
(some output removed for clarity)
/nix/store/h5abh0vljgzg381lna922gqknx6yc0v7-stream-hello-2.12.1-env

$ /nix/store/h5abh0vljgzg381lna922gqknx6yc0v7-stream-hello-2.12.1-env | docker image load
(some output removed for clarity)
Loaded image: hello-2.12.1-env:latest
```

پس از راه‌اندازی یک کنتینر تعاملی، می‌توانیم با اجرای `cowsay` در دسترس بودن بسته اضافی را بررسی کنیم:

```shell
$ docker container run -it hello-2.12.1-env:latest
[nix-shell:~]$ cowsay "Hello, world!"
 _______________
< Hello, world! >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
:::

:::{.example #ex-dockerTools-streamNixShellImage-addingShellHook}
# افزودن یک `shellHook` به یک تصویر Docker ساخته‌شده با `streamNixShellImage`

این مثال نحوه افزودن یک دستور `shellHook` به یک تصویر ساخته‌شده با `streamNixShellImage` را نشان می‌دهد.
در این حالت، ما صرفاً رشته `Hello, world!` را در خروجی چاپ می‌کنیم.
تصویر Docker تولیدشده نامی مانند `hello-<version>-env` و تگ `latest` خواهد داشت.
این مثال از [](#ex-dockerTools-streamNixShellImage-hello) به عنوان نقطه شروع استفاده می‌کند.

```nix
{ dockerTools, hello }:
dockerTools.streamNixShellImage {
  tag = "latest";
  drv = hello.overrideAttrs (old: {
    shellHook = ''
      ${old.shellHook or ""}
      echo "Hello, world!"
    '';
  });
}
```

نتیجه‌ی ساخت این بسته، اسکریپتی است که می‌توان آن را اجرا کرد و به `docker image load` پایپ نمود تا تصویر تولیدشده بارگذاری شود.

```shell
$ nix-build
(some output removed for clarity)
/nix/store/iz4dhdvgzazl5vrgyz719iwjzjy6xlx1-stream-hello-2.12.1-env

$ /nix/store/iz4dhdvgzazl5vrgyz719iwjzjy6xlx1-stream-hello-2.12.1-env | docker image load
(some output removed for clarity)
Loaded image: hello-2.12.1-env:latest
```

پس از راه‌اندازی یک کنتینر تعاملی، می‌توانیم نتیجه‌ی `shellHook` را مشاهده کنیم:

```shell
$ docker container run -it hello-2.12.1-env:latest
Hello, world!

[nix-shell:~]$
```
:::
