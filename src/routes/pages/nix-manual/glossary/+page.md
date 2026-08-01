# 12. واژه‌نامه

- [`∅`]<a id="gloss-empty-set"></a>

  نماد مجموعه خالی. در زمینه تاریخچه پروفایل، این نشان می‌دهد که یک بسته در نسخه خاصی از پروفایل حضور ندارد.

- [`ε`]<a id="gloss-epsilon"></a>

  نماد اپسیلون. در زمینه یک بسته، این به معنای خالی بودن نسخه است. به‌ویژه، این derivation فاقد صفت نسخه است.

- [دایرکتوری پایه (base directory)]<a id="gloss-base-directory"></a>

  مکان و مسیری که مسیرهای نسبی بر اساس آن حل می‌شوند.

  - برای عبارت‌ها در یک فایل، دایرکتوری پایه، پوشه‌ای است که آن فایل را در خود جای داده است.
    این مشابه دایرکتوری یک [URL پایه](https://datatracker.ietf.org/doc/html/rfc1808#section-3.3) است.
    

  
  - برای عبارت‌های نوشته‌شده در آرگومان‌های خط فرمان با استفاده از [`--expr`](/pages/nix-manual/command-ref/opt-common#opt-expr)، دایرکتوری پایه، دایرکتوری کاری فعلی است.

  [دایرکتوری پایه]: #gloss-base-directory

- [کَش باینری (binary cache)]<a id="gloss-binary-cache"></a>

  یک *کَش باینری* انبار Nixی است که از قالب متفاوتی استفاده می‌کند: فراداده (metadata) و امضاهای آن به جای [پایگاه‌داده Nix] در فایل‌های `.narinfo` نگهداری می‌شوند. این قالب متفاوت، سرویس‌دهی اشیاء انبار را از طریق شبکه ساده‌تر می‌کند، اما نمی‌تواند میزبان ساخت‌ها باشد. نمونه‌هایی از کش‌های باینری شامل باکت‌های S3 و [کَش باینری NixOS](https://cache.nixos.org) می‌شوند.

- [سیستم ساخت (build system)]<a id="gloss-build-system"></a>

  اصطلاحی عمومی برای نرم‌افزاری که با خودکارسازی فراخوانی کامپایلرها، لینکرها و سایر ابزارها، ساخت نرم‌افزار را تسهیل می‌کند.

  Nix می‌تواند به عنوان یک سیستم ساخت عمومی استفاده شود.
  این ابزار هیچ شناختی از هیچ زبان برنامه‌نویسی یا زنجیره ابزار خاصی ندارد.
  این جزئیات در [عبارت‌های derivation](#gloss-derivation-expression) مشخص می‌شوند.

- [بسته (closure)]<a id="gloss-closure"></a>

  بسته یک مسیر انبار، مجموعه ای از مسیرهای انبار است که مستقیماً یا غیرمستقیم از آن مسیر انبار «قابل دسترسی» هستند؛ یعنی بستهٔ آن مسیر تحت رابطهٔ *ارجاعات* است. برای یک بسته، بستهٔ derivation آن معادل وابستگی‌های زمان ساخت است، در حالی که بستهٔ [مسیر خروجی] آن معادل وابستگی‌های زمان اجرای آن است. برای استقرار صحیح، لازم است کل بسته‌ها مستقر شوند، در غیر این صورت ممکن است در زمان اجرا فایل‌ها گم شوند. دستور `nix-store --query --requisites` بسته‌های مسیرهای انبار را چاپ می‌کند.

  به عنوان مثال، اگر [شیء انبار] در مسیر `P` شامل یک [ارجاع] به یک شیء انبار در مسیر `Q` باشد، آنگاه `Q` در بستهٔ `P` قرار دارد. علاوه بر این، اگر `Q` به `R` ارجاع دهد، آنگاه `R` نیز در بستهٔ `P` قرار دارد.

  برای جزئیات بیشتر به [ارجاعات](/pages/nix-manual/store/store-object#references) مراجعه کنید.

  [بسته]: #gloss-closure

- [آدرس محتوا (content address)]<a id="gloss-content-address"></a>

  یک [*آدرس محتوا*](https://en.wikipedia.org/wiki/Content-addressable_storage)، روشی امن برای ارجاع به داده‌های تغییرناپذیر است.
  این ارجاع مستقیماً از محتوای داده‌هایی که به آن‌ها ارجاع داده می‌شود محاسبه می‌شود، به این معنی که ارجاع [*ضد دستکاری*](https://en.wikipedia.org/wiki/Tamperproofing) است — تغییرات داده‌ها همیشه باید به آدرس‌های محتوای متمایز منتهی شوند.

برای اطلاع از نحوه استفادهٔ Nix از آدرس‌دهی محتوا (content-addressing)، به موارد زیر مراجعه کنید:

    - [اشیای سیستم‌فایل مبتنی بر آدرس محتوا](/pages/nix-manual/store/file-system-object/content-address)
    - [اشیای انبار مبتنی بر آدرس محتوا](/pages/nix-manual/store/store-object/content-address)
    - [derivation مبتنی بر آدرس محتوا](#gloss-content-addressing-derivation)

  مقاله‌ی Software Heritage در مورد [*شناسه‌های ذاتی و بیرونی*](https://www.softwareheritage.org/2020/07/09/intrinsic-vs-extrinsic-identifiers) نیز مقدمهٔ خوبی برای درک ارزش آدرس‌دهی محتوا در مقایسه با سایر طرح‌های ارجاع است.

  علاوه بر آدرس‌دهی محتوا، انبار Nix از [آدرس‌دهی ورودی](#gloss-input-addressed-store-object) نیز استفاده می‌کند.

- [انبار مبتنی بر آدرس محتوا]<a id="gloss-content-addressed-store"></a>

  اصطلاح صنعتی برای سیستم‌های ذخیره‌سازی و بازیابی که از [آدرس‌دهی محتوا](#gloss-content-address) استفاده می‌کنند. انبار Nix همچنین دارای [آدرس‌دهی ورودی](#gloss-input-addressed-store-object) و فراداده (metadata) است.

- [شیء انبار مبتنی بر آدرس محتوا]<a id="gloss-content-addressed-store-object"></a>

  یک [شیء انبار] که [مبتنی بر آدرس محتوا](#gloss-content-address) است،
  یعنی [مسیر انبار] آن توسط محتوای آن تعیین می‌شود.
  این مورد شامل derivationها، خروجی‌های [derivationهای مبتنی بر آدرس محتوا](#gloss-content-addressing-derivation) و خروجی‌های [derivationهای با خروجی ثابت](#gloss-fixed-output-derivation) می‌شود.

  برای جزئیات بیشتر به [اشیای انبار مبتنی بر آدرس محتوا](/pages/nix-manual/store/store-object/content-address) مراجعه کنید.

- [derivation مبتنی بر آدرس محتوا]<a id="gloss-content-addressing-derivation"></a>

  یک derivation که صفت
  [`__contentAddressed`](/pages/nix-manual/language/advanced-attributes#adv-attr-__contentAddressed)
  در آن روی مقدار `true` تنظیم شده است.

- [derivation]<a id="gloss-derivation"></a>

  می‌توان یک derivation را به عنوان یک [تابع خالص](https://en.wikipedia.org/wiki/Pure_function) در نظر گرفت که [اشیای انبار][store object] جدیدی را از اشیای انبار موجود تولید می‌کند.

  Derivationها به شکل [فرآیندهای سیستم‌عامل که در یک sandbox اجرا می‌شوند](/pages/nix-manual/store/building) پیاده‌سازی می‌شوند.
  این sandbox به‌طور پیش‌فرض تنها اجازهٔ خواندن از اشیای انباری را می‌دهد که به عنوان ورودی مشخص شده‌اند، و تنها اجازهٔ نوشتن روی [خروجی‌های][output] تعیین‌شده را می‌دهد تا به عنوان [اشیای انبار ثبت شوند](/pages/nix-manual/store/building#processing-outputs).

  یک derivation معمولاً به عنوان یک [عبارت derivation] در [زبان Nix] مشخص می‌شود، و به یک [derivation انبار][store derivation] [فراوانی می‌یابد][instantiate].
  راه‌های متعددی برای به دست آوردن اشیای انبار از derivationهای انبار وجود دارد که به طور جمعی [تحقق‌یافتن][realise] نامیده می‌شوند.

  [derivation]: #gloss-derivation

- [عبارت derivation]<a id="gloss-derivation-expression"></a>

  توصیفی از یک [derivation انبار] با استفاده از [مقدمات `derivation` (پیش‌فرض)][./language/derivations.md] در [زبان Nix].

  [عبارت derivation]: #gloss-derivation-expression

- [مسیر derivation]<a id="gloss-derivation-path"></a>

  یک [مسیر انبار] که به طور منحصربه‌فرد یک [derivation انبار] را شناسایی می‌کند.

  برای جزئیات بیشتر به [ارجاع به derivationهای انبار](/pages/nix-manual/store/derivation#derivation-path) مراجعه کنید.

  نباید با [مسیر در حال اشتقاق] اشتباه گرفته شود.

  [مسیر derivation]: #gloss-derivation-path

- [سازندهٔ derivation (deriver)]<a id="gloss-deriver"></a>

  آن [derivation انبار] که یک [مسیر خروجی] را تولید کرده است.

  سازندهٔ یک مسیر خروجی را می‌توان با گزینه‌ی `--deriver` در دستور
  [`nix-store --query`](/pages/nix-manual/command-ref/nix-store/query)
  استعلام کرد.

- [مسیر در حال اشتقاق (deriving path)]<a id="gloss-deriving-path"></a>

  مسیرهای در حال اشتقاق راهی برای ارجاع به [اشیای انبار][store object] هستند که ممکن است هنوز [تحقق نیافته باشند][realise].

برای جزئیات بیشتر، به [مسیر derivation](/pages/nix-manual/store/derivation#deriving-path) مراجعه کنید.

  نباید با [مسیر derivation] اشتباه گرفته شود.

- [گراف جهت‌دار بدون دور]<a id="gloss-directed-acyclic-graph"></a>

  یک [گراف جهت‌دار بدون دور](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG) گرافی است که یال‌های آن دارای جهت هستند («a به b» با یال «b به a» یکی نیست) و هیچ مسیر ممکنی (که از به هم پیوستن یال‌ها ایجاد شود) یک چرخه تشکیل نمی‌دهد.

  گراف‌های DAG برای Nix بسیار مهم هستند.
  به‌ویژه، [خودارجاعی‌های][reference] غیر-[شیء انبار][store object] یک چرخه تشکیل می‌دهند.

- [ویژگی آزمایشی]<a id="gloss-experimental-feature"></a>

  قابلیتی که هنوز تثبیت نشده است و توسط پرچم‌های ویژگی‌های آزمایشی نام‌گذاری‌شده محافظت می‌شود.
  این پرچم‌ها با تنظیم [`experimental-features`](/pages/nix-manual/command-ref/conf-file#conf-experimental-features) فعال یا غیرفعال می‌شوند.

  راهنمای مشارکت در خصوص [هدف و چرخه عمر ویژگی‌های آزمایشی](/pages/nix-manual/development/experimental-features) را مطالعه کنید.

- [شیء سیستم‌فایل]<a id="gloss-file-system-object"></a>

  مدل داده‌ی Nix برای نمایش داده‌های ساده‌شده‌ی سیستم‌فایل.

  برای جزئیات بیشتر، به [شیء سیستم‌فایل](/pages/nix-manual/store/file-system-object) مراجعه کنید.

  [file system object]: #gloss-file-system-object

- [derivation خروجی‌ثابت]<a id="gloss-fixed-output-derivation"></a> (FOD)

  یک [store derivation] که در آن هش رمزنگاری‌شده‌ی [خروجی] از پیش با استفاده از صفت [`outputHash`](/pages/nix-manual/language/advanced-attributes#adv-attr-outputHash) تعیین می‌شود، و در آن فایل اجرایی [`builder`](/pages/nix-manual/language/derivations#attr-builder) به شبکه دسترسی دارد.

- [بسته / هرمتیک (Hermetic)]<a id="gloss-hermetic"></a>

  یک فرآیند ارزیابی یا ساخت زمانی هرمتیک است که بتوان مجموعه تمام ورودی‌های تأثیرگذار بر آن را به صورت مکانیکی شناسایی کرد.
  در سطح ساخت، این امر از طریق ایزوله‌سازی (sandboxing) حاصل می‌شود؛ و در سطح ارزیابی، با محدود کردن دسترسی ناخالص (همانند [ارزیابی خالص](/pages/nix-manual/command-ref/conf-file#conf-pure-eval)) به همراه [قفل‌گذاری](#gloss-locking) یا [سنجاق کردن](#gloss-pinning) ورودی‌های دریافت‌شده، که به صورت گذرا روی [دریافت‌های خالص](/pages/nix-manual/command-ref/conf-file#pure-fetch) اعمال می‌شوند.

- [IFD]<a id="gloss-ifd"></a>

  [درون‌ریزی از Derivation](/pages/nix-manual/language/import-from-derivation)

- [derivation ناخالص]<a id="gloss-impure-derivation"></a>

  [یک ویژگی آزمایشی](/pages/nix-manual/development/experimental-features#xp-feature-impure-derivations) که به derivationها اجازه می‌دهد به صراحت به عنوان ناخالص علامت‌گذاری شوند،
  تا همیشه بازسازی شوند و خروجی‌های آن‌ها توسط فرایندهای بعدی برای تحقق‌بخشیدن (realise) مجدداً استفاده نشوند.

- [شیء انبار آدرس‌دهی‌شده با ورودی]<a id="gloss-input-addressed-store-object"></a>

  یک شیء انبار که با ساخت یک derivation غیر-[مبتنی بر محتوا](#gloss-content-addressing-derivation) و غیر-[خروجی‌ثابت](#gloss-fixed-output-derivation) تولید می‌شود.

  برای جزئیات بیشتر، به [خروجی‌های derivation آدرس‌دهی‌شده با ورودی](/pages/nix-manual/store/derivation/outputs/input-address) مراجعه کنید.

- [قابل‌نصب]<a id="gloss-installable"></a>

  چیزی که می‌تواند در انبار Nix محقق (realise) شود.

  برای جزئیات بیشتر درباره [`دستورات nix`](/pages/nix-manual/command-ref/new-cli/nix) (آزمایشی)، به [قابل‌نصب‌ها](/pages/nix-manual/command-ref/new-cli/nix#installables) مراجعه کنید.

- [instantiate کردن (ساخت شیء derivation)]<a id="gloss-instantiate"></a>، instantiation

  ترجمه یک [عبارت derivation] به یک [store derivation].

  به [`nix-instantiate`](/pages/nix-manual/command-ref/nix-instantiate) مراجعه کنید که یک store derivation از یک عبارت Nix که به یک derivation ارزیابی می‌شود، تولید می‌کند.

  [instantiate]: #gloss-instantiate

- [قفل‌گذاری (Locking)]<a id="gloss-locking"></a>

در مدیریت بسته، *ثابت‌سازی نسخه (Pinning)* مفهوم یا فرآیندی است که طی آن یک فایل قفل ایجاد می‌شود. این فایل هر ورودی ارزیابی تغییرپذیری را به یک مرجع تغییرناپذیر نگاشت می‌کند، به طوری که ارزیابی‌های آینده به جای اشاره به آنچه مراجع تغییرپذیر در حال حاضر نشان می‌دهند، به همان نسخه‌های تغییرناپذیر منتهی شوند.

- [بایگانی نیکس (NAR)]<a id="gloss-nar"></a>

  یک بایگانی نیکس (*N*ix *AR*chive). این یک سریال‌سازی از یک مسیر در انبار نیکس است. این بایگانی می‌تواند شامل فایل‌های معمولی، پوشه‌ها و پیوندهای نمادین باشد. بایگانی‌های NAR با استفاده از `nix-store --dump` و `nix-store --restore` تولید و استخراج می‌شوند.

  برای جزئیات بیشتر به [بایگانی نیکس](/pages/nix-manual/store/file-system-object/content-address#serial-nix-archive) مراجعه کنید.

- [پایگاه‌داده نیکس]<a id="gloss-nix-database"></a>

  یک پایگاه‌داده SQLite برای ردیابی [مرجع]ها بین [شیء انبار]ها. این یک جزئیات پیاده‌سازی از [انبار محلی] است.

  مکان پیش‌فرض: `/nix/var/nix/db`.

  [پایگاه‌داده نیکس]: #gloss-nix-database

- [عبارت نیکس (Nix expression)]<a id="gloss-nix-expression"></a>

  یک استفاده از [زبان نیکس] که از نظر نحوی معتبر است.

  > **مثال**
  >
  > محتویات یک فایل `.nix` یک عبارت نیکس را تشکیل می‌دهند.

  عبارت‌های نیکس، [عبارت‌های درایویشن][derivation expression] را مشخص می‌کنند که در انبار نیکس به عنوان [درایویشن‌های انبار][store derivation] [مؤسس][instantiate] می‌شوند.
  سپس این درایویشن‌ها می‌توانند برای تولید [خروجی‌ها][output] [محقق][realise] شوند.

  > **مثال**
  >
  > ساخت و استقرار نرم‌افزار با استفاده از نیکس مستلزم نوشتن عبارت‌های نیکس برای توصیف [بسته‌ها][package] و ترکیب‌های آن‌ها است.

- [نمونه نیکس (Nix instance)]<a id="gloss-nix-instance"></a>
  
  1. یک نصب از نیکس، که شامل حضور یک [انبار] و مدیر بسته نیکس است که روی آن انبار کار می‌کند.
     یک نصب محلی نیکس و یک [سازنده راه دور](/pages/nix-manual/advanced-topics/distributed-builds) دو نمونه از نمونه‌های نیکس هستند.
  2. یک فرآیند در حال اجرای نیکس، مانند دستور `nix`.

- [خروجی (output)]<a id="gloss-output"></a>

  یک [شیء انبار] که توسط یک [درایویشن انبار] تولید می‌شود.
  برای جزئیات بیشتر به [آرگومان `outputs` برای تابع `derivation`](/pages/nix-manual/language/derivations#attr-outputs) مراجعه کنید.

  [خروجی]: #gloss-output

- [بسته خروجی (output closure)]\
  [بسته (closure)] یک [مسیر خروجی]. این بسته فقط شامل مواردی است که از خروجی [قابل‌دستیابی] هستند.

- [مسیر خروجی (output path)]<a id="gloss-output-path"></a>

  [مسیر انبار] به [خروجی] یک [درایویشن انبار].

  [مسیر خروجی]: #gloss-output-path

- [بسته (package)]<a id="package"></a>

  یک بسته نرم‌افزاری؛ فایل‌هایی که برای یک هدف خاص به هم تعلق دارند، به همراه فراداده (metadata).

  نیکس فایل‌ها را به عنوان [شیء سیستم‌فایل][file system object] نمایش می‌دهد و نحوه تعلق آن‌ها به یکدیگر به عنوان [مرجع]ها بین [شیء انبار]هایی که حاوی این اشیاء سیستم‌فایل هستند، کدگذاری می‌شود.

  [زبان نیکس] امکان نام‌گذاری بسته‌ها را بر حسب [مجموعه‌های صفت](/pages/nix-manual/language/types#type-attrs) شامل موارد زیر فراهم می‌کند:
  - صفاتی که به فایل‌های یک بسته اشاره دارند، معمولاً در قالب [خروجی‌های درایویشن](#gloss-output)،
  - صفاتی با فراداده، مانند اطلاعاتی درباره نحوه استفاده از بسته.

  شکل دقیق این مجموعه‌های صفت بستگی به توافق دارد.

  [بسته]: #package

- [ثابت‌سازی نسخه (Pinning)]<a id="gloss-pinning"></a>

مانند [قفل کردن](#gloss-locking)، اما یک پین تنها یک ورودی را قفل می‌کند.
یک راهکار پین‌کردن ممکن است مجموعه‌ای از پین‌ها را مدیریت کند،
اما هدف از پایین به بالا (bottom-up) را برای تثبیت مرجع یک ورودی بر اساس تقاضا برآورده می‌کند،
در حالی که قفل کردن دلالت بر رویکردی از بالا به پایین دارد که در آن همه پین‌ها در یک مکان واحد «وادار» می‌شوند.
این «وادارسازی» عموماً به واسطه مکانیسم‌های سطح بالایی مانند سیستم‌های ماژول زبان برنامه‌نویسی به دست می‌آید.
نیکس چنین سیستم ماژول محدودکننده‌ای ندارد، زیرا حتی یک فلیک نیز می‌تواند از عبارت‌هایی استفاده کند که به تنهایی پین یا قفل می‌شوند.
این امر متکی بر کامل بودن قفل نیست، بلکه بر یک ویژگی دریافت گذرا (transitive) متکی است؛ نگاه کنید به [هرمسیت](#gloss-hermetic).

- [پروفایل]<a id="gloss-profile"></a>

  یک پیوند نمادین به *محیط کاربر* فعلی یک کاربر، برای نمونه:
  `/nix/var/nix/profiles/default`.

- [خلوص]&lt;a id="gloss-خلوص"&gt;&lt;/a&gt;

  این فرض که درایویشن‌های مساوی نیکس هنگام اجرا همواره خروجی یکسانی تولید می‌کنند. این موضوع را به‌طور کلی نمی‌توان تضمین کرد (برای نمونه، یک سازنده می‌تواند به ورودی‌های خارجی مانند شبکه یا زمان سیستم متکی باشد) اما مدل نیکس آن را فرض می‌گیرد.

- [قابل‌دسترس]<a id="gloss-reachable"></a>

  یک مسیر انبار `Q` از مسیر انبار دیگری چون `P` قابل‌دسترس است اگر `Q` در *بستار* رابطهٔ *ارجاعات* باشد.

  برای جزئیات به [ارجاعات](/pages/nix-manual/store/store-object#references) مراجعه کنید.

- [محقق‌سازی (realise)]<a id="gloss-realise"></a>، تحقق

  اطمینان از اینکه یک [مسیر انبار] [معتبر][validity] است.

  این کار از راه‌های زیر قابل دستیابی است:
  - دریافت یک [شیء انبار] پیش‌ساخته از یک [جایگزین‌ساز]
  - [ساختن](/pages/nix-manual/store/building) [derivation] متناظر با آن
  - تفویض به یک [ماشین راه دور](/pages/nix-manual/command-ref/conf-file#conf-builders) و بازیابی خروجی‌ها

  برای توضیحات دقیق درباره الگوریتم، به [`nix-store --realise`](/pages/nix-manual/command-ref/nix-store/realise) مراجعه کنید.

  همچنین نگاه کنید به [`nix-build`](/pages/nix-manual/command-ref/nix-build) و [`nix build`](/pages/nix-manual/command-ref/new-cli/nix3-build) (آزمایشی).

  [realise]: #gloss-realise

- [ارجاع (reference)]<a id="gloss-reference"></a>

  یک یال از یک [شیء انبار] به شیء دیگر.

  برای جزئیات به [ارجاعات](/pages/nix-manual/store/store-object#references) مراجعه کنید.

  [reference]: #gloss-reference

  برای جزئیات به [ارجاعات](/pages/nix-manual/store/store-object#references) مراجعه کنید.

- [ارجاع‌دهنده]<a id="gloss-referrer"></a>

  یک یال معکوس از یک [شیء انبار] به شیء دیگر.

- [ملزومات (requisite)]<a id="gloss-requisite"></a>

  یک شیء انبار که از یک [شیء انبار] داده‌شده توسط یک مسیر (زنجیره‌ای از ارجاعات) [قابل‌دسترس] است.
  [بستار] مجموعهٔ ملزومات است.

  برای جزئیات به [ارجاعات](/pages/nix-manual/store/store-object#references) مراجعه کنید.

- [انبار (store)]<a id="gloss-store"></a>

  مجموعه‌ای از [اشیاء انبار][store object]، به همراه عملکردهایی برای دستکاری آن مجموعه.
  برای جزئیات به [انبار نیکس](/pages/nix-manual/store) مراجعه کنید.

  انواع زیادی از انبارها وجود دارد، برای جزئیات به [انواع انبار](/pages/nix-manual/store/types) مراجعه کنید.

  [store]: #gloss-store

- [store derivation]<a id="gloss-store-derivation"></a>

  یک [derivation] که به عنوان یک [شیء انبار] نمایش داده می‌شود.

  برای جزئیات به [Store Derivation](/pages/nix-manual/store/derivation#store-derivation) مراجعه کنید.

  [store derivation]: #gloss-store-derivation

- [شیء انبار (store object)]<a id="gloss-store-object"></a>

  بخشی از محتوای یک [انبار].

  یک شیء انبار شامل یک [شیء سیستم‌فایل]، [ارجاعات][reference] به سایر اشیاء انبار، و سایر فراداده‌ها است.
  می‌توان توسط یک [مسیر انبار] به آن ارجاع داد.

  برای جزئیات به [شیء انبار](/pages/nix-manual/store/store-object) مراجعه کنید.

  [store object]: #gloss-store-object

- [مسیر انبار]<a id="gloss-store-path"></a>

مکان یک [store object] در سیستم‌فایل، یعنی یک فرزند مستقیم از پوشه‌ی انبار Nix.

> **مثال**
>
> `/nix/store/jf6gn2dzna4nmsfbdxsd7kwhsk6gnnlr-git-2.38.1`

برای جزئیات بیشتر به [Store Path](/pages/nix-manual/store/store-path) مراجعه کنید.

[store path]: #gloss-store-path

- [string interpolation]<a id="gloss-string-interpolation"></a>

  گسترش دادن عبارت‌های محصور شده در `${'{'}'{'{'}'{'}'} {'{'}'{'}'}'{'}'}` درون یک [string]، [path] یا [attribute name].

  برای جزئیات بیشتر به [String interpolation](/pages/nix-manual/language/string-interpolation) مراجعه کنید.

  [string]: ./language/types.md#type-string
  [path]: ./language/types.md#type-path
  [attribute name]: ./language/types.md#type-attrs

- [SRI]<a id="gloss-sri"></a>

  [Subresource Integrity](https://www.w3.org/TR/SRI/) (SRI) یک [مشخصه W3C](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) برای فراداده‌های یکپارچگی است.
  Nix از فرمت هش SRI (`&lt;algorithm&gt;-&lt;Base64 hash&gt;`) استفاده می‌کند تا هش‌های محتوا را به شکلی خودتوصیف مشخص کند، زیرا الگوریتم هش بخشی از این فرمت است.

  [SRI]: #gloss-sri

- [substitute]<a id="gloss-substitute"></a>

  یک substitute (جایگزین) یک فراخوانی فرمان ذخیره‌شده در [Nix database] است که نحوه ساخت یک store object را توصیف می‌کند و مکانیزم ساخت عادی (یعنی derivationها) را دور می‌زند. معمولاً substitute با بارگیری یک نسخه پیش‌ساخته از store object از یک سرور، آن را می‌سازد.

- [substituter]<a id="gloss-substituter"></a>

  یک [store]<a id="gloss-store"></a> اضافی که Nix می‌تواند به جای ساختن store objectها، آن‌ها را از آن دریافت کند.
  اغلب substituter یک [binary cache](#gloss-binary-cache) است، اما هر انبار دیگری نیز می‌تواند به عنوان substituter عمل کند.

  برای جزئیات بیشتر به [`substituters` configuration option](/pages/nix-manual/command-ref/conf-file#conf-substituters) مراجعه کنید.

  [substituter]: #gloss-substituter

- [user environment]<a id="gloss-user-env"></a>

  یک store object خودکار ساخته‌شده که شامل مجموعه‌ای از پیوندهای نمادین (symlinks) به برنامه‌های «فعال»، یعنی سایر مسیرهای انبار (store paths) است. این موارد به طور خودکار توسط [`nix-env`](/pages/nix-manual/command-ref/nix-env) تولید می‌شوند. به *profiles* مراجعه کنید.

- [validity]<a id="gloss-validity"></a>

  یک مسیر انبار (store path) در صورتی معتبر است که تمام [store object]های موجود در [closure] آن قابل خواندن از [store] باشند.

  برای یک [local store]، این به معنای موارد زیر است:
  - مسیر انبار به یک [store object] موجود در آن [store] منتهی شود.
  - مسیر انبار در [Nix database] به عنوان معتبر فهرست شده باشد.
  - تمام مسیرهای موجود در [closure] مسیر انبار معتبر باشند.

  [validity]: #gloss-validity
  [local store]: store/types/local-store.md

[Nix language]: /pages/nix-manual/language
