# مشارکت

## افزودن یادداشت انتشار

پوشه `doc/manual/rl-next` حاوی ورودی‌های یادداشت انتشار برای تمام تغییرات منتشرنشده است.

تغییرات قابل‌مشاهده برای کاربر باید همراه با یک یادداشت انتشار ارائه شوند.

### افزودن یک ورودی

در اینجا نمونه‌ای از یک ورودی کامل آورده شده است. نام فایل در سند ادغام نمی‌شود.

```
---
synopsis: Basically a title
issues: 1234
prs: 1238
---

Here's one or more paragraphs that describe the change.

- It's markdown
- Add references to the manual using [links like this](@_at_docroot@/example.md)
```
<!-- برای خوانندگان متن خام: یعنی استفاده از @docroot@ -->

تغییرات مهم باید هدر زیر را اضافه کنند تا به بالا منتقل شوند.

```
significance: significant
```

<!-- Keep an eye on https://codeberg.org/fgaz/changelog-d/issues/1 -->
همچنین می‌توانید [مستندات قالب](https://github.com/haskell/cabal/blob/master/CONTRIBUTING.md#changelog) را مطالعه کنید.

### فرآیند ساخت

نسخه‌ها دارای یک فایل `rl-MAJOR.MINOR.md` از‌پیش‌محاسبه‌شده هستند و فاقد فایل `rl-next.md` می‌باشند.

## شاخه‌ها

- [`master`](https://github.com/NixOS/nix/commits/master)

  شاخه اصلی توسعه. تمام تغییرات در این شاخه تایید و ادغام می‌شوند.
  هنگام توسعه یک تغییر، شاخه‌ای را بر اساس آخرین نسخه `master` ایجاد کنید.

  نگه‌دارندگان تلاش می‌کنند تا آن را [در وضعیتی آماده برای انتشار نگه دارند](#reverting).

- [`maintenance-*.*`](https://github.com/NixOS/nix/branches/all?query=maintenance)

  این شاخه‌ها صرفاً موضوع انتقال‌های معکوس (backports) هستند و آن‌ها نیز [در وضعیتی](#reverting) آماده برای انتشار نگهداری می‌شوند.

  به [`maintainers/backporting.md`](https://github.com/NixOS/nix/blob/master/maintainers/backporting.md) مراجعه کنید.

- [`latest-release`](https://github.com/NixOS/nix/tree/latest-release)

  آخرین نسخه پچ از آخرین نسخه فرعی.

  به [`maintainers/release-process.md`](https://github.com/NixOS/nix/blob/master/maintainers/release-process.md) مراجعه کنید.

- [`backport-*-to-*`](https://github.com/NixOS/nix/branches/all?query=backport)

  به‌طور کلی شاخه‌هایی که توسط اکشن انتقال معکوس ایجاد شده‌اند.

  به [`maintainers/backporting.md`](https://github.com/NixOS/nix/blob/master/maintainers/backporting.md) مراجعه کنید.

- [_سایر_](https://github.com/NixOS/nix/branches/all)

  شاخه‌هایی که با الگوهای فوق مطابقت ندارند باید شاخه‌های ویژگی (feature branches) باشند.

## بازگردانی

اگر مشخص شود که تغییری به اشتباه ادغام شده است یا حاوی یک رگرسیون (regression) است، ممکن است بازگردانی شود.
بازگردانی به معنای رد کردن مشارکت نیست، بلکه صرفاً بخشی از یک فرآیند توسعه مؤثر است.
این کار تضمین می‌کند که توسعه با روان‌ترین شکل ممکن، حداقل میزان ابهام و سربار کمتر ادامه یابد.
اگر نگه‌دارندگان مجبور باشند بیش از حد نگران جلوگیری از بازگردانی‌ها باشند، نمی‌توانند به همان میزان تغییرات را ادغام کنند.
با پذیرش بازگردانی‌ها به عنوان بخش مثبتی از فرآیند توسعه، همه برنده می‌شوند.

با این حال، عقب‌نشینی ممکن است ناامیدکننده باشد، بنابراین نگه‌دارندگان در تلاش بعدی حمایت ویژه‌ای از شما خواهند کرد.
