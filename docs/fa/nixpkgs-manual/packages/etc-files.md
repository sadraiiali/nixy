/بسته‌ها
  - Glibc -> Glibc

Check Persian fluency:
# فایل‌های /etc {#etc}

برخی فراخوانی‌ها در Glibc به دسترسی به فایل‌های زمان اجرا در `/

```bash
> nix-shell -p iana-etc

[nix-shell:~]$ env | grep NIX_ETC
NIX_ETC_SERVICES=/nix/store/aj866hr8fad8flnggwdhrldm0g799ccz-iana-etc-20210225/etc/services
NIX_ETC_PROTOCOLS=/nix/store/aj866hr8fad8flnggwdhrldm0g799ccz-iana-etc-20210225/etc/protocols
```

نسخه Nixpkgs از [glibc](https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/libraries
