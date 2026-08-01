# 5. زبان Nix

زبان Nix برای ایجاد و ترکیب راحت [درایویشن‌ها](/pages/nix-manual/glossary#gloss-derivation) طراحی شده است – توصیف‌های دقیقی از اینکه چگونه محتویات فایل‌های موجود برای تولید فایل‌های جدید استفاده می‌شوند.

> **نکته**
>
> این صفحات به عنوان مرجع نوشته شده‌اند.
> اگر در حال یادگیری Nix هستید، nix.dev دارای یک [مقدمه خوب بر زبان Nix](https://nix.dev/tutorials/nix-language) است.

این زبان به این صورت است:

- *مخصوص حوزه*

  زبان Nix به طور اختصاصی برای کار با فایل‌های متنی ساخته شده است.
  بارزترین ویژگی‌های آن عبارتند از:

  - [مقدمات مسیر سیستم‌فایل](/pages/nix-manual/language/types#type-path)، برای دسترسی به کدهای منبع
  - [رشته‌های تورفته](/pages/nix-manual/language/string-literals) و [درون‌گذاری رشته](/pages/nix-manual/language/string-interpolation)، برای ایجاد محتویات فایل
  - [رشته‌های دارای زمینه‌های متنی](/pages/nix-manual/language/string-context)، برای پیوند دادن شفاف فایل‌ها

  این زبان دارای [توابع توکار](/pages/nix-manual/language/builtins) برای یکپارچه‌سازی با [انبار Nix](/pages/nix-manual/store) است که فایل‌ها را مدیریت می‌کند و امکان [تحقق](/pages/nix-manual/glossary#gloss-realise) درایویشن‌های اعلام‌شده در زبان Nix را فراهم می‌سازد.

- *اعلانی (declarative)*

  هیچ مفهومی به نام اجرای مراحل ترتیبی وجود ندارد.
  وابستگی‌ها بین عملیات فقط از طریق داده‌ها برقرار می‌شوند.

- *خالص (pure)*

  مقادیر نمی‌توانند در طول محاسبات تغییر کنند.
  اگر ورودی تابع تغییر نکند، توابع همیشه خروجی یکسانی تولید می‌کنند.

- *تابعی (functional)*

  توابع درست مانند هر مقدار دیگری هستند.
  توابع را می‌توان به نام‌ها اختصاص داد، به عنوان آرگومان دریافت کرد، یا توسط توابع بازگرداند.

- *تنبل (lazy)*

  مقادیر تنها زمانی محاسبه می‌شوند که به آن‌ها نیاز باشد.

- *با نوع‌بندی پویا*

  خطاهای نوع تنها زمانی شناسایی می‌شوند که عبارت‌ها ارزیابی شوند.

# نمای کلی

این یک نمای کلی و ناقص از ویژگی‌های زبان، به همراه مثال است.

&lt;table&gt;
 &lt;tr&gt;
  &lt;th&gt;
   مثال
  &lt;/th&gt;
  &lt;th&gt;
   توضیحات
  &lt;/th&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   *مقادیر پایه ([مقدمات](/pages/nix-manual/language/types#primitives))*

  &lt;/td&gt;
  &lt;td&gt;

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `"hello world"`

  &lt;/td&gt;
  &lt;td&gt;

   یک [رشته](/pages/nix-manual/language/types#type-string)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;
```
   ''
     multi
      line
       string
   ''
   ```

&lt;/td&gt;
  &lt;td&gt;

   
   یک رشته‌ی چندخطی. فضای خالی پیشوند مشترک را حذف می‌کند. به `"multi\n line\n  string"` ارزیابی می‌شود.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `# Explanation`

  &lt;/td&gt;
  &lt;td&gt;

   یک [توضیح](/pages/nix-manual/language/syntax#comments).

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `"hello ${'{'}'{'{'}'{'}'} {'{'}'{'{'}'{'}'} a = "world"; {'{'}'{'}'}'{'}'}.a {'{'}'{'}'}'{'}'}"`

   `"1 2 ${'{'}'{'{'}'{'}'}toString 3{'{'}'{'}'}'{'}'}"`

   `"${'{'}'{'{'}'{'}'}pkgs.bash{'{'}'{'}'}'{'}'}/bin/sh"`

  &lt;/td&gt;
  &lt;td&gt;

   [درون‌گذاری رشته](/pages/nix-manual/language/string-interpolation) (به `"hello world"`، `"1 2 3"`، `"/nix/store/&lt;hash&gt;-bash-&lt;version&gt;/bin/sh"` گسترش می‌یابد)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `true`, `false`

  &lt;/td&gt;
  &lt;td&gt;

   [مقادیر بولین](/pages/nix-manual/language/types#type-bool)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `null`

  &lt;/td&gt;
  &lt;td&gt;

   مقدار [پوچ (Null)](/pages/nix-manual/language/types#type-null)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `123`

  &lt;/td&gt;
  &lt;td&gt;

   یک [عدد صحیح](/pages/nix-manual/language/types#type-int)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `3.141`

  &lt;/td&gt;
  &lt;td&gt;

   یک [عدد اعشاری (Floating point number)](/pages/nix-manual/language/types#type-float)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `/etc`

  &lt;/td&gt;
  &lt;td&gt;

   یک [مسیر](/pages/nix-manual/language/types#type-path) مطلق

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `./foo.png`

  &lt;/td&gt;
  &lt;td&gt;

   یک [مسیر](/pages/nix-manual/language/types#type-path) نسبی نسبت به فایلی که حاوی این عبارت Nix است

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `~/.config`

  &lt;/td&gt;
  &lt;td&gt;

   یک [مسیر](/pages/nix-manual/language/types#type-path) خانه. به `"&lt;user's home directory&gt;/.config"` ارزیابی می‌شود.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `&lt;nixpkgs&gt;`

  &lt;/td&gt;
  &lt;td&gt;

   یک [مسیر جستجو](/pages/nix-manual/language/constructs/lookup-path) برای فایل‌های Nix. مقدار با توجه به [متغیر محیطی `$NIX_PATH`](/pages/nix-manual/command-ref/env-common#env-NIX_PATH) تعیین می‌شود.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   *مقادیر ترکیبی*

  &lt;/td&gt;
  &lt;td&gt;

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x = 1; y = 2; {'{'}'{'}'}'{'}'}`

  &lt;/td&gt;
  &lt;td&gt;

   یک [مجموعه ویژگی](/pages/nix-manual/language/types#type-attrs) با صفت‌های به نام `x` و `y`

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} foo.bar = 1; {'{'}'{'}'}'{'}'}`

  &lt;/td&gt;
  &lt;td&gt;

   یک مجموعه تو در تو، معادل `{'{'}'{'{'}'{'}'} foo = {'{'}'{'{'}'{'}'} bar = 1; {'{'}'{'}'}'{'}'}; {'{'}'{'}'}'{'}'}`

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `rec {'{'}'{'{'}'{'}'} x = "foo"; y = x + "bar"; {'{'}'{'}'}'{'}'}`

  &lt;/td&gt;
  &lt;td&gt;

   یک [مجموعه ویژگی بازگشتی](/pages/nix-manual/language/syntax#recursive-sets)، معادل `{'{'}'{'{'}'{'}'} x = "foo"; y = "foobar"; {'{'}'{'}'}'{'}'}`.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `[ "foo" "bar" "baz" ]`

   `[ 1 2 3 ]`

   `[ (f 1) {'{'}'{'{'}'{'}'} a = 1; b = 2; {'{'}'{'}'}'{'}'} [ "c" ] ]`

  &lt;/td&gt;
  &lt;td&gt;

   [فهرست‌ها](/pages/nix-manual/language/types#type-list) با سه عنصر.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   *عملگرها*

  &lt;/td&gt;
  &lt;td&gt;

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `"foo" + "bar"`

  &lt;/td&gt;
  &lt;td&gt;

   الحاق رشته

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `1 + 2`

  &lt;/td&gt;
  &lt;td&gt;

   جمع اعداد صحیح

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `"foo" == "f" + "oo"`

  &lt;/td&gt;
  &lt;td&gt;

   آزمون برابری (به `true` ارزیابی می‌شود)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `"foo" != "bar"`

  &lt;/td&gt;
  &lt;td&gt;

   آزمون نابرابری (به `true` ارزیابی می‌شود)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `!true`

  &lt;/td&gt;
  &lt;td&gt;

   نقیض بولین

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x = 1; y = 2; {'{'}'{'}'}'{'}'}.x`

  &lt;/td&gt;
  &lt;td&gt;

   [انتخاب صفت](/pages/nix-manual/language/types#type-attrs) (به `1` ارزیابی می‌شود)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x = 1; y = 2; {'{'}'{'}'}'{'}'}.z or 3`

  &lt;/td&gt;
  &lt;td&gt;

   [انتخاب صفت](/pages/nix-manual/language/types#type-attrs) با مقدار پیش‌فرض (به `3` ارزیابی می‌شود)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x = 1; y = 2; {'{'}'{'}'}'{'}'} // {'{'}'{'{'}'{'}'} z = 3; {'{'}'{'}'}'{'}'}`

&lt;/td&gt;
  &lt;td&gt;

   ادغام دو مجموعه (مجموعه سمت راست اولویت دارد)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   *ساختارهای کنترلی*

  &lt;/td&gt;
  &lt;td&gt;

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `if 1 + 1 == 2 then "yes!" else "no!"`

  &lt;/td&gt;
  &lt;td&gt;

   [عبارت شرطی](/pages/nix-manual/language/syntax#conditionals).

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `assert 1 + 1 == 2; "yes!"`

  &lt;/td&gt;
  &lt;td&gt;

   بررسی [ادعا (Assertion)](/pages/nix-manual/language/syntax#assertions) (نتیجه ارزیابی آن `"yes!"` است).

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `let x = "foo"; y = "bar"; in x + y`

  &lt;/td&gt;
  &lt;td&gt;

   تعریف متغیر. [عبارت‌های `let`](/pages/nix-manual/language/syntax#let-expressions) را ببینید.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `with builtins; head [ 1 2 3 ]`

  &lt;/td&gt;
  &lt;td&gt;

   افزودن تمام صفات از مجموعه داده‌شده به حوزه (نتیجه ارزیابی آن `1` است).

   برای جزئیات و نکات مربوط به سایه‌اندازی (shadowing)، [عبارت‌های `with`](/pages/nix-manual/language/syntax#with-expressions) را ببینید.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `inherit pkgs src;`

  &lt;/td&gt;
  &lt;td&gt;

   متغیرها را به حوزه فعلی (مجموعه ویژگی یا اتصالات `let`) اضافه می‌کند.
   به صورت `pkgs = pkgs; src = src;` بازنویسی می‌شود.
   [به ارث بردن صفات](/pages/nix-manual/language/syntax#inheriting-attributes) را ببینید.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `inherit (pkgs) lib stdenv;`

  &lt;/td&gt;
  &lt;td&gt;

   صفات را از مجموعه ویژگی داخل پرانتز به حوزه فعلی (مجموعه ویژگی یا اتصالات `let`) اضافه می‌کند.
   به صورت `lib = pkgs.lib; stdenv = pkgs.stdenv;` بازنویسی می‌شود.
   [به ارث بردن صفات](/pages/nix-manual/language/syntax#inheriting-attributes) را ببینید.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   *[تابع‌ها](/pages/nix-manual/language/syntax#functions) (لامبداها)*

  &lt;/td&gt;
  &lt;td&gt;

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `x: x + 1`

  &lt;/td&gt;
  &lt;td&gt;

   یک [تابع](/pages/nix-manual/language/syntax#functions) که یک عدد صحیح دریافت کرده و آن را یک واحد افزایش‌داده‌شده برمی‌گرداند.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `x: y: x + y`

  &lt;/td&gt;
  &lt;td&gt;

   [تابع](/pages/nix-manual/language/syntax#functions) کری‌شده (Curried)، معادل `x: (y: x + y)`. می‌توان از آن مانند تابعی استفاده کرد که دو آرگومان گرفته و مجموع آن‌ها را برمی‌گرداند.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `(x: x + 1) 100`

  &lt;/td&gt;
  &lt;td&gt;

   یک فراخوانی [تابع](/pages/nix-manual/language/syntax#functions) (نتیجه ارزیابی آن 101 است)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `let inc = x: x + 1; in inc (inc (inc 100))`

  &lt;/td&gt;
  &lt;td&gt;

   یک [تابع](/pages/nix-manual/language/syntax#functions) که به یک متغیر متصل شده و متعاقباً با نام فراخوانی می‌شود (نتیجه ارزیابی آن 103 است)

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x, y {'{'}'{'}'}'{'}'}: x + y`

  &lt;/td&gt;
  &lt;td&gt;

   یک [تابع](/pages/nix-manual/language/syntax#functions) که مجموعه‌ای با صفات الزامی `x` و `y` را انتظار دارد و آن‌ها را به هم الحاق می‌کند

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x, y ? "bar" {'{'}'{'}'}'{'}'}: x + y`

  &lt;/td&gt;
  &lt;td&gt;

   یک [تابع](/pages/nix-manual/language/syntax#functions) که مجموعه‌ای با صفت الزامی `x` و صفت اختیاری `y` را انتظار دارد، و از `"bar"` به عنوان مقدار پیش‌فرض برای `y` استفاده می‌کند

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x, y, ... {'{'}'{'}'}'{'}'}: x + y`

  &lt;/td&gt;
  &lt;td&gt;

   یک [تابع](/pages/nix-manual/language/syntax#functions) که مجموعه‌ای با صفات الزامی `x` و `y` را انتظار دارد و سایر صفات را نادیده می‌گیرد

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `{'{'}'{'{'}'{'}'} x, y {'{'}'{'}'}'{'}'} @ args: x + y`

   `args @ {'{'}'{'{'}'{'}'} x, y {'{'}'{'}'}'{'}'}: x + y`

  &lt;/td&gt;
  &lt;td&gt;

   یک [تابع](/pages/nix-manual/language/syntax#functions) که مجموعه‌ای با صفات الزامی `x` و `y` را انتظار دارد، و کل مجموعه را به `args` متصل می‌کند

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   *تابع‌های توکار*

  &lt;/td&gt;
  &lt;td&gt;

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `import ./foo.nix`

  &lt;/td&gt;
  &lt;td&gt;

بارگذاری و بازگرداندن عبارت Nix در فایل داده‌شده.
   به [import](/pages/nix-manual/language/builtins#builtins-import) مراجعه کنید.

  &lt;/td&gt;
 &lt;/tr&gt;
 &lt;tr&gt;
  &lt;td&gt;

   `map (x: x + x) [ 1 2 3 ]`

  &lt;/td&gt;
  &lt;td&gt;

   اعمال یک تابع روی هر عنصر از یک فهرست (نتیجه ارزیابی آن `[ 2 4 6 ]` خواهد بود).
   به [`map`](/pages/nix-manual/language/builtins#builtins-map) مراجعه کنید.

  &lt;/td&gt;
 &lt;/tr&gt;
&lt;/table&gt;
