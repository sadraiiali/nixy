# شناسه‌ها

یک *شناسه* (identifier) دنباله‌ای از کاراکترهای [ASCII](https://en.wikipedia.org/wiki/ASCII) است که:
- با یک حرف (`a-z`، `A-Z`) یا زیرخط (`_`) آغاز می‌شود
- می‌تواند شامل هر تعداد از موارد زیر باشد:
  - حروف (`a-z`، `A-Z`)
  - ارقام (`0-9`)
  - زیرخط‌ها (`_`)
  - آپاستروف‌ها (`'`)
  - خط تیرهها (`-`)
- جزو [کلمات کلیدی](#keywords) نباشد

> **نحو (Syntax)**
>
> *identifier* ~ `[A-Za-z_][A-Za-z0-9_'-]*`

# نام‌ها

یک *نام* (name) می‌تواند به صورت یک [شناسه](#identifiers) یا یک [رشته‌ی متنی صریح](./string-literals.md) نوشته شود.

> **نحو (Syntax)**
>
> *name* → *identifier* | *string*

نام‌ها در [مجموعه‌های صفت](./syntax.md#attrs-literal)، [اتصال‌های `let`](./syntax.md#let-expressions) و [`inherit`](./syntax.md#inheriting-attributes) استفاده می‌شوند.
دو نام زمانی با هم یکسان هستند که نمایانگر دنبالهٔ یکسانی از کاراکترها باشند، صرف‌نظر از اینکه به صورت شناسه یا رشته نوشته شده باشند.

# کلمات کلیدی

این کلمات کلیدی رزرو شده‌اند و نمی‌توانند به عنوان [شناسه](#identifiers) استفاده شوند:

- [`assert`](./syntax.md#assertions)
- [`else`][if]
- [`if`][if]
- [`in`][let]
- [`inherit`](./syntax.md#inheriting-attributes)
- [`let`][let]
- [`or`](./operators.md#attribute-selection) (به یادداشت مراجعه کنید)
- [`rec`](./syntax.md#recursive-sets)
- [`then`][if]
- [`with`](./syntax.md#with-expressions)

[if]: ./syntax.md#conditionals
[let]: ./syntax.md#let-expressions

> **نکته**
>
> ارزیاب زبان Nix در حال حاضر به دلایل سازگاری با نسخه‌های قبلی، اجازه می‌دهد از `or` به عنوان یک نام در برخی از زمینه‌ها استفاده شود.
> به کاربران توصیه می‌شود که به این ویژگی اتکا نکنند.
>
> مشکلات دیرینه‌ای در نحوه‌ی تجزیه (parsing) کلمه‌ی `or` به عنوان یک نام وجود دارد که بدون ایجاد تغییر ناسازگار (breaking change) در زبان، قابل حل نیستند.
