# 5.4.1. Derivationها

مهم‌ترین تابع توکار، `derivation` است که برای توصیف یک [store derivation] در سطح انبار استفاده می‌شود.
برای اطلاع از ماهیت یک store derivation، به [فصل انبار](/pages/nix-manual/store/derivation) مراجعه کنید؛
این بخش صرفاً به نحوه ایجاد آن از طریق زبان Nix می‌پردازد.

این تابع توکار یک مجموعه ویژگی به عنوان ورودی دریافت می‌کند که ویژگی‌های آن مشخص‌کننده‌ ورودی‌های فرآیند هستند.
این تابع یک مجموعه ویژگی خروجی می‌دهد و به عنوان اثر جانبی ارزیابی، یک [store derivation] تولید می‌کند.

[store derivation]: /pages/nix-manual/glossary#gloss-store-derivation
## ویژگی‌های ورودی

### الزامی

- [`name`]<a id="attr-name"></a> ([String](/pages/nix-manual/language/types#type-string))

  یک نام نمادین برای derivation.
  برای اینکه ببینید این نام روی چه چیزی تأثیر می‌گذارد، به [خروجی‌های derivation](/pages/nix-manual/store/derivation/outputs#outputs) مراجعه کنید.

  [store path]: store/store-path.md

  > **مثال**
  >

> ```nix
> derivation {
>   name = "hello";
>   # ...
> }
> ```
>
  > مسیر derivation برابر با `/nix/store/&lt;hash&gt;-hello.drv` خواهد بود.
  > مسیرهای [output](#attr-outputs) به شکل `/nix/store/&lt;hash&gt;-hello[-&lt;output&gt;]` خواهند بود.

- [`system`]<a id="attr-system"></a> ([String](/pages/nix-manual/language/types#type-string))

  مراجعه کنید به [system](/pages/nix-manual/store/derivation#system).

  > **مثال**
  >
  > اعلام یک derivation برای ساخت روی یک نوع سیستم خاص:
  >

> ```nix
> derivation {
>   # ...
>   system = "x86_64-linux";
>   # ...
> }
> ```

> **مثال**
>
> یک derivation را اعلام کنید تا روی نوع سیستمی که عبارت را ارزیابی می‌کند ساخته شود:
>

> ```nix
> derivation {
>   # ...
>   system = builtins.currentSystem;
>   # ...
> }
> ```
> [`builtins.currentSystem`](/pages/nix-manual/language/builtins#builtins-currentSystem) دارای مقدار [`system` configuration option] است و به طور پیش‌فرض روی نوع سیستم نصب فعلی Nix تنظیم می‌شود.

- [`builder`]<a id="attr-builder"></a> ([Path](/pages/nix-manual/language/types#type-path) | [String](/pages/nix-manual/language/types#type-string))

  بخش [builder](/pages/nix-manual/store/derivation#builder) را ببینید.

  > **مثال**
  >
  > از فایل واقع در مسیر `/bin/bash` به عنوان فایل اجرایی سازنده (Builder) استفاده کنید:
  >

> ```nix
> derivation {
>   # ...
>   builder = "/bin/bash";
>   # ...
> };
> ```

  > **مثال**
  >
  > کپی کردن یک فایل محلی به انبار نیکس برای استفاده به عنوان فایل اجرایی سازنده (builder):
  >

> ```nix
> derivation {
>   # ...
>   builder = ./builder.sh;
>   # ...
> };
> ```

> **مثال**
>
> از یک فایل متعلق به درایویشن دیگری به‌عنوان فایل اجرایی سازنده (builder) استفاده کنید:
>

> ```nix
> let pkgs = import <nixpkgs> {}; in
> derivation {
>   # ...
>   builder = "${pkgs.python}/bin/python";
>   # ...
> };
> ```

### اختیاری

- [`args`]<a id="attr-args"></a> ([فهرست](/pages/nix-manual/language/types#type-list) [رشته](/pages/nix-manual/language/types#type-string))

  پیش‌فرض: `[ ]`

  به [args](/pages/nix-manual/store/derivation#args) مراجعه کنید.

  > **مثال**
  >
  > ارسال آرگومان‌ها به Bash برای تفسیر یک فرمان شل:
  >

> ```nix
> derivation {
>   # ...
>   builder = "/bin/bash";
>   args = [ "-c" "echo hello world > $out" ];
>   # ...
> };
> ```

- [`outputs`]<a id="attr-outputs"></a> ([فهرست](/pages/nix-manual/language/types#type-list) از [رشته](/pages/nix-manual/language/types#type-string))

  پیش‌فرض: `[ "out" ]`

  خروجی‌های نمادین درایویشن.
  نام هر خروجی به عنوان یک متغیر محیطی به فایل اجرایی [`builder`](#attr-builder) ارسال می‌شود که مقدار آن روی [مسیر انبار] مربوطه تنظیم شده است.

  به طور پیش‌فرض، یک درایویشن یک خروجی واحد به نام `out` تولید می‌کند.
  با این حال، درایویشن‌ها می‌توانند چندین خروجی تولید کنند.
  این امر به [اشیاء انبار] (store objects) مرتبط و [بستارهای](/pages/nix-manual/glossary#gloss-closure) آن‌ها اجازه می‌دهد تا به صورت جداگانه کپی یا [جمع‌آوری زباله (garbage collection)](/pages/nix-manual/glossary#gloss-closure) شوند.

  > **مثال**
  >
  > یک بسته کتابخانه را تصور کنید که یک کتابخانه پویا، فایل‌های هدر و مستندات را فراهم می‌کند.
  > برنامه‌ای که به چنین کتابخانه‌ای لینک می‌شود، در زمان اجرا نیازی به فایل‌های هدر و مستندات ندارد و در زمان ساخت نیز نیازی به مستندات ندارد.
  > بنابراین، بسته کتابخانه می‌تواند موارد زیر را مشخص کند:
  >

> ```nix
> derivation {
>   # ...
>   outputs = [ "lib" "dev" "doc" ];
>   # ...
> }
> ```
>
> این کار باعث می‌شود Nix متغیرهای محیطی `lib`، `dev` و `doc` را که حاوی مسیرهای انبار موردنظر برای هر خروجی هستند، به سازنده (Builder) ارسال کند.
> سازنده (Builder) معمولاً کاری شبیه به این انجام خواهد داد:
>

> ```bash
> ./configure \
>   --libdir=$lib/lib \
>   --includedir=$dev/include \
>   --docdir=$doc/share/doc
> ```
>
> برای یک بسته با سبک Autoconf.

نام یک خروجی با نام derivation ترکیب می‌شود تا [بخش نام](/pages/nix-manual/store/store-path#name) مربوط به مسیر انبارِ خروجی را ایجاد کند، مگر اینکه `out` باشد؛ در این صورت، فقط از نام derivation استفاده می‌شود.

> **مثال**
>
>

> ```nix
> derivation {
>   name = "example";
>   outputs = [ "lib" "dev" "doc" "out" ];
>   # ...
> }
> ```
> مسیر derivation انبار `/nix/store/&lt;hash&gt;-example.drv` خواهد بود.
> مسیرهای خروجی عبارتند از
> - `/nix/store/&lt;hash&gt;-example-lib`
> - `/nix/store/&lt;hash&gt;-example-dev`
> - `/nix/store/&lt;hash&gt;-example-doc`
> - `/nix/store/&lt;hash&gt;-example`

شما می‌توانید با انتخاب هر خروجی از یک derivation به عنوان یک صفت (attribute)، به آن ارجاع دهید.
نخستین عنصر `outputs`، *خروجی پیش‌فرض* را تعیین می‌کند و در نهایت در سطح بالا قرار می‌گیرد.

> **مثال**
>
> یک خروجی را با نام صفت (attribute) انتخاب کنید:
>

> ```nix
> let
>   myPackage = derivation {
>     name = "example";
>     outputs = [ "lib" "dev" "doc" "out" ];
>     # ...
>   };
> in myPackage.dev
> ```
>
> از آنجا که `lib` اولین خروجی است، `myPackage` معادل `myPackage.lib` است.

- برای مشاهده صفت‌های اختیاری و کمتر استفاده‌شده‌ی بیشتر، به [صفات پیشرفته](/pages/nix-manual/language/advanced-attributes) مراجعه کنید.

  

- هر صفت دیگری به عنوان یک متغیر محیطی به سازنده منتقل می‌شود.
  مقادیر صفت‌ها به شکل زیر به متغیرهای محیطی تبدیل می‌شوند:

    - رشته‌ها بدون تغییر منتقل می‌شوند.

    - اعداد صحیح به نماد اعشاری تبدیل می‌شوند.

    - اعداد اعشاری با دقت از‌پیش‌تعیین‌شده به نماد اعشاری ساده یا علمی تبدیل می‌شوند.

    - یک *مسیر* (مثلاً `../foo/sources.tar`) باعث می‌شود که فایل ارجاع‌داده‌شده به انبار کپی شود؛ مکان آن در انبار در متغیر محیطی قرار می‌گیرد. ایده این است که تمام منابع باید در انبار Nix قرار داشته باشند، زیرا تمام ورودی‌های یک derivation باید در انبار Nix سکونت داشته باشند.

    - یک *derivation* باعث می‌شود که آن derivation پیش از derivation فعلی ساخته شود. متغیر محیطی روی [مسیر انبار] [خروجی](#attr-outputs) پیش‌فرض آن derivation تنظیم می‌شود.

    - فهرست‌های انواع قبلی نیز مجاز هستند. آن‌ها به سادگی و با جداکنندهٔ فاصله به یکدیگر متصل می‌شوند.

    - مقدار `true` به عنوان رشته‌ی `1` منتقل می‌شود و `false` و `null` به عنوان یک رشته‌ی خالی منتقل می‌شوند.
