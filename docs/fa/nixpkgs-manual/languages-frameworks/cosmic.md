# COSMIC {#sec-language-cosmic}

## بسته‌بندی برنامه‌های COSMIC {#ssec-cosmic-packaging}

‏COSMIC (Computer Operating System Main Interface Components) یک محیط دسکتاپ توسعه‌یافته توسط System76 است که عمدتاً برای توزیع Linux به نام Pop!_OS ساخته شده است. برنامه‌ها در بوم‌سازگان COSMIC به زبان Rust نوشته شده‌اند و از libcosmic استفاده می‌کنند که روی چارچوب رابط کاربر گرافیکی Iced بنا شده است. این بخش نحوه بسته‌بندی و یکپارچه‌سازی صحیح برنامه‌های COSMIC را در Nix توضیح می‌دهد.

### libcosmicAppHook {#ssec-cosmic-libcosmic-app-hook}

‏`libcosmicAppHook` یک قلاب راه‌اندازی است که با پیکربندی و پوشش‌دهی (wrapping) خودکار برنامه‌های مبتنی بر libcosmic به این امر کمک می‌کند. این قلاب بسیاری از نیازمندی‌های رایج را مدیریت می‌کند، مانند:

- تنظیم پیونددهی مناسب برای کتابخانه‌هایی که ممکن است توسط برنامه‌های libcosmic/iced به صورت dlopen بارگیری شوند
- پیکربندی مسیرهای XDG برای اسکیماهای تنظیمات، آیکون‌ها و سایر منابع
- مدیریت متغیرهای محیطی Vergen برای اطلاعات زمان ساخت
- تنظیم پرچم‌های پیونددهنده (linker flags) زبان Rust برای کتابخانه‌های خاص

برای استفاده از این قلاب، کافی است آن را به `nativeBuildInputs` بسته خود اضافه کنید:

```nix
{
  lib,
  rustPlatform,
  libcosmicAppHook,
}:
rustPlatform.buildRustPackage {
  # ...
  nativeBuildInputs = [ libcosmicAppHook ];
  # ...
}
```

### پشتیبان تنظیمات {#ssec-cosmic-settings-fallback}

برنامه‌های COSMIC از کامپوننت‌های رابط کاربری libcosmic استفاده می‌کنند که ممکن است به دسترسی به تنظیمات تم نیاز داشته باشند. بسته `cosmic-settings` تنظیمات تم پیش‌فرض را به‌عنوان یک پشتیبان در پوشه `share` خود ارائه می‌دهد. به طور پیش‌فرض، `libcosmicAppHook` این مسیر پشتیبان را در `XDG_DATA_DIRS` قرار می‌دهد و تضمین می‌کند که برنامه‌های COSMIC حتی اگر تنظیمات تم در جای دیگری از سیستم در دسترس نباشند، به آن‌ها دسترسی داشته باشند.

این رفتار پشتیبان را می‌توان با تنظیم `includeSettings = false` هنگام گنجاندن hook غیرفعال کرد:

```nix
{
  lib,
  rustPlatform,
  libcosmicAppHook,
}:
let
  # Get build-time version of libcosmicAppHook
  libcosmicAppHook' = (libcosmicAppHook.__spliced.buildHost or libcosmicAppHook).override {
    includeSettings = false;
  };
in
rustPlatform.buildRustPackage {
  # ...
  nativeBuildInputs = [ libcosmicAppHook' ];
  # ...
}
```

توجه داشته باشید که `cosmic-settings` یک برنامه مجزا بوده و بخشی از خود سیستم تنظیمات libcosmic نیست. این برنامه فقط برای ارائه این تنظیمات تم جایگزین (fallback)، به صورت پیش‌فرض در `libcosmicAppHook` قرار گرفته است.

### آیکون‌ها {#ssec-cosmic-icons}

برنامه‌های COSMIC می‌توانند از آیکون‌های تم آیکون COSMIC استفاده کنند. اگرچه برنامه‌های COSMIC می‌توانند بدون این آیکون‌ها ساخت و اجرا شوند، اما فاقد برخی عناصر بصری خواهند بود. `libcosmicAppHook` به طور خودکار `cosmic-icons` را به عنوان جایگزین در `XDG_DATA_DIRS` برنامه رپ‌شده (wrapped) قرار می‌دهد تا اطمینان حاصل شود که برنامه حتی در صورت عدم نصب سرتاسری تم آیکون COSMIC روی سیستم، به آیکون‌های مورد نیاز خود دسترسی دارد.

برخلاف جایگزین `cosmic-settings`، جایگزین `cosmic-icons` قابل حذف یا غیرفعال‌سازی نیست، چرا که دسترسی به این آیکون‌ها برای رندر بصری مناسب برنامه‌های COSMIC ضروری است.

### کتابخانه‌های زمان اجرا {#ssec-cosmic-runtime-libraries}

برنامه‌های COSMIC ساخته‌شده بر پایه libcosmic و Iced به چند کتابخانه زمان اجرا نیاز دارند که به جای پیوند مستقیم، از طریق dlopen بارگذاری می‌شوند. `libcosmicAppHook` با تنظیم پرچم‌های مناسب لینک‌کننده Rust اطمینان حاصل می‌کند که این کتابخانه‌ها به درستی پیوند داده شوند. کتابخانه‌های پوشش‌داده‌شده عبارتند از:

- کتابخانه‌های گرافیکی (EGL, Vulkan)
- کتابخانه‌های ورودی (xkbcommon)
- پروتکل‌های سرور نمایش (Wayland, X11)

این موضوع تضمین می‌کند که برنامه‌ها در زمان اجرا به درستی کار کنند، اگرچه از بارگذاری پویا برای این وابستگی‌ها استفاده می‌کنند.

### افزودن آرگومان‌های سفارشی رپر {#ssec-cosmic-custom-wrapper-args}

شما می‌توانید با استفاده از `libcosmicAppWrapperArgs` در قلاب `preFixup` آرگومان‌های بیشتری را به رپر ارسال کنید:

```nix
{
  lib,
  rustPlatform,
  libcosmicAppHook,
}:
rustPlatform.buildRustPackage {
  # ...
  preFixup = ''
    libcosmicAppWrapperArgs+=(--set-default ENVIRONMENT_VARIABLE VALUE)
  '';
  # ...
}
```

## مشکلات متداول {#ssec-cosmic-common-issues}

### تنظیم متغیرهای محیطی Vergen {#ssec-cosmic-common-issues-vergen}

بسیاری از برنامه‌های COSMIC از کریت Rust مربوط به Vergen برای دریافت اطلاعات زمان ساخت استفاده می‌کنند. `libcosmicAppHook` به طور خودکار متغیر محیطی `VERGEN_GIT_COMMIT_DATE` را بر اساس `SOURCE_DATE_EPOCH` تنظیم می‌کند تا از ساخت‌های بازتولیدپذیر اطمینان حاصل شود.

با این حال، برخی از برنامه‌ها ممکن است به طور صریح به متغیرهای محیطی اضافی Vergen نیاز داشته باشند. بدون تنظیم مناسب این متغیرها، ممکن است با شکست در ساخت و خطاهایی مانند زیر مواجه شوید:

```
>   cargo:rerun-if-env-changed=VERGEN_GIT_COMMIT_DATE
>   cargo:rerun-if-env-changed=VERGEN_GIT_SHA
>
>   --- stderr
>   Error: no suitable 'git' command found!
> warning: build failed, waiting for other jobs to finish...
```

در حالی که `libcosmicAppHook` متغیر `VERGEN_GIT_COMMIT_DATE` را مدیریت می‌کند، ممکن است لازم باشد متغیرهای دیگر را به‌طور صریح تنظیم کنید. برای برنامه‌هایی که به این متغیرها نیاز دارند، باید آن‌ها را مستقیماً در تعریف بسته تنظیم کنید:

```nix
{
  lib,
  rustPlatform,
  libcosmicAppHook,
}:
rustPlatform.buildRustPackage {
  # ...
  env = {
    VERGEN_GIT_COMMIT_DATE = "2025-01-01";
    VERGEN_GIT_SHA = "0000000000000000000000000000000000000000"; # SHA-1 hash of the commit
  };
  # ...
}
```

همهٔ برنامه‌های COSMIC به این متغیرها نیاز ندارند، اما برای مواردی که نیاز دارند، تنظیم صریح آن‌ها از شکست‌های ساخت جلوگیری می‌کند.
