# 10.3. قالب آرشیو نیکس (NAR)

این مشخصات کامل فرمت [Nix Archive] است.
فرمت آرشیو نیکس از مشخصات انتزاعی یک درخت [file system object] پیروی می‌کند،
زیرا به گونه‌ای طراحی شده است که دقیقاً همان ساختار داده را سریال‌سازی کند.

[Nix Archive]: /pages/nix-manual/store/file-system-object/content-address#serial-nix-archive
[file system object]: /pages/nix-manual/store/file-system-object
فرمت این مشخصات به [Extended Backus–Naur form](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) نزدیک است، با این استثنا که تابع `str(..)` / قانون پارامتردار، پیشوند طول را به رشته‌ها اضافه کرده و آن‌ها را پد (padding) می‌کند.
این کار تجزیه فرمت باینری حاصل را آسان‌تر می‌کند.

کاربران عادی *نیازی* به دانستن این اطلاعات ندارند.
اما برای کسانی که علاقه‌مندند دقیقاً بدانند Nix چگونه کار می‌کند، به عنوان مثال اگر در حال پیاده‌سازی مجدد آن هستند، این اطلاعات می‌تواند مفید باشد.

```ebnf
nar = str("nix-archive-1"), nar-obj;

nar-obj = str("("), nar-obj-inner, str(")");

nar-obj-inner
  = str("type"), str("regular") regular
  | str("type"), str("symlink") symlink
  | str("type"), str("directory") directory
  ;

regular = [ str("executable"), str("") ], str("contents"), str(contents);

symlink = str("target"), str(target);

(* side condition: directory entries must be ordered by their names *)
directory = { directory-entry };

directory-entry = str("entry"), str("("), str("name"), str(name), str("node"), nar-obj, str(")");
```

تابع `str` / قانون پارامتردار به شکل زیر تعریف می‌شود:

- `str(s)` = `int(|s|), pad(s);`

- `int(n)` = نمایش عدد ۶۴ بیتی با ترتیب بایت کوچک (little endian) برای عدد `n`

- `pad(s)` = دنباله بایت‌های `s` که با صفرها تا ضریبی از ۸ بایت پد (پر) شده است.

## مشخصات Kaitai Struct

فرمت آرشیو نیکس (NAR) همچنین به‌طور رسمی با استفاده از [Kaitai Struct](https://kaitai.io/)، یک زبان توصیف رابط (IDL) برای تعریف ساختارهای داده‌ی باینری، توصیف شده است.

> ابزار Kaitai Struct مشخصاتی مستقل از زبان و قابل‌خواندن توسط ماشین را فراهم می‌کند که می‌توان آن را به تجزیه‌کننده‌هایی برای زبان‌های برنامه‌نویسی مختلف (مانند C++، پایتون، جاوا، Rust) کامپایل کرد.

```yaml

```

منبع این مشخصات را می‌توانید در [اینجا](https://github.com/nixos/nix/blob/master/src/nix-manual/source/protocols/nix-archive/nar.ksy) بیابید. مشارکت‌ها و بهبودها در این مشخصات استقبال می‌شود.
