# واژه‌نامه

- [`∅`]{#gloss-empty-set}

  نماد مجموعه خالی. در زمینه تاریخچه پروفایل، این نشان می‌دهد که یک بسته در نسخه خاصی از پروفایل حضور ندارد.

- [`ε`]{#gloss-epsilon}

  نماد اپسیلون. در زمینه یک بسته، این به معنای خالی بودن نسخه است. به‌ویژه، این derivation فاقد صفت نسخه است.

- [دایرکتوری پایه (base directory)]{#gloss-base-directory}

  مکان و مسیری که مسیرهای نسبی بر اساس آن حل می‌شوند.

  - برای عبارت‌ها در یک فایل، دایرکتوری پایه، پوشه‌ای است که آن فایل را در خود جای داده است.
    این مشابه دایرکتوری یک [URL پایه](https://datatracker.ietf.org/doc/html/rfc1808#section-3.3) است.
    <!-- که برای حل URLهای غیرخالی کافی است -->

  <!--
    نگارش این بخش ممکن است عجیب به نظر برسد، اما دلایل زیر را دارد:
      * "with --expr": این یک پرچم (flag) است، نه یک گزینه با مقداری همراه
      * "written in": خود عبارت باید به عنوان یک آرگومان نوشته شود،
        در حالی که عبارت طبیعی‌تر "passed as an argument" ممکن است این برداشت را ایجاد کند
        که عبارت می‌تواند از طریق نام فایل ارسال شود.
    -->
  - برای عبارت‌های نوشته‌شده در آرگومان‌های خط فرمان با استفاده از [`--expr`](@docroot@/command-ref/opt-common.html#opt-expr)، دایرکتوری پایه، دایرکتوری کاری فعلی است.

  [دایرکتوری پایه]: #gloss-base-directory

- [کَش باینری (binary cache)]{#gloss-binary-cache}

  یک *کَش باینری* انبار Nixی است که از قالب متفاوتی استفاده می‌کند: فراداده (metadata) و امضاهای آن به جای [پایگاه‌داده Nix] در فایل‌های `.narinfo` نگهداری می‌شوند. این قالب متفاوت، سرویس‌دهی اشیاء انبار را از طریق شبکه ساده‌تر می‌کند، اما نمی‌تواند میزبان ساخت‌ها باشد. نمونه‌هایی از کش‌های باینری شامل باکت‌های S3 و [کَش باینری NixOS](https://cache.nixos.org) می‌شوند.

- [سیستم ساخت (build system)]{#gloss-build-system}

  اصطلاحی عمومی برای نرم‌افزاری که با خودکارسازی فراخوانی کامپایلرها، لینکرها و سایر ابزارها، ساخت نرم‌افزار را تسهیل می‌کند.

  Nix می‌تواند به عنوان یک سیستم ساخت عمومی استفاده شود.
  این ابزار هیچ شناختی از هیچ زبان برنامه‌نویسی یا زنجیره ابزار خاصی ندارد.
  این جزئیات در [عبارت‌های derivation](#gloss-derivation-expression) مشخص می‌شوند.

- [بسته (closure)]{#gloss-closure}

  بسته یک مسیر انبار، مجموعه ای از مسیرهای انبار است که مستقیماً یا غیرمستقیم از آن مسیر انبار «قابل دسترسی» هستند؛ یعنی بستهٔ آن مسیر تحت رابطهٔ *ارجاعات* است. برای یک بسته، بستهٔ derivation آن معادل وابستگی‌های زمان ساخت است، در حالی که بستهٔ [مسیر خروجی] آن معادل وابستگی‌های زمان اجرای آن است. برای استقرار صحیح، لازم است کل بسته‌ها مستقر شوند، در غیر این صورت ممکن است در زمان اجرا فایل‌ها گم شوند. دستور `nix-store --query --requisites` بسته‌های مسیرهای انبار را چاپ می‌کند.

  به عنوان مثال، اگر [شیء انبار] در مسیر `P` شامل یک [ارجاع] به یک شیء انبار در مسیر `Q` باشد، آنگاه `Q` در بستهٔ `P` قرار دارد. علاوه بر این، اگر `Q` به `R` ارجاع دهد، آنگاه `R` نیز در بستهٔ `P` قرار دارد.

  برای جزئیات بیشتر به [ارجاعات](@docroot@/store/store-object.md#references) مراجعه کنید.

  [بسته]: #gloss-closure

- [آدرس محتوا (content address)]{#gloss-content-address}

  یک [*آدرس محتوا*](https://en.wikipedia.org/wiki/Content-addressable_storage)، روشی امن برای ارجاع به داده‌های تغییرناپذیر است.
  این ارجاع مستقیماً از محتوای داده‌هایی که به آن‌ها ارجاع داده می‌شود محاسبه می‌شود، به این معنی که ارجاع [*ضد دستکاری*](https://en.wikipedia.org/wiki/Tamperproofing) است — تغییرات داده‌ها همیشه باید به آدرس‌های محتوای متمایز منتهی شوند.

برای اطلاع از نحوه استفادهٔ Nix از آدرس‌دهی محتوا (content-addressing)، به موارد زیر مراجعه کنید:

    - [اشیای سیستم‌فایل مبتنی بر آدرس محتوا](@docroot@/store/file-system-object/content-address.md)
    - [اشیای انبار مبتنی بر آدرس محتوا](@docroot@/store/store-object/content-address.md)
    - [derivation مبتنی بر آدرس محتوا](#gloss-content-addressing-derivation)

  مقاله‌ی Software Heritage در مورد [*شناسه‌های ذاتی و بیرونی*](https://www.softwareheritage.org/2020/07/09/intrinsic-vs-extrinsic-identifiers) نیز مقدمهٔ خوبی برای درک ارزش آدرس‌دهی محتوا در مقایسه با سایر طرح‌های ارجاع است.

  علاوه بر آدرس‌دهی محتوا، انبار Nix از [آدرس‌دهی ورودی](#gloss-input-addressed-store-object) نیز استفاده می‌کند.

- [انبار مبتنی بر آدرس محتوا]{#gloss-content-addressed-store}

  اصطلاح صنعتی برای سیستم‌های ذخیره‌سازی و بازیابی که از [آدرس‌دهی محتوا](#gloss-content-address) استفاده می‌کنند. انبار Nix همچنین دارای [آدرس‌دهی ورودی](#gloss-input-addressed-store-object) و فراداده (metadata) است.

- [شیء انبار مبتنی بر آدرس محتوا]{#gloss-content-addressed-store-object}

  یک [شیء انبار] که [مبتنی بر آدرس محتوا](#gloss-content-address) است،
  یعنی [مسیر انبار] آن توسط محتوای آن تعیین می‌شود.
  این مورد شامل derivationها، خروجی‌های [derivationهای مبتنی بر آدرس محتوا](#gloss-content-addressing-derivation) و خروجی‌های [derivationهای با خروجی ثابت](#gloss-fixed-output-derivation) می‌شود.

  برای جزئیات بیشتر به [اشیای انبار مبتنی بر آدرس محتوا](@docroot@/store/store-object/content-address.md) مراجعه کنید.

- [derivation مبتنی بر آدرس محتوا]{#gloss-content-addressing-derivation}

  یک derivation که صفت
  [`__contentAddressed`](./language/advanced-attributes.md#adv-attr-__contentAddressed)
  در آن روی مقدار `true` تنظیم شده است.

- [derivation]{#gloss-derivation}

  می‌توان یک derivation را به عنوان یک [تابع خالص](https://en.wikipedia.org/wiki/Pure_function) در نظر گرفت که [اشیای انبار][store object] جدیدی را از اشیای انبار موجود تولید می‌کند.

  Derivationها به شکل [فرآیندهای سیستم‌عامل که در یک sandbox اجرا می‌شوند](@docroot@/store/building.md) پیاده‌سازی می‌شوند.
  این sandbox به‌طور پیش‌فرض تنها اجازهٔ خواندن از اشیای انباری را می‌دهد که به عنوان ورودی مشخص شده‌اند، و تنها اجازهٔ نوشتن روی [خروجی‌های][output] تعیین‌شده را می‌دهد تا به عنوان [اشیای انبار ثبت شوند](@docroot@/store/building.md#processing-outputs).

  یک derivation معمولاً به عنوان یک [عبارت derivation] در [زبان Nix] مشخص می‌شود، و به یک [derivation انبار][store derivation] [فراوانی می‌یابد][instantiate].
  راه‌های متعددی برای به دست آوردن اشیای انبار از derivationهای انبار وجود دارد که به طور جمعی [تحقق‌یافتن][realise] نامیده می‌شوند.

  [derivation]: #gloss-derivation

- [عبارت derivation]{#gloss-derivation-expression}

  توصیفی از یک [derivation انبار] با استفاده از [مقدمات `derivation` (پیش‌فرض)][./language/derivations.md] در [زبان Nix].

  [عبارت derivation]: #gloss-derivation-expression

- [مسیر derivation]{#gloss-derivation-path}

  یک [مسیر انبار] که به طور منحصربه‌فرد یک [derivation انبار] را شناسایی می‌کند.

  برای جزئیات بیشتر به [ارجاع به derivationهای انبار](@docroot@/store/derivation/index.md#derivation-path) مراجعه کنید.

  نباید با [مسیر در حال اشتقاق] اشتباه گرفته شود.

  [مسیر derivation]: #gloss-derivation-path

- [سازندهٔ derivation (deriver)]{#gloss-deriver}

  آن [derivation انبار] که یک [مسیر خروجی] را تولید کرده است.

  سازندهٔ یک مسیر خروجی را می‌توان با گزینه‌ی `--deriver` در دستور
  [`nix-store --query`](@docroot@/command-ref/nix-store/query.md)
  استعلام کرد.

- [مسیر در حال اشتقاق (deriving path)]{#gloss-deriving-path}

  مسیرهای در حال اشتقاق راهی برای ارجاع به [اشیای انبار][store object] هستند که ممکن است هنوز [تحقق نیافته باشند][realise].

برای جزئیات بیشتر، به [مسیر derivation](./store/derivation/index.md#deriving-path) مراجعه کنید.

  نباید با [مسیر derivation] اشتباه گرفته شود.

- [گراف جهت‌دار بدون دور]{#gloss-directed-acyclic-graph}

  یک [گراف جهت‌دار بدون دور](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG) گرافی است که یال‌های آن دارای جهت هستند («a به b» با یال «b به a» یکی نیست) و هیچ مسیر ممکنی (که از به هم پیوستن یال‌ها ایجاد شود) یک چرخه تشکیل نمی‌دهد.

  گراف‌های DAG برای Nix بسیار مهم هستند.
  به‌ویژه، [خودارجاعی‌های][reference] غیر-[شیء انبار][store object] یک چرخه تشکیل می‌دهند.

- [ویژگی آزمایشی]{#gloss-experimental-feature}

  قابلیتی که هنوز تثبیت نشده است و توسط پرچم‌های ویژگی‌های آزمایشی نام‌گذاری‌شده محافظت می‌شود.
  این پرچم‌ها با تنظیم [`experimental-features`](./command-ref/conf-file.html#conf-experimental-features) فعال یا غیرفعال می‌شوند.

  راهنمای مشارکت در خصوص [هدف و چرخه عمر ویژگی‌های آزمایشی](@docroot@/development/experimental-features.md) را مطالعه کنید.

- [شیء سیستم‌فایل]{#gloss-file-system-object}

  مدل داده‌ی Nix برای نمایش داده‌های ساده‌شده‌ی سیستم‌فایل.

  برای جزئیات بیشتر، به [شیء سیستم‌فایل](@docroot@/store/file-system-object.md) مراجعه کنید.

  [file system object]: #gloss-file-system-object

- [derivation خروجی‌ثابت]{#gloss-fixed-output-derivation} (FOD)

  یک [store derivation] که در آن هش رمزنگاری‌شده‌ی [خروجی] از پیش با استفاده از صفت [`outputHash`](./language/advanced-attributes.md#adv-attr-outputHash) تعیین می‌شود، و در آن فایل اجرایی [`builder`](@docroot@/language/derivations.md#attr-builder) به شبکه دسترسی دارد.

- [بسته / هرمتیک (Hermetic)]{#gloss-hermetic}

  یک فرآیند ارزیابی یا ساخت زمانی هرمتیک است که بتوان مجموعه تمام ورودی‌های تأثیرگذار بر آن را به صورت مکانیکی شناسایی کرد.
  در سطح ساخت، این امر از طریق ایزوله‌سازی (sandboxing) حاصل می‌شود؛ و در سطح ارزیابی، با محدود کردن دسترسی ناخالص (همانند [ارزیابی خالص](@docroot@/command-ref/conf-file.md#conf-pure-eval)) به همراه [قفل‌گذاری](#gloss-locking) یا [سنجاق کردن](#gloss-pinning) ورودی‌های دریافت‌شده، که به صورت گذرا روی [دریافت‌های خالص](@docroot@/command-ref/conf-file.md#pure-fetch) اعمال می‌شوند.

- [IFD]{#gloss-ifd}

  [درون‌ریزی از Derivation](./language/import-from-derivation.md)

- [derivation ناخالص]{#gloss-impure-derivation}

  [یک ویژگی آزمایشی](@docroot@/development/experimental-features.md#xp-feature-impure-derivations) که به derivationها اجازه می‌دهد به صراحت به عنوان ناخالص علامت‌گذاری شوند،
  تا همیشه بازسازی شوند و خروجی‌های آن‌ها توسط فرایندهای بعدی برای تحقق‌بخشیدن (realise) مجدداً استفاده نشوند.

- [شیء انبار آدرس‌دهی‌شده با ورودی]{#gloss-input-addressed-store-object}

  یک شیء انبار که با ساخت یک derivation غیر-[مبتنی بر محتوا](#gloss-content-addressing-derivation) و غیر-[خروجی‌ثابت](#gloss-fixed-output-derivation) تولید می‌شود.

  برای جزئیات بیشتر، به [خروجی‌های derivation آدرس‌دهی‌شده با ورودی](store/derivation/outputs/input-address.md) مراجعه کنید.

- [قابل‌نصب]{#gloss-installable}

  چیزی که می‌تواند در انبار Nix محقق (realise) شود.

  برای جزئیات بیشتر درباره [`دستورات nix`](./command-ref/new-cli/nix.md) (آزمایشی)، به [قابل‌نصب‌ها](./command-ref/new-cli/nix.md#installables) مراجعه کنید.

- [instantiate کردن (ساخت شیء derivation)]{#gloss-instantiate}، instantiation

  ترجمه یک [عبارت derivation] به یک [store derivation].

  به [`nix-instantiate`](./command-ref/nix-instantiate.md) مراجعه کنید که یک store derivation از یک عبارت Nix که به یک derivation ارزیابی می‌شود، تولید می‌کند.

  [instantiate]: #gloss-instantiate

- [قفل‌گذاری (Locking)]{#gloss-locking}

در مدیریت بسته، *ثابت‌سازی نسخه (Pinning)* مفهوم یا فرآیندی است که طی آن یک فایل قفل ایجاد می‌شود. این فایل هر ورودی ارزیابی تغییرپذیری را به یک مرجع تغییرناپذیر نگاشت می‌کند، به طوری که ارزیابی‌های آینده به جای اشاره به آنچه مراجع تغییرپذیر در حال حاضر نشان می‌دهند، به همان نسخه‌های تغییرناپذیر منتهی شوند.

- [بایگانی نیکس (NAR)]{#gloss-nar}

  یک بایگانی نیکس (*N*ix *AR*chive). این یک سریال‌سازی از یک مسیر در انبار نیکس است. این بایگانی می‌تواند شامل فایل‌های معمولی، پوشه‌ها و پیوندهای نمادین باشد. بایگانی‌های NAR با استفاده از `nix-store --dump` و `nix-store --restore` تولید و استخراج می‌شوند.

  برای جزئیات بیشتر به [بایگانی نیکس](store/file-system-object/content-address.html#serial-nix-archive) مراجعه کنید.

- [پایگاه‌داده نیکس]{#gloss-nix-database}

  یک پایگاه‌داده SQLite برای ردیابی [مرجع]ها بین [شیء انبار]ها. این یک جزئیات پیاده‌سازی از [انبار محلی] است.

  مکان پیش‌فرض: `/nix/var/nix/db`.

  [پایگاه‌داده نیکس]: #gloss-nix-database

- [عبارت نیکس (Nix expression)]{#gloss-nix-expression}

  یک استفاده از [زبان نیکس] که از نظر نحوی معتبر است.

  > **مثال**
  >
  > محتویات یک فایل `.nix` یک عبارت نیکس را تشکیل می‌دهند.

  عبارت‌های نیکس، [عبارت‌های درایویشن][derivation expression] را مشخص می‌کنند که در انبار نیکس به عنوان [درایویشن‌های انبار][store derivation] [مؤسس][instantiate] می‌شوند.
  سپس این درایویشن‌ها می‌توانند برای تولید [خروجی‌ها][output] [محقق][realise] شوند.

  > **مثال**
  >
  > ساخت و استقرار نرم‌افزار با استفاده از نیکس مستلزم نوشتن عبارت‌های نیکس برای توصیف [بسته‌ها][package] و ترکیب‌های آن‌ها است.

- [نمونه نیکس (Nix instance)]{#gloss-nix-instance}
  <!-- مبهم -->
  1. یک نصب از نیکس، که شامل حضور یک [انبار] و مدیر بسته نیکس است که روی آن انبار کار می‌کند.
     یک نصب محلی نیکس و یک [سازنده راه دور](@docroot@/advanced-topics/distributed-builds.md) دو نمونه از نمونه‌های نیکس هستند.
  2. یک فرآیند در حال اجرای نیکس، مانند دستور `nix`.

- [خروجی (output)]{#gloss-output}

  یک [شیء انبار] که توسط یک [درایویشن انبار] تولید می‌شود.
  برای جزئیات بیشتر به [آرگومان `outputs` برای تابع `derivation`](@docroot@/language/derivations.md#attr-outputs) مراجعه کنید.

  [خروجی]: #gloss-output

- [بسته خروجی (output closure)]\
  [بسته (closure)] یک [مسیر خروجی]. این بسته فقط شامل مواردی است که از خروجی [قابل‌دستیابی] هستند.

- [مسیر خروجی (output path)]{#gloss-output-path}

  [مسیر انبار] به [خروجی] یک [درایویشن انبار].

  [مسیر خروجی]: #gloss-output-path

- [بسته (package)]{#package}

  یک بسته نرم‌افزاری؛ فایل‌هایی که برای یک هدف خاص به هم تعلق دارند، به همراه فراداده (metadata).

  نیکس فایل‌ها را به عنوان [شیء سیستم‌فایل][file system object] نمایش می‌دهد و نحوه تعلق آن‌ها به یکدیگر به عنوان [مرجع]ها بین [شیء انبار]هایی که حاوی این اشیاء سیستم‌فایل هستند، کدگذاری می‌شود.

  [زبان نیکس] امکان نام‌گذاری بسته‌ها را بر حسب [مجموعه‌های صفت](@docroot@/language/types.md#type-attrs) شامل موارد زیر فراهم می‌کند:
  - صفاتی که به فایل‌های یک بسته اشاره دارند، معمولاً در قالب [خروجی‌های درایویشن](#gloss-output)،
  - صفاتی با فراداده، مانند اطلاعاتی درباره نحوه استفاده از بسته.

  شکل دقیق این مجموعه‌های صفت بستگی به توافق دارد.

  [بسته]: #package

- [ثابت‌سازی نسخه (Pinning)]{#gloss-pinning}

مانند [قفل کردن](#gloss-locking)، اما یک پین تنها یک ورودی را قفل می‌کند.
یک راهکار پین‌کردن ممکن است مجموعه‌ای از پین‌ها را مدیریت کند،
اما هدف از پایین به بالا (bottom-up) را برای تثبیت مرجع یک ورودی بر اساس تقاضا برآورده می‌کند،
در حالی که قفل کردن دلالت بر رویکردی از بالا به پایین دارد که در آن همه پین‌ها در یک مکان واحد «وادار» می‌شوند.
این «وادارسازی» عموماً به واسطه مکانیسم‌های سطح بالایی مانند سیستم‌های ماژول زبان برنامه‌نویسی به دست می‌آید.
نیکس چنین سیستم ماژول محدودکننده‌ای ندارد، زیرا حتی یک فلیک نیز می‌تواند از عبارت‌هایی استفاده کند که به تنهایی پین یا قفل می‌شوند.
این امر متکی بر کامل بودن قفل نیست، بلکه بر یک ویژگی دریافت گذرا (transitive) متکی است؛ نگاه کنید به [هرمسیت](#gloss-hermetic).

- [پروفایل]{#gloss-profile}

  یک پیوند نمادین به *محیط کاربر* فعلی یک کاربر، برای نمونه:
  `/nix/var/nix/profiles/default`.

- [خلوص]{#gloss-خلوص}

  این فرض که درایویشن‌های مساوی نیکس هنگام اجرا همواره خروجی یکسانی تولید می‌کنند. این موضوع را به‌طور کلی نمی‌توان تضمین کرد (برای نمونه، یک سازنده می‌تواند به ورودی‌های خارجی مانند شبکه یا زمان سیستم متکی باشد) اما مدل نیکس آن را فرض می‌گیرد.

- [قابل‌دسترس]{#gloss-reachable}

  یک مسیر انبار `Q` از مسیر انبار دیگری چون `P` قابل‌دسترس است اگر `Q` در *بستار* رابطهٔ *ارجاعات* باشد.

  برای جزئیات به [ارجاعات](@docroot@/store/store-object.md#references) مراجعه کنید.

- [محقق‌سازی (realise)]{#gloss-realise}، تحقق

  اطمینان از اینکه یک [مسیر انبار] [معتبر][validity] است.

  این کار از راه‌های زیر قابل دستیابی است:
  - دریافت یک [شیء انبار] پیش‌ساخته از یک [جایگزین‌ساز]
  - [ساختن](@docroot@/store/building.md) [derivation] متناظر با آن
  - تفویض به یک [ماشین راه دور](@docroot@/command-ref/conf-file.md#conf-builders) و بازیابی خروجی‌ها

  برای توضیحات دقیق درباره الگوریتم، به [`nix-store --realise`](@docroot@/command-ref/nix-store/realise.md) مراجعه کنید.

  همچنین نگاه کنید به [`nix-build`](./command-ref/nix-build.md) و [`nix build`](./command-ref/new-cli/nix3-build.md) (آزمایشی).

  [realise]: #gloss-realise

- [ارجاع (reference)]{#gloss-reference}

  یک یال از یک [شیء انبار] به شیء دیگر.

  برای جزئیات به [ارجاعات](@docroot@/store/store-object.md#references) مراجعه کنید.

  [reference]: #gloss-reference

  برای جزئیات به [ارجاعات](@docroot@/store/store-object.md#references) مراجعه کنید.

- [ارجاع‌دهنده]{#gloss-referrer}

  یک یال معکوس از یک [شیء انبار] به شیء دیگر.

- [ملزومات (requisite)]{#gloss-requisite}

  یک شیء انبار که از یک [شیء انبار] داده‌شده توسط یک مسیر (زنجیره‌ای از ارجاعات) [قابل‌دسترس] است.
  [بستار] مجموعهٔ ملزومات است.

  برای جزئیات به [ارجاعات](@docroot@/store/store-object.md#references) مراجعه کنید.

- [انبار (store)]{#gloss-store}

  مجموعه‌ای از [اشیاء انبار][store object]، به همراه عملکردهایی برای دستکاری آن مجموعه.
  برای جزئیات به [انبار نیکس](./store/index.md) مراجعه کنید.

  انواع زیادی از انبارها وجود دارد، برای جزئیات به [انواع انبار](./store/types/index.md) مراجعه کنید.

  [store]: #gloss-store

- [store derivation]{#gloss-store-derivation}

  یک [derivation] که به عنوان یک [شیء انبار] نمایش داده می‌شود.

  برای جزئیات به [Store Derivation](@docroot@/store/derivation/index.md#store-derivation) مراجعه کنید.

  [store derivation]: #gloss-store-derivation

- [شیء انبار (store object)]{#gloss-store-object}

  بخشی از محتوای یک [انبار].

  یک شیء انبار شامل یک [شیء سیستم‌فایل]، [ارجاعات][reference] به سایر اشیاء انبار، و سایر فراداده‌ها است.
  می‌توان توسط یک [مسیر انبار] به آن ارجاع داد.

  برای جزئیات به [شیء انبار](@docroot@/store/store-object.md) مراجعه کنید.

  [store object]: #gloss-store-object

- [مسیر انبار]{#gloss-store-path}

مکان یک [store object] در سیستم‌فایل، یعنی یک فرزند مستقیم از پوشه‌ی انبار Nix.

> **مثال**
>
> `/nix/store/jf6gn2dzna4nmsfbdxsd7kwhsk6gnnlr-git-2.38.1`

برای جزئیات بیشتر به [Store Path](@docroot@/store/store-path.md) مراجعه کنید.

[store path]: #gloss-store-path

- [string interpolation]{#gloss-string-interpolation}

  گسترش دادن عبارت‌های محصور شده در `${ }` درون یک [string]، [path] یا [attribute name].

  برای جزئیات بیشتر به [String interpolation](./language/string-interpolation.md) مراجعه کنید.

  [string]: ./language/types.md#type-string
  [path]: ./language/types.md#type-path
  [attribute name]: ./language/types.md#type-attrs

- [SRI]{#gloss-sri}

  [Subresource Integrity](https://www.w3.org/TR/SRI/) (SRI) یک [مشخصه W3C](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) برای فراداده‌های یکپارچگی است.
  Nix از فرمت هش SRI (`<algorithm>-<Base64 hash>`) استفاده می‌کند تا هش‌های محتوا را به شکلی خودتوصیف مشخص کند، زیرا الگوریتم هش بخشی از این فرمت است.

  [SRI]: #gloss-sri

- [substitute]{#gloss-substitute}

  یک substitute (جایگزین) یک فراخوانی فرمان ذخیره‌شده در [Nix database] است که نحوه ساخت یک store object را توصیف می‌کند و مکانیزم ساخت عادی (یعنی derivationها) را دور می‌زند. معمولاً substitute با بارگیری یک نسخه پیش‌ساخته از store object از یک سرور، آن را می‌سازد.

- [substituter]{#gloss-substituter}

  یک [store]{#gloss-store} اضافی که Nix می‌تواند به جای ساختن store objectها، آن‌ها را از آن دریافت کند.
  اغلب substituter یک [binary cache](#gloss-binary-cache) است، اما هر انبار دیگری نیز می‌تواند به عنوان substituter عمل کند.

  برای جزئیات بیشتر به [`substituters` configuration option](./command-ref/conf-file.md#conf-substituters) مراجعه کنید.

  [substituter]: #gloss-substituter

- [user environment]{#gloss-user-env}

  یک store object خودکار ساخته‌شده که شامل مجموعه‌ای از پیوندهای نمادین (symlinks) به برنامه‌های «فعال»، یعنی سایر مسیرهای انبار (store paths) است. این موارد به طور خودکار توسط [`nix-env`](./command-ref/nix-env.md) تولید می‌شوند. به *profiles* مراجعه کنید.

- [validity]{#gloss-validity}

  یک مسیر انبار (store path) در صورتی معتبر است که تمام [store object]های موجود در [closure] آن قابل خواندن از [store] باشند.

  برای یک [local store]، این به معنای موارد زیر است:
  - مسیر انبار به یک [store object] موجود در آن [store] منتهی شود.
  - مسیر انبار در [Nix database] به عنوان معتبر فهرست شده باشد.
  - تمام مسیرهای موجود در [closure] مسیر انبار معتبر باشند.

  [validity]: #gloss-validity
  [local store]: @docroot@/store/types/local-store.md

[Nix language]: ./language/index.md
