# توکارها

این بخش مقادیر و توابع توکار موجود در ارزیاب زبان Nix را فهرست می‌کند.
تمام توکارها از طریق ثابت سراسری [`builtins`](#builtins-builtins) در دسترس هستند.

برخی از توکارها همچنین مستقیماً در محدوده سراسری قرار دارند:

- [`derivation`](#builtins-derivation)
- `derivationStrict`
- [`abort`](#builtins-abort)
- [`baseNameOf`](#builtins-baseNameOf)
- [`break`](#builtins-break)
- [`dirOf`](#builtins-dirOf)
- [`false`](#builtins-false)
- [`fetchGit`](#builtins-fetchGit)
- `fetchMercurial`
- [`fetchTarball`](#builtins-fetchTarball)
- [`fetchTree`](#builtins-fetchTree)
- [`fromTOML`](#builtins-fromTOML)
- [`import`](#builtins-import)
- [`isNull`](#builtins-isNull)
- [`map`](#builtins-map)
- [`null`](#builtins-null)
- [`placeholder`](#builtins-placeholder)
- [`removeAttrs`](#builtins-removeAttrs)
- [`scopedImport`](#builtins-scopedImport)
- [`throw`](#builtins-throw)
- [`toString`](#builtins-toString)
- [`true`](#builtins-true)

<!-- This tip (use `lib` instead) is a "layer violation", but serves an important social role. -->

> **نکته**
>
> **آیا باید از `builtins` استفاده کنم یا `lib`؟**
>
> توکارها به گونه‌ای طراحی شده‌اند که یک رابط پایدار باشند که عبارت‌ها بتوانند در طول زمان به آن‌ها وابسته باشند،
> به‌طوری‌که مثلاً نسخه‌های قدیمی Nixpkgs به ارزیابی بازتولیدپذیر خود ادامه دهند.
>
> در مقابل، این یعنی آن‌ها برخی عادات خاص را انباشته کرده‌اند که Nix قادر به تغییرشان نیست،
> اما کتابخانه‌ای مثل کتابخانه Nixpkgs (`lib`) *می‌تواند* آن رفتارها را بهبود ببخشد، جایگزین کند یا منسوخ اعلام نماید،
> زیرا کدهای منبع آن در مواردی که بازتولیدپذیری اهمیت دارد، سنجاق می‌شوند.
>
> بنابراین، اگرچه استفاده مستقیم از `builtins` اشتباه نیست،
> مثلاً در پروژه‌های کوچک مستقل از Nixpkgs،
> اما استفاده از کتابخانه‌ای مانند `lib` به عنوان منبع اصلی توابع، تجربه بهتری را برای شما رقم خواهد زد،
> زیرا توابع مسئله‌دار را پنهان می‌کند، بقیه را اصلاح می‌کند،
> و به شما کمک می‌کند تا کدهای خود را با استفاده از انقضاهای آتی (که همچنان به اندازه کافی نادر هستند) بهبود ببخشید.

<dl>
  <dt id="builtins-derivation"><a href="#builtins-derivation"><code>derivation <var>attrs</var></code></a></dt>
  <dd><p><var>derivation</var> در
         <a href="derivations.md">بخش مخصوص خودش</a> شرح داده شده است.</p></dd>
