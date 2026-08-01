# Hy {#sec-language-hy}

## نصب {#ssec-hy-installation}

### نصب بدون بسته‌ها {#installation-without-packages}

شما می‌توانید `hy` را از طریق nix-env یا با افزودن آن به `configuration.nix` با ارجاع به صفت `hy` نصب کنید. این نوع نصب، `hy` را به محیط شما اضافه می‌کند و به‌خوبی با `python3` کار می‌کند.

::: {.caution}
بسته‌هایی که همراه با derivation پایتون شما نصب شده‌اند، از این طریق برای `hy` قابل دسترسی نیستند.
:::

### نصب همراه با بسته‌ها {#installation-with-packages}

ایجاد یک derivation برای `hy` به همراه بسته‌های سفارشی `python` بسیار ساده و مشابه روشی است که پایتون انجام می‌دهد. صفت `hy` تابع `withPackages` را ارائه می‌دهد که یک derivation سفارشی برای `hy` با بسته‌های مشخص‌شده ایجاد می‌کند.

برای مثال، اگر می‌خواهید یک شل با `matplotlib` و `numpy` ایجاد کنید، می‌توانید این کار را به این صورت انجام دهید:

```ShellSession
$ nix-shell -p "hy.withPackages (ps: with ps; [ numpy matplotlib ])"
```

یا اگر می‌خواهید `configuration.nix` خود را گسترش دهید:
```nix
{
  # ...

  environment.systemPackages = with pkgs; [
    (hy.withPackages (
      py-packages: with py-packages; [
        numpy
        matplotlib
      ]
    ))
  ];
}
```
