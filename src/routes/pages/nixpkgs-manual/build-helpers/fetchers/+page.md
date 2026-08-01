# <a id="chap-pkgs-fetchers"></a> دریافت‌کننده‌ها

ساخت نرم‌افزار با استفاده از Nix اغلب مستلزم بارگیری کد منبع و سایر فایل‌ها از اینترنت است.
برای این منظور، ما از توابعی استفاده می‌کنیم که آن‌ها را _دریافت‌کننده_ می‌نامیم؛ این توابع کدهای منبع راه دور را از طریق پروتکل‌ها و سرویس‌های مختلف به دست می‌آورند.

Nix دریافت‌کننده‌های توکار ارائه می‌دهد، مانند [`fetchTarball`](https://nixos.org/manual/nix/stable/language/builtins.html#builtins-fetchTarball).
Nixpkgs دریافت‌کننده‌های خودش را ارائه می‌دهد که به گونه متفاوتی کار می‌کنند:

- یک دریافت‌کننده توکار، فایل‌ها را در زمان ارزیابی بارگیری و در کش ذخیره می‌کند و یک [مسیر انبار (store path)](https://nixos.org/manual/nix/stable/glossary#gloss-store-path) تولید می‌نماید.
  یک دریافت‌کننده Nixpkgs یک [derivation](https://nixos.org/manual/nix/stable/glossary#gloss-derivation) با ([خروجی ثابت](https://nixos.org/manual/nix/stable/glossary#gloss-fixed-output-derivation)) ایجاد می‌کند و فایل‌ها در زمان ساخت بارگیری می‌شوند.
- دریافت‌کننده‌های توکار پس از انقضای [`tarball-ttl`](https://nixos.org/manual/nix/stable/command-ref/conf-file#conf-tarball-ttl)، کش خود را باطل می‌کنند و برای بررسی به روز بودن ورودی کش، به فعالیت شبکه‌ای نیاز خواهند داشت.
  دریافت‌کننده‌های Nixpkgs تنها در صورتی بارگیری مجدد انجام می‌دهند که هش مشخص‌شده تغییر کند یا شیء انبار در دسترس نباشد.
- دریافت‌کننده‌های توکار از [جایگزین‌ها (substituters)](https://nixos.org/manual/nix/stable/command-ref/conf-file#conf-substituters) استفاده نمی‌کنند.
  درایویشن‌های تولیدشده توسط دریافت‌کننده‌های Nixpkgs به صورت شفاف از هر کش باینری پیکربندی‌شده استفاده خواهند کرد.

این امر زمان مورد نیاز برای ارزیابی Nixpkgs را به میزان قابل توجهی کاهش می‌دهد و به [Hydra](https://nixos.org/hydra) اجازه می‌دهد کدهای منبع استفاده‌شده توسط Nixpkgs را در [کش باینری عمومی](https://cache.nixos.org) نگهداری و دوباره توزیع کند.
به این دلایل، استفاده از دریافت‌کننده‌های توکار Nix در Nixpkgs مجاز نیست.

جدول زیر تفاوت‌ها را خلاصه می‌کند:

| دریافت‌کننده‌ها | بارگیری | خروجی | کش | بارگیری مجدد هنگام |
|-|-|-|-|-|
| `builtins.fetch*` | زمان ارزیابی | مسیر انبار (store path) | `/nix/store`، `~/.cache/nix` | انقضای `tarball-ttl`، عدم وجود در کش `~/.cache/nix`، عدم وجود شیء خروجی انبار در انبار محلی |
| `pkgs.fetch*` | زمان ساخت | derivation | `/nix/store`، جایگزین‌ها | عدم دسترسی به شیء خروجی انبار |

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> کمک‌رسان‌های `pkgs.fetchFrom*` به جای کل تاریخچهٔ نسخه‌ها، _اسنپ‌شات‌های_ کدهای منبع تحت کنترل نسخه را دریافت می‌کنند که کارآمدتر است.
> `pkgs.fetchgit` به طور پیش‌فرض نیز همین رفتار را دارد، اما می‌توان آن را از طریق صفات خاصی که به آن داده می‌شود تغییر داد.

## <a id="chap-pkgs-fetchers-caveats"></a> هشدارها

از آنجا که دریافت‌کننده‌های Nixpkgs درایویشن‌های با خروجی ثابت هستند، باید یک [هش خروجی](https://nixos.org/manual/nix/stable/language/advanced-attributes#adv-attr-outputHash) مشخص شود، که معمولاً به صورت غیرمستقیم از طریق صفت `hash` انجام می‌شود.
این هش به خروجی derivation اشاره دارد، که می‌تواند با خود سورس راه دور متفاوت باشد!

این موضوع دارای پیامدهای زیر است که باید از آن‌ها آگاه باشید:

- از ابزارهای Nix (یا آگاه از Nix) برای تولید هش خروجی استفاده کنید.

- هنگام تغییر هر یک از پارامترهای دریافت‌کننده، همیشه هش خروجی را به‌روزرسانی کنید.
  از یکی از روش‌های [](#sec-pkgs-fetchers-updating-source-hashes) استفاده کنید.
  در غیر این صورت، اشیاء موجود در انبار که با هش خروجی مطابقت دارند، به جای دریافت محتوای جدید، دوباره استفاده خواهند شد.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> مشکل مشابهی هنگام آزمایش تغییرات در پیاده‌سازی یک دریافت‌کننده رخ می‌دهد.
>   اگر خروجی derivation از قبل در انبار Nix وجود داشته باشد، شکست‌های تست ممکن است شناسایی‌نشده باقی بمانند.
>   تابع [`invalidateFetcherByDrvHash`](#tester-invalidateFetcherByDrvHash) به جلوگیری از استفادهٔ مجدد درایویشن‌های ذخیره‌شده در کش کمک می‌کند.

## <a id="sec-pkgs-fetchers-updating-source-hashes"></a> به‌روزرسانی هش‌های کد منبع

چندین روش برای به دست آوردن هش مربوط به یک سورس راه دور وجود دارد.
مگر اینکه متوجه باشید دریافت‌کننده‌ای که استفاده می‌کنید چگونه هش را از محتوای بارگیری‌شده محاسبه می‌کند، باید از [روش هش ساختگی](#sec-pkgs-fetchers-updating-source-hashes-fakehash-method) استفاده کنید.

1. <a id="sec-pkgs-fetchers-updating-source-hashes-fakehash-method"></a> روش هش ساختگی: در دستورالعمل بسته خود، هش را روی یکی از موارد زیر قرار دهید

   - `""`
   - `lib.fakeHash`
   - `lib.fakeSha256`
   - `lib.fakeSha512`

   برای ساخت تلاش کنید، هش‌های محاسبه‌شده را از پیام‌های خطا استخراج کرده و آن‌ها را در دستورالعمل قرار دهید.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> شما باید حتماً از یکی از این چهار هش ساختگی استفاده کنید و نه یک هش انتخاب‌شده به صورت دلخواه.
>    برای جزئیات به [](#sec-pkgs-fetchers-secure-hashes) مراجعه کنید.

<a id="ex-fetchers-update-fod-hash"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # به‌روزرسانی هش کد منبع با روش هش ساختگی
>
>    دستورالعمل زیر را که یک فایل ساده تولید می‌کند در نظر بگیرید:

> ```nix
>    { fetchurl }:
>    fetchurl {
>      url = "https://raw.githubusercontent.com/NixOS/nixpkgs/23.05/.version";
>      hash = "sha256-ZHl1emidXVojm83LCVrwULpwIzKE/mYwfztVkvpruOM=";
>    }
>    ```
>
> یک اشتباه رایج، به‌روزرسانی پارامتر یک دریافت‌کننده مانند `url` بدون به‌روزرسانی هش است:

> ```nix
>    { fetchurl }:
>    fetchurl {
>      url = "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version";
>      hash = "sha256-ZHl1emidXVojm83LCVrwULpwIzKE/mYwfztVkvpruOM=";
>    }
>    ```
>
> **این همان خروجی قبلی را تولید خواهد کرد!**
>    مقدار هش را برابر یک رشته خالی قرار دهید:

> ```nix
>    { fetchurl }:
>    fetchurl {
>      url = "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version";
>      hash = "";
>    }
>    ```
>
> هنگام ساخت بسته، از پیام خطا برای تعیین هش صحیح استفاده کنید:

> ```shell
>    $ nix-build
>    (some output removed for clarity)
>    error: hash mismatch in fixed-output derivation '/nix/store/7yynn53jpc93l76z9zdjj4xdxgynawcw-version.drv':
>            specified: sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
>                got:    sha256-BZqI7r0MNP29yGH5+yW2tjU9OOpOCEvwWKrWCv5CQ0I=
>    error: build of '/nix/store/bqdjcw5ij5ymfbm41dq230chk9hdhqff-version.drv' failed
>    ```

2. پیش‌دریافت سورس با [`nix-prefetch-&lt;type&gt; &lt;URL&gt;`](https://search.nixos.org/packages?buckets={'{'}'{'{'}'{'}'}%22package_attr_set%22%3A[%22No%20package%20set%22]%2C%22package_license_set%22%3A[]%2C%22package_maintainers_set%22%3A[]%2C%22package_platforms%22%3A[]{'{'}'{'}'}'{'}'}&query=nix-prefetch)، که در آن `&lt;type&gt;` یکی از موارد زیر است:

   - `url`
   - `git`
   - `hg`
   - `cvs`
   - `bzr`
   - `svn`
   - `darcs`
   - `pijul`

   هش در stdout چاپ می‌شود.

3. پیش‌دریافت بر اساس سورس بسته (با `nix-prefetch-url '&lt;nixpkgs&gt;' -A &lt;package&gt;.src`، که در آن `&lt;package&gt;` نام صفت (attribute) بسته است).
   هش در stdout چاپ می‌شود.

   این روش زمانی که نسخه بسته موجود را ارتقا داده‌اید و می‌خواهید هش جدید را پیدا کنید به خوبی کار می‌کند، اما اگر بسته از طریق صفت (attribute) قابل دسترسی نباشد یا بسته دارای سورس‌های متعدد باشد (`.srcs`، سورس‌های وابسته به معماری و غیره)، بی‌فایده است.

4. هش بالادستی (Upstream hash): زمانی که بالادستی `sha256` یا `sha512` ارائه می‌دهد از آن استفاده کنید.
   وقتی بالادستی `md5` ارائه می‌دهد از آن استفاده نکنید، در عوض `sha256` را محاسبه کنید.

   یک نکته ظریف این است که ابزارهای `nix-prefetch-*` هش‌ها را با کدگذاری `nix32` (یک انطباق base32 مخصوص Nix) تولید می‌کنند، اما بالادستی معمولاً کدگذاری شانزده‌شانزدهی (`base16`) ارائه می‌دهد.
   دریافت‌کننده‌ها هر دو فرمت را متوجه می‌شوند.
   Nixpkgs هیچ فرمت واحدی را استاندارد نمی‌کند.

   می‌توانید با استفاده از [`nix-hash`](https://nixos.org/manual/nix/stable/command-ref/nix-hash) بین فرمت‌های هش تبدیل انجام دهید.

5. استخراج هش از یک آرشیو سورس محلی با `sha256sum`.
   اگر هش سفارشی `base32` Nix را می‌خواهید، از `nix-prefetch-url file:///path/to/archive` استفاده کنید.

## <a id="sec-pkgs-fetchers-secure-hashes"></a> دریافت امن هش‌ها

همواره ایده خوبی است که هنگام بارگیری محتوای سورس، از حملات مرد میانی (MITM) اجتناب کنید.
در غیر این صورت، ممکن است نادانسته به جای سورس مورد نظر، بدافزار بارگیری کنید و به جای هش سورس واقعی، در نهایت از هش بدافزار استفاده کنید.
در ادامه ملاحظات امنیتی برای این سناریو آمده است:

- URLهای `http://` برای پیش‌دریافت هش‌ها امن نیستند.

- هش‌های بالادستی باید از طریق یک پروتکل امن به دست آیند.

- URLهای `https://` هنگام استفاده از `nix-prefetch-*` یا برای هش‌های بالادستی، محافظت‌های بیشتری به شما می‌دهند.

- URLهای `https://` هنگام استفاده از [روش هش جعلی](#sec-pkgs-fetchers-updating-source-hashes-fakehash-method) *تنها در صورتی* امن هستند که از یکی از هش‌های جعلی فهرست‌شده استفاده کنید.
  اگر از هر هش دیگری استفاده کنید، حتی اگر از URLهای HTTPS استفاده کنید، بارگیری در معرض حملات مرد میانی قرار خواهد گرفت.

  به بیان دقیق‌تر، اگر از هر هش دیگری استفاده کنید، هنگام بارگیری محتوا، [پرچم `--insecure`](https://curl.se/docs/manpage.html#-k) به فراخوانی زیرین `curl` ارسال خواهد شد.

## <a id="sec-pkgs-fetchers-proxy"></a> استفاده از پروکسی

دریافت‌کننده‌های Nixpkgs می‌توانند از پروکسی http(s) استفاده کنند. هر دریافت‌کننده به طور خودکار متغیرهای محیطی مرتبط با پروکسی (`http_proxy`، `https_proxy` و غیره) را از طریق [impureEnvVars](https://nixos.org/manual/nix/stable/language/advanced-attributes#adv-attr-impureEnvVars) به ارث می‌برد.

متغیر محیطی `NIX_SSL_CERT_FILE` نیز در دریافت‌کننده‌ها به ارث برده می‌شود و می‌توان از آن برای ارائه یک بسته گواهی سفارشی به دریافت‌کننده‌ها استفاده کرد. این کار معمولاً برای کارکرد صحیح پروکسی https بدون خطاهای اعتبارسنجی گواهی لازم است.

برای استفاده از یک نمونه موقت Tor به عنوان پروکسی جهت دریافت از آدرس‌های `.onion`، عبارت `nativeBuildInputs = [ tor.proxyHook ];` را به پارامترهای دریافت‌کننده اضافه کنید.

<a id="fetchurl"></a>
## <a id="sec-pkgs-fetchers-fetchurl"></a> `fetchurl`

`fetchurl` یک [derivation با خروجی ثابت](https://nixos.org/manual/nix/stable/glossary.html#gloss-fixed-output-derivation) برمی‌گرداند که محتوا را از یک URL مشخص دانلود کرده و محتوای دست‌نخورده را در انبار نیکس (Nix store) ذخیره می‌کند.

این تابع به صورت داخلی از `curl(1)` استفاده می‌کند و اجازه می‌دهد رفتار آن با مشخص کردن چند صفت (attribute) در آرگومانِ `fetchurl` تغییر کند (مستندات صفت‌های `curlOpts`، `curlOptsList` و `netrcPhase` را ببینید).

[مسیر انبار](https://nixos.org/manual/nix/stable/store/store-path) حاصل با هشی که به `fetchurl` داده شده و همچنین مقادیر `name` (یا `pname` و `version`) تعیین می‌شود.

اگر هنگام فراخوانی `fetchurl` هیچ‌کدام از `name` یا `pname` و `version` مشخص نشده باشند، به طور پیش‌فرض از [نام پایه (basename)](https://nixos.org/manual/nix/stable/language/builtins.html#builtins-baseNameOf) مربوط به `url` یا اولین عنصر `urls` استفاده خواهد شد.
اگر `pname` و `version` مشخص شده باشند، `fetchurl` از آن مقادیر استفاده کرده و `name` را حتی اگر مشخص شده باشد، نادیده می‌گیرد.

### <a id="sec-pkgs-fetchers-fetchurl-inputs"></a> ورودی‌ها

`fetchurl` نیازمند یک مجموعه ویژگی (attribute set) با صفت‌های زیر است:

`url` (رشته؛ _اختیاری_)
: آدرس URL برای دانلود.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> باید یکی از `url` یا `urls` مشخص شود، اما نه هر دو.

  تمامی URLها با فرمت [مشخص‌شده در اینجا](https://curl.se/docs/url-syntax.html#rfc-3986-plus) پشتیبانی می‌شوند.

  _مقدار پیش‌فرض:_ `""`.

`urls` (لیستی از رشته‌ها؛ _اختیاری_)
: لیستی از URLها که مکان‌های دانلود برای یک محتوای یکسان را مشخص می‌کند.
  هر URL به ترتیب امتحان می‌شود تا زمانی که یکی از آن‌ها با موفقیت محتوا را دریافت کند یا همه آن‌ها با شکست مواجه شوند.
  برای درک نحوه تاثیر این صفت بر رفتار `fetchurl` به [](#ex-fetchers-fetchurl-nixpkgs-version-multiple-urls) مراجعه کنید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> باید یکی از `url` یا `urls` مشخص شود، اما نه هر دو.

  _مقدار پیش‌فرض:_ `[]`.

`hash` (رشته؛ _اختیاری_)
: هش خروجی derivation مربوط به `fetchurl` که از فرمت داده‌های متای یکپارچگی همان‌طور که توسط [SRI](https://www.w3.org/TR/SRI/) تعریف شده است، پیروی می‌کند.
  برای اطلاعات بیشتر، [](#chap-pkgs-fetchers-caveats) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توصیه می‌شود به جای سایر صفت‌های مربوط به هش که برای سازگاری عقب‌رو وجود دارند، از صفت `hash` استفاده کنید.
>
>   اگر `hash` مشخص نشده باشد، باید `outputHash` و `outputHashAlgo` یا یکی از `sha512`، `sha256` یا `sha1` را مشخص کنید.

  _مقدار پیش‌فرض:_ `""`.

`outputHash` (رشته؛ _اختیاری_)
: هش خروجی derivation مربوط به `fetchurl` به فرمتی که Nix انتظار دارد.
  برای اطلاعات بیشتر درباره فرمت آن، [مستندات راهنمای Nix](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-outputHash) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توصیه می‌شود به جای آن از صفت `hash` استفاده کنید.
>
>   اگر `outputHash` مشخص شده باشد، باید `outputHashAlgo` را نیز مشخص کنید.

  _مقدار پیش‌فرض:_ `""`.

`outputHashAlgo` (رشته؛ _اختیاری_)
: الگوریتم مورد استفاده برای تولید مقدار مشخص‌شده در `outputHash`.
  برای اطلاعات بیشتر درباره مقادیری که پشتیبانی می‌کند، [مستندات راهنمای Nix](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-outputHashAlgo) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توصیه می‌شود به جای آن از صفت `hash` استفاده کنید.
>
>   اگر `outputHash` نیز مشخص نشده باشد، مقدار مشخص‌شده در `outputHashAlgo` نادیده گرفته خواهد شد.

  _مقدار پیش‌فرض:_ `""`.

`sha1` (رشته؛ _اختیاری_)
: هش SHA-1 خروجی derivation / اشتقاق ساختِ `fetchurl` به قالبی که مورد انتظار Nix است.
  برای اطلاعات بیشتر درباره قالب آن، [مستندات راهنمای Nix](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-outputHash) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توصیه می‌شود به جای آن از صفت (attribute) `hash` استفاده کنید.

  _مقدار پیش‌فرض:_ `""`.

`sha256` (رشته؛ _اختیاری_)
: هش SHA-256 خروجی derivation / اشتقاق ساختِ `fetchurl` به قالبی که مورد انتظار Nix است.
  برای اطلاعات بیشتر درباره قالب آن، [مستندات راهنمای Nix](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-outputHash) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توصیه می‌شود به جای آن از صفت (attribute) `hash` استفاده کنید.

  _مقدار پیش‌فرض:_ `""`.

`sha512` (رشته؛ _اختیاری_)
: هش SHA-512 خروجی derivation / اشتقاق ساختِ `fetchurl` به قالبی که مورد انتظار Nix است.
  برای اطلاعات بیشتر درباره قالب آن، [مستندات راهنمای Nix](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-outputHash) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> توصیه می‌شود به جای آن از صفت (attribute) `hash` استفاده کنید.

  _مقدار پیش‌فرض:_ `""`.

`name` (رشته؛ _اختیاری_)
: نام نمادین فایل بارگیری‌شده هنگام ذخیره در انبار نیکس (Nix store).
  برای جزئیات درباره نحوه تعیین نام فایل، [بررسی اجمالی `fetchurl`](#sec-pkgs-fetchers-fetchurl) را ببینید.

  _مقدار پیش‌فرض:_ `""`.

`pname` (رشته؛ _اختیاری_)
: یک نام پایه، که با `version` ترکیب می‌شود تا نام نمادین فایل بارگیری‌شده را هنگام ذخیره در انبار نیکس (Nix store) تشکیل دهد.
  برای جزئیات درباره نحوه تعیین نام فایل، [بررسی اجمالی `fetchurl`](#sec-pkgs-fetchers-fetchurl) را ببینید.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> اگر `pname` مشخص شده باشد، باید `version` را نیز مشخص کنید، در غیر این صورت `fetchurl` مقدار `pname` را نادیده خواهد گرفت.

  _مقدار پیش‌فرض:_ `""`.

`version` (رشته؛ _اختیاری_)
: یک نسخه، که با `pname` ترکیب می‌شود تا نام نمادین فایل بارگیری‌شده را هنگام ذخیره در انبار نیکس (Nix store) تشکیل دهد.
  برای جزئیات درباره نحوه تعیین نام فایل، [بررسی اجمالی `fetchurl`](#sec-pkgs-fetchers-fetchurl) را ببینید.

  _مقدار پیش‌فرض:_ `""`.

`recursiveHash` (بولین؛ _اختیاری_) <a id="sec-pkgs-fetchers-fetchurl-inputs-recursiveHash"></a>
: اگر برابر با `true` تنظیم شود، به Nix اعلام می‌کند که هش داده‌شده به `fetchurl` با استفاده از حالت `"recursive"` محاسبه شده است.
  برای اطلاعات بیشتر در مورد حالت‌های موجود، [مستندات راهنمای Nix](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-outputHashMode) را ببینید.

  به طور پیش‌فرض، زمانی که صفت (attribute) `executable` روی `true` تنظیم شده باشد، `fetchurl` از حالت `"recursive"` استفاده می‌کند، بنابراین در این حالت نیازی به مشخص کردن `recursiveHash` ندارید.

  _مقدار پیش‌فرض:_ `false`.

`executable` (بولین؛ _اختیاری_)
: اگر `true` باشد، بیت قابل اجرا را روی فایل بارگیری‌شده تنظیم می‌کند.

  _مقدار پیش‌فرض:_ `false`.

`downloadToTemp` (بولین؛ _اختیاری_) <a id="sec-pkgs-fetchers-fetchurl-inputs-downloadToTemp"></a>
: اگر `true` باشد، فایل بارگیری‌شده را به جای مکان مورد انتظار در انبار نیکس (Nix store)، در یک مکان موقت ذخیره می‌کند.
  این حالت هنگام استفاده در کنار صفت (attribute) `postFetch` مفید است، در غیر این صورت `fetchurl` هیچ خروجی با‌معنایی تولید نخواهد کرد.

  مکان فایل بارگیری‌شده در متغیر `$downloadedFile` قرار خواهد گرفت، که باید توسط اسکریپت موجود در صفت (attribute) `postFetch` استفاده شود.
  برای درک نحوه کار با این صفت (attribute)، [](#ex-fetchers-fetchurl-nixpkgs-version-postfetch) را ببینید.

  _مقدار پیش‌فرض:_ `false`.

`postFetch` (رشته؛ _اختیاری_)
: اسکریپتی که پس از دانلود موفقیت‌آمیز فایل و قبل از پایان اجرای `fetchurl` اجرا می‌شود.
  برای پس‌پردازش، جهت بررسی یا تغییر دادن فایل به نحوی، مفید است.
  برای درک نحوه کار با این صفت (attribute)، به [](#ex-fetchers-fetchurl-nixpkgs-version-postfetch) مراجعه کنید.

  _مقدار پیش‌فرض:_ `""`.

`netrcPhase` (رشته یا مقدار پوچ (Null)؛ _اختیاری_)
: اسکریپتی که برای ایجاد یک فایل `netrc(5)` جهت استفاده با `curl(1)` اجرا می‌شود.
  این اسکریپت باید فایل `netrc` را (توجه داشته باشید که با "." شروع نمی‌شود) در پوشه‌ای که در حال حاضر در آن اجرا می‌شود (`$PWD`) ایجاد کند.

  این اسکریپت در طول آماده‌سازی انجام‌شده توسط `fetchurl` و قبل از اجرای هر کدی برای دانلود محتوای مشخص‌شده اجرا می‌شود.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> در صورت مشخص شدن، `fetchurl` به طور خودکار فراخوانی `curl(1)` را برای استفاده از فایل `netrc` تغییر می‌دهد، بنابراین نیازی به اضافه کردن هیچ چیزی به `curlOpts` یا `curlOptsList` ندارید.

> <span class="admonition-kind" data-kind="caution"></span>
>
> **احتیاط**
>
> از آنجا که `netrcPhase` باید در کد منبع Nix شما مشخص شود، هرگونه اطلاعات محرمانه‌ای که مستقیماً در آن قرار دهید بر اساس طراحی، قابل‌خواندن برای همگان خواهد بود (هم در کد منبع شما و هم زمانی که derivation در انبار Nix ایجاد می‌شود).
>
>   اگر می‌خواهید از این رفتار اجتناب کنید، مستندات `netrcImpureEnvVars` را برای روشی جایگزین جهت مواجهه با این اطلاعات محرمانه ببینید.

  _مقدار پیش‌فرض_: `null`.

`netrcImpureEnvVars` (فهرستی از رشته‌ها؛ _اختیاری_)
: در صورت مشخص شدن، `fetchurl` این نام‌های متغیرهای محیطی را به فهرست [متغیرهای محیطی ناخالص](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-impureEnvVars) اضافه می‌کند، که از محیط کاربر فراخواننده به سازنده (Builder) اجراکننده کد `fetchurl` منتقل می‌شوند.

  این مورد هنگام استفاده همراه با `netrcPhase` برای پنهان کردن اطلاعات محرمانه‌ای که در آن استفاده می‌شود مفید است، زیرا اسکریپت موجود در `netrcPhase` به جای آن تنها نیاز دارد به متغیرهای محیطی حاوی اطلاعات محرمانه ارجاع دهد.
  با این حال، توجه داشته باشید که این متغیرها به یک دلیل متغیرهای _ناخالص_ نامیده می‌شوند:
  محیطی که ساخت (Build) را آغاز می‌کند باید این متغیرها را اعلام کرده باشد تا همه چیز به درستی کار کند، که به این معنی است که به آماده‌سازی اضافی خارج از آنچه Nix کنترل می‌کند نیاز است.

  _مقدار پیش‌فرض:_ `[]`.

`curlOpts` (رشته؛ _اختیاری_)
: در صورت مشخص شدن، این مقدار هنگام دانلود URL(های) داده‌شده به `fetchurl` به فراخوانی `curl(1)` اضافه می‌شود.
  چندین آرگومان معمولاً می‌توانند با فاصله از هم جدا شوند، اما مقادیر دارای فاصله خالی به عنوان چند آرگومان (به جای یک مقدار واحد) تفسیر می‌شوند، حتی اگر آن مقدار اسکیپ شده باشد.
  برای روشی جهت ارسال مقادیر دارای فاصله خالی، `curlOptsList` را ببینید.

  _مقدار پیش‌فرض:_ `""`.

`curlOptsList` (فهرستی از رشته‌ها؛ _اختیاری_)
: در صورت مشخص شدن، هر عنصر از این فهرست هنگام دانلود URL(های) داده‌شده به `fetchurl` به عنوان یک آرگومان به فراخوانی `curl(1)` پاس داده می‌شود.
  این امکان ارسال مقادیری را که شامل فاصله هستند بدون نیاز به اسکیپ کردن فراهم می‌کند.

  _مقدار پیش‌فرض:_ `[]`.

`showURLs` (بولی (Boolean)؛ _اختیاری_)
: اگر روی `true` تنظیم شود، این امر مانع از دانلود هر چیزی توسط `fetchurl` می‌شود.
  در عوض، فهرستی از تمام URLهایی را که برای دانلود محتوا استفاده می‌کرد (مثلاً پس از حل کردن URLهای `mirror://`) خروجی می‌دهد.
  این برای دیباگ (اشکال‌زدایی) مفید است.

  _مقدار پیش‌فرض:_ `false`.

`meta` (مجموعه صفات (Attribute Set)؛ _اختیاری_)
: هرگونه [ویژگی‌های فراداده (meta-attributes)](#chap-meta) را برای derivation بازگردانده‌شده توسط `fetchurl` مشخص می‌کند.

  _مقدار پیش‌فرض:_ `{'{'}'{'{'}'{'}'}{'{'}'{'}'}'{'}'}`.

`passthru` (مجموعه ویژگی؛ _اختیاری_)
: مشخص‌کنندهٔ هرگونه ویژگی‌های اضافی [`passthru`](#chap-passthru) برای derivation بازگردانده‌شده توسط `fetchurl` است.
  توجه داشته باشید که `fetchurl` [ویژگی‌های `passthru` مخصوص به خود را](#ssec-pkgs-fetchers-fetchurl-passthru-outputs) تعریف می‌کند.
  ویژگی‌های مشخص‌شده در `passthru` می‌توانند ویژگی‌های پیش‌فرض بازگردانده‌شده توسط `fetchurl` را بازنشانی کنند.

  _مقدار پیش‌فرض:_ `{'{'}'{'{'}'{'}'}{'{'}'{'}'}'{'}'}`.

`preferLocalBuild` (بولین؛ _اختیاری_)
: این همان ویژگی است که [در راهنمای Nix تعریف شده است](https://nixos.org/manual/nix/stable/language/advanced-attributes.html#adv-attr-preferLocalBuild).
  این مقدار به صورت پیش‌فرض `true` است زیرا دانلود محتوا توسط یک ماشین راه دور صرفاً ترافیک شبکه را دوبرابر می‌کند (زیرا ماشین محلی ممکن است در هر صورت نتایج حاصل از derivation را بارگیری کند)، اما این گزینه می‌تواند در مواردی که دسترسی به شبکه در ماشین‌های محلی محدود شده است مفید باشد.

  _مقدار پیش‌فرض:_ `true`.

`nativeBuildInputs` (لیستی از مجموعه‌های ویژگی؛ _اختیاری_)
: بسته‌های اضافی مورد نیاز برای بارگیری محتوا.
  این گزینه برای مثال زمانی مفید است که به بسته‌های اضافی برای `postFetch` یا `netrcPhase` نیاز داشته باشید.
  دارای معانی یکسان با [](#var-stdenv-nativeBuildInputs) است.
  برای درک نحوه استفاده از این ویژگی با `postFetch` به [](#ex-fetchers-fetchurl-nixpkgs-version-postfetch) مراجعه کنید.

  _مقدار پیش‌فرض:_ `[]`.

### <a id="ssec-pkgs-fetchers-fetchurl-passthru-outputs"></a> خروجی‌های Passthru

همچنین `fetchurl` ویژگی‌های [`passthru`](#chap-passthru) مخصوص به خود را تعریف می‌کند:

`url` (رشته)

: همان ویژگی `url` که در آرگومان به `fetchurl` پاس داده شده است.

### <a id="ssec-pkgs-fetchers-fetchurl-examples"></a> نمونه‌ها

<a id="ex-fetchers-fetchurl-nixpkgs-version"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استفاده از `fetchurl` برای بارگیری یک فایل
>
> بسته زیر یک فایل کوچک را از یک URL بارگیری می‌کند و رایج‌ترین روش استفاده از `fetchurl` را نشان می‌دهد:
>

> ```nix
> { fetchurl }:
> fetchurl {
>   url = "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version";
>   hash = "sha256-BZqI7r0MNP29yGH5+yW2tjU9OOpOCEvwWKrWCv5CQ0I=";
> }
> ```
>
> پس از ساخت بسته، فایل بارگیری شده و در انبار نیکس (Nix store) قرار خواهد گرفت:
>

> ```shell
> $ nix-build
> (output removed for clarity)
> /nix/store/4g9y3x851wqrvim4zcz5x2v3zivmsq8n-version
>
> $ cat /nix/store/4g9y3x851wqrvim4zcz5x2v3zivmsq8n-version
> 23.11
> ```

<a id="ex-fetchers-fetchurl-nixpkgs-version-multiple-urls"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استفاده از `fetchurl` برای بارگیری یک فایل با چند URL ممکن
>
> بسته زیر [](#ex-fetchers-fetchurl-nixpkgs-version) را برای استفاده از چند URL تطبیق می‌دهد.
> نخستین URL عمداً به‌گونه‌ای طراحی شده است که خطایی برگرداند تا نشان دهد چگونه `fetchurl` چندین URL را امتحان می‌کند تا زمانی که یکی را پیدا کند که کار کند (یا همه URLها با شکست مواجه شوند).
>

> ```nix
> { fetchurl }:
> fetchurl {
>   urls = [
>     "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/does-not-exist"
>     "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version"
>   ];
>   hash = "sha256-BZqI7r0MNP29yGH5+yW2tjU9OOpOCEvwWKrWCv5CQ0I=";
> }
> ```
>
> پس از ساخت بسته، هر دو URL برای بارگیری فایل استفاده خواهند شد:
>

> ```shell
> $ nix-build
> (some output removed for clarity)
> trying https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/does-not-exist
> (some output removed for clarity)
> curl: (22) The requested URL returned error: 404
>
> trying https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version
> (some output removed for clarity)
> /nix/store/n9asny31z32q7sdw6a8r1gllrsfy53kl-does-not-exist
>
> $ cat /nix/store/n9asny31z32q7sdw6a8r1gllrsfy53kl-does-not-exist
> 23.11
> ```
>
> با این حال، توجه داشته باشید که نام فایل از اولین URL گرفته شده است (این موضوع در [بررسی کلی `fetchurl`](#sec-pkgs-fetchers-fetchurl) بیشتر توضیح داده شده است).
> برای اطمینان از اینکه نتیجه بدون توجه به اینکه از کدام URLها استفاده می‌شود دارای نام یکسانی خواهد بود، می‌توانیم بسته را تغییر دهیم:
>

> ```nix
> { fetchurl }:
> fetchurl {
>   name = "nixpkgs-version";
>   urls = [
>     "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/does-not-exist"
>     "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version"
>   ];
>   hash = "sha256-BZqI7r0MNP29yGH5+yW2tjU9OOpOCEvwWKrWCv5CQ0I=";
> }
> ```
>
> پس از ساخت بسته، نتیجه نامی را که مشخص کرده‌ایم خواهد داشت:
>

> ```shell
> $ nix-build
> (output removed for clarity)
> /nix/store/zczb6wl3al6jm9sm5h3pr6nqn0i5ji9z-nixpkgs-version
> ```

<a id="ex-fetchers-fetchurl-nixpkgs-version-postfetch"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # دستکاری محتوای بارگیری‌شده توسط `fetchurl`
>
> ممکن است دستکاری مستقیم محتوای بارگیری‌شده توسط `fetchurl` در derivation آن مفید باشد.
> در این مثال، [](#ex-fetchers-fetchurl-nixpkgs-version) را طوری تطبیق می‌دهیم تا نتیجه‌ی اجرای بسته `hello` به محتوایی که بارگیری می‌کنیم اضافه شود، صرفاً برای اینکه نحوه دستکاری محتوا را نشان دهیم.
>

> ```nix
> {
>   fetchurl,
>   hello,
>   lib,
> }:
> fetchurl {
>   url = "https://raw.githubusercontent.com/NixOS/nixpkgs/23.11/.version";
>
>   nativeBuildInputs = [ hello ];
>
>   downloadToTemp = true;
>   postFetch = ''
>     hello >> "$downloadedFile"
>     mv "$downloadedFile" "$out"
>   '';
>
>   hash = "sha256-ceooQQYmDx5+0nfg40uU3NNI2yKrixP7HZ/xLZUNv+w=";
> }
> ```
>
> پس از ساخت بسته، عبارت "Hello, world!" به انتهای فایل حاصل اضافه خواهد شد:
>

> ```shell
> $ nix-build
> (output removed for clarity)
> /nix/store/ifi6pp7q0ag5h7c5v9h1c1c7bhd10c7f-version
>
> $ cat /nix/store/ifi6pp7q0ag5h7c5v9h1c1c7bhd10c7f-version
> 23.11
> Hello, world!
> ```
>
> توجه داشته باشید که `hash` مشخص‌شده در بسته با هش مشخص‌شده در [](#ex-fetchers-fetchurl-nixpkgs-version) متفاوت است، زیرا محتویات خروجی تغییر کرده است (اگرچه فایل واقعی بارگیری‌شده یکسان است).
> برای جزئیات بیشتر درباره نحوه کار با صفت `hash` هنگام تغییر خروجی، به [](#chap-pkgs-fetchers-caveats) مراجعه کنید.

## <a id="sec-pkgs-fetchers-fetchzip"></a> `fetchzip`

یک [derivation با خروجی ثابت](https://nixos.org/manual/nix/stable/glossary.html#gloss-fixed-output-derivation) برمی‌گرداند که یک آرشیو را از یک URL مشخص بارگیری کرده و آن را از حالت فشرده خارج می‌کند.

برخلاف نامش، `fetchzip` به فایل‌های `.zip` محدود نمی‌شود و به‌طور پیش‌فرض می‌توان از آن برای [قالب‌های مختلف تاربال فشرده‌شده](#tar-files) نیز استفاده کرد.
این قابلیت را می‌توان با مشخص کردن صفت‌های اضافی گسترش داد، برای درک نحوه انجام این کار به [](#ex-fetchers-fetchzip-rar-archive) مراجعه کنید.

### <a id="sec-pkgs-fetchers-fetchzip-inputs"></a> ورودی‌ها

`fetchzip` به یک مجموعه ویژگی نیازمند است و بیشتر صفت‌ها به فراخوانی زیرین [`fetchurl`](#sec-pkgs-fetchers-fetchurl) منتقل می‌شوند.

صفت‌های زیر در `fetchzip` در مقایسه با آنچه `fetchurl` انتظار دارد، به‌گونه‌ای متفاوت پردازش می‌شوند:

`name` (رشته؛ _اختیاری_)
: مانند آنچه در `fetchurl` تعریف شده کار می‌کند، اما مقدار پیش‌فرض متفاوتی نسبت به `fetchurl` دارد.

  _مقدار پیش‌فرض:_ `"source"`.

`nativeBuildInputs` (لیستی از مجموعه ویژگی؛ _اختیاری_)
: مانند آنچه در `fetchurl` تعریف شده کار می‌کند، اما توسط `fetchzip` نیز افزوده می‌شود تا شامل بسته‌هایی برای مواجهه با آرشیوهای اضافی (مانند `.zip`) باشد.

  _مقدار پیش‌فرض:_ `[]`.

`postFetch` (رشته؛ _اختیاری_)
: مانند آنچه در `fetchurl` تعریف شده کار می‌کند، اما کد مورد نیاز برای عملکرد `fetchzip` نیز به آن افزوده می‌شود.

> <span class="admonition-kind" data-kind="caution"></span>
>
> **احتیاط**
>
> تغییر فایل‌ها در `$out` فقط در `postFetch` ایمن است.
>   برای موارد پیچیده‌تر، به پیاده‌سازی `fetchzip` مراجعه کنید.

  _مقدار پیش‌فرض:_ `""`.

`stripRoot` (بولی؛ _اختیاری_)
: اگر `true` باشد، محتویات از حالت فشرده خارج‌شده یک سطح در درخت پوشه به بالا منتقل می‌شوند.

  این ویژگی برای آرشیوهایی مفید است که در یک پوشه منفرد از حالت فشرده خارج می‌شوند که معمولاً شامل مقادیری است که با زمان تغییر می‌کنند، مانند شماره نسخه‌ها.
  در این حالت (و وقتی `stripRoot` برابر `true` است)، `fetchzip` این پوشه را حذف کرده و محتویات از حالت فشرده خارج‌شده را در پوشه سطح بالا در دسترس قرار می‌دهد.

  [](#ex-fetchers-fetchzip-simple-striproot) نشان می‌دهد که این صفت چه کاری انجام می‌دهد.

  این صفت به `fetchurl` منتقل **نمی‌شود**.

  _مقدار پیش‌فرض:_ `true`.

`extension` (رشته یا تهی؛ _اختیاری_)
: در صورت تنظیم، نام آرشیو بارگیری‌شده توسط `fetchzip` به نام فایلی با پسوند مشخص‌شده در این صفت تغییر می‌یابد.

  این امر هنگام پشتیبانی `fetchzip` از انواع اضافی آرشیوها مفید است، زیرا ممکن است پیاده‌سازی از پسوند یک آرشیو برای تعیین اینکه آیا می‌تواند آن را از حالت فشرده خارج کند یا خیر، استفاده کند.
  اگر URLی که برای بارگیری محتویات استفاده می‌کنید با پسوند مرتبط با آرشیو ختم نمی‌شود، از این صفت برای اصلاح نام فایل آرشیو استفاده کنید.

  این صفت به `fetchurl` منتقل **نمی‌شود**.

  _مقدار پیش‌فرض:_ `null`.

`recursiveHash` (بولی؛ _اختیاری_)
: [مانند آنچه در `fetchurl` تعریف شده](#sec-pkgs-fetchers-fetchurl-inputs-recursiveHash) کار می‌کند، اما مقدار پیش‌فرض آن با `fetchurl` متفاوت است.

  _مقدار پیش‌فرض:_ `true`.

`downloadToTemp` (بولی؛ _اختیاری_)
: [مانند آنچه در `fetchurl` تعریف شده](#sec-pkgs-fetchers-fetchurl-inputs-downloadToTemp) کار می‌کند، اما مقدار پیش‌فرض آن با `fetchurl` متفاوت است.

  _مقدار پیش‌فرض:_ `true`.

`extraPostFetch` **منسوخ‌شده**
: این صفت (attribute) منسوخ شده است.
  لطفاً به جای آن از `postFetch` استفاده کنید.

  این صفت (attribute) به `fetchurl` منتقل **نمی‌شود**.

### <a id="sec-pkgs-fetchers-fetchzip-examples"></a> نمونه‌ها

<a id="ex-fetchers-fetchzip-simple-striproot"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استفاده از `fetchzip` برای خروجی مستقیم محتوا
>
> دستورالعمل زیر نحوه استفاده از `fetchzip` را برای خارج کردن یک آرشیو `.tar.gz` از حالت فشرده نشان می‌دهد:
>

> ```nix
> { fetchzip }:
> fetchzip {
>   url = "https://github.com/NixOS/patchelf/releases/download/0.18.0/patchelf-0.18.0.tar.gz";
>   hash = "sha256-3ABYlME9R8klcpJ7MQpyFEFwHmxDDEzIYBqu/CpDYmg=";
> }
> ```
>
> این آرشیو تمام محتویات خود را در پوشه‌ای به نام `patchelf-0.18.0` دارد.
> این بدان معناست که پس از خارج کردن از حالت فشرده، باید وارد این پوشه شوید تا محتویات آرشیو را ببینید.
> با این حال، `fetchzip` این کار را از طریق صفت `stripRoot` (که به طور پیش‌فرض فعال است) آسان‌تر می‌کند.
>
> پس از ساخت دستورالعمل، خروجی derivation تمام فایل‌های موجود در آرشیو را در سطح بالا نشان خواهد داد:
>

> ```shell
> $ nix-build
> (output removed for clarity)
> /nix/store/1b7h3fvmgrcddvs0m299hnqxlgli1yjw-source
>
> $ ls /nix/store/1b7h3fvmgrcddvs0m299hnqxlgli1yjw-source
> aclocal.m4  completions  configure.ac  m4           Makefile.in  patchelf.spec     README.md  tests
> build-aux   configure    COPYING       Makefile.am  patchelf.1   patchelf.spec.in  src        version
> ```
>
> اگر `stripRoot` روی `false` تنظیم شود، خروجی derivation همان آرشیو فشرده‌زدایی‌شده به همان صورت خواهد بود:
>

> ```nix
> { fetchzip }:
> fetchzip {
>   url = "https://github.com/NixOS/patchelf/releases/download/0.18.0/patchelf-0.18.0.tar.gz";
>   hash = "sha256-uv3FuKE4DqpHT3yfE0qcnq0gYjDNQNKZEZt2+PUAneg=";
>   stripRoot = false;
> }
> ```
>
> > <span class="admonition-kind" data-kind="caution"></span>
> >
> > **احتیاط**
> >
> > هش تغییر کرد!
> > هرگاه صفات یک دریافت‌کننده Nixpkgs را تغییر می‌دهید، [به یاد داشته باشید که هش را باطل کنید](#chap-pkgs-fetchers-caveats)، در غیر این صورت نتایجی را که انتظار دارید به دست نخواهید آورد!
>
>
> پس از ساخت دستور ساخت:
>

> ```shell
> $ nix-build
> (output removed for clarity)
> /nix/store/2hy5bxw7xgbgxkn0i4x6hjr8w3dbx16c-source
>
> $ ls /nix/store/2hy5bxw7xgbgxkn0i4x6hjr8w3dbx16c-source
> patchelf-0.18.0
> ```

<a id="ex-fetchers-fetchzip-rar-archive"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استفاده از `fetchzip` برای از حالت فشرده خارج کردن یک فایل `.rar`
>
> بسته `unrar` یک [قلاب راه‌اندازی](#ssec-setup-hooks) برای از حالت فشرده خارج کردن آرشیوهای `.rar` در طول [فاز استخراج](#ssec-unpack-phase) ارائه می‌دهد، که می‌توان از آن به همراه `fetchzip` برای استخراج آن آرشیوها استفاده کرد:
>

> ```nix
> { fetchzip, unrar }:
> fetchzip {
>   url = "https://archive.org/download/SpaceCadet_Plus95/Space_Cadet.rar";
>   hash = "sha256-fC+zsR8BY6vXpUkVd6i1jF0IZZxVKVvNi6VWCKT+pA4=";
>   stripRoot = false;
>   nativeBuildInputs = [ unrar ];
> }
> ```
>
> از آنجا که این فایل `.rar` به‌خصوص، محتویات خود را درون یک پوشه داخل آرشیو قرار نمی‌دهد، مقدار `stripRoot` باید برابر با `false` تنظیم شود.
>
> پس از ساخت این دستورالعمل، خروجی derivation فایل‌های خارج‌شده از حالت فشرده را نشان خواهد داد:
>

> ```shell
> $ nix-build
> (output removed for clarity)
> /nix/store/zpn7knxfva6rfjja2gbb4p3l9w1f0d36-source
>
> $ ls /nix/store/zpn7knxfva6rfjja2gbb4p3l9w1f0d36-source
> FONT.DAT      PINBALL.DAT  PINBALL.EXE	PINBALL2.MID  TABLE.BMP    WMCONFIG.EXE
> MSCREATE.DIR  PINBALL.DOC  PINBALL.MID	Sounds	     WAVEMIX.INF
> ```

## <a id="fetchpatch"></a> `fetchpatch`

`fetchpatch` بسیار شبیه به `fetchurl` عمل می‌کند و آرگومان‌های یکسانی را انتظار دارد. این تابع فایل‌های پچ را به عنوان سورس در نظر می‌گیرد و قبل از محاسبه‌ی چک‌سام، آن‌ها را نرمال‌سازی می‌کند. برای مثال، کامنت‌ها یا سایر بخش‌های ناپایداری را که گاهی توسط سیستم‌های کنترل نسخه اضافه می‌شوند و ممکن است به مرور زمان تغییر کنند، حذف می‌کند.

- `relative`: مشابه استفاده از پرچم `--relative` در `git-diff`، تنها تغییرات داخل پوشه‌ی مشخص‌شده را نگه‌می‌دارد و مسیرها را نسبت به آن نسبی می‌کند.
- `stripLen`: اولین مؤلفه‌های `stripLen` را از مسیر فایل‌ها در پچ حذف می‌کند.
- `decode`: داده‌های دانلودشده را قبل از پردازش به عنوان پچ، از طریق این دستور هدایت (pipe) می‌کند.
- `extraPrefix`: این رشته را به عنوان پیشوند به مسیر فایل‌ها اضافه می‌کند.
- `excludes`: فایل‌های منطبق با این الگوها را مستثنی می‌کند (بعد از آرگومان‌های بالا اعمال می‌شود).
- `includes`: تنها فایل‌های منطبق با این الگوها را شامل می‌شود (بعد از آرگومان‌های بالا اعمال می‌شود).
- `hunks`: هانک‌های (hunks) مشخص‌شده را از هر فایل انتخاب می‌کند (بعد از آرگومان‌های بالا اعمال می‌شود).
  توجه داشته باشید که می‌توانید لیستی از اعداد یا بازه‌هایی از اعداد را مشخص کنید
  (برای مثال، `[ 1 2 3 4 ]`، `[ "1-4" ]`، `[ "-4" ]` یا `[ "1-" ]` همگی بازه مؤثر یکسانی در پچی خواهند بود که ۴ هانک را روی یک فایل اعمال می‌کند).
- `revert`: پچ را بازگردانی (revert) می‌کند.

توجه داشته باشید که چون چک‌سام پس از اعمال این تغییرات محاسبه می‌شود، استفاده یا تغییر این آرگومان‌ها هیچ تأثیری نخواهد داشت مگر اینکه آرگومان `hash` نیز تغییر داده شود.

اکثر دریافت‌کننده‌های دیگر به جای یک فایل تکی، یک پوشه برمی‌گردانند.

## <a id="fetchdebianpatch"></a> `fetchDebianPatch`

یک پوسته (wrapper) حول `fetchpatch` است که موارد زیر را دریافت می‌کند:
- `patch` و `hash`: نام فایل پچ،
  و هش آن پس از نرمال‌سازی توسط `fetchpatch`؛
- `pname`: نام بسته سورس Debian؛
- `version`: شماره نسخه آپ‌استریم (upstream)؛
- `debianRevision`: [Debian revision number] (در صورت وجود)؛
- `area` مربوط به آرشیو Debian: `main` (پیش‌فرض)، `contrib` یا `non-free`.

در ادامه یک نمونه از به‌کارگیری `fetchDebianPatch` آورده شده است:

```nix
{
  lib,
  fetchDebianPatch,
  buildPythonPackage,
}:

buildPythonPackage rec {
  pname = "pysimplesoap";
  version = "1.16.2";
  src = <...>;

  patches = [
    (fetchDebianPatch {
      inherit pname version;
      debianRevision = "5";
      patch = "Add-quotes-to-SOAPAction-header-in-SoapClient.patch";
      hash = "sha256-xA8Wnrpr31H8wy3zHSNfezFNjUJt1HbSXn3qUMzeKc0=";
    })
  ];

  # ...
}
```

پچ‌ها از `sources.debian.org` دریافت می‌شوند و بنابراین باید از نسخه بسته‌ای باشند که در آرشیو Debian بارگذاری شده است. بسته‌ها ممکن است پس از اینکه آن نسخه خاص دیگر در هیچ یک از مجموعه‌ها (مجموعه‌هایی مانند stable، testing، unstable و غیره) قرار نداشت، از آنجا حذف شوند؛ بنابراین نگه‌دارندگان باید از `copy-tarballs.pl` برای آرشیو کردن پچ استفاده کنند، اگر لازم است که برای مدت طولانی‌تری در دسترس باشد.

[Debian revision number]: https://www.debian.org/doc/debian-policy/ch-controlfields.html#version

## <a id="fetchsvn"></a> `fetchsvn`

همراه با Subversion استفاده می‌شود. انتظار یک `url` به یک پوشه Subversion، یک `rev` و یک `hash` را دارد.

## <a id="fetchgit"></a> `fetchgit`

همراه با Git استفاده می‌شود. انتظار یک `url` به یک مخزن Git، یک `rev` یا `tag` و یک `hash` را دارد. `rev` در این حالت می‌تواند شناسه کامیت کامل Git (هش SHA1) باشد، یا می‌توانید از `tag` برای نام تگ مانند `refs/tags/v1.0` استفاده کنید.

اگر می‌خواهید یک تگ را دریافت کنید، باید به جای `rev` پارامتر `tag` را پاس دهید که تأثیری مشابه با تنظیم `rev = "refs/tags"/${'{'}'{'{'}'{'}'}version{'{'}'{'}'}'{'}'}"` دارد.
این کار از نظر تداخل‌های احتمالی نام شاخه و تگ، ایمن‌تر از تنظیم ساده‌ی `rev = version` است.

علاوه بر این، آرگومان‌های اختیاری زیر را می‌توان ارائه داد:

*`fetchSubmodules`* (Boolean)

: آیا زیرماژول‌های یک مخزن نیز دریافت شوند یا خیر.

*`fetchLFS`* (Boolean)

: آیا اشیای LFS دریافت شوند یا خیر.

*`preFetch`* (String)

: کد شل که قرار است قبل از دریافت مخزن اجرا شود تا اجازه تغییر محیطی که دریافت‌کننده در آن اجرا می‌شود را بدهد.

*`postFetch`* (String)

: کد شل که پس از دریافت موفقیت‌آمیز مخزن اجرا می‌شود. این کد می‌تواند کارهایی مانند بررسی یا تغییر شکل فایل را انجام دهد.

*`leaveDotGit`* (Boolean)

: آیا پوشه `.git` نسخه کلون‌شده نباید پس از checkout حذف شود یا خیر.

  با این حال توجه داشته باشید که فرمت مخزن Git پایدار نیست و بنابراین این پرچم به خودی خود برای استفاده واقعی مناسب نیست.
  تنها از این گزینه برای اهداف تست یا همراه با حذف پوشه `.git` در `postFetch` استفاده کنید.

*`deepClone`* (Boolean)

: کلون کردن کامل مخزن به جای ایجاد یک کلون سطحی (shallow clone).
  این گزینه دلالت بر `leaveDotGit` دارد.

*`fetchTags`* (Boolean)

: آیا تمام تگ‌ها از مخزن راه دور دریافت شوند یا خیر. این گزینه زمانی مفید است که فرآیند ساخت نیاز به اجرای `git describe` یا سایر دستوراتی داشته باشد که به اطلاعات تگ نیاز دارند. این پارامتر مستلزم `leaveDotGit` است، زیرا تگ‌ها در پوشه `.git` ذخیره می‌شوند.

*`sparseCheckout`* (List of String)

: جلوگیری از دریافت بلاک‌های داده (blob) غیرضروری از سرور توسط Git.
  این گزینه زمانی مفید است که فقط بخش‌هایی از مخزن مورد نیاز باشد.

<a id="ex-fetchgit-sparseCheckout"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # از `sparseCheckout` برای شامل کردن تنها برخی پوشه‌ها استفاده کنید:

> ```nix
>   { stdenv, fetchgit }:
>
>   stdenv.mkDerivation {
>     name = "hello";
>     src = fetchgit {
>       url = "https://...";
>       sparseCheckout = [
>         "directory/to/be/included"
>         "another/directory"
>       ];
>       hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
>     };
>   }
>   ```

  برای اطلاعات بیشتر، [git sparse-checkout](https://git-scm.com/docs/git-sparse-checkout) را ببینید.

*`rootDir`* (رشته)

: وقتی خالی نباشد، فقط محتویات زیرپوشهٔ مخزن (Repository) را در نتیجه کپی می‌کند. به‌طور خودکار `sparseCheckout` و `nonConeMode` را تنظیم می‌کند تا از دریافت بخش‌های اضافی جلوگیری شود. با `leaveDotGit` ناسازگار است.

برخی از پارامترهای اضافی برای موارد استفاده خاص را می‌توان در پارامترهای تابع در اعلان `fetchgit` یافت: `pkgs/build-support/fetchgit/default.nix`.
ممکن است پارامترهای جدیدی در آینده اضافه شوند بدون اینکه بلافاصله در اینجا مستند شوند.

## <a id="fetchfossil"></a> `fetchfossil`

همراه با Fossil استفاده می‌شود. انتظار `url` به یک آرشیو Fossil، `rev` و `hash` را دارد.

## <a id="fetchcvs"></a> `fetchcvs`

همراه با CVS استفاده می‌شود. انتظار `cvsRoot`، `tag` و `hash` را دارد.

## <a id="fetchhg"></a> `fetchhg`

همراه با Mercurial استفاده می‌شود. انتظار `url`، `rev` و `hash` را دارد که با [`&lt;pkg&gt;.overrideAttrs`](#sec-pkg-overrideAttrs) قابل بازنشانی است.

تعدادی از توابع دریافت‌کننده (fetcher)، بخشی از `fetchurl` و `fetchzip` را پوشش می‌دهند. این توابع عمدتاً توابع کمکی جهت راحتی کار برای مقاصد پرکاربرد کد منبع در مجموعه‌ی بسته‌های نیکس (Nixpkgs) هستند. این دریافت‌کننده‌های پوشش‌دهنده در زیر آورده شده‌اند.

## <a id="fetchfromgitea"></a> `fetchFromGitea`، `fetchFromForgejo` و `fetchFromCodeberg`

`fetchFromGitea` که نام مستعار آن `fetchFromForgejo` نیز هست، انتظار پنج آرگومان دارد. `domain` نام سرور Gitea/Forgejo است. `owner` یک رشته مربوط به کاربر یا سازمانی است که این مخزن (Repository) را کنترل می‌کند. `repo` مربوط به نام مخزن نرم‌افزار است. این‌ها در بالای هر صفحه HTML در Gitea/Forgejo به صورت `owner`/`repo` قرار دارند. `rev` مربوط به هش کامیت Git یا برچسب (مانند `v1.0`) است که از Git بارگیری خواهد شد. در نهایت، `hash` مربوط به هش پوشه استخراج‌شده است. باز هم الگوریتم‌های هش دیگری نیز در دسترس هستند، اما در حال حاضر `hash` ترجیح داده می‌شود.

از آنجا که &lt;codeberg.org&gt; در حال حاضر محبوب‌ترین سرور عمومی Forgejo است، دریافت‌کننده `fetchFromCodeberg` نیز در دسترس است که صفت `domain` را از قبل مقداردهی می‌کند.

## <a id="fetchfromgithub"></a> `fetchFromGitHub`

`fetchFromGitHub` انتظار چهار آرگومان دارد. `owner` یک رشته مربوط به کاربر یا سازمان GitHub است که این مخزن (Repository) را کنترل می‌کند. `repo` مربوط به نام مخزن نرم‌افزار است. این‌ها در بالای هر صفحه HTML در GitHub به صورت `owner`/`repo` قرار دارند. `rev` مربوط به هش کامیت Git یا برچسب (مانند `v1.0`) است که از Git بارگیری خواهد شد. اما اگر نیاز به دریافت یک برچسب دارید، بهتر است از پارامتر `tag` استفاده کنید که این کار را به روشی امن‌تر و با کد تکراری کمتر انجام می‌دهد. در نهایت، `hash` مربوط به هش پوشه استخراج‌شده است. باز هم الگوریتم‌های هش دیگری نیز در دسترس هستند، اما در حال حاضر `hash` ترجیح داده می‌شود.

برای استفاده از یک نمونه متفاوت GitHub، از `githubBase` استفاده کنید (به‌طور پیش‌فرض `"github.com"` است).

به‌طور پیش‌فرض، `fetchFromGitHub` از `fetchzip` برای بارگیری آرشیو کد منبع GitHub برای بازبینی مشخص‌شده استفاده می‌کند.
با این حال، `fetchFromGitHub` در هر یک از موارد زیر به‌طور خودکار به استفاده از `fetchgit` تغییر حالت می‌دهد:

- `forceFetchGit` ،`leaveDotGit` ،`deepClone` ،`fetchLFS` یا `fetchSubmodules` روی `true` تنظیم شده باشند
- `sparseCheckout` شامل هرگونه درایه‌ای باشد (یک لیست غیرخالی باشد)
- `rootDir` روی یک رشته غیرخالی تنظیم شده باشد

هنگامی که از `fetchgit` استفاده می‌شود، برای مستندات گزینه‌های موجود آن به بخش `fetchgit` مراجعه کنید.

## <a id="fetchfromgitlab"></a> `fetchFromGitLab`

این برای مخازن GitLab استفاده می‌شود. رفتاری مشابه `fetchFromGitHub` دارد و انتظار `owner` ،`repo` ،`rev` و `hash` را دارد.

برای استفاده از یک نمونهٔ مشخص GitLab، از `domain` استفاده کنید (پیش‌فرض آن `"gitlab.com"` است).

## <a id="fetchfromgitiles"></a> `fetchFromGitiles`

این تابع برای مخازن Gitiles استفاده می‌شود. آرگومان‌های مورد انتظار مشابه `fetchgit` هستند.

## <a id="fetchfrombitbucket"></a> `fetchFromBitbucket`

برای مخازن میزبانی‌شده در Bitbucket (`"bitbucket.org"`) متعلق به شرکت استرالیایی Atlassian استفاده می‌شود. این تابع به آرگومان‌های `owner` و `repo` نیاز دارد که هر دو رشته‌هایی هستند که به شناسهٔ فضای کاری (workspace ID) و نام مخزن میزبانی‌شده روی ابر Bitbucket اشاره می‌کنند، و همچنین به یکی از آرگومان‌های `tag` یا `rev` نیاز دارد.

به طور پیش‌فرض، `fetchFromBitbucket` تلاش می‌کند اسنپ‌شات تاربالِ یک کامیت را در `tag` یا `rev` مشخص‌شده از آدرس `https://bitbucket.org/&lt;owner&gt;/&lt;repo&gt;/get/&lt;tag-or-rev&gt;.tar.gz` دریافت کند.

با این حال، در هر یک از حالات زیر، `fetchFromBitbucket` به طور خودکار به استفاده از `fetchgit` سوییچ کرده و دریافت را از `https://bitbucket.org/&lt;owner&gt;/&lt;repo&gt;.git` انجام می‌دهد:

- `forceFetchGit` ،`leaveDotGit` ،`deepClone` ،`fetchLFS` یا `fetchSubmodules` روی `true` تنظیم شده باشند
- `sparseCheckout` شامل ورودی‌هایی باشد (یک لیست غیرخالی باشد)
- `rootDir` روی یک رشته غیرخالی تنظیم شده باشد

هنگامی که `fetchgit` استفاده می‌شود، برای مستندات گزینه‌های موجود آن به بخش `fetchgit` مراجعه کنید.

## <a id="fetchfromrepoorcz"></a> `fetchFromRepoOrCz`

این تابع برای مخازن repo.or.cz استفاده می‌شود. آرگومان‌های مورد انتظار بسیار مشابه `fetchFromGitHub` در بالا هستند.

## <a id="fetchfromsourcehut"></a> `fetchFromSourcehut`

این تابع برای مخازن sourcehut استفاده می‌شود. مشابه `fetchFromGitHub` در بالا،
انتظار `owner` ،`repo` ،`rev` و `hash` را دارد، اما علامت مدک (~) را در
ابتدای نام کاربری فراموش نکنید! آرگومان‌های مورد انتظار همچنین شامل `vc` ("git" (پیش‌فرض)
یا "hg")، `domain` و `fetchSubmodules` هستند.

اگر `fetchSubmodules` برابر با `true` باشد، `fetchFromSourcehut` به ترتیب از `fetchgit`
یا `fetchhg` استفاده می‌کند در حالی که `fetchSubmodules` یا `fetchSubrepos` روی `true` تنظیم شده‌اند.
در غیر این صورت، دریافت‌کننده از `fetchzip` استفاده می‌کند.

## <a id="fetchfromradicle"></a> `fetchFromRadicle`

این تابع برای مخازن Radicle استفاده می‌شود. آرگومان‌های مورد انتظار مشابه `fetchgit` هستند.

نیازمند یک آرگومان `seed` (مانند `seed.radicle.dev` یا `rosa.radicle.network`) و یک آرگومان `repo`
(شناسهٔ مخزن *بدون* پیشوند `:rad`) است. همچنین یک آرگومان اختیاری `node` را می‌پذیرد که
شامل شناسهٔ گرهی است که باید ref مشخص‌شده از آن دریافت شود. اگر `node` برابر با `null` (پیش‌فرض)
باشد، در عوض یک ref استاندارد (canonical ref) دریافت می‌شود.

```nix
fetchFromRadicle {
  seed = "seed.radicle.dev";
  repo = "z3gqcJUoA1n9HaHKufZs5FCSGazv5"; # heartwood
  tag = "releases/1.3.0";
  hash = "sha256-4o88BWKGGOjCIQy7anvzbA/kPOO+ZsLMzXJhE61odjw=";
}
```

## <a id="fetchradiclepatch"></a> `fetchRadiclePatch`

`fetchRadiclePatch` بسیار شبیه به `fetchFromRadicle` کار می‌کند و تقریباً همان آرگومان‌ها را انتظار دارد. با این حال، به جای آرگومان `rev` یا `tag`، یک آرگومان `revision` مورد انتظار است که شناسه بازبینی کامل پچ Radicle را برای دریافت شامل می‌شود.

```nix
fetchRadiclePatch {
  seed = "rosa.radicle.network";
  repo = "z4V1sjrXqjvFdnCUbxPFqd5p4DtH5"; # radicle-explorer
  revision = "d97d872386c70607beda2fb3fc2e60449e0f4ce4"; # patch: d77e064
  hash = "sha256-ttnNqj0lhlSP6BGzEhhUOejKkkPruM9yMwA5p9Di4bk=";
}
```

## <a id="requirefile"></a> `requireFile`

`requireFile` امکان درخواست فایل‌هایی را فراهم می‌کند که به صورت خودکار قابل دریافت نیستند، اما محتوای آن‌ها مشخص است.
این یک راهکار چاره‌سازِ نهایی و مفید برای محدودیت‌های مجوزی است که بازتوزیع را ممنوع می‌کنند، یا برای بارگیری‌هایی که تنها پس از احراز هویت تعاملی در مرورگر قابل دسترسی هستند.
اگر فایل درخواستی در انبار نیکس (Nix store) موجود باشد، derivation حاصل ساخته نخواهد شد، زیرا خروجی مورد انتظار آن از قبل در دسترس است.
در غیر این صورت، سازنده (Builder) اجرا می‌شود، اما با پیامی که نحوهٔ ارائهٔ فایل را به کاربر توضیح می‌دهد با شکست مواجه می‌شود. برای مثال، کد زیر:

```nix
requireFile {
  name = "jdk-${version}_linux-x64_bin.tar.gz";
  url = "https://www.oracle.com/java/technologies/javase-jdk11-downloads.html";
  hash = "sha256-lL00+F7jjT71nlKJ7HRQuUQ7kkxVYlZh//5msD8sjeI=";
}
```
منجر به این پیام خطا می‌شود:
```
***
Unfortunately, we cannot download file jdk-11.0.10_linux-x64_bin.tar.gz automatically.
Please go to https://www.oracle.com/java/technologies/javase-jdk11-downloads.html to download it yourself, and add it to the Nix store
using either
  nix-store --add-fixed sha256 jdk-11.0.10_linux-x64_bin.tar.gz
or
  nix-prefetch-url --type sha256 file:///path/to/jdk-11.0.10_linux-x64_bin.tar.gz

***
```

این تابع فقط باید برای نرم‌افزارهای غیرقابل توزیع مجدد با مجوز غیرآزاد استفاده شود که لازم است کاربر را ملزم به بارگیری دستی آن‌ها کنیم.
این تابع بسته‌هایی تولید می‌کند که نمی‌توانند به صورت خودکار ساخته شوند.

## <a id="fetchtorrent"></a> `fetchtorrent`

`fetchtorrent` انتظار دو آرگومان را دارد. `url` که می‌تواند یک Magnet URI (پیوند مگنت) مانند `magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c` یا یک URL با پروتکل HTTP اشاره‌کننده به یک فایل `.torrent` باشد. همچنین می‌تواند یک آرگومان `config` دریافت کند که یک فایل پیکربندی `settings.json` ایجاد کرده و آن را به `transmission` (برنامه زیرین انجام‌دهنده دریافت) تحویل می‌دهد. گزینه‌های پیکربندی موجود برای `transmission` را می‌توانید در [اینجا](https://github.com/transmission/transmission/blob/main/docs/Editing-Configuration-Files.md#options) پیدا کنید.

```nix
{ fetchtorrent }:

fetchtorrent {
  config = {
    peer-limit-global = 100;
  };
  url = "magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c";
  hash = "";
}
```

### <a id="fetchtorrent-parameters"></a> Parameters

- `url`: یک URI مگنت (پیوند مگنت) مانند `magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c` یا یک URL از نوع HTTP که به یک فایل `.torrent` اشاره می‌کند.

- `backend`: برنامه بیت‌تورنتی که باید استفاده شود. پیش‌فرض: `"transmission"`. مقادیر معتبر `"rqbit"` یا `"transmission"` هستند. در زمان نگارش این متن، این دو مناسب‌ترین کلاینت‌های تورنت برای دریافت در یک درایویشن با خروجی ثابت (fixed-output derivation) هستند، زیرا می‌توان پس از استفاده به راحتی از آن‌ها خارج شد. `rqbit` به زبان Rust نوشته شده است و اندازه closure کوچک‌تری نسبت به `transmission` دارد، و ویژگی‌های عملکرد و کشف همتا (peer discovery) میان این کلاینت‌ها متفاوت است، به طوری که تصمیم‌گیری درباره اینکه کدام‌یک بهترین است نیاز به آزمایش دارد.

- `config`: هنگام استفاده از `transmission` به عنوان `backend`، می‌توان یک پیکربندی JSON به transmission ارائه داد. برای اطلاعات در مورد نحوه پیکربندی، به [مستندات بالادستی](https://github.com/transmission/transmission/blob/main/docs/Editing-Configuration-Files.md) مراجعه کنید.

## <a id="fetchitchio"></a> `fetchItchIo`

`fetchItchIo` یک دریافت‌کننده برای دانلود دارایی‌های بازی از [itch.io](https://itch.io/) است. این تابع آرگومان‌های زیر را می‌پذیرد:

- `gameUrl`: URL صفحه فروشگاه بازی.
- `upload`: شناسه عددی دارایی برای دانلود. برای یافتن شناسه آپلود یک دارایی، هنگام دانلود دارایی با استفاده از مرورگر، بخش پایانی مسیر (basename) در URL درخواست را بررسی کنید.
- `hash`.
- `name` (اختیاری): نام درایویشن (derivation)، که اغلب همان نام فایل دارایی است.
- `extraMessage` (اختیاری): پیام اضافی که در صورت عدم ارائه کلید API یا در صورتی که حساب کاربری بازی را خریداری نکرده باشد، چاپ می‌شود.

برای کارکرد صحیح این دریافت‌کننده، متغیر محیطی `NIX_ITCHIO_API_KEY` باید برای فرآیند ساخت Nix (که در حالت چندکاربره همان nix-daemon است) تنظیم شود، و اگر بازی غیررایگان باشد، این کلید باید متعلق به حسابی باشد که بازی را خریداری کرده است.
برای دریافت کلید API خود، به [بخش "API key"](https://itch.io/user/settings/api-keys) در تنظیمات حساب کاربری خود در itch.io بروید.

```nix
{ fetchItchIo }:

fetchItchIo {
  name = "DungeonDuelMonsters-linux-x64.zip";
  hash = "sha256-gq2nGwpaStqaVI1pL63xygxOI/z53o+zLwiKizG98Ks=";
  gameUrl = "https://mikaygo.itch.io/ddm";
  upload = "13371354";
}
```
