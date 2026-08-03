# مجموعه‌ی کامل سینتکس Markdown

**صفحه‌ی تست** داخلی در `/test/syntax`. این صفحه فرم‌های Markdown (و چند فرم HTML) را که این اپلیکیشن واقعاً با mdsvex، Prism و CSS سایت رندر می‌کند جمع می‌کند. برای بررسی طرح‌بندی، راست‌به‌چپ (RTL)، چپ‌به‌راست (LTR) کد، کادرهای اخطار و رفت‌وبرگشت ویرایشگر از آن استفاده کنید.

## فهرست مطالب

- [پاراگراف‌ها و تأکید](#paragraphs)
- [سرتیترها و لنگرها](#headings)
- [پیوندها](#links)
- [تصاویر](#images)
- [فهرست‌ها](#lists)
- [نقل‌قول‌ها](#blockquotes)
- [تذکرات / کادرهای اخطار](#admonitions)
- [کد درون‌خطی و کلید کیبورد](#inline-code)
- [بلوک‌های کد محصور](#fenced-code)
- [جداول](#tables)
- [خط افقی](#hr)
- [برجسته‌سازی با mark](#mark)
- [کارت‌های هاب](#hub-cards)
- [نمونه‌ی مختلط راست‌به‌چپ](#mixed)
- [الگوهای صفحه‌ی راهنما (از nix-shell)](#manpage)

---

## پاراگراف‌ها و تأکید

<span id="paragraphs"></span>

یک پاراگراف ساده با متن **پررنگ**، *کج*، ***پررنگ کج***، و مقداری `inline code` که در جمله ترکیب شده‌است تا شکستن خطوط و ایزوله‌سازی قابل‌مشاهده بمانند.

اگر تجزیه‌کننده (parser) آن‌ها را بپذیرد، می‌توانید از __پررنگ با زیرخط__ و _کج با زیرخط_ نیز استفاده کنید.

شکستن خط سخت پس از دو فاصله:
خط دوم باید زیر خط اول قرار بگیرد.

## سرتیترها و لنگرها

<span id="headings"></span>

# سرتیتر ۱ (در صفحات محتوایی نادر است)

## سرتیتر ۲

### سرتیتر ۳

#### سرتیتر ۴

##### سرتیتر ۵

###### سرتیتر ۶

سرتیتر با هدف قطعه (fragment) صریح:

## <span id="named-heading"></span> سرتیتر نام‌گذاری‌شده

پیوند به آن قطعه: [پرش به سرتیتر نام‌گذاری‌شده](#named-heading).

## پیوندها

<span id="links"></span>

- مسیر داخلی: [گام‌های نخستین](/pages/first-steps)
- مستندات داخلی: [نصب Nix](/pages/nix-dev/install-nix)
- HTTPS خارجی: [nixos.org](https://nixos.org/)
- گیت‌هاب خارجی: [NixOS/nix](https://github.com/NixOS/nix)
- سبک YouTube (آیکون از طریق rehype): [ویدیو نمونه](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
- پیوند خودکار: <https://nix.dev/>
- پیوند مبتنی بر ارجاع: [راهنمای Nix][nix-manual]
- پیوند با صفت title: [Nixpkgs](https://github.com/NixOS/nixpkgs "Nixpkgs repository")

[nix-manual]: /pages/nix-manual

شبیه به ایمیل (در صورت مجاز بودن): <noreply@example.com>

## تصاویر

<span id="images"></span>

تصویر درون‌خطی با متن جایگزین (آیکون سایت):

![دانه برف Nix](/icons/nix-snowflake.svg)

تصویر پیوندداده‌شده:

[![منوی بوت NixOS](https://nixos.org/images/screenshots/nixos-boot-menu.png)](https://nixos.org/images/screenshots/nixos-boot-menu.png)

## فهرست‌ها

<span id="lists"></span>

نامرتب:

- آلفا
- براوو
  - تو در تو ۱
  - تو در تو ۲
- چارلی

مرتب:

1. نخست
2. دوم
   1. مرتب تو در تو
   2. دوباره مرتب تو در تو
3. سوم

فهرست فشرده با کد درون‌خطی: `nix`، `nixos-rebuild`، `/nix/store`.

فهرست غیرفشرده:

- پاراگراف اول در یک آیتم فهرست.

  پاراگراف دوم در همان آیتم.

- آیتمی دیگر.

سبک وظیفه (GFM، در صورت فعال بودن):

- [x] آیتم انجام‌شده
- [ ] آیتم باز

## نقل‌قول‌ها

<span id="blockquotes"></span>

> یک نقل‌قول ادبی ساده. کدهای تو در تو مانند `hello` باید به صورت LTR باقی بمانند.
>
> پاراگراف دوم در همان نقل‌قول.

> نقل‌قول‌های تو در تو:
>
> > خط نقل‌قول درونی.

## تذکرات / کادرهای اخطار

<span id="admonitions"></span>

انتشار سایت دستورات MyST را به نقل‌قول‌هایی همراه با
`<span class="admonition-kind" data-kind="…"></span>` و یک خط **عنوان** تبدیل می‌کند.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> این یک کادر «نکته» است. پیوندها کار می‌کنند: [nix.dev](https://nix.dev/).

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> برای ابزارهای آنی، `nix shell` را ترجیح دهید.

> <span class="admonition-kind" data-kind="hint"></span>
>
> **راهنمایی**
>
> در CSS هم‌خانواده‌ی tip است.

> <span class="admonition-kind" data-kind="important"></span>
>
> **مهم**
>
> پیش از ارتقا، این مطلب را بخوانید.

> <span class="admonition-kind" data-kind="attention"></span>
>
> **توجه**
>
> هم‌خانواده با مهم.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> فلیک‌ها ممکن است کل درخت را در انبار کپی کنند.

> <span class="admonition-kind" data-kind="caution"></span>
>
> **احتیاط**
>
> ابتدا دسترسی‌ها را بررسی کنید.

> <span class="admonition-kind" data-kind="danger"></span>
>
> **خطر**
>
> عملیات مخرب.

> <span class="admonition-kind" data-kind="error"></span>
>
> **خطا**
>
> ساخت با شکست مواجه شد.

> <span class="admonition-kind" data-kind="seealso"></span>
>
> **همچنین ببینید**
>
> مرتبط: [واژه‌نامه](/glossary).

> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> یک مثال کاربردی کوتاه.

> <span class="admonition-kind" data-kind="admonition"></span>
>
> **اعلان**
>
> نوع اعلان عمومی.

کادر اخطار همراه با بلوک کد محصور در داخل:

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> اجرا کنید:
>
> ```shell
> $ nix --version
> nix (Nix) 2.11.0
> ```

کادر اخطار همراه با فهرست:

> <span class="admonition-kind" data-kind="tip"></span>
>
> **راهنمایی**
>
> چک‌لیست:
>
> - نصب Nix
> - باز کردن یک ترمینال **جدید**
> - اجرای `nix --version`

کادر قدیمی فقط با عنوان پررنگ (بدون تگ `admonition-kind`):

> **توجه**
>
> زمانی استایل‌دهی می‌شود که اولین فرزند یک عنوان قوی باشد.

## کد درون‌خطی و kbd

<span id="inline-code"></span>

مسیرها و فلگ‌ها باید در پاراگراف‌های راست‌به‌چپ (RTL) به صورت چپ‌به‌راست (LTR) خوانده شوند: `/nix/store`، `~/.config/nix/nix.conf`، `--extra-experimental-features`، `pkgs.hello`.

تراشه‌های شبیه صفحه‌کلید اغلب در این اپلیکیشن با بک‌تیک نوشته می‌شوند (`Ctrl+E`، `Ctrl+K`)؛ در صورت نیاز از HTML `kbd` هم استفاده می‌شود:

برای ویرایش در محیط توسعه، کلیدهای <kbd>Ctrl</kbd>+<kbd>E</kbd> را فشار دهید.

علامت‌گذاری ترکیبی: استفاده از `foo.bar` و `a/b/c` در کنار کلمات فارسی یا انگلیسی.

## بلوک‌های کد محصورشده

<span id="fenced-code"></span>

### Nix

```nix
{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  packages = [
    pkgs.hello
    pkgs.cowsay
  ];
}
```

### شل / Bash

```shell
$ curl -L https://nixos.org/nix/install | sh -s -- --daemon
$ nix --version
```

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "hello from bash"
```

### نشست شل

```shell-session
$ nix-env -iA nixpkgs.hello
installing 'hello-2.12.1'
$ hello
Hello, world!
```

### تفاوت (Diff)

```diff
--- a/flake.nix
+++ b/flake.nix
@@ -1,5 +1,6 @@
 {
   description = "demo";
+  # added line
 }
```

### JSON

```json
{
  "name": "example",
  "version": 1,
  "nested": { "ok": true }
}
```

### متن / plain

```text
/nix/store/b6gvzjyb2pg0…-firefox-33.1
```

### حصار بدون برچسب زبان

```
plain fence without a language tag
line two
```

### اشاره به حصارها در متن

برای نوشتن یک حصار در مستندات، با سه بک‌تیک و شناسه‌ی زبان مانند `nix` شروع کنید.

## جدول‌ها

<span id="tables"></span>

| پرچم | معنی | پیش‌فرض |
| --- | --- | --- |
| `max-jobs` | درایویشن‌های موازی | `1` |
| `cores` | هسته‌ها به ازای هر ساخت | `0` (همه) |
| `NIX_BUILD_CORES` | بازنشانی متغیر محیطی | از `cores` |

نمایش ترازسازی:

| چپ | وسط | راست |
| :--- | :---: | ---: |
| a | b | c |
| سلول طولانی‌تر | وسط | 42 |

## خط افقی

<span id="hr"></span>

بالای خط.

---

پایین خط.

## برجسته‌سازی با mark

<span id="mark"></span>

Nix یک <mark>مدیر بسته‌ی کاملاً تابعی</mark> است. برجسته‌سازی به‌صورت HTML `<mark>` برای mdsvex باقی می‌ماند (در ویرایشگر درون‌صفحه‌ای: `Ctrl+H`).

## کارت‌های هاب

<span id="hub-cards"></span>

HTML مختص سایت که در هاب‌های nix.dev استفاده می‌شود (توسط مسیر تبدیل HTML به Markdown در ویرایشگر حفظ می‌شود):

<div class="nd-hub-cards" data-no-panel>
  <a class="nd-hub-card" href="/pages/nix-dev/tutorials" data-no-panel="1">
    <span class="nd-hub-card__title">آموزش‌ها</span>
    <span class="nd-hub-card__desc">درس‌هایی برای شروع کار</span>
  </a>
  <a class="nd-hub-card" href="/pages/nix-dev/guides" data-no-panel="1">
    <span class="nd-hub-card__title">راهنماها</span>
    <span class="nd-hub-card__desc">دستورالعمل‌ها و شیوه‌نامه‌ها</span>
  </a>
  <a class="nd-hub-card" href="/pages/nix-dev/reference" data-no-panel="1">
    <span class="nd-hub-card__title">مرجع</span>
    <span class="nd-hub-card__desc">جزئیات فنی دقیق</span>
  </a>
  <a class="nd-hub-card" href="/pages/nix-dev/concepts" data-no-panel="1">
    <span class="nd-hub-card__title">مفاهیم</span>
    <span class="nd-hub-card__desc">تاریخچه و ایده‌ها</span>
  </a>
</div>

## نمونه ترکیبی (متن فارسی)

<span id="mixed"></span>

هنگامی که صفحه راست‌به‌چپ (RTL) است، شناسه‌های انگلیسی باید چپ‌به‌راست (LTR) بمانند: با دستور `curl -L https://nixos.org/nix/install | sh` نصب کنید، سپس `nix --version` را بررسی کنید. مسیرهای انبار شبیه `/nix/store/…-hello-2.12.1` هستند.

> <span class="admonition-kind" data-kind="warning"></span>
>
> **هشدار**
>
> اطلاعات محرمانه را در مسیری که به انبار کپی می‌شود قرار ندهید، برای مثال `./secrets/token`.

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

---

پایان نمونه جامع. اگر موردی در اینجا به شکل نادرست رندر شد، پیش از دستکاری تک‌تک صفحات مستندات، CSS یا mdsvex را اصلاح کنید.
