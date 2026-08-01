(file-sets-tutorial)=
# کار با فایل‌های محلی

برای ساخت یک پروژه محلی در یک derivation نیکس، کدهای منبع باید برای [فایل اجرایی `builder`](/pages/nix-manual/language/derivations#attr-builder) آن قابل دسترس باشند.
به طور پیش‌فرض، `builder` در یک [محیط ایزوله](/pages/nix-manual/command-ref/conf-file-prefix#conf-sandbox) اجرا می‌شود که تنها اجازه خواندن از انبار نیکس را می‌دهد.
زبان Nix دارای قابلیت‌های توکاری برای کپی کردن فایل‌های محلی به انبار و ارائه مسیرهای حاصل در انبار است.

با این حال، استفاده مستقیم از این قابلیت‌ها می‌تواند چالش‌برانگیز باشد:

- تبدیل مسیرها به رشته‌ها (Coercion)، مانند الگوی رایج `src = ./.`،
  درایویشن را به نام پوشه فعلی وابسته می‌کند.
  علاوه بر این، همیشه کل پوشه، از جمله فایل‌های غیرضروری را به انبار اضافه می‌کند،
  که با تغییر آن‌ها باعث ساخت‌های جدید غیرضروری می‌شود.

- تابع [`builtins.path`](/pages/nix-manual/language/builtins-prefix#builtins-path)
  (و به طور معادل [`lib.sources.cleanSourceWith`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.sources.cleanSourceWith))
  می‌تواند این مشکلات را حل کند.
  با این حال، بیان انتخاب مسیر دلخواه با استفاده از رابط تابع `filter` اغلب دشوار است.

در این آموزش شما یاد خواهید گرفت که چگونه از [کتابخانه `lib.fileset`](https://nixos.org/manual/nixpkgs/stable/#sec-functions-library-fileset) متعلق به Nixpkgs برای کار با فایل‌های محلی در درایویشن‌ها استفاده کنید.
این کتابخانه روی قابلیت‌های توکار لایه انتزاعی ایجاد می‌کند و یک رابط امن‌تر و راحت‌تر ارائه می‌دهد.

## مجموعه‌فایل‌ها

یک _مجموعه‌فایل_ (file set) یک نوع داده‌است که نمایانگر مجموعه‌ای از فایل‌های محلی است.
مجموعه‌فایل‌ها را می‌توان با توابع مختلف این کتابخانه ایجاد، ترکیب و دستکاری کرد.

شما می‌توانید با استفاده از [`nix repl`](/pages/nix-manual/command-ref/experimental-commands) کتابخانه را بررسی کرده و درباره‌ی آن بیاموزید:

```shell-session
$ nix repl -f channel:nixos-23.11
...
nix-repl> fs = lib.fileset
```

تابع [`trace`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.trace) فایل‌های موجود در یک مجموعه فایل معین را به‌صورت قالب‌بندی‌شده و خوانا نمایش می‌دهد:

```shell-session
nix-repl> fs.trace ./. null
trace: /home/user (all files in directory)
null
```

تمام توابعی که انتظار یک مجموعه‌فایل به عنوان آرگومان را دارند، می‌توانند یک [مسیر](/pages/nix-manual/language/values#type-path) را نیز بپذیرند.
چنین آرگومان‌های مسیری سپس [به‌طور ضمنی به مجموعه‌ها تبدیل می‌شوند](https://nixos.org/manual/nixpkgs/stable/#sec-fileset-path-coercion) که شامل _تمام_ فایل‌های موجود در مسیر داده‌شده هستند.
در ردگیری (trace) قبلی، این موضوع با `(all files in directory)` نشان داده شده‌است.

:::{tip}
تابع `trace` اولین آرگومان خود را به صورت خوانا و ساختاریافته چاپ کرده و دومین آرگومان را بازمی‌گرداند.
اما از آنجا که اغلب فقط به این چاپ ساختاریافته در `nix repl` نیاز دارید، می‌توانید آرگومان دوم را حذف کنید:

```shell-session
nix-repl> fs.trace ./.
trace: /home/user (all files in directory)
«lambda @ /nix/store/1czr278x24s3bl6qdnifpvm5z03wfi2p-nixpkgs-src/lib/fileset/default.nix:555:8»
```
:::

با اینکه مجموعه‌فایل‌ها از نظر مفهومی شامل فایل‌های محلی هستند، اما این فایل‌ها هرگز به انبار نیکس اضافه *نمی‌شوند* مگر اینکه صراحتاً درخواست شود.
بنابراین، لازم نیست چندان نگران کپی شدن تصادفی رازها (secrets) به درون انبار قابل‌خواندن برای همگان باشید.

در این مثال، با وجود اینکه پوشه خانه را چاپ زیبا و ساختاریافته‌اید، هیچ فایلی کپی نشد.
این در تضاد با تبدیل اجباری مسیرها به رشته‌ها، مانند `"${./.}"` است،
که کل پوشه را در هنگام ارزیابی به انبار نیکس کپی می‌کند.

:::{warning}
هنگام استفاده از [ویژگی‌های آزمایشی `flakes` و `nix-command`](/pages/nix-manual/command-ref/experimental-commands)،
یک پوشه محلی درون یک فلیک همیشه به طور *کامل* در انبار نیکس کپی می‌شود، مگر اینکه یک مخزن گیت باشد.
:::

این تبدیل اجباری ضمنی برای فایل‌ها نیز کار می‌کند:

```shell-session
$ touch some-file
```

```shell-session
nix-repl> fs.trace ./some-file
trace: /home/user
trace: - some-file (regular)
```

علاوه بر فایل موجود، این دستور [نوع فایل](/pages/nix-manual/language/builtins-prefix#builtins-readFileType) آن را نیز چاپ می‌کند.

## پروژه نمونه

برای آزمایش بیشتر با کتابخانه، یک پروژه نمونه بسازید.
یک پوشه جدید ایجاد کنید، وارد آن شوید و `npins` را برای ثابت‌سازی نسخه Nixpkgs (Pinning) وابستگی Nixpkgs راه‌اندازی کنید:

```shell-session
$ mkdir fileset
$ cd fileset
$ nix-shell -p npins --run "npins init --bare; npins add github nixos nixpkgs --branch nixos-23.11"
```

سپس یک فایل `default.nix` با محتوای زیر ایجاد کنید:

```{code-block} nix
:caption: default.nix
{
  system ? builtins.currentSystem,
  sources ? import ./npins,
}:
let
  pkgs = import sources.nixpkgs {
    config = { };
    overlays = [ ];
    inherit system;
  };
in
pkgs.callPackage ./package.nix { }
```

دو فایل منبع برای کار اضافه کنید:

```shell-session
$ echo hello > hello.txt
$ echo world > world.txt
```

## افزودن فایل‌ها به انبار Nix

فایل‌های موجود در یک مجموعه‌فایل مشخص را می‌توان با استفاده از [`toSource`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.toSource) به انبار Nix اضافه کرد.
آرگومان این تابع نیازمند یک صفت (attribute) به نام `root` است تا مشخص کند کدام پوشه منبع باید در انبار کپی شود.
فقط فایل‌های موجود در صفت `fileset` در نتیجه گنجانده می‌شوند.

فایل `package.nix` را به صورت زیر تعریف کنید:

```{code-block} nix
:caption: package.nix
{ stdenv, lib }:
let
  fs = lib.fileset;
  sourceFiles = ./hello.txt;
in

fs.trace sourceFiles

stdenv.mkDerivation {
  name = "fileset";
  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };
  postInstall = ''
    mkdir $out
    cp -v hello.txt $out
  '';
}
```

فراخوانی `fs.trace` مجموعه فایل را که به عنوان ورودی درایویشن استفاده خواهد شد، چاپ می‌کند.

ساخت آن را امتحان کنید:

:::{note}
بار اول دریافت Nixpkgs کمی طول خواهد کشید.
:::

```
$ nix-build
trace: /home/user/fileset
trace: - hello.txt (regular)
this derivation will be built:
  /nix/store/3ci6avmjaijx5g8jhb218i183xi7bi2n-fileset.drv
...
'hello.txt' -> '/nix/store/sa4g6h13v0zbpfw6pzva860kp5aks44n-fileset/hello.txt'
...
/nix/store/sa4g6h13v0zbpfw6pzva860kp5aks44n-fileset
```

اما مزیت واقعی کتابخانه مجموعه‌فایل‌ها از امکانات آن برای ترکیب مجموعه‌فایل‌ها به روش‌های مختلف ناشی می‌شود.

## تفاوت

برای اینکه بتوانید هر دو فایل `hello.txt` و `world.txt` را در خروجی کپی کنید، کل پوشه پروژه را مجدداً به عنوان یک سورس اضافه کنید:

```{code-block} diff
:caption: package.nix
 { stdenv, lib }:
 let
   fs = lib.fileset;
-  sourceFiles = ./hello.txt;
+  sourceFiles = ./.;
 in

 fs.trace sourceFiles

 stdenv.mkDerivation {
   name = "fileset";
   src = fs.toSource {
     root = ./.;
     fileset = sourceFiles;
   };
   postInstall = ''
     mkdir $out
-    cp -v hello.txt $out
+    cp -v {hello,world}.txt $out
   '';
 }
```

این به طور دلخواه کار خواهد کرد:

```shell-session
$ nix-build
trace: /home/user/fileset (all files in directory)
this derivation will be built:
  /nix/store/fsihp8872vv9ngbkc7si5jcbigs81727-fileset.drv
...
'hello.txt' -> '/nix/store/wmsxfgbylagmf033nkazr3qfc96y7mwk-fileset/hello.txt'
'world.txt' -> '/nix/store/wmsxfgbylagmf033nkazr3qfc96y7mwk-fileset/world.txt'
...
/nix/store/wmsxfgbylagmf033nkazr3qfc96y7mwk-fileset
```

با این حال، اگر دوباره `nix-build` را اجرا کنید، مسیر خروجی متفاوت خواهد بود!

```shell-session
$ nix-build
trace: /home/user/fileset (all files in directory)
this derivation will be built:
  /nix/store/nlh7ismrf27xsnl3m20vfz6rvwlbbbca-fileset.drv
...
'hello.txt' -> '/nix/store/xknflcvjaa8dj6a6vkg629zmcrgz10rh-fileset/hello.txt'
'world.txt' -> '/nix/store/xknflcvjaa8dj6a6vkg629zmcrgz10rh-fileset/world.txt'
...
/nix/store/xknflcvjaa8dj6a6vkg629zmcrgz10rh-fileset
```

مشکل اینجاست که `nix-build` به طور پیش‌فرض یک پیوند نمادین (symlink) به نام `result` در پوشه کاری ایجاد می‌کند که به مسیر انبار تولیدشده اشاره دارد:

```
$ ls -l result
result -> /nix/store/xknflcvjaa8dj6a6vkg629zmcrgz10rh-fileset
```

از آنجا که `src` به کل پوشه اشاره دارد و محتویات آن با موفقیت `nix-build` تغییر می‌کند، نیکس مجبور خواهد شد هر بار از نو شروع کند.

:::{note}
این اتفاق بدون کتابخانه مجموعه‌فایل‌ها نیز رخ می‌دهد، برای مثال هنگام تنظیم مستقیم `src = ./.;`.
:::

تابع [`difference`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.difference) یک مجموعه‌فایل را از مجموعه‌فایل دیگر کم می‌کند.
نتیجه، یک مجموعه‌فایل جدید است که شامل تمام فایل‌های موجود در آرگومان اول است که در آرگومان دوم وجود ندارند.

از آن برای فیلتر کردن `./result` با تغییر تعریف `sourceFiles` استفاده کنید:

```{code-block} diff
:caption: package.nix
 { stdenv, lib }:
 let
   fs = lib.fileset;
-  sourceFiles = ./.;
+  sourceFiles = fs.difference ./. ./result;
 in
```

با ساختن این، کتابخانه مجموعه‌فایل‌ها مشخص خواهد کرد که چه فایل‌هایی از پوشه برداشته می‌شوند:

```shell-session
$ nix-build
trace: /home/user/fileset
trace: - package.nix (regular)
trace: - default.nix (regular)
trace: - hello.txt (regular)
trace: - npins (all files in directory)
trace: - world.txt (regular)
this derivation will be built:
  /nix/store/zr19bv51085zz005yk7pw4s9sglmafvn-fileset.drv
...
'hello.txt' -> '/nix/store/vhyhk6ij39gjapqavz1j1x3zbiy3qc1a-fileset/hello.txt'
'world.txt' -> '/nix/store/vhyhk6ij39gjapqavz1j1x3zbiy3qc1a-fileset/world.txt'
...
/nix/store/vhyhk6ij39gjapqavz1j1x3zbiy3qc1a-fileset
```

تلاش برای تکرار ساخت (build)، از مسیر انبار (store path) موجود مجدداً استفاده خواهد کرد:

```
$ nix-build
trace: /home/user/fileset
trace: - package.nix (regular)
trace: - default.nix (regular)
trace: - hello.txt (regular)
trace: - npins (all files in directory)
trace: - world.txt (regular)
/nix/store/vhyhk6ij39gjapqavz1j1x3zbiy3qc1a-fileset
```

## فایل‌های گمشده

با این حال، حذف پیوند نمادین `./result` مشکل جدیدی ایجاد می‌کند:

```shell-session
$ rm result
$ nix-build
error: lib.fileset.difference: Second argument (negative set)
  (/home/user/fileset/result) is a path that does not exist.
  To create a file set from a path that may not exist, use `lib.fileset.maybeMissing`.
```

دستورالعمل‌های موجود در پیام خطا را دنبال کنید و از [`maybeMissing`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.maybeMissing) برای ایجاد یک مجموعه‌فایل از مسیری که ممکن است وجود نداشته باشد استفاده کنید (در این صورت مجموعه‌فایل خالی خواهد بود):

```{code-block} diff
:caption: package.nix
 { stdenv, lib }:
 let
   fs = lib.fileset;
-  sourceFiles = fs.difference ./. ./result;
+  sourceFiles = fs.difference ./. (fs.maybeMissing ./result);
 in
```

این کار اکنون با استفاده از کل پوشه کار می‌کند، زیرا `./result` حضور ندارد:

```
$ nix-build
trace: /home/user/fileset (all files in directory)
this derivation will be built:
  /nix/store/zr19bv51085zz005yk7pw4s9sglmafvn-fileset.drv
...
/nix/store/vhyhk6ij39gjapqavz1j1x3zbiy3qc1a-fileset
```

تلاش مجدد برای ساخت، ردگیری (trace) متفاوتی را تولید خواهد کرد، اما همان مسیر خروجی را به همراه خواهد داشت:

```
$ nix-build
trace: /home/user/fileset
trace: - package.nix (regular)
trace: - default.nix (regular)
trace: - hello.txt (regular)
trace: - npins (all files in directory)
trace: - world.txt (regular)
/nix/store/vhyhk6ij39gjapqavz1j1x3zbiy3qc1a-fileset
```

## اجتماع (استثنا کردن صریح فایل‌ها)

هنوز یک مشکل وجود دارد:
تغییر دادن _هرکدام_ از فایل‌های گنجانده‌شده باعث می‌شود که derivation مجدداً ساخته شود، با اینکه اصلاً به آن فایل‌ها وابسته نیست.

یک خط خالی به `package.nix` اضافه کنید:

```shell-session
$ echo >> package.nix
```

بار دیگر، Nix از صفر شروع خواهد کرد:

```shell-session
$ nix-build
trace: /home/user/fileset
trace: - default.nix (regular)
trace: - npins (all files in directory)
trace: - package.nix (regular)
trace: - string.txt (regular)
this derivation will be built:
  /nix/store/zmgpqlpfz2jq0w9rdacsnpx8ni4n77cn-filesets.drv
...
/nix/store/6pffjljjy3c7kla60nljk3fad4q4kkzn-filesets
```

یک راه برای رفع این مشکل استفاده از [`unions`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.unions) است.

یک مجموعه فایل حاوی اشتراک (union) فایل‌هایی که باید مستثنی شوند بسازید (`fs.unions [ ... ]`)، و آن را (`difference`) از پوشه کامل (`./.`) کسر کنید:

```{code-block} nix
:caption: package.nix
  sourceFiles =
    fs.difference
      ./.
      (fs.unions [
        (fs.maybeMissing ./result)
        ./default.nix
        ./package.nix
        ./npins
      ]);
```

این به شکلی که انتظار می‌رود کار خواهد کرد:

```
$ nix-build
trace: /home/user/fileset
trace: - hello.txt (regular)
trace: - world.txt (regular)
this derivation will be built:
  /nix/store/gr2hw3gdjc28fmv0as1ikpj7lya4r51f-fileset.drv
...
/nix/store/ckn40y7hgqphhbhyrq64h9r6rvdh973r-fileset
```

تغییر دادن هر یک از فایل‌های مستثنی‌شده، دیگر لزوماً باعث ساخت جدید نمی‌شود:

```
$ echo >> package.nix
```

```
$ nix-build
trace: /home/user/fileset
trace: - hello.txt (regular)
trace: - world.txt (regular)
/nix/store/ckn40y7hgqphhbhyrq64h9r6rvdh973r-fileset
```

## فیلتر

تابع [`fileFilter`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.fileFilter) امکان فیلتر کردن مجموعه‌فایل‌ها را فراهم می‌کند به‌طوری‌که هر فایل مشمول، معیارهای داده‌شده را برآورده کند.

از آن برای انتخاب تمام فایل‌هایی که نام‌شان با `.nix` ختم می‌شود استفاده کنید:

```{code-block} diff
:caption: package.nix
   sourceFiles =
     fs.difference
       ./.
       (fs.unions [
         (fs.maybeMissing ./result)
-        ./default.nix
-        ./package.nix
+        (fs.fileFilter (file: file.hasExt "nix") ./.)
         ./npins
       ]);
```

این موضوع نتیجه را تغییر نمی‌دهد، حتی اگر یک فایل `.nix` جدید اضافه کنیم.

```shell-session
$ nix-build
trace: /home/user/fileset
trace: - hello.txt (regular)
trace: - world.txt (regular)
/nix/store/ckn40y7hgqphhbhyrq64h9r6rvdh973r-fileset
```

به‌طور ویژه، رویکرد استفاده از `difference ./.` به‌طور صریح فایل‌هایی را که باید _مستثنی شوند_ انتخاب می‌کند، به این معنا که فایل‌های جدید اضافه شده به پوشه‌ی منبع به‌طور پیش‌فرض شامل می‌شوند.
بسته به پروژه‌ی شما، این روش ممکن است نسبت به روش جایگزین در بخش بعدی مناسب‌تر باشد.

## اشتراک (انتخاب صریح فایل‌ها)

در تقابل با روش قبلی، می‌توان از `unions` نیز برای انتخاب فقط فایل‌هایی که باید _شامل شوند_ استفاده کرد.
این یعنی فایل‌های جدید اضافه شده به پوشه‌ی فعلی به‌طور پیش‌فرض نادیده گرفته خواهند شد.

چند فایل اضافی ایجاد کنید:

```shell-session
$ mkdir src
$ touch build.sh src/select.{c,h}
```

سپس مجموعه‌فایل‌ها را فقط از فایل‌هایی بسازید که قرار است صراحتاً گنجانده شوند:

```{code-block} nix
:caption: package.nix
{ stdenv, lib }:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./hello.txt
    ./world.txt
    ./build.sh
    (fs.fileFilter
      (file: file.hasExt "c" || file.hasExt "h")
      ./src
    )
  ];
in

fs.trace sourceFiles

stdenv.mkDerivation {
  name = "fileset";
  src = fs.toSource {
    root = ./.;
    fileset = sourceFiles;
  };
  postInstall = ''
    cp -vr . $out
  '';
}
```

اسکریپت `postInstall` ساده‌سازی شده‌است تا متکی بر این باشد که کدهای منبع به شکل مناسبی ازپیش‌فیلتر شده باشند:

```shell-session
$ nix-build
trace: /home/user/fileset
trace: - build.sh (regular)
trace: - hello.txt (regular)
trace: - src (all files in directory)
trace: - world.txt (regular)
this derivation will be built:
  /nix/store/sjzkn07d6a4qfp60p6dc64pzvmmdafff-fileset.drv
...
'.' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset'
'./build.sh' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset/build.sh'
'./hello.txt' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset/hello.txt'
'./world.txt' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset/world.txt'
'./src' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset/src'
'./src/select.c' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset/src/select.c'
'./src/select.h' -> '/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset/src/select.h'
...
/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset
```

فقط فایل‌های مشخص‌شده استفاده می‌شوند، حتی زمانی که یک فایل جدید اضافه شود:

```shell-session
$ touch src/select.o README.md

$ nix-build
trace: - build.sh (regular)
trace: - hello.txt (regular)
trace: - src
trace:   - select.c (regular)
trace:   - select.h (regular)
trace: - world.txt (regular)
/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset
```

## تطبیق فایل‌های ردیابی‌شده توسط Git

اگر یک پوشه بخشی از یک مخزن Git باشد، ارسال آن به [`gitTracked`](https://nixos.org/manual/nixpkgs/stable/#function-library-lib.fileset.gitTracked) یک مجموعه‌فایل به شما می‌دهد که فقط شامل فایل‌های ردیابی‌شده توسط Git است.

یک مخزن محلی Git ایجاد کنید و تمام فایل‌ها به جز `src/select.o` و `./result` را به آن اضافه کنید:

```shell-session
$ git init
Initialized empty Git repository in /home/user/fileset/.git/
$ git add -A
$ git reset src/select.o result
```

برای استفاده مجدد از این مجموعه فایل‌ها با `gitTracked`:

```{code-block} nix
:caption: package.nix
  sourceFiles = fs.gitTracked ./.;
```

دوباره آن را بسازید:

```shell-session
$ nix-build
warning: Git tree '/home/user/fileset' is dirty
trace: /home/vg/src/nix.dev/fileset
trace: - README.md (regular)
trace: - package.nix (regular)
trace: - build.sh (regular)
trace: - default.nix (regular)
trace: - hello.txt (regular)
trace: - npins (all files in directory)
trace: - src
trace:   - select.c (regular)
trace:   - select.h (regular)
trace: - world.txt (regular)
this derivation will be built:
  /nix/store/p9aw3fl5xcjbgg9yagykywvskzgrmk5y-fileset.drv
...
/nix/store/cw4bza1r27iimzrdbfl4yn5xr36d6k5l-fileset
```

با این حال، این شامل موارد زیادی می‌شود، زیرا همه این فایل‌ها برای ساخت derivation به شکلی که در ابتدا در نظر گرفته شده بود، مورد نیاز نیستند.

:::{note}
هنگام استفاده از [ویژگی‌های آزمایشی `flakes` و `nix-command`](/pages/nix-manual/command-ref/experimental-commands)،
این تابع مورد نیاز نیست، زیرا `nix build` به طور پیش‌فرض فقط به فایل‌هایی اجازه دسترسی می‌دهد که توسط Git ردیابی می‌شوند.
با این حال، برای فراهم کردن تجربه توسعه‌دهنده یکسان برای Nix پایدار، استفاده از این تابع همچنان توصیه می‌شود.
:::

## اشتراک (Intersection)

اینجاست که `intersection` وارد میدان می‌شود.
این تابع امکان ایجاد مجموعه‌فایلی را فراهم می‌کند که فقط شامل فایل‌هایی است که در _هر دو_ مجموعه‌فایل داده‌شده حضور دارند.

تمام فایل‌هایی را انتخاب کنید که هم توسط Git ردیابی شده‌اند *و* برای ساخت مرتبط هستند:

```{code-block} nix
:caption: package.nix
  sourceFiles =
    fs.intersection
      (fs.gitTracked ./.)
      (fs.unions [
        ./hello.txt
        ./world.txt
        ./build.sh
        ./src
      ]);
```

این همان خروجی روش دیگر را تولید خواهد کرد و بنابراین از یک نتیجه‌ی ساخت قبلی استفاده مجدد می‌کند:

```shell-session
$ nix-build
warning: Git tree '/home/user/fileset' is dirty
trace: - build.sh (regular)
trace: - hello.txt (regular)
trace: - src
trace:   - select.c (regular)
trace:   - select.h (regular)
trace: - world.txt (regular)
/nix/store/zl4n1g6is4cmsqf02dci5b2h5zd0ia4r-fileset
```

## نتیجه‌گیری

ما نمونه‌هایی را از نحوه‌ی استفاده از تمام توابع بنیادی مجموعه‌فایل‌ها نشان داده‌ایم.
برای موارد استفاده‌ی پیچیده‌تر، آن‌ها را می‌توان در صورت نیاز با یکدیگر ترکیب کرد.

برای مشاهده‌ی فهرست کامل و جزئیات بیشتر، به [مستندات مرجع `lib.fileset`](https://nixos.org/manual/nixpkgs/stable/#sec-functions-library-fileset) مراجعه کنید.
