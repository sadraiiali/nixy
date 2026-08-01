# درایویشن‌ها

مهم‌ترین تابع توکار، `derivation` است که برای توصیف یک [store derivation] در سطح انبار استفاده می‌شود.
برای اطلاع از ماهیت یک store derivation، به [فصل انبار](@docroot@/store/derivation/index.md) مراجعه کنید؛
این بخش صرفاً به نحوه ایجاد آن از طریق زبان Nix می‌پردازد.

این تابع توکار یک مجموعه ویژگی به عنوان ورودی دریافت می‌کند که ویژگی‌های آن مشخص‌کننده ورودی‌های فرآیند هستند.
این تابع یک مجموعه ویژگی خروجی می‌دهد و به عنوان اثر جانبی ارزیابی، یک [store derivation] تولید می‌کند.

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

## ویژگی‌های ورودی

### الزامی

- [`name`]{#attr-name} ([String](@docroot@/language/types.md#type-string))

  یک نام نمادین برای derivation.
  برای اینکه ببینید این نام روی چه چیزی تأثیر می‌گذارد، به [خروجی‌های derivation](@docroot@/store/derivation/outputs/index.md#outputs) مراجعه کنید.

  [store path]: @docroot@/store/store-path.md

  > **مثال**
  >
```nix
  > derivation {
  >   name = "hello";
  >   # ...
  > }
  > ```
>
  > مسیر derivation برابر با `/nix/store/<hash>-hello.drv` خواهد بود.
  > مسیرهای [output](#attr-outputs) به شکل `/nix/store/<hash>-hello[-<output>]` خواهند بود.

- [`system`]{#attr-system} ([String](@docroot@/language/types.md#type-string))

  مراجعه کنید به [system](@docroot@/store/derivation/index.md#system).

  > **مثال**
  >
  > اعلام یک derivation برای ساخت روی یک نوع سیستم خاص:
  >
```nix
  > derivation {
  > # ...
  > system = "x86_64-linux";
  > # ...
  > }
  > ```

> **مثال**
>
> یک derivation را اعلام کنید تا روی نوع سیستمی که عبارت را ارزیابی می‌کند ساخته شود:
>
```nix
  > derivation {
  >   # ...
  >   system = builtins.currentSystem;
  >   # ...
  > }
  > ```
> [`builtins.currentSystem`](@docroot@/language/builtins.md#builtins-currentSystem) دارای مقدار [`system` configuration option] است و به طور پیش‌فرض روی نوع سیستم نصب فعلی Nix تنظیم می‌شود.

- [`builder`]{#attr-builder} ([Path](@docroot@/language/types.md#type-path) | [String](@docroot@/language/types.md#type-string))

  بخش [builder](@docroot@/store/derivation/index.md#builder) را ببینید.

  > **مثال**
  >
  > از فایل واقع در مسیر `/bin/bash` به عنوان فایل اجرایی سازنده (Builder) استفاده کنید:
  >
```nix
  > derivation {
  > # ...
  > builder = "/bin/bash";
  > # ...
  > };
  > ```

<!-- -->

  > **مثال**
  >
  > کپی کردن یک فایل محلی به انبار نیکس برای استفاده به عنوان فایل اجرایی سازنده (builder):
  >
```nix
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
```nix
  > let pkgs = import <nixpkgs> {}; in
  > derivation {
  > # ...
  > builder = "${pkgs.python}/bin/python";
  > # ...
  > };
  > ```

### اختیاری

- [`args`]{#attr-args} ([فهرست](@docroot@/language/types.md#type-list) [رشته](@docroot@/language/types.md#type-string))

  پیش‌فرض: `[ ]`

  به [args](@docroot@/store/derivation/index.md#args) مراجعه کنید.

  > **مثال**
  >
  > ارسال آرگومان‌ها به Bash برای تفسیر یک فرمان شل:
  >
```nix
  > derivation {
  >   # ...
  >   builder = "/bin/bash";
  >   args = [ "-c" "echo hello world > $out" ];
  >   # ...
  > };
  > ```

- [`outputs`]{#attr-outputs} ([فهرست](@docroot@/language/types.md#type-list) از [رشته](@docroot@/language/types.md#type-string))

  پیش‌فرض: `[ "out" ]`

  خروجی‌های نمادین درایویشن.
  نام هر خروجی به عنوان یک متغیر محیطی به فایل اجرایی [`builder`](#attr-builder) ارسال می‌شود که مقدار آن روی [مسیر انبار] مربوطه تنظیم شده است.

  به طور پیش‌فرض، یک درایویشن یک خروجی واحد به نام `out` تولید می‌کند.
  با این حال، درایویشن‌ها می‌توانند چندین خروجی تولید کنند.
  این امر به [اشیاء انبار] (store objects) مرتبط و [بستارهای](@docroot@/glossary.md#gloss-closure) آن‌ها اجازه می‌دهد تا به صورت جداگانه کپی یا [جمع‌آوری زباله (garbage collection)](@docroot@/glossary.md#gloss-closure) شوند.

  > **مثال**
  >
  > یک بسته کتابخانه را تصور کنید که یک کتابخانه پویا، فایل‌های هدر و مستندات را فراهم می‌کند.
  > برنامه‌ای که به چنین کتابخانه‌ای لینک می‌شود، در زمان اجرا نیازی به فایل‌های هدر و مستندات ندارد و در زمان ساخت نیز نیازی به مستندات ندارد.
  > بنابراین، بسته کتابخانه می‌تواند موارد زیر را مشخص کند:
  >
```nix
  > derivation {
  > # ...
  > outputs = [ "lib" "dev" "doc" ];
  > # ...
  > }
  > ```
>
> این کار باعث می‌شود Nix متغیرهای محیطی `lib`، `dev` و `doc` را که حاوی مسیرهای انبار موردنظر برای هر خروجی هستند، به سازنده (Builder) ارسال کند.
> سازنده (Builder) معمولاً کاری شبیه به این انجام خواهد داد:
>
```bash
  > ./configure \
  >   --libdir=$lib/lib \
  >   --includedir=$dev/include \
  >   --docdir=$doc/share/doc
  > ```
>
> برای یک بسته با سبک Autoconf.

نام یک خروجی با نام derivation ترکیب می‌شود تا [بخش نام](@docroot@/store/store-path.md#name) مربوط به مسیر انبارِ خروجی را ایجاد کند، مگر اینکه `out` باشد؛ در این صورت، فقط از نام derivation استفاده می‌شود.

> **مثال**
>
>
```nix
  > derivation {
  > name = "example";
  > outputs = [ "lib" "dev" "doc" "out" ];
  > # ...
  > }
  > ```
> مسیر derivation انبار `/nix/store/<hash>-example.drv` خواهد بود.
> مسیرهای خروجی عبارتند از
> - `/nix/store/<hash>-example-lib`
> - `/nix/store/<hash>-example-dev`
> - `/nix/store/<hash>-example-doc`
> - `/nix/store/<hash>-example`

شما می‌توانید با انتخاب هر خروجی از یک derivation به عنوان یک صفت (attribute)، به آن ارجاع دهید.
نخستین عنصر `outputs`، *خروجی پیش‌فرض* را تعیین می‌کند و در نهایت در سطح بالا قرار می‌گیرد.

> **مثال**
>
> یک خروجی را با نام صفت (attribute) انتخاب کنید:
>
```nix
  > let
  > myPackage = derivation {
  > name = "example";
  > outputs = [ "lib" "dev" "doc" "out" ];
  > # ...
  > };
  > in myPackage.dev
  > ```
>
> از آنجا که `lib` اولین خروجی است، `myPackage` معادل `myPackage.lib` است.

<!-- FIXME: refer to the output attributes when we have one -->

- برای مشاهده صفت‌های اختیاری و کمتر استفاده‌شدهٔ بیشتر، به [صفات پیشرفته](./advanced-attributes.md) مراجعه کنید.

  <!-- FIXME: This should be moved here -->

- هر صفت دیگری به عنوان یک متغیر محیطی به سازنده منتقل می‌شود.
  مقادیر صفت‌ها به شکل زیر به متغیرهای محیطی تبدیل می‌شوند:

    - رشته‌ها بدون تغییر منتقل می‌شوند.

    - اعداد صحیح به نماد اعشاری تبدیل می‌شوند.

    - اعداد اعشاری با دقت از‌پیش‌تعیین‌شده به نماد اعشاری ساده یا علمی تبدیل می‌شوند.

    - یک *مسیر* (مثلاً `../foo/sources.tar`) باعث می‌شود که فایل ارجاع‌داده‌شده به انبار کپی شود؛ مکان آن در انبار در متغیر محیطی قرار می‌گیرد. ایده این است که تمام منابع باید در انبار Nix قرار داشته باشند، زیرا تمام ورودی‌های یک derivation باید در انبار Nix سکونت داشته باشند.

    - یک *derivation* باعث می‌شود که آن derivation پیش از derivation فعلی ساخته شود. متغیر محیطی روی [مسیر انبار] [خروجی](#attr-outputs) پیش‌فرض آن derivation تنظیم می‌شود.

    - فهرست‌های انواع قبلی نیز مجاز هستند. آن‌ها به سادگی و با جداکنندهٔ فاصله به یکدیگر متصل می‌شوند.

    - مقدار `true` به عنوان رشته‌ی `1` منتقل می‌شود و `false` و `null` به عنوان یک رشته‌ی خالی منتقل می‌شوند.

<!-- FIXME: add a section on output attributes -->
