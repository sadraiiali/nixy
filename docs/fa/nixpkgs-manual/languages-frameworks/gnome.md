# GNOME {#sec-language-gnome}

## بسته‌بندی برنامه‌های GNOME {#ssec-gnome-packaging}

برنامه‌ها در دنیای GNOME به زبان‌های مختلفی نوشته شده‌اند، اما همگی از کتابخانه‌های مبتنی بر GObject مانند GLib، GTK یا GStreamer استفاده می‌کنند. این کتابخانه‌ها غالباً ماژولار هستند و برای یافتن ماژول‌های خود به جستجو در پوشه‌های خاصی متکی هستند. با این حال، به دلیل سازمان‌دهی خاص سیستم‌فایل در Nix، این کار بدون مداخله‌ی ما با شکست مواجه خواهد شد. خوشبختانه، این کتابخانه‌ها معمولاً اجازه می‌دهند که پوشه‌ها از طریق متغیرهای محیطی بازنویسی شوند، چه به‌صورت نیتیو و چه به لطف یک پچ در nixpkgs. [کپسوله‌سازی (Wrapping)](#fun-wrapProgram) فایل‌های اجرایی برای اطمینان از اینکه مسیرهای درست در دسترس برنامه هستند، بخش عمده‌ای از بسته‌بندی یک برنامه دسکتاپ مدرن را تشکیل می‌دهد. در این بخش، ماژول‌های مختلف مورد نیاز چنین برنامه‌هایی، متغیرهای محیطی لازم برای بارگذاری ماژول‌ها، و در نهایت اسکریپتی را که این کار را برای ما انجام می‌دهد، توصیف خواهیم کرد.

### تنظیمات {#ssec-gnome-settings}

[رابط برنامه‌نویسی کاربرد (API) GSettings](https://developer.gnome.org/gio/stable/GSettings.html) اغلب برای ذخیره تنظیمات استفاده می‌شود. طرح‌واره‌های (schemas) GSettings برای دانستن نوع و سایر متاداده‌های مقادیر ذخیره‌شده مورد نیاز هستند. GLib به دنبال فایل‌های `glib-2.0/schemas/gschemas.compiled` در داخل پوشه‌های `XDG_DATA_DIRS` می‌گردد.

در Linux، رابط برنامه‌نویسی کاربرد (API) GSettings با استفاده از بخشسمت سرور (Backend) [dconf](https://gitlab.gnome.org/GNOME/dconf) پیاده‌سازی شده است. شما باید [ماژول GIO](#ssec-gnome-gio-modules) متعلق به `dconf` را به متغیر `GIO_EXTRA_MODULES` اضافه کنید، در غیر این صورت بخشسمت سرور (Backend) `memory` استفاده خواهد شد و تنظیمات ذخیره‌شده ماندگار نخواهند بود.

در نهایت به خود سرویس D-Bus دیتابیس dconf نیاز خواهید داشت. می‌توانید آن را با استفاده از `programs.dconf.enable` فعال کنید.

برخی برنامه‌ها نیز برای مواردی مانند خواندن پیکربندی پروکسی یا سفارشی‌سازی رابط کاربری به `gsettings-desktop-schemas` نیاز دارند. این وابستگی اغلب توسط توسعه‌دهندگان بالادستی ذکر نمی‌شود؛ باید `org.gnome.desktop` و `org.gnome.system` را grep کنید تا ببینید آیا به این طرح‌واره‌ها نیاز است یا خیر.

### ماژول‌های GIO {#ssec-gnome-gio-modules}

کتابخانه [GIO](https://developer.gnome.org/gio/stable/ch01.html) در GLib از چند [نقطه توسعه](https://developer.gnome.org/gio/stable/extending-gio.html) پشتیبانی می‌کند. به‌طور ویژه، آن‌ها امکانات زیر را فراهم می‌کنند:

* پیاده‌سازی بخشسمت سرور (Backend)های تنظیمات (که قبلاً [ذکر شد](#ssec-gnome-settings))
* افزودن پشتیبانی از TLS
* تنظیمات پروکسی
* سیستم‌های فایل مجازی

ماژول‌ها معمولاً در پوشه `lib/gio/modules/` یک بسته نصب می‌شوند و اگر به هر یک از این ویژگی‌ها نیاز دارید، باید آن‌ها را به `GIO_EXTRA_MODULES` اضافه کنید.

به‌طور خاص، توصیه می‌کنیم:

* افزودن `dconf.lib` برای هر نرم‌افزاری در Linux که [GSettings](#ssec-gnome-settings) را می‌خواند (حتی به‌صورت متعدی از طریق مثلاً مدیر فایل GTK)
* افزودن `glib-networking` برای هر نرم‌افزاری که با استفاده از GIO یا libsoup به شبکه دسترسی پیدا می‌کند – glib-networking شامل ماژولی است که پشتیبانی از TLS را پیاده‌سازی کرده و تنظیمات پروکسی سرتاسر سیستم را بارگذاری می‌کند

برای اجازه دادن به نرم‌افزار جهت استفاده از سیستم‌های فایل مجازی مختلف، بسته `gvfs` نیز می‌تواند اضافه شود. اما این معمولاً یک ویژگی اختیاری است، بنابراین ما به‌طور معمول از `gvfs` موجود در سیستم استفاده می‌کنیم (مثلاً نصب‌شده به‌صورت سراسری با استفاده از ماژول‌های NixOS).

### بارگذارکننده‌های GdkPixbuf {#ssec-gnome-gdk-pixbuf-loaders}

برنامه‌های GTK معمولاً از [GdkPixbuf](https://gitlab.gnome.org/GNOME/gdk-pixbuf/) برای بارگیری تصاویر استفاده می‌کنند. اما بسته `gdk-pixbuf` تنها از فرمت‌های بیت‌مپ پایه‌ای مانند JPEG، PNG یا TIFF پشتیبانی می‌کند و برای سایر فرمت‌ها به استفاده از ماژول‌های بارگذار شخص ثالث نیاز دارد. این امر به‌ویژه دشوار است زیرا خود GTK شامل آیکون‌های SVG است که بدون بارگذار ارائه‌شده توسط `librsvg` قابل رندر نیستند.

برخلاف سایر کتابخانه‌های ذکرشده در این بخش، GdkPixbuf تنها از یک مقدار واحد در متغیر محیطی کنترل‌کننده خود یعنی `GDK_PIXBUF_MODULE_FILE` پشتیبانی می‌کند. قرار است این متغیر به یک فایل کش اشاره کند که حاوی اطلاعاتی درباره بارگذارهای موجود است. هر بسته بارگذار شامل یک فایل `lib/gdk-pixbuf-2.0/2.10.0/loaders.cache` خواهد بود که بارگذارهای پیش‌فرض در بسته `gdk-pixbuf` به همراه بارگذار موجود در خود بسته را توصیف می‌کند. اگر می‌خواهید از چندین بارگذار شخص ثالث استفاده کنید، باید فایل کش خود را به صورت دستی ایجاد کنید. خوشبختانه، این مورد بسیار نادر است زیرا [بارگذارهای زیادی وجود ندارند](https://gitlab.gnome.org/federico/gdk-pixbuf-survey/blob/master/src/modules.md).

بسته `gdk-pixbuf` حاوی [یک setup hook](#ssec-gnome-hooks-gdk-pixbuf) است که `GDK_PIXBUF_MODULE_FILE` را از وابستگی‌ها تنظیم می‌کند، اما همان‌طور که در بخش‌های بعدی اشاره شده، بسیار محدود است. بارگذارها باید این setup hook را انتشار دهند.

### آیکون‌ها {#ssec-gnome-icons}

وقتی یک برنامه از آیکون‌ها استفاده می‌کند، باید یک تم آیکون در طول زمان اجرا در `XDG_DATA_DIRS` در دسترس باشد. بسته تم پیش‌فرض و بدون آیکون [hicolor-icon-theme](https://www.freedesktop.org/wiki/Software/icon-theme/) (که باید توسط هر تم آیکونی انتشار یابد) حاوی [یک setup hook](#ssec-gnome-hooks-hicolor-icon-theme) است که تم‌های آیکون را از ورودی‌های ساخت (buildInputs) جمع‌آوری کرده و مسیر داده‌های آن‌ها را به متغیر محیطی `XDG_ICON_DIRS` اضافه می‌کند (این متغیر مخصوص Nixpkgs است و در واقع یک متغیر استاندارد XDG نیست). متأسفانه، اتکا به این روش به این معنی است که هر کاربر فارغ از ترجیح خود مجبور به دانلود تم شامل‌شده در عبارت بسته خواهد بود. به همین دلیل، ما نصب تم آیکون را به عهده کاربر می‌گذاریم. اگر از یکی از محیط‌های دسکتاپ استفاده می‌کنید، احتمالاً از قبل یک تم آیکون نصب کرده‌اید.

در موارد نادری که نیاز به استفاده از آیکون‌های موجود در وابستگی‌ها دارید (به عنوان مثال، زمانی که یک برنامه استفاده از یک تم آیکون خاص را اجبار می‌کند)، می‌توانید از موارد زیر برای جمع‌آوری آن‌ها استفاده کنید:

```nix
{
  buildInputs = [ pantheon.elementary-icon-theme ];
  preFixup = ''
    gappsWrapperArgs+=(
      # The icon theme is hardcoded.
      --prefix XDG_DATA_DIRS : "$XDG_ICON_DIRS"
    )
  '';
}
```

برای جلوگیری از دسترسی پرهزینه به سیستم‌فایل هنگام یافتن آیکون‌ها، GTK و [همچنین Qt](https://woboq.com/blog/qicon-reads-gtk-icon-cache-in-qt57.html) می‌توانند به فایل‌های `icon-theme.cache` از پوشه‌های سطح بالایی تم‌ها اتکا کنند. این فایل‌ها با استفاده از `gtk-update-icon-cache` تولید می‌شوند، که انتظار می‌رود هر زمان آیکونی به یک تم آیکون اضافه یا از آن حذف می‌شود (معمولاً یک آیکون برنامه در تم `hicolor`) اجرا شود و برخی برنامه‌ها واقعاً پس از نصب آیکون این کار را انجام می‌دهند. با این حال، از آنجا که بسته‌ها توسط Nix در پیشوند اختصاصی خود نصب می‌شوند، این امر منجر به تداخل می‌شود. به همین دلیل، `gtk3` یک [setup hook](#ssec-gnome-hooks-gtk-drop-icon-theme-cache) ارائه می‌دهد که فایل را از فرایند نصب پاک می‌کند. از آنجا که اکثر برنامه‌ها فقط آیکون اختصاصی خود را ارائه می‌دهند که هنگام راه‌اندازی بارگذاری می‌شود، این موضوع نباید تاثیر چندانی بر آن‌ها بگذارد. از طرف دیگر، تم‌های آیکون بسیار بزرگ‌تر و گسترده‌تر استفاده می‌شوند، بنابراین ما باید آن‌ها را کش کنیم. از آنجا که توصیه می‌کنیم تم‌های آیکون را به‌صورت سراسری نصب کنید، فایل‌های کش را از تمام بسته‌های موجود در یک پروفایل با استفاده از یک ماژول NixOS تولید خواهیم کرد. اگر محیط دسکتاپ شما این کار را انجام نمی‌دهد، می‌توانید تولید کش را با استفاده از گزینه `gtk.iconCache.enable` فعال کنید.

### بسته‌بندی تم‌های آیکون {#ssec-icon-theme-packaging}

تم‌های آیکون ممکن است از تم‌های آیکون دیگر ارث‌بری کنند. این ارث‌بری با استفاده از کلید `Inherits` در فایل `index.theme` که همراه با تم آیکون توزیع می‌شود، مشخص می‌گردد. طبق [مشخصات تم آیکون](https://specifications.freedesktop.org/icon-theme-spec/latest)، آیکون‌هایی که توسط تم ارائه نشده‌اند، در تم‌های آیکون والدی آن جستجو می‌شوند. بنابراین تم‌های والد باید به عنوان وابستگی نصب شوند تا تجربه کامل‌تری نسبت به مجموعه‌های آیکون مورد استفاده حاصل شود.

بسته `hicolor-icon-theme` یک setup hook ارائه می‌دهد که پیوندهای نمادین (symlinks) برای تم‌های والد در پوشه `share/icons` از پوشه تم فعلی در انبار نیکس (Nix store) ایجاد می‌کند و اطمینان حاصل می‌کند که آن‌ها در زمان اجرا قابل یافتن هستند. برای اینکه این امر کار کند، بسته‌های ارائه‌دهنده تم‌های آیکون والد باید همراه با `hicolor-icon-theme` به عنوان وابستگی‌های ساخت منتشریافته فهرست شوند.

همچنین مطمئن شوید که `icon-theme.cache` برای هر تم ارائه‌شده توسط بسته نصب شده است، و `dontDropIconThemeCache` را روی `true` تنظیم کنید تا فایل کش توسط setup hook مربوط به `gtk3` حذف نشود.

### تم‌های GTK {#ssec-gnome-themes}

پیش از این، لازم بود یک تم GTK در `XDG_DATA_DIRS` قرار داشته باشد. از زمانی که GTK تم Adwaita را در خود ادغام کرده است، این کار دیگر برای اکثر برنامه‌ها ضروری نیست. برخی از برنامه‌ها (به عنوان مثال، برنامه‌هایی که برای [elementary HIG](https://docs.elementary.io/hig) طراحی شده‌اند) ممکن است به یک تم خاص مانند `pantheon.elementary-gtk-theme` نیاز داشته باشند.

### GObject introspection typelibs {#ssec-gnome-typelibs}

[GObject introspection](https://gitlab.gnome.org/GNOME/gobject-introspection) به برنامه‌ها اجازه می‌دهد تا به راحتی از کتابخانه‌های C در زبان‌های دیگر استفاده کنند. این کار از طریق فایل‌های `typelib` انجام می‌شود که در `GI_TYPELIB_PATH` جستجو می‌شوند.

### پلاگین‌های مختلف {#ssec-gnome-plugins}

اگر برنامه شما از [GStreamer](https://gstreamer.freedesktop.org/) یا [Grilo](https://gitlab.gnome.org/GNOME/grilo) استفاده می‌کند، باید به ترتیب `GST_PLUGIN_SYSTEM_PATH_1_0` و `GRL_PLUGIN_PATH` را تنظیم کنید.

## دربارهٔ قلاب‌های `wrapGApps*` {#ssec-gnome-hooks}

با توجه به الزامات بالا، عبارت بسته به سرعت به‌هم‌ریخته و شلوغ خواهد شد:

```nix
{
  preFixup = ''
    for f in $(find $out/bin/ $out/libexec/ -type f -executable); do
      wrapProgram "$f" \
        --prefix GIO_EXTRA_MODULES : "${getLib dconf}/lib/gio/modules" \
        --prefix XDG_DATA_DIRS : "$out/share" \
        --prefix XDG_DATA_DIRS : "$out/share/gsettings-schemas/${name}" \
        --prefix XDG_DATA_DIRS : "${gsettings-desktop-schemas}/share/gsettings-schemas/${gsettings-desktop-schemas.name}" \
        --prefix XDG_DATA_DIRS : "${hicolor-icon-theme}/share" \
        --prefix GI_TYPELIB_PATH : "${
          lib.makeSearchPath "lib/girepository-1.0" [
            pango
            json-glib
          ]
        }"
    done
  '';
}
```

خوشبختانه، ما یک [خانواده از قلاب‌ها]{#ssec-gnome-hooks-wrapgappshook} داریم که این کار را خودکار می‌کنند. آن‌ها در کنار سایر قلاب‌های آماده‌سازی که متغیرهای محیطی را مقداردهی می‌کنند کار می‌کنند و سپس تمام فایل‌های اجرایی موجود در پوشه‌های `bin` و `libexec` را با استفاده از متغیرهای مذکور لفاف‌پیچی (wrap) می‌کنند. اگر یک بسته دارای خروجی‌های متعدد باشد، این قلاب‌ها به صورت پیش‌فرض روی `outputBin` یا در صورت تنظیم، روی خروجی‌های فهرست‌شده در `wrapGAppsInOutputs` کار خواهند کرد.

- [`wrapGAppsHook3`]{#ssec-gnome-hooks-wrapgappshook3} برای برنامه‌های GTK 3. برای سهولت، این قلاب همچنین `dconf.lib` (برای یک ماژول GIO که بک‌اند GSettings را با استفاده از `dconf` پیاده‌سازی می‌کند)، `gtk3` (برای اسکیمای GSettings) و `librsvg` (برای بارگذار GdkPixbuf) را به بستار (closure) اضافه می‌کند.
- [`wrapGAppsHook4`]{#ssec-gnome-hooks-wrapgappshook4} برای برنامه‌های GTK 4. مانند `wrapGAppsHook3` است اما `gtk3` را با `gtk4` جایگزین می‌کند.
- [`wrapGAppsNoGuiHook`]{#ssec-gnome-hooks-wrapgappsnoguihook} برای برنامه‌های بدون رابط گرافیکی. مانند موارد بالا است اما `gtk3` و `librsvg` را وارد بستار نمی‌کند.

این قلاب‌ها اقدامات زیر را انجام می‌دهند:

- خود قلاب `wrapGApps*` پوشهٔ `share` مربوط به بسته را به `XDG_DATA_DIRS` اضافه می‌کند.

- []{#ssec-gnome-hooks-glib} قلاب آماده‌سازی `glib` متغیر `GSETTINGS_SCHEMAS_PATH` را مقداردهی می‌کند و سپس قلاب `wrapGApps*` آن را به ابتدای `XDG_DATA_DIRS` می‌افزاید.

- []{#ssec-gnome-hooks-gdk-pixbuf} قلاب آماده‌سازی `gdk-pixbuf` متغیر `GDK_PIXBUF_MODULE_FILE` را با مسیر بزرگ‌ترین فایل `loaders.cache` از وابستگی‌های شامل [بارگذارهای GdkPixbuf](#ssec-gnome-gdk-pixbuf-loaders) مقداردهی می‌کند. این روش زمانی که تنها دو بسته شامل بارگذار وجود داشته باشد (`gdk-pixbuf` و برای مثال `librsvg`) به خوبی کار می‌کند – بسته دوم را انتخاب می‌کند، با این انتظار معقول که چون علاوه بر بارگذارهای پیش‌فرض، بارگذار اضافی را هم توصیف می‌کند بزرگ‌تر خواهد بود. اما وقتی بیش از دو بستهٔ بارگذار وجود داشته باشد، این منطق از کار می‌افتد. یک راه حل ممکن، ساخت یک فایل کش سفارشی برای هر بستهٔ شامل برنامه است، همان‌طور که ماژول NixOS با مسیر `services/x11/gdk-pixbuf.nix` انجام می‌دهد. قلاب `wrapGApps*` متغیر محیطی `GDK_PIXBUF_MODULE_FILE` را در وراپر (wrapper) تولیدشده کپی می‌کند.

- []{#ssec-gnome-hooks-gtk-drop-icon-theme-cache} یکی از قلاب‌های آماده‌سازی `gtk3` فایل‌های `icon-theme.cache` را از پوشه‌های تم آیکون بسته حذف می‌کند تا از تداخل جلوگیری شود. بسته‌های تم آیکون باید با تنظیم `dontDropIconThemeCache = true;` از این امر جلوگیری کنند.

- []{#ssec-gnome-hooks-dconf} کتابخانه `dconf.lib` یک وابستگی برای قلاب `wrapGApps*` است، که سپس آن را به متغیر `GIO_EXTRA_MODULES` نیز اضافه می‌کند.

- []{#ssec-gnome-hooks-hicolor-icon-theme} قلاب آماده‌سازی `hicolor-icon-theme` تم‌های آیکون را به `XDG_ICON_DIRS` اضافه می‌کند.

- []{#ssec-gnome-hooks-gobject-introspection} قلاب آماده‌سازی `gobject-introspection` متغیر `GI_TYPELIB_PATH` را با پوشه‌های `lib/girepository-1.0` وابستگی‌ها مقداردهی می‌کند، که سپس توسط قلاب `wrapGApps*` به وراپر اضافه می‌شود. این قلاب همچنین پوشه‌های `share` وابستگی‌ها را به `XDG_DATA_DIRS` می‌افزاید که هدف آن ترویج فایل‌های GIR است اما [بستارهای](https://github.com/NixOS/nixpkgs/issues/32790) بسته‌هایی که از قلاب `wrapGApps*` استفاده می‌کنند را نیز آلوده می‌کند.

- []{#ssec-gnome-hooks-gst-grl-plugins} قلاب‌های آماده‌سازی `gst_all_1.gstreamer` و `grilo` به ترتیب متغیرهای `GST_PLUGIN_SYSTEM_PATH_1_0` و `GRL_PLUGIN_PATH` را مقداردهی می‌کنند که سپس توسط قلاب `wrapGApps*` به وراپر اضافه خواهند شد.

- []{#ssec-gnome-hooks-libglycin} [قلاب آماده‌سازی](#libglycin-setup-hook) مربوط به `libglycin` متغیر `XDG_DATA_DIRS` را با مسیر بارگذارها مقداردهی می‌کند.

همچنین می‌توانید با استفاده از `gappsWrapperArgs` در قلاب `preFixup`، آرگومان‌های اضافی را به `makeWrapper` ارسال کنید:

```nix
{
  preFixup = ''
    gappsWrapperArgs+=(
      # Thumbnailers
      --prefix XDG_DATA_DIRS : "${gdk-pixbuf}/share"
      --prefix XDG_DATA_DIRS : "${librsvg}/share"
      --prefix XDG_DATA_DIRS : "${shared-mime-info}/share"
    )
  '';
}
```

## به‌روزرسانی بسته‌های GNOME {#ssec-gnome-updating}

اکثر بسته‌های GNOME دارای [`updateScript`](#var-passthru-updateScript) هستند، بنابراین می‌توان با اجرای `nix-shell maintainers/scripts/update.nix --argstr package nautilus` به آخرین تاربال کد منبع به‌روزرسانی کرد، یا حتی به‌صورت دسته‌جمعی با `nix-shell maintainers/scripts/update.nix --argstr path gnome` این کار را انجام داد. فایل `NEWS` بسته را بخوانید تا ببینید چه تغییراتی ایجاد شده است.

## مشکلات رایج {#ssec-gnome-common-issues}

### `GLib-GIO-ERROR **: 06:04:50.903: No GSettings schemas are installed on the system` {#ssec-gnome-common-issues-no-schemas}

هیچ اسکیمایی در `XDG_DATA_DIRS` در دسترس نیست. به‌طور موقت یک بستهٔ تصادفی حاوی اسکیماها مانند `gsettings-desktop-schemas` را به `buildInputs` اضافه کنید. قلاب‌های راه‌اندازی مربوط به [`glib`](#ssec-gnome-hooks-glib) و [`wrapGApps*`](#ssec-gnome-hooks-wrapgappshook) در دسترس قرار دادن اسکیماها برای برنامه را بر عهده خواهند گرفت و شما اسکیماهای مفقود واقعی را در [خطای بعدی](#ssec-gnome-common-issues-missing-schema) خواهید دید. یا می‌توانید برای یافتن اسکیماهای واقعیِ استفاده‌شده، کد منبع را بررسی کنید.

### `GLib-GIO-ERROR **: 06:04:50.903: Settings schema ‘org.gnome.foo’ is not installed` {#ssec-gnome-common-issues-missing-schema}

بسته فاقد برخی اسکیماهای GSettings است. می‌توانید بسته‌ای که حاوی اسکیما است را با `nix-locate org.gnome.foo.gschema.xml` پیدا کنید و اجازه دهید قلاب‌ها عملیات wrapping را همان‌طور که در [بالا](#ssec-gnome-common-issues-no-schemas) گفته شد، مدیریت کنند.

### هنگام استفاده از قلاب `wrapGApps*` با deriverها یا قلاب‌های خاص، ممکن است با باینری‌های دو بار wrap شده مواجه شوید. {#ssec-gnome-common-issues-double-wrapped}

دلیل این امر آن است که برخی قلاب‌های راه‌اندازی مانند `qt6.wrapQtAppsHook` نیز برنامه‌ها را با استفاده از `makeWrapper` wrap می‌کنند. به همین ترتیب، برخی deriverها (مانند `python.pkgs.buildPythonApplication`) به‌طور خودکار قلاب‌های راه‌اندازیِ مخصوص به خود را فرا می‌خوانند که wrapper تولید می‌کنند.

ساده‌ترین راهکار این است که wrapping خودکارِ قلاب `wrapGApps*` را با استفاده از `dontWrapGApps = true;` غیرفعال کنید و در عین حال آرگومان‌های `makeWrapper` آن را به یک wrapper دیگر پاس دهید.

در مورد یک برنامهٔ پایتون، این کار می‌تواند به شکل زیر باشد:

```nix
python3.pkgs.buildPythonApplication {
  pname = "gnome-music";
  version = "3.32.2";

  nativeBuildInputs = [
    wrapGAppsHook3
    gobject-introspection
    # ...
  ];

  dontWrapGApps = true;

  # Arguments to be passed to `makeWrapper`, only used by buildPython*
  preFixup = ''
    makeWrapperArgs+=("''${gappsWrapperArgs[@]}")
  '';
}
```

و برای یک برنامه Qt مانند:

```nix
stdenv.mkDerivation {
  pname = "calibre";
  version = "3.47.0";

  nativeBuildInputs = [
    wrapGAppsHook3
    qt6.wrapQtAppsHook
    qmake
    # ...
  ];

  dontWrapGApps = true;

  preFixup = ''
    qtWrapperArgs+=("''${gappsWrapperArgs[@]}")
  '';
}
```

### من در حال بسته‌بندی پروژه‌ای هستم که نمی‌توان آن را wrap کرد، مانند یک کتابخانه یا افزونه GNOME Shell. {#ssec-gnome-common-issues-unwrappable-package}

می‌توانید به برنامه‌هایی که به کتابخانه وابسته هستند تکیه کنید تا متغیرهای محیطی لازم را تنظیم کنند، اما نادیده گرفتن این موضوع ساده است. در عوض توصیه می‌کنیم در صورت امکان، مسیرها را در کد منبع پچ کنید. در ادامه چند نمونه آورده شده است:

- []{#ssec-gnome-common-issues-unwrappable-package-gnome-shell-ext} [جایگزینی یک `GI_TYPELIB_PATH` در افزونه GNOME Shell](https://github.com/NixOS/nixpkgs/blob/e981466fbb08e6231a1377539ff17fbba3270fda/pkgs/by-name/gn/gnome-shell-extensions/package.nix#L25-L32) – ما از `replaceVars` برای گنجاندن مسیر یک typelib در پچ استفاده می‌کنیم.

- []{#ssec-gnome-common-issues-unwrappable-package-gsettings} نمونه‌های زیر در حال هاردکد کردن مسیرهای اسکیمای GSettings هستند. برای دریافت مسیرهای اسکیما از توابع زیر استفاده می‌کنیم:

  * `glib.getSchemaPath` یک صفت (attribute) بسته nix را به عنوان آرگومان می‌پذیرد.

  * `glib.makeSchemaPath` یک خروجی بسته مانند `$out` و نام یک derivation را می‌پذیرد. اگر اسکیمایی که باید هاردکد کنید در همان derivation قرار دارد، باید از این تابع استفاده کنید.

  []{#ssec-gnome-common-issues-unwrappable-package-gsettings-vala} [هاردکد کردن مسیر اسکیمای GSettings در پلاگین Vala (کتابخانه به‌صورت پویا بارگذاری‌شده)](https://github.com/NixOS/nixpkgs/blob/7bb8f05f12ca3cff9da72b56caa2f7472d5732bc/pkgs/desktops/pantheon/apps/elementary-files/default.nix#L78-L86) – در اینجا نمی‌توان از `replaceVars` استفاده کرد زیرا اسکیما از همان بسته می‌آید و مانع از ارسال مسیر آن به تابع می‌شود، که احتمالاً به دلیل یک [اشکال (Bug) در Nix](https://github.com/NixOS/nix/issues/1846) است.

  []{#ssec-gnome-common-issues-unwrappable-package-gsettings-c} [هاردکد کردن مسیر اسکیمای GSettings در کتابخانه C](https://github.com/NixOS/nixpkgs/blob/29c120c065d03b000224872251bed93932d42412/pkgs/development/libraries/glib-networking/default.nix#L31-L34) – هیچ چیز خاصی به‌جز استفاده از [پچ Coccinelle](https://github.com/NixOS/nixpkgs/pull/67957#issuecomment-527717467) برای تولید خود پچ وجود ندارد.

### من باید یک باینری را خارج از پوشه‌های `bin` و `libexec` wrap کنم. {#ssec-gnome-common-issues-weird-location}

می‌توانید فرایند wrap کردن را به‌صورت دستی با `wrapGApp` در فاز `preFixup` اجرا کنید. این تابع مسیر یک برنامه را به‌عنوان اولین آرگومان می‌پذیرد؛ آرگومان‌های باقی‌مانده مستقیماً به تابع [`wrapProgram`](#fun-wrapProgram) منتقل می‌شوند.
