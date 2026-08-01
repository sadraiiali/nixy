# <a id="distributed-build-setup-tutorial"></a> راه‌اندازی ساخت‌های توزیع‌شده

نیکس می‌تواند با پخش کردن کار روی چندین کامپیوتر به‌طور هم‌زمان، سرعت ساخت‌ها را افزایش دهد.

## مقدمه

در این آموزش، یک ماشین ساخت مجزا را راه‌اندازی می‌کنید و ماشین محلی خود را به‌گونه‌ای پیکربندی می‌کنید که ساخت‌ها را به آن محول کند.

### چه چیزی خواهید آموخت؟

شما یاد خواهید گرفت که چگونه:
- یک کاربر جدید برای دسترسی ساخت راه دور از یک ماشین محلی به سازنده راه دور ایجاد کنید
- سازنده‌های راه دور را با یک پیکربندی پایدار تنظیم کنید
- اتصال و احراز هویت سازنده راه دور را آزمایش کنید
- ماشین محلی را برای توزیع خودکار ساخت‌ها پیکربندی کنید

### به چه چیزهایی نیاز دارید؟

- آشنایی با [زبان Nix](/pages/nix-dev/tutorials/nix-language)
- آشنایی با [module-system-tutorial](/pages/nix-dev/tutorials/module-system)

- یک *ماشین محلی* (مثال نام هاست: `localmachine`)

  کامپیوتری [که Nix روی آن نصب شده است](/pages/nix-dev/install-nix) و ساخت‌ها را بین ماشین‌های دیگر توزیع می‌کند.

- یک *ماشین راه دور* (مثال نام هاست: `remotemachine`)

  کامپیوتری که NixOS را اجرا می‌کند و کارهای ساخت را از *ماشین محلی* می‌پذیرد.
  برای راه‌اندازی یک سیستم NixOS راه دور، [provisioning-remote-machines-tutorial](/pages/nix-dev/tutorials/nixos/provisioning-remote-machines) را دنبال کنید.

### چقدر زمان می‌برد؟

- ۲۵ دقیقه

## ایجاد یک جفت کلید SSH

دیمن Nix در *ماشین محلی* به عنوان کاربر `root` اجرا می‌شود و برای احراز هویت خود در ماشین‌های راه دور به فایل کلید *خصوصی* نیاز دارد.
*ماشین راه دور* برای تشخیص *ماشین محلی* به کلید *عمومی* نیاز خواهد داشت.

روی *ماشین محلی*، دستور زیر را به عنوان `root` اجرا کنید تا یک جفت کلید SSH ایجاد شود:

```shell
# ssh-keygen -f /root/.ssh/remotebuild
```

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> نام و محل قرارگیری فایل‌های جفت کلید را می‌توان به دلخواه انتخاب کرد.

## <a id="set-up-remote-builder"></a> راه‌اندازی سازنده راه دور

در پوشه پیکربندی NixOS *ماشین راه دور*، فایل `remote-builder.nix` را ایجاد کنید:

```nix
{
  users.users.remotebuild = {
    isSystemUser = true;
    group = "remotebuild";
    useDefaultShell = true;

    openssh.authorizedKeys.keyFiles = [ ./remotebuild.pub ];
  };

  users.groups.remotebuild = {};

  nix.settings.trusted-users = [ "remotebuild" ];
}
```

فایل `remotebuild.pub` را در این پوشه کپی کنید.

این ماژول پیکربندی یک کاربر جدید به نام `remotebuild` بدون پوشه خانه ایجاد می‌کند.
کاربر `root` روی *ماشین محلی* قادر خواهد بود با استفاده از کلید SSH تولیدشده‌ی قبلی، از طریق SSH به سازنده راه دور وارد شود.

ماژول جدید NixOS را به پیکربندی موجودِ *ماشین راه دور* اضافه کنید:

```nix
{
  imports = [
    ./remote-builder.nix
  ];

  # ...
}
```

پیکربندی جدید را به عنوان کاربر root فعال کنید:

```shell
nixos-rebuild switch --no-flake --target-host root@remotemachine
```

### تست احراز هویت

مطمئن شوید که اتصال SSH و احراز هویت به درستی کار می‌کنند.
روی *ماشین محلی*، به عنوان `root` اجرا کنید:

```shell
# ssh remotebuild@remotemachine -i /root/.ssh/remotebuild "echo hello"
hello
```

اگر پیام `hello` قابل مشاهده باشد، احراز هویت بهران انجام شده است.

این ورود آزمایشی همچنین کلید هاست سازنده راه دور را به فایل `/root/.ssh/known_hosts` ماشین محلی اضافه می‌کند.
ورودهای بعدی توسط بررسی‌های کلید هاست متوقف نخواهند شد.

## <a id="set-up-distributed-builds"></a> راه‌اندازی ساخت‌های توزیع‌شده

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> اگر *ماشین محلی* شما NixOS را اجرا می‌کند، از این بخش صرف‌نظر کنید و [Nix را از طریق گزینه‌های ماژول پیکربندی کنید](#distributed-builds-config-nixos).

Nix را به عنوان کاربر `root` با افزودن موارد زیر به [فایل پیکربندی Nix](/pages/nix-manual/command-ref/conf-file-prefix) پیکربندی کنید تا از سازنده راه دور استفاده کند:

```
# cat << EOF >> /etc/nix/nix.conf
builders = ssh-ng://remotebuild@remotebuilder $(nix-instantiate --eval -E builtins.currentSystem) /root/.ssh/remotemachine - - nixos-test,big-parallel,kvm
builders-use-substitutes = true
```

**توضیح مفصل**
خط اول ماشین راه دور را به عنوان یک سازنده راه دور با مشخص کردن موارد زیر ثبت می‌کند:
- پروتکل، کاربر و نام هاست
- [نوع سیستم](/pages/nix-manual/command-ref/conf-file-prefix#conf-system) *ماشین محلی*

  این کار وظایف مربوط به آن نوع سیستم را به *ماشین راه دور* محول می‌کند.

- مکان کلید SSH
- فهرستی از [قابلیت‌های پشتیبانی‌شده سیستم](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features)

  این فهرست خاص باید مشخص شود تا بتوان ساخت کامپایلرها و اجرای [ماشین‌های مجازی تست یکپارچه‌سازی](/pages/nix-dev/tutorials/nixos/integration-testing-using-virtual-machines) را به ماشین‌های راه دور محول کرد.

برای جزئیات بیشتر، [مستندات مرجع مربوط به تنظیمات `builders`](/pages/nix-manual/command-ref/conf-file-prefix#conf-builders) را ببینید.

خط دوم به تمام سازندگان راه دور دستور می‌دهد که وابستگی‌ها را به جای *ماشین محلی*، از کش‌های باینری خودشان دریافت کنند.
این فرض در نظر گرفته می‌شود که سرعت اتصال به اینترنت سازندگان راه دور حداقل به اندازه سرعت اتصال به اینترنت ماشین محلی است.

برای فعال کردن این پیکربندی، خدمت پس‌زمینه Nix را مجدداً راه‌اندازی کنید:

**Linux**
در لینوکس با `systemd`، به عنوان کاربر `root` اجرا کنید:

```shell
# systemctl restart nix-daemon.service
```

**macOS**
در macOS، به عنوان `root` اجرا کنید:

```shell
# sudo launchctl stop org.nixos.nix-daemon
# sudo launchctl start org.nixos.nix-daemon
```
<a id="distributed-builds-config-nixos"></a>

اگر *ماشین محلی* شما NixOS را اجرا می‌کند، در پوشه پیکربندی آن، فایل `distributed-builds.nix` را ایجاد کنید:

```nix
{ pkgs, ... }:
{
  nix.distributedBuilds = true;
  nix.settings.builders-use-substitutes = true;

  nix.buildMachines = [
    {
      hostName = "remotebuilder";
      sshUser = "remotebuild";
      sshKey = "/root/.ssh/remotebuild";
      system = pkgs.stdenv.hostPlatform.system;
      supportedFeatures = [ "nixos-test" "big-parallel" "kvm" ];
    }
  ];
}
```

**توضیح تفصیلی**
این ماژول پیکربندی، بیلدهای توزیع‌شده را فعال کرده و سازنده راه دور را اضافه می‌کند و موارد زیر را مشخص می‌کند:
- نام هاست SSH و نام کاربری
- مکان کلید SSH
- [نوع سیستم](/pages/nix-manual/command-ref/conf-file-prefix#conf-system) *ماشین محلی*

  این کار وظایف مربوط به آن نوع سیستم را به *ماشین راه دور* محول می‌کند.

- فهرستی از [ویژگی‌های سیستم پشتیبانی‌شده](/pages/nix-manual/command-ref/conf-file-prefix#conf-system-features)

  این فهرست خاص باید مشخص شود تا بتوان ساخت کامپایلرها و اجرای [ماشین‌های مجازی تست یکپارچه‌سازی](/pages/nix-dev/tutorials/nixos/integration-testing-using-virtual-machines) را به ماشین‌های راه دور محول کرد.

برای جزئیات بیشتر، به [مستندات گزینه NixOS درمورد `nix.buildMachines`](https://search.nixos.org/options?query=nix.buildMachines) مراجعه کنید.

گزینه `builders-use-substitutes` به تمام سازنده‌های راه دور دستور می‌دهد تا به‌جای دریافت وابستگی‌ها از *ماشین محلی*، آن‌ها را از کش‌های باینری خودشان دریافت کنند.
این فرض را در نظر می‌گیرد که اتصال اینترنت سازنده‌های راه دور حداقل به سرعت اتصال اینترنت ماشین محلی است.

ماژول جدید NixOS را به پیکربندی ماشین موجود اضافه کنید:

```nix
{
  imports = [
    ./distributed-builds.nix
  ];

  # ...
}
```

پیکربندی جدید را به عنوان `root` فعال کنید:

```shell
# nixos-rebuild switch
```
## تست بیلدهای توزیع‌شده

تلاش برای ساخت یک درایویشن جدید روی *ماشین محلی*:

```shell
$ nix-build --max-jobs 0 -E "$(cat << EOF
(import <nixpkgs> {}).writeText "test" "$(date)"
EOF
)"
this derivation will be built:
  /nix/store/9csjdxv6ir8ccnjl6ijs36izswjgchn0-test.drv
building '/nix/store/9csjdxv6ir8ccnjl6ijs36izswjgchn0-test.drv' on 'ssh://remotebuilder'...
copying 0 paths...
copying 1 paths...
copying path '/nix/store/hvj5vyg4723nly1qh5a8daifbi1yisb3-test' from 'ssh://remotebuilder'...
/nix/store/hvj5vyg4723nly1qh5a8daifbi1yisb3-test
```

درایویشن حاصل با هر بار فراخوانی تغییر می‌کند؛ زیرا به زمان فعلی سیستم وابسته است و بنابراین هرگز نمی‌تواند در کش محلی وجود داشته باشد.
[آرگومان خط فرمان `--max-jobs 0`](/pages/nix-manual/command-ref/conf-file-prefix#conf-max-jobs) باعث می‌شود Nix آن را روی سازنده راه دور بسازد.

آخرین خط خروجی حاوی مسیر خروجی است و نشان می‌دهد که توزیع ساخت همان‌طور که انتظار می‌رود کار می‌کند.

## بهینه‌سازی پیکربندی سازنده راه دور

برای به حداکثر رساندن موازی‌سازی، فعال کردن جمع‌آوری زباله (garbage collection) خودکار، و جلوگیری از مصرف تمام حافظه توسط ساخت‌های Nix، خطوط زیر را به ماژول پیکربندی `remote-builder.nix` خود اضافه کنید:

```diff
 {
   users.users.remotebuild = {
     isNormalUser = true;
     createHome = false;
     group = "remotebuild";

     openssh.authorizedKeys.keyFiles = [ ./remotebuild.pub ];
   };

   users.groups.remotebuild = {};

-  nix.settings.trusted-users = [ "remotebuild" ];
+  nix = {
+    nrBuildUsers = 64;
+    settings = {
+      trusted-users = [ "remotebuild" ];
+
+      min-free = 10 * 1024 * 1024;
+      max-free = 200 * 1024 * 1024;

+      max-jobs = "auto";
+      cores = 0;
+    };
+  };

+  systemd.services.nix-daemon.serviceConfig = {
+    MemoryAccounting = true;
+    MemoryMax = "90%";
+    OOMScoreAdjust = 500;
+  };
}
```

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> برای کسب اطلاعات بیشتر درباره گزینه‌های موجود در [`nix.settings`](https://search.nixos.org/options?show=nix.settings)، به [راهنمای مرجع Nix](/pages/nix-manual/command-ref/conf-file-prefix) مراجعه کنید.

سازنده‌های راه دور می‌توانند ویژگی‌های عملکردی متفاوتی داشته باشند.
برای هر مورد در `nix.buildMachines`، صفت‌های `maxJobs`، `speedFactor` و `supportedFeatures` را برای هر سازنده راه دور به درستی تنظیم کنید.
این کار به Nix روی *ماشین محلی* کمک می‌کند تا ساخت‌ها را بهینه‌ترین شکل ممکن توزیع کند.

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> برای جزئیات بیشتر به [مستندات گزینه NixOS درباره `nix.buildMachines`](https://search.nixos.org/options?query=nix.buildMachines) مراجعه کنید.

فیلد `nix.buildMachines.*.publicHostKey` را روی کلید هاست عمومی هر سازنده راه دور تنظیم کنید تا توزیع ساخت در برابر سناریوهای حمله مرد میانی ایمن شود.

## گام‌های بعدی

- [custom-binary-cache](/pages/nix-dev/guides/recipes/add-binary-cache) روی هر سازنده راه دور
- [post-build-hooks](/pages/nix-dev/guides/recipes/post-build-hook) برای بارگذاری آبجکت‌های انبار به یک کش باینری

برای راه‌اندازی چندین سازنده، دستورالعمل‌های بخش [set-up-remote-builder](#set-up-remote-builder) را برای هر سازنده راه دور تکرار کنید.
تمام سازنده‌های راه دور جدید را به صفت `nix.buildMachines` که در بخش [set-up-distributed-builds](#set-up-distributed-builds) نشان داده شده است، اضافه کنید.

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> ماشین‌های ساخت راه دور را به گونه‌ای پیکربندی کنید که [میزبانی یک کش باینری](/pages/nix-dev/tutorials/nixos/binary-cache-setup) را بر عهده داشته باشند و از آن‌ها به عنوان [کش‌های باینری ترجیحی](/pages/nix-dev/guides/recipes/add-binary-cache) برای کاهش ترافیک خارجی خود استفاده کنید.

## جایگزین‌ها

- [nixbuild.net](https://nixbuild.net) - سازنده‌های راه دور Nix به عنوان یک سرویس
- [Hercules CI](https://hercules-ci.com/) - ادغام مداوم با توزیع خودکار ساخت
- [garnix](https://garnix.io/) - ادغام مداوم میزبانی‌شده با توزیع ساخت

## مراجع

- [راهنمای مرجع Nix: تنظیمات مربوط به بیلدهای توزیع‌شده](/pages/nix-manual/command-ref/conf-file-prefix#conf-builders)
