# Fish {#sec-fish}

‏Fish یک «شل خط فرمان هوشمند و کاربرپسند» با پشتیبانی از پلاگین‌ها است.

## اسکریپت‌های Vendor در Fish {#sec-fish-vendor}

هر بسته‌ای ممکن است تکمیل‌کننده‌ها (completions)، قطعه‌کدهای پیکربندی و توابع مخصوص به خود در Fish را همراه داشته باشد. این موارد باید به ترتیب در `$out/share/fish/vendor_{completions,conf,functions}.d` نصب شوند.

وقتی گزینه‌های `programs.fish.enable` و `programs.fish.vendor.{completions,config,functions}.enable` از ماژول NixOS برای Fish روی true تنظیم شوند، این مسیرها در محیط سیستم جاری به‌صورت پیوند نمادین (symlink) قرار می‌گیرند و به طور خودکار

```nix
wrapFish {
  pluginPkgs = with fishPlugins; [
    pure
    foreign-env
  ];
  completionDirs = [ ];
  functionDirs = [ ];
  confDirs = [ "/path/to/some/fish/init/dir/" ];
}
```
