# نام

`nix-collect-garbage` - حذف [اشیاء انبار] غیرقابل‌دسترس

# خلاصه

`nix-collect-garbage` [`--delete-old`] [`-d`] [`--delete-older-than` *period*] [`--max-freed` *bytes*] [`--dry-run`]

# توضیحات

دستور `nix-collect-garbage` عمدتاً یک نام مستعار برای [`nix-store --gc`](@docroot@/command-ref/nix-store/gc.md) است.
به عبارت دیگر، تمام [اشیاء انبار] غیرقابل‌دسترس را در انبار Nix حذف می‌کند تا سیستم شما پاکسازی شود.

با این حال، این دستور دو گزینهٔ اضافی ارائه می‌دهد،
[`--delete-old`](#opt-delete-old) و [`--delete-older-than`](#opt-delete-older-than)،
که [پروفایل]‌های قدیمی را نیز حذف می‌کنند و به طور بالقوه امکان حذف [اشیاء انبار] بیشتری را فراهم می‌کنند، زیرا پروفایل‌ها نیز ریشه‌های جمع‌آوری زباله (garbage collection) هستند.
این گزینه‌ها معادل اجرای
[`nix-env --delete-generations`](@docroot@/command-ref/nix-env/delete-generations.md)
با آرگومان‌های مختلف روی چندین پروفایل،
پیش از اجرای `nix-collect-garbage` (یا صرفاً `nix-store --gc`) بدون هیچ پرچمی است.

> **نکته**
>
> حذف پیکربندی‌های قبلی، بازگردانی (rollback) به آن‌ها را غیرممکن می‌سازد.

این پرچم‌ها باید با احتیاط استفاده شوند، زیرا به طور بالقوه نسل‌های پروفایل‌های مورد استفاده توسط سایر کاربران روی سیستم را حذف می‌کنند.

## مکان‌های جستجو شده برای پروفایل‌ها

دستور `nix-collect-garbage` نمی‌تواند از تمام پروفایل‌ها مطلع باشد؛ آن اطلاعات وجود ندارد.
در عوض، این دستور چند مکان را بررسی می‌کند و روی تمام پروفایل‌هایی که در آنجا می‌یابد عمل می‌کند:

1. مکان‌های پیش‌فرض پروفایل همان‌طور که در بخش [پروفایل]های راهنما مشخص شده‌است.

2. > **نکته**
   >
   > ناپایدار؛ در معرض تغییر
   >
   > به این قابلیت اتکا نکنید؛ این قابلیت صرفاً برای اهداف مهاجرت وجود دارد و ممکن است در آینده تغییر کند.
   > این مسیرهای منسوخ‌شده همچنان جزئیات پیاده‌سازی خصوصی Nix باقی می‌مانند.

   مسیرهای `$NIX_STATE_DIR/profiles` و `$NIX_STATE_DIR/profiles/per-user`.

   به‌جز `$NIX_STATE_DIR/profiles/per-user/root` و `$NIX_STATE_DIR/profiles/default`، این پوشه‌ها دیگر توسط دستورات دیگر استفاده نمی‌شوند.
   دستور `nix-collect-garbage` به هر حال برای پاکسازی پروفایل‌ها از نسخه‌های قدیمی‌تر Nix به آن‌ها نگاهی می‌اندازد.

# گزینه‌ها

این گزینه‌ها برای حذف [پروفایل]‌های قدیمی پیش از حذف [اشیاء انبار] غیرقابل‌دسترس هستند.

- <span id="opt-delete-old">[`--delete-old`](#opt-delete-old)</span> / `-d`

  حذف تمام نسل‌های قدیمی پروفایل‌ها.

  این معادل فراخوانی [`nix-env --delete-generations old`](@docroot@/command-ref/nix-env/delete-generations.md#generations-old) روی هر پروفایل یافت‌شده‌است.

- <span id="opt-delete-older-than">[`--delete-older-than`](#opt-delete-older-than)</span> *period*

  حذف تمام نسل‌های پروفایل‌هایی که قدیمی‌تر از مقدار مشخص‌شده هستند (به‌جز نسل‌هایی که در آن مقطع زمانی فعال بوده‌اند).
  مقدار *period* مقداری مانند `30d` است که به معنای ۳۰ روز خواهد بود.

  این معادل فراخوانی [`nix-env --delete-generations <period>`](@docroot@/command-ref/nix-env/delete-generations.md#generations-time) روی هر پروفایل یافت‌شده‌است.
  برای اطلاعات بیشتر دربارهٔ آرگومان *period*، مستندات آن دستور را مشاهده کنید.

- <span id="opt-max-freed">[`--max-freed`](#opt-max-freed)</span> *bytes*

   <!-- duplication from https://github.com/NixOS/nix/blob/442a2623e48357ff72c77bb11cf2cf06d94d2f90/doc/manual/source/command-ref/nix-store/gc.md?plain=1#L39-L44 -->

  به حذف مسیرها ادامه بده تا زمانی که حداقل *bytes* بایت حذف شود،
  سپس متوقف شو. آرگومان *bytes* می‌تواند با پسوند ضرب‌کنندهٔ
  `K`، `M`، `G` یا `T` دنبال شود که نشان‌دهندهٔ واحدهای KiB، MiB، GiB یا TiB است.

{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# نمونه

برای حذف کردن تمام چیزهایی از انبار Nix که توسط نسل‌های فعلی هر پروفایل استفاده نمی‌شوند، دستور زیر را اجرا کنید:

```console
$ nix-collect-garbage -d
```

[profiles]: @docroot@/command-ref/files/profiles.md
[store objects]: @docroot@/store/store-object.md
