# <a id="agda"></a> Agda

## <a id="how-to-use-agda"></a> نحوه استفاده از Agda

Agda به عنوان بسته [agda](https://search.nixos.org/packages?channel=unstable&show=agda&from=0&size=30&sort=relevance&query=agda) در دسترس است.

بسته `agda` یک Agda-wrapper نصب می‌کند که `agda` را با مقدار `--library-file` تنظیم‌شده روی یک library-file تولیدشده درون انبار نیکس (Nix store) فراخوانی می‌کند؛ این بدان معناست که library-file شما در `$HOME/.agda/libraries` نادیده گرفته خواهد شد. به‌طور پیش‌فرض، بسته agda نرم‌افزار Agda را بدون هیچ کتابخانه‌ای نصب می‌کند، یعنی library-file تولیدشده خالی است. برای استفاده از Agda به همراه کتابخانه‌ها، می‌توان از تابع `agda.withPackages` استفاده کرد. این تابع یکی از موارد زیر را می‌پذیرد:

* لیستی از بسته‌ها،
* یا تابعی که در صورت دریافت مجموعه ویژگی `agdaPackages`، لیستی از بسته‌ها را برمی‌گرداند،
* یا یک مجموعه ویژگی شامل لیستی از بسته‌ها و یک درایویشن GHC برای کامپایل (به زیر مراجعه کنید).
* یا یک مجموعه ویژگی شامل تابعی که در صورت دریافت مجموعه ویژگی `agdaPackages`، لیستی از بسته‌ها را برمی‌گرداند و یک درایویشن GHC برای کامپایل (به زیر مراجعه کنید).

به عنوان مثال، فرض کنید نسخه‌ای از Agda را می‌خواهیم که به کتابخانه استاندارد دسترسی داشته باشد. این نسخه را می‌توان با عبارت‌های زیر به دست آورد:

```nix
agda.withPackages [ agdaPackages.standard-library ]
```

یا

```nix
agda.withPackages (p: [ p.standard-library ])
```

یا می‌توان آن را مانند بخش [کامپایل Agda](#compiling-agda) فراخوانی کرد.

اگر می‌خواهید از نسخه دیگری از یک کتابخانه استفاده کنید (برای مثال یک نسخه توسعه)، صفت `src` بسته را بازنویسی کنید تا به مخزن محلی شما اشاره کند.

```nix
agda.withPackages (p: [
  (p.standard-library.overrideAttrs (oldAttrs: {
    version = "local version";
    src = /path/to/local/repo/agda-stdlib;
  }))
])
```

همچنین می‌توانید به یک مخزن GitHub ارجاع دهید

```nix
agda.withPackages (p: [
  (p.standard-library.overrideAttrs (oldAttrs: {
    version = "1.5";
    src = fetchFromGitHub {
      repo = "agda-stdlib";
      owner = "agda";
      rev = "v1.5";
      hash = "sha256-nEyxYGSWIDNJqBfGpRDLiOAnlHJKEKAOMnIaqfVZzJk=";
    };
  }))
])
```

اگر می‌خواهید از کتابخانه‌ای استفاده کنید که به Nixpkgs اضافه نشده است، می‌توانید با فراخوانی `agdaPackages.mkDerivation` یک وابستگی به یک کتابخانه محلی اضافه کنید.

```nix
agda.withPackages (p: [
  (p.mkDerivation {
    pname = "your-agda-lib";
    version = "1.0.0";
    src = /path/to/your-agda-lib;
  })
])
```

دوباره می‌توانید به GitHub ارجاع دهید.

```nix
agda.withPackages (p: [
  (p.mkDerivation {
    pname = "your-agda-lib";
    version = "1.0.0";
    src = fetchFromGitHub {
      repo = "repo";
      owner = "owner";
      version = "...";
      rev = "...";
      hash = "...";
    };
  })
])
```

برای اطلاعات بیشتر در مورد `mkDerivation`، [ساخت بسته‌های Agda](#building-agda-packages) را ببینید.

Agda به‌طور پیش‌فرض از این کتابخانه‌ها استفاده نخواهد کرد. برای اینکه به Agda بگوییم از یک کتابخانه استفاده کند، چند گزینه داریم:

* فراخوانی `agda` با پرچم library:

```ShellSession
  $ agda -l standard-library -i . MyFile.agda
  ```
* یک فایل `my-library.agda-lib` برای پروژه‌ای که روی آن کار می‌کنید بنویسید که ممکن است شبیه به این باشد:
```
  name: my-library
  include: .
  depend: standard-library
  ```
* فایل `~/.agda/defaults` را ایجاد کرده و هر کتابخانه‌ای را که می‌خواهید به‌طور پیش‌فرض استفاده کنید، اضافه نمایید.

اطلاعات بیشتر را می‌توانید در [مستندات رسمی Agda درباره مدیریت کتابخانه](https://agda.readthedocs.io/en/v2.6.1/tools/package-system.html) بیابید.

## <a id="compiling-agda"></a> کامپایل کردن Agda

ماژول‌های Agda را می‌توان با استفاده از بک‌اند GHC و پرچم `--compile` کامپایل کرد. نسخه‌ای از `ghc` همراه با `ieee754` از طریق پرچم `--with-compiler` در دسترس برنامه Agda قرار می‌گیرد.
این مورد را می‌توان با نسخه دیگری از `ghc` به صورت زیر بازنشانی کرد:

```nix
agda.withPackages {
  pkgs = [
    # ...
  ];
  ghc = haskell.compiler.ghcHEAD;
}
```

برای نصب Agda بدون GHC، از `ghc = null;` استفاده کنید.

## <a id="writing-agda-packages"></a> نوشتن بسته‌های Agda

برای نوشتن یک derivation نیکس برای یک کتابخانه Agda، ابتدا بررسی کنید که کتابخانه دارای یک فایل (تک) `*.agda-lib` باشد.

سپس می‌توان یک derivation را با استفاده از `agdaPackages.mkDerivation` نوشت. این تابع دارای آرگومان‌های مشابهی با `stdenv.mkDerivation` است که موارد زیر به آن اضافه شده‌اند:

* `libraryName` باید نامی باشد که در فایل `*.agda-lib` ظاهر می‌شود و مقدار پیش‌فرض آن `pname` است.
* `libraryFile` باید نام فایلِ مربوط به فایل `*.agda-lib` باشد و مقدار پیش‌فرض آن `${'{'}'{'{'}'{'}'}libraryName{'{'}'{'}'}'{'}'}.agda-lib` است.

در ادامه یک نمونه `default.nix` آورده شده است:

```nix
{
  nixpkgs ? <nixpkgs>,
}:
with (import nixpkgs { });
agdaPackages.mkDerivation {
  version = "1.0";
  pname = "my-agda-lib";
  src = ./.;
  buildInputs = [ agdaPackages.standard-library ];
}
```

### <a id="building-agda-packages"></a> ساخت بسته‌های Agda

فاز ساخت پیش‌فرض برای `agdaPackages.mkDerivation` دستور `agda --build-library` را اجرا می‌کند.
اگر برای ساخت بسته به چیز دیگری (مثلاً `make`) نیاز باشد، باید `buildPhase` بازنویسی شود.
علاوه بر این، اگر گام‌هایی وجود دارند که باید قبل از بررسی کتابخانه انجام شوند، می‌توان از `preBuild` یا `configurePhase` استفاده کرد.
`agda` و کتابخانه‌های Agda موجود در `buildInputs` در طول فاز ساخت در دسترس قرار می‌گیرند.

### <a id="installing-agda-packages"></a> نصب بسته‌های Agda

فاز نصب پیش‌فرض، فایل‌های سورس Agda، فایل‌های رابط Agda (`*.agdai`) و فایل‌های `*.agda-lib` را در پوشه خروجی کپی می‌کند.
این رفتار قابل بازنویسی است.

به طور پیش‌فرض، سورس‌های Agda فایل‌هایی هستند که به `.agda` ختم می‌شوند، یا فایل‌های literate Agda که به `.lagda`، `.lagda.tex`، `.lagda.org`، `.lagda.md` یا `.lagda.rst` ختم می‌شوند. فهرست پسوندهای سورس شناخته‌شدهٔ Agda را می‌توان با تنظیم متغیر پیکربندی `extraExtensions` گسترش داد.

## <a id="maintaining-the-agda-package-set-on-nixpkgs"></a> نگهداری مجموعه بسته‌های Agda در Nixpkgs

هدف ما ارائه تمام کتابخانه‌های رایج Agda به عنوان بسته در `nixpkgs`
و به‌روز نگه داشتن آن‌ها است.
مشارکت‌ها و کمک به نگهداری همیشه مورد استقبال قرار می‌گیرد،
اما تلاش لازم برای نگهداری معمولاً کم است زیرا بوم‌سازگان Agda کاملاً کوچک است.

مجموعه بسته‌های Agda در `nixpkgs` تلاش می‌کند نقشی مشابه [Stackage](https://www.stackage.org/) در دنیای Haskell ایفا کند.
این یک مجموعه دست‌چین‌شده از کتابخانه‌هاست که:

1. همواره با یکدیگر کار می‌کنند.
2. تا حد امکان به‌روز هستند.

در حالی که بوم‌سازگان Haskell بسیار بزرگ است و Stackage بسیار خودکار عمل می‌کند،
مجموعه بسته‌های Agda کوچک است و (هنوز) می‌توان آن را به صورت دستی نگهداری کرد.

### <a id="adding-agda-packages-to-nixpkgs"></a> افزودن بسته‌های Agda به Nixpkgs

برای افزودن یک بسته Agda به `nixpkgs`، باید derivation در مسیر `pkgs/development/libraries/agda/${'{'}'{'{'}'{'}'}library-name{'{'}'{'}'}'{'}'}/default.nix` نوشته شود و یک ورودی به `pkgs/top-level/agda-packages.nix` اضافه گردد. در اینجا، بسته در اسکوپی با دسترسی به تمام کتابخانه‌های دیگر Agda فراخوانی می‌شود، بنابراین derivation می‌تواند شبیه به این باشد:

```nix
{
  mkDerivation,
  standard-library,
  fetchFromGitHub,
}:

mkDerivation {
  pname = "my-library";
  version = "1.0";
  src = <...>;
  buildInputs = [ standard-library ];
  meta = <...>;
}
```

می‌توانید برای ایده گرفتن بیشتر، به سایر فایل‌های موجود در `pkgs/development/libraries/agda/` نگاهی بیندازید.

توجه داشته باشید که تابع درایویشن با مقداردهی `mkDerivation` به `agdaPackages.mkDerivation` فراخوانی می‌شود، بنابراین می‌توانید از مجموعه‌ای مشابه آنچه در `default.nix` خود در بخش [نوشتن بسته‌های Agda](#writing-agda-packages) داشتید استفاده کنید، با این تفاوت که `agdaPackages.mkDerivation` با `mkDerivation` جایگزین شود.

در اینجا اسکلت یک درایویشن نمونه برای iowa-stdlib آورده شده است:

```nix
mkDerivation {
  version = "1.5.0";
  pname = "iowa-stdlib";

  src = <...>;

  libraryFile = "";
  libraryName = "IAL-1.3";

  buildPhase = ''
    runHook preBuild

    patchShebangs find-deps.sh
    make

    runHook postBuild
  '';
}
```

این کتابخانه فایلی به نام `.agda-lib` دارد، بنابراین یک رشته خالی به `libraryFile` می‌دهیم زیرا هیچ چیزی پیش از `.agda-lib` در نام فایل قرار ندارد. این فایل شامل `name: IAL-1.3` است، و بنابراین `libraryName =  "IAL-1.3"` قرار می‌دهیم. این کتابخانه از فایل `Everything.agda` استفاده نمی‌کند و در عوض یک Makefile دارد، بنابراین نیازی به تنظیم `everythingFile` نیست و یک `buildPhase` سفارشی تنظیم می‌کنیم.

هنگام نوشتن یک بسته Agda، بسیار مهم است که مطمئن شوید هیچ فایل `.agda-lib` به عنوان یک فایل منفرد به انبار اضافه نشود (برای مثال با استفاده از `writeText`). این امر باعث می‌شود Agda تصور کند انبار نیکس (Nix store) یک کتابخانه Agda است و هر زمان که چیزی را نوع‌سنجی می‌کند، تلاش خواهد کرد در آن بنویسد. ببینید: [https://github.com/agda/agda/issues/4613](https://githcub.com/agda/agda/issues/4613).

در درخواست کشش مربوط به افزودن این کتابخانه،
می‌توانید با نوشتن در یک نظر بررسی کنید که آیا به‌درستی ساخته می‌شود یا خیر:

```
@ofborg build agdaPackages.my-library
```

### <a id="agda-maintaining-packages"></a> نگه‌داری بسته‌های Agda

همان‌طور که پیش‌تر اشاره شد، هدف داشتن یک مجموعه بسته‌ی سازگار و به‌روز است.
این دو شرط گاهی یکدیگر را نفی می‌کنند:
برای مثال، اگر `agdaPackages.standard-library` را به دلیل انتشار یک نسخه بالادستی به‌روزرسانی کنیم،
این کار معمولاً باعث شکستگی بسیاری از وابستگی‌های معکوس می‌شود،
یعنی کتابخانه‌های پایین‌دستی Agda که به کتابخانه استاندارد وابسته هستند.
در `nixpkgs` ما معمولاً جزو نخستین کسانی هستیم که متوجه این موضوع می‌شویم،
زیرا تست‌های ساخت آماده‌ای برای بررسی این مسئله داریم.

در یک pull request که مثلاً کتابخانه استاندارد را به‌روزرسانی می‌کند، باید کامنت زیر را بنویسید:

```
@ofborg build agdaPackages.standard-library.passthru.tests
```

این کار تمام وابستگی‌های معکوس کتابخانه استاندارد را می‌سازد،
برای نمونه `agdaPackages.agda-categories`.

در برخی موارد، ساخت _همه_ بسته‌های Agda مفید است.
این کار را می‌توان با کامنت گیت‌هاب زیر انجام داد:

```
@ofborg build agda.passthru.tests.allPackages
```

گاه ساخت‌های وابستگی‌های معکوس شکست می‌خورند، زیرا هنوز به‌روزرسانی و منتشر نشده‌اند.
شما باید با ثبت سریع یک issue، نگه‌دارندگان را از این شکست مطلع کرده
و به خطای ساخت (که می‌توانید آن را از لاگ‌های ofborg به دست آورید) اشاره نمایید.
اگر انگیزه دارید، حتی می‌توانید یک pull request ارسال کنید که مشکل را برطرف سازد.
معمولاً نگه‌دارندگان ظرف یک یا دو هفته با انتشار نسخه‌ای جدید پاسخ خواهند داد.
ارتقای نسخهٔ آن وابستگی معکوس باید یک کامیت بعدی روی PR شما باشد.

در موارد نادری که انتظار نمی‌رود انتشار جدیدی در زمانی پذیرفتنی صورت گیرد،
بستهٔ شکست‌خورده را با تنظیم `meta.broken = true;` به عنوان خراب مشخص کنید.
این کار آن را از تست ساخت مستثنی می‌کند.
بعداً وقتی مشکل برطرف شد می‌توان آن را اضافه کرد
و در این میان، مانع پیشرفت کل مجموعه بسته‌ها نمی‌شود.
