(contributing-how-to-get-help)=
# نحوه دریافت کمک

اگر برای یکی از مشارکت‌های خود به کمک نیاز دارید، مکان‌های مختلفی وجود دارد که می‌توانید برای دریافت راهنمایی به آن‌ها مراجعه کنید.

## نحوه پیدا کردن نگه‌دارندگان

برای کارایی بهتر و شانس موفقیت بیشتر، باید سعی کنید ابتدا با افراد یا گروه‌هایی که دانش تخصصی‌تری دارند تماس بگیرید:

- اگر مشارکت شما مربوط به بسته‌ای در مجموعهٔ بسته‌های نیکس (Nixpkgs) است، نگه‌دارندگان آن را در صفت [`maintainers`](https://nixos.org/manual/nixpkgs/stable/#var-meta-maintainers) جستجو کنید.
- بررسی کنید که آیا تیم خاصی مسئول زیرسیستم مربوطه هست یا خیر:
  - در [وب‌سایت NixOS](https://nixos.org/community/#governance-teams).
  - در [فهرست تیم‌های نگه‌دارنده مجموعهٔ بسته‌های نیکس (Nixpkgs)](https://github.com/NixOS/nixpkgs/blob/master/maintainers/team-list.nix).
  - در فایل‌های `CODEOWNERS` برای [مجموعهٔ بسته‌های نیکس (Nixpkgs)](https://github.com/NixOS/nixpkgs/blob/master/ci/OWNERS) یا [Nix](https://github.com/NixOS/nix/blob/master/.github/CODEOWNERS).
- خروجی [`git blame`](https://git-scm.com/docs/git-blame) یا [`git log`](https://www.git-scm.com/docs/git-log) را برای فایل‌هایی که به کمک نیاز دارید بررسی کنید.
  آدرس‌های ایمیل افرادی را که کدهای مرتبط را کامیت کرده‌اند، یادداشت کنید.

## از کدام کانال‌های ارتباطی استفاده کنیم

هنگامی که افراد مورد نظر خود را پیدا کردید، می‌توانید از طریق یکی از [پلتفرم‌های ارتباطی جامعهٔ کاربری](https://nixos.org/community) با آن‌ها تماس بگیرید:

- [GitHub](https://github.com/nixos)

  تمام کدهای منبع روی گیت‌هاب نگهداری می‌شوند.
  این مکان مناسبی برای بحث دربارهٔ جزئیات پیاده‌سازی است.

  در نظرات ایشوها (Issues) یا توضیحات پول ریکوئست‌ها (Pull Requests)، [نام کاربری گیت‌هاب](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#mentioning-people-and-teams) موجود در [`فایل maintainers-list.nix`](https://github.com/NixOS/nixpkgs/blob/master/maintainers/maintainer-list.nix) را منشن کنید.

- [Discourse](https://discourse.nixos.org)

  Discourse برای اطلاعیه‌ها، هماهنگی‌ها و سوالات بازپایان استفاده می‌شود.

  برای منشن کردن یا تماس مستقیم با یک کاربر خاص، سعی کنید از نام کاربری گیت‌هاب موجود در [`فایل maintainers-list.nix`][maintainers-list] استفاده کنید.
  توجه داشته باشید که برخی افراد ممکن است نام کاربری متفاوتی در Discourse داشته باشند.

- [Matrix]

  Matrix برای تبادلات زودگذر و به‌موقع و پیام‌های مستقیم استفاده می‌شود.

  برای تماس با یک نگه‌دارنده، از شناسه Matrix آن‌ها که در [`فایل maintainers-list.nix`][maintainers-list] یافت می‌شود، استفاده کنید.
  اگر شناسه Matrix برای نگه‌دارندهٔ خاصی وجود نداشت، سعی کنید نام کاربری گیت‌هاب آن‌ها را جستجو کنید، زیرا اکثر افراد ترجیح می‌دهند از یک نام کاربری ثابت در کانال‌های مختلف استفاده کنند.

  تیم‌های نگه‌دارنده گاهی اوقات اتاق عمومی Matrix خود را دارند.

- ایمیل

  از آدرس‌های ایمیلی که با `git log` پیدا کرده‌اید، استفاده کنید.

- جلسات و رویدادها

  برای رویدادهای زنده یا حضوری، [تقویم رسمی NixOS](https://calendar.google.com/calendar/u/0/embed?src=b9o52fobqjak8oq8lfkhg3t0qg@group.calendar.google.com) و [تقویم جامعهٔ کاربری Discourse](https://discourse.nixos.org/t/community-calendar/18589) را بررسی کنید.
  برخی از تیم‌های جامعهٔ کاربری جلسات منظمی برگزار می‌کنند و یادداشت‌های جلسات خود را منتشر می‌سازند.

## مکان‌های دیگر

اگر کاربر یا گروه خاصی را پیدا نکرده‌اید که بتواند در مشارکت به شما کمک کند، می‌توانید با استفاده از یکی از کانال‌های ارتباطی رسمی زیر، از کل جامعهٔ کاربری سوال بپرسید:

- اتاقی مرتبط با سوال شما در [فضای Matrix مربوط به NixOS][matrix].
- [دسته‌بندی *راهنما* (Help)](https://discourse.nixos.org/c/learn/9) در Discourse.
- اتاق عمومی [`#nix`](https://matrix.to/#/#nix:nixos.org) در Matrix.

[matrix]: https://matrix.to/#/#community:nixos.org
[maintainers-list]: https://github.com/NixOS/nixpkgs/blob/master/maintainers/maintainer-list.nix
