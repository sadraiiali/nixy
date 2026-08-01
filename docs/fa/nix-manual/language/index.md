# زبان Nix

زبان Nix برای ایجاد و ترکیب راحت [درایویشن‌ها](@docroot@/glossary.md#gloss-derivation) طراحی شده‌است، توصیف‌های دقیقی از اینکه چگونه محتویات فایل‌های موجود برای تولید فایل‌های جدید استفاده می‌شوند.

> **نکته**
>
> این صفحات به عنوان مرجع نوشته شده‌اند.
> اگر در حال یادگیری Nix هستید، nix.dev دارای یک [مقدمه خوب بر زبان Nix](https://nix.dev/tutorials/nix-language) است.

این زبان به این صورت است:

- *مخصوص حوزه*

  زبان Nix به طور اختصاصی برای کار با فایل‌های متنی ساخته شده‌است.
  بارزترین ویژگی‌های آن عبارتند از:

  - [مقدمات مسیر سیستم‌فایل](@docroot@/language/types.md#type-path)، برای دسترسی به کدهای منبع
  - [رشته‌های تورفته](@docroot@/language/string-literals.md) و [درون‌گذاری رشته](@docroot@/language/string-interpolation.md)، برای ایجاد محتویات فایل
  - [رشته‌های دارای زمینه‌های متنی](@docroot@/language/string-context.md)، برای پیوند دادن شفاف فایل‌ها

  این زبان دارای [توابع توکار](@docroot@/language/builtins.md) برای یکپارچه‌سازی با [انبار Nix](@docroot@/store/index.md) است که فایل‌ها را مدیریت می‌کند و امکان [تحقق](@docroot@/glossary.md#gloss-realise) درایویشن‌های اعلام‌شده در زبان Nix را فراهم می‌سازد.

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

<table>
 <tr>
  <th>
   مثال
  </th>
  <th>
   توضیحات
  </th>
 </tr>
 <tr>
  <td>

   *مقادیر پایه ([مقدمات](@docroot@/language/types.md#primitives))*

  </td>
  <td>

  </td>
 </tr>
 <tr>
  <td>

   `"hello world"`

  </td>
  <td>

   یک [رشته](@docroot@/language/types.md#type-string)

  </td>
 </tr>
 <tr>
  <td>
```
   ''
     multi
      line
       string
   ''
   ```

</td>
  <td>

   <!-- FIXME: using two no-break spaces, because apparently mdBook swallows the second regular space! -->
   یک رشته‌ی چندخطی. فضای خالی پیشوند مشترک را حذف می‌کند. به `"multi\n line\n  string"` ارزیابی می‌شود.

  </td>
 </tr>
 <tr>
  <td>

   `# Explanation`

  </td>
  <td>

   یک [توضیح](@docroot@/language/syntax.md#comments).

  </td>
 </tr>
 <tr>
  <td>

   `"hello ${ { a = "world"; }.a }"`

   `"1 2 ${toString 3}"`

   `"${pkgs.bash}/bin/sh"`

  </td>
  <td>

   [درون‌گذاری رشته](@docroot@/language/string-interpolation.md) (به `"hello world"`، `"1 2 3"`، `"/nix/store/<hash>-bash-<version>/bin/sh"` گسترش می‌یابد)

  </td>
 </tr>
 <tr>
  <td>

   `true`, `false`

  </td>
  <td>

   [مقادیر بولین](@docroot@/language/types.md#type-bool)

  </td>
 </tr>
 <tr>
  <td>

   `null`

  </td>
  <td>

   مقدار [پوچ (Null)](@docroot@/language/types.md#type-null)

  </td>
 </tr>
 <tr>
  <td>

   `123`

  </td>
  <td>

   یک [عدد صحیح](@docroot@/language/types.md#type-int)

  </td>
 </tr>
 <tr>
  <td>

   `3.141`

  </td>
  <td>

   یک [عدد اعشاری (Floating point number)](@docroot@/language/types.md#type-float)

  </td>
 </tr>
 <tr>
  <td>

   `/etc`

  </td>
  <td>

   یک [مسیر](@docroot@/language/types.md#type-path) مطلق

  </td>
 </tr>
 <tr>
  <td>

   `./foo.png`

  </td>
  <td>

   یک [مسیر](@docroot@/language/types.md#type-path) نسبی نسبت به فایلی که حاوی این عبارت Nix است

  </td>
 </tr>
 <tr>
  <td>

   `~/.config`

  </td>
  <td>

   یک [مسیر](@docroot@/language/types.md#type-path) خانه. به `"<user's home directory>/.config"` ارزیابی می‌شود.

  </td>
 </tr>
 <tr>
  <td>

   `<nixpkgs>`

  </td>
  <td>

   یک [مسیر جستجو](@docroot@/language/constructs/lookup-path.md) برای فایل‌های Nix. مقدار با توجه به [متغیر محیطی `$NIX_PATH`](../command-ref/env-common.md#env-NIX_PATH) تعیین می‌شود.

  </td>
 </tr>
 <tr>
  <td>

   *مقادیر ترکیبی*

  </td>
  <td>

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; }`

  </td>
  <td>

   یک [مجموعه ویژگی](@docroot@/language/types.md#type-attrs) با صفت‌های به نام `x` و `y`

  </td>
 </tr>
 <tr>
  <td>

   `{ foo.bar = 1; }`

  </td>
  <td>

   یک مجموعه تو در تو، معادل `{ foo = { bar = 1; }; }`

  </td>
 </tr>
 <tr>
  <td>

   `rec { x = "foo"; y = x + "bar"; }`

  </td>
  <td>

   یک [مجموعه ویژگی بازگشتی](@docroot@/language/syntax.md#recursive-sets)، معادل `{ x = "foo"; y = "foobar"; }`.

  </td>
 </tr>
 <tr>
  <td>

   `[ "foo" "bar" "baz" ]`

   `[ 1 2 3 ]`

   `[ (f 1) { a = 1; b = 2; } [ "c" ] ]`

  </td>
  <td>

   [فهرست‌ها](@docroot@/language/types.md#type-list) با سه عنصر.

  </td>
 </tr>
 <tr>
  <td>

   *عملگرها*

  </td>
  <td>

  </td>
 </tr>
 <tr>
  <td>

   `"foo" + "bar"`

  </td>
  <td>

   الحاق رشته

  </td>
 </tr>
 <tr>
  <td>

   `1 + 2`

  </td>
  <td>

   جمع اعداد صحیح

  </td>
 </tr>
 <tr>
  <td>

   `"foo" == "f" + "oo"`

  </td>
  <td>

   آزمون برابری (به `true` ارزیابی می‌شود)

  </td>
 </tr>
 <tr>
  <td>

   `"foo" != "bar"`

  </td>
  <td>

   آزمون نابرابری (به `true` ارزیابی می‌شود)

  </td>
 </tr>
 <tr>
  <td>

   `!true`

  </td>
  <td>

   نقیض بولین

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; }.x`

  </td>
  <td>

   [انتخاب صفت](@docroot@/language/types.md#type-attrs) (به `1` ارزیابی می‌شود)

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; }.z or 3`

  </td>
  <td>

   [انتخاب صفت](@docroot@/language/types.md#type-attrs) با مقدار پیش‌فرض (به `3` ارزیابی می‌شود)

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; } // { z = 3; }`

</td>
  <td>

   ادغام دو مجموعه (مجموعه سمت راست اولویت دارد)

  </td>
 </tr>
 <tr>
  <td>

   *ساختارهای کنترلی*

  </td>
  <td>

  </td>
 </tr>
 <tr>
  <td>

   `if 1 + 1 == 2 then "yes!" else "no!"`

  </td>
  <td>

   [عبارت شرطی](@docroot@/language/syntax.md#conditionals).

  </td>
 </tr>
 <tr>
  <td>

   `assert 1 + 1 == 2; "yes!"`

  </td>
  <td>

   بررسی [ادعا (Assertion)](@docroot@/language/syntax.md#assertions) (نتیجه ارزیابی آن `"yes!"` است).

  </td>
 </tr>
 <tr>
  <td>

   `let x = "foo"; y = "bar"; in x + y`

  </td>
  <td>

   تعریف متغیر. [عبارت‌های `let`](@docroot@/language/syntax.md#let-expressions) را ببینید.

  </td>
 </tr>
 <tr>
  <td>

   `with builtins; head [ 1 2 3 ]`

  </td>
  <td>

   افزودن تمام صفات از مجموعه داده‌شده به حوزه (نتیجه ارزیابی آن `1` است).

   برای جزئیات و نکات مربوط به سایه‌اندازی (shadowing)، [عبارت‌های `with`](@docroot@/language/syntax.md#with-expressions) را ببینید.

  </td>
 </tr>
 <tr>
  <td>

   `inherit pkgs src;`

  </td>
  <td>

   متغیرها را به حوزه فعلی (مجموعه ویژگی یا اتصالات `let`) اضافه می‌کند.
   به صورت `pkgs = pkgs; src = src;` بازنویسی می‌شود.
   [به ارث بردن صفات](@docroot@/language/syntax.md#inheriting-attributes) را ببینید.

  </td>
 </tr>
 <tr>
  <td>

   `inherit (pkgs) lib stdenv;`

  </td>
  <td>

   صفات را از مجموعه ویژگی داخل پرانتز به حوزه فعلی (مجموعه ویژگی یا اتصالات `let`) اضافه می‌کند.
   به صورت `lib = pkgs.lib; stdenv = pkgs.stdenv;` بازنویسی می‌شود.
   [به ارث بردن صفات](@docroot@/language/syntax.md#inheriting-attributes) را ببینید.

  </td>
 </tr>
 <tr>
  <td>

   *[تابع‌ها](@docroot@/language/syntax.md#functions) (لامبداها)*

  </td>
  <td>

  </td>
 </tr>
 <tr>
  <td>

   `x: x + 1`

  </td>
  <td>

   یک [تابع](@docroot@/language/syntax.md#functions) که یک عدد صحیح دریافت کرده و آن را یک واحد افزایش‌داده‌شده برمی‌گرداند.

  </td>
 </tr>
 <tr>
  <td>

   `x: y: x + y`

  </td>
  <td>

   [تابع](@docroot@/language/syntax.md#functions) کری‌شده (Curried)، معادل `x: (y: x + y)`. می‌توان از آن مانند تابعی استفاده کرد که دو آرگومان گرفته و مجموع آن‌ها را برمی‌گرداند.

  </td>
 </tr>
 <tr>
  <td>

   `(x: x + 1) 100`

  </td>
  <td>

   یک فراخوانی [تابع](@docroot@/language/syntax.md#functions) (نتیجه ارزیابی آن 101 است)

  </td>
 </tr>
 <tr>
  <td>

   `let inc = x: x + 1; in inc (inc (inc 100))`

  </td>
  <td>

   یک [تابع](@docroot@/language/syntax.md#functions) که به یک متغیر متصل شده و متعاقباً با نام فراخوانی می‌شود (نتیجه ارزیابی آن 103 است)

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y }: x + y`

  </td>
  <td>

   یک [تابع](@docroot@/language/syntax.md#functions) که مجموعه‌ای با صفات الزامی `x` و `y` را انتظار دارد و آن‌ها را به هم الحاق می‌کند

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y ? "bar" }: x + y`

  </td>
  <td>

   یک [تابع](@docroot@/language/syntax.md#functions) که مجموعه‌ای با صفت الزامی `x` و صفت اختیاری `y` را انتظار دارد، و از `"bar"` به عنوان مقدار پیش‌فرض برای `y` استفاده می‌کند

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y, ... }: x + y`

  </td>
  <td>

   یک [تابع](@docroot@/language/syntax.md#functions) که مجموعه‌ای با صفات الزامی `x` و `y` را انتظار دارد و سایر صفات را نادیده می‌گیرد

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y } @ args: x + y`

   `args @ { x, y }: x + y`

  </td>
  <td>

   یک [تابع](@docroot@/language/syntax.md#functions) که مجموعه‌ای با صفات الزامی `x` و `y` را انتظار دارد، و کل مجموعه را به `args` متصل می‌کند

  </td>
 </tr>
 <tr>
  <td>

   *تابع‌های توکار*

  </td>
  <td>

  </td>
 </tr>
 <tr>
  <td>

   `import ./foo.nix`

  </td>
  <td>

بارگذاری و بازگرداندن عبارت Nix در فایل داده‌شده.
   به [import](@docroot@/language/builtins.md#builtins-import) مراجعه کنید.

  </td>
 </tr>
 <tr>
  <td>

   `map (x: x + x) [ 1 2 3 ]`

  </td>
  <td>

   اعمال یک تابع روی هر عنصر از یک فهرست (نتیجه ارزیابی آن `[ 2 4 6 ]` خواهد بود).
   به [`map`](@docroot@/language/builtins.md#builtins-map) مراجعه کنید.

  </td>
 </tr>
</table>
