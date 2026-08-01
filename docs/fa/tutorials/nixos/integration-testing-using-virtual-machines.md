(integration-testing-vms)=

# تست یکپارچه‌سازی با ماشین‌های مجازی NixOS

## چه چیزی خواهید آموخت؟

این آموزش قابلیت‌های مجموعه‌ی بسته‌های نیکس (Nixpkgs) را برای تست کردن پیکربندی‌های NixOS معرفی می‌کند.
همچنین نشان می‌دهد چگونه سناریوهای تست توزیع‌شده که شامل چندین ماشین هستند را راه‌اندازی کنید.

## به چه چیزی نیاز دارید؟

- یک [نصب Nix](<install-nix>) فعال روی لینوکس یا [NixOS](https://nixos.org/manual/nixos/stable/index.html#sec-installation)
- دانش پایه‌ای از [زبان Nix](<reading-nix-language>)
- دانش پایه‌ای از [پیکربندی NixOS](<nixos-vms>)

## مقدمه

مجموعه‌ی بسته‌های نیکس (Nixpkgs) یک [محیط آزمایش](https://nixos.org/manual/nixos/stable/index.html#sec-nixos-tests) برای خودکارسازی تست یکپارچه‌سازی سیستم‌های توزیع‌شده فراهم می‌کند.
این محیط امکان تعریف تست‌ها را بر اساس مجموعه‌ای از پیکربندی‌های اعلانی (declarative) NixOS و استفاده از یک شل پایتون برای تعامل با آن‌ها از طریق [QEMU](https://www.qemu.org/) به عنوان بخشسمت سرور (Backend) فراهم می‌کند.
این تست‌ها به‌طور گسترده برای اطمینان از عملکرد صحیح NixOS استفاده می‌شوند، بنابراین به‌طور کلی به آن‌ها [تست‌های NixOS](https://nixos.org/manual/nixos/stable/index.html#sec-nixos-tests) می‌گویند.
آن‌ها را می‌توان خارج از NixOS و روی هر ماشین لینوکسی نوشته و اجرا کرد[^darwin].

[^darwin]: پشتیبانی از [اجرای تست‌های ماشین مجازی NixOS روی macOS](https://github.com/NixOS/nixpkgs/issues/108984) نیز پیاده‌سازی شده اما [در حال حاضر مستند نشده است](https://github.com/NixOS/nixpkgs/issues/254552).

ویژگی‌های طراحی Nix باعث می‌شود تست‌های یکپارچه‌سازی بازتولیدپذیر باشند، که این امر آن‌ها را در یک خط لوله ادغام مداوم (CI) بسیار باارزش می‌کند.

## تابع `testers.runNixOSTest`

تست‌های ماشین مجازی NixOS با استفاده از تابع `testers.runNixOSTest` تعریف می‌شوند.
الگوی تست‌های ماشین مجازی NixOS به این شکل است:

```nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.testers.runNixOSTest {
  name = "test-name";
  nodes = {
    machine1 = { config, pkgs, ... }: {
      # ...
    };
    machine2 = { config, pkgs, ... }: {
      # ...
    };
  };
  testScript = { nodes, ... }: ''
    # ...
  '';
}
```

تابع `testers.runNixOSTest` یک [ماژول](https://nixos.org/manual/nixos/stable/#sec-writing-modules) را برای مشخص کردن [گزینه‌های تست](https://nixos.org/manual/nixos/stable/index.html#sec-test-options-reference) دریافت می‌کند.
از آنجا که این ماژول فقط مقادیر پیکربندی را تنظیم می‌کند، می‌توان از نمادگذاری خلاصه‌شده‌ی ماژول استفاده کرد.

مقادیر پیکربندی زیر باید تنظیم شوند:

- [`name`](https://nixos.org/manual/nixos/stable/index.html#test-opt-name) نام تست را تعریف می‌کند.

- [`nodes`](https://nixos.org/manual/nixos/stable/index.html#test-opt-nodes) شامل مجموعه‌ای از پیکربندی‌های نام‌گذاری‌شده‌است، زیرا یک اسکریپت تست می‌تواند شامل بیش از یک ماشین مجازی باشد.
  هر ماشین مجازی از روی یک پیکربندی NixOS ساخته می‌شود.

- [`testScript`](https://nixos.org/manual/nixos/stable/index.html#test-opt-testScript) اسکریپت تست پایتون را، یا به صورت یک رشته‌ی تحت‌الفظی یا به صورت تابعی که یک صفت `nodes` را می‌گیرد، تعریف می‌کند.
  این اسکریپت تست پایتون می‌تواند از طریق نام‌های استفاده‌شده برای `nodes` به ماشین‌های مجازی دسترسی داشته باشد.
  این اسکریپت دارای دسترسی‌های کاربر ارشد (super user) در ماشین‌های مجازی است.
  در اسکریپت پایتون، هر ماشین مجازی از طریق شیء `machine` قابل دسترسی است.
  NixOS [متدهای](https://nixos.org/manual/nixos/stable/index.html#ssec-machine-objects) لازم برای اجرای تست‌ها روی این پیکربندی‌ها را فراهم می‌کند.

چارچوب تست به‌طور خودکار ماشین‌های مجازی را راه‌اندازی کرده و اسکریپت پایتون را اجرا می‌کند.

## مثال حداقلی

به عنوان یک تست حداقلی روی پیکربندی پیش‌فرض، بررسی می‌کنیم که آیا کاربران `root` و `alice` می‌توانند Firefox را اجرا کنند.
این مثال را از صفر می‌سازیم.

۱. از یک [نسخه‌ی سنجاق‌شده از Nixpkgs](ref-pinning-nixpkgs) استفاده کنید، و [گزینه‌های پیکربندی و اورلی‌ها را به طور صریح تنظیم کنید](nixpkgs-config) تا از بازنویسی غیرعمدی آن‌ها توسط پیکربندی سراسری جلوگیری شود:
```nix
   let
     nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
     pkgs = import nixpkgs { config = {}; overlays = []; };
   in

   pkgs.testers.runNixOSTest {
     # ...
   }
   ```

1. تست را با یک نام توصیفی برچسب‌گذاری کنید:
```nix
   name = "minimal-test";
   ```

1. از آنجا که این مثال تنها از یک ماشین مجازی استفاده می‌کند، نودی که مشخص می‌کنیم به‌سادگی `machine` نامیده می‌شود.
   این نام اختیاری است و می‌توان آن را آزادانه انتخاب کرد.
   به عنوان پیکربندی، از بخش‌های مرتبطِ پیکربندی پیش‌فرض استفاده می‌کنید [که در یک آموزش قبلی از آن استفاده کردیم](<nixos-vms>):
```nix
   nodes.machine = { config, pkgs, ... }: {
     users.users.alice = {
       isNormalUser = true;
       extraGroups = [ "wheel" ];
       packages = with pkgs; [
         firefox
         tree
       ];
     };

     system.stateVersion = "23.11";
   };
   ```

1. این اسکریپت تست است:
```python
   machine.wait_for_unit("default.target")
   machine.succeed("su -- alice -c 'which firefox'")
   machine.fail("su -- root -c 'which firefox'")
   ```

این اسکریپت پایتون به `machine` اشاره می‌کند که نام انتخاب‌شده برای پیکربندی ماشین مجازی استفاده‌شده در مجموعه ویژگی `nodes` است.

این اسکریپت تا زمانی که `systemd` به `default.target` برسد صبر می‌کند.
این اسکریپت از دستور `su` برای جابه‌جایی بین کاربران و از دستور `which` برای بررسی دسترسی کاربر به `firefox` استفاده می‌کند.
این اسکریپت انتظار دارد که دستور `which firefox` برای کاربر `alice` با موفقیت اجرا شود و برای `root` با شکست مواجه گردد.

این اسکریپت مقدار صفت `testScript` خواهد بود.

محتوای کامل فایل `minimal-test.nix` به شکل زیر است:

```nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.testers.runNixOSTest {
  name = "minimal-test";

  nodes.machine = { config, pkgs, ... }: {

    users.users.alice = {
      isNormalUser = true;
      extraGroups = [ "wheel" ];
      packages = with pkgs; [
        firefox
        tree
      ];
    };

    system.stateVersion = "23.11";
  };

  testScript = ''
    machine.wait_for_unit("default.target")
    machine.succeed("su -- alice -c 'which firefox'")
    machine.fail("su -- root -c 'which firefox'")
  '';
}
```

## اجرای تست‌ها

برای راه‌اندازی تمام ماشین‌ها و اجرای اسکریپت تست:

```shell-session
$ nix-build minimal-test.nix
```

...
    اسکریپت تست در ۱۰.۹۶ ثانیه به پایان رسید
    در حال پاکسازی
    در حال خاتمه دادن به ماشین (شناسه پردازه 10)
    (۰.۰۰ ثانیه)
    /nix/store/bx7z3imvxxpwkkza10vb23czhw7873w2-vm-test-run-minimal-test

## پوسته تعاملی پایتون در ماشین مجازی

هنگام توسعه تست‌ها یا زمانی که مشکلی رخ می‌دهد، ایجاد تغییرات تعاملی در تست یا دسترسی به یک ترمینال برای یک ماشین بسیار مفید است.

برای شروع یک جلسه تعاملی پایتون با چارچوب آزمایش:

```shell-session
$ $(nix-build -A driverInteractive minimal-test.nix)/bin/nixos-test-driver
```

در اینجا می‌توانید هر یک از عملیات‌های آزمایش را اجرا کنید.
صفت `testScript` را از فایل `minimal-test.nix` با استفاده از تابع `test_script()` اجرا کنید.

اگر ماشین مجازی هنوز راه‌اندازی نشده باشد، محیط آزمایش در اولین فراخوانی یک متد روی شیء `machine`، این کار را انجام می‌دهد.

اما همچنین می‌توانید راه‌اندازی ماشین مجازی را به صورت دستی با دستور زیر فعال کنید:

```shell-session
>>> machine.start()
```
برای یک نود خاص،

یا

```shell-session
>>> start_all()
```
برای تمام نودها.

شما می‌توانید با استفاده از دستور زیر وارد یک شل تعاملی روی ماشین مجازی شوید:

```shell-session
>>> machine.shell_interact()
```

و دستورات شل را اجرا کنید مانند:

```shell-session
uname -a
```

Linux server 5.10.37 #1-NixOS SMP Fri May 14 07:50:46 UTC 2021 x86_64 GNU/Linux

::::{dropdown} اجرای مجدد تست‌های موفق

<!-- FIXME: this should be a separate recipe that can be linked to, as it's a bit of knowledge one will need now and again. -->

از آنجا که نتایج تست در انبار Nix نگهداری می‌شوند، یک تست موفق کش (cache) می‌شود.
این یعنی تا زمانی که تنظیمات تست (پیکربندی گره و اسکریپت تست) از نظر معنایی یکسان باقی بماند، نیکس تست را بار دوم اجرا نخواهد کرد.
بنابراین، برای اجرای مجدد یک تست، باید نتیجه را حذف کرد.

اگر سعی کنید نتیجه را با استفاده از پیوند نمادین (symlink) حذف کنید، با خطای زیر مواجه خواهید شد:

```shell-session
nix-store --delete ./result
```

پیدا کردن ریشه‌های جمع‌کننده‌ی زباله (garbage collector)...
۰ مسیر انبار حذف شد، ۰.۰۰ مگابایت فضا آزاد شد
خطا: امکان حذف مسیر `/nix/store/4klj06bsilkqkn6h2sia8dcsi72wbcfl-vm-test-run-unnamed` وجود ندارد زیرا هنوز فعال است. برای اطلاع از دلیل آن، از دستور زیر استفاده کنید: nix-store --query --roots

در عوض، پیوند نمادین (symlink) را حذف کرده و تازه پس از آن نتیجه‌ی کش‌شده را حذف کنید:

```shell-session
rm ./result
nix-store --delete /nix/store/4klj06bsilkqkn6h2sia8dcsi72wbcfl-vm-test-run-unnamed
```

این کار را می‌توان با یک دستور نیز انجام داد:

```shell-session
result=$(readlink -f ./result) rm ./result && nix-store --delete $result
```
## تست‌ها با چندین ماشین مجازی

تست‌ها می‌توانند شامل چندین ماشین مجازی باشند، برای مثال جهت تست ارتباط کلاینت و سرور.

پیکربندی نمونه‌ی زیر شامل موارد زیر است:
- یک ماشین مجازی به نام `server` که [nginx](https://nginx.org/en/) را با پیکربندی پیش‌فرض اجرا می‌کند.
- یک ماشین مجازی به نام `client` که ابزار `curl` را برای ارسال درخواست HTTP در اختیار دارد.
- یک `testScript` که منطق تست را بین `client` و `server` هماهنگ می‌کند.

محتوای کامل فایل `client-server-test.nix` به شکل زیر است:

```{code-block}
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.testers.runNixOSTest {
  name = "client-server-test";

  nodes.server = { pkgs, ... }: {
    networking = {
      firewall = {
        allowedTCPPorts = [ 80 ];
      };
    };
    services.nginx = {
      enable = true;
      virtualHosts."server" = {};
    };
  };

  nodes.client = { pkgs, ... }: {
    environment.systemPackages = with pkgs; [
      curl
    ];
  };

  testScript = ''
    server.wait_for_unit("default.target")
    client.wait_for_unit("default.target")
    client.succeed("curl http://server/ | grep -o \"Welcome to nginx!\"")
  '';
}
```

اسکریپت تست مراحل زیر را انجام می‌دهد:
1) سرور را اجرا کرده و منتظر آماده شدن آن بمانید.
1) کلاینت را اجرا کرده و منتظر آماده شدن آن بمانید.
1) دستور `curl` را روی کلاینت اجرا کرده و از `grep` برای بررسی رشته بازگشتی مورد انتظار استفاده کنید.
   تست بر اساس مقدار بازگشتی موفق یا ناموفق می‌شود.

اجرای تست:

```shell-session
$ nix-build client-server-test.nix
```

## اطلاعات بیشتر در رابطه با تست‌های NixOS

- اجرای ماشین‌های مجازی تست یکپارچه‌سازی روی ادغام مداوم (CI) نیازمند شتاب‌دهی سخت‌افزاری است، که بسیاری از سرویس‌های ادغام مداوم از آن پشتیبانی نمی‌کنند.

  برای اجرای ماشین‌های مجازی تست یکپارچه‌سازی در [GitHub Actions](<github-actions>)، به بخش [نحوه غیرفعال کردن شتاب‌دهی سخت‌افزاری](https://github.com/cachix/install-nix-action#how-do-i-run-nixos-tests) مراجعه کنید.

- NixOS همراه با مجموعه بزرگی از تست‌ها ارائه می‌شود که می‌توانند به عنوان مثال‌های آموزشی عمل کنند.

  یک منبع الهام خوب [پل زدن Matrix با یک IRC](https://github.com/NixOS/nixpkgs/blob/master/nixos/tests/matrix/appservice-irc.nix) است.

<!-- TODO: move examples from https://wiki.nixos.org/wiki/NixOS_Testing_library to the NixOS manual and troubleshooting tips to nix.dev -->

## گام‌های بعدی

- [](module-system-deep-dive)
- [](bootable-iso-image)
- [](nixos-docker-images)
