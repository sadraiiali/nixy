# سرو کردن انبار Nix از طریق SSH

شما می‌توانید به Nix بگویید که به طور خودکار باینری‌های مورد نیاز را از یک انبار Nix راه دور از طریق SSH دریافت کند. برای مثال، دستور زیر Firefox را نصب می‌کند و اگر مسیرهای انبار موجود در بستهٔ بستهٔ (closure) مربوط به Firefox روی سرور `avalon` موجود باشند، آن‌ها را به صورت خودکار دریافت می‌کند:

```console
$ nix-env --install --attr nixpkgs.firefox --substituters ssh://alice@avalon
```

این روش مشابه جایگزین کش باینری است که Nix معمولاً از آن استفاده می‌کند، با این تفاوت که به جای HTTP از SSH استفاده می‌کند: اگر یک مسیر انبار `P` مورد نیاز باشد، Nix ابتدا بررسی می‌کند که آیا در انبار Nix روی `avalon` موجود است یا خیر. اگر موجود نباشد، به استفاده از جایگزین کش باینری و سپس ساخت از روی کد منبع بازمی‌گردد.

> **نکته**
>
> جایگزین SSH در حال حاضر به شما اجازه نمی‌دهد که عبارت عبور (passphrase) SSH را به صورت تعاملی وارد کنید. بنابراین، باید از `ssh-add` برای بارگذاری کلید خصوصی رمزگشایی‌شده در `ssh-agent` استفاده کنید.

همچنین می‌توانید کلوژر (closure) یک مسیر انبار را بدون نصب آن در پروفایل خود کپی کنید، به عنوان مثال:

```console
$ nix-store --realise /nix/store/m85bxg…-firefox-34.0.5 --substituters
ssh://alice@avalon
```

این اساساً معادل انجام کار زیر است

```console
$ nix-copy-closure --from alice@avalon
/nix/store/m85bxg…-firefox-34.0.5
```

شما می‌توانید از ویژگی *فرمان اجباری* (forced command) در SSH برای راه‌اندازی یک حساب کاربری محدود جهت دسترسی به جایگزین‌کننده (substituter) SSH استفاده کنید که به شما امکان دسترسی فقط‌خواندنی به انبار Nix محلی را می‌دهد و نه چیز بیشتر. برای مثال، خطوط زیر را به `sshd_config` اضافه کنید تا کاربر `nix-ssh` محدود شود:

    Match User nix-ssh
      AllowAgentForwarding no
      AllowTcpForwarding no
      PermitTTY no
      PermitTunnel no
      X11Forwarding no
      ForceCommand nix-store --serve
    Match All

در NixOS، می‌توانید همین کار را با افزودن موارد زیر به فایل `configuration.nix` خود انجام دهید:

```nix
nix.sshServe.enable = true;
nix.sshServe.keys = [ "ssh-dss AAAAB3NzaC1k... bob@example.org" ];
```

که در آن خط دوم، کلیدهای عمومی کاربرانی را فهرست می‌کند که اجازه اتصال دارند.
