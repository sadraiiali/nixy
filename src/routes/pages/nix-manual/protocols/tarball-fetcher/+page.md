# 10.2. ارائه فلیک‌های تاربال (Tarball Flakes)

فلیک‌های تاربال را می‌توان به عنوان تاربال‌های معمولی از طریق HTTP یا سیستم‌فایل (برای URLهای `file://`) سرو کرد. مگر اینکه سرور پروتکل تاربال HTTP قابل قفل‌سازی را پیاده‌سازی کند، مسئولیت اطمینان از اینکه URL همیشه محتوای تاربال یکسانی را تولید می‌کند، بر عهده کاربر است.

یک سرور HTTP می‌تواند یک URL HTTP «تغییرناپذیر» مناسب برای فایل‌های قفل (`lock files`) بازگرداند. این امر به کاربران اجازه می‌دهد ورودی فلیک تاربالی را در `flake.nix` مشخص کنند که آخرین نسخه یک فلیک را درخواست می‌کند (به عنوان مثال `https://example.org/hello/latest.tar.gz`)، در حالی که `flake.lock` یک URL را ثبت می‌کند که محتوای آن تغییر نخواهد کرد (به عنوان مثال `https://example.org/hello/&lt;revision&gt;.tar.gz`). برای انجام این کار، سرور باید یک [هدر `Link` در HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link) با صفت `rel` تنظیم‌شده روی `immutable`، به شکل زیر بازگرداند:

```
Link: <flakeref>; rel="immutable"
```

(نکات لازم: نویسه‌های `&lt;` و `>` در اطراف *flakeref* الزامی هستند.)

مقدار *flakeref* باید یک flakeref تاربال (tarball) باشد. این مقدار می‌تواند شامل صفات فلیک تاربال یعنی `narHash`، `rev`، `revCount` و `lastModified` باشد. اگر `narHash` درج شود، مقدار آن باید [هش NAR][Nix Archive] تاربال استخراج‌شده باشد (که از طریق دستور `nix hash path` محاسبه می‌شود). Nix محتوای تاربال ارائه‌شده را با صفت `narHash` بررسی و تطبیق می‌دهد. صفات `rev` و `revCount` زمانی مفید هستند که فلیک تاربال، آینه‌ای از یک نوع دریافت‌کننده (fetcher) باشد که دارای آن صفات است؛ مانند Git یا GitHub. این صفات توسط Nix بررسی نمی‌شوند.

```
Link: <https://example.org/hello/442793d9ec0584f6a6e82fa253850c8085bb150a.tar.gz
  ?rev=442793d9ec0584f6a6e82fa253850c8085bb150a
  &revCount=835
  &narHash=sha256-GUm8Uh/U74zFCwkvt9Mri4DSM%2BmHj3tYhXUkYpiv31M%3D>; rel="immutable"
```

برای فلیک‌های تاربال، مقدار صفت فلیک `lastModified` به عنوان برچسب زمانی (timestamp) جدیدترین فایل درون تاربال تعریف می‌شود.

## پشتیبانی از Gitea و Forgejo

این پروتکل از نسخه v1.22.1 به بعد در Gitea و از نسخه‌های v7.0.4/v8.0.0 به بعد در Forgejo پشتیبانی می‌شود و می‌توان آن را با الگوی URL فلیک زیر مورد استفاده قرار داد:

```
https://<domain name>/<owner>/<repo>/archive/<reference or revision>.tar.gz
```

> **مثال**
> 
>

```nix
> # flake.nix
> {
>    inputs = {
>      foo.url = "https://gitea.example.org/some-person/some-flake/archive/main.tar.gz";
>      bar.url = "https://gitea.example.org/some-other-person/other-flake/archive/442793d9ec0584f6a6e82fa253850c8085bb150a.tar.gz";
>      qux = {
>        url = "https://forgejo.example.org/another-person/some-non-flake-repo/archive/development.tar.gz";
>        flake = false;
>      };
>    };
>    outputs = { foo, bar, qux }: { /* ... */ };
> }
```

[بایگانی نیکس]: /pages/nix-manual/store/file-system-object/content-address#serial-nix-archive
