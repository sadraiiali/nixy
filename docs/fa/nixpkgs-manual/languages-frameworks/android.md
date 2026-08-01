# Android {#android}

محیط ساخت Android سه ویژگی اصلی و تعدادی ویژگی پشتیبان ارائه می‌دهد.

## استفاده از androidenv با Android Studio {#using-androidenv-with-android-studio}

از صفت (attribute) `android-studio-full` برای یک Android SDK بسیار کامل، شامل تصاویر سیستم، استفاده کنید:

```nix
{ buildInputs = [ android-studio-full ]; }
```

این کاملاً معادل است با:

```nix
{ buildInputs = [ androidStudioPackages.stable.full ]; }
```

همچنین می‌توانید composeAndroidPackages را به passthroughِ `withSdk` پاس دهید:

```nix
{
  buildInputs = [
    (android-studio.withSdk (androidenv.composeAndroidPackages { includeNDK = true; }).androidsdk)
  ];
}
```

این موارد متغیرهای `ANDROID_HOME` و `ANDROID_NDK_ROOT` را به پوشه‌های SDK و NDK در محیط ساخت Android مشخص‌شده صادر می‌کنند.

## استقرار یک نصب Android SDK به همراه افزونه‌ها {#deploying-an-android-sdk-installation-with-plugins}

همچنین می‌توانید SDK را به‌طور جداگانه با مجموعهٔ دلخواهی از افزونه‌ها یا زیرمجموعه‌هایی از یک SDK استقرار دهید.

```nix
with import <nixpkgs> { };

let
  androidComposition = androidenv.composeAndroidPackages {
    platformVersions = [
      "34"
      "35"
      "latest"
    ];
    systemImageTypes = [ "google_apis_playstore" ];
    abiVersions = [
      "armeabi-v7a"
      "arm64-v8a"
    ];
    includeNDK = true;
    includeExtras = [ "extras;google;auto" ];
  };
in
androidComposition.androidsdk
```

فراخوانی تابع فوق مشخص می‌کند که ما یک Android SDK با نسخه‌های پلاگین تعیین‌شده در بالا می‌خواهیم. به طور پیش‌فرض، اکثر پلاگین‌ها غیرفعال هستند. استثناهای قابل توجه، زیربسته‌های tools، platform-tools و build-tools هستند.

گزینه‌های زیر پشتیبانی می‌شوند:

* `cmdLineToolsVersion` نسخه بسته `cmdline-tools` مورد استفاده را مشخص می‌کند. مقدار پیش‌فرض آن آخرین نسخه است.
* `toolsVersion` نسخه بسته `tools` را مشخص می‌کند. توجه داشته باشید که `tools` منسوخ شده است و در حال حاضر تنها نسخه `26.1.1` در دسترس است، بنابراین گزینه‌های زیادی در اینجا وجود ندارد؛ با این حال، اگر آن را نمی‌خواهید می‌توانید مقدارش را `null` قرار دهید. مقدار پیش‌فرض آن آخرین نسخه است.
* `platformToolsVersion` نسخه پلاگین `platform-tools` را مشخص می‌کند. مقدار پیش‌فرض آن آخرین نسخه است.
* `buildToolsVersions` نسخه‌های پلاگین‌های `build-tools` مورد استفاده را مشخص می‌کند. مقدار پیش‌فرض آن آخرین نسخه است.
* `includeEmulator` مشخص می‌کند که آیا بسته شبیه‌ساز استقرار یابد یا خیر (به طور پیش‌فرض `false`). در صورت فعال بودن، نسخه شبیه‌ساز برای استقرار را می‌توان با تنظیم پارامتر `emulatorVersion` مشخص کرد. اگر روی `"if-supported"` تنظیم شود، در صورت پشتیبانی سیستم، شبیه‌ساز استقرار داده می‌شود.
* `includeCmake` مشخص می‌کند که آیا CMake باید گنجانده شود یا خیر. مقدار پیش‌فرض آن روی پلتفرم‌های x86-64 و Darwin برابر با true است و از `"if-supported"` نیز پشتیبانی می‌کند.
* `cmakeVersions` مشخص می‌کند که کدام نسخه‌های CMake باید استقرار یابند. مقدار پیش‌فرض آن آخرین نسخه است.
* `includeNDK` مشخص می‌کند که باندل Android NDK باید گنجانده شود یا خیر. مقدار پیش‌فرض آن `false` است، اگرچه می‌توان آن را روی `true` یا `"if-supported"` تنظیم کرد.
* `ndkVersions` نسخه‌های NDK مورد استفاده را مشخص می‌کند. این‌ها در زیر پوشه `ndk` در ریشه SDK پیوند داده می‌شوند و اولین مورد در زیر پوشه `ndk-bundle` پیوند داده می‌شود. مقدار پیش‌فرض آن آخرین نسخه است.
* `ndkVersion` معادل مشخص کردن یک ورودی در `ndkVersions` است و در صورت ارائه، `ndkVersions` این پارامتر را بازنویسی می‌کند.
* `includeExtras` آرایه‌ای از رشته‌های شناسه است که به بسته‌های افزوده دلخواه که باید نصب شوند اشاره می‌کند. توجه داشته باشید که برنامه‌های اضافی ممکن است با همه پلتفرم‌ها سازگار نباشند (به عنوان مثال، دستگاه Google TV head unit که کامپایل aarch64-linux ندارد).
* `platformVersions` مشخص می‌کند که کدام نسخه‌های SDK پلتفرم باید گنجانده شوند. به طور پیش‌فرض تنها شامل آخرین سطح API می‌شود، اگرچه می‌توانید موارد بیشتری اضافه کنید.
* `numLatestPlatformVersions` مشخص می‌کند در صورت استفاده از مقدار پیش‌فرض برای `platformVersions`، چه تعداد از آخرین سطوح API گنجانده شوند. مقدار پیش‌فرض آن 1 است، اگرچه می‌توانید آن را مثلاً به 5 افزایش دهید تا بسته‌های API مربوط به 5 سال اخیر Android را دریافت کنید.
* `minPlatformVersion` و `maxPlatformVersion` در صورت ارائه هر دو، نسبت به `platformVersions` اولویت دارند. توجه داشته باشید که مقدار پیش‌فرض `maxPlatformVersion` همیشه آخرین نسخه پلتفرم Android SDK است، که به شما امکان می‌دهد با تعیین `minPlatformVersion` حداقل نسخه SDK پشتیبانی‌شده توسط ترکیب Android خود را توصیف کنید.

برای هر نسخه پلتفرم مشخص‌شده، می‌توانیم گزینه‌های زیر را اعمال کنیم:

* `includeSystemImages` مشخص می‌کند که آیا تصویر سیستم برای هر SDK پلتفرم باید گنجانده شود یا خیر.
* `includeSources` مشخص می‌کند که آیا کدهای منبع برای هر نسخه SDK باید گنجانده شوند یا خیر.
* `useGoogleAPIs` مشخص می‌کند که برای هر نسخه پلتفرم انتخاب‌شده، Google API باید گنجانده شود.
* `useGoogleTVAddOns` مشخص می‌کند که برای هر نسخه پلتفرم انتخاب‌شده، افزودنی Google TV باید گنجانده شود.

برای هر تصویر سیستم درخواستی می‌توانیم گزینه‌های زیر را مشخص کنیم:

* `systemImageTypes` مشخص می‌کند که چه نوع ایمیج‌های سیستمی باید شامل شوند.
  مقدار پیش‌فرض: `default`.
* `abiVersions` مشخص می‌کند که چه نوع نسخه ABI از هر ایمیج سیستم باید
  شامل شود. مقادیر پیش‌فرض `armeabi-v7a` و `arm64-v8a` هستند.

بیشتر آرگومان‌های تابع دارای تنظیمات پیش‌فرض معقولی هستند و در صورت امکان، آخرین نسخه‌های ابزارها را ترجیح می‌دهند. همچنین می‌توانید برای هر نسخه از افزونه که اهمیت خاصی برایتان ندارد و صرفاً آخرین نسخه آن را می‌خواهید، مقدار "latest" را مشخص کنید.

می‌توانید نام‌های مجوز را مشخص کنید:

* `extraLicenses` فهرستی از نام‌های مجوز است.
  می‌توانید این نام‌ها را از repo.json یا `querypackages.sh licenses` به دست آورید. اگر accept_license را روی true تنظیم کنید، مجوز SDK (`android-sdk-license`) برای شما پذیرفته می‌شود. اگر کاری مانند کار با SDKهای پیش‌نمایش انجام می‌دهید، باید `android-sdk-preview-license` یا هر مجوزی که در اینجا مربوط می‌شود را اضافه کنید.

علاوه بر این، می‌توانید مخازنی را که composeAndroidPackages از آن‌ها دریافت می‌کند بازنشانی کنید:

* `repoJson` مسیر یک فایل repo.json تولیدشده را مشخص می‌کند. می‌توانید این فایل را با اجرای `generate.sh` تولید کنید، که به نوبه خود `mkrepo.rb` را فراخوانی می‌کند.
* `repoXmls` یک مجموعه ویژگی شامل مسیرهای فایل‌های XML مخزن است. در صورت مشخص شدن، نسبت به `repoJson` اولویت دارد و یک ساخت محلی را راه‌اندازی می‌کند که بر اساس XMLهای مخزن داده‌شده، یک repo.json را در انبار Nix می‌نویسد. توجه داشته باشید که این قابلیت از import-from-derivation استفاده می‌کند.

```nix
{
  repoXmls = {
    packages = [ ./xml/repository2-1.xml ];
    images = [
      ./xml/android-sys-img2-1.xml
      ./xml/android-tv-sys-img2-1.xml
      ./xml/android-wear-sys-img2-1.xml
      ./xml/android-wear-cn-sys-img2-1.xml
      ./xml/google_apis-sys-img2-1.xml
      ./xml/google_apis_playstore-sys-img2-1.xml
    ];
    addons = [ ./xml/addon2-1.xml ];
  };
}
```

هنگام ساخت عبارت بالا با:

```bash
$ nix-build
```

Android SDK همراه با تمامی نسخه‌های مورد نظر افزونه استقرار می‌یابد.

ما همچنین می‌توانیم زیرمجموعه‌هایی از Android SDK را استقرار دهیم. برای مثال، جهت استقرار تنها بسته `platform-tools`، می‌توانید عبارت زیر را ارزیابی کنید:

```nix
with import <nixpkgs> { };

let
  androidComposition = androidenv.composeAndroidPackages {
    # ...
  };
in
androidComposition.platform-tools
```

## استفاده از ترکیب‌های از‌پیش‌تعریف‌شده بسته‌های Android {#using-predefined-android-package-compositions}

علاوه بر ترکیب دستی مجموعه‌ای از بسته‌های Android، استفاده از یک ترکیب از‌پیش‌تعریف‌شده که شامل مجموعه نسبتاً کاملی از بسته‌های Android است نیز امکان‌پذیر است:

از عبارت نیکس (Nix expression) زیر می‌توان برای استقرار کل SDK استفاده کرد:

```nix
with import <nixpkgs> { };

androidenv.androidPkgs.androidsdk
```

همچنین می‌توان تنها از یک پلاگین استفاده کرد:

```nix
with import <nixpkgs> { };

androidenv.androidPkgs.platform-tools
```

## ایجاد نمونه‌های شبیه‌ساز {#spawning-emulator-instances}

برای اهداف تست، تولید خودکار اسکریپت‌هایی که نمونه‌های شبیه‌ساز را با تمام تنظیمات پیکربندی دلخواه راه‌اندازی می‌کنند، می‌تواند بسیار کاربردی باشد.

یک اسکریپت راه‌اندازی شبیه‌ساز را می‌توان با فراخوانی تابع `emulateApp {}` پیکربندی کرد:

```nix
with import <nixpkgs> { };

androidenv.emulateApp {
  name = "emulate-MyAndroidApp";
  platformVersion = "28";
  abiVersion = "x86"; # armeabi-v7a, mips, x86_64
  systemImageType = "google_apis_playstore";
}
```

می‌توان پرچم‌های اضافی را از طریق متغیر محیطی زمان اجرا `$NIX_ANDROID_EMULATOR_FLAGS` به شبیه‌ساز Android SDK اعمال کرد.

همچنین امکان مشخص کردن یک APK برای استقرار درون شبیه‌ساز و نام‌های بسته و activity برای راه‌اندازی آن وجود دارد:

```nix
with import <nixpkgs> { };

androidenv.emulateApp {
  name = "emulate-MyAndroidApp";
  platformVersion = "24";
  abiVersion = "armeabi-v7a"; # mips, x86, x86_64
  systemImageType = "default";
  app = ./MyApp.apk;
  package = "MyApp";
  activity = "MainActivity";
}
```

علاوه بر APKهای پیش‌ساخته، می‌توانید پارامتر APK را به فراخوانی تابع `buildApp {}` که در مثال قبلی نشان داده شد نیز متصل کنید.

## نکاتی درباره متغیرهای محیطی در پروژه‌های Android {#notes-on-environment-variables-in-android-projects}

* `ANDROID_HOME` باید به Android SDK اشاره کند. در عبارت‌های Nix شما، این مقدار باید `${androidComposition.androidsdk}/libexec/android-sdk` باشد. توجه داشته باشید که `ANDROID_SDK_ROOT` منسوخ شده است، اما اگر به ابزارهایی متکی هستید که به آن نیاز دارند، می‌توانید آن را نیز صادر (export) کنید.
* اگر در حال توسعه NDK هستید، `ANDROID_NDK_ROOT` باید به Android NDK اشاره کند. در عبارت‌های Nix شما، این مقدار باید `${ANDROID_HOME}/ndk-bundle` باشد.

اگر در حال اجرای پلاگین Android Gradle هستید، باید `GRADLE_OPTS` را صادر کنید تا aapt2 را طوری بازنشانی کنید که به باینری aapt2 در انبار نیکس (Nix store) نیز اشاره کند، یا از یک محیط FHS استفاده کنید تا aapt2 بسته‌بندی‌شده بتواند اجرا شود. اگر نمی‌خواهید از یک محیط FHS استفاده کنید، چیزی مانند این باید کار کند:

```nix
let
  buildToolsVersion = "30.0.3";

  # Use buildToolsVersion when you define androidComposition
  androidComposition = <...>;
in
pkgs.mkShell rec {
  ANDROID_HOME = "${androidComposition.androidsdk}/libexec/android-sdk";
  ANDROID_NDK_ROOT = "${ANDROID_HOME}/ndk-bundle";

  # Use the same buildToolsVersion here
  GRADLE_OPTS = "-Dorg.gradle.project.android.aapt2FromMavenOverride=${ANDROID_HOME}/build-tools/${buildToolsVersion}/aapt2";
}
```

اگر از cmake استفاده می‌کنید، باید آن را در یک قلاب شل (shell hook) یا پروفایل محیطی FHS به PATH اضافه کنید.
به انتهای این مسیر شماره ساخت اضافه می‌شود، اما پیشوند آن به شکل مناسبی شامل نسخه است.
بنابراین، چیزی شبیه به این باید کافی باشد:

```nix
let
  cmakeVersion = "3.10.2";

  # Use cmakeVersion when you define androidComposition
  androidComposition = <...>;
in
pkgs.mkShell rec {
  ANDROID_HOME = "${androidComposition.androidsdk}/libexec/android-sdk";
  ANDROID_NDK_ROOT = "${ANDROID_HOME}/ndk-bundle";

  # Use the same cmakeVersion here
  shellHook = ''
    export PATH="$(echo "$ANDROID_HOME/cmake/${cmakeVersion}".*/bin):$PATH"
  '';
}
```

توجه داشته باشید که اجرای Android Studio با مقداردهی ANDROID_HOME، در صورت عدم وجود فایل `local.properties`، به‌طور خودکار این فایل را ایجاد کرده و `sdk.dir` را روی $ANDROID_HOME تنظیم می‌کند. اگر از NDK نیز استفاده می‌کنید، ممکن است لازم باشد `ndk.dir` را به این فایل اضافه کنید.

یک نمونه `shell.nix` که تمام این کارها را برای شما انجام می‌دهد در `examples/shell.nix` ارائه شده است. این shell.nix شامل یک قلاب شل (shell hook) است که local.properties را با مقادیر صحیح sdk.dir و ndk.dir بازنویسی می‌کند. این امر تضمین می‌کند که هنگام اجرای Android Studio در داخل nix-shell، پوشه‌های SDK و NDK هر دو درست باشند.

## نکاتی در مورد بهبود سازگاری build.gradle {#notes-on-improving-build.gradle-compatibility}

اطمینان حاصل کنید که buildToolsVersion و ndkVersion شما با آنچه در androidenv تعریف شده مطابقت داشته باشد. اگر از cmake استفاده می‌کنید، مطمئن شوید که نسخه تعریف‌شده برای آن نیز درست است.

در غیر این صورت، ممکن است با خطاهای مبهمی از سوی aapt2 و پلاگین Android Gradle مواجه شوید که هشدار می‌دهند به دلیل قابل نوشتن نبودن پوشه SDK، امکان نصب ابزارهای ساخت وجود ندارد.

```gradle
android {
    buildToolsVersion "30.0.3"
    ndkVersion = "22.0.7026061"
    externalNativeBuild {
        cmake {
            version "3.10.2"
        }
    }
}

```

## استعلام نسخه‌های موجود برای هر پلاگین {#querying-the-available-versions-of-each-plugin}

تمامی بسته‌های androidenv در [search.nixos.org](https://search.nixos.org) در دسترس هستند.
توجه داشته باشید که سازگاری `aarch64-linux` در حال حاضر نامنظم است، اگرچه `x86_64-linux` و `aarch64-darwin` به خوبی پشتیبانی می‌شوند. دلیل این امر آن است که تعاریف مخزن گوگل، برخی بسته‌ها را برای "همه" معماری‌ها علامت‌گذاری می‌کنند در حالی که واقعاً فقط برای `x86_64` یا `aarch64` هستند.

## به‌روزرسانی عبارت‌های تولیدشده {#updating-the-generated-expressions}

فایل repo.json از فایل‌های XML که مدیر بسته Android Studio استفاده می‌کند تولید می‌شود.
برای به‌روزرسانی عبارت‌ها، اسکریپت `update.sh` را که در زیرپوشه `pkgs/development/mobile/androidenv/` ذخیره شده است اجرا کنید:

```bash
./update.sh
```

این کار به صورت خودکار توسط اسکریپت به‌روزرسانی nixpkgs اجرا می‌شود.

## ساخت یک برنامه Android با Ant {#building-an-android-application-with-ant}

علاوه بر SDK، امکان ساخت یک پروژه Android مبتنی بر Ant و استقرار خودکار تمام پلاگین‌های Android مورد نیاز پروژه نیز وجود دارد. اکثر پروژه‌های جدیدتر Android از Gradle استفاده می‌کنند و این بخش صرفاً به دلایل تاریخی آورده شده است.

```nix
with import <nixpkgs> { };

androidenv.buildApp {
  name = "MyAndroidApp";
  src = ./myappsources;
  release = true;

  # If release is set to true, you need to specify the following parameters
  keyStore = ./keystore;
  keyAlias = "myfirstapp";
  keyStorePassword = "mykeystore";
  keyAliasPassword = "myfirstapp";

  # Any Android SDK parameters that install all the relevant plugins that a
  # build requires
  platformVersions = [ "24" ];

  # When we include the NDK, then ndk-build is invoked before Ant gets invoked
  includeNDK = true;
}
```

به غیر از پارامترهای ساخت مختص برنامه (`name`، `src`، `release` و پارامترهای keystore)، تابع `buildApp {}` از تمام پارامترهای تابعی که تابع ترکیب SDK (تابعی که در بخش قبلی نشان داده شد) پشتیبانی می‌کند، پشتیبانی می‌کند.

این تابع ساخت به‌ویژه زمانی مفید است که قصد داشته باشید از [Hydra](https://nixos.org/hydra) استفاده کنید: راهکار ادغام مداوم (CI) مبتنی بر Nix برای ساخت برنامه‌های Android. یک Android APK به عنوان یک فرآوردهٔ ساخت ارائه می‌شود و می‌توان آن را با رفتن به صفحهٔ نتیجهٔ ساخت، روی هر دستگاه Android دارای مرورگر وب نصب کرد.
