# اجرای تست‌ها

## تحلیل پوشش تست

[گزارش تحلیل پوشش تست] به‌صورت آنلاین در دسترس است.
می‌توانید آن را خودتان بسازید:

[گزارش تحلیل پوشش تست]: https://hydra.nixos.org/job/nix/master/coverage/latest/download-by-type/report/coverage

```
# nix build .#hydraJobs.coverage
# xdg-open ./result/index.html
```

[سوابق گسترده‌ای از معیارهای ساخت](https://hydra.nixos.org/job/nix/master/coverage#tabs-charts)، مانند پوشش تست در طول زمان، به صورت آنلاین نیز در دسترس هستند.

## تست‌های واحد

تست‌های واحد با استفاده از چارچوب‌های [googletest] و [rapidcheck] تعریف می‌شوند.

[googletest]: https://google.github.io/googletest/
[rapidcheck]: https://github.com/emil-e/rapidcheck
[property testing]: https://en.wikipedia.org/wiki/Property_testing

### ساختار فایل‌های منبع و هدر

> نمونه‌ای از چند فایل که بخش زیادی از موارد توصیف‌شده در ادامه را نشان می‌دهند
>
```
> src
> ├── libexpr
> │   ├── meson.build
> │   ├── include/nix/expr/value/context.hh
> │   ├── value/context.cc
> │   …
> │
> ├── libutil-tests
> │   ├── meson.build
> │   …
> │   ├── data
> │   │   ├── git/tree.txt
> │       …
> │
> ├── libexpr-test-support
> │   ├── meson.build
> │   ├── include/nix/expr
> │   │   ├── meson.build
> │   │   └── tests
> │   │       ├── value/context.hh
> │   │       …
> │   ├── tests
> │       ├── value/context.cc
> │       …
> │
> ├── libexpr-tests
> │   ├── meson.build
> │   ├── value/context.cc
> │    …
> …
> ```

آزمون‌ها برای هر کتابخانه Nix (`libnixexpr`، `libnixstore` و غیره) در داخل یک پوشه به نام `src/${library_name_without-nix}-test` قرار دارند.
با فرض وجود یک جفت رابط (سرآیند) و پیاده‌سازی در کتابخانه اصلی، مثلاً `src/libexpr/include/nix/expr/value/context.hh` و `src/libexpr/value/context.cc`، ما آزمون‌های آن را در `src/libexpr-tests/value/context.cc` می‌نویسیم و (احتمالاً) رابط‌های اضافی را برای اهداف آزمایشی در `src/libexpr-test-support/include/nix/expr/tests/value/context.hh` و `src/libexpr-test-support/tests/value/context.cc` اعلام/تعریف می‌کنیم.

داده‌های مربوط به تست‌های واحد در یک زیرپوشه `data` متعلق به پوشهٔ هر فایل اجرایی تست واحد ذخیره می‌شوند.
برای نمونه، کد `libnixstore` در `src/libstore` قرار دارد و داده‌های تست آن در `src/libstore-tests/data` هستند.
مسیر پوشهٔ `src/${library_name_without-nix}-test/data` از طریق متغیر محیطی `_NIX_TEST_UNIT_DATA` به فایل اجرایی تست واحد ارسال می‌شود.
توجه داشته باشید که هر فایل اجرایی تنها داده‌های مربوط به تست‌های خودش را دریافت می‌کند.

کتابخانه‌های تست واحد در `src/${library_name_without-nix}-test-support` قرار دارند.
تمام سرآیندها در یک زیرپوشه `tests` قرار گرفته‌اند تا با دستور `#include "nix/tests/"` وارد (include) شوند.

استفاده از تمام این پوشه‌های مجزا برای تست‌های واحد ممکن است نامطلوب به نظر برسد، زیرا برای مثال تست‌ها «درست در کنار» بخشی از کدی که در حال تست آن هستند قرار ندارند.
اما سازماندهی تست‌ها به این روش یک مزیت بزرگ دارد:
هیچ خطری وجود ندارد که کاراکترهای عام‌شمول (wildcards) سیستم ساختِ کتابخانه، به اشتباه کد تستی را انتخاب کنند که نباید به عنوان بخشی از کتابخانه ساخته و نصب شود.

### اجرای تست‌ها

شما می‌توانید کل مجموعه تست را با دستور `meson test` از داخل پوشه ساخت Meson اجرا کنید، یا تست‌های یک کامپوننت خاص را با دستور `meson test nix-store-tests` اجرا نمایید.
همچنین دانستن متغیرهای محیطی که Google Test می‌پذیرد خالی از لطف نیست:

1. [`GTEST_FILTER`](https://google.github.io/googletest/advanced.html#running-a-subset-of-the-tests)

   این گزینه برای فیلتر کردن با دانه‌بندی ریزترِ تست‌هایی که باید اجرا شوند، استفاده می‌شود.


2. [`GTEST_BRIEF`](https://google.github.io/googletest/advanced.html#suppressing-test-passes)

   این گزینه برای جلوگیری از ثبت گزارش (log) تست‌های موفق استفاده می‌شود.

3. [`GTEST_BREAK_ON_FAILURE`](https://google.github.io/googletest/advanced.html#turning-assertion-failures-into-break-points)

   این گزینه برای ایجاد یک نقطه توقف (breakpoint) در دیباگر هنگام وقوع خطای اَسرشن (assertion failure) استفاده می‌شود.

با ترکیب دو مورد اول، ممکن است کسی دستور زیر را اجرا کند

```bash
GTEST_BRIEF=1 GTEST_FILTER='ErrorTraceTest.*' meson test nix-expr-tests -v
```

### اشکال‌زدایی تست‌ها

برای اشکال‌زدایی، ترکیب گزینه سوم بالا با پرچم [`--gdb`](https://mesonbuild.com/Unit-tests.html#other-test-options) در Meson مفید است:

```bash
GTEST_BRIEF=1 GTEST_FILTER='Group.my-failing-test' meson test nix-expr-tests --gdb
```

این کار اقدامات زیر را انجام خواهد داد:

1. اجرای تست واحد با GDB

2. اجرای فقط `Group.my-failing-test`

3. متوقف کردن برنامه در هنگام شکست خوردن تست، به کاربر اجازه می‌دهد تا دستورات دلخواهی را به GDB صادر کند.

### تست مشخصه‌سازی { #characterisation-testing-unit }

برای بحث گسترده‌تر پیرامون تست مشخصه‌سازی، به [تست مشخصه‌سازی تابعی](#characterisation-testing-functional) مراجعه کنید.

مشابه مشخصه‌سازی تابعی، از `_NIX_TEST_ACCEPT=1` نیز استفاده می‌شود.
برای مثال:
```shell-session
$ _NIX_TEST_ACCEPT=1 meson test nix-store-tests -v
...
[  SKIPPED ] WorkerProtoTest.string_read
[  SKIPPED ] WorkerProtoTest.string_write
[  SKIPPED ] WorkerProtoTest.storePath_read
[  SKIPPED ] WorkerProtoTest.storePath_write
...
```
نتیجه‌ی مورد انتظار «gold master» را برای تست‌های توصیفی `libnixstore` بازسازی خواهد کرد.
تست‌های توصیفی خود را به عنوان «رد شده (skipped)» علامت‌گذاری خواهند کرد، زیرا به جای تست کردن واقعی چیزی، نتیجه‌ی مورد انتظار را بازسازی کرده‌اند.

### تست طرح‌واره‌ی JSON

در پوشه‌ی `doc/manual/source/protocols/json/` تعدادی صفحه راهنما داریم که از [JSON Schema](https://json-schema.org/) تولید شده‌اند.
آن طرح‌واره‌ی JSON در برابر داده‌های تست فایل JSON که در [تست‌های توصیفی](#characterisation-testing-unit) برای سریال‌سازی و د سریال‌سازی JSON در `src/json-schema-checks` استفاده می‌شوند، تست می‌شود.
با استفاده از تست‌های سریال‌سازی و دسریال‌سازی JSON و این تست همان داده‌ها در برابر طرح‌واره، اطمینان حاصل می‌کنیم که راهنما، پیاده‌سازی و یک طرح‌واره‌ی قابل‌خواندن برای ماشین، همگی با یکدیگر هماهنگ هستند.

### کتابخانه‌های پشتیبانی از تست واحد

هدرها و کدهایی وجود دارند که نه تنها برای تست کتابخانه‌ی مورد نظر، بلکه برای کتابخانه‌های پایین‌دست (downstream) نیز استفاده می‌شوند.
برای مثال، ما [property testing] را با کتابخانه‌ی [rapidcheck] انجام می‌دهیم.
این کار مستلزم نوشتن «نمونه‌های» `Arbitrary` است که برای توصیف نحوه‌ی تولید مقادیر یک نوع داده‌ی مشخص به منظور اجرای تست‌های ویژگی (property tests) استفاده می‌شوند.
از آنجا که انواع داده شامل انواع داده‌ی دیگر هستند، «نمونه‌های» `Arbitrary` برای یک نوع داده نه تنها برای تست کردن همان نوع مفید هستند، بلکه برای هر نوع داده‌ی دیگری که شامل آن باشد نیز کاربرد دارند.
انواع پایین‌دست مکرراً حاوی انواع بالادست هستند، بنابراین بسیار مهم است که نمونه‌های arbitrary را به اشتراک بگذاریم تا تست‌های ویژگی کتابخانه‌های پایین‌دست نیز بتوانند از آن‌ها استفاده کنند.

مهم است که این کتابخانه‌های تستی خودشان شامل هیچ تست واقعی نباشند.
در برخی پلتفرم‌ها، آن‌ها به عنوان بخشی از هر فایل اجرایی تستی که از آن‌ها استفاده می‌کند اجرا می‌شوند که امری تکراری و اضافی است.
در سایر پلتفرم‌ها اصلا اجرا نخواهند شد.

## تست‌های تابعی

تست‌های تابعی در زیر پوشه‌ی `tests/functional` قرار دارند و در `tests/functional/meson.build` فهرست شده‌اند.
هر تست یک اسکریپت Bash است.

تست‌های تابعی در طول `installCheck` در ساخت بسته `nix` و همچنین جدا از ساخت، در تست‌های ماشین مجازی اجرا می‌شوند.

### اجرای کل مجموعه تست

کل مجموعه تست (تست‌های تابعی و واحد) را می‌توان با دستور زیر اجرا کرد:

```shell-session
$ checkPhase
```

### گروه‌بندی تست‌ها

گاهی اوقات گروه‌بندی تست‌های مرتبط مفید است تا بتوان آن‌ها را به‌راحتی و بدون اجرای کل مجموعه تست با هم اجرا کرد.
هر گروه تست در یک زیرپوشه از `tests` قرار دارد.
برای مثال، `tests/functional/ca/meson.build` یک گروه تست `ca` را برای خروجی‌های درایویشن با آدرس‌دهی محتوا تعریف می‌کند.

آن گروه تست را می‌توان به شکل زیر اجرا کرد:

```shell-session
$ meson test --suite ca
ninja: Entering directory `/home/jcericson/src/nix/master/build'
ninja: no work to do.
[1-20/20] 🌑 nix-functional-tests:ca / ca/why-depends                                1/20 nix-functional-tests:ca / ca/nix-run                                  OK               0.16s
[2-20/20] 🌒 nix-functional-tests:ca / ca/why-depends                                2/20 nix-functional-tests:ca / ca/import-derivation                        OK               0.17s
```

### اجرای تست‌های منفرد

تست‌های منفرد را می‌توان با `meson` اجرا کرد:

```shell-session
$ meson test --verbose ${testName}
ninja: Entering directory `/home/jcericson/src/nix/master/build'
ninja: no work to do.
1/1 nix-functional-tests:main / ${testName}        OK               0.41s

Ok:                 1
Expected Fail:      0
Fail:               0
Unexpected Pass:    0
Skipped:            0
Timeout:            0

Full log written to /home/jcericson/src/nix/master/build/meson-logs/testlog.txt
```

پرچم `--verbose` باعث می‌شود که Meson خروجی کنسول هر تست را نیز برای اشکال‌زدایی آسان‌تر نمایش دهد.
سپس اسکریپت تست با `set -x` ردیابی (traced) می‌شود و خروجی با وقوع آن نمایش داده می‌شود،
صرف‌نظر از اینکه تست موفق شود یا شکست بخورد.

همچنین تست‌ها را می‌توان مستقیماً و بدون `meson` اجرا کرد:

```shell-session
$ TEST_NAME=${testName} NIX_REMOTE='' PS4='+(${BASH_SOURCE[0]-$0}:$LINENO) tests/functional/${testName}.sh
+(${testName}.sh:1) foo
output from foo
+(${testName}.sh:2) bar
output from bar
...
```

### اشکال‌زدایی تست‌های تابعی ناموفق

هنگامی که یک تست تابعی با شکست مواجه می‌شود، معمولاً این اتفاق در جایی در میانه‌ی اسکریپت رخ می‌دهد.

برای فهمیدن مشکل، بسیار راحت است که تست را به طور عادی تا دستور `nix` ناموفق اجرا کنید و سپس آن دستور را با یک دیباگر مانند GDB اجرا کنید.

برای مثال، اگر اسکریپت به شکل زیر باشد:

```bash
foo
nix blah blub
bar
```
این‌گونه ویرایش کنید:

```diff
 foo
-nix blah blub
+gdb --args nix blah blub
 bar
```

سپس، اجرای تست با [`--interactive`](https://mesonbuild.com/Unit-tests.html#other-test-options) از تسخیر ترمینال توسط Meson جلوگیری می‌کند تا بتوانید پس از رسیدن اسکریپت به آن نقطه، وارد محیط GDB شوید:

```shell-session
$ meson test ${testName} --interactive
...
+ gdb blash blub
GNU gdb (GDB) 12.1
...
(gdb)
```

می‌توان فراخوانی Nix را به تمام روش‌های معمول دیباگ (اشکال‌زدایی) کرد.
برای مثال، `run` را وارد کنید تا فراخوانی Nix آغاز شود.

### آزمایش توصیف رفتار { #characterisation-testing-functional }

گاهی اوقات، Nix از تکنیکی به نام [آزمایش توصیف رفتار](https://en.wikipedia.org/wiki/Characterization_test) به عنوان بخشی از تست‌های عملکردی استفاده می‌کند.
این تکنیک شامل گنجاندن خروجی/رفتار دقیق نسخه قبلی Nix در یک تست است تا بررسی شود که Nix در آینده نیز به تولید همان رفتار ادامه می‌دهد.

برای مثال، این تکنیک برای تست‌های زبان استفاده می‌شود تا هم مقدار نهایی چاپ‌شده در صورت موفقیت‌آمیز بودن ارزیابی، و هم هرگونه خطا و هشدار مواجه‌شده بررسی شود.

بازسازی خروجی مورد انتظار اغلب مفید است.
برای انجام این کار، تست(های) شکست‌خورده را با `_NIX_TEST_ACCEPT=1` مجدداً اجرا کنید.
برای مثال:
```bash
_NIX_TEST_ACCEPT=1 meson test lang
```
این قرارداد همچنین با [آزمون‌های واحد مشخصه‌سازی](#characterisation-testing-unit) نیز به اشتراک گذاشته شده است.

یک وضعیت جالب برای مستندسازی، حالتی است که این آزمون‌ها «بیش‌برازش‌شده» (overfitted) هستند.
آزمون‌های زبان نیز نمونه‌ای از این موضوع هستند.
خروجی موفقیت‌آمیز مورد انتظار ارزیابی باید بسیار پایدار باشد — ما قصد نداریم تغییرات خراب‌کننده (breaking changes) در (بخش‌های پایدار) زبان Nix ایجاد کنیم.
با این حال، خطاها و اخطارهای حین ارزیابی (چه موفقیت‌آمیز و چه ناموفق) به این صورت پایدار نیستند.
ما آزادی عمل داریم که نحوه نمایش آن‌ها را در هر زمانی تغییر دهیم.

شاید تعجب‌آور باشد که ما رفتارهای غیرمعیاری مانند خروجی‌های تشخیصی را آزمایش می‌کنیم.
خروجی‌های تشخیصی در واقع یک رابط پایدار نیستند، اما همچنان برای کاربران اهمیت دارند.
با ثبت خروجی مورد انتظار، مجموعه آزمون در برابر تغییرات تصادفی محافظت می‌کند و اطمینان حاصل می‌کند که *نتیجه* (و نه فقط کدی که آن را پیاده‌سازی می‌کند) مسیرهای کد تشخیصی تحت بازبینی کد قرار دارد.
رگرسیون‌ها شناسایی می‌شوند و بهبودها همیشه در بازبینی کد نمایان می‌شوند.

برای اطمینان از اینکه تست مشخصه‌سازی تغییر عمدی این رابط‌ها را دشوارتر نمی‌کند، همیشه باید یک روش آسان برای بازسازی خروجی مورد انتظار وجود داشته باشد، همان‌طور که این کار را با `_NIX_TEST_ACCEPT=1` انجام می‌دهیم.

### اجرای تست‌های عملکردی روی NixOS

ما تست‌های عملکردی را نه تنها در فرآیند ساخت (build)، بلکه در تست‌های ماشین مجازی (VM) نیز اجرا می‌کنیم.
این کار به ما کمک می‌کند تا اطمینان حاصل کنیم که Nix روی NixOS و محیط‌هایی که ویژگی‌های مشابهی دارند و بازتولید آن‌ها در یک محیط ساخت دشوار است، به درستی کار می‌کند.

این تست‌ها را می‌توان با دستور زیر اجرا کرد:

```shell
nix build .#hydraJobs.tests.functional_user
```

به‌طور کلی، این ساخت کافی است، اما در نسخه‌های شبانه یا ادغام مداوم (CI)، ما صفات `functional_root` و `functional_trusted` را نیز تست می‌کنیم که در آن‌ها مجموعه تست با سطوح متفاوتی از مجوز اجرا می‌شود.

## تست‌های یکپارچه‌سازی

تست‌های یکپارچه‌سازی در فلیک Nix تحت صفت `hydraJobs.tests` تعریف شده‌اند.
این تست‌ها شامل هر چیزی هستند که باید با سرویس‌های خارجی تعامل داشته باشند یا Nix را در یک راه‌اندازی توزیع‌شده غیربدیهی اجرا کنند.
از آنجا که این تست‌ها هزینه‌بر هستند و به چیزی فراتر از امکانات ارائه‌شده توسط راه‌اندازی استاندارد GitHub Actions نیاز دارند، بیشتر آن‌ها فقط روی شاخه‌ی master (در <https://hydra.nixos.org/jobset/nix/master>) اجرا می‌شوند.

شما می‌توانید آن‌ها را به‌صورت دستی با دستور `nix build .#hydraJobs.tests.{testName}` یا `nix-build -A hydraJobs.tests.{testName}` اجرا کنید.

## تست‌های نصب‌کننده

محیط ادغام مداوم GitHub Actions در مخزن Nix همچنین نصب‌کننده را روی درخواست‌های پول (PR) تست می‌کند. این کار نیازی به راه‌اندازی اضافی ندارد و از [GHA Artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) استفاده می‌کند و می‌تواند در هر فورک از مخزن Nix اجرا شود.

- کار (job) `tests` نصب‌کننده‌ها را برای پلتفرم‌های زیر تولید کرده و آن‌ها را به‌عنوان یک فرآوردهٔ ساخت (artifact) بارگذاری می‌کند:
  - `x86_64-linux`
  - `aarch64-darwin`

- کار `installer_test` (که روی لینوکس و macOS اجرا می‌شود) تلاش می‌کند تا Nix را با نصب‌کننده‌ی ذخیره‌شده در کش (cached) نصب کرده و یک دستور پیش‌پاافتاده‌ی Nix را اجرا کند.
- هم نصب‌کننده‌ی اسکریپتی و هم [نصب‌کننده‌ی مستقل مبتنی بر زبان Rust](https://github.com/NixOS/nix-installer) تست می‌شوند.

شما می‌توانید تاربال و اسکریپت نصب‌کننده را به‌صورت دستی با اجرای دستور `nix build .#hydraJobs.installerScriptForGHA.<system-double>` تولید کنید.

## کار کردن روی مستندات

### استفاده از نصب‌کننده‌ی تولیدشده توسط ادغام مداوم برای تست دستی

پس از اتمام اجرای ادغام مداوم، می‌توانید خروجی را بررسی کنید تا فرآوردهٔ ساخت نصب‌کننده را استخراج کنید:
1. روی نمای جزئیات اجرای ادغام مداوم کلیک کنید.
2. به سمت پایین به بخش `Artifacts` اسکرول کنید.
3. فرآوردهٔ ساخت نصب‌کننده‌ی مربوطه را بارگیری کنید (`installer-darwin` برای `aarch64-darwin` و `installer-linux` برای `x86_64-linux`).
4. فرآوردهٔ ساخت `.zip` بارگیری‌شده را از حالت فشرده خارج کنید.
5. برای تولید یک دستور نصب، مسیر فرآوردهٔ ساخت استخراج‌شده را در این الگو قرار دهید:
```console
    sh <path/to/artifact>/install --tarball-url-prefix file://<path/to/artifact>
    ```
