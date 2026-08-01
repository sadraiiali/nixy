# ارتقای Nix

> **نکته**
>
> این دستورالعمل‌های ارتقا در مواردی اعمال می‌شود که Nix پیرو [دستورالعمل‌های نصب در این راهنما](./index.md) نصب شده باشد.

بررسی کنید که چه نسخه‌ای از Nix نصب خواهد شد؛ برای نمونه، از یکی از [کانال‌های انتشار](http://channels.nixos.org/) مانند `nixpkgs-unstable`:

```console
$ nix-shell -p nix -I nixpkgs=channel:nixpkgs-unstable --run "nix --version"
nix (Nix) 2.18.1
```

> **هشدار**
>
> نوشتن در [انبار محلی](@docroot@/store/types/local-store.md) با نسخه جدیدتری از Nix، برای مثال با ساختن درایویشن‌ها به کمک [`nix-build`](@docroot@/command-ref/nix-build.md) یا [`nix-store --realise`](@docroot@/command-ref/nix-store/realise.md)، ممکن است طرحواره پایگاه‌داده را تغییر دهد!
> بنابراین، بازگشت به نسخه قدیمی‌تری از Nix ممکن است مستلزم پاکسازی پایگاه‌داده انبار پیش از قابل‌استفاده شدن آن باشد.

## چندکاربره لینوکس

```console
$ sudo su
# nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
# systemctl daemon-reload
# systemctl restart nix-daemon
```

## چندکاربره در macOS

```console
$ sudo nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
$ sudo launchctl remove org.nixos.nix-daemon
$ sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist
```

## تک‌کاربره برای تمام پلتفرم‌ها

```console
$ nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
```
