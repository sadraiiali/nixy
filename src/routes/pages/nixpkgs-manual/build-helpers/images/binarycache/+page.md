# <a id="sec-pkgs-binary-cache"></a> pkgs.mkBinaryCache

`pkgs.mkBinaryCache` تابعی برای ایجاد کش‌های باینری فایل مسطح Nix است.
چنین کشی به عنوان یک پوشه روی دیسک وجود دارد و می‌توان با دادن `--substituter file:///path/to/cache` به دستورات Nix، از آن به عنوان یک جایگزین‌کننده (substituter) Nix استفاده کرد.

بسته‌های Nix معمولاً از طریق [HTTP, SSH, or S3](https://nixos.org/manual/nix/stable/package-management/sharing-packages.html) بین ماشین‌ها به اشتراک گذاشته می‌شوند، اما کش باینری فایل مسطح هنوز هم در برخی موقعیت‌ها می‌تواند مفید باشد.
به عنوان مثال، می‌توانید آن را مستقیماً به ماشین دیگری کپی کنید، یا آن را روی یک سیستم‌فایل شبکه‌ای در دسترس قرار دهید.
همچنین می‌تواند روشی راحت برای در دسترس قرار دادن برخی بسته‌های Nix در داخل یک کنتینر از طریق bind-mounting باشد.

`mkBinaryCache` منتظر یک آرگومان با صفت `rootPaths` است.
`rootPaths` باید لیستی از درایویشن‌ها باشد.
بستار متعدی (transitive closure) خروجی‌های این درایویشن‌ها درون کش کپی خواهد شد.

## <a id="sec-pkgs-binary-cache-arguments"></a> آرگومان‌های اختیاری

`compression` (`"none"` یا `"xz"` یا `"zstd"`؛ _اختیاری_)

: الگوریتم فشرده‌سازی مورد استفاده.

  _مقدار پیش‌فرض:_ `zstd`.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> این تابع برای موارد استفاده پیشرفته در نظر گرفته شده است.
> روش رایج‌تر برای کار با کش‌های باینری فایل مسطح، استفاده از دستور [nix-copy-closure](https://nixos.org/manual/nix/stable/command-ref/nix-copy-closure.html) است.
> همچنین ممکن است بخواهید [dockerTools](#sec-pkgs-dockerTools) را برای نیازهای کانتینرسازی خود در نظر بگیرید.

<a id="sec-pkgs-binary-cache-example"></a>
<a id="ex-mkbinarycache-copying-package-closure"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # کپی کردن یک بسته و بستار آن به ماشینی دیگر با `mkBinaryCache`
>
> درایویشن زیر یک کش باینری فایل مسطح شامل بستار `hello` خواهد ساخت.
>

> ```nix
> { mkBinaryCache, hello }: mkBinaryCache { rootPaths = [ hello ]; }
> ```
>
> کش (Cache) را روی یک ماشین بسازید.
> توجه داشته باشید که این دستور همچنان همان بسته Nix دقیق بالا را می‌سازد، اما برای ساخت آن مستقیماً از یک عبارت، کمی کد boilerplate اضافه می‌کند.
>

> ```shellSession
> $ nix-build -E 'let pkgs = import <nixpkgs> {}; in pkgs.callPackage ({ mkBinaryCache, hello }: mkBinaryCache { rootPaths = [hello]; }) {}'
> /nix/store/azf7xay5xxdnia4h9fyjiv59wsjdxl0g-binary-cache
> ```
>
> پوشه حاصل را به ماشین دیگری که آن را `host2` می‌نامیم، کپی کنید:
>

> ```shellSession
> $ scp result host2:/tmp/hello-cache
> ```
>
> در این مرحله، هنگام ساخت درایویشن‌ها روی `host2` می‌توان از کش به عنوان یک substituter استفاده کرد:
>

> ```shellSession
> $ nix-build -A hello '<nixpkgs>' \
>   --option require-sigs false \
>   --option trusted-substituters file:///tmp/hello-cache \
>   --option substituters file:///tmp/hello-cache
> /nix/store/zhl06z4lrfrkw5rp0hnjjfrgsclzvxpm-hello-2.12.1
> ```
