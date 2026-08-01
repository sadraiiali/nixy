# <a id="sec-urxvt"></a> Urxvt

Urxvt که با نام rxvt-unicode نیز شناخته می‌شود، یک شبیه‌ساز ترمینال با قابلیت سفارشی‌سازی بالا

```nix
rxvt-unicode.override {
  configure =
    { availablePlugins, ... }:
    {
      plugins = with availablePlugins; [
        perls
        resize-font
        vtwheel
      ];
    };
}
```

اگر تابع `configure` یک مجموعه ویژگی را بدون صفت `plugins` برگرداند، `availablePlugins` به‌طور خودکار استفاده خواهد شد.

برای افزودن پلاگین‌ها و در عین حال حفظ تمامی پلاگین‌های پیش‌فرض نصب‌شده، می‌توان از روش زیر استفاده کرد:

```nix
rxvt-unicode.override {
  configure =
    { availablePlugins, ... }:
    {
      plugins = (builtins.attrValues availablePlugins) ++ [ custom-plugin ];
    };
}
```

برای دریافت فهرستی از تمام افزونه‌های موجود، Nix REPL را باز کرده و اجرا کنید

```ShellSession
$ nix repl
:l <nixpkgs>
map (p: p.name) pkgs.rxvt-unicode.plugins
```

یا اینکه، اگر شل (Shell) شما Bash یا zsh است و قابلیت تکمیل فعال است، عبارت `nixpkgs.rxvt-unicode.plugins.&lt;tab&gt;` را تای

```nix
rxvt-unicode.override {
  configure =
    { availablePlugins, ... }:
    {
      pluginsDeps = [ xsel ];
    };
}
```

`perlDeps` روشی کاربردی برای ارائه بسته‌های Perl به افزونه‌های سفارشی شما (در `$HOME/.urxvt/ext`) است. برای مثال، اگر به `AnyEvent` نیاز دارید می‌توانید این‌طور عمل کنید:

```nix
rxvt-unicode.override {
  configure =
    { availablePlugins, ... }:
    {
      perlDeps = with perlPackages; [ AnyEvent ];
    };
}
```

vt plugins <a id="sec-urxvt-pkg"></a>` -> `## بسته‌بندی افزونه‌های urxvt <a id="sec-urxvt-pkg"></a>``
- Backtick content preserved:

```nix
{ passthru.perlPackages = [ "self" ]; }
```

این کار باعث می‌شود wrapperِ urxvt وابستگی را شناسایی کرده و مسیر Perl را بر همین اساس تنظیم کند.
