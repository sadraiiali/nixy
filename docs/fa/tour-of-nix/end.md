# پایان

> درس **۳۵** از ۳۵ · مسیر `end`

## کار به پایان رسید!
تبریک می‌گویم! شما به پایان این دوره رسیدید و موفق شدید!

**امیدواریم از «گشتی در Nix» لذت برده باشید!** اگر می‌خواهید با ما در **تماس** باشید،
لطفاً یک مسئله (issue) در [https://github.com/nixcloud/tour_of_nix](https://github.com/nixcloud/tour_of_nix/issues) ثبت کنید.

## آموزش

یک منبع عالی عبارت است از <https://nixcademy.com/>

## مشاوره

یک منبع عالی عبارت است از <https://nixos.org/community/commercial-support>

## مطالعات بیشتر

* [راهنمای Nixpkgs](https://nixos.org/nixpkgs/manual)

  موضوعاتی از جمله: buildPhases، overrideها و پشتیبانی از زبان‌های برنامه‌نویسی خاص را پوشش می‌دهد.

* [ویکی NixOS](https://nixos.wiki/)

  نمونه‌های کاربردی عملی، مانند [برگه‌ی تقلب (Cheatsheet)](https://nixos.wiki/wiki/Cheatsheet).

* [سایت nix.dev](https://nix.dev/)

  مقدمه‌ای بر nix-shell، فلیک‌ها و جریان‌های کاری.

* [Nix به روایت مثال](https://medium.com/@MrJamesFisher/nix-by-example-a0063a1a4c55)

  درخت‌های تجزیه، ترتیب ارزیابی، انواع داده‌های مرکب، تنبلی، شرطی‌ها، عبارت‌های Let و خیلی موارد دیگر…

* [قرص‌های Nix (nix pills) اثر لوکا برونو (Luca Bruno)](https://lethalman.blogspot.de/2014/07/nix-pill-1-why-you-should-give-it-try.html)

  قرص‌های Nix مقدمه‌ای فوق‌العاده برای برنامه‌نویسی با Nix هستند و از خواندن آن‌ها لذت فراوانی خواهید برد!

## کمک‌های مالی

از حمایت مالی برای میزبانی تور Nix استقبال می‌شود:

 ??PAYPAL??

## مشارکت

از گسترش دادن تور Nix استقبال می‌شود، این یک پروژه متن‌باز است! در <https://github.com/nixcloud/tour_of_nix/issues> مسائل (issues) ایجاد کنید یا فایل questions.json را ویرایش کرده و یک PR بسازید!

### ویرایش دستی
فایل <https://nixcloud.io/tour/questions.json> را بارگیری کرده و آن را در ویرایشگر دلخواه خود باز کنید.

### استفاده از ویرایشگر درون‌خطی

میانبرها:

* `ctrl+,` - مارک‌داون را درون ویرایشگر بارگذاری می‌کند
* `ctrl+.` - کد markdown2html را در سمت راست کامپایل می‌کند

  **توجه:** این کار را دو بار انجام دهید تا ویرایشگر به وضعیت قبلی خود بازگردد!

* `ctrl+i` - ویرایشگر را به محتوای پیش‌فرض بازنشانی می‌کند
* `ctrl+s` - سوالات را در فایل `questions.json` داخل پوشه‌ی `downloads` شما ذخیره می‌کند

اگر می‌خواهید سوالات جدیدی اضافه کنید، از کنسول جاوااسکریپت استفاده کنید.

**هشدار:** میانبر `ctrl+shift+i` در مرورگر کروم کار نمی‌کند، بنابراین برای کلیک راست (RMB) و گزینه‌ی `inspect element` از ماوس استفاده کنید. از طریق همان کنسول جاوااسکریپت می‌توانید شیء `questions` را که در بردارنده تمام سوالات است، گسترش دهید.

**هشدار:** ممکن است بخواهید مدتی با این جریان کاری کار کنید زیرا ممکن است به طور تصادفی مشارکت‌های خود را «بازنویسی» یا «بازنشانی» کنید!

## کد شروع

```nix
with import <nixpkgs> { }; 
rec {
  made_it = "it is done";
}
```

## راه حل

```nix
with import <nixpkgs> { }; 
rec {
  made_it = "it is done";
}
```

## ویدیو

[یوتیوب](https://www.youtube.com/watch?v=qWxGtbeRGhU&list=PLMr2KA8WWojv-4cgqIiVebml0FrMl8N_-)

---

منبع: [گشتی در Nix](https://nixcloud.io/tour/?id=end) · [گیت‌هاب](https://github.com/nixcloud/tour_of_nix)
