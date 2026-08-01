# سؤالات متداول

## ریشه نام Nix چیست؟

> نام *Nix* از واژه هلندی *niks* به معنای *هیچ* گرفته شده است؛
> اقدامات ساخت هیچ‌چیز را که به‌طور صریح به عنوان ورودی اعلام نشده باشد، نمی‌بینند.
>
> — <cite>[Nix: A Safe and Policy-Free System for Software Deployment](https://edolstra.github.io/pubs/nspfssd-lisa2004-final.pdf), LISA XVIII, 2004</cite>

لوگوی Nix از [ایده‌ای برای لوگوی Haskell](https://wiki.haskell.org/File:Sgf-logo-blue.png) و این حقیقت که [*nix* در زبان لاتین به معنای *برف* است](https://nix-dev.science.uu.narkive.com/VDaaP1BY/nix-logo) الهام گرفته شده است.

## فلیک‌ها (Flakes) چیستند؟

به [flakes-definition](/pages/nix-dev/concepts/flakes) مراجعه کنید.

## <a id="channel-branches"></a> از کدام شاخه کانال باید استفاده کنم؟

مجموعه‌ی بسته‌های نیکس (Nixpkgs) و NixOS دارای نسخه‌های پایدار و غلتان (rolling) هستند.

این نسخه‌ها در گونه‌هایی به نام «شاخه‌های کانال» توزیع می‌شوند:
شاخه‌های Git که برای انتشارها استفاده می‌شوند و همچنین به کانال‌های Nix تبدیل می‌شوند.

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> برای اطلاعات بیشتر درباره کانال‌ها به ورودی [`nix-channel`](/pages/nix-manual/command-ref/nix-channel) در راهنمای Nix و برای استراتژی انشعاب‌گیری Nixpkgs به [راهنمای مشارکت در Nixpkgs](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md#branch-conventions) مراجعه کنید.

### پایدار

نسخه‌های پایدار به‌منظور رفع باگ‌ها یا آسیب‌پذیری‌های امنیتی به‌روزرسانی‌های محافظه‌کارانه‌ای دریافت می‌کنند؛ در غیر این صورت نسخه‌های بسته تغییر نمی‌کنند.
یک نسخه پایدار جدید هر شش ماه یک‌بار عرضه می‌شود.

- در لینوکس (از جمله NixOS و WSL)، از [`nixos-*`](https://github.com/NixOS/nixpkgs/branches/all?query=nixos-) استفاده کنید.

  این شاخه‌ها به کامیت‌هایی اشاره می‌کنند که در آن‌ها بیشتر بسته‌های لینوکس پیش‌ساخته شده‌اند و می‌توان آن‌ها را از کش باینری دریافت کرد.
  علاوه بر این، این کامیت‌ها مجموعه تست کامل NixOS را با موفقیت پشت سر گذاشته‌اند.

- در macOS/Darwin، از [`nixpkgs-*-darwin`](https://github.com/NixOS/nixpkgs/branches/all?query=nixpkgs-) استفاده کنید.

  این شاخه‌ها به کامیت‌هایی اشاره می‌کنند که در آن‌ها بیشتر بسته‌های Darwin پیش‌ساخته شده‌اند و می‌توان آن‌ها را از کش باینری دریافت کرد.

- در هر پلتفرم دیگری، استفاده از هر یک از موارد فوق تفاوتی ایجاد نمی‌کند.

  Hydra هیچ باینری‌ای را برای پلتفرم‌های دیگر پیش‌ساخته نمی‌کند.

تمام این «شاخه‌های کانال» از شاخه مربوط به [`release-*`](https://github.com/NixOS/nixpkgs/branches/all?query=release-) پیروی می‌کنند.

> <span class="admonition-kind" data-kind="admonition"></span>
>
> **مثال**
>
> `nixos-23.05` و `nixpkgs-23.05-darwin` هر دو بر اساس `release-23.05` ساخته شده‌اند.

### غلتان (Rolling)

نسخه‌های غلتان از [`master`](https://github.com/NixOS/nixpkgs/branches/all?query=master)، شاخه اصلی توسعه، پیروی می‌کنند.

- در لینوکس (از جمله NixOS و WSL)، از [`nixos-unstable`](https://github.com/NixOS/nixpkgs/branches/all?query=nixos-unstable) استفاده کنید.
- در هر پلتفرم دیگری، از [`nixpkgs-unstable`](https://github.com/NixOS/nixpkgs/branches/all?query=nixpkgs-unstable) استفاده کنید.

شاخه‌های کانال [`*-small`](https://github.com/NixOS/nixpkgs/branches/all?query=-small) مجموعه‌تست کوچک‌تری را پشت سر گذاشته‌اند، به این معنا که نسبت به شاخه‌ی پایه خود به‌روزتر هستند، اما تضمین‌های پایداری کمتری ارائه می‌دهند.

## آیا ناخالصی‌ای در ساخت‌های ایزوله شده (Sandboxed) باقی مانده است؟

بله. موارد زیر وجود دارند:

- معماری CPU: تلاش زیادی می‌شود تا از کامپایل دستورات بومی به نفع دستورات پشتیبانی‌شدهٔ از‌پیش‌تعیین‌شده جلوگیری شود.
- زمان/تاریخ فعلی سیستم.
- سیستم‌فایل مورد استفاده برای ساخت (نیز ببینید: [`TMPDIR`](/pages/nix-manual/command-ref/env-common#env-TMPDIR)).
- پارامترهای هسته لینوکس، از جمله:
  - [قابلیت‌های IPv6](https://github.com/NixOS/nix/issues/5615).
  - مفسرهای binfmt، برای مثال آنهایی که با [`boot.binfmt.emulatedSystems`](https://search.nixos.org/options?show=boot.binfmt.emulatedSystems) پیکربندی شده‌اند.
- رفتار زمانی سیستم ساخت، یک ساخت موازی Make ممکن است در برخی موارد ورودی‌های درستی دریافت نکند.
- درج مقادیر تصادفی، برای مثال از `/dev/random` یا `/dev/urandom`.
- تفاوت‌های بین نسخه‌های Nix. برای نمونه، یک نسخه جدید Nix ممکن است یک متغیر محیطی جدید معرفی کند. Nix تضمین نمی‌کند که دستوری مانند `env > $out` در آینده منجر به خروجی یکسانی شود.
