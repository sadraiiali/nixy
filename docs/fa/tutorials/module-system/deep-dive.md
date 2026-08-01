(module-system-deep-dive)=
# بررسی عمیق سیستم ماژول

یا: *پوشاندن دنیا در قالب ماژول‌ها*

در این آموزش، نمونه‌ای جامع از نحوه پوشاندن یک رابط برنامه‌نویسی کاربرد (API) موجود با ماژول‌های Nix را دنبال خواهید کرد.

## نمای کلی

این آموزش، [ارائه مربوط به ماژول‌ها](https://infinisil.com/modules.mp4) اثر [@infinisil](https://github.com/infinisil) ([منبع](https://github.com/tweag/summer-of-nix-modules)) را برای شرکت‌کنندگان [Summer of Nix](https://github.com/ngi-nix/summer-of-nix) در سال ۲۰۲۱ دنبال می‌کند.

تماشای همزمان آن در کنار این آموزش می‌تواند به شما کمک کند تا تغییرات کدهایی را که روی آن‌ها کار می‌کنید، بهتر دنبال کنید.

### چه چیزی خواهید آموخت؟

شما ماژول‌هایی را برای تعامل با [Google Maps API](https://developers.google.com/maps/documentation/maps-static) خواهید نوشت و گزینه‌های ماژولی را اعلام می‌کنید که نمایانگر هندسه نقشه، پین‌های مکان و موارد دیگر هستند.

در طول این آموزش، ابتدا برخی پیکربندی‌های *نادرست* را خواهید نوشت تا فرصتی برای بحث درباره‌ی پیام‌های خطای حاصل و نحوه حل آن‌ها، به‌ویژه هنگام بحث درباره‌ی چک کردن تایپ‌ها فراهم شود.

### به چه چیزی نیاز دارید؟

شما برای این تمرین از دو اسکریپت کمک‌رسان استفاده خواهید کرد.
فایل‌های {download}`map.sh <files/map.sh>` و {download}`geocode.sh <files/geocode.sh>` را در پوشه کاری خود بارگیری کنید.

:::{warning}
برای اجرای مثال‌های این آموزش، به یک [کلید Google API](https://developers.google.com/maps/documentation/maps-static/start#before-you-begin) در مسیر `$XDG_DATA_HOME/google-api/key` نیاز دارید.
:::

## ماژول خالی

مورد زیر را در فایلی به نام `default.nix` بنویسید:

```{code-block} nix
:caption: default.nix
{ ... }:
{

}
```

## اعلام گزینه‌ها

ما به چند تابع کمک‌رسان نیاز خواهیم داشت که از [کتابخانه Nixpkgs](https://github.com/NixOS/nixpkgs/tree/master/lib) تأمین می‌شوند؛ این کتابخانه توسط سیستم ماژول به عنوان `lib` ارسال می‌شود:

```{code-block} diff
:caption: default.nix
- { ... }:
+ { lib, ... }:
{

}
```

با استفاده از [`lib.mkOption`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.options.mkOption)، گزینه `scripts.output` را طوری declare کنید که از نوع `lines` باشد:

```{code-block} diff
:caption: default.nix
 { lib, ... }: {

+ options = {
+   scripts.output = lib.mkOption {
+     type = lib.types.lines;
+   };
+ };

 }
```

نوع `lines` به این معناست که تنها مقادیر معتبر، رشته‌ها هستند و تعاریف چندگانه باید با نویسه‌های خط جدید (newlines) به یکدیگر متصل شوند.

:::{note}
نام و مسیر صفت این گزینه اختیاری است.
در اینجا ما از `scripts` استفاده می‌کنیم، زیرا بعداً اسکریپت دیگری را اضافه خواهیم کرد، و این یکی را `output` می‌نامیم، زیرا نگاشت حاصل را خروجی خواهد داد.
:::

## ارزیابی ماژول‌ها

یک فایل جدید به نام `eval.nix` بنویسید تا [`lib.evalModules`](https://nixos.org/manual/nixpkgs/unstable/#module-system-lib-evalModules) را فراخوانی کرده و ماژول موجود در `default.nix` را ارزیابی کند:

```{code-block} nix
:caption: eval.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in
pkgs.lib.evalModules {
  modules = [
    ./default.nix
  ];
}
```

دستور زیر را اجرا کنید:

:::{warning}
این کار منجر به بروز خطا خواهد شد.
:::

```console
nix-instantiate --eval eval.nix -A config.scripts.output
```

:::{dropdown} توضیح تفصیلی
دستور [`nix-instantiate --eval`](/pages/nix-manual/command-ref/nix-instantiate) فایل Nix را در مسیر مشخص‌شده تجزیه (parse) و ارزیابی کرده و نتیجه را چاپ می‌کند.
تابع `evalModules` یک مجموعه ویژگی تولید می‌کند که در آن مقادیر نهایی پیکربندی در صفت `config` ظاهر می‌شوند.
بنابراین، ما عبارت Nix را در `eval.nix` در [مسیر صفت](/pages/nix-manual/language/operators#attribute-selection) `config.scripts.output` ارزیابی می‌کنیم.
:::

پیغام خطا نشان می‌دهد که گزینه‌ی `scripts.output` استفاده شده اما تعریف نشده‌است: پیش از دسترسی به گزینه، باید مقداری برای آن تعیین شود.
شما این کار را در مراحل بعدی انجام خواهید داد.

## چک کردن تایپ‌ها

همان‌طور که پیش‌تر ذکر شد، نوع `lines` تنها مقادیر رشته‌ای را مجاز می‌داند.

:::{warning}
در این بخش، یک مقدار نامعتبر تنظیم خواهید کرد و با یک خطای نوع مواجه می‌شوید.
:::

اگر در عوض تلاش کنید یک عدد صحیح به گزینه اختصاص دهید چه اتفاقی می‌افتد؟

خطوط زیر را به `default.nix` اضافه کنید:

```{code-block} diff
:caption: default.nix
 { lib, ... }: {

  options = {
    scripts.output = lib.mkOption {
      type = lib.types.lines;
    };
  };

+ config = {
+   scripts.output = 42;
+ };
 }
```

اکنون سعی کنید دستور قبلی را اجرا کنید و اولین خطای ماژول خود را مشاهده کنید:

```console
$ nix-instantiate --eval eval.nix -A config.scripts.output
error:
...
       error: A definition for option `scripts.output' is not of type `strings concatenated with "\n"'. Definition values:
       - In `/home/nix-user/default.nix': 42
```

تعریف `scripts.output = 42;` باعث بروز یک خطای نوع (type error) شد: اعداد صحیح، رشته‌هایی نیستند که با کاراکتر خط جدید به هم متصل شوند.

برای اینکه این ماژول از بررسی‌های نوع عبور کرده و گزینه `scripts.output` را با موفقیت ارزیابی کند، اکنون یک رشته به `scripts.output` اختصاص خواهید داد.

در این حالت، یک دستور شل اختصاص می‌دهید که اسکریپت {download}`map <files/map.sh>` را در پوشه جاری اجرا می‌کند.
این اسکریپت به نوبه خود API استاتیک گوگل مپس (Google Maps Static API) را فراخوانی می‌کند تا یک نقشه جهانی تولید کند.
خروجی برای نمایش با [`feh`](https://feh.finalrewind.org/)، یک نمایشگر تصویر مینیمال، ارسال می‌شود.

با تغییر مقدار `scripts.output` به رشته‌ی زیر، `default.nix` را به‌روزرسانی کنید:

```{code-block} diff
:caption: default.nix
   config = {
-    scripts.output = 42;
+    scripts.output = ''
+      ./map.sh size=640x640 scale=2 | feh -
+    '';
   };
```

## زنگ تفریح: اسکریپت‌های تکرارپذیر

آن دستور ساده احتمالاً روی سیستم شما به شکلی که مدنظر است کار نخواهد کرد، زیرا ممکن است فاقد وابستگی‌های لازم (`curl` و `feh`) باشد.
ما می‌توانیم این مشکل را با بسته‌بندی اسکریپت خام {download}`map <files/map.sh>` به وسیله‌ی `pkgs.writeShellApplication` حل کنیم.

ابتدا، با افزودن ماژولی که `config._module.args` را تنظیم می‌کند، یک آرگومان `pkgs` را در ارزیابی ماژول خود دردسترس قرار دهید:

```{code-block} diff
:caption: eval.nix
 pkgs.lib.evalModules {
   modules = [
+    ({ config, ... }: { config._module.args = { inherit pkgs; }; })
     ./default.nix
   ];
 }
```

:::{note}
این مکانیسم در حال حاضر فقط [در کد سیستم ماژول مستند شده‌است](https://github.com/NixOS/nixpkgs/blob/master/lib/modules.nix#L140-L182)، و آن مستندات ناقص و قدیمی هستند.
:::

سپس فایل `default.nix` را تغییر دهید تا محتوای زیر را داشته باشد:

```{code-block} nix
:caption: default.nix
{ pkgs, lib, ... }: {

  options = {
    scripts.output = lib.mkOption {
      type = lib.types.package;
    };
  };

  config = {
    scripts.output = pkgs.writeShellApplication {
      name = "map";
      runtimeInputs = with pkgs; [ curl feh ];
      text = ''
        ${./map.sh} size=640x640 scale=2 | feh -
      '';
    };
  };
}
```

این کار به آرگومان افزوده‌شده‌ی قبلی `pkgs` دسترسی پیدا می‌کند تا بتوانیم از وابستگی‌ها استفاده کنیم، و فایل `map` موجود در پوشه جاری را در انبار Nix کپی می‌کند تا برای اسکریپت بسته‌بندی‌شده (که آن نیز در انبار Nix قرار خواهد داشت) در دسترس باشد.

اسکریپت را با دستور زیر اجرا کنید:

```console
nix-build eval.nix -A config.scripts.output
./result/bin/map
```

برای تکرار سریع‌تر، یک ترمینال جدید باز کنید و [`entr`](https://github.com/eradman/entr) را طوری تنظیم کنید که هر زمان هر فایل کدی در پوشه فعلی تغییر کرد، اسکریپت را مجدداً اجرا کند:

```console
nix-shell -p entr findutils bash --run \
  "ls *.nix | \
   entr -rs ' \
     nix-build eval.nix -A config.scripts.output --no-out-link \
     | xargs printf -- \"%s/bin/map\" \
     | xargs bash \
   ' \
  "
```

این دستور کارهای زیر را انجام می‌دهد:
- فهرست‌کردن تمام فایل‌های `.nix`
- واداشتن `entr` به نظارت بر آن‌ها از نظر تغییرات. خاتمه‌دادن به دستور فراخوانی‌شده در هر تغییر با `-r`.
- در هر تغییر:
    - اجرای دستور `nix-build` مشابه بالا، اما بدون اضافه‌کردن پیوند نمادین `./result`
    - برداشتن مسیر انبار حاصل و الحاق `/bin/map` به آن
    - اجرای فایل اجرایی در مسیر ساخته‌شده به این روش

## اعلام گزینه‌های بیشتر

به‌جای تنظیم مستقیم تمام پارامترهای اسکریپت، این کار را از طریق سیستم ماژول انجام خواهیم داد.
این کار نه‌تنها مقداری ایمنی از طریق چک کردن تایپ‌ها اضافه می‌کند، بلکه اجازه می‌دهد انتزاع‌هایی برای مدیریت پیچیدگی در حال رشد و نیازمندی‌های در حال تغییر بسازیم.

بیایید با معرفی گزینه دیگری به نام `requestParams` شروع کنیم که نمایانگر پارامترهای درخواست ارائه‌شده به رابط برنامه‌نویسی کاربرد (API) گوگل مپ خواهد بود.

نوع آن `listOf <elementType>` خواهد بود که فهرستی از عناصر یک نوع است.

در این صورت، به‌جای `lines` می‌خواهید نوع عناصر فهرست `str` (یک نوع رشته عمومی) باشد.

تفاوت بین `str` و `lines` در رفتار ادغام آن‌ها است:
نوع گزینه‌های ماژول نه‌تنها مقادیر معتبر را بررسی می‌کنند، بلکه مشخص می‌کنند که چگونه تعاریف متعدد یک گزینه باید در یک گزینه ترکیب شوند.
- برای `lines`، تعاریف چندگانه با الحاق همراه با خطوط جدید ادغام می‌شوند.
- برای `str`، تعاریف چندگانه مجاز نیستند. این موضوع در اینجا مشکلی ایجاد نمی‌کند، زیرا نمی‌توان یک عنصر فهرست را چندین بار تعریف کرد.

موارد زیر را به فایل `default.nix` خود اضافه کنید:

```{code-block} diff
:caption: default.nix
     scripts.output = lib.mkOption {
       type = lib.types.package;
     };
+
+    requestParams = lib.mkOption {
+      type = lib.types.listOf lib.types.str;
+    };
   };

  config = {
    scripts.output = pkgs.writeShellApplication {
      name = "map";
      runtimeInputs = with pkgs; [ curl feh ];
      text = ''
        ${./map.sh} size=640x640 scale=2 | feh -
      '';
    };
+
+    requestParams = [
+      "size=640x640"
+      "scale=2"
+    ];
   };
 }
```

## وابستگی گزینه‌ها به یکدیگر

یک ماژول مشخص عموماً گزینه‌ای را اعلام می‌کند که نتیجه‌ای را برای استفاده در بخش‌های دیگر تولید می‌کند، در این مورد `scripts.output`.

گزینه‌ها می‌توانند به گزینه‌های دیگر وابسته باشند، که این امکان را فراهم می‌کند تا انتزاعات مفیدتری ساخته شوند.

در اینجا، ما می‌خواهیم گزینه `scripts.output` از مقادیر `requestParams` به عنوان آرگومان‌هایی برای اسکریپت `./map` استفاده کند.

### دسترسی به مقادیر گزینه

برای در دسترس قرار دادن مقادیر گزینه برای یک ماژول، آرگومان‌های تابعی که ماژول را اعلام می‌کند باید شامل صفت `config` باشد.

فایل `default.nix` را برای افزودن صفت `config` به‌روزرسانی کنید:

```{code-block} diff
:caption: default.nix
-{ pkgs, lib, ... }: {
+{ pkgs, lib, config, ... }: {
```

هنگامی که ماژولی که گزینه‌ها را تنظیم می‌کند ارزیابی می‌شود، مقادیر حاصل را می‌توان از طریق نام صفات متناظر آن‌ها در زیر `config` دسترسی داشت.

:::{note}
مقادیر گزینه را نمی‌توان مستقیماً از خود همان ماژول فراخوانی یا بررسی کرد.

سیستم ماژول تمام ماژول‌هایی را که دریافت می‌کند ارزیابی نموده و هر یک از آن‌ها می‌توانند مقدار یک گزینه خاص را تعریف کنند.
اینکه وقتی یک گزینه توسط چندین ماژول تنظیم می‌شود چه اتفاقی می‌افتد، توسط نوع آن گزینه تعیین می‌شود.
:::

:::{warning}
*آرگومان* `config` با *صفت* `config` یکسان **نیست**:
- *آرگومان* `config` نتیجه ارزیابی تنبل (lazy evaluation) سیستم ماژول را در خود نگه می‌دارد، که تمام ماژول‌های ارسال‌شده به `evalModules` و `imports` آن‌ها را لحاظ می‌کند.
- *صفت* `config` یک ماژول، مقادیر گزینه‌های همان ماژول خاص را برای ارزیابی در اختیار سیستم ماژول قرار می‌دهد.
:::

اکنون تغییرات زیر را در `default.nix` اعمال کنید:

```{code-block} diff
:caption: default.nix
   config = {
     scripts.output = pkgs.writeShellApplication {
       name = "map";
       runtimeInputs = with pkgs; [ curl feh ];
       text = ''
-        ${./map.sh} size=640x640 scale=2 | feh -
+        ${./map.sh} ${lib.concatStringsSep " "
+          config.requestParams} | feh -
       '';
```

در اینجا، مقدار صفت `config.requestParams` توسط سیستم ماژول بر اساس تعاریف موجود در همان فایل مقداردهی می‌شود.

:::{note}
ارزیابی تنبل (lazy evaluation) در زبان Nix به سیستم ماژول اجازه می‌دهد تا یک مقدار را در آرگومان `config` که به ماژول تعریف‌کننده‌ی آن مقدار پاس داده می‌شود، در دسترس قرار دهد.
:::

سپس از `lib.concatStringsSep " "` برای به هم پیوستن هر عنصر فهرست از مقدار `config.requestParams` به یک رشته‌ی واحد استفاده می‌شود، به‌طوری که عناصر فهرست `requestParams` با یک کاراکتر فاصله (space) از هم جدا می‌شوند.

نتیجه‌ی این امر، نمایانگر فهرست آرگومان‌های خط فرمان برای پاس دادن به اسکریپت `./map` است.

## تعاریف شرطی
گاهی اوقات، می‌خواهید مقادیر گزینه اختیاری باشند. این کار زمانی می‌تواند مفید باشد که تعریف مقدار برای یک گزینه اجباری نباشد، مانند مورد زیر.

شما یک گزینه‌ی جدید به نام `map.zoom` برای کنترل سطح بزرگنمایی (zoom) نقشه تعریف خواهید کرد. اگر هیچ آرگومان متناظری پاس داده نشود، رابط برنامه‌نویسی کاربرد (API) گوگل مپ سطح بزرگنمایی را استنباط خواهد کرد؛ وضعیتی که می‌توانید آن را با `nullOr <type>` نشان دهید که نمایانگر مقادیر از نوع `<type>` یا `null` است. این موضوع به‌طور خودکار به این معنا _نیست_ که وقتی گزینه تعریف نشده‌است، مقدار چنین گزینه‌ای برابر با `null` باشد -- ما همچنان باید یک مقدار پیش‌فرض تعریف کنیم.

مجموعه ویژگی `map` را به همراه گزینه‌ی `zoom` در اعلامیه‌ی `options` سطح بالا، به شکل زیر اضافه کنید:

```{code-block} diff
:caption: default.nix
     requestParams = lib.mkOption {
       type = lib.types.listOf lib.types.str;
     };
+
+    map = {
+      zoom = lib.mkOption {
+        type = lib.types.nullOr lib.types.int;
+        default = null;
+      };
+    };
   };
```

برای استفاده از این امکان، از تابع `mkIf <condition> <definition>` استفاده کنید که تعریف مورد نظر را تنها در صورتی اضافه می‌کند که شرط به `true` ارزیابی شود.
افزودنی‌های زیر را به فهرست `requestParams` در بلوک `config` اضافه کنید:

```{code-block} diff
:caption: default.nix
     requestParams = [
       "size=640x640"
       "scale=2"
+      (lib.mkIf (config.map.zoom != null)
+        "zoom=${toString config.map.zoom}")
     ];
   };
```

این کار تنها در صورتی یک پارامتر `zoom` به فراخوانی اسکریپت اضافه می‌کند که مقدار `config.map.zoom` برابر با `null` نباشد.

## مقادیر پیش‌فرض

فرض کنید که در برنامه خود می‌خواهیم رفتار پیش‌فرض متفاوتی داشته باشیم که سطح بزرگ‌نمایی را روی `10` تنظیم می‌کند، به‌طوری که بزرگ‌نمایی خودکار باید به‌صورت صریح فعال شود.

این کار را می‌توان با استفاده از آرگومان `default` برای [`mkOption`](https://github.com/NixOS/nixpkgs/blob/master/lib/options.nix) انجام داد.
اگر مقدار گزینه‌ای که آن را اعلام می‌کند به شکل دیگری مشخص نشده باشد، از این مقدار استفاده خواهد شد.

خط مربوطه را اصلاح کنید:

```{code-block} diff
:caption: default.nix
     map = {
       zoom = lib.mkOption {
         type = lib.types.nullOr lib.types.int;
-        default = null;
+        default = 10;
       };
     };
   };
```

## پوشش دادن دستورات شل

اکنون گزینه‌هایی را برای کنترل ابعاد نقشه و سطح زوم اعلام کرده‌اید، اما راهی برای مشخص کردن اینکه نقشه باید روی چه نقطه‌ای متمرکز شود فراهم نکرده‌اید.

اکنون گزینه `center` را اضافه کنید، احتمالاً با مکان خودتان به عنوان مقدار پیش‌فرض:

```{code-block} diff
:caption: default.nix
         type = lib.types.nullOr lib.types.int;
         default = 10;
       };
+
+      center = lib.mkOption {
+        type = lib.types.nullOr lib.types.str;
+        default = "switzerland";
+      };
     };
   };
```

برای پیاده‌سازی این رفتار، از ابزار {download}`geocode <files/geocode.sh>` استفاده خواهید کرد که نام مکان‌ها را به مختصات تبدیل می‌کند.
راه‌های متعددی برای قابل‌دسترس کردن یک بسته جدید وجود دارد، اما به عنوان یک تمرین، آن را به عنوان یک گزینه در سیستم ماژول اضافه خواهید کرد.

ابتدا یک گزینه جدید برای جای دادن بسته اضافه کنید:

```{code-block} diff
:caption: default.nix
   options = {
     scripts.output = lib.mkOption {
       type = lib.types.package;
     };
+
+    scripts.geocode = lib.mkOption {
+      type = lib.types.package;
+    };
```

سپس مقدار آن گزینه را طوری تعریف کنید که با قرار دادن یک فراخوان به اسکریپت درون `writeShellApplication`، اسکریپت خام را بازتولیدپذیر سازید:

```{code-block} diff
:caption: default.nix
   config = {
+    scripts.geocode = pkgs.writeShellApplication {
+      name = "geocode";
+      runtimeInputs = with pkgs; [ curl jq ];
+      text = ''exec ${./geocode.sh} "$@"'';
+    };
+
     scripts.output = pkgs.writeShellApplication {
       name = "map";
       runtimeInputs = with pkgs; [ curl feh ];
```

اکنون یک فراخوانی `mkIf` دیگر به فهرست `requestParams` اضافه کنید که در آن از طریق `config.scripts.geocode` به بسته‌ی بسته‌بندی‌شده دسترسی پیدا می‌کنید و فایل اجرایی `/bin/geocode` را در داخل آن اجرا می‌کنید:

```{code-block} diff
:caption: default.nix
       "scale=2"
       (lib.mkIf (config.map.zoom != null)
         "zoom=${toString config.map.zoom}")
+      (lib.mkIf (config.map.center != null)
+        "center=\"$(${config.scripts.geocode}/bin/geocode ${
+          lib.escapeShellArg config.map.center
+        })\"")
     ];
   };
```

این بار، شما از `escapeShellArg` استفاده کرده‌اید تا مقدار `config.map.center` را به عنوان یک آرگومان خط فرمان به `geocode` ارسال کنید و نتیجه را با درون‌گذاری رشته مجدداً وارد رشته‌ی `requestParams` کنید که مقدار `center` را تنظیم می‌کند.

پیچیدن اجرای دستور شل در ماژول‌های Nix تکنیک مفیدی برای کنترل تغییرات سیستم است، زیرا به‌جای سر و کار داشتن با پیچیدگی‌های فرار دادن (escaping) دستی، از رابط صفات و مقادیر ارگونومیک‌تری استفاده می‌کند.

## تفکیک ماژول‌ها

[طرحواره ماژول](https://nixos.org/manual/nixos/stable/#sec-writing-modules) شامل صفت `imports` است که امکان ترکیب ماژول‌های بیشتر را فراهم می‌کند؛ برای مثال، جهت تقسیم یک پیکربندی بزرگ به چندین فایل.

به‌طور خاص، این امکان را به شما می‌دهد تا اعلام‌های گزینه را از جایی که در پیکربندی خود استفاده می‌شوند، جداسازی کنید.

یک ماژول جدید به نام `marker.nix` ایجاد کنید که در آن بتوانید گزینه‌هایی را برای تعریف پین‌های مکان و سایر نشانگرها روی نقشه اعلام کنید:

```{code-block} diff
:caption: marker.nix
{ lib, config, ... }: {

}
```

این فایل جدید را در `default.nix` با استفاده از صفت `imports` ارجاع دهید:

```{code-block} diff
:caption: default.nix
 { pkgs, lib, config, ... }: {

+  imports = [
+    ./marker.nix
+  ];
+
```

## نوع `submodule`

ما می‌خواهیم چندین نشانگر روی نقشه تنظیم کنیم.
یک نشانگر، نوعی پیچیده با چندین فیلد است.

اینجا دقیقاً جایی است که یکی از کاربردی‌ترین انواع موجود در سیستم نوع سیستم ماژول وارد میدان می‌شود: `submodule`.
این نوع به شما اجازه می‌دهد ماژول‌های تو در تو با گزینه‌های مختص به خود را تعریف کنید.

در اینجا، شما یک گزینه جدید به نام `map.markers` تعریف خواهید کرد که نوع آن فهرستی از زیرماژول‌ها است که هر کدام دارای یک نوع تو در تو به نام `location` هستند و به شما اجازه می‌دهند فهرستی از نشانگرها را روی نقشه تعریف کنید.

هر انتساب نشانگرها در طول ارزیابی `config` سطح بالا چک‌شده از نظر تایپ (type-checked) خواهد شد.

تغییرات زیر را در فایل `marker.nix` اعمال کنید:

```{code-block} diff
:caption: marker.nix
-{ lib, config, ... }: {
+{ lib, config, ... }:
+let
+  markerType = lib.types.submodule {
+    options = {
+      location = lib.mkOption {
+        type = lib.types.nullOr lib.types.str;
+        default = null;
+      };
+    };
+  };
+in {
+
+  options = {
+    map.markers = lib.mkOption {
+      type = lib.types.listOf markerType;
+    };
+  };
```

## تعریف گزینه‌ها در سایر ماژول‌ها

به‌دلیل نحوه ترکیب تعاریف گزینه‌ها توسط سیستم ماژول، می‌توانید آزادانه مقادیری را به گزینه‌های تعریف‌شده در سایر ماژول‌ها اختصاص دهید.

در این حالت، شما از گزینه `map.markers` برای تولید و افزودن عناصر جدید به فهرست `requestParams` استفاده خواهید کرد تا نشانگرهای اعلام‌شده‌ی شما روی نقشه بازگردانده‌شده ظاهر شوند، اما از ماژول اعلام‌شده در `marker.nix`.

برای پیاده‌سازی این رفتار، بلوک `config` زیر را به `marker.nix` اضافه کنید:

```{code-block} diff
:caption: marker.nix
+  config = {
+
+    map.markers = [
+      { location = "new york"; }
+    ];
+
+    requestParams = let
+      paramForMarker =
+        builtins.map (marker: "$(${config.scripts.geocode}/bin/geocode ${
+          lib.escapeShellArg marker.location})") config.map.markers;
+    in [ "markers=\"${lib.concatStringsSep "|" paramForMarker}\"" ];
+  };
```

:::{warning}
برای جلوگیری از تداخل با تنظیم گزینه `map` و مقدار نهایی پیکربندی `config.map`, در اینجا ما از تابع `map` به صورت صریح به شکل `builtins.map` استفاده می‌کنیم.
:::

در اینجا، شما بار دیگر از `escapeShellArg` و درون‌گذاری رشته برای تولید یک رشته‌ی Nix استفاده کردید که این بار فهرستی جدا شده با خط عمودی (|) از صفات موقعیت جغرافیایی‌کدگذاری‌شده را تولید می‌کند.

مقدار `requestParams` نیز روی فهرست حاصل از رشته‌ها تنظیم شد که به لطف رفتار ادغام پیش‌فرض نوع `list`، به فهرست `requestParams` تعریف‌شده در `default.nix` الحاق می‌شود.

هنگام تعریف نشانگرهای متعدد، تعیین مرکز یا سطح بزرگنمایی مناسب برای نقشه ممکن است چالش‌برانگیز باشد؛ ساده‌تر این است که اجازه دهید رابط برنامه‌نویسی کاربرد (API) این کار را برای شما انجام دهد.

برای دستیابی به این هدف، تغییرات زیر را بالاتر از اعلان `requestParams` به `marker.nix` اضافه کنید:

```{code-block} diff
:caption: marker.nix
+    map.center = lib.mkIf
+      (lib.length config.map.markers >= 1)
+      null;
+
+    map.zoom = lib.mkIf
+      (lib.length config.map.markers >= 2)
+      null;
+
     requestParams = let
       paramForMarker = marker:
         let
```

در این حالت، رفتار پیش‌فرض رابط برنامه‌نویسی کاربرد (API) گوگل مپس هنگامی که مرکز یا سطح بزرگنمایی (zoom level) به آن ارسال نمی‌شود، این است که مرکز هندسی تمام نشانگرهای داده‌شده را انتخاب کند و سطح بزرگنمایی مناسبی را برای مشاهده‌ی هم‌زمان تمام نشانگرها تنظیم نماید.

## زیرماژول‌های تو در تو

در مرحله‌ی بعد، می‌خواهیم به چندین کاربر نام‌گذاری‌شده اجازه دهیم تا هر کدام فهرستی از نشانگرها را تعریف کنند.

برای این کار، یک گزینه‌ی `users` با نوع `lib.types.attrsOf <subtype>` اضافه خواهید کرد که به شما اجازه می‌دهد `users` را به عنوان یک مجموعه ویژگی تعریف کنید که مقادیر آن دارای نوع `<subtype>` هستند.

در اینجا، آن زیرماژول، زیرماژول دیگری خواهد بود که اجازه می‌دهد یک نشانگر مبدأ را اعلان کنید؛ این کار برای پرس‌وجو از رابط برنامه‌نویسی کاربرد (API) جهت دریافت مسیر پیشنهادی برای یک سفر مناسب است.

این کار بار دیگر از زیرماژول `markerType` استفاده خواهد کرد و ساختاری تو در تو از زیرماژول‌ها را فراهم می‌سازد.

برای انتشار تعاریف نشانگر از `users` به گزینه‌ی `map.markers`، تغییرات زیر را اعمال کنید.

در بلوک `let`:

```{code-block} diff
:caption: marker.nix
+  userType = lib.types.submodule {
+    options = {
+      departure = lib.mkOption {
+        type = markerType;
+        default = {};
+      };
+    };
+  };
+
 in {
```

این کار یک نوع زیرماژول (submodule type) را برای یک کاربر تعریف می‌کند، با یک گزینه `departure` از نوع `markerType`.

در بلوک `options`، بالاتر از `map.markers`:

```{code-block} diff
:caption: marker.nix
+    users = lib.mkOption {
+      type = lib.types.attrsOf userType;
+    };
```

این امر امکان‌پذیر می‌سازد تا یک مجموعه ویژگی `users` در هر زیرماژولی که `marker.nix` را درون‌ریزی می‌کند، به `config` اضافه شود؛ در این صورت هر صفت از نوع `userType` خواهد بود که در مرحله‌ی قبل اعلام شد.

در بلوک `config`، بالاتر از `map.center`:

```{code-block} diff
:caption: marker.nix
   config = {

-    map.markers = [
-      { location = "new york"; }
-    ];
+    map.markers = lib.filter
+      (marker: marker.location != null)
+      (lib.concatMap (user: [
+        user.departure
+      ]) (lib.attrValues config.users));

     map.center = lib.mkIf
       (lib.length config.map.markers >= 1)
```

این کار تمام نشانگرهای `departure` را از تمامی کاربران موجود در آرگومان `config` برمی‌دارد و اگر صفت `location` آن‌ها `null` نباشد، آن‌ها را به `map.markers` اضافه می‌کند.

مجموعه ویژگی `config.users` به `attrValues` داده می‌شود که لیستی از مقادیر هر یک از صفات موجود در مجموعه (در اینجا، مجموعه `config.users` که تعریف کرده‌اید) را برمی‌گرداند؛ این لیست به صورت الفبایی مرتب شده‌است (که همان نحوه ذخیره‌سازی نام صفات در زبان Nix است).

بازگشت به `default.nix`، مقدار گزینه حاصل برای `map.markers` همچنان توسط `requestParams` فراخوانی می‌شود که به نوبه خود برای تولید آرگومان‌هایی برای اسکریپتی استفاده می‌شود که در نهایت رابط برنامه‌نویسی کاربرد (API) گوگل مپ را صدا می‌زند.

تعریف گزینه‌ها به این روش به شما امکان می‌دهد چندین مقدار `users.<name>.departure.location` را تنظیم کرده و نقشه‌ای با زوم و مرکز مناسب، به همراه پین‌های منطبق بر مقادیر `departure.location` برای *تمامی* `users` تولید کنید.

در رویداد Summer of Nix سال ۲۰۲۱، این مورد پایه و اساس یک نسخه نمایشی از نقشه تعاملی چندنفره را تشکیل داد.

## نوع `strMatching`

اکنون که نقشه می‌تواند با چندین نشانگر رندر شود، زمان آن رسیده‌است که برخی سفارشی‌سازی‌های ظاهری را اضافه کنیم.

برای تشخیص نشانگرها از یکدیگر، گزینه دیگری را به زیرماژول `markerType` اضافه کنید تا برچسب‌گذاری روی هر پین نشانگر مجاز باشد.

مستندات رابط برنامه‌نویسی کاربرد (API) بیان می‌کند که [این برچسب‌ها باید یک حرف بزرگ یا یک عدد باشند](https://developers.google.com/maps/documentation/maps-static/start#MarkerStyles).

شما می‌توانید این را با استفاده از نوع `strMatching "<regex>"` پیاده‌سازی کنید؛ که در آن `<regex>` یک عبارت منظم است که هر مقدار مطابق را می‌پذیرد، که در این مورد یک حرف بزرگ یا یک عدد است.

در بلوک `let`:

```{code-block} diff
:caption: marker.nix
         type = lib.types.nullOr lib.types.str;
         default = null;
       };
+
+      style.label = lib.mkOption {
+        type = lib.types.nullOr
+          (lib.types.strMatching "[A-Z0-9]");
+        default = null;
+      };
     };
   };
```

بار دیگر، `types.nullOr` مقادیر `null` را مجاز می‌داند و مقدار پیش‌فرض روی `null` تنظیم شده‌است.

در تابع `paramForMarker`:

```{code-block} diff
:caption: marker.nix
     requestParams = let
-      paramForMarker =
-        builtins.map (marker: "$(${config.scripts.geocode}/bin/geocode ${
-         lib.escapeShellArg marker.location})") config.map.markers;
-    in [ "markers=\"${lib.concatStringsSep "|" paramForMarker}\"" ];
+      paramForMarker = marker:
+        let
+          attributes =
+            lib.optional (marker.style.label != null)
+            "label:${marker.style.label}"
+            ++ [
+              "$(${config.scripts.geocode}/bin/geocode ${
+                lib.escapeShellArg marker.location
+              })"
+            ];
+        in "markers=\"${lib.concatStringsSep "|" attributes}\"";
+      in
+        builtins.map paramForMarker config.map.markers;
```

توجه کنید که چگونه اکنون یک `marker` منحصربه‌فرد برای هر کاربر با به هم چسباندن صفات `label` و `location` ایجاد می‌کنیم و آن‌ها را به `requestParams` اختصاص می‌دهیم.
برچسب (label) برای هر `marker` تنها در صورتی به پارامترهای CLI منتقل می‌شود که `marker.style.label` تنظیم شده باشد.

## توابع به عنوان آرگومان‌های ماژول

در حال حاضر، اگر برچسبی به‌طور صریح تنظیم نشده باشد، هیچ‌کدام نمایش داده نخواهند شد.
اما از آنجا که هر صفت `users` دارای یک نام است، می‌توانیم به جای آن از آن به عنوان یک مقدار خودکار استفاده کنیم.

این تابع `firstUpperAlnum` به شما اجازه می‌دهد تا اولین کاراکتر نام کاربری را، با نوع صحیح برای انتقال به `departure.style.label`، بازیابی کنید:

```{code-block} diff
:caption: marker.nix
{ lib, config, ... }:
 let
+  # Returns the uppercased first letter
+  # or number of a string
+  firstUpperAlnum = str:
+    lib.mapNullable lib.head
+    (builtins.match "[^A-Z0-9]*([A-Z0-9]).*"
+    (lib.toUpper str));

   markerType = lib.types.submodule {
     options = {
```

با تبدیل آرگومان ورودی به تابع `lib.types.submodule`، می‌توانید به آرگومان‌های درون آن دسترسی پیدا کنید.

یکی از آرگومان‌های خاصی که به‌طور خودکار برای ماژول‌های فرعی (submodules) در دسترس است، `name` نام دارد؛ هنگامی که این آرگومان در `attrsOf` استفاده شود، نام صفتی را که ماژول فرعی تحت آن تعریف شده‌است به شما می‌دهد:

```{code-block} diff
:caption: marker.nix
-  userType = lib.types.submodule {
+  userType = lib.types.submodule ({ name, ... }: {
     options = {
       departure = lib.mkOption {
         type = markerType;
         default = {};
       };
     };
-  };
```

در این حالت، شما به راحتی به نام موجود در گزینه‌ی `label` از زیرماژول‌های marker دسترسی ندارید، در غیر این صورت می‌توانستید یک مقدار `default` تعیین کنید.

در عوض می‌توانید از بخش `config` در زیرماژول `user` برای تنظیم یک پیش‌فرض استفاده کنید، به این صورت:

```{code-block} diff
:caption: marker.nix
+
+    config = {
+      departure.style.label = lib.mkDefault
+        (firstUpperAlnum name);
+    };
+  });

 in {

```

:::{note}
گزینه‌های ماژول دارای یک *اولویت* (priority) هستند که به صورت یک عدد صحیح نشان داده می‌شود و تقدم تنظیم گزینه روی یک مقدار خاص را تعیین می‌کند.
هنگام ادغام مقادیر، اولویتی که کمترین مقدار عددی را داشته باشد برنده است.

تغییردهنده‌ی `lib.mkDefault` اولویت مقدار آرگومان خود را روی ۱۰۰۰ تنظیم می‌کند که پایین‌ترین تقدم است.

این کار تضمین می‌کند که سایر مقادیر تنظیم‌شده برای همان گزینه اولویت بالاتری خواهند داشت.
:::

## انواع `either` و `enum`

برای کنتراست بصری بهتر، مفید خواهد بود که راهی برای تغییر *رنگ* یک نشانگر (marker) داشته باشیم.

در اینجا برای این منظور از دو توابع نوع جدید استفاده خواهید کرد:
- `either <this> <that>`، که دو نوع را به عنوان آرگومان می‌پذیرد و اجازه می‌دهد هر کدام از آن‌ها استفاده شوند
- `enum [ <allowed values> ]`، که لیستی از مقادیر مجاز را می‌پذیرد و اجازه استفاده از هر یک از آن‌ها را می‌دهد

در بلوک `let`، گزینه‌ی `colorType` زیر را اضافه کنید که می‌تواند رشته‌هایی شامل نام‌های رنگ‌های داده‌شده یا یک مقدار RGB را در خود نگه دارد، سپس نوع ترکیبی جدید را اضافه کنید:

```{code-block} diff
:caption: marker.nix
     ...
     (builtins.match "[^A-Z0-9]*([A-Z0-9]).*"
     (lib.toUpper str));

+  # Either a color name or `0xRRGGBB`
+  colorType = lib.types.either
+    (lib.types.strMatching "0x[0-9A-F]{6}")
+    (lib.types.enum [
+      "black" "brown" "green" "purple" "yellow"
+      "blue" "gray" "orange" "red" "white" ]);
+
   markerType = lib.types.submodule {
     options = {
       location = lib.mkOption {
```

این امکان را فراهم می‌کند که یا رشته‌هایی که با یک عدد هگزادسیمال ۲۴ بیتی مطابقت دارند را بپذیرید یا رشته‌هایی که با یکی از نام‌های رنگ مشخص‌شده برابر هستند.

در انتهای بلوک `let`، گزینه `style.color` را اضافه کرده و یک مقدار پیش‌فرض مشخص کنید:

```{code-block} diff
:caption: marker.nix
           (lib.types.strMatching "[A-Z0-9]");
         default = null;
       };
+
+      style.color = lib.mkOption {
+        type = colorType;
+        default = "red";
+      };
     };
   };
```

اکنون یک ورودی به فهرست `paramForMarker` اضافه کنید که از گزینه جدید استفاده می‌کند:

```{code-block} diff
:caption: marker.nix
               (marker.style.label != null)
               "label:${marker.style.label}"
             ++ [
+              "color:${marker.style.color}"
               "$(${config.scripts.geocode}/bin/geocode ${
                 lib.escapeShellArg marker.location
               })"
```

اگر نشانگرهای متفاوتی را تنظیم می‌کنید، داشتن قابلیت تغییر اندازه آن‌ها به صورت مجزا بسیار مفید خواهد بود.

یک گزینه جدید به نام `style.size` به فایل `marker.nix` اضافه کنید که به شما امکان می‌دهد از بین مجموعه اندازه‌های ازپیش‌تعریف‌شده یکی را انتخاب کنید:

```{code-block} diff
:caption: marker.nix
         type = colorType;
         default = "red";
       };
+
+      style.size = lib.mkOption {
+        type = lib.types.enum
+          [ "tiny" "small" "medium" "large" ];
+        default = "medium";
+      };
     };
   };
```

اکنون یک نگاشت برای پارامتر size در `paramForMarker` اضافه کنید که یک رشته‌ی مناسب را برای ارسال به API انتخاب می‌کند:

```{code-block} diff
:caption: marker.nix
     requestParams = let
       paramForMarker = marker:
         let
+          size = {
+            tiny = "tiny";
+            small = "small";
+            medium = "mid";
+            large = null;
+          }.${marker.style.size};
+
```

در نهایت، یک فراخوان دیگر `lib.optional` به رشته‌ی `attributes` اضافه کنید، و از اندازه انتخاب‌شده بهره ببرید:

```{code-block} diff
:caption: marker.nix
           attributes =
             lib.optional
               (marker.style.label != null)
               "label:${marker.style.label}"
+            ++ lib.optional
+              (size != null)
+              "size:${size}"
             ++ [
               "color:${marker.style.color}"
               "$(${config.scripts.geocode}/bin/geocode ${
```

## زیرماژول `pathType`

تا اینجا، شما گزینه‌ای برای اعلام یک نشانگر *مبدا* و همچنین چندین گزینه برای پیکربندی بازنمایی بصری آن ایجاد کرده‌اید.

اکنون می‌خواهیم مسیری را از موقعیت کاربر تا یک مقصد محاسبه و نمایش دهیم.

گزینه جدید تعریف‌شده در بخش بعد به شما این امکان را می‌دهد که یک نشانگر *مقصد* تنظیم کنید که همراه با مبدا به شما اجازه می‌دهد با استفاده از ماژول جدید تعریف‌شده در زیر، *مسیرها* را روی نقشه ترسیم کنید.

برای شروع، یک فایل `path.nix` جدید با محتوای زیر ایجاد کنید:

```{code-block} nix
:caption: path.nix
{ lib, config, ... }:
let
  pathType = lib.types.submodule {
    options = {
      locations = lib.mkOption {
        type = lib.types.listOf lib.types.str;
      };
    };
  };
in
{
  options = {
    map.paths = lib.mkOption {
      type = lib.types.listOf pathType;
    };
  };
  config = {
    requestParams =
      let
        attrForLocation = loc:
          "$(${config.scripts.geocode}/bin/geocode ${lib.escapeShellArg loc})";
        paramForPath = path:
          let
            attributes =
              builtins.map attrForLocation path.locations;
          in
          ''path="${lib.concatStringsSep "|" attributes}"'';
      in
      builtins.map paramForPath config.map.paths;
  };
}
```

ماژول `path.nix` گزینه‌ای را برای تعریف فهرستی از مسیرها روی `map` اعلام می‌کند که در آن هر مسیر، فهرستی از رشته‌ها برای موقعیت‌های جغرافیایی است.

در صفت `config`، فراخوانی رابط برنامه‌نویسی کاربرد (API) را با تنظیم مقدار گزینه `requestParams` با مختصات به‌طور مناسب تبدیل‌شده بهبود می‌بخشیم؛ این مقدار با پارامترهای درخواست تنظیم‌شده در جاهای دیگر ادغام (Concatenate) خواهد شد.

اکنون این ماژول جدید `path.nix` را از ماژول `marker.nix` خود درون‌ریزی کنید:

```{code-block} diff
:caption: marker.nix
 in {

+  imports = [
+    ./path.nix
+  ];
+
   options = {

     users = lib.mkOption {
```

تعریف گزینه `departure` را به یک گزینه `arrival` جدید در فایل `marker.nix` کپی کنید تا پیاده‌سازی اولیه مسیر تکمیل شود:

```{code-block} diff
:caption: marker.nix
         type = markerType;
         default = {};
       };
+
+      arrival = lib.mkOption {
+        type = markerType;
+        default = {};
+      };
     };
```

در ادامه، یک صفت `arrival.style.label` به بلوک `config` اضافه کنید که صفت `departure.style.label` را بازتاب می‌دهد:

```{code-block} diff
:caption: marker.nix
     config = {
       departure.style.label = lib.mkDefault
         (firstUpperAlnum name);
+      arrival.style.label = lib.mkDefault
+        (firstUpperAlnum name);
     };
   });
```

در نهایت، فهرست خروجی تابع ارسال‌شده به `concatMap` در `map.markers` را به‌گونه‌ای به‌روزرسانی کنید که شامل مارکر `arrival` برای هر کاربر نیز بشود:

```{code-block} diff
:caption: marker.nix
     map.markers = lib.filter
       (marker: marker.location != null)
       (lib.concatMap (user: [
-        user.departure
+        user.departure user.arrival
       ]) (lib.attrValues config.users));

     map.center = lib.mkIf
```

اکنون شما پایه و اساس لازم برای تعریف مسیرها روی نقشه را دارید که جفت‌های نقاط مبدأ و مقصد را به یکدیگر متصل می‌کنند.

در ماژول path، مسیری را تعریف کنید که مکان‌های مبدأ و مقصد هر کاربر را به هم متصل کند:

```{code-block} diff
:caption: path.nix
   config = {
+
+    map.paths = builtins.map (user: {
+      locations = [
+        user.departure.location
+        user.arrival.location
+      ];
+    }) (lib.filter (user:
+      user.departure.location != null
+      && user.arrival.location != null
+    ) (lib.attrValues config.users));
+
     requestParams = let
       attrForLocation = loc:
         "$(geocode ${lib.escapeShellArg loc})";
```

صفت جدید `map.paths` شامل فهرستی از تمام مسیرهای معتبر تعریف‌شده برای همه کاربران است.

یک مسیر تنها در صورتی معتبر است که صفات `departure` و `arrival` برای آن کاربر تنظیم شده باشند.

## محدودیت `between` روی مقادیر عدد صحیح

کاربران شما نظرات خود را اعلام کرده‌اند و خواستار این هستند که بتوانند استایل مسیرهای خود را با یک گزینه‌ی `weight` سفارشی‌سازی کنند.

همان‌طور که پیش‌تر دیدید، اکنون یک زیرماژول جدید برای استایل مسیر اعلام خواهید کرد.

اگرچه می‌توانید گزینه‌ی `style.weight` را نیز مستقیماً اعلام کنید، اما در این حالت باید از زیرماژول استفاده کنید تا بتوانید بعداً نوع استایل مسیر را مجدداً استفاده کنید.

گزینه‌ی زیرماژول `pathStyleType` را به بلوک `let` در فایل `path.nix` اضافه کنید:
```{code-block} diff
:caption: path.nix
 { lib, config, ... }:
 let
+
+  pathStyleType = lib.types.submodule {
+    options = {
+      weight = lib.mkOption {
+        type = lib.types.ints.between 1 20;
+        default = 5;
+      };
+    };
+  };
+
   pathType = lib.types.submodule {
```

:::{note}
نوع `ints.between <lower> <upper>` اعداد صحیح را در محدوده مشخص‌شده (شامل کران‌ها) مجاز می‌داند.
:::

وزن مسیر به‌طور پیش‌فرض روی ۵ تنظیم می‌شود، اما می‌توان آن را روی هر مقدار عدد صحیح در محدوده ۱ تا ۲۰ قرار داد، به طوری که وزن‌های بیشتر، مسیرهای ضخیم‌تری را روی نقشه ایجاد می‌کنند.

اکنون یک گزینه `style` به مجموعه `options` در ادامه فایل اضافه کنید:

```{code-block} diff
:caption: path.nix
     options = {
       locations = lib.mkOption {
         type = lib.types.listOf lib.types.str;
       };
+
+      style = lib.mkOption {
+        type = pathStyleType;
+        default = {};
+      };
     };

   };
```

در نهایت، فهرست `attributes` را در `paramForPath` به‌روزرسانی کنید:

```{code-block} diff
:caption: path.nix
       paramForPath = path:
         let
           attributes =
-            builtins.map attrForLocation path.locations;
+            [
+              "weight:${toString path.style.weight}"
+            ]
+            ++ builtins.map attrForLocation path.locations;
         in "path=\"${lib.concatStringsSep "|" attributes}\"";
```

## زیرماژول `pathStyle`

کاربران هنوز در واقع نمی‌توانند سبک مسیر را شخصی‌سازی کنند.
یک گزینه جدید به نام `pathStyle` برای هر کاربر معرفی کنید.

سیستم ماژول به شما اجازه می‌دهد تا مقادیر یک گزینه را چندین بار اعلام کنید و اگر نوع‌ها اجازه دهند، وظیفه ادغام کردن مقادیر هر اعلامیه با یکدیگر را بر عهده می‌گیرد.

این امر باعث می‌شود تا امکان داشتن یک تعریف برای گزینه `users` در ماژول `marker.nix` و همچنین تعریف دیگری برای `users` در `path.nix` فراهم شود:

```{code-block} diff
:caption: path.nix
 in {
   options = {
+
+    users = lib.mkOption {
+      type = lib.types.attrsOf (lib.types.submodule {
+        options.pathStyle = lib.mkOption {
+          type = pathStyleType;
+          default = {};
+        };
+      });
+    };
+
     map.paths = lib.mkOption {
       type = lib.types.listOf pathType;
     };
```

سپس خطی را با استفاده از گزینه `user.pathStyle` در `map.paths` اضافه کنید که در آن مسیرهای هر کاربر پردازش می‌شوند:

```{code-block} diff
:caption: path.nix
         user.departure.location
         user.arrival.location
       ];
+      style = user.pathStyle;
     }) (lib.filter (user:
       user.departure.location != null
       && user.arrival.location != null
```

## استایل‌دهی مسیر: رنگ

همانند نشانگرها، مسیرها نیز باید رنگ‌های قابل‌سفارشی‌سازی داشته باشند.

می‌توانید این کار را با استفاده از انواعی که تا به اینجای کار با آن‌ها آشنا شده‌اید انجام دهید.

یک بلوک `colorType` جدید به فایل `path.nix` اضافه کنید و نام‌های رنگ مجاز و مقادیر هگزادسیمال RGB/RGBA را مشخص کنید:

```{code-block} diff
:caption: path.nix
 { lib, config, ... }:
 let

+  # Either a color name, `0xRRGGBB` or `0xRRGGBBAA`
+  colorType = lib.types.either
+    (lib.types.strMatching "0x[0-9A-F]{6}([0-9A-F]{2})?")
+    (lib.types.enum [
+      "black" "brown" "green" "purple" "yellow"
+      "blue" "gray" "orange" "red" "white"
+    ]);
+
   pathStyleType = lib.types.submodule {
```

زیر گزینه `weight`، یک گزینه `color` جدید اضافه کنید تا از مقدار جدید `colorType` استفاده کند:

```{code-block} diff
:caption: path.nix
         type = lib.types.ints.between 1 20;
         default = 5;
       };
+
+      color = lib.mkOption {
+        type = colorType;
+        default = "blue";
+      };
     };
   };
```

در نهایت، خطی با استفاده از گزینه `color` را به فهرست `attributes` اضافه کنید:

```{code-block} diff
:caption: path.nix
           attributes =
             [
               "weight:${toString path.style.weight}"
+              "color:${path.style.color}"
             ]
             ++ map attrForLocation path.locations;
         in "path=${
```

## استایل‌دهی بیشتر

حالا که تا اینجا پیش آمده‌اید، برای بهبود بیشتر ظاهر نقشه‌ی رندرشده، یک گزینه‌ی استایل دیگر اضافه کنید که به مسیرها اجازه دهد به صورت *ژئودزیک* (geodesic)، یعنی کوتاه‌ترین فاصله‌ی «خط راست» بین دو نقطه روی زمین، ترسیم شوند.

از آنجا که این ویژگی را می‌توان فعال یا غیرفعال کرد، می‌توانید این کار را با استفاده از نوع `bool` انجام دهید که می‌تواند `true` یا `false` باشد.

اکنون تغییرات زیر را روی `path.nix` اعمال کنید:

```{code-block} diff
:caption: path.nix
         type = colorType;
         default = "blue";
       };
+
+      geodesic = lib.mkOption {
+        type = lib.types.bool;
+        default = false;
+      };
     };
   };
```

همچنین مطمئن شوید که خطی اضافه کنید تا از آن مقدار در فهرست `attributes` استفاده شود، به طوری که مقدار گزینه در فراخوانی API گنجانده شود:

```{code-block} diff
:caption: path.nix
             [
               "weight:${toString path.style.weight}"
               "color:${path.style.color}"
+              "geodesic:${lib.boolToString path.style.geodesic}"
             ]
             ++ map attrForLocation path.locations;
         in "path=${
```

## جمع‌بندی

در این آموزش، با کمک چندین تابع کمکی جدید از بخش `lib` مجموعه‌ی بسته‌های نیکس (Nixpkgs)، یادگرفتید که چگونه ماژول‌های سفارشی Nix را بنویسید تا سرویس‌های خارجی را تحت کنترل اعلانی (declarative) درآورید.

شما چندین ماژول را در فایل‌های مختلف تعریف کردید که هر کدام شامل زیرماژول‌های مجزایی هستند که از چک کردن تایپ‌ها (type checking) سیستم ماژول بهره می‌برند.

این ماژول‌ها ویژگی‌های رابط برنامه‌نویسی کاربرد (API) خارجی را به شیوه‌ای اعلانی در معرض نمایش گذاشتند.

اکنون می‌توانید با Nix دنیا را فتح کنید.
