# <a id="sec-firefox"></a> Firefox

## <a id="build-wrapped-firefox-with-extensions-and-policies"></a> ساخت Firefox پوشانده‌شده با افزونه‌ها و سیاست‌ها

تابع `wrapFirefox` امکان ارسال سیاست‌ها، تنظیمات و افزونه‌های در دسترس برای Firefox را فراهم می‌کند. با کمک `fetchFirefoxAddon` می‌توان نسخه‌ای از Firefox را ساخت که افزونه‌ها به صورت ازپیش‌نصب‌شده همراه آن هستند:

```nix
{
  # Nix firefox addons only work with the firefox-esr package.
  myFirefox = wrapFirefox firefox-esr-unwrapped {
    nixExtensions = [
      (fetchFirefoxAddon {
        name = "ublock"; # Has to be unique!
        url = "https://addons.mozilla.org/firefox/downloads/file/3679754/ublock_origin-1.31.0-an+fx.xpi";
        hash = "sha256-2e73AbmYZlZXCP5ptYVcFjQYdjDp4iPoEPEOSCVF5sA=";
      })
    ];

    extraPolicies = {
      CaptivePortal = false;
      DisableFirefoxStudies = true;
      DisablePocket = true;
      DisableTelemetry = true;
      DisableFirefoxAccounts = true;
      FirefoxHome = {
        Pocket = false;
        Snippets = false;
      };
      UserMessaging = {
        ExtensionRecommendations = false;
        SkipOnboarding = true;
      };
      SecurityDevices = {
        # Use a proxy module rather than `nixpkgs.config.firefox.smartcardSupport = true`
        "PKCS#11 Proxy Module" = "${pkgs.p11-kit}/lib/p11-kit-proxy.so";
      };
    };

    extraPrefs = ''
      // Show more ssl cert infos
      lockPref("security.identityblock.show_extended_validation", true);
    '';
  };
}
```

اگر `nixExtensions != null` باشد، تمامی افزونه‌های نصب‌شده به صورت دستی از پروفایل مرورگر شما حذف خواهند شد.
برای مشاهده سیاست‌های سازمانی موجود، از [سیاست‌های سازمانی](https://github.com/mozilla/policy-templates#
