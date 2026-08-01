# سرو کردن انبار Nix از طریق HTTP

شما می‌توانید به راحتی انبار Nix یک ماشین را از طریق HTTP به اشتراک بگذارید. این امکان را به ماشین‌های دیگر می‌دهد تا مسیرهای انبار را از آن ماشین دریافت کنند تا نصب‌ها سرعت پیدا کنند. این کار از همان مکانیسم *کش باینری* استفاده می‌کند که Nix معمولاً برای دریافت باینری‌های پیش‌ساخته از <https://cache.nixos.org> بهره می‌برد.

دیمنی (daemon) که درخواست‌های کش باینری را از طریق HTTP مدیریت می‌کند، یعنی `nix-serve`، بخشی از توزیع Nix نیست، اما می‌توانید آن را از Nixpkgs نصب کنید:

```console
$ nix-env --install --attr nixpkgs.nix-serve
```

سپس می‌توانید سرور را راه‌اندازی کنید که به اتصال‌های HTTP روی هر پورتی که دوست دارید گوش دهد:

```console
$ nix-serve -p 8080
```

برای بررسی اینکه آیا به درستی کار می‌کند، تلاش کنید فایل [`nix-cache-info`](@docroot@/protocols/binary-cache/nix-cache-info.md) را روی کلاینت دریافت کنید:

```console
$ curl http://avalon:8080/nix-cache-info
StoreDir: /nix/store
WantMassQuery: 1
Priority: 30
```

هنگام نوشتن در یک کش باینری (مثلاً با [`nix copy`](@docroot@/command-ref/new-cli/nix3-copy.md))، اگر فایل [`nix-cache-info`](@docroot@/protocols/binary-cache/nix-cache-info.md) وجود نداشته باشد، Nix آن را به‌طور خودکار ایجاد می‌کند.

در سمت کاربر (client)، می‌توانید با استفاده از `--substituters` به Nix بگویید که از کش باینری شما استفاده کند، برای مثال:

```console
$ nix-env --install --attr nixpkgs.firefox --substituters http://avalon:8080/
```

گزینهٔ `substituters` به نیکس می‌گوید که علاوه بر کش‌های پیش‌فرض شما، مانند <https://cache.nixos.org>، از این کش باینری نیز استفاده کند. بنابراین، برای هر مسیر در کلوژر (closure) متعلق به Firefox، نیکس ابتدا بررسی می‌کند که آیا آن مسیر روی سرور `avalon` یا سایر کش‌های باینری موجود است یا خیر. اگر موجود نباشد، به ساخت از روی کد منبع بازخواهد گشت.

همچنین می‌توانید با اضافه کردن خطی به فایل پیکربندی `nix.conf` به این شکل، به نیکس بگویید که همیشه از کش باینری شما استفاده کند:

    substituters = http://avalon:8080/ https://cache.nixos.org/
