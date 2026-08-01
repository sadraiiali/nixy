# <a id="ad-hoc-envs"></a> محیط‌های شل آنی (ad-hoc)

در یک محیط شل نیکس، می‌توانید بلافاصله از هر برنامه‌ای که با نیکس بسته‌بندی شده است استفاده کنید، بدون اینکه نیاز باشد آن را به طور دائم نصب کنید.

همچنین می‌توانید دستور احضار چنین شلی را با دیگران به اشتراک بگذارید، و این دستور روی تمام توزیع‌های لینوکس، WSL و macOS کار خواهد کرد[^1].

[^1]: همه بسته‌ها برای لینوکس و macOS پشتیبانی نمی‌شوند. به‌ویژه پشتیبانی از برنامه‌های گرافیکی ممکن است متغیر باشد.

## ایجاد یک محیط شل

هنگامی که [نیکس را نصب کردید](/pages/nix-dev/install-nix)، می‌توانید از آن برای ایجاد *محیط‌های شل* جدید با برنامه‌هایی که می‌خواهید استفاده کنید، بهره ببرید.

در این بخش، دو برنامه عجیب و غریب به نام‌های `cowsay` و `lolcat` را اجرا خواهید کرد که احتمالاً روی دستگاه خود نصب ندارید:

```shell
$ cowsay no can do
The program ‘cowsay’ is currently not installed.

$ echo no chance | lolcat
The program ‘lolcat’ is currently not installed.
```

از `nix-shell` با گزینه `-p` (`--packages`) استفاده کنید تا مشخص کنیم به بسته‌های `cowsay` و `lolcat` نیاز داریم:

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> اولین اجرای `nix-shell` برای این بسته‌ها ممکن است به دلیل بارگیری تمامی وابستگی‌ها کمی طول بکشد.

```shell
$ nix-shell -p cowsay lolcat
these 3 derivations will be built:
 /nix/store/zx1j8gchgwzfjn7sr4r8yxb7a0afkjdg-builder.pl.drv
 /nix/store/h9sbaa2k8ivnihw2czhl5b58k0f7fsfh-lolcat-100.0.1.drv
 ...

[nix-shell:~]$
```

درون شل نیکس (Nix shell)، می‌توانید از برنامه‌های ارائه‌شده توسط این بسته‌ها استفاده کنید:

```shell
[nix-shell:~]$ cowsay Hello, Nix! | lolcat
```

برای خروج از شل، `exit` را تایپ کنید یا `CTRL-D` را فشار دهید؛ در این صورت برنامه‌ها دیگر در دسترس نخواهند بود.

```shell
[nix-shell:~]$ exit
exit

$ cowsay no more
The program ‘cowsay’ is currently not installed.

$ echo all gone | lolcat
The program ‘lolcat’ is currently not installed.
```

## اجرای یک‌باره‌ی برنامه‌ها

با اجرای مستقیم هر برنامه می‌توانید سرعت را حتی بیشتر کنید:

```shell
$ nix-shell -p cowsay --run "cowsay Nix"
```

اگر دستور فقط شامل نام برنامه باشد، نیازی به نقل‌قول نیست:

```shell
$ nix-shell -p hello --run hello
```

## جستجوی بسته‌ها

چه چیزی را می‌توانید در یک محیط شل (Shell) قرار دهید؟
اگر به آن فکر کنید، احتمالاً بسته نیکس مربوط به آن وجود دارد.

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> نام برنامه‌ای را که می‌خواهید اجرا کنید در [search.nixos.org](https://search.nixos.org/packages) وارد کنید تا بسته‌هایی که آن را فراهم می‌کنند پیدا کنید.

برای مثال زیر، نام بسته‌های این برنامه‌ها را پیدا کنید:

- `git`
- `nvim`
- `npm`

در نتایج جستجو، هر آیتم نام بسته را نشان می‌دهد و جزئیات، برنامه‌های موجود را فهرست می‌کنند.[^2]

[^2]: نام یک بسته با نام یک برنامه یکسان نیست. بسیاری از بسته‌ها چندین برنامه، یا اگر کتابخانه باشند هیچ برنامه‌ای را فراهم نمی‌کنند. حتی برای بسته‌هایی که دقیقاً یک برنامه را فراهم می‌کنند، نام بسته و برنامه لزوماً یکسان نیست.

## <a id="run-any-program"></a> اجرای هر ترکیبی از برنامه‌ها

هنگامی که نام بسته را در اختیار داشتید، می‌توانید یک شل با آن بسته راه‌اندازی کنید.
آرگومان `-p` (`--packages`) می‌تواند چندین نام بسته را بپذیرد.

یک شل Nix را با بسته‌هایی که `git`، `nvim` و `npm` را فراهم می‌کنند راه‌اندازی کنید.
باز هم، اجرای اول ممکن است برای بارگیری تمام وابستگی‌ها کمی طول بکشد.

```shell
$ nix-shell -p git neovim nodejs
these 9 derivations will be built:
 /nix/store/7gz8jyn99kw4k74bgm4qp6z487l5ap06-packdir-start.drv
 /nix/store/d6fkgxc3b04m85wrhg6j0l5y0ray82l7-packdir-opt.drv
 /nix/store/da6njv7r0zzc2n54n2j54g2a5sbi4a5i-manifest.vim.drv
 /nix/store/zs4jb2ybr4rcyzwq0dagg9rlhlc368h6-builder.pl.drv
 /nix/store/g8sl2xnsshfrz9f39ki94k8p15vp3xd7-vim-pack-dir.drv
 /nix/store/jmxkg8b1psk52awsvfziy9nq6dwmxmjp-luajit-2.1.0-2022-10-04-env.drv
 /nix/store/kn83q8yk6ds74zgyklrjhvv5wkv5wmch-python3-3.10.9-env.drv
 /nix/store/m445wn3vizcgg7syna2cdkkws3kk1gq8-neovim-ruby-env.drv
 /nix/store/r2wa882mw99c311a4my7hcis9lq3kp3v-neovim-0.8.1.drv
these 151 paths will be fetched (186.43 MiB download, 1018.20 MiB unpacked):
 /nix/store/046zxlxhq4srm3ggafkymx794bn1jksc-bzip2-1.0.8
 /nix/store/0p1jxcb7b4p8jhhlf8qnjc4cqwy89460-unibilium-2.1.1
 /nix/store/0q4fpnqmg8liqraj7zidylcyd062f6z0-perl5.36.0-URI-5.05
 ...

[nix-shell:~]$
```

### <a id="check-package-version"></a> بررسی نسخه بسته (check-package-version)

بررسی کنید که نسخه‌ی مشخصی از این برنامه‌ها را که توسط نیکس ارائه شده‌اند در اختیار دارید، حتی اگر هر یک از آن‌ها را از قبل روی دستگاه خود نصب کرده بودید.

```shell
[nix-shell:~]$ which git
/nix/store/3cdi52xh6lk3h1fb51jkxs3p561p37wg-git-2.38.3/bin/git

[nix-shell:~]$ git --version
git version 2.38.3

[nix-shell:~]$ which nvim
/nix/store/ynskzgkf07lmrrs3cl2kzr9ah487lwab-neovim-0.8.1/bin/nvim

[nix-shell:~]$ nvim --version | head -1
NVIM v0.8.1

[nix-shell:~]$ which npm
/nix/store/q12w83z0i5pi1y0m6am7qmw1r73228sh-nodejs-18.12.1/bin/npm

[nix-shell:~]$ npm --version
8.19.2
```

## نشست‌های شل تو در تو

اگر موقتاً به یک برنامه اضافی نیاز دارید، می‌توانید یک شل Nix تو در تو اجرا کنید.
برنامه‌های ارائه‌شده توسط بسته‌های مشخص‌شده به محیط فعلی اضافه خواهند شد.

```shell
[nix-shell:~]$ nix-shell -p python3
this path will be fetched (11.42 MiB download, 62.64 MiB unpacked):
 /nix/store/pwy30a7siqrkki9r7xd1lksyv9fg4l1r-python3-3.10.11
copying path '/nix/store/pwy30a7siqrkki9r7xd1lksyv9fg4l1r-python3-3.10.11' from 'https://cache.nixos.org'...

[nix-shell:~]$ python --version
Python 3.10.11
```

برای بازگشت به محیط قبلی، طبق معمول از شل خارج شوید.

## <a id="towards-reproducibility"></a> در مسیر بازتولیدپذیری

این محیط‌های شل بسیار راحت هستند، اما مثال‌های ارائه‌شده تاکنون هنوز بازتولیدپذیر نیستند.
اجرای این دستورات روی ماشینی دیگر ممکن است نسخه‌های متفاوتی از بسته‌ها را دریافت کند، که این موضوع به زمان نصب Nix روی آن ماشین بستگی دارد.

منظور ما از بازتولیدپذیری چیست؟
یک مثال کاملاً بازتولیدپذیر، صرف‌نظر از زمان و مکان اجرای دستور، دقیقاً نتایج یکسانی را ارائه می‌دهد.
محیط فراهم‌شده هر بار کاملاً یکسان خواهد بود.

مثال زیر یک محیط کاملاً بازتولیدپذیر ایجاد می‌کند.
شما می‌توانید آن را در هر کجا و در هر زمانی اجرا کنید تا دقیقاً همان نسخه از `git` را دریافت کنید.

```shell
$ nix-shell -p git --run "git --version" --pure -I nixpkgs=https://github.com/NixOS/nixpkgs/tarball/2a601aafdc5605a5133a2ca506a34a3a73377247
...
git version 2.33.1
```

در اینجا سه مورد در جریان است:

1. `--run` [دستور Bash](https://www.gnu.org/software/bash/manual/bash.html#Shell-Commands) داده‌شده را در محیط ایجادشده توسط Nix اجرا می‌کند و پس از اتمام، خارج می‌شود.

 هر زمان که بخواهید به سرعت برنامه‌ای را که روی سیستم خود نصب ندارید اجرا کنید، می‌توانید از این قابلیت به همراه `nix-shell` استفاده کنید.

2. `--pure` هنگام اجرای شل، بیشتر متغیرهای محیطی تنظیم‌شده روی سیستم شما را کنار می‌گذارد.

 این یعنی فقط `git` ارائه‌شده توسط Nix در داخل آن شل در دسترس است.
 این کار برای دستورات تک‌خطی ساده مانند مثال مفید است.
 با این حال، هنگام توسعه، معمولاً می‌خواهید ویرایشگر و سایر ابزارهای خود را در دسترس داشته باشید.
 بنابراین توصیه می‌کنیم `--pure` را برای محیط‌های توسعه حذف کنید و تنها زمانی که به ایزوله‌سازی اضافی نیاز است، آن را اضافه کنید.

3. `-I` تعیین می‌کند که چه چیزی به عنوان منبع اعلامیه‌های بسته استفاده شود.

 در اینجا ما [یک نسخه خاص (Git revision) از nixpkgs](https://github.com/NixOS/nixpkgs/tree/2a601aafdc5605a5133a2ca506a34a3a73377247) را فراهم کرده‌ایم که هیچ شکی باقی نمی‌گذارد که کدام نسخه از بسته‌ها در آن مجموعه استفاده خواهد شد.

## مراجع

- [راهنمای Nix: `nix-shell`](/pages/nix-manual/command-ref/nix-shell) (یا دستور `man nix-shell` را اجرا کنید)
- [راهنمای Nix: گزینه `-I`](/pages/nix-manual/command-ref/opt-common#opt-I)

## گام‌های بعدی

- [reproducible-scripts](/pages/nix-dev/tutorials/first-steps/reproducible-scripts) استفاده از Nix برای اسکریپت‌های تکرارپذیر
- [reading-nix-language](/pages/nix-dev/tutorials/nix-language) یادگیری نحوه خواندن زبان Nix که برای اعلام بسته‌ها و پیکربندی‌ها استفاده می‌شود
- [declarative-reproducible-envs](/pages/nix-dev/tutorials/first-steps/declarative-shell) ایجاد محیط‌های شل تکرارپذیر با یک فایل پیکربندی اعلانی (declarative)
- [pinning-nixpkgs](/pages/nix-dev/tutorials/first-steps/towards-reproducibility-pinning-nixpkgs) یادگیری روش‌های مختلف مشخص کردن نسخه‌های دقیق منابع بسته

اگر آزمایش کردن Nix فعلاً برای شما به پایان رسیده است، ممکن است بخواهید با اجرای مثال‌ها، مقداری از فضای دیسک اشغال‌شده توسط نسخه‌های مختلف برنامه‌های بارگیری‌شده را آزاد کنید:

```shell
$ nix-collect-garbage
```
