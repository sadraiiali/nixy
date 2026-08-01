(custom-binary-cache)=
# پیکربندی Nix برای استفاده از یک کش باینری سفارشی

Nix را می‌توان به گونه‌ای پیکربندی کرد که با استفاده از تنظیمات [`substituters`](/pages/nix-manual/command-ref/conf-file-prefix#conf-substituters) و [`trusted-public-keys`](/pages/nix-manual/command-ref/conf-file-prefix#conf-trusted-public-keys)، از یک کش باینری - به صورت انحصاری یا علاوه بر cache.nixos.org - استفاده کند.

:::{tip}
آموزش مربوط به [راه‌اندازی کش باینری HTTP](setup-http-binary-cache) را دنبال کرده و یک جفت کلید برای امضای اشیاء انبار ایجاد کنید.
:::

:::{warning}
Nix هر شیء انبار درخواست‌شده‌ای را که با کلیدهای خصوصی متناظر با کلیدهای عمومی پیکربندی‌شده امضا شده باشد، می‌پذیرد.
بنابراین، دسترسی به آن کلیدهای خصوصی به شما امکان می‌دهد تا فایل‌های دلخواهی را جایگزین انبار Nix خود کنید.
این شامل فایل‌های اجرایی می‌شود که ممکن است با دسترسی‌های سطح بالا یا به‌طور خودکار اجرا شوند!

فقط کلیدهای عمومی را که بدون قید و شرط به آن‌ها اعتماد دارید، اضافه کنید.
:::

برای مثال، با فرض وجود یک کش باینری در آدرس `https://example.org` با کلید عمومی `My56...Q==%` و تعدادی درایویشن در `default.nix`، می‌توانید با ارسال [تنظیمات به عنوان پرچم‌های خط فرمان](/pages/nix-manual/command-ref/conf-file-prefix#command-line-flags)، کاری کنید که Nix یک بار به صورت انحصاری از آن کش استفاده کند:

```shell-session
$ nix-build --substituters https://example.org --trusted-public-keys example.org:My56...Q==%
```

برای پیکربندی دائمی جهت تلاش برای استفاده از کش باینری سفارشی پیش از کش عمومی، آن را به عنوان `extra-substiters` با مقدار `priority` پایین‌تر به [فایل پیکربندی Nix](/pages/nix-manual/command-ref/conf-file-prefix#configuration-file) اضافه کنید:

```shell-session
$ echo "extra-substituters = https://example.org?priority=30" >> /etc/nix/nix.conf
$ echo "extra-trusted-public-keys = example.org:My56...Q==%" >> /etc/nix/nix.conf
```

برای استفاده همیشگی و صرفاً از کش باینری سفارشی:

```shell-session
$ echo "substituters = https://example.org" >> /etc/nix/nix.conf
$ echo "trusted-public-keys = example.org:My56...Q==%" >> /etc/nix/nix.conf
```

::::{admonition} NixOS
در NixOS، نیکس از طریق گزینه [`nix.settings`](https://search.nixos.org/options?show=nix.settings) پیکربندی می‌شود:

```nix
{ ... }: {
  nix.settings = {
    substituters = [ "https://example.org?priority=30" ];
    trusted-public-keys = [ "example.org:My56...Q==%" ];
  };
}
```
::::

:::{tip}
برای کاهش ترافیک خارجی خود، از [ماشین‌های بیلد راه دور](distributed-build-setup-tutorial) به عنوان کش‌های باینری ترجیحی استفاده کنید.
:::
