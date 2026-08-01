# 3.7. ارتقای Nix

> **نکته**
>
> این دستورالعمل‌های ارتقا در مواردی اعمال می‌شود که Nix پیرو [دستورالعمل‌های نصب در این راهنما](/pages/nix-manual/installation) نصب شده باشد.

بررسی کنید که چه نسخه‌ای از Nix نصب خواهد شد؛ برای نمونه، از یکی از [کانال‌های انتشار](http://channels.nixos.org/) مانند `nixpkgs-unstable`:

```shell
$ nix-shell -p nix -I nixpkgs=channel:nixpkgs-unstable --run "nix --version"
nix (Nix) 2.18.1
```

> **هشدار**
>
> نوشتن در [انبار محلی](/pages/nix-manual/store/types/local-store) با نسخه جدیدتری از Nix، برای مثال با ساختن درایویشن‌ها به کمک [`nix-build`](/pages/nix-manual/command-ref/nix-build) یا [`nix-store --realise`](/pages/nix-manual/command-ref/nix-store/realise)، ممکن است طرحواره پایگاه‌داده را تغییر دهد!
> بنابراین، بازگشت به نسخه قدیمی‌تری از Nix ممکن است مستلزم پاکسازی پایگاه‌داده انبار پیش از قابل‌استفاده شدن آن باشد.

## چندکاربره لینوکس

```shell
$ sudo su
# nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
# systemctl daemon-reload
# systemctl restart nix-daemon
```

## چندکاربره در macOS

```shell
$ sudo nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
$ sudo launchctl remove org.nixos.nix-daemon
$ sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist
```

## تک‌کاربره برای تمام پلتفرم‌ها

```shell
$ nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
```
