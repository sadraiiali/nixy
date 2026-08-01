nixpkgs/blob/master/pkgs/applications/editors/eclipse) قرار دارند.

    Nixpkgs چندین بسته ارائه می‌دهد که Eclipse را به اشکال مختلف نصب می‌کنند. این

```ShellSession
$ nix-env -f '<nixpkgs>' -qaP -A eclipses --description
```

همان‌طور که انتظار می‌رود، پس از نصب یک گونه از Eclipse، می‌توان آن را با استفاده از دستور `eclipse` اجرا کرد. سپس از داخل خود Eclipse، امکان نصب پلاگین‌ها به روش معمول وجود دارد؛ یا با مشخص کردن دستی یک سایت به‌روزرسانی Eclipse، یا با نصب پلاگین Marketplace Client و استفاده از آن برای پیدا کردن و نصب سایر پلاگین‌ها. این روش نصب، یک نصب از Eclipse ارائه می‌دهد که شباهت زیادی به Eclipse نصب‌شده به صورت دستی دارد.

اگر ترجیح می‌دهید پلاگین‌ها را به شیوه‌ی اعلانی‌تری نصب کنید، Nixpkgs نیز چند پلاگین Eclipse ارائه می‌دهد که می‌توان آن‌ها را در یک _محیط Eclipse_ نصب کرد. این نوع محیط با استفاده از تابع `eclipseWithPlugins` ایجاد می‌شود که در مجموعه ویژگی `nixpkgs.eclipses` قرار دارد. این تابع آرگومان `{ eclipse, plugins ? [], jvmArgs ? [] }` را می‌پذیر

```nix
{
  packageOverrides = pkgs: {
    myEclipse =
      with pkgs.eclipses;
      eclipseWithPlugins {
        eclipse = eclipse-platform;
        jvmArgs = [ "-Xmx2048m" ];
        plugins = [ plugins.color-theme ];
      };
  };
}
```

به پیکربندی Nixpkgs خود (`~/.config/nixpkgs/config.nix`) و نصب آن با اجرای `nix-env -f '<nix

```ShellSession
$ nix-env -f '<nixpkgs>' -qaP -A eclipses.plugins --description
```

اگر نیاز به نصب پلاگین‌هایی باشد که در Nixpkgs موجود نیستند، ممکن است بتوان این پلاگین‌ها را خارج از Nixpkgs و با استفاده از توابع `buildEclipseUpdateSite` و `buildEclipsePlugin` موجود در

```nix
{
  packageOverrides = pkgs: {
    myEclipse =
      with pkgs.eclipses;
      eclipseWithPlugins {
        eclipse = eclipse-platform;
        jvmArgs = [ "-Xmx2048m" ];
        plugins = [
          plugins.color-theme
          (plugins.buildEclipsePlugin {
            pname = "myplugin1";
            version = "1.0";
            srcFeature = fetchurl {
              url = "http://…/features/myplugin1.jar";
              hash = "sha256-123…";
            };
            srcPlugin = fetchurl {
              url = "http://…/plugins/myplugin1.jar";
              hash = "sha256-123…";
            };
          })
          (plugins.buildEclipseUpdateSite {
            pname = "myplugin2";
            version = "1.0";
            src = fetchurl {
              stripRoot = false;
              url = "http://…/myplugin2.zip";
              hash = "sha256-123…";
            };
          })
        ];
      };
  };
}
```
