# <a id="sec-pkgs-nix-gitignore"></a> pkgs.nix-gitignore

`pkgs.nix-gitignore` تابعی است که عملکردی مشابه `builtins.filterSource` دارد، اما امکان فیلتر کردن با استفاده از قالب gitignore را نیز فراهم می‌کند.

## <a id="sec-pkgs-nix-gitignore-usage"></a> نحوه استفاده

`pkgs.nix-gitignore` تعدادی تابع را صادر می‌کند، اما به احتمال زیاد به یکی از توابع `gitignoreSource` یا `gitignoreSourcePure` نیاز خواهید داشت. هر دوی آن‌ها به عنوان آرگومان اول خود، یکی از موارد زیر را می‌پذیرند: ۱. فایلی حاوی خطوط gitignore، ۲. رشته‌ای حاوی خطوط gitignore، یا ۳. فهرستی از هر یک از این دو مورد. این موارد در قالب یک رشته بزرگ واحد به یکدیگر متصل خواهند شد.

```nix
{
  pkgs ? import <nixpkgs> { },
}:
{

  src = nix-gitignore.gitignoreSource [ ] ./source;
  # Simplest version

  src = nix-gitignore.gitignoreSource ''
    supplemental-ignores
  '' ./source;
  # This one reads the ./source/.gitignore and concats the auxiliary ignores

  src = nix-gitignore.gitignoreSourcePure ''
    ignore-this
    ignore-that
  '' ./source;
  # Use this string as gitignore, don't read ./source/.gitignore.

  src = nix-gitignore.gitignoreSourcePure [
    ''
      ignore-this
      ignore-that
    ''
    ~/.gitignore
  ] ./source;
  # It also accepts a list (of strings and paths) that will be concatenated
  # once the paths are turned to strings via readFile.
}
```

این توابع با تنظیم اولین آرگومان فیلتر روی `(_: _: true)`، از توابع `Filter` مشتق شده‌اند:

```nix
{
  gitignoreSourcePure = gitignoreFilterSourcePure (_: _: true);
  gitignoreSource = gitignoreFilterSource (_: _: true);
}
```

این توابع فیلتر همان آرگومان‌هایی را می‌پذیرند که تابع `builtins.filterSource` به فیلترهای خود پاس می‌دهد، بنابراین `fn: gitignoreFilterSourcePure fn ""` باید از نظر مصداقی معادل `filterSource` باشد. اگر فایل چه توسط فیلتر شما و چه توسط gitignoreFilter در فهرست سیاه قرار گیرد، در فهرست سیاه قرار خواهد گرفت.

اگر می‌خواهید فیلتر خودتان را از ابتدا بسازید، می‌توانید از

```nix
{ gitignoreFilter = ign: root: filterPattern (gitignoreToPatterns ign) root; }
```

## <a id="sec-pkgs-nix-gitignore-usage-recursive"></a> فایل‌های gitignore در زیرپوشه‌ها

اگر می‌خواهید از فیلتری استفاده کنید که همانند رفتار پیش‌فرض git، فایل‌های .gitignore را در زیرپوشه‌ها جستجو کند، از این تابع استفاده کنید:

```nix
{
  # gitignoreFilterRecursiveSource = filter: patterns: root:
  # OR
  gitignoreRecursiveSource = gitignoreFilterSourcePure (_: _: true);
}
```
