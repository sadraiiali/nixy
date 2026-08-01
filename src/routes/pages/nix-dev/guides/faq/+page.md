# پرسش‌های متداول

## نیکس

### چگونه کد زبان Nix را به‌طور خودکار قالب‌بندی کنیم؟

[`nixfmt`](https://github.com/NixOS/nixfmt) قالب‌بندی‌کننده‌ی رسمی برای کد *Nix language* است.
لطفاً برای دستورالعمل‌های نصب به مخزن سورس آن مراجعه کنید.

از `nixfmt` [برای قالب‌بندی تمام کدها](https://github.com/NixOS/nixpkgs/blob/master/ci/default.nix) در *Nixpkgs* استفاده می‌شود.

### چگونه در زبان Nix بین مسیرها و رشته‌ها تبادل انجام دهیم (تبدیل کنیم)؟

راهنمای مرجع Nix را در بخش‌های [درون‌گذاری رشته](/pages/nix-manual/language/string-interpolation) و [عملگرها روی مسیرها و رشته‌ها](/pages/nix-manual/language/operators#string-concatenation) مطالعه کنید.

### چگونه وابستگی‌های معکوس یک بسته را بسازیم؟

```shell
$ nix-shell -p nixpkgs-review --run "nixpkgs-review wip"
```

### چگونه می‌توانم فایل‌های dotfiles را در \$HOME با استفاده از Nix مدیریت کنم؟

به &lt;https://github.com/nix-community/home-manager&gt; مراجعه کنید.

### روند توصیه‌شده برای ساخت بسته‌های سفارشی چیست؟

لطفاً [packaging-tutorial](/pages/nix-dev/tutorials/packaging-existing-software) را مطالعه کنید.

### چگونه از یک کلون از مخزن Nixpkgs برای به‌روزرسانی یا نوشتن بسته‌های جدید استفاده کنیم؟

لطفاً [packaging-tutorial](/pages/nix-dev/tutorials/packaging-existing-software) و [راهنمای مشارکت Nixpkgs](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md) را مطالعه کنید.

## NixOS

### چگونه برنامه‌های اجرایی غیر نیکس را اجرا کنیم؟

سیستم‌عامل NixOS نمی‌تواند به‌طور پیش‌فرض برنامه‌های اجرایی پیوند داده‌شده‌ی پویا که برای محیط‌های عمومی لینوکس در نظر گرفته شده‌اند را اجرا کند.
دلیل این امر آن است که بر اساس طراحی، این سیستم‌عامل نه مسیر کتابخانه سراسری دارد و نه از [استاندارد سلسله‌مراتب سیستم‌فایل](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) (FHS) پیروی می‌کند.

چند روش برای حل این عدم تطابق در انتظارات محیطی وجود دارد:

- از نسخه بسته‌بندی‌شده در Nixpkgs استفاده کنید (در صورتی که وجود داشته باشد).
  می‌توانید بسته‌های موجود را در &lt;https://search.nixos.org/packages&gt; جستجو کنید.

- یک عبارت Nix برای برنامه بنویسید تا آن را در پیکربندی خودتان بسته‌بندی کنید.

  رویکردهای متعددی برای این کار وجود دارد:
  - ساخت از روی کد منبع.

    بسیاری از برنامه‌های متن‌باز از نظر محل قرارگیری فایل‌هایشان در زمان کامپایل بسیار انعطاف‌پذیر هستند.
    برای آشنایی با این موضوع، [packaging-tutorial](/pages/nix-dev/tutorials/packaging-existing-software) را ببینید.
  - [هدر ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) برنامه را تغییر دهید تا با استفاده از [`autoPatchelfHook`](https://nixos.org/manual/nixpkgs/stable/#setup-hook-autopatchelfhook) شامل مسیر کتابخانه‌ها باشد.

    اگر ساخت از روی کد منبع امکان‌پذیر نیست، این کار را انجام دهید.
  - برنامه را طوری بپیچید که با استفاده از [`buildFHSEnv`](https://nixos.org/manual/nixpkgs/stable/#sec-fhs-environments) در یک محیط شبیه به FHS اجرا شود.

    این آخرین راه‌حل است، اما گاهی اوقات ضروری است؛ مثلاً اگر برنامه، سایر برنامه‌های اجرایی را بارگیری و اجرا کند.

- با استفاده از [`nix-ld`](https://github.com/Mic92/nix-ld) یک مسیر کتابخانه ایجاد کنید که فقط برای برنامه‌های بسته‌بندی‌نشده اعمال شود.
  این مورد را به `configuration.nix` خود اضافه کنید:

```nix
    programs.nix-ld.enable = true;
    programs.nix-ld.libraries = with pkgs; [
      # Add any missing dynamic libraries for unpackaged programs
      # here, NOT in environment.systemPackages
    ];
  ```

سپس دستور `nixos-rebuild switch` را اجرا کنید و برای انتشار متغیرهای محیطی جدید، از سیستم خارج شده و دوباره وارد شوید.
(این کار فقط هنگام فعال‌سازی `nix-ld` ضروری است؛ تغییرات کتابخانه‌های گنجانده‌شده بلافاصله پس از ساخت مجدد اعمال می‌شوند.)

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> ابزار `nix-ld` برای فایل‌های اجرایی ۳۲ بیتی روی ماشین‌های `x86_64` کار نمی‌کند.

- برنامه خود را در محیط شبیه به FHS که برای بسته Steam ساخته شده است، با استفاده از [`steam-run`](https://nixos.org/manual/nixpkgs/stable/#sec-steam-run) اجرا کنید:

```shell
  $ nix-shell -p steam-run --run "steam-run <command>"
  ```

### چگونه ISO خودم را بسازم؟

به &lt;http://nixos.org/nixos/manual/index.html#sec-building-image&gt; مراجعه کنید.

### چگونه به هر یک از ماشین‌ها در تست‌های NixOS متصل شوم؟

پچ زیر را اعمال کنید:

```diff
diff --git a/nixos/lib/test-driver/test-driver.pl b/nixos/lib/test-driver/test-driver.pl
index 8ad0d67..838fbdd 100644
--- a/nixos/lib/test-driver/test-driver.pl
+++ b/nixos/lib/test-driver/test-driver.pl
@@ -34,7 +34,7 @@ foreach my $vlan (split / /, $ENV{VLANS} || "") {
     if ($pid == 0) {
         dup2(fileno($pty->slave), 0);
         dup2(fileno($stdoutW), 1);
-        exec "vde_switch -s $socket" or _exit(1);
+        exec "vde_switch -tap tap0 -s $socket" or _exit(1);
     }
     close $stdoutW;
     print $pty "version\n";
```

و پس از آن شبکه `vde_switch` باید به صورت محلی قابل دسترسی باشد.

### چگونگی راه‌اندازی اولیه (Bootstrap) NixOS درون یک نصب موجود از لینوکس؟

چند ابزار برای این کار وجود دارد:

- &lt;https://github.com/nix-community/nixos-anywhere&gt;
- &lt;https://github.com/jeaye/nixos-in-place&gt;
- &lt;https://github.com/elitak/nixos-infect&gt;
- &lt;https://github.com/cleverca22/nix-tests/tree/master/kexec&gt;
