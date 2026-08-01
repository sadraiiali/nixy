# Ruby {#sec-language-ruby}

## استفاده از Ruby {#using-ruby}

چندین نسخه از مفسرهای Ruby در Nix موجود است، همچنین بیش از ۲۵۰ جم (gem) و برنامه‌های متعدد نوشته‌شده به زبان Ruby. صفت (attribute) `ruby` به مفسر پیش‌فرض Ruby اشاره دارد که در حال حاضر MRI 3.3 است. همچنین امکان ارجاع به نسخه‌های خاص، مانند `ruby_3_y`، `jruby` یا `mruby` وجود دارد.

در درخت Nixpkgs، بسته‌های Ruby بسته به کاربردشان در سراسر آن یافت می‌شوند و از مجموعه بسته‌های اصلی فراخوانی می‌گردند. با این حال، جم‌های Ruby مجموعه‌های مجزایی هستند و برای هر

```ShellSession
$ nix-shell -p "ruby.withPackages (ps: with ps; [ nokogiri pry ])"
```

روش دیگر، که توصیه نمی‌شود، ایجاد یک محیط و فهرست کردن مستقیم تمام بسته‌ها است.

```ShellSession
$ nix-shell -p ruby.gems.nokogiri ruby.gems.pry
```

باز هم امکان اجرای مفسر از طریق شل وجود دارد. مفسر Ruby دارای صفت `gems` است که شامل تمام جم‌های Ruby برای آن مفسر خاص می‌شود.

```nix
with import <nixpkgs> { };
ruby.withPackages (
  ps: with ps; [
    nokogiri
    pry
  ]
)
```

در اینجا چه اتفاقی می‌افتد؟

1. کار را با درون‌ریزی مجموعهٔ بسته‌های نیکس (Nixpkgs) آغاز می‌کنیم. `import <nixpkgs>` تابع `<

```ShellSession
$ nix-shell -p "ruby.withPackages (ps: with ps; [ nokogiri pry ])" --run "pry"
```

یا بلافاصله `nokogiri` را در pry فراخوانی کنید:

```ShellSession
$ nix-shell -p "ruby.withPackages (ps: with ps; [ nokogiri pry ])" --run "pry -rnokogiri"
```

یا یک اسکریپت را با استفاده از این محیط اجرا کنید:

```ShellSession
$ nix-shell -p "ruby.withPackages (ps: with ps; [ nokogiri pry ])" --run "ruby example.rb"
```

#### استفاده از `nix-shell` به عنوان شیبنگ {#using-nix-shell-as-shebang}

در واقع، برای مورد آخر، روش

```ruby
#! /usr/bin/env nix-shell
#! nix-shell -i ruby -p "ruby.withPackages (ps: with ps; [ nokogiri rest-client ])"

require 'nokogiri'
require 'rest-client'

body = RestClient.get('http://example.com').body
puts Nokogiri::HTML(body).at('h1').text
```

## توسعه با Ruby {#developing-with-ruby}

### استفاده از یک Gemfile موجود {#using-an-existing-gemfile}

در بیشتر موارد، شما از قبل یک `Gemfile.lock` دارید که تمام وابستگی‌های شما را فهرست می‌کند. از این فایل می‌توان برای تولید یک `gemset.nix` استفاده کرد که جهت دریافت جم‌ها و ترکیب آن‌ها در یک محیط واحد به کار می‌رود. دلیل نیاز به یک فایل جداگانه این است که Nix مستلزم داشتن چک‌سام (checksum) برای هر ورودی به ساخت شماست. از آنجا که `Gemfile.lock` تولیدشده توسط `bundler` چک‌سام‌ها را ارائه نمی‌دهد، ابتدا باید هر جم را بارگیری کنیم، SHA256 آن را محاسبه کرده و در این فایل جداگانه ذخیره کنیم.

بنابراین گام‌های رسیدن از تنها یک `Gemfile` به یک `gemset.nix` عبارتند از:

```ShellSession
$ bundle lock
$ bundix
```

اگر از قبل یک `Gemfile.lock` دارید، می‌توانید `bundix` را اجرا کنید و به همان شکل کار خواهد کرد.

برای به‌روزرسانی جم‌های موجود در `Gemfile.lock` خود، می‌توانید از پرچم `bundix -l` استفاده کنید که در صورت جدیدتر بودن زمان تغییرات `Gemfile`، یک `Gemfile.lock` جدید می‌سازد.

هنگامی که `gemset.nix` تولید شد، می‌توان آن را در یک derivation / اشتقاق ساخت `bundlerEnv` به کار

```nix
# ...
let
  gems = bundlerEnv {
    name = "gems-for-some-project";
    gemdir = ./.;
  };
in
mkShell {
  packages = [
    gems
    gems.wrappedRuby
  ];
}
```

با داشتن این فایل در پوشه خود، می‌توانید `nix-shell` را برای ساخت و استفاده از جم‌ها اجرا کنید. بخش‌های مهم در اینجا `bundlerEnv` و `wrappedRuby` هستند.

‏`bundlerEnv` یک پوشش (wrapper) روی تمام جم‌های موجود در gemset شما است. این بدان معناست که تمامی پوشه‌های `/lib` و `/bin` در دسترس خواهند بود و فایل‌های اجرایی تمام جم‌ها (حتی وابستگی‌های غیرمستقیم) در `$PATH` شما قرار خواهند گرفت. `wrappedRuby` تمامی فایل‌های اجرایی همراه خود Ruby را در اختیارتان قرار می‌دهد، اما به صورت پوشش‌دار تا بتوانند به راحتی جم‌های موجود در gemset شما را پیدا کنند.

یکی از مشکلات رایجی که ممکن است با آن مواجه شوید این است که هم Ruby و هم `bundler` را در gemset خود داشته باشید. این موضوع منجر به تداخل برای `/bin/bundle` و `/bin/bundler` می‌شود. می‌توانید این مشکل را با قرار دادن Ruby یا جم‌های خود درون یک فراخوانی `lowPrio` حل کنید. بنابراین برای دادن اولویت به `bundler` موجود در gemset، به این صورت استفاده می‌شود:

```nix
# ...
mkShell {
  buildInputs = [
    gems
    (lowPrio gems.wrappedRuby)
  ];
}
```

گاهی اوقات یک Gemfile به فایل‌های دیگری ارجاع می‌دهد؛ مانند `.ruby-version` یا gemهای vendored. هنگام کپی کردن Gemfile به انبار نیکس (Nix store) باید آن فایل‌ها را نیز در کنار آن کپی کنیم. این کار با استفاده از `extraConfigPaths` امکان‌پذیر است. برای مثال:

```nix
{
  gems = bundlerEnv {
    name = "gems-for-some-project";
    gemdir = ./.;
    extraConfigPaths = [ "${./.}/.ruby-version" ];
  };
}
```

### پیکربندی‌ها و راهکارهای مختص Gem {#gem-specific-configurations-and-workarounds}

در برخی موارد، به‌ویژه اگر gem دارای افزونه‌های بومی (native extensions) باشد، ممکن است نیاز باشد نحوه ساخت gem را تغییر دهید.

این کار از طریق یک فایل پیکربندی مشترک انجام می‌شود که شامل تمامی راهکارها برای هر gem است.

این فایل در مسیر `/pkgs/development/ruby-modules/gem-config/default.nix` قرار دارد؛ از آنجا که این فایل از قبل شامل ورودی‌های

```nix
{
  pg_version ? "10",
  pkgs ? import <nixpkgs> { },
}:
let
  myRuby = pkgs.ruby.override {
    defaultGemConfig = pkgs.defaultGemConfig // {
      pg = attrs: {
        buildFlags = [
          "--with-pg-config=${pkgs."postgresql_${pg_version}".pg_config}/bin/pg_config"
        ];
      };
    };
  };
in
myRuby.withPackages (ps: with ps; [ pg ])
```

و یک مثال با `bundlerEnv`:

```nix
{
  pg_version ? "10",
  pkgs ? import <nixpkgs> { },
}:
let
  gems = pkgs.bundlerEnv {
    name = "gems-for-some-project";
    gemdir = ./.;
    gemConfig = pkgs.defaultGemConfig // {
      pg = attrs: {
        buildFlags = [
          "--with-pg-config=${pkgs."postgresql_${pg_version}".pg_config}/bin/pg_config"
        ];
      };
    };
  };
in
mkShell {
  buildInputs = [
    gems
    gems.wrappedRuby
  ];
}
```

و در نهایت از طریق اورلی‌ها:

```nix
{
  pg_version ? "10",
}:
let
  pkgs = import <nixpkgs> {
    overlays = [
      (self: super: {
        defaultGemConfig = super.defaultGemConfig // {
          pg = attrs: {
            buildFlags = [
              "--with-pg-config=${pkgs."postgresql_${pg_version}".pg_config}/bin/pg_config"
            ];
          };
        };
      })
    ];
  };
in
pkgs.ruby.withPackages (ps: with ps; [ pg ])
```

سپس می‌توانیم هر نسخه‌ای از postgresql را که می‌خواهیم به دست آوریم و جم `pg` همواره به درستی به آن ارجاع خواهد داد:

```ShellSession
$ nix-shell --argstr pg_version 9_4 --run 'ruby -rpg -e "puts PG.library_version"'
90421

$ nix-shell --run 'ruby -rpg -e "puts PG.library_version"'
100007
```

البته برای این مورد استفاده، می‌توان از اورلی‌ها نیز استفاده کرد چرا که پیکربندی `pg` به نام مستعار `postgresql` وابسته است، اما برای اهداف نمایشی همین کافی خواهد بود.

### Gemهای مخصوص پلتفرم {#ruby-platform-specif-gems}

در حال حاضر، bundix با gemهای پیش‌ساخته و مخصوص پلتفرم مشکلاتی دارد: [
```shell
$ bundle config set force_ruby_platform true
```
- به صورت محلی (در `<project-root>/.bundle/config` تنظیم خواهد شد):
```shell
$ bundle config set --local force_ruby_platform true
```

### افزودن یک gem به gemset پیش‌فرض {#adding-a-gem-to-the-default-gemset}

اکنون که می‌دانید چگونه یک محیط کاری Ruby را با Nix راه‌اندازی کنید، زمان آن رسیده‌است که فراتر رفته و توسعه با Ruby را به‌طور عملی آغاز کنید. ابتدا نگاهی به نحوه بسته‌بندی gemهای Ruby در Nix خواهیم داشت. سپس بررسی می‌کنیم که چگونه می‌توانید از حالت توسعه (development mode) همراه با کد خود استفاده کنید.

تمام gemها در مجموعه استاندارد به‌طور خودکار از یک `Gemfile` واحد تولید می‌شوند. برطرف‌سازی وابستگی‌ها با `bundler` انجام می‌شود که احتمال سازگار بودن همه gemها با یکدیگر را افزایش می‌دهد.

برای افزودن یک gem جدید به Nixpkgs، می‌توانید آن را در `/pkgs/development/ruby-modules/with

```shell
NIX_PATH=nixpkgs=$PWD nix-shell -p "ruby.withPackages (ps: with ps; [ name-of-your-gem ])"
```

برای بررسی gemها از نظر وجود هرگونه آسیب‌پذیری امنیتی، اسکریپت `./maintainers/scripts/audit-ruby-packages/audit-ruby-packages.bash` را اجرا

```ruby
source 'https://rubygems.org' do
  gem 'mdl'
end
```

اگر می‌خواهید نسخه خاصی را بسته‌بندی کنید، می‌توانید از نحو استاندارد Gemfile برای آن استفاده کنید، مثلاً `gem 'mdl', '0.5.0'`، اما اگر به هر حال آخرین نسخه پایدار را می‌خواهید، به‌روزرسانی با اجرای مجدد گام‌های `bundle lock` و `bundix` آسان‌تر است.

اکنون می‌توانید یک `default.nix` هم بسازید که به این شکل است:

```nix
{ bundlerApp }:

bundlerApp {
  pname = "mdl";
  gemdir = ./.;
  exes = [ "mdl" ];
}
```

تنها کاری که باقی می‌ماند، تولید فایل‌های `Gemfile.lock` و `gemset.nix` مربوطه طبق توضیحات بخش `Using an existing Gemfile` در بالا است.

#### بسته

```nix
{
  lib,
  bundlerApp,
  makeWrapper,
  git,
  gnutar,
  gzip,
}:

bundlerApp {
  pname = "r10k";
  gemdir = ./.;
  exes = [ "r10k" ];

  nativeBuildInputs = [ makeWrapper ];

  postBuild = ''
    wrapProgram $out/bin/r10k --prefix PATH : ${
      lib.makeBinPath [
        git
        gnutar
        gzip
      ]
    }
  '';
}
```
