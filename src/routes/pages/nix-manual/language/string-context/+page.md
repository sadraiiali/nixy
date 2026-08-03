# 5.1.1. محتوای رشته

> **نکته**
>
> این یک مبحث پیشرفته است.
> زبان Nix به گونه‌ای طراحی شده است که بدون نیاز به اینکه برنامه نویس آگاهانه با زمینه رشته‌ها سر و کار داشته باشد یا حتی بداند آن‌ها چیستند، مورد استفاده قرار گیرد.

یک رشته در زبان Nix صرفاً دنباله‌ای از کاراکترها مانند رشته‌ها در سایر زبان‌ها نیست.
بلکه در واقع زوجی از یک دنباله از کاراکترها و یک *زمینه رشته* (string context) است.
زمینه رشته یک مجموعه (بدون ترتیب) از *عناصر زمینه رشته* است.

هدف از زمینه‌های رشته، جمع‌آوری مقادیر غیررشته‌ای متصل‌شده به رشته‌ها از طریق
[الحاق رشته](/pages/nix-manual/language/operators#string-concatenation)،
[درون‌گذاری رشته](/pages/nix-manual/language/string-interpolation)،
و عملیات‌های مشابه است.
ایده این است که کاربر می‌تواند هنگام ایجاد فایل‌های متنی از طریق عبارت‌های Nix، بدون پیگیری دستی مسیرهای دقیق، به فایل‌های دیگر ارجاع دهد.
Nix تضمین خواهد کرد که تمام فایل‌های ارجاع‌شده قابل دسترسی باشند - یعنی تمام [مسیرهای انبار](/pages/nix-manual/glossary#gloss-store-path) [معتبر](/pages/nix-manual/glossary#gloss-validity) باشند.

> **نکته**
>
> زمینه‌های رشته در کد به سبک متعارف (idiomatic) زبان Nix به‌طور صریح دستکاری *نمی‌شوند*.

عناصر زمینه رشته به شکل‌های مختلفی وجود دارند:

- [مسیر اشتقاق‌پذیر]<a id="string-context-element-derived-path"></a>

  یک عنصر زمینه رشته از این نوع، یک [مسیر اشتقاق‌پذیر](/pages/nix-manual/glossary#gloss-deriving-path) است.
  آن‌ها می‌توانند از نوع [ثابت](#string-context-constant) یا [خروجی](#string-context-output) باشند که با انواع مسیرهای اشتقاق‌پذیر مطابقت دارند.

  - [عناصر زمینه رشته ثابت]<a id="string-context-constant"></a>

    > **مثال**
    >
    > [`builtins.storePath`] یک رشته با یک عنصر زمینه رشته ثابت منفرد ایجاد می‌کند:
    >

> ```nix
> builtins.getContext (builtins.storePath "/nix/store/ikwkxz4wwlp2g1428n7dy729cg1d9hin-hello-2.10")
> ```
> ارزیابی می‌شود به
>

> ```nix
> {
>   "/nix/store/ikwkxz4wwlp2g1428n7dy729cg1d9hin-hello-2.10" = {
>     path = true;
>   };
> }
> ```

[deriving path]: /pages/nix-manual/glossary#gloss-deriving-path
    [store path]: glossary.md#gloss-store-path
    [`builtins.storePath`]: ./builtins.md#builtins-storePath

  - [عناصر زمینه رشته‌ای خروجی]<a id="string-context-output"></a>

    > **مثال**
    >
    > رفتار زمینه‌های رشته‌ای به بهترین شکل با یک تابع توکار که همچنان آزمایشی است نشان داده می‌شود: [`builtins.outputOf`].
    > این مثال با نسخه پایدار Nix کار *نخواهد* کرد!
    >

> ```nix
> builtins.getContext
>   (builtins.outputOf
>     (builtins.storePath "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv")
>     "out")
> ```
> ارزیابی می‌شود به
>

> ```nix
> {
>   "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv" = {
>     outputs = [ "out" ];
>   };
> }
> ```

[`builtins.outputOf`]: /pages/nix-manual/language/builtins#builtins-outputOf
- [*derivation deep*]<a id="string-context-element-derivation-deep"></a>

  مفهوم *derivation deep* یک ویژگی پیشرفته است که برای استفاده با [`exportReferencesGraph` derivation attribute](/pages/nix-manual/language/advanced-attributes#adv-attr-exportReferencesGraph) در نظر گرفته شده است.
  یک عنصر زمینه رشته‌ای *derivation deep* یک مسیر derivation است و هم به خروجی‌های آن و هم به کل کلوژر ساخت (build closure) آن derivation اشاره دارد:
  تمام خروجی‌های آن، تمام derivationهای دیگری که derivation داده‌شده به آن‌ها وابسته است، و تمام خروجی‌های آن‌ها.

  > **مثال**
  >
  > بهترین راه برای نشان دادن زمینه‌های رشته‌ای *derivation deep* استفاده از [`builtins.addDrvOutputDependencies`] است.
  > یک عنصر زمینه رشته‌ای ثابت معمولی را که به یک derivation اشاره می‌کند در نظر بگیرید، و آن را به یک عنصر زمینه رشته‌ای «Derivation deep» تبدیل کنید.
  >

> ```nix
> builtins.getContext
>   (builtins.addDrvOutputDependencies
>     (builtins.storePath "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv"))
> ```
> ارزیابی می‌شود به
>

> ```nix
> {
>   "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv" = {
>     allOutputs = true;
>   };
> }
> ```

[`builtins.addDrvOutputDependencies`]: /pages/nix-manual/language/builtins#builtins-addDrvOutputDependencies
  [`builtins.unsafeDiscardOutputDependency`]: ./builtins.md#builtins-unsafeDiscardOutputDependency

## بررسی زمینه‌های رشته (string contexts)

به‌طور کلی، [`builtins.hasContext`] مشخص می‌کند که آیا یک رشته دارای زمینه غیرخالی است یا خیر.

هنگامی که به اطلاعات با دانه‌بندی ریزتر نیاز باشد، می‌توان از [`builtins.getContext`] استفاده کرد.
این تابع یک [مجموعه صفت] نماینده زمینه رشته ایجاد می‌کند که می‌توان آن را طبق روال عادی بررسی کرد.

[`builtins.hasContext`]: /pages/nix-manual/language/builtins#builtins-hasContext
[`builtins.getContext`]: /pages/nix-manual/language/builtins#builtins-getContext
[attribute set]: /pages/nix-manual/language/types#type-attrs
## پاکسازی زمینه‌های رشته

[`builtins.unsafeDiscardStringContext`](/pages/nix-manual/language/builtins#builtins-unsafeDiscardStringContext) کپی‌ای از یک رشته، اما با زمینه رشته‌ی خالی ایجاد می‌کند.
رشته بازگردانده‌شده را می‌توان به راه‌های بیشتری استفاده کرد؛ مثلاً توسط عملگرهایی که نیازمند خالی بودن زمینه رشته هستند.
لزوم پاک کردن صریح زمینه رشته در چنین مواردی کمک می‌کند تا اطمینان حاصل شود که عناصر زمینه رشته به‌اشتباه از دست نمی‌روند.
نشانگر «ناامن» (unsafe) تنها برای یادآوری این موضوع است که Nix به‌طور معمول تضمین می‌کند که وابستگی‌ها ردیابی می‌شوند، در حالی که رشته بازگردانده‌شده آن‌ها را از دست داده است.

## ساخت زمینه‌های رشته

[`builtins.appendContext`] کپی‌ای از یک رشته، اما با عناصر زمینه رشته‌ی اضافی ایجاد می‌کند.
زمینه به‌طور صریح توسط یک [مجموعه صفت] در قالبی که [`builtins.getContext`] تولید می‌کند، مشخص می‌شود.
یک رشته با زمینه‌های دلخواه را می‌توان به این شکل ساخت:

1. ایجاد یک رشته با عناصر زمینه رشته‌ی دلخواه.
   (محتویات رشته اهمیتی ندارند.)
2. استخراج زمینه آن با [`builtins.getContext`].
3. ترکیب آن با یک رشته پایه و فراخوانی‌های مکرر [`builtins.appendContext`].

[`builtins.appendContext`]: /pages/nix-manual/language/builtins#builtins-appendContext
