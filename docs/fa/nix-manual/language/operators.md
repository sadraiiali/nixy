# عملگرها

| نام | نحو | وابستگی جهتی | اولویت |
|----------------------------------------|--------------------------------------------|---------------|------------|
| [انتخاب صفت (Attribute selection)] | *attrset* `.` *attrpath* \[ `or` *expr* \] | هیچ‌کدام | ۱ |
| [فراخوانی تابع (Function application)] | *func* *expr* | چپ‌گرا | ۲ |
| [منفی‌سازی ریاضی (Arithmetic negation)][arithmetic] | `-` *number* | هیچ‌کدام | ۳ |
| [بررسی وجود صفت (Has attribute)] | *attrset* `?` *attrpath* | هیچ‌کدام | ۴ |
| الحاق لیست | *list* `++` *list* | راست‌گرا | ۵ |
| [ضرب (Multiplication)][arithmetic] | *number* `*` *number* | چپ‌گرا | ۶ |
| [تقسیم (Division)][arithmetic] | *number* `/` *number* | چپ‌گرا | ۶ |
| [تفریق (Subtraction)][arithmetic] | *number* `-` *number* | چپ‌گرا | ۷ |
| [جمع (Addition)][arithmetic] | *number* `+` *number* | چپ‌گرا | ۷ |
| [الحاق رشته (String concatenation)] | *string* `+` *string* | چپ‌گرا | ۷ |
| [الحاق مسیر (Path concatenation)] | *path* `+` *path* | چپ‌گرا | ۷ |
| [الحاق مسیر و رشته] | *path* `+` *string* | چپ‌گرا | ۷ |
| [الحاق رشته و مسیر] | *string* `+` *path* | چپ‌گرا | ۷ |
| نفی منطقی (`NOT`) | `!` *bool* | هیچ‌کدام | ۸ |
| [به‌روزرسانی (Update)] | *attrset* `//` *attrset* | راست‌گرا | ۹ |
| [کوچک‌تر از (Less than)][Comparison] | *expr* `<` *expr* | هیچ‌کدام | ۱۰ |
| [کوچک‌تر یا مساوی (Less than or equal to)][Comparison] | *expr* `<=` *expr* | هیچ‌کدام | ۱۰ |
| [بزرگ‌تر از (Greater than)][Comparison] | *expr* `>` *expr* | هیچ‌کدام | ۱۰ |
| [بزرگ‌تر یا مساوی (Greater than or equal to)][Comparison] | *expr* `>=` *expr* | هیچ‌کدام | ۱۰ |
| [برابری (Equality)] | *expr* `==` *expr* | هیچ‌کدام | ۱۱ |
| نابرابری | *expr* `!=` *expr* | هیچ‌کدام | ۱۱ |
| [عطف منطقی (Logical conjunction)] (`AND`) | *bool* `&&` *bool* | چپ‌گرا | [۱۲](#precedence-and-disjunctive-normal-form) |
| [فصل منطقی (Logical disjunction)] (`OR`) | *bool* <code>\|\|</code> *bool* | چپ‌گرا | [۱۳](#precedence-and-disjunctive-normal-form) |
| [استلزام منطقی (Logical implication)] | *bool* `->` *bool* | راست‌گرا | ۱۴ |
| [عملگر پایپ (Pipe operator)] (آزمایشی) | *expr* `\|>` *func* | چپ‌گرا | ۱۵ |
| [عملگر پایپ (Pipe operator)] (آزمایشی) | *func* `<\|` *expr* | راست‌گرا | ۱۵ |

[string]: ./types.md#type-string
[path]: ./types.md#type-path
[number]: ./types.md#type-float
[list]: ./types.md#type-list
[attribute set]: ./types.md#type-attrs

<!-- TODO(@rhendric, #10970): ^ rationalize number -> int/float -->

## انتخاب صفت

> **نحو (Syntax)**
>
> *attrset* `.` *attrpath* \[ `or` *expr* \]

صفت مشخص‌شده توسط مسیر صفت *attrpath* را از [مجموعه ویژگی] *attrset* انتخاب کنید.
اگر صفت وجود نداشته باشد، در صورت ارائه‌شدن *expr* پس از `or`، آن را برمی‌گرداند؛ در غیر این صورت، ارزیابی متوقف می‌شود.

[Attribute selection]: #attribute-selection

## فراخوانی تابع

> **نحو (Syntax)**
>
> *func* *expr*

مقدار قابل‌فراخوانی *func* را روی آرگومان *expr* اعمال کنید. به عدم وجود هرگونه علامت عملگر مشهود توجه کنید.
یک مقدار قابل‌فراخوانی یکی از موارد زیر است:
- یک [تابع تعریف‌شده توسط کاربر][function]
- یک تابع [توکار][builtins]
- یک مجموعه ویژگی دارای [صفت `__functor`](./syntax.md#attr-__functor)

> **هشدار**
>
> آیتم‌های [فهرست][list] نیز با فاصله از یکدیگر جدا می‌شوند، به این معنی که فراخوانی‌های تابع در آیتم‌های فهرست باید داخل پرانتز قرار گیرند.

## بررسی وجود صفت

> **نحو (Syntax)**
>
> *attrset* `?` *attrpath*

بررسی کنید که آیا [مجموعه ویژگی] *attrset* حاوی صفت مشخص‌شده توسط *attrpath* است یا خیر.
نتیجه یک مقدار [بولی (Boolean)][Boolean] است.

همچنین ببینید: [`builtins.hasAttr`](@docroot@/language/builtins.md#builtins-hasAttr)

[Boolean]: ./types.md#type-bool

[Has attribute]: #has-attribute

پس از ارزیابی *attrset* و *attrpath*، پیچیدگی محاسباتی برای *n* صفت در *attrset* برابر با O(log(*n*)) است.

## محاسبات ریاضی

اعداد نوع خود را حفظ خواهند کرد مگر اینکه با انواع عددی دیگر ترکیب شوند:
عملیات مختص اعداد صحیح همیشه اعداد صحیح بازمی‌گردانند، در حالی که هر عملیاتی که شامل حداقل یک عدد اعشاری باشد، یک عدد اعشاری بازمی‌گرداند.

ارزیابی عملیات عددی زیر باعث بروز خطای ارزیابی می‌شود:
- تقسیم بر صفر
- سرریز عدد صحیح، یعنی هر عملیاتی که نتیجه‌ای خارج از محدوده قابل‌نمایش [اعداد صحیح زبان Nix](./syntax.md#number-literal) تولید کند.

همچنین ببینید [مقایسه (Comparison)][Comparison] و [برابری (Equality)][Equality].

عملگر `+` سربارگذاری شده‌است تا روی رشته‌ها و مسیرها نیز کار کند.

[arithmetic]: #arithmetic

## الحاق رشته

> **نحو (Syntax)**
>
> *string* `+` *string*

دو [رشته][string] را به هم متصل کرده و [زمینه‌های رشته‌ای](./string-context.md) آن‌ها را ادغام کنید.

[String concatenation]: #string-concتامين

## الحاق مسیر

> **نحو (Syntax)**
>
> *path* `+` *path*

دو [مسیر][path] را به هم متصل کنید.
نتیجه یک مسیر است.

[Path concatenation]: #path-concatenation

## الحاق مسیر و رشته

> **نحو (Syntax)**
>
> *path* + *string*

*[مسیر]* را به *[رشته]* متصل کنید.
نتیجه یک مسیر است.

> **نکته**
>
> رشته نباید دارای [زمینه رشته‌ای](./string-context.md) باشد که به یک [مسیر انبار] ارجاع دهد.

[Path and string concatenation]: #path-and-string-concatenation

## الحاق رشته و مسیر

> **نحو (Syntax)**
>
> *string* + *path*

*[رشته]* را به *[مسیر]* متصل کنید.
نتیجه یک رشته‌است.

> **مهم**
>
> فایل یا پوشه موجود در *path* باید وجود داشته باشد و در [انبار] کپی شود.
> مسیر به عنوان [مسیر انبار] مربوطه در نتیجه ظاهر می‌شود.

[store path]: @docroot@/store/store-path.md
[store]: @docroot@/glossary.md#gloss-store

[String and path concatenation]: #string-and-path-concatenation

## به‌روزرسانی (Update)

> **نحو (Syntax)**
>
> *attrset1* // *attrset2*

[مجموعه ویژگی] *attrset1* را با نام‌ها و مقادیر حاصل از *attrset2* به‌روزرسانی کنید.

مجموعه ویژگی بازگشتی بازگردانده‌شده شامل تمام صفات موجود در *attrset1* و *attrset2* خواهد بود.
اگر نام صفتی در هر دو وجود داشته باشد، مقدار صفت از دومی گرفته می‌شود.

این عملگر در هر دو *attrset1* و *attrset2* [سخت‌گیرانه (strict)](@docroot@/language/evaluation.md#strictness) است.
این بدان معناست که هر دو آرگومان به [فرم نرمال سر ضعیف (weak head normal form)](@docroot@/language/evaluation.md#values) ارزیابی می‌شوند، بنابراین خود مجموعه‌های ویژگی ارزیابی می‌شوند، اما مقادیر صفات آن‌ها ارزیابی نمی‌شوند.

[Update]: #update

## مقایسه

مقایسه به صورت زیر انجام می‌شود:

- [حسابی][arithmetic] برای [اعداد][number]
- لغت‌نامه‌ای برای [رشته‌ها][string] و [مسیرها][path]
- لغت‌نامه‌ای آیتم‌به‌آیتم برای [فهرست‌ها][list]:
  عنصرهای واقع در یک اینдекс در هر دو فهرست بر اساس نوعشان مقایسه شده و اگر برابر باشند، از آن‌ها صرف‌نظر می‌شود.

تمام عملگرهای مقایسه بر اساس `<` پیاده‌سازی شده‌اند و هم‌ارزی‌های زیر برقرار است:

| مقایسه | پیاده‌سازی |
|-------------|-----------------------|
| *a* `<=` *b* | `! (` *b* `<` *a* `)` |
| *a* `>`  *b* | *b* `<` *a* |
| *a* `>=` *b* | `! (` *a* `<` *b* `)` |

[Comparison]: #comparison

## برابری

- [مجموعه‌های ویژگی][attribute set] ابتدا بر اساس نام صفات و سپس بر اساس آیتم‌ها تا زمان یافتن اختلاف مقایسه می‌شوند.
- [فهرست‌ها][list] ابتدا بر اساس طول و سپس بر اساس آیتم‌ها تا زمان یافتن اختلاف مقایسه می‌شوند.
- مقایسه [توابع][function] متمایز مقدار `false` را برمی‌گرداند، اما توابع یکسان ممکن است مشمول [بهینه‌سازی همانی مقدار](#value-identity-optimization) شوند.
- اعداد از نظر نوع سازگار هستند، به عملگرهای [حسابی][arithmetic] مراجعه کنید.
- اعداد اعشاری فقط تا یک دقت محدود با هم تفاوت دارند.

عملگر `==` در هر دو آرگومان [سخت‌گیرانه (strict)](@docroot@/language/evaluation.md#strictness) است؛ هنگام مقایسه انواع مرکب ([مجموعه‌های ویژگی][attribute set] و [فهرست‌ها][list])، در مقادیر درون آن‌ها به طور جزئی سخت‌گیرانه است: آن‌ها تا زمان یافتن اختلاف ارزیابی می‌شوند. <!-- این بخش به‌شدت ناقص توصیف شده و بر اینکه کدام عبارت‌ها به درستی ارزیابی شوند تأثیر می‌گذارد؛ و صرفاً مربوط به «ترتیب» یا پیام‌های خطا نیست. -->

### بهینه‌سازی همانی مقدار

نیکس مقایسه‌های برابری مقادیر تو در تو را از طریق برابری اشاره‌گر یا به شکلی انتزاعی‌تر، یعنی _همانی_ (identity) انجام می‌دهد.
معناشناسی نیکس در حالت ایده‌آل هویت منحصربه‌فردی را به مقادیر به هنگام ایجاد اختصاص نمی‌دهد، اما برابری از این قاعده مستثنی است.
مزیت قابل بحث این کار کارایی بالاتر آن است و به ساختارهای حلقوی اجازه می‌دهد مقایسه شوند؛ به عنوان مثال، عبارت `let x = { x = x; }; in x == x` به `true` ارزیابی می‌شود.
با این حال، در نتیجه‌ی این امر، هنگام انجام مقایسه در یک فهرست یا مجموعه ویژگی، تابع با خودش برابر می‌شود، که در تضاد با یک مقایسه مستقیم ساده است.

[function]: ./syntax.md#functions

[Equality]: #equality

## عطف منطقی

> **نحو (Syntax)**
>
> *bool1* `&&` *bool2*

AND منطقی. معادل `if` *bool1* `then` *bool2* `else false`.

این عملگر در *bool1* [سخت‌گیرانه (strict)](@docroot@/language/evaluation.md#strictness) است، اما *bool2* را تنها در صورتی ارزیابی می‌کند که *bool1* برابر با `true` باشد.

> **مثال**
>
```nix
> true && false
> => false
>
> false && throw "never evaluated"
> => false
> ```

[Logical conjunction]: #logical-conjunction

## فصل منطقی (Logical disjunction)

> **نحو**
>
> *bool1* `||` *bool2*

عملگر OR منطقی. معادل `if` *bool1* `then true` `else` *bool2* است.

این عملگر روی *bool1* [سخت‌گیرانه](@docroot@/language/evaluation.md#strictness) (strict) عمل می‌کند، اما *bool2* را تنها در صورتی ارزیابی می‌کند که مقدار *bool1* برابر با `false` باشد.

> **مثال**
>
```nix
> true || false
> => true
>
> true || throw "never evaluated"
> => true
> ```

[Logical disjunction]: #logical-disjunction

### اولویت و فرم نرمال فصل

اولویت عملگرهای `&&` و `||` با فرم نرمال فصل (disjunctive normal form) مطابقت دارد.
بدون پرانتز، یک عبارت چندین «وضعیت مجاز» (که با `||` به هم متصل شده‌اند) را توصیف می‌کند، که در آن هر وضعیت شامل چندین شرط هم‌زمان (که با `&&` به هم متصل شده‌اند) است.

برای مثال، عبارت `A || B && C || D && E` به شکل `A || (B && C) || (D && E)` تجزیه (parse) می‌شود که سه وضعیت مجاز را توصیف می‌کند: A برقرار است، یا هم‌زمان B و C برقرارند، یا هم‌زمان D و E برقرارند.

## استلزام منطقی

> **نحو (Syntax)**
>
> *bool1* `->` *bool2*

استلزام منطقی. معادل است با `!`*bool1* `||` *bool2* (یا `if` *bool1* `then` *bool2* `else true`).

این عملگر نسبت به *bool1* [سخت‌گیرانه](@docroot@/language/evaluation.md#strictness) (strict) است، اما *bool2* را تنها در صورتی ارزیابی می‌کند که *bool1* برابر با `true` باشد.

> **مثال**
>
```nix
> true -> false
> => false
>
> false -> throw "never evaluated"
> => true
> ```

[تکلیف منطقی]: #logical-implication

## عملگرهای خط لوله

- *a* `|>` *b* معادل است با *b* *a*
- *a* `<|` *b* معادل است با *a* *b*

> **مثال**
>
> ```
> nix-repl> 1 |> builtins.add 2 |> builtins.mul 3
> 9
>
> nix-repl> builtins.add 1 <| builtins.mul 2 <| 3
> 7
> ```

> **هشدار**
>
> این سینتکس بخشی از یک [ویژگی آزمایشی](@docroot@/development/experimental-features.md) است و ممکن است در نسخه‌های آتی تغییر کند.
>
> برای استفاده از این سینتکس، مطمئن شوید که [ویژگی آزمایشی `pipe-operators`](@docroot@/development/experimental-features.md#xp-feature-pipe-operators) فعال است.
> برای مثال، مورد زیر را در [`nix.conf`](@docroot@/command-ref/conf-file.md) لحاظ کنید:
>
> ```
> extra-experimental-features = pipe-operators
> ```

[عملگر خط عمودی (Pipe operator)]: #pipe-operators
[توابع داخلی (builtins)]: ./builtins.md
[فراخوانی تابع (Function application)]: #function-application
