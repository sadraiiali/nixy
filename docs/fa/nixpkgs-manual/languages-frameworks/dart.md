# Dart {#sec-language-dart}

## برنامه‌های Dart {#ssec-dart-applications}

تابع `buildDartApplication` برنامه‌های Dart مدیریت‌شده با pub را می‌سازد.

این تابع وابستگی‌های Dart خود را به صورت خودکار از طریق `pub2nix` دریافت می‌کند، و (از طریق مجموعه‌ای از قلاب‌ها) فایل‌های اجرایی مشخص‌شده در فایل pubspec را ساخته و نصب می‌کند. این قلاب‌ها در صورت نیاز می‌توانند در درایویشن‌های دیگر نیز استفاده شوند. فازها نیز می‌توانند بازنشانی شوند تا کاری متفاوت از نصب باینری‌ها انجام دهند.

اگر در حال بسته‌بندی یک برنامه دسکتاپ Flutter هستید، به جای آن از [`buildFlutterApplication`](#ssec-dart-flutter) استفاده کنید.

`pubspecLock` همان فایل تجزیه‌شده‌ی pubspec.lock است. pub2nix از آن برای دانلود بسته‌های مورد نیاز استفاده می‌کند.
این فایل را می‌توان با چیزی مانند `yq . pubspec.lock` از YAML به JSON تبدیل کرد و سپس توسط Nix خواند.

به عنوان جایگزین، می‌توان از `autoPubspecLock` استفاده کرد و آن را روی مسیر یک فایل معمولی `pubspec.lock` تنظیم نمود. این روش به import-from-derivation متکی است و در Nixpkgs مجاز نیست، اما در مواقع دیگر می‌تواند مفید باشد.

::: {.warning}
هنگام استفاده از `autoPubspecLock` با یک پوشه‌ی کد منبع محلی، مطمئن شوید که از عملگر الحاق (مانند `autoPubspecLock = src + "/pubspec.lock";`) استفاده می‌کنید و نه درون‌گذاری رشته.

درون‌گذاری رشته تمام پوشه‌ی کد منبع شما را در انبار نیکس (Nix store) کپی کرده و از مسیر انبار آن استفاده می‌کند؛ بدین معنا که تغییرات غیرمرتبط در درخت کد منبع شما باعث بازسازی درایویشن تولیدشده‌ی `pubspec.lock` خواهد شد!
:::

اگر بسته دارای وابستگی‌های بسته‌ای Git باشد، هش‌ها باید در مجموعه `gitHashes` ارائه شوند. اگر هشی موجود نباشد، پیام خطایی مبنی بر افزودن آن به شما نشان داده خواهد شد.

دستورات اجرای `dart` را می‌توان از طریق `pubGetScript` و `dartCompileCommand` بازنشانی کرد؛ همچنین می‌توانید با استفاده از `dartCompileFlags` یا `dartJitFlags` پرچم‌ها را اضافه کنید.

Dart از چند [نوع خروجی](https://dart.dev/tools/dart-compile#types-of-output) پشتیبانی می‌کند؛ شما می‌توانید با استفاده از `dartOutputType` (پیش‌فرض `exe`) بین آن‌ها انتخاب کنید. اگر می‌خواهید مسیر باینری‌ها یا مسیر کد منبعی که از آن می‌آیند را بازنشانی کنید، می‌توانید از `dartEntryPoints` استفاده کنید. خروجی‌هایی که به زمان اجرا نیاز دارند به صورت خودکار با زمان اجرای مربوطه پوشش داده می‌شوند (`dartaotruntime` برای `aot-snapshot`، دستور `dart run` برای `jit-snapshot` و `kernel`، و `node` برای `js`)؛ این رفتار را می‌توان از طریق `dartRuntimeCommand` بازنشانی کرد.

```nix
{
  lib,
  buildDartApplication,
  fetchFromGitHub,
}:

buildDartApplication (finalAttrs: {
  pname = "dart-sass";
  version = "1.62.1";

  src = fetchFromGitHub {
    owner = "sass";
    repo = "dart-sass";
    tag = finalAttrs.version;
    hash = "sha256-U6enz8yJcc4Wf8m54eYIAnVg/jsGi247Wy8lp1r1wg4=";
  };

  pubspecLock = lib.importJSON ./pubspec.lock.json;
})
```

### پچ کردن وابستگی‌ها {#ssec-dart-applications-patching-dependencies}

برخی بسته‌های Dart به پچ‌ها یا تغییرات محیط ساخت نیاز دارند. درایویشن‌های بسته را می‌توان با آرگومان `customSourceBuilders` سفارشی‌سازی کرد.

مجموعه‌ای از این سفارشی‌سازی‌ها را می‌توان در Nixpkgs، در پوشه `development/compilers/dart/package-source-builders` یافت.

این امر امکان به اشتراک‌گذاری اصلاحات بسته‌ها را بین تمام برنامه‌هایی که از آن‌ها استفاده می‌کنند فراهم می‌کند. اکیداً توصیه می‌شود به جای گنجاندن اصلاحات در خود derivation برنامه، آن‌ها را به این مجموعه اضافه کنید.

### اجرای برنامه‌های اجرایی از dev_dependencies {#ssec-dart-applications-build-tools}

بسیاری از برنامه‌های Dart به اجرای برنامه‌های اجرایی بخش `dev_dependencies` در `pubspec.yaml` پیش از ساخت نیاز دارند.

این کار را می‌توان در `preBuild` به یکی از دو روش انجام داد:

1. بسته‌بندی ابزار با `buildDartApplication`، افزودن آن به Nixpkgs و اجرای آن مانند هر برنامه دیگر
2. اجرای ابزار از کش بسته

از میان این روش‌ها، روش اول زمانی توصیه می‌شود که از ابزاری استفاده می‌کنید که نیازی به داشتن یک نسخه خاص ندارد.

برای روش دوم، می‌توان از تابع `packageRun` موجود در `dartConfigHook` استفاده کرد.
این یک جایگزین برای `dart run` است که به Pub متکی نیست.

به عنوان مثال، برای `build_runner`:

```bash
packageRun build_runner build
```

از `dart run <package_name>` استفاده _نکنید_، زیرا این کار سعی خواهد کرد وابستگی‌ها را با Pub دانلود کند.

### استفاده با nix-shell {#ssec-dart-applications-nix-shell}

#### استفاده از وابستگی‌ها از انبار نیکس (Nix store) {#ssec-dart-applications-nix-shell-deps}

از آنجا که `buildDartApplication` به جای `pub get` وابستگی‌ها را تأمین می‌کند، باید به صراحت به Dart گفته شود که آن‌ها را کجا پیدا کند.

دستورات زیر را در پوشه کد منبع اجرا کنید تا Dart را به شکل مناسبی پیکربندی کنید.
پس از انجام این کار از `pub` استفاده نکنید؛ زیرا خودش وابستگی‌ها را بارگیری کرده و این تغییرات را بازنویسی خواهد کرد.

```bash
cp --no-preserve=all "$pubspecLockFilePath" pubspec.lock
mkdir -p .dart_tool && cp --no-preserve=all "$packageConfig" .dart_tool/package_config.json
```

## برنامه‌های Flutter {#ssec-dart-flutter}

تابع `buildFlutterApplication` برنامه‌های Flutter را می‌سازد.

برای جزئیات بیشتر در مورد فایل‌ها و آرگومان‌های مورد نیاز، [مستندات Dart](#ssec-dart-applications) را ببینید.

`flutter` در Nixpkgs همیشه به `flutterPackages.stable` اشاره دارد که آخرین نسخه‌ی بسته‌بندی‌شده‌است. برای جلوگیری از خرابی‌های پیش‌بینی‌نشده در زمان ارتقا، بسته‌ها در Nixpkgs باید به جای استفاده مستقیم از `flutter`، از نسخه‌ی مشخصی از flutter مانند `flutter335` و `flutter338` استفاده کنند.

```nix
{ flutter335, fetchFromGitHub }:

flutter335.buildFlutterApplication (finalAttrs: {
  pname = "firmware-updater";
  version = "0-unstable-2025-09-09";

  # To build for the Web, use the targetFlutterPlatform argument.
  # targetFlutterPlatform = "web";

  src = fetchFromGitHub {
    owner = "canonical";
    repo = "firmware-updater";
    rev = "402e97254b9d63c8d962c46724995e377ff922c8";
    hash = "sha256-nQn5mlgNj157h++67+mhez/F1ALz4yY+bxiGsi0/xX8=";
    fetchSubmodules = true;
  };

  pubspecLock = lib.importJSON ./pubspec.lock.json;

  sourceRoot = "${finalAttrs.src.name}/apps/firmware_updater";

  gitHashes.fwupd = "sha256-l/+HrrJk1mE2Mrau+NmoQ7bu9qhHU6wX68+m++9Hjd4=";
})
```

### استفاده به همراه nix-shell {#ssec-dart-flutter-nix-shell}

نکات استفاده از `nix-shell` مختص Flutter در این بخش آورده شده‌است. برای دستورالعمل‌های عمومی `nix-shell` به [مستندات Dart](#ssec-dart-applications-nix-shell) مراجعه کنید.

#### ورود به شل {#ssec-dart-flutter-nix-shell-enter}

به‌صورت پیش‌فرض، تنها وابستگی‌های مربوط به `targetFlutterPlatform` در محیط ساخت در دسترس هستند. این موضوع برای کوچک نگه داشتن closureها مفید است اما می‌تواند در طول توسعه مشکل‌ساز شود. به عنوان مثال، ساخت برنامه‌های وب برای Linux در طول توسعه جهت بهره‌مندی از ویژگی‌های بومی مانند بارگذاری مجدد سریع با حفظ وضعیت (stateful hot reload) رایج است.

برای ورود به شلی که تمام پلتفرم‌های هدف معمول در آن در دسترس باشند، از صفت (attribute) `multiShell` استفاده کنید.

به عنوان مثال: `nix-shell '<nixpkgs>' -A fluffychat-web.multiShell`.
