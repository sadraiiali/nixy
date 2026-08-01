# <a id="sec-pkgs-appimageTools"></a> pkgs.appimageTools

`pkgs.appimageTools` مجموعه‌ای از توابع برای استخراج و بسته‌بندی فایل‌های [AppImage](https://appimage.org/) است.
این توابع برای زمانی در نظر گرفته شده‌اند که بسته‌بندی سنتی از منبع غیرممکن باشد، یا زمان زیادی ببرد.
برای اجرای سریع یک فایل AppImage، می‌توان از `pkgs.appimage-run` نیز استفاده کرد.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> رابط برنامه‌نویسی کاربرد (API) مربوط به `appimageTools` ناپایدار است و ممکن است در آینده دستخوش تغییرات ناسازگار با نسخه‌های قبلی شود.

## <a id="ssec-pkgs-appimageTools-wrapping"></a> بسته‌بندی (Wrapping)

برای بسته‌بندی (wrap) هر AppImage از `wrapType2` استفاده کنید.
این کار یک محیط FHS شامل بسته‌های متعددی ایجاد می‌کند که [انتظار می‌رود وجود داشته باشند](https://github.com/AppImage/pkg2appimage/blob/master/excludelist) تا AppImage کار کند.
`wrapType2` انتظار آرگومانی حاوی صفت `src` و همچنین صفت `name` یا صفات `pname` و `version` را دارد.

این تابع در نهایت [`buildFHSEnv`](#sec-fhs-environments) را فراخوانی می‌کند و هر صفت (attribute) اضافی در آرگومان ورودی به `wrapType2` به آن منتقل خواهد شد.
این بدان معناست که برای مثال می‌توانید صفت `extraInstallCommands` را ارسال کنید و همان تأثیری را خواهد داشت که در [`buildFHSEnv`](#sec-fhs-environments) توصیف شده است.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> در گذشته، `appimageTools` هر دو تابع `wrapType1` و `wrapType2` را ارائه می‌داد تا بسته به نوع AppImage که بسته‌بندی می‌شد استفاده شوند.
> با این حال، [این دو در اوایل سال ۲۰۲۰ یکپارچه شدند](https://github.com/NixOS/nixpkgs/pull/81833)، به این معنی که اکنون هر دو تابع `wrapType1` و `wrapType2` رفتار یکسانی دارند.

<a id="ex-wrapping-appimage-from-github"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # بسته‌بندی یک AppImage از GitHub
>

> ```nix
> { appimageTools, fetchurl }:
> appimageTools.wrapType2 {
>   pname = "nuclear";
>   version = "0.6.30";
>
>   src = fetchurl {
>     url = "https://github.com/nukeop/nuclear/releases/download/v${version}/nuclear-v${version}.AppImage";
>     hash = "sha256-he1uGC1M/nFcKpMM9JKY4oeexJcnzV0ZRxhTjtJz6xw=";
>   };
> }
> ```

آرگومان ارسال‌شده به `wrapType2` همچنین می‌تواند شامل صفت (attribute) `extraPkgs` باشد، که به شما اجازه می‌دهد بسته‌های اضافی را درون محیط FHS که AppImage شما در آن اجرا خواهد شد قرار دهید.
`extraPkgs` باید تابعی باشد که لیستی از بسته‌ها را برمی‌گرداند.
چند روش برای یافتن وابستگی‌های مورد نیاز یک برنامه وجود دارد:

  - بررسی فایل‌های استخراج‌شده AppImage، خواندن اسکریپت‌های آن و اجرای `patchelf` و `ldd` روی فایل‌های اجرایی آن.
    این کار همچنین در `appimage-run` با تنظیم `APPIMAGE_DEBUG_EXEC=bash` امکان‌پذیر است.
  - اجرای `strace -vfefile` روی فایل اجرایی پوشش‌داده‌شده و پیدا کردن کتابخانه‌هایی که یافت نمی‌شوند.

<a id="ex-wrapping-appimage-with-extrapkgs"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # پوشش‌دهی یک AppImage با بسته‌های اضافی
>

> ```nix
> { appimageTools, fetchurl }:
> appimageTools.wrapType2 {
>   pname = "irccloud";
>   version = "0.16.0";
>
>   src = fetchurl {
>     url = "https://github.com/irccloud/irccloud-desktop/releases/download/v${version}/IRCCloud-${version}-linux-x86_64.AppImage";
>     hash = "sha256-/hMPvYdnVB1XjKgU2v47HnVvW4+uC3rhRjbucqin4iI=";
>   };
>
>   extraPkgs = pkgs: [ pkgs.at-spi2-core ];
> }
> ```

## <a id="ssec-pkgs-appimageTools-extracting"></a> استخراج

اگر نیاز به استخراج محتویات یک AppImage دارید، از `extract` استفاده کنید.
این تابع معمولاً در Nixpkgs برای نصب فایل‌های اضافی، علاوه بر [پوشش‌دهی (wrapping)](#ssec-pkgs-appimageTools-wrapping) AppImage، استفاده می‌شود.
`extract` به آرگومانی با صفت (attribute) `src` و همچنین صفت `name` یا صفات `pname` و `version` نیاز دارد.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> در گذشته، `appimageTools` هر دو تابع `extractType1` و `extractType2` را ارائه می‌داد تا بسته به نوع AppImage در حال استخراج استفاده شوند.
> با این حال، [آن‌ها در اوایل سال ۲۰۲۰ یکپارچه شدند](https://github.com/NixOS/nixpkgs/pull/81572)، به این معنی که در حال حاضر هر دو تابع `extractType1` و `extractType2` رفتاری کاملاً مشابه `extract` دارند.

<a id="ex-extracting-appimage"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استخراج یک AppImage برای نصب فایل‌های اضافی
>
> `wrapType2` به‌طور خودکار AppImage را برای شما استخراج کرده و آن را از طریق صفت `contents` در دسترس قرار می‌دهد.
> توجه کنید که چگونه از `finalAttrs.contents` در `extraInstallCommands` برای نصب فایل‌های اضافی استخراج‌شده از AppImage استفاده شده است.
>

> ```nix
> { appimageTools, fetchurl }:
> appimageTools.wrapType2 (finalAttrs: {
>   pname = "irccloud";
>   version = "0.16.0";
>
>   src = fetchurl {
>     url = "https://github.com/irccloud/irccloud-desktop/releases/download/v${version}/IRCCloud-${version}-linux-x86_64.AppImage";
>     hash = "sha256-/hMPvYdnVB1XjKgU2v47HnVvW4+uC3rhRjbucqin4iI=";
>   };
>
>   extraPkgs = pkgs: [ pkgs.at-spi2-core ];
>
>   extraInstallCommands = ''
>     mv $out/bin/irccloud-${version} $out/bin/irccloud
>     install -m 444 -D ${finalAttrs.contents}/irccloud.desktop $out/share/applications/irccloud.desktop
>     install -m 444 -D ${finalAttrs.contents}/usr/share/icons/hicolor/512x512/apps/irccloud.png \
>       $out/share/icons/hicolor/512x512/apps/irccloud.png
>     substituteInPlace $out/share/applications/irccloud.desktop \
>       --replace-fail 'Exec=AppRun' 'Exec=irccloud'
>   '';
> })
> ```

`appimageTools` همچنین تابع `extract` را در صورتی که نیاز به انجام دستی آن داشته باشید ارائه می‌دهد، که نیازمند آرگومان‌های `pname`، `version` و `src` است (`src` همان فایل AppImage برای استخراج است).

آرگومان‌های ارسال‌شده به `extract` می‌توانند شامل یک صفت (attribute) به نام `postExtract` نیز باشند که به شما اجازه می‌دهد پس از استخراج فایل‌ها از AppImage، دستورات تکمیلی را اجرا کنید.
`postExtract` باید یک رشته حاوی دستورات جهت اجرا باشد.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> هنگام تعیین `postExtract`، باید به جای `appimageTools.wrapType2` از `appimageTools.wrapAppImage` استفاده کنید.
> در غیر این صورت، `wrapType2` محتوای AppImage را بدون رعایت دستورالعمل‌های `postExtract` استخراج خواهد کرد.

<a id="ex-extracting-appimage-with-postextract"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استخراج یک AppImage برای نصب فایل‌های اضافی، با استفاده از `postExtract`
>
> این یک بازنویسی از [](#ex-extracting-appimage) برای استفاده از `postExtract` و `wrapAppImage` است.
>

> ```nix
> { appimageTools, fetchurl }:
> appimageTools.wrapAppImage (finalAttrs: {
>   pname = "irccloud";
>   version = "0.16.0";
>
>   src = fetchurl {
>     url = "https://github.com/irccloud/irccloud-desktop/releases/download/v${version}/IRCCloud-${version}-linux-x86_64.AppImage";
>     hash = "sha256-/hMPvYdnVB1XjKgU2v47HnVvW4+uC3rhRjbucqin4iI=";
>   };
>
>   contents = appimageTools.extract {
>     inherit (finalAttrs) pname version src;
>     postExtract = ''
>       substituteInPlace $out/irccloud.desktop --replace-fail 'Exec=AppRun' 'Exec=irccloud'
>     '';
>   };
>
>   extraPkgs = pkgs: [ pkgs.at-spi2-core ];
>
>   extraInstallCommands = ''
>     mv $out/bin/irccloud-${version} $out/bin/irccloud
>     install -m 444 -D ${finalAttrs.contents}/irccloud.desktop $out/share/applications/irccloud.desktop
>     install -m 444 -D ${finalAttrs.contents}/usr/share/icons/hicolor/512x512/apps/irccloud.png \
>       $out/share/icons/hicolor/512x512/apps/irccloud.png
>   '';
> })
> ```
