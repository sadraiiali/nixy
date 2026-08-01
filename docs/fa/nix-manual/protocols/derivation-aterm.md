# فرمت فایل درایویشن «ATerm»

به دلایل تاریخی، [درایویشن‌های انبار][store derivation] روی دیسک با فرمت «Annotated Term» (یا به اختصار ATerm) ذخیره می‌شوند
([راهنما](https://homepages.cwi.nl/~daybuild/daily-books/technology/aterm-guide/aterm-guide.html)،
[مقاله](https://doi.org/10.1002/(SICI)1097-024X(200003)30:3%3C259::AID-SPE298%3E3.0.CO;2-Y)).

## فرمت ATerm استفاده‌شده

درایویشن‌ها در یکی از فرمت‌های زیر سریال‌سازی می‌شوند:

-
```
  Derive(...)
  ```

برای تمام درایویشن‌های پایدار.

-
```
  DrvWithVersion(<version-string>, ...)
  ```

تنها `version-string`هایی که امروزه استفاده می‌شوند مربوط به [ویژگی‌های آزمایشی](@docroot@/development/experimental-features.md) هستند:

  - `"xp-dyn-drv"` برای ویژگی آزمایشی [`dynamic-derivations`](@docroot@/development/experimental-features.md#xp-feature-dynamic-derivations).

## استفاده برای کدگذاری به شیء انبار

هنگامی که یک derivation به یک [شیء انبار] کدگذاری می‌شود، ما انتخاب‌های زیر را انجام می‌دهیم:

- [نام] مسیر انبار همان نام derivation به همراه پسوند `.drv` در انتها است.

  در واقع، فرمت ATerm بالا شامل نام derivation *نیست*، با این فرض که یک مسیر انبار نیز به‌طور جانبی (out-of-band) فراهم خواهد شد.

- این derivation با استفاده از ["روش متن" (Text)] از آدرس‌دهی محتواییِ derivationها، بر اساس محتوا آدرس‌دهی می‌شود.

در حال حاضر ما همیشه derivationها را با استفاده از فرمت ATerm (و دو انتخاب قبلی) به شیء انبار کدگذاری می‌کنیم،
اما این حق را برای خود محفوظ می‌داریم که در آینده انواع جدیدی از derivationها را به‌گونه‌ای متفاوت کدگذاری کنیم.

[store derivation]: @docroot@/glossary.md#gloss-store-derivation
[store object]: @docroot@/glossary.md#gloss-store-object
["Text" method]: @docroot@/store/store-object/content-address.md#method-text
