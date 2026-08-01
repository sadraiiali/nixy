# <a id="flakes-definition"></a> فلیک‌ها

## فلیک‌ها چیستند؟

فلیک‌ها یک فایل ورودی به نام `flake.nix` ارائه می‌دهند که هدف آن اشتراک‌گذاری کد نیکس است.
آن‌ها ساخت برنامه‌ها را با نسخهٔ یکسان آسان می‌کنند.

فایل `flake.nix` فایلی است که ورودی‌ها و خروجی‌ها را با یک [ساختار استاندارد] اعلام می‌کند.

> نکته: [آزمایشی (Experimental)]، و به [Nix 2.4] نیاز دارد.

این فایل می‌تواند به شکل زیر باشد:

```nix
{
  description = "My example flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux = {
      default = self.packages.x86_64-linux.hello;
      hello = nixpkgs.legacyPackages.x86_64-linux.hello;
    };
  };
}
```

[`outputs`] شامل [built-in types] مختلفی است، اما می‌توان آن را [extended] کرد.
نمای کلی آن‌ها را می‌توانید در [wiki] بیابید.

[`inputs`] به شما امکان می‌دهد وابستگی‌ها را اعلام کنید.

هنگامی که یک [`nix` command] را اجرا می‌کنید، نیکس یک [`flake.lock`] برای سنجاق کردن Nixpkgs ایجاد می‌کند تا وابستگی‌ها ثابت شوند.

اگر این وابستگی‌ها دارای [`inputs`] مخصوص به خود باشند، نیکس فایل‌های قفل _آن‌ها_ را بررسی می‌کند تا نسخه‌های قابل‌استفاده را پیدا کند.
استفاده از نسخه‌های یکسان کمک می‌کند اطمینان حاصل شود که برنامه‌ها مطابق انتظار کار می‌کنند، اما می‌توانید این موارد را بازنویسی کنید.

[`nix` command]ها به طور پیش‌فرض به‌صورت بومی با فلیک‌ها یکپارچه می‌شوند.

```bash
nix build github:NixOS/nixpkgs#hello
```

شما می‌توانید [references] را به پوشه‌های پروژه محلی (مثلاً `.`) یا راه دور (مثلاً `github:NixOS/nixpkgs`) ارسال کنید.
برای جزئیات بیشتر، به راهنمای مربوط به [`nix` command]ها مراجعه کنید.

نام‌های مستعارِ فلیک‌ها در یک [registry] ذخیره می‌شوند.
این مورد را می‌توان از طریق [command-line] یا گزینهٔ [`nix.registry`] در NixOS گسترش داد.

[^subset]: فلیک‌ها به‌طور پیش‌فرض در حالت خالص (pure) اجرا می‌شوند و ساخت‌ها را از محیط هاست ایزوله می‌کنند.
این پدیده ارزیابی هرمتیک نیز نامیده می‌شود و از ارزیابی توابع [impure] (غیر شبکه‌ای) جلوگیری می‌کند.
فیلدهای `inputs` و فراداده (metadata) در فلیک نمی‌توانند عبارت‌های دلخواه Nix باشند.
هدف از این کار جلوگیری از محاسبات پیچیده و احتمالاً پایان‌ناپذیر است.
پارامتر تابع در فیلد `outputs` باید مشخص شود: این فیلد از [eta-reduction] پشتیبانی نمی‌کند.

راهنمای NixOS در ادامه [flake-based installs] را بیشتر توضیح می‌دهد.

[Experimental]: /pages/nix-manual/development/experimental-features#xp-feature-flakes
[Nix 2.4]: https://nix.dev/manual/nix/stable/release-notes/rl-2.4.html#highlights
[standard structure]: /pages/nix-manual/command-ref/experimental-commands#flake-format
[`nix` command]: /pages/nix-manual/command-ref/experimental-commands
[references]: /pages/nix-manual/command-ref/experimental-commands#flake-references
[`outputs`]: https://wiki.nixos.org/wiki/Flakes#Output_schema
[built-in types]: https://github.com/NixOS/nix/blob/38c755f168b7c38cd4687aacf5d7e59f049658d3/src/nix/flake.cc#L594-L769
[extended]: https://github.com/NixOS/nix/blob/38c755f168b7c38cd4687aacf5d7e59f049658d3/src/nix/flake.cc#L772-L776
[wiki]: https://wiki.nixos.org/wiki/Flakes#Output_schema
[`inputs`]: /pages/nix-manual/command-ref/experimental-commands#flake-inputs
[`flake.lock`]: /pages/nix-manual/command-ref/experimental-commands#lock-files
[impurities]: /pages/nix-manual/language#impurities
[registry]: https://github.com/NixOS/flake-registry
[command-line]: /pages/nix-manual/command-ref/experimental-commands
[`nix.registry`]: https://search.nixos.org/options?channel=unstable&show=nix.registry&query=registry
[eta-reduction]: https://wiki.haskell.org/Eta_conversion
[flake-based installs]: https://nixos.org/manual/nixos/stable/#sec-installation-manual-installing

## آیا باید در پروژه‌ام از فلیک‌ها استفاده کنم؟

فلیک‌ها یک فرمت توسعهٔ تجربی با مسائل حل‌نشده هستند.
عملکرد آن‌ها را به‌طور کلی می‌توان بدون استفاده از خود آن‌ها نیز به دست آورد.

اگر نیاز به اجرای نرم‌افزار موجودی دارید که از قبل از فلیک‌ها استفاده می‌کرده است، یا می‌خواهید در توسعهٔ آن‌ها مشارکت کنید، با خیال راحت از آن‌ها استفاده کنید.
اگر می‌خواهید خودتان کد Nix بنویسید، راهنمای ما دربارهٔ [dependency management] را نیز در نظر بگیرید.[^flake-inputs]
این نمای کلی می‌تواند به شما کمک کند تا ضمن حفظ سازگاری، آنچه را که از فلیک‌ها نیاز دارید به دست آورید.

[dependency management]: https://nix.dev/guides/recipes/dependency-management.html

[^flake-inputs]: مخازن Nix که فقط نقطه ورود فلیک ارائه می‌دهند را می‌توان با استفاده از [`flake-inputs`] درون‌ریزی کرد.

### قابلیت کشف

نخستین گام در استفاده از فلیک‌ها، افزودن یک فایل `flake.nix` است که `outputs` را مشخص می‌کند.

مزایا:

- استفاده از کدهای سایر پروژه‌های مبتنی بر فلیک.
- بررسی معتبر بودن ساختار فایل `flake.nix` توسط Nix.

معایب:

- فلیک‌ها هیچ [parameters] ندارند.
  این یعنی `flake.nix` و کاربر نهایی آن باید دربارهٔ [`system`] استفاده‌شده صریح باشند.
  این کار با استفاده از ابزارهایی مانند [`flake-utils`] ساده‌تر می‌شود.
- به عنوان یک ویژگی تجربی، فلیک‌ها ممکن است هنوز تغییر کنند.

گزینه‌های جایگزین:

- استفاده از فلیک‌ها به عنوان پوسته‌های نازک (thin wrappers) روی کد موجود نیکس.
  به این ترتیب، کد می‌تواند به هر دو روش استفاده شود.
- استفاده از ماژول‌های Nix: کاربران فلیک می‌توانند این موارد را با `flake = false;` درون‌ریزی کنند.
- از نسخه NixOS 26.05 به بعد، یک یا چند پیکربندی NixOS را می‌توان از یک [`system.nix` entrypoint] بارگذاری کرد.

[`import`]: https://nix.dev/tutorials/nix-language#import
[`system.nix` entrypoint]: https://nixos.org/manual/nixos/stable/release-notes.html#sec-release-26.05-highlights

### اجرای دستورها

فلیک‌ها از طریق [v3 `nix` command line interface] در نیکس استفاده می‌شوند.
این رابط می‌تواند برنامه‌ها را با استفاده از ارجاعی مانند `.` یا `github:NixOS/nixpkgs` بسازد یا اجرا کند.

شما می‌توانید این قابلیت را برای یک دستور با اضافه کردن موارد زیر فعال کنید:

```
 --experimental-features 'nix-command flakes'
```
```یا به صورت دائمی در پیکربندی‌های NixOS یا Home Manager با استفاده از:

```
nix.settings.experimental-features = [ "nix-command" "flakes" ];
```

برای ساختن درایویشن در بخش `packages.x86_64-linux.default` فایل `flake.nix` خود، این دستور را اجرا کنید:

```
```bash
nix build .#packages.x86_64-linux.default
```

می‌توانید این دستور را به صورت `nix build .#default` یا صرفاً `nix build` کوتاه‌سازی کنید.

دستور `nix run` برنامه‌ها را در `outputs.apps` اجرا می‌کند.
دستور `nix run .#default` مقدار `outputs.apps.default` را اجرا می‌کند.
دستور `nix run` به تنهایی نیز همان را اجرا می‌کند.

برای مثال، برای اجرای بسته `hello` از *Nixpkgs*:

```bash
nix run nixpkgs#hello -- --greeting "hello from flakes"
```

این کار از نسخه تعیین‌شده توسط نام مستعار `nixpkgs` در رجیستری شما استفاده می‌کند.

برای اجرای بسته `hello` از شاخه `nixpkgs-unstable` در *Nixpkgs*:

```bash
nix run github:NixOS/nixpkgs/nixpkgs-unstable#hello
```

[v3 `nix` command line interface]: /pages/nix-manual/command-ref/experimental-commands

مزایا:

- فلیک‌ها (Flakes) ساخت‌ها را کش می‌کنند تا در ساخت‌های یکسان بعدی در زمان صرفه‌جویی شود.
  این کار می‌تواند زمان را ذخیره کند؛ برای مثال، اگر ساخت‌های بدون تغییر را در ادغام مداوم (CI) اجرا کنید.
- فلیک‌ها باعث می‌شوند اجرای برنامه‌ها، از جمله از مخزن‌های راه دور، آسان‌تر شود.
- فلیک‌ها به‌طور پیش‌فرض در [حالت خالص] اجرا می‌شوند.
  این امر سبکی از برنامه‌نویسی را ترویج می‌کند که احتمال بازتولیدپذیر[^reproducible] بودن برنامه‌ها را افزایش می‌دهد.
- برای پروژه‌هایی که از [Git] استفاده می‌کنند، فلیک‌ها فقط فایل‌های ردیابی‌شده را می‌سازند.
  این کار به جلوگیری از ساخت‌های مجدد کمک می‌کند.

[pure mode]: /pages/nix-manual/language#impurities

[^reproducible]: حتی در حالت خالص نیز بازتولیدپذیری [در واقع تضمین نمی‌شود].

[not actually guaranteed]: https://discourse.nixos.org/t/nix-flakes-explained-what-they-solve-why-they-matter-and-the-future/72302/7

معایب:

- ساخت‌ها کل پوشه فلیک را در انبار نیکس کپی می‌کنند.
  این کار آن‌ها را کش می‌کند، اما برای مخزن‌های حجیمی مانند *Nixpkgs* می‌تواند [کندتر] باشد.
- پیاده‌سازی همچنان برای [فلیک‌ها] و [رابط خط فرمان v3] مشکلاتی دارد.
- برای اینکه فلیک‌ها فایل‌ها را ببینند، فایل‌ها باید در وضعیت استیج (Staged) قرار گیرند.

[slower]: https://github.com/NixOS/nix/issues/3121
[flakes]: https://github.com/NixOS/nix/issues?q=is%3Aissue+is%3Aopen+label%3Aflakes+sort%3Areactions-%2B1-desc
[v3 CLI]: https://github.com/NixOS/nix/issues?q=is%3Aissue+is%3Aopen+label%3Anew-cli+sort%3Areactions-%2B1-desc

راه‌حل‌های جایگزین:

- فایل‌های ساده‌ی نیکس را می‌توان با [دستورات v2] (مانند [`nix-build`]، [`nix-shell`]) یا با [`--file` flag] یا `-f` در دستورات v3 استفاده کرد.
- در *NixOS*، می‌توانید با تنظیم [`nixpkgs.flake.source = pkgs.path;`] در پیکربندی NixOS خود، بخش `nixpkgs` در دستورات v3 را به یک مجموعه بسته `pkgs` تبدیل کنید.
  همچنین [مدیریت وابستگی] را مشاهده کنید.
- با استفاده از [`builtins.fetchTree`] از ویژگی آزمایشی [`fetch-tree`]، می‌توان [`nix run`] را برای نقطه‌ورودی‌های غیرفلیک شبیه‌سازی کرد[^emulated].

[Git]: https://git-scm.com/
[v2 CLI]: /pages/nix-manual/command-ref/main-commands
[`--file` flag]: /pages/nix-manual/command-ref/experimental-commands#options-that-change-the-interpretation-of-installables
[`nix-build`]: /pages/nix-manual/command-ref/nix-build
[`nix-shell`]: /pages/nix-manual/command-ref/nix-shell
[`nixpkgs.flake.source = pkgs.path;`]: https://search.nixos.org/options?channel=unstable&show=nixpkgs.flake.source&query=nixpkgs.flake.source
[managing dependencies]: https://nix.dev/guides/recipes/dependency-management#managing-nixos-configurations
[`builtins.fetchTree`]: https://noogle.dev/f/builtins/fetchTree
[`fetch-tree`]: /pages/nix-manual/development/experimental-features#xp-feature-fetch-tree
[`nix run`]: /pages/nix-manual/command-ref/experimental-commands

[^emulated]: دستور `nix run github:NixOS/nixpkgs#hello` برای پروژه‌های غیرفلیک ممکن است شبیه به `nix-shell -p '(import (builtins.fetchTree "github:NixOS/nixpkgs").outPath {'{'}'{'{'}'{'}'} {'{'}'{'}'}'{'}'}).hello' --run 'hello'` به نظر برسد.
یک دستور جایگزین `nix-run` که از نحو `nix run` استفاده می‌کند را می‌توان با استفاده از یک آلیاس Bash به صورت `alias nix-run='run() {'{'}'{'{'}'{'}'} $(nix-instantiate --raw --impure --eval --expr "(import &lt;nixpkgs&gt; {'{'}'{'{'}'{'}'}{'{'}'{'}'}'{'}'}).lib.getExe (import (builtins.fetchTree \"$(cut -d "#" -f 1 &lt;&lt;&lt; "$1")\").outPath {'{'}'{'{'}'{'}'} {'{'}'{'}'}'{'}'}).$(cut -d "#" -f 2 &lt;&lt;&lt; "$1")"); {'{'}'{'}'}'{'}'}; run'` تعریف کرد.

### مدیریت وابستگی

صفت `inputs` در فلیک‌ها می‌تواند وابستگی‌ها را مدیریت کند.
به طور پیش‌فرض، این کار وابستگی‌های بازگشتی را به صورت ضمنی مدیریت می‌کند.
در صورتی که یک کتابخانه چندین بار استفاده شود، این امر می‌تواند نسخه‌های متفاوتی از همان کتابخانه را به دست دهد.
اگر مایل باشید، می‌توانید با استفاده از دستورات `follows` این موارد را بازنویسی کنید:

```
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
}
```

به این ترتیب، ورودی‌های Home Manager از `nixpkgs` انتخابی شما مجدداً استفاده می‌کنند.

مزایا:

- بازتولید نرم‌افزار منتشرشده را با پیروی از نسخه‌های استفاده‌شده توسط آن‌ها آسان می‌کند.
- می‌توانید ورودی‌های بازگشتی را بازنویسی کنید.

معایب:

- فلیک‌ها به‌طور پیش‌فرض از نسخه‌های موجود در `flake.lock` وابستگی‌ها تبعیت می‌کنند، بنابراین اگر این موارد را با `follows` بازنویسی نکنید، ممکن است با موارد زیر مواجه شوید:
  - چندین نسخه از یک وابستگی یکسان.
  - وابستگی‌های منسوخ‌شده، در صورتی که نسخه‌های آن‌ها به‌طور فعال به‌روز نشوند.
- وابستگی‌ها به‌صورت اشتیاق‌آميز دریافت می‌شوند و وابستگی‌هایی را بارگیری می‌کنند که ممکن است از آن‌ها استفاده نکنید.
- اگر از فلیک‌ها استفاده نکنید، بازنویسی وابستگی‌های مدیریت‌شده توسط ورودی‌های فلیک دشوار است.
- اگر فلیک شما به عنوان یک کتابخانه استفاده شود، باید دستورات `follows` را برای تمام ورودی‌های بازگشتی اضافه کنید.
  در غیر این صورت، مصرف‌کنندگان پایین‌دست نمی‌توانند `follows` خود را روی ورودی‌های غیرمستقیم شما اعمال کنند.

گزینه‌های جایگزین:

- مدیریت وابستگی‌ها با [`npins`].
- مدیریت درون‌خطی وابستگی‌ها با استفاده از توابعی مانند [fetchers] یا [`builtins.fetchTree`].
- استفاده از `inputs.&lt;name&gt;.flake = false;`

[fetchers]: https://nixos.org/manual/nixpkgs/stable/#chap-pkgs-fetchers
[`flake-inputs`]: https://github.com/fricklerhandwerk/flake-inputs
[`npins`]: https://nix.dev/guides/recipes/dependency-management.html

### نیکس صرفاً مبتنی بر فلیک (Flake-only Nix)

از آنجا که فلیک‌ها (تا حد زیادی [^subset]) از Nix به عنوان یک زبان داخلی استفاده می‌کنند، حتی می‌توانید تمام کد Nix را در فایل‌های فلیک قرار دهید.
در جامعه‌ی کاربری، این سبک کدنویسی الگوی درندریت (dendritic pattern) نامیده می‌شود.
با استفاده از فلیک‌ها، این الگو با کتابخانه [`flake-parts`](https://github.com/hercules-ci/flake-parts) آسان‌تر می‌شود،
کتابخانه‌ای که به شما اجازه می‌دهد کد را در فایل‌های مختلف شبیه به فلیک پخش کنید.

مزایا:

- به استفاده از طرح‌واره و ورودی‌های فلیک‌ها از هر چنین کد Nix کمک می‌کند.

Cons:

- دسترسی به این کد را بدون استفاده از فلیک‌ها دشوارتر می‌کند.

گزینه‌های جایگزین:

- استفاده از فلیک‌ها به عنوان پوشش‌های سبک روی کدهای موجود Nix، به طوری که کد بتواند به هر دو روش استفاده شود.
- استفاده از کتابخانه [`flake-compat`] برای قرار دادن بسته پیش‌فرض یا شل یک فلیک در معرض کاربران غیر فلیک.
- انتشار صریح پارامترهای مورد نیاز در سراسر ماژول‌ها یا استفاده از [`specialArgs`] در NixOS.

[`flake-compat`]: https://github.com/NixOS/flake-compat
[`specialArgs`]: https://nixos.org/manual/nixos/unstable/options#opt-_module.args

### تاریخچه

- مفهوم‌سازی
  - فلیک‌ها در [RFC 49] پیشنهاد شدند و طی یک [نوشته وبلاگ] معرفی شدند.
- طراحی
  - پیشنهاد فلیک‌ها به دلیل تلاش برای حل مشکلات بسیار زیاد به‌صورت هم‌زمان و در لایه انتزاعی نادرست، مورد انتقاد قرار گرفت.
  - این طراحی همچنان دارای [مشکلات مختلفی] از جمله در زمینه‌های مدیریت نسخه، قابلیت ترکیب‌پذیری، کامپایل متقاطع و وابستگی متقابل تنگاتنگ با Nixpkgs است.
  - همچنین هنوز [سوالات طراحی باز] زیادی پیرامون رابط خط فرمان `nix` وجود دارد.
- پیاده‌سازی
  - هنوز [مشکلاتی در پیاده‌سازی] وجود دارد.
- فرآیند
  - در حالی که هنوز نگرانی‌های حل‌نشده‌ای درباره طراحی وجود داشت،
    پیاده‌سازی بدون پذیرفته شدن RFC ادغام شد (و در واقع در زمان ادغام پس گرفته شد)،
    که این امر سوالاتی را درباره روند صحیح اجرایی مطرح می‌کند.
  - این RFC بدون هیچ‌گونه جدول زمانی برای خاتمه دادن به این آزمایش بسته شد.
  - پروژه‌های زیادی به فلیک‌ها وابسته شدند، که این امر تکرار و بهبود طراحی آن‌ها را بدون شکستن کد بسیاری از کاربران دشوارتر کرد.
- جامعه کاربری
  - این طراحی توسط تمام بخش‌های جامعه کاربری پذیرفته نشده بود، به عنوان مثال *Nixpkgs* از آن در ابزارهای داخلی خود استفاده نکرد.
    در نتیجه این امر، رویکردهای انشعابی نسبت به فلیک‌ها شکل گرفت،
    به طوری که مثلاً شرکت Determinate Systems (که ویژگی‌های انحصاری پیرامون فلیک‌ها ارائه می‌دهد) به‌طور یک‌جانبه این ویژگی را پایدار اعلام کرد،
    در حالی که انشعاب Nix مبتنی بر جامعهٔ کاربری یعنی Lix [مجموعه ویژگی‌ها را یکپارچه کرد] تا به عنوان یک «نسخه ۱» عملی تبدیل شود.
    چنین انشعاب‌هایی به طور بالقوه می‌توانند وعدهٔ یک رابط یکپارچه را که در وهله اول آزمایش فلیک‌ها را به جلو راند، نقض کنند.

[RFC 49]: https://github.com/NixOS/rfcs/pull/49
[نوشته وبلاگ]: https://tweag.io/blog/2020-05-25-flakes/
[مشکلات مختلفی]: https://wiki.lix.systems/books/lix-contributors/page/flakes-feature-freeze#bkmrk-design-issues-of-fla
[سوالات طراحی باز]: https://github.com/NixOS/nix/issues?q=is%3Aissue+is%3Aopen+label%3Anew-cli+sort%3Areactions-%2B1-desc
[مشکلاتی در پیاده‌سازی]: https://github.com/NixOS/nix/issues?q=is%3Aissue+is%3Aopen+label%3Aflakes+sort%3Areactions-%2B1-desc
[مجموعه ویژگی‌ها را یکپارچه کرد]: https://wiki.lix.systems/books/lix-contributors/page/flake-stabilisation-proposal

## مطالعات بیشتر

- [مقاله ویکی](https://wiki.nixos.org/wiki/Flakes)
- [فلیک‌ها واقعی نیستند و نمی‌توانند به شما آسیب برسانند: راهنمای استفاده از فلیک‌های نیکس به روش غیرفلیک](https://jade.fyi/blog/flakes-arent-real/) (Jade Lovelace، ژانویه ۲۰۲۴)
- [فلیک‌های نیکس آزمایشی است که کارهای زیادی را به‌طور هم‌زمان انجام داد...](https://samuel.dionne-riel.com/blog/2023/09/06/flakes-is-an-experiment-that-did-too-much-at-once.html) ([نظرات](https://discourse.nixos.org/t/nix-flakes-is-an-experiment-that-did-too-much-at-once/32707)) (Samuel Dionne-Riel، سپتامبر ۲۰۲۳)
- [تجربی به معنای ناپایدار نیست](https://determinate.systems/posts/experimental-does-not-mean-unstable) ([نظرات](https://discourse.nixos.org/t/experimental-does-not-mean-unstable-detsyss-perspective-on-nix-flakes/32703)) (Graham Christensen، سپتامبر ۲۰۲۳)
- [ساعت نیکس: مقایسه فلیک‌ها با نیکس سنتی](https://www.youtube.com/watch?v=atmoYyBAhF4) (Silvan Mosberger، نوامبر ۲۰۲۲)
