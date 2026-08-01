# <a id="ios"></a> iOS

این کامپوننت در اصل یک غلاف (wrapper) / راه‌کار دور زدن است که امکان در دسترس قرار دادن یک نصب Xcode را به‌عنوان یک بسته Nix از طریق ایجاد پیوندهای نمادین به فایل‌های اجرایی مربوطه روی سیستم میزبان فراهم می‌کند.

از آنجا که Xcode را نمی‌توان با Nix بسته‌بندی کرد و همچنین نمی‌توانیم آن را به‌عنوان یک بسته Nix (به دلیل مجوز آن) منتشر کنیم، این در واقع تنها استراتژی یکپارچه‌سازی است که امکان انجام ساخت‌های برنامه iOS را که با سایر کامپوننت‌های بوم‌

```nix
let
  pkgs = import <nixpkgs> { };

  xcodeenv = import ./xcodeenv { inherit (pkgs) stdenv; };
in
xcodeenv.composeXcodeWrapper {
  version = "9.2";
  xcodeBaseDir = "/Applications/Xcode.app";
}
```

با استقرار عبارت بالا با `nix-build` و بررسی محتوای آن، متوجه خواهید شد که چندین فایل اجرایی مرتبط با Xcode به عنوان یک بسته Nix ارائه شده‌اند:

```bash
$ ls result/bin
lrwxr-xr-x  1 sander  staff  94  1 jan  1970 Simulator -> /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app/Contents/MacOS/Simulator
lrwxr-xr-x  1 sander  staff  17  1 jan  1970 codesign -> /usr/bin/codesign
lrwxr-xr-x  1 sander  staff  17  1 jan  1970 security -> /usr/bin/security
lrwxr-xr-x  1 sander  staff  21  1 jan  1970 xcode-select -> /usr/bin/xcode-select
lrwxr-xr-x  1 sander  staff  61  1 jan  1970 xcodebuild -> /Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild
lrwxr-xr-x  1 sander  staff  14  1 jan  1970 xcrun -> /usr/bin/xcrun
```

## <a id="building-an-ios-application"></a> ساخت یک برنامه iOS

ما می‌توانیم با اجرای تابع `xcodeenv.buildApp {'{'}'{'{'}'{'}'}{'{'}'{'}'}'{'}'}` یک فایل اجرایی برنامه iOS برای شبیه‌ساز، یا یک فایل IPA/xcarchive برای اهداف انتشار (مانند نصب‌های ad-hoc، سازمانی یا فروشگاهی) بسازیم:

```nix
let
  pkgs = import <nixpkgs> { };

  xcodeenv = import ./xcodeenv { inherit (pkgs) stdenv; };
in
xcodeenv.buildApp {
  name = "MyApp";
  src = ./myappsources;
  sdkVersion = "11.2";

  target = null; # Corresponds to the name of the app by default
  configuration = null; # Release for release builds, Debug for debug builds
  scheme = null; # -scheme will correspond to the app name by default
  sdk = null; # null will set it to 'iphonesimulator` for simulator builds or `iphoneos` to real builds
  xcodeFlags = "";

  release = true;
  certificateFile = ./mycertificate.p12;
  certificatePassword = "secret";
  provisioningProfile = ./myprovisioning.profile;
  signMethod = "ad-hoc"; # 'enterprise' or 'store'
  generateIPA = true;
  generateXCArchive = false;

  enableWirelessDistribution = true;
  installURL = "/installipa.php";
  bundleId = "mycompany.myapp";
  appVersion = "1.0";

  # Supports all xcodewrapper parameters as well
  xcodeBaseDir = "/Applications/Xcode.app";
}
```

تابع فوق پارامترهای مختلفی می‌پذیرد:

* پارامترهای `name` و `src` اجباری هستند و نام برنامه و مکانی که کد منبع در آن قرار دارد را مشخص می‌کنند.
* `sdkVersion` مشخص می‌کند از کدام نسخه iOS SDK استفاده شود.

همچنین تنظیم پارامترهای `xcodebuild` امکان‌پذیر است. این کار تنها در شرایط نادر مورد نیاز است. در بیشتر موارد مقادیر پیش‌فرض باید کافی باشد:

* `target` مشخص می‌کند کدام تارگت `xcodebuild` برای ساخت انتخاب شود. به طور پیش‌فرض تارگتی را می‌گیرد که هم‌نام با برنامه است.
* پارامتر `configuration` در صورت تمایل قابل بازنشانی است. به طور پیش‌فرض، یک ساخت دیباگ برای شبیه‌ساز و یک ساخت انتشار برای دستگاه‌های واقعی انجام می‌دهد.
* پارامتر `scheme` مشخص می‌کند

```nix
let
  pkgs = import <nixpkgs> { };

  xcodeenv = import ./xcodeenv { inherit (pkgs) stdenv; };
in
xcode.simulateApp {
  name = "simulate";

  # Supports all xcodewrapper parameters as well
  xcodeBaseDir = "/Applications/Xcode.app";
}
```

عبارت بالا اسکریپتی تولید می‌کند که شبیه‌ساز را از نصب Xcode ارائه‌شده راه‌اندازی می‌کند. این اسکریپت را می‌توان به صورت زیر اجرا کرد:

```bash
./result/bin/run-test-simulator
```

به‌طور پیش‌فرض، اسکریپت نمای کلی از UDID را برای تمام نمونه‌های شبیه‌ساز در دسترس نشان می‌دهد و از شما می‌خواهد یکی را انتخاب کنید. همچنین می‌توانید یک UDID را به‌عنوان پارامتر خط فرمان ارائه دهید تا یک نمونه به‌طور خودکار راه‌اندازی شود:

```bash
./result/bin/run-test-simulator 5C93129D-CF39-4B1A-955F-15180C3BD4B8
```

همچنین می‌توانید اسکریپت شبیه‌ساز را گسترش دهید تا به‌طور خودکار یک برنامه را در نمونه شبیه‌ساز درخواستی استقرار داده و راه‌اندازی کند:

```nix
let
  pkgs = import <nixpkgs> { };

  xcodeenv = import ./xcodeenv { inherit (pkgs) stdenv; };
in
xcode.simulateApp {
  name = "simulate";
  bundleId = "mycompany.myapp";
  app = xcode.buildApp {
    # ...
  };

  # Supports all xcodewrapper parameters as well
  xcodeBaseDir = "/Applications/Xcode.app";
}
```

با ارائهٔ نتیجهٔ تابع `xcode.buildApp {'{'}'{'{'}'{'}'}{'{'}'{'}'}'{'}'}` و پیکربندی شناسهٔ app bundle، برنامه به صورت خودکار استقرار یافته و اجرا می‌شود.

```bash
$ rm -rf ~/Library/Developer/Xcode/DerivedData
```
