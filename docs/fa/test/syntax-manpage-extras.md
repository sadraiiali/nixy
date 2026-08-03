## الگوهای صفحه‌ی راهنما (از nix-shell)

<span id="manpage"></span>

الگوهای گرفته‌شده از `/pages/nix-manual/command-ref/nix-shell` (شامل `#env-NIX_BUILD_SHELL`). دقیقاً مانند نسخه‌ی منتشرشده در سایت نگه‌داشته شده‌اند تا نحوه‌ی رندر شدن و اشکالات قابل‌مشاهده باقی بمانند.

### خلاصه (Synopsis) چندخطی

<span id="synopsis"></span>

خلاصه‌ی دستور man page را **نباید** به‌صورت پاراگراف Markdown چندخطی نوشت (خطوط ادغام می‌شوند و بک‌تیک‌ها خراب جفت می‌شوند). شکل درست: بلوک `text` محصور (مثل صفحه‌ی `nix-shell`):

```text
nix-shell
  [--arg name value]
  [--argstr name value]
  [{--attr | -A} attrPath]
  [--command cmd]
  [--run cmd]
  [--exclude regexp]
  [--pure]
  [--keep name]
  {{--packages | -p} {packages | expressions} … | [path]}
```

برای آکولاد **خارج از** حصار (در متن عادی) هنوز از escapeهای Svelte استفاده کنید: `{'{'}` و `{'}'}`.

### متن‌های جایگزین اریب (Italic) در کنار پرچم‌ها (Flags)

<span id="placeholders"></span>

- `--command` *cmd* ، اجرای *cmd* در یک شل تعاملی.
- `--run` *cmd* ، مشابه `--command`، اما غیرتعاملی.
- `--exclude` *regexp* ، رد کردن وابستگی‌هایی که مسیر انبار آن‌ها با *regexp* مطابقت دارد.
- `--keep` *name* ، حفظ متغیر محیطی *name* تحت `--pure`.

### کد درون‌خطی داخل یک پیوند فرگمنت

<span id="code-in-link"></span>

همچنین ببینید [`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL) و [`NIX_PATH`](#named-heading).

### موجودیت‌های HTML: علامت‌های بزرگ‌تر/کوچک‌تر و شناسه‌ی span با escape

<span id="html-entities"></span>

متن ساده با شکل موجودیت (entity) از یک مسیر Nix: شل از `&lt;nixpkgs&gt;` روی `NIX_PATH` می‌آید.

درون علامت‌های بَک‌تیک (همان‌طور که اغلب منتشر می‌شود): `` `&lt;nixpkgs&gt;` `` در مقایسه با حالت خام درون یک بلوک کد:

```shell
$ nix-shell '<nixpkgs>' --attr pan
```

شناسه‌ی محدوده‌ی فراریافته که یک شناسه پیوندخورده را دربر گرفته‌است (شکل انتشاریافته پیرامون متغیرهای محیطی):

- &lt;span id="env-NIX_BUILD_SHELL"&gt;[`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL)&lt;/span&gt;

  شل مورد استفاده برای راه‌اندازی محیط تعاملی.
  پیش‌فرض آن `bash` است که از `bashInteractive` در `&lt;nixpkgs&gt;` گرفته می‌شود، در غیر این صورت از `bash` روی `PATH` استفاده می‌کند.

### کادرهای اخطار تو در تو زیر یک آیتم فهرست

<span id="nested-callouts"></span>

- &lt;span id="env-DEMO"&gt;[`DEMO_VAR`](#env-DEMO)&lt;/span&gt;

  توضیحات متغیر.

  > **نکته**
  >
  > یادداشت تو در تو زیر یک آیتم فهرست (فقط عنوان ضخیم، بدون محدوده‌ی `admonition-kind`).

  > **مثال**
  >
  > کادر مثال تو در تو زیر همان آیتم فهرست.

### حصار خراب در کادر اخطار (شکل انتشاریافته)

<span id="broken-fence-callout"></span>

نحوه ارسال کدهای تو در تو در برخی از صفحات راهنما در حال حاضر (حصار باز به‌طور کامل داخل نقل‌قول نیست):

> **مثال**
>
> این کادر ممکن است حصار را به‌طور تمیز احاطه نکند:

```nix
  > #!/usr/bin/env -S nix-shell --pure
  > let
  >   pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/854fdc68881791812eddd33b2fed94b954979a8e.tar.gz") {};
  > in
  > pkgs.mkShell {
  >   buildInputs = pkgs.bashInteractive;
  > }
  > ```

### زبان‌های محصور اضافی (نمونه‌های shebang)

<span id="extra-langs"></span>

#### پایتون

```python
#! /usr/bin/env nix-shell
#! nix-shell -i python3 --packages python3 python3Packages.prettytable

import prettytable
print("hello")
```

#### پرل

```perl
#! /usr/bin/env nix-shell
#! nix-shell -i perl
#! nix-shell --packages perl

use strict;
print "hello\n";
```

#### Haskell

```haskell
#! /usr/bin/env nix-shell
#! nix-shell -i runghc --packages 'haskellPackages.ghcWithPackages (ps: [ps.tagsoup])'

main = putStrLn "hello"
```

### بلوک کد تورفته (بدون علامت fence)

<span id="indented-code"></span>

تورفته با چهار فاصله (بدون سه بکتیک):

    #! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/0672315759b3e15e2121365f067c1c8c56bb4722.tar.gz

### حصار تو در تو درست زیر یک کادر اخطار (برای مقایسه)

<span id="correct-nested-fence"></span>

> **نکته**
>
> هنگامی که حصار به‌طور کامل درون نقل‌قول قرار دارد، این ساختار را ترجیح دهید:
>
> ```shell
> $ nix-shell '<nixpkgs>' --attr pan --pure
> ```
