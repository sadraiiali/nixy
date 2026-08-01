# <a id="sec-weechat"></a> WeeChat

می‌توان WeeChat را به‌گونه‌ای پیکربندی کرد که تنها شامل افزونه‌های انتخابی شما باشد؛ این کار اندازه closure آن را در مقایسه با پیکربندی پیش‌فرض که شامل تمام افزونه‌های موجود است، کاهش می‌دهد. برای استفاده از این قابلیت، عبارتی را نصب کنید که پیکربندی آن را بازنشانی کند، مانند:

```nix
weechat.override {
  configure = (
    { availablePlugins, ... }:
    {
      plugins = with availablePlugins; [
        python
        perl
      ];
    }
  );
}
```

خودکار از `availablePlugins` استفاده خواهد شد.

پلاگین‌های در حال حاضر در دسترس عبارتند از `python`، `perl`، `ruby`، `guile`

```nix
weechat.override {
  configure =
    { availablePlugins, ... }:
    {
      plugins = with availablePlugins; [
        (python.withPackages (
          ps: with ps; [
            pycrypto
            python-dbus
          ]
        ))
      ];
    };
}
```

برای اینکه تمامی افزونه‌های پیش‌فرض نیز به‌صورت نصب‌شده باقی بمانند، می‌توان از روش زیر استفاده کرد:

```nix
weechat.override {
  configure =
    { availablePlugins, ... }:
    {
      plugins = builtins.attrValues (
        availablePlugins
        // {
          python = availablePlugins.python.withPackages (
            ps: with ps; [
              pycrypto
              python-dbus
            ]
          );
        }
      );
    };
}
```

WeeChat امکان تنظیم مقادیر پیش‌فرض را هنگام راه‌اندازی با استفاده از `--run-command` فراهم می‌کند. از متد `configure` می‌توان برای ارسال دستورات به برنامه استفاده کرد:

```nix
weechat.override {
  configure =
    { availablePlugins, ... }:
    {
      init = ''
        /set foo bar
        /server add libera irc.libera.chat
      '';
    };
}
```

هنگام اجرای `weechat --run-command "your-commands"`، می‌توان مقادیر بیشتری را به فهرست دستورها اضافه کرد.

علاوه بر این، امکان مشخص کردن اسکریپت‌هایی وجود دارد که هنگام راه‌اندازی `weechat` بارگیری شوند. این اسکریپت‌ها پیش از دستورهای `init` بارگیری خواهند شد:

```nix
weechat.override {
  configure =
    { availablePlugins, ... }:
    {
      scripts = with pkgs.weechatScripts; [
        weechat-xmpp
        weechat-matrix-bridge
        wee-slack
      ];
      init = ''
        /set plugins.var.python.jabber.key "val"
      '';
    };
}
```

در `nixpkgs` یک زیربسته وجود دارد که شامل درایویشن‌ها برای اسکریپت‌های WeeChat است. چنین درایویشن‌هایی انتظار صفت `passthru.scripts` را دارند که شامل فهرستی از تمامی اسکریپت‌های داخل مسیر انبار است. علاوه بر این، همه اسکریپت‌ها باید در `$out/share` قرار داشته باشند. یک درایویشن نمونه به این صورت است:

```nix
{ stdenv, fetchurl }:

stdenv.mkDerivation {
  name = "exemplary-weechat-script";
  src = fetchurl {
    url = "https://scripts.tld/your-scripts.tar.gz";
    hash = "...";
  };
  passthru.scripts = [
    "foo.py"
    "bar.lua"
  ];
  installPhase = ''
    runHook preInstall

    mkdir $out/share
    cp foo.py $out/share
    cp bar.lua $out/share

    runHook postInstall
  '';
}
```
