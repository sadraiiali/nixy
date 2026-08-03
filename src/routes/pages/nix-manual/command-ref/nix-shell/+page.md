# 8.3.2. nix-shell

## نام

`nix-shell` - راه‌اندازی یک شل تعاملی بر اساس یک عبارت نیکس (Nix expression)

## خلاصه دستور

```text
nix-shell
  [--arg name value]
  [--argstr name value]
  [{--attr | -A} attrPath]
  [--command cmd]
  [--run cmd]
  [--exclude regexp]
  [--pure]
  [--keep name]
  {{--packages | -p} {packages | expressions} … | [path]}
```

## رفع ابهام
این صفحه راهنما (man page) دستور `nix-shell` را توصیف می‌کند که با دستور `nix shell` متفاوت است. برای مستندات مربوط به مورد دوم، دستور `nix shell --help` را اجرا کنید یا به `man nix3-env-shell` مراجعه کنید.

## توضیحات
دستور `nix-shell` وابستگی‌های derivation مشخص‌شده را می‌سازد، اما خود derivation را نمی‌سازد. سپس یک شل تعاملی را راه‌اندازی می‌کند که در آن تمام متغیرهای محیطی تعریف‌شده توسط *مسیر* derivation روی مقادیر متناظرشان تنظیم شده‌اند و اسکریپت `$stdenv/setup` منبع‌دهی (source) شده است. این کار برای بازتولید کردن محیط یک derivation جهت توسعه مفید است.

اگر *مسیر* (`path`) داده نشده باشد، `nix-shell` به‌طور پیش‌فرض از فایل `shell.nix` (در صورت وجود) و در غیر این صورت از `default.nix` استفاده می‌کند.

اگر *مسیر* با `http://` یا `https://` شروع شود، به عنوان URL یک فایل فشرده (tarball) تفسیر می‌شود که بارگیری شده و در یک مکان موقت استخراج می‌شود. فایل فشرده باید شامل یک پوشه سطح بالای منفرد باشد که حداقل حاوی فایلی به نام `default.nix` است.

اگر derivation متغیر `shellHook` را تعریف کند، پس از منبع‌دهی `$stdenv/setup` اجرا خواهد شد. از آنجا که این قلاب (hook) توسط ساخت‌های معمولی Nix اجرا نمی‌شود، به شما اجازه می‌دهد تا مقداردهی اولیه‌ی مختص `nix-shell` را انجام دهید. برای مثال، صفت derivation

```nix
shellHook =
  ''
    echo "Hello shell"
    export SOME_API_TOKEN="$(cat ~/.config/some-app/api-token)"
  '';
```

باعث می‌شود `nix-shell` عبارت `Hello shell` را چاپ کند و متغیر محیطی `SOME_API_TOKEN` را روی مقدار پیکربندی‌شده توسط کاربر تنظیم کند.

## گزینه‌ها
تمام گزینه‌هایی که در اینجا فهرست نشده‌اند، به `nix-store --realise` منتقل می‌شوند، به استثنای `--arg` و `--attr` / `-A` که به `nix-instantiate` فرستاده می‌شوند.

- `--command` *cmd*

  در محیط درایویشن، دستور شل *cmd* را اجرا کنید. این دستور در یک شل تعاملی اجرا می‌شود. (برای استفاده از یک شل غیرتعاملی، به‌جای آن از `--run` استفاده کنید.) با این حال، یک فراخوانی به `exit` به طور ضمنی به دستور اضافه می‌شود، بنابراین شل پس از اجرای دستور خارج خواهد شد. برای جلوگیری از این امر، `return` را در انتهای آن اضافه کنید؛ مثلاً `--command "echo Hello; return"` عبارت `Hello` را چاپ کرده و سپس شما را وارد شل تعاملی می‌کند. این کار می‌تواند برای انجام هرگونه مقداردهی اولیه اضافی مفید باشد.

- `--run` *cmd*

  مشابه `--command` است، اما دستور را در یک شل غیرتعاملی اجرا می‌کند. این بدان معناست (از جمله موارد دیگر) که اگر هنگام اجرای دستور کلیدهای Ctrl-C را فشار دهید، شل خارج می‌شود.

- `--exclude` *regexp*

  هیچ‌یک از وابستگی‌هایی را که مسیر انبار آن‌ها با عبارت منظم *regexp* مطابقت دارد، نسازید. این گزینه ممکن است چندین بار مشخص شود.

- `--pure`

  اگر این پرچم مشخص شود، محیط قبل از شروع شل تعاملی تقریباً به طور کامل پاکسازی می‌شود، بنابراین محیطی را دریافت می‌کنید که شباهت بیشتری به ساخت «واقعی» نیکس دارد. چند متغیر، به ویژه `HOME`، `USER` و `DISPLAY`، حفظ می‌شوند. توجه داشته باشید که شل مورد استفاده برای اجرای دستورات از [`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL) / `&lt;nixpkgs&gt;` از `NIX_PATH` به دست می‌آید و بنابراین تحت تأثیر `--pure` قرار نمی‌گیرد.

- `--packages` / `-p` *packages*…

  محیطی را راه‌اندازی کنید که در آن بسته‌های مشخص‌شده موجود باشند. آرگومان‌های خط فرمان به عنوان نام صفت‌ها در مجموعه‌ی بسته‌های نیکس تفسیر می‌شوند. بنابراین، `nix-shell --packages libjpeg openjdk` شلی را شروع می‌کند که در آن بسته‌های مشخص‌شده با نام صفت‌های `libjpeg` و `openjdk` موجود هستند.

- `-i` *interpreter*

  مفسر اسکریپت زنجیره‌ای که توسط `nix-shell` فراخوانی می‌شود. فقط در اسکریپت‌های `#!` (که در ادامه توضیح داده شده‌اند) قابل استفاده است.

- `--keep` *name*

  هنگامی که یک شل `--pure` راه‌اندازی می‌شود، متغیرهای محیطی فهرست‌شده را نگه دارید.

## متغیرهای محیطی
- <span id="env-NIX_BUILD_SHELL">[`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL)</span>

  شل مورد استفاده برای راه‌اندازی محیط تعاملی.
  به طور پیش‌فرض روی `bash` مربوط به `bashInteractive` یافت‌شده در `&lt;nixpkgs&gt;` تنظیم می‌شود، و در صورت پیدا نشدن، به `bash` موجود در `PATH` بازمی‌گردد.

  > **نکته**
  >
  > شلی که با استفاده از این روش به دست می‌آید لزوماً ممکن است با هیچ‌یک از شل‌های درخواست‌شده در *path* یکسان نباشد.

  

  > **مثال**
  >
  > با وجود `--pure`، این فراخوانی به یک محیط شل کاملاً بازتولیدپذیر منجر نخواهد شد:
  >

> ```nix
> #!/usr/bin/env -S nix-shell --pure
> let
>   pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/854fdc68881791812eddd33b2fed94b954979a8e.tar.gz") {};
> in
> pkgs.mkShell {
>   buildInputs = pkgs.bashInteractive;
> }
> ```

## مثال‌ها
برای ساخت وابستگی‌های بسته Pan و راه‌اندازی یک شل تعاملی که در آن ساخته شود:

```shell
$ nix-shell '<nixpkgs>' --attr pan
[nix-shell]$ eval ${unpackPhase:-unpackPhase}
[nix-shell]$ cd $sourceRoot
[nix-shell]$ eval ${patchPhase:-patchPhase}
[nix-shell]$ eval ${configurePhase:-configurePhase}
[nix-shell]$ eval ${buildPhase:-buildPhase}
[nix-shell]$ ./pan/gui/pan
```

دلیل استفاده از فرم `eval $`در اینجا این است که آن دسته از بسته‌هایی که این فازها را بازنویسی (override) می‌کنند، مقادیر بازنویسی‌شده را از طریق صادرات (export) متغیر محیطی با همین نام انجام می‌دهند.
در اینجا به Bash گفته می‌شود که یا محتویات`configurePhase` را ارزیابی کند (اگر به عنوان یک متغیر وجود داشته باشد)، و در غیر این صورت، تابع `configurePhase` را ارزیابی کند.

برای پاکسازی اولیه محیط و انجام مقداری مقداردهی اولیه خودکار اضافی برای شل تعاملی:

```shell
$ nix-shell '<nixpkgs>' --attr pan --pure \
    --command 'export NIX_DEBUG=1; export NIX_CORES=8; return'
```

عبارت‌های Nix را همچنین می‌توان با استفاده از پرچم‌های `-E` و `-p` در خط فرمان ارائه داد. برای مثال، دستور زیر یک شل حاوی بسته‌های `sqlite` و `libX11` را راه‌اندازی می‌کند:

```shell
$ nix-shell --expr 'with import <nixpkgs> { }; runCommand "dummy" { buildInputs = [ sqlite xorg.libX11 ]; } ""'
```

یک روش کوتاه‌تر برای انجام همین کار عبارت است از:

```shell
$ nix-shell --packages sqlite xorg.libX11
[nix-shell]$ echo $NIX_LDFLAGS
… -L/nix/store/j1zg5v…-sqlite-3.8.0.2/lib -L/nix/store/0gmcz9…-libX11-1.6.1/lib …
```

توجه داشته باشید که `-p` چندین عبارت کامل Nix را که در `buildInputs = [ ... ]` نشان‌داده‌شده در بالا معتبر هستند می‌پذیرد، و محدود به نام بسته‌ها نیست. بنابراین، دستور زیر نیز معتبر است:

```shell
$ nix-shell --packages sqlite 'git.override { withManual = false; }'
```

پرچم `-p` به جستجوی Nixpkgs در مسیر جستجو می‌پردازد. می‌توانید با ارسال `-I` یا تنظیم متغیر محیطی `NIX_PATH` آن را بازنویسی کنید. برای مثال، دستور زیر یک شل حاوی بسته Pan از یک کامیت (revision) مشخص از Nixpkgs را در اختیار شما قرار می‌دهد:

```shell
$ nix-shell --packages pan -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/8a3eea054838b55aca962c3fbde9c83c102b8bf2.tar.gz

[nix-shell:~]$ pan --version
Pan 0.139
```

## استفاده به عنوان مفسر `#!
شما می‌توانید از `nix-shell` به عنوان یک مفسر اسکریپت استفاده کنید تا به اسکریپت‌های نوشته‌شده با زبان‌های دلخواه اجازه دهید وابستگی‌های خود را از طریق Nix دریافت کنند. این کار با آغاز کردن اسکریپت با خطوط زیر انجام می‌شود:

```bash
#! /usr/bin/env nix-shell
#! nix-shell -i real-interpreter --packages packages
```

که در آن *real-interpreter* مفسر اسکریپت «واقعی» است که توسط `nix-shell` پس از دریافت وابستگی‌ها و مقداردهی اولیه محیط فراخوانی خواهد شد و *packages* نام صفت‌های وابستگی‌ها در Nixpkgs هستند.

خطوطی که با `#! nix-shell` شروع می‌شوند، گزینه‌های `nix-shell` را مشخص می‌کنند (به بالا مراجعه کنید). توجه داشته باشید که نمی‌توانید بنویسید `#! /usr/bin/env nix-shell -i ...`، زیرا بسیاری از سیستم‌عامل‌ها تنها اجازه یک آرگومان را در خطوط `#!` می‌دهند.

به عنوان مثال، در اینجا یک اسکریپت پایتون وجود دارد که به پایتون و بسته `prettytable` وابسته است:

```python
#! /usr/bin/env nix-shell
#! nix-shell -i python3 --packages python3 python3Packages.prettytable

import prettytable

## Print a simple table.
t = prettytable.PrettyTable(["N", "N^2"])
for n in range(1, 10): t.add_row([n, n * n])
print(t)
```

به همین ترتیب، اسکریپت Perl زیر مشخص می‌کند که به Perl و بسته‌های `HTML::TokeParser::Simple`، `LWP` و `LWP::Protocol::Https` نیاز دارد:

```perl
#! /usr/bin/env nix-shell
#! nix-shell -i perl 
#! nix-shell --packages perl 
#! nix-shell --packages perlPackages.HTMLTokeParserSimple 
#! nix-shell --packages perlPackages.LWP
#! nix-shell --packages perlPackages.LWPProtocolHttps

use HTML::TokeParser::Simple;

## Fetch nixos.org and print all hrefs.
my $p = HTML::TokeParser::Simple->new(url => 'https://nixos.org/');

while (my $token = $p->get_tag("a")) {
    my $href = $token->get_attr("href");
    print "$href\n" if $href;
}
```

گاهی اوقات لازم است یک عبارت Nix ساده را برای سفارشی‌سازی یک بسته مانند Terraform ارسال کنید:

```bash
#! /usr/bin/env nix-shell
#! nix-shell -i bash --packages 'terraform.withPlugins (plugins: [ plugins.openstack ])'

terraform apply
```

> **توجه**
>
> هنگام ارسال یک عبارت سادهٔ Nix در یک شِبَنگ (shebang) مربوط به nix-shell، باید از نقل‌قول‌های تکی یا جفت (`'`, `"`) استفاده کنید.

در نهایت، با استفاده از ادغام چندین شِبَنگ nix-shell، اسکریپت Haskell زیر از یک شاخهٔ خاص از Nixpkgs/NixOS (شاخه پایدار 20.03) استفاده می‌کند:

```haskell
#! /usr/bin/env nix-shell
#! nix-shell -i runghc --packages 'haskellPackages.ghcWithPackages (ps: [ps.download-curl ps.tagsoup])'
#! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-20.03.tar.gz

import Network.Curl.Download
import Text.HTML.TagSoup
import Data.Either
import Data.ByteString.Char8 (unpack)

-- Fetch nixos.org and print all hrefs.
main = do
  resp <- openURI "https://nixos.org/"
  let tags = filter (isTagOpenName "a") $ parseTags $ unpack $ fromRight undefined resp
  let tags' = map (fromAttrib "href") tags
  mapM_ putStrLn $ filter (/= "") tags'
```

اگر می‌خواهید دقیق‌تر عمل کنید، می‌توانید نسخه (revision) مشخصی از Nixpkgs را تعیین کنید:

    #! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/0672315759b3e15e2121365f067c1c8c56bb4722.tar.gz

تمامی مثال‌های بالا برای دریافت وابستگی‌ها از Nixpkgs از `-p` استفاده کردند. همچنین می‌توانید برای ساخت وابستگی‌های خودتان از یک عبارت Nix استفاده کنید. برای مثال، نمونه‌ی پایتون را می‌توان به این شکل نوشت:

```python
#! /usr/bin/env nix-shell
#! nix-shell deps.nix -i python
```

جایی که فایل `deps.nix` در همان پوشه اسکریپت دارای `#!` شامل موارد زیر است:

```nix
with import <nixpkgs> {};

runCommand "dummy" { buildInputs = [ python3 python3Packages.prettytable ]; } ""
```

نام فایل اسکریپت به عنوان نخستین آرگومان به مفسری منتقل می‌شود که توسط پرچم `-i` مشخص شده است.

به‌جز نخستین خط که دستوری برای سیستم‌عامل است، خطوط اضافی `#! nix-shell` نیازی نیست در ابتدای فایل قرار گیرند.
این امر اجازه می‌دهد تا آن‌ها را در کامنت‌های بلوکی برای زبان‌هایی که در آن‌ها `#` کامنت را آغاز نمی‌کند، مانند ECMAScript، Erlang، PHP یا Ruby، قرار دهید.
