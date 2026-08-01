# صفات پیشرفته

درایویشن‌ها می‌توانند برخی از صفات اختیاری که کمتر استفاده می‌شوند را اعلام کنند.

## ورودی‌ها

  - [`exportReferencesGraph`]{#adv-attr-exportReferencesGraph}\
    این صفت به سازنده‌ها اجازه می‌دهد به گراف ارجاعات ورودی‌های خود دسترسی داشته باشند. این صفت فهرستی از ورودی‌ها در انبار Nix است که سازنده باید گراف ارجاعات آن‌ها را بداند. مقدار این صفت باید فهرستی از جفت‌های `[ name1 path1 name2 path2 ... ]` باشد. گراف ارجاعات هر *pathN* در یک فایل متنی با نام *nameN* در پوشه ساخت موقت ذخیره خواهد شد. فایل‌های متنی دارای قالبی هستند که توسط `nix-store --register-validity` استفاده می‌شود (در حالی که فیلدهای درایور خالی گذاشته شده‌اند). برای مثال، وقتی درایویشن زیر ساخته می‌شود:
```nix
    derivation {
      ...
      exportReferencesGraph = [ "libfoo-graph" libfoo ];
    };
    ```

گراف ارجاعات `libfoo` در فایل `libfoo-graph` در پوشه ساخت موقت قرار می‌گیرد.

تابع `exportReferencesGraph` برای سازنده‌هایی مفید است که می‌خواهند کاری روی کلاستر یک مسیر انبار انجام دهند. نمونه‌ها شامل سازنده‌ها در NixOS هستند که رمدیسک اولیه را برای راه‌اندازی لینوکس (یک آرشیو `cpio` حاوی کلاستر اسکریپت راه‌اندازی) و تصویر ISO-9660 را برای سی‌دی نصب (که با یک انبار Nix حاوی کلاستر یک پیکربندی بوت‌شدنی NixOS پر شده است) تولید می‌کنند.

  - [`passAsFile`]{#adv-attr-passAsFile}\
    فهرستی از نام صفات که باید به‌جای متغیرهای محیطی، از طریق فایل‌ها منتقل شوند. برای مثال، اگر شما دارای
```nix
    passAsFile = ["big"];
    big = "a very long string";
    ```

سپس هنگامی که سازنده (builder) اجرا می‌شود، متغیر محیطی `bigPath` شامل مسیر مطلق یک فایل موقت خواهد بود که حاوی `a very long string` است. یعنی برای هر صفت *x* که در `passAsFile` فهرست شده باشد، Nix یک متغیر محیطی `xPath` را ارسال می‌کند که حاوی مسیر فایل دربردارندهٔ مقدار صفت *x* است. این ویژگی زمانی مفید است که بخواهید رشته‌های بزرگی را به یک سازنده (builder) ارسال کنید، زیرا اکثر سیستم‌عامل‌ها محدودیتی را بر روی اندازه محیط (معمولاً چند صد کیلوبایت) اعمال می‌کنند.

  - [`__structuredAttrs`]{#adv-attr-structuredAttrs}\
    اگر صفت ویژهٔ `__structuredAttrs` روی مقدار `true` تنظیم شود، سایر صفات derivation در یک فایل با فرمت JSON سریالایز می‌شوند.

    این کار نیاز به [`passAsFile`](#adv-attr-passAsFile) را از بین می‌برد؛ زیرا بر خلاف محیط‌های فرآیند، فایل‌های JSON هیچ‌گونه محدودیت انواعی در اندازه ندارند.
    همچنین این امکان را فراهم می‌کند تا تنظیمات derivation را به شکلی ساختاریافته تنظیم کنید؛
    برای نمونه [`outputChecks`](#adv-attr-outputChecks) را ببینید.

    برای جزئیات بیشتر، به [بخش مربوطه در صفحه derivation](@docroot@/store/derivation/index.md#structured-attrs) مراجعه کنید.

    > **Warning**
    >
    > اگر روی `true` تنظیم شود، سایر صفات پیشرفته مانند [`allowedReferences`](#adv-attr-allowedReferences)، [`allowedRequisites`](#adv-attr-allowedRequisites)،
    [`disallowedReferences`](#adv-attr-disallowedReferences)، [`disallowedRequisites`](#adv-attr-disallowedRequisites)، maxSize و maxClosureSize
    هیچ اثری نخواهند داشت.

## بررسی‌های خروجی

[بخش مربوطه در صفحه خروجی derivation](@docroot@/store/derivation/outputs/index.md) را ببینید.

  - [`allowedReferences`]{#adv-attr-allowedReferences}\
    صفت اختیاری `allowedReferences` فهرستی از ارجاعات (وابستگی‌های) مجاز خروجی سازنده (builder) را مشخص می‌کند. برای مثال،
```nix
    allowedReferences = [];
    ```

تضمین می‌کند که خروجی یک derivation نمی‌تواند هیچ‌گونه وابستگی زمان اجرا به ورودی‌های خود داشته باشد. برای اجازه دادن به اینکه یک خروجی دارای وابستگی زمان اجرا به خودش باشد، از `"out"` به عنوان یک عنصر فهرست استفاده کنید. این ویژگی در NixOS برای بررسی این موضوع استفاده می‌شود که فایل‌های تولیدشده مانند رم‌دیسک‌های اولیه برای راه‌اندازی لینوکس، وابستگی‌های تصادفی به مسیرهای دیگر در انبار Nix نداشته باشند.

  - [`allowedRequisites`]{#adv-attr-allowedRequisites}\
    این صفت شبیه به `allowedReferences` است، اما ملزومات مجاز کل کلوزر (closure)، یعنی تمام وابستگی‌ها را به صورت بازگشتی مشخص می‌کند. برای مثال،
```nix
    allowedRequisites = [ foobar ];
    ```

تضمین می‌کند که خروجی یک derivation نمی‌تواند هیچ وابستگی زمان اجرای دیگری به غیر از `foobar` داشته باشد، و علاوه بر این، تضمین می‌کند که خودِ `foobar` نیز هیچ وابستگی دیگری را وارد نکند.

  - [`disallowedReferences`]{#adv-attr-disallowedReferences}\
    صفت اختیاری `disallowedReferences` فهرستی از ارجاعات (وابستگی‌های) غیرمجاز خروجی سازنده را مشخص می‌کند. برای مثال،
```nix
    disallowedReferences = [ foo ];
    ```

تضمین می‌کند که خروجی یک derivation نمی‌تواند وابستگی زمان اجرای مستقیماً به derivation مربوط به `foo` داشته باشد.

  - [`disallowedRequisites`]{#adv-attr-disallowedRequisites}\
    این صفت مشابه `disallowedReferences` است، اما نیازمندی‌های غیرمجاز را برای کل closure (بستار)، یعنی تمام وابستگی‌ها به صورت بازگشتی، مشخص می‌کند. برای مثال،
```nix
    disallowedRequisites = [ foobar ];
    ```

تضمین می‌کند که خروجی یک derivation نمی‌تواند هیچ وابستگی زمان اجرایی به `foobar` یا هر derivation دیگری که به‌صورت بازگشتی به `foobar` وابسته است، داشته باشد.

  - [`outputChecks`]{#adv-attr-outputChecks}\
    هنگام استفاده از [صفت‌های ساختاریافته](#adv-attr-structuredAttrs)، صفت `outputChecks`
    امکان تعریف بررسی‌ها را به ازای هر خروجی فراهم می‌کند.

    علاوه بر
    [`allowedReferences`](#adv-attr-allowedReferences)، [`allowedRequisites`](#adv-attr-allowedRequisites)،
    [`disallowedReferences`](#adv-attr-disallowedReferences) و [`disallowedRequisites`](#adv-attr-disallowedRequisites)،
    صفت‌های زیر نیز در دسترس هستند:

    - `maxSize` حداکثر اندازه [شیء انبار](@docroot@/store/store-object.md) حاصل را تعریف می‌کند.
    - `maxClosureSize` حداکثر اندازه closure خروجی را تعریف می‌کند.
    - `ignoreSelfRefs` کنترل می‌کند که آیا هنگام بررسی ارجاعات/ملزومات مجاز، باید خودارجعی‌ها (self-references) در نظر گرفته شوند یا خیر.

    مثال:
```nix
    __structuredAttrs = true;

    outputChecks.out = {
      # The closure of 'out' must not be larger than 256 MiB.
      maxClosureSize = 256 * 1024 * 1024;

      # It must not refer to the C compiler or to the 'dev' output.
      disallowedRequisites = [ stdenv.cc "dev" ];
    };

    outputChecks.dev = {
      # The 'dev' output must not be larger than 128 KiB.
      maxSize = 128 * 1024;
    };
    ```

## سایر تغییرات خروجی

  - [`unsafeDiscardReferences`]{#adv-attr-unsafeDiscardReferences}\
    هنگام استفاده از [صفات ساختاریافته](#adv-attr-structuredAttrs)، صفت `unsafeDiscardReferences` یک مجموعه ویژگی با یک مقدار بولین برای هر نام خروجی است.
    اگر روی `true` تنظیم شود، اسکن کردن خروجی برای یافتن وابستگی‌های زمان اجرا را غیرفعال می‌کند.

    مثال:
```nix
    __structuredAttrs = true;
    unsafeDiscardReferences.out = true;
    ```

این امر به عنوان مثال هنگام تولید تصاویر سیستم‌فایل خودمختار با انبار Nix تعبیه‌شدهٔ خود مفید است: هش‌های یافت‌شده در چنین تصویری به انبار تعبیه‌شده اشاره می‌کنند و نه انبار Nix میزبان.

## زمان‌بندی ساخت

  - [`preferLocalBuild`]{#adv-attr-preferLocalBuild}\
    اگر این صفت روی مقدار `true` تنظیم شود و [ساخت‌های توزیع‌شده فعال باشند](@docroot@/command-ref/conf-file.md#conf-builders)، در صورت امکان، درایویشن به جای ارسال به یک ماشین راه دور، به‌صورت محلی ساخته خواهد شد.
    این گزینه برای درایویشن‌هایی مفید است که ساخت آن‌ها به‌صورت محلی کم‌هزینه‌تر است.

  - [`allowSubstitutes`]{#adv-attr-allowSubstitutes}\
    اگر این صفت روی مقدار `false` تنظیم شود، Nix همیشه این درایویشن را (به‌صورت محلی یا راه دور) خواهد ساخت؛ و تلاشی برای جایگزینی خروجی‌های آن نخواهد کرد.
    این گزینه برای درایویشن‌هایی مفید است که ساخت آن‌ها ارزان‌تر از جایگزین کردنشان است.

    با تنظیم [`always-allow-substitutes`](@docroot@/command-ref/conf-file.md#conf-always-allow-substitutes) روی `true` می‌توان از این صفت صرف‌نظر کرد.

    > **نکته**
    >
    > اگر روی `false` تنظیم شود، [`builder`] باید قادر باشد روی نوع سیستم مشخص‌شده در [`صفت system`](./derivations.md#attr-system) اجرا شود، زیرا درایویشن قابل جایگزینی نیست.

    [`builder`]: ./derivations.md#attr-builder

- [`requiredSystemFeatures`]{#adv-attr-requiredSystemFeatures}\
  اگر یک درایویشن دارای صفت `requiredSystemFeatures` باشد، Nix آن را فقط روی ماشینی می‌سازد که ویژگی‌های متناظر در [پیکربندی `system-features`](@docroot@/command-ref/conf-file.md#conf-system-features) آن تنظیم شده باشند.

  به عنوان مثال، تنظیم
```nix
  requiredSystemFeatures = [ "kvm" ];
  ```

تضمین می‌کند که derivation فقط روی ماشینی با قابلیت `kvm` قابل ساخت است.

# پیکربندی سازنده ناخالص

  - [`impureEnvVars`]{#adv-attr-impureEnvVars}\
    این صفت به شما اجازه می‌دهد فهرستی از متغیرهای محیطی را مشخص کنید
    که باید از محیط کاربر فراخواننده به سازنده منتقل شوند. معمولاً وقتی سازنده
    اجرا می‌شود، محیط به‌طور کامل پاک‌سازی می‌شود، اما با استفاده از این صفت می‌توانید
    اجازه دهید متغیرهای محیطی خاصی بدون تغییر منتقل شوند. برای مثال،
    `fetchurl` در Nixpkgs دارای خط زیر است
```nix
    impureEnvVars = [ "http_proxy" "https_proxy" ... ];
    ```

تا از آن برای استفاده از پیکربندی سرور پروکسی مشخص‌شده توسط کاربر
    در متغیرهای محیطی `http_proxy` و موارد مشابه استفاده کند.

    این صفت فقط در [درایویشن‌های با خروجی ثابت][fixed-output derivation] مجاز است،
    جایی که ناخالصی‌هایی مانند اینها مشکلی ندارند؛ زیرا (هش)
    خروجی از پیش مشخص است. این صفت برای سایر
    درایویشن‌ها نادیده گرفته می‌شود.

    > **هشدار**
    >
    > پیاده‌سازی `impureEnvVars` متغیرهای محیطی را از
    > فرآیند سازنده فعلی می‌گیرد. وقتی یک daemon در حال ساخت است،
    > متغیرهای محیطی آن استفاده می‌شوند. بدون daemon،
    > متغیرهای محیطی از محیط `nix-build` گرفته می‌شوند.

    اگر [ویژگی آزمایشی [`configurable-impure-env`](@docroot@/development/experimental-features.md#xp-feature-configurable-impure-env)](@docroot@/development/experimental-features.md#xp-feature-configurable-impure-env)
    فعال باشد، این متغیرهای محیطی را می‌توان از طریق
    تنظیمات پیکربندی [`impure-env`](@docroot@/command-ref/conf-file.md#conf-impure-env)
    نیز کنترل کرد.

## تنظیم نوع درایویشن

همان‌طور که در [خروجی‌های درایویشن و انواع درایویشن‌ها](@docroot@/store/derivation/outputs/index.md) بحث شد، چندین نوع درایویشن / نوع خروجی درایویشن وجود دارد.
انتخاب صفات زیر مشخص می‌کند که ما در حال ساخت چه نوع درایویشنی هستیم.

- [`__contentAddressed`]

- [`outputHash`]

- [`outputHashAlgo`]

- [`outputHashMode`]

سه نوع درایویشن بر اساس ترکیب‌های زیر از این صفات انتخاب می‌شوند.
سایر ترکیب‌ها نامعتبر هستند.

- [درایویشن‌های آدرس‌دهی‌شده بر اساس ورودی](@docroot@/store/derivation/outputs/input-address.md)

  این حالت پیش‌فرض برای `builtins.derivation` است.
  نیکس در حال حاضر فقط از یک نوع آدرس‌دهی بر اساس ورودی پشتیبانی می‌کند، بنابراین به اطلاعات دیگری نیاز نیست.

  مقدار `__contentAddressed = false;` نیز ممکن است گنجانده شود، اما ضروری نیست و بررسی ویژگی آزمایشی را فعال خواهد کرد.

- [درایویشن‌های با خروجی ثابت][fixed-output derivation]

  تمامی موارد [`outputHash`]، [`outputHashAlgo`] و [`outputHashMode`].

  <!--

  صفت `__contentAddressed` نادیده گرفته می‌شود، زیرا درایویشن‌های با خروجی ثابت طبق تعریف، همیشه خروجی‌های خود را بر اساس محتوا آدرس‌دهی می‌کنند.

  **TODO CHECK**

  -->

- [درایویشن‌های آدرس‌دهی‌شده بر اساس محتوا (شناور)](@docroot@/store/derivation/outputs/content-address.md)

  هر دو صفت [`outputHashAlgo`] و [`outputHashMode`]، به همراه `__contentAddressed = true;` و *بدون* `outputHash`.

  اگر هش خروجی ارائه می‌شد، خروجی درایویشن به جای «شناور»، «ثابت» می‌بود.

اطلاعات بیشتر درباره صفات `output*` و مقادیری که می‌توانند به خود اختصاص دهند در ادامه آمده است:

  - [`outputHashMode`]{#adv-attr-outputHashMode}

    این صفت مشخص می‌کند که چگونه فایل‌های یک خروجی درایویشن آدرس‌دهی‌شده بر اساس محتوا، برای تولید یک آدرس محتوا پردازش (هَش) می‌شوند.

    این کار در ترکیب با [`outputHashAlgo`](#adv-attr-outputHashAlgo) انجام می‌شود.
    مشخص کردن یکی بدون دیگری یک خطا محسوب می‌شود (مگر اینکه [`outputHash`] نیز مشخص شده باشد و الگوریتم هش مخصوص به خود را همان‌طور که در ادامه توضیح داده شده، شامل شود).

    صفت `outputHashMode` نحوه محاسبه هش را تعیین می‌کند.
    این صفت باید یکی از مقادیر زیر باشد:

      - [`"flat"`](@docroot@/store/store-object/content-address.md#method-flat)

        این حالت پیش‌فرض است.

      - [`"recursive"` یا `"nar"`](@docroot@/store/store-object/content-address.md#method-nix-archive)

> **سازگاری**
        >
        > عبارت `"recursive"` روش سنتی برای نشان دادن این موضوع است،
        > و از سال ۲۰۰۵ (تقریباً تمام تاریخچهٔ Nix) پشتیبانی می‌شود.
        > عبارت `"nar"` واضح‌تر است و با سایر بخش‌های Nix (مانند رابط خط فرمان) سازگاری دارد،
        > با این حال پشتیبانی از آن فقط از نسخه ۲.۲۱ به Nix اضافه شده است.

      - [`"text"`](@docroot@/store/store-object/content-address.md#method-text)

        > **هشدار**
        >
        > استفاده از این روش برای خروجی‌های derivation بخشی از ویژگی آزمایشی [`dynamic-derivations`][xp-feature-dynamic-derivations] است.

      - [`"git"`](@docroot@/store/store-object/content-address.md#method-git)

        > **هشدار**
        >
        > این روش بخشی از ویژگی آزمایشی [`git-hashing`][xp-feature-git-hashing] است.

    برای کسب اطلاعات بیشتر درباره فرآیندی که این پرچم کنترل می‌کند، به [اشیای انبار با آدرس محتوایی](@docroot@/store/store-object/content-address.md) مراجعه کنید.

  - [`outputHashAlgo`]{#adv-attr-outputHashAlgo}

    این گزینه، الگوریتم هش مورد استفاده برای محاسبهٔ داده‌های [شیء سیستم‌فایل] یک خروجی derivation با آدرس محتوایی را مشخص می‌کند.

    این مورد به همراه [`outputHashMode`](#adv-attr-outputHashAlgo) کار می‌کند.
    مشخص کردن یکی بدون دیگری یک خطا محسوب می‌شود (مگر اینکه `outputHash` نیز مشخص شده باشد و شامل الگوریتم هش مخصوص به خود باشد که در ادامه توضیح داده شده است).

    صفت `outputHashAlgo` الگوریتم هش مورد استفاده برای محاسبهٔ هش را مشخص می‌کند.
    در حال حاضر این مقدار می‌تواند `"blake3"`، `"sha1"`، `"sha256"`، `"sha512"` یا `null` باشد.

    مقدار `outputHashAlgo` تنها زمانی می‌تواند `null` باشد که `outputHash` از فرمت SRI پیروی کند، زیرا در این صورت انتخاب الگوریتم هش توسط `outputHash` تعیین می‌شود.

  - [`outputHash`]{#adv-attr-outputHash}

    این صفت، هش خروجی یک خروجی منفرد از یک [derivation با خروجی ثابت] را مشخص می‌کند.

    صفت `outputHash` باید رشته‌ای باشد که حاوی هش با کدگذاری هگزادسیمال یا "nix32"، یا به پیروی از فرمت فراداده‌های یکپارچگی تعریف‌شده توسط [SRI](@docroot@/glossary.md#gloss-sri) باشد.
    [کدگذاری "nix32"](@docroot@/protocols/nix32.md) گونه‌ای از کدگذاری Base32 مختص Nix است.

    > **نکته**
    >
    > تابع [`convertHash`](@docroot@/language/builtins.md#builtins-convertHash) نحوهٔ تبدیل بین کدگذاری‌های مختلف را نشان می‌دهد.
    > [دستور `nix-hash`](../command-ref/nix-hash.md) حاوی اطلاعاتی دربارهٔ نحوهٔ دریافت هش برای برخی محتویات و همچنین تبدیل به کدگذاری‌ها و از آن‌ها است.

  - [`__contentAddressed`]{#adv-attr-__contentAddressed}

    > **هشدار**
    >
    > این صفت بخشی از یک [ویژگی آزمایشی](@docroot@/development/experimental-features.md) است.
    >
    > برای استفاده از این صفت، باید ویژگی آزمایشی
    > [`ca-derivations`][xp-feature-ca-derivations] را فعال کنید.
    > به عنوان مثال، در فایل [nix.conf](../command-ref/conf-file.md) می‌توانید این مورد را اضافه کنید:
    >
```
    > extra-experimental-features = ca-derivations
    > ```

این یک مقدار بولی (boolean) با مقدار پیش‌فرض `false` است.
این گزینه تعیین می‌کند که آیا derivation به‌صورت آدرس‌دهی‌شده بر اساس محتوای شناور (floating content-addressing) است یا خیر.

[`__contentAddressed`]: #adv-attr-__contentAddressed
[`outputHash`]: #adv-attr-outputHash
[`outputHashAlgo`]: #adv-attr-outputHashAlgo
[`outputHashMode`]: #adv-attr-outputHashMode

[fixed-output derivation]: @docroot@/glossary.md#gloss-fixed-output-derivation
[file system object]: @docroot@/store/file-system-object.md
[store object]: @docroot@/store/store-object.md
[xp-feature-dynamic-derivations]: @docroot@/development/experimental-features.md#xp-feature-dynamic-derivations
[xp-feature-git-hashing]: @docroot@/development/experimental-features.md#xp-feature-git-hashing
