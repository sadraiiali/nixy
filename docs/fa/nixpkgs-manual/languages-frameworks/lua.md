# Lua {#lua}

## استفاده از Lua {#lua-userguide}

### نگاهی کلی به Lua {#lua-overview}

چندین نسخه از مفسر Lua در دسترس است: luajit، lua 5.1، 5.2، 5.3.
صفت (attribute) `lua` به مفسر پیش‌فرض اشاره دارد، همچنین امکان اشاره به نسخه‌های خاص وجود دارد، برای مثال `lua5_2` به Lua 5.2 اشاره می‌کند.

کتابخانه‌های Lua در مجموعه‌های جداگانه‌ای قرار دارند، به طوری که برای هر نسخه از مفسر یک مجموعه وجود دارد.

مفسرها دارای چندین صفت (attribute) مشترک هستند. یکی از این صفات `pkgs` است که یک مجموعه بسته از کتابخانه‌های Lua برای این مفسر خاص می‌باشد. برای مثال، بسته `busted` مربوط به مفسر پیش‌فرض، `lua.pkgs.busted` است و نسخه lua 5

```nix
with import <nixpkgs> { };

lua5_2.withPackages (
  ps: with ps; [
    busted
    luafilesystem
  ]
)
```

و آن را در پروفایل خود نصب کنید با

```shell
nix-env -if build.nix
```
اکنون می‌توانید از مفسر Lua و همچنین بسته‌های اضافی (`busted` و `luafilesystem`) که به محیط افزوده‌اید استفاده کنید.

#### محیط Lua تعریف‌شده در `~/.config/nixpkgs/config.nix` {#lua-environment-defined-in-.confignixpkgsconfig.nix}

اگر ترجیح می‌دهید، می‌توانید این محیط را به‌عنوان یک بازنشانی بسته به مجموعهٔ Nixpkgs نیز اضافه کنید، برای مثال با استفاده از `config.nix`،

```nix
{
  # ...

  packageOverrides =
    pkgs: with pkgs; {
      myLuaEnv = lua5_2.withPackages (
        ps: with ps; [
          busted
          luafilesystem
        ]
      );
    };
}
```

و آن را در پروفایل خود نصب کنید با:

```shell
nix-env -iA nixpkgs.myLuaEnv
```
محیط با ارجاع به صفت (attribute) نصب می‌شود، با فرض اینکه از کانال `nixpkgs` استفاده شده باشد.

#### محیط Lua تعریف‌شده در `/etc/nixos/configuration.nix` {#lua-environment-defined-in-etcnixosconfiguration.nix}

برای کامل‌تر شدن بحث، در اینجا مثال دیگری از نحوه نصب محیط به‌صورت سرتاسر سیستم ارائه شده‌است.

```nix
{
  # ...

  environment.systemPackages = with pkgs; [
    (lua.withPackages (
      ps: with ps; [
        busted
        luafilesystem
      ]
    ))
  ];
}
```

### چگونه یک بسته Lua را با استفاده از اورلی‌ها بازنشانی کنیم؟ {#how-to-override-a-lua-package-using-overlays}

از قالب اورلی زیر استفاده کنید:

```nix
final: prev: {

  lua = prev.lua.override {
    packageOverrides = luaself: luaprev: {

      luarocks-nix = luaprev.luarocks-nix.overrideAttrs (old: {
        pname = "luarocks-nix";
        src = /home/my_luarocks/repository;
      });
    };
  };

  luaPackages = lua.pkgs;
}
```

### محیط موقت Lua با `nix-shell` {#temporary-lua-environment-with-nix-shell}

دو روش برای بارگیری یک شل با بسته‌های Lua وجود دارد. روش اول و پیشنهادی این است که محیطی با `lua.buildEnv` یا `lua.withPackages` ایجاد کرده و آن را بارگیری کنید. برای مثال:

```sh
$ nix-shell -p 'lua.withPackages(ps: with ps; [ busted luafilesystem ])'
```

یک شل (Shell) باز می‌کند که از طریق آن می‌توانید مفسر را اجرا کنید.

```sh
[nix-shell:~] lua
```

روش دیگر، که توصیه نمی‌شود، محیطی ایجاد نمی‌کند و مستلزم آن است که بسته‌ها را مستقیماً فهرست کنید،

```sh
$ nix-shell -p lua.pkgs.busted lua.pkgs.luafilesystem
```
مجدداً، امکان اجرای مفسر از طریق شل وجود دارد.
مفسر Lua دارای صفت `pkgs` است که تمام کتابخانه‌های Lua را برای آن مفسر خاص دربردارد.

## توسعه با Lua {#lua-developing}

اکنون که می‌دانید چگونه یک محیط کاری Lua با Nix داشته باشید، زمان آن رسیده‌است که فراتر رفته و توسعه با Lua را به صورت عملی آغاز کنید. برای بسته‌بندی نرم‌افزار Lua دو روش وجود دارد: یا روی luarocks قرار دارد و بیشتر آن می‌تواند توسط مبدل luarocks2nix مدیریت شود، یا بسته‌بندی باید به صورت دستی انجام گیرد. ابتدا روش luarocks و سپس روش دستی را ارائه می‌کنیم.

### بسته‌بندی یک کتابخانه در luarocks {#packaging-a-library-on-luarocks}

وب‌سایت [Luarocks.org](https://luarocks.org/) مخزن اصلی بسته‌های Lua است.
این سایت دو نوع بسته ارائه می‌دهد: `rockspec` و `src.rock` (معادل یک [rockspec](https://github.com/luarocks/luarocks/wiki/Rockspec-format) اما همراه با سورس).

بسته‌های مبتنی بر Luarocks در فایل [pkgs/development/lua-modules/generated-packages.nix](https://github.com/NixOS/n

```sh

nix-shell -p luarocks-packages-updater --run luarocks-packages-updater
```

برای افزودن یک بسته جدید بدون به‌روزرسانی همه بسته‌ها، دستور زیر را اجرا کنید:

```sh

nix-shell -p luarocks-packages-updater
luarocks-packages-updater add [--maintainers "<maintainer>"] <package-name>
```

توانید بسته خود را طبق روال معمول توسعه دهید، فقط فراموش نکنید که آن را درون یک فراخوانی `toLuaModule` قرار دهید؛ برای نمونه:

Let's double-check all rules:
1. Output ONLY

```nix
{
  mynewlib = toLuaModule (
    stdenv.mkDerivation {
      # ...
    }
  );
}
```

همچنین تابع `buildLuaPackage` وجود دارد که می‌تواند زمانی که ماژول‌های lua برای luarocks بسته‌بندی نشده‌اند، مورد استفاده قرار گیرد. می‌توانید چند نمونه را در `pkgs/top-level/lua-packages.nix` ببینید.
```nix
{
  luaposix = buildLuarocksPackage {
    pname = "luaposix";
    version = "34.0.4-1";

    src = fetchurl {
      url = "https://raw.githubusercontent.com/rocks-moonscript-org/moonrocks-mirror/master/luaposix-34.0.4-1.src.rock";
      hash = "sha256-4mLJG8n4m6y4Fqd0meUDfsOb9RHSR0qa/KD5KCwrNXs=";
    };
    disabled = (luaOlder "5.1") || (luaAtLeast "5.4");
    propagatedBuildInputs = [
      bit32
      lua
      std_normalize
    ];

    meta = {
      homepage = "https://github.com/luaposix/luaposix/";
      description = "Lua bindings for POSIX";
      maintainers = with lib.maintainers; [
        vyp
        lblasc
      ];
      license = lib.licenses.mit;
    };
  };
}
```

`buildLuarocksPackage` بیشتر وظایف را به luarocks واگذار می‌کند:

* این تابع `luarocks` را به‌عنوان استخراج‌کننده برای فایل‌های `src.rock` (که در واقع فایل‌های zip هستند) اضافه می‌کند.
* فاز `configurePhase` یک فایل پیکربندی موقت luarocks می‌نویسد که مسیر آن از طریق متغیر محیطی `LUAROCKS_CONFIG` صادر (export) می‌شود.
* فاز `buildPhase` هیچ کاری انجام نمی‌دهد.
* فاز `installPhase` دستور `luarocks make --deps-mode=none --tree $out` را برای ساخت و نصب بسته فراخوانی می‌کند.
* در فاز `postFixup`، تابع Bash با نام `wrapLuaPrograms` فراخوانی می‌شود تا تمام برنامه‌های موجود در پوشه `$out/bin/*` را لفاف‌پیچی (wrap) کند تا شامل متغیر محیطی `$PATH` شده و کتابخانه‌های وابسته را به `LUA_PATH` و `LUA_CPATH` اسکریپت اضافه کند.

این تابع آرگومان‌های زیر را می‌پذیرد:

* 'luarocksConfig': یک مقدار Nix که مستقیماً به پیکربندی luarocks مورد استفاده در طول نصب

```nix
lua.withPackages (ps: [ ps.luafilesystem ])
```

`withPackages` مجموعه بسته‌های صحیح مربوط به نسخهٔ مفسر خاص را به عنوان یک آرگومان به تابع پاس می‌دهد. در مثال بالا، `ps` برابر با `luaPackages` است.
اما همچنین می‌توانید به راحتی به

```nix
lua5_1.withPackages (ps: [ ps.lua ])
```

اکنون، `ps` روی `lua5_1.pkgs` تنظیم شده‌است که با نسخهٔ مفسر مطابقت دارد.

### راهنمای مشارکت در Lua {#lua-contributing}

قوانین
