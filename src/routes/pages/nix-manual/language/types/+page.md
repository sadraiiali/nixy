# 5.1. انواع داده

هر مقدار در زبان Nix دارای یکی از انواع زیر است:

* [عدد صحیح](#type-int)
* [اعشاری](#type-float)
* [بولین](#type-bool)
* [رشته](#type-string)
* [مسیر](#type-path)
* [نال (Null)](#type-null)
* [مجموعه ویژگی](#type-attrs)
* [فهرست](#type-list)
* [تابع](#type-function)
* [خارجی](#type-external)

## مقادیر اولیه (Primitives)

### <a id="type-int"></a> عدد صحیح

یک _عدد صحیح_ (Integer) در زبان Nix یک عدد صحیح علامت‌دار ۶۴ بیتی است.

اعداد صحیح نامنفی را می‌توان به عنوان [مقالید عدد صحیح](/pages/nix-manual/language/syntax#number-literal) بیان کرد.
اعداد صحیح منفی با استفاده از [عملگر منفی‌سازی حسابی](/pages/nix-manual/language/operators#arithmetic) ایجاد می‌شوند.
تابع [`builtins.isInt`](/pages/nix-manual/language/builtins#builtins-isInt) را می‌توان برای تشخیص اینکه آیا یک مقدار عدد صحیح است یا خیر، استفاده کرد.

### <a id="type-float"></a> اعشاری

یک عدد _اعشاری_ (Float) در زبان Nix یک عدد اعشاری ۶۴ بیتی بر اساس استاندارد [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) است.

بیشتر اعداد اعشاری نامنفی را می‌توان به عنوان [مقالید اعشاری](/pages/nix-manual/language/syntax#number-literal) بیان کرد.
اعداد اعشاری منفی با استفاده از [عملگر منفی‌سازی حسابی](/pages/nix-manual/language/operators#arithmetic) ایجاد می‌شوند.
تابع [`builtins.isFloat`](/pages/nix-manual/language/builtins#builtins-isFloat) را می‌توان برای تشخیص اینکه آیا یک مقدار اعشاری است یا خیر، استفاده کرد.

### <a id="type-bool"></a> بولین

یک مقدار _بولین_ (Boolean) در زبان Nix یکی از مقادیر _true_ (درست) یا _false_ (نادرست) است.

این مقادیر به عنوان صفاتی از [`builtins`](/pages/nix-manual/language/builtins#builtins-builtins) به صورت [`builtins.true`](/pages/nix-manual/language/builtins#builtins-true) و [`builtins.false`](/pages/nix-manual/language/builtins#builtins-false) در دسترس هستند.
تابع [`builtins.isBool`](/pages/nix-manual/language/builtins#builtins-isBool) را می‌توان برای تشخیص اینکه آیا یک مقدار بولین است یا خیر، استفاده کرد.

### <a id="type-string"></a> رشته

یک _رشته_ (String) در زبان Nix دنباله‌ای تغییرناپذیر و با طول محدود از بایت‌ها به همراه یک [زمینه رشته](/pages/nix-manual/language/string-context) است.
Nix فرض یا پشتیبانی ذاتی برای کار با انکودینگ‌های کاراکتری ندارد.

مقادیر رشته‌ای بدون زمینه رشته را می‌توان به عنوان [مقالید رشته‌ای](/pages/nix-manual/language/string-literals) بیان کرد.
تابع [`builtins.isString`](/pages/nix-manual/language/builtins#builtins-isString) را می‌توان برای تشخیص اینکه آیا یک مقدار رشته است یا خیر، استفاده کرد.

### <a id="type-path"></a> مسیر

یک _مسیر_ (Path) در زبان Nix دنباله‌ای تغییرناپذیر و با طول محدود از بایت‌ها است که با `/` شروع می‌شود و نشان‌دهنده یک مسیر سیستم‌فایل متعارف به سبک POSIX است.
مقادیر مسیر با مقادیر رشته‌ای متفاوت هستند، حتی اگر حاوی دنباله بایت‌های یکسانی باشند.
عملیاتی که مسیرها را تولید می‌کنند، نتیجه را درست مانند تابع استاندارد C یعنی [`realpath`] ساده‌سازی می‌کنند، با این تفاوت که هیچ‌گونه تفکیک پیوند نمادینی (symbolic link resolution) انجام نمی‌شود.

[`realpath`]: https://pubs.opengroup.org/onlinepubs/9699919799/functions/realpath.html

مسیرها برای ارجاع به فایل‌های محلی مناسب هستند و اغلب بر رشته‌ها ترجیح داده می‌شوند.
- مقادیر مسیر شامل اسلش‌های پایانی یا تکراری، `.` یا `..` نیستند.
- مقادیر مسیر نسبی به طور خودکار نسبت به [پوشه پایه] خود حل می‌شوند.
- ابزارها می‌توانند مقادیر مسیر را تشخیص داده و قابلیت‌های اضافی مانند تکمیل خودکار (autocompletion)، خودکارسازی بازسازی کد (refactoring automation) و پرش به فایل (jump-to-file) را فراهم کنند.

[base directory]: /pages/nix-manual/glossary#gloss-base-directory
برای معتبر بودن یک مقدار مسیر، نیازی نیست که فایلی در آن مسیرِ مشخص وجود داشته باشد، اما مسیری که با استفاده از [درون‌گذاری رشته] یا [الحاق رشته و مسیر] به یک رشته تبدیل می‌شود، باید به یک فایل یا پوشه قابل‌خواندن اشاره کند که در انبار نیکس کپی خواهد شد.
برای نمونه، ارزیابی `"${'{'}./foo.txt{'}'}"` باعث می‌شود که فایل `foo.txt` از همان پوشه در انبار نیکس کپی شود و نتیجه‌ی آن رشته‌ی `"/nix/store/&lt;hash&gt;-foo.txt"` باشد.
عملیات‌هایی مانند [`import`] نیز می‌توانند انتظار داشته باشند که یک مسیر به یک فایل یا پوشه قابل‌خواندن ارجاع دهد.

[درون‌گذاری رشته]: /pages/nix-manual/language/string-interpolation#interpolated-expression
[الحاق رشته و مسیر]: /pages/nix-manual/language/operators#string-and-path-concatenation
[`import`]: /pages/nix-manual/language/builtins#builtins-import
> **نکته**
>
> زبان Nix فرض می‌کند که تمام فایل‌های ورودی هنگام ارزیابی یک عبارت نیکس _بدون تغییر_ باقی می‌مانند.
> برای نمونه، فرض کنید در طول یک نشست `nix repl` از یک مسیر فایل در یک رشته‌ی درون‌گذاری‌شده استفاده کرده‌اید.
> بعداً در همان نشست، پس از تغییر محتوای فایل، ارزیابی مجدد رشته‌ی درون‌گذاری‌شده با همان مسیر فایل ممکن است یک [مسیر انبار] جدید برنگرداند، زیرا ممکن است Nix محتوای فایل را مجدداً نخواند.
> در صورت نیاز، از `:r` برای بازنشانی repl استفاده کنید.

[مسیر انبار]: /pages/nix-manual/store/store-path
مقادیر مسیر را می‌توان به صورت [لیترال‌های مسیر](/pages/nix-manual/language/syntax#path-literal) بیان کرد.
تابع [`builtins.isPath`](/pages/nix-manual/language/builtins#builtins-isPath) را می‌توان برای تشخیص اینکه آیا یک مقدار از نوع مسیر است یا خیر، به کار برد.

### <a id="type-null"></a> تهی (Null)

تنها یک مقدار از نوع _تهی_ در زبان Nix وجود دارد.

این مقدار به عنوان یک صفت در مجموعه ویژگی [`builtins`](/pages/nix-manual/language/builtins#builtins-builtins) با نام [`builtins.null`](/pages/nix-manual/language/builtins#builtins-null) در دسترس است.

## مقادیر مرکب

### <a id="type-attrs"></a> مجموعه ویژگی

یک مجموعه ویژگی را می‌توان با یک [لیترال مجموعه ویژگی](/pages/nix-manual/language/syntax#attrs-literal) ساخت.
تابع [`builtins.isAttrs`](/pages/nix-manual/language/builtins#builtins-isAttrs) را می‌توان برای تشخیص اینکه آیا یک مقدار مجموعه ویژگی است یا خیر، به کار برد.

### <a id="type-list"></a> فهرست

یک فهرست را می‌توان با یک [لیترال فهرست](/pages/nix-manual/language/syntax#list-literal) ساخت.
تابع [`builtins.isList`](/pages/nix-manual/language/builtins#builtins-isList) را می‌توان برای تشخیص اینکه آیا یک مقدار فهرست است یا خیر، به کار برد.

## <a id="type-function"></a> تابع

یک تابع را می‌توان با یک [عبارت تابع](/pages/nix-manual/language/syntax#functions) ساخت.
تابع [`builtins.isFunction`](/pages/nix-manual/language/builtins#builtins-isFunction) را می‌توان برای تشخیص اینکه آیا یک مقدار تابع است یا خیر، به کار برد.

## <a id="type-external"></a> خارجی

یک مقدار _خارجی_، مقداری کدر (opaque) است که توسط یک [افزونه‌ی](/pages/nix-manual/command-ref/conf-file#conf-plugin-files) Nix ایجاد شده است.
چنین مقداری را می‌توان در عبارت‌های نیکس جایگزین کرد، اما ایجاد و استفاده از آن صرفاً توسط کد افزونه انجام می‌شود.
