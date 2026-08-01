# درون‌گذاری رشته

درون‌گذاری رشته یک ویژگی زبانی است که در آن یک [رشته]، [مسیر] یا [نام صفت][attribute set] می‌تواند حاوی عبارت‌هایی باشد که در داخل `${ }` (علامت دلار با آکولاد) قرار گرفته‌اند.

چنین ساختاری *رشته درون‌گذاری‌شده* نامیده می‌شود و عبارت درون آن یک [عبارت درون‌گذاری‌شده](#interpolated-expression) است.

[string]: ./types.md#type-string
[path]: ./types.md#type-path
[attribute set]: ./types.md#type-attrs

> **نحو**
>
> *interpolation_element* → `${` *expression* `}`

## مثال‌ها

### رشته

به‌جای نوشتن

```nix
"--with-freetype2-library=" + freetype + "/lib"
```

(که در آن `freetype` یک [عبارت derivation] است)، به جای آن می‌توانید بنویسید

[عبارت derivation]: @docroot@/glossary.md#gloss-derivation-expression

```nix
"--with-freetype2-library=${freetype}/lib"
```

مورد دوم به‌طور خودکار به مورد اول ترجمه می‌شود.

یک مثال پیچیده‌تر (از عبارت Nix مربوط به [Qt](http://www.trolltech.com/products/qt)):

```nix
configureFlags = "
  -system-zlib -system-libpng -system-libjpeg
  ${if openglSupport then "-dlopen-opengl
    -L${mesa}/lib -I${mesa}/include
    -L${libXmu}/lib -I${libXmu}/include" else ""}
  ${if threadSupport then "-thread" else "-no-thread"}
";
```

توجه داشته باشید که عبارت‌ها و رشته‌های Nix می‌توانند به طور دلخواه تو در تو باشند؛ در این حالت، رشته‌ی بیرونی شامل عبارت‌های درون‌گذاری‌شده‌ی مختلفی است که خودشان حاوی رشته‌هایی هستند (مانند `"-thread"` به عنوان مثال)، و برخی از آن‌ها به نوبه خود حاوی عبارت‌های درون‌گذاری‌شده هستند (مانند `${mesa}`).

برای نوشتن یک `${` به صورت صریح در یک رشته‌ی معمولی، آن را با یک اسلش به عقب (`\`) فرار (escape) دهید.

> **مثال**
>
```nix
> "echo \${PATH}"
> ```
>
>     "echo ${PATH}"

برای نوشتن یک کاراکتر `${` به شکل تحت‌اللفظی (literal) در یک رشته تورفته، آن را با دو علامت نقل‌قول تکی (`''`) فرار (escape) دهید.

> **مثال**
>
```nix
> ''
> echo ''${PATH}
> ''
> ```
>
> "echo ${PATH}\n"

مقدار `$${` را می‌توان به صورت تحت‌اللفظی در هر رشته‌ای نوشت.

> **مثال**
>
> در ابزار Make، علامت `$` در نام فایل‌ها یا دستورات ساخت به شکل `$$` نمایش داده می‌شود؛ برای اطلاعات بیشتر به [GNU `make`: Basics of Variable Reference](https://www.gnu.org/software/make/manual/html_node/Reference.html#Basics-of-Variable-References) مراجعه کنید.
> این موضوع را می‌توان مستقیماً در رشته‌های زبان Nix بیان کرد:
>
```nix
> ''
>   MAKEVAR = Hello
>   all:
>   	@export BASHVAR=world; echo $(MAKEVAR) $${BASHVAR}
> ''
> ```
>
>     "MAKEVAR = Hello\nall:\n\t@export BASHVAR=world; echo $(MAKEVAR) $\${BASHVAR}\n"

برای جزئیات بیشتر، [مستندات مربوط به رشته‌ها][string] را ببینید.

### مسیر (Path)

به‌جای نوشتن

```nix
./. + "/" + foo + "-" + bar + ".nix"
```

یا

```nix
./. + "/${foo}-${bar}.nix"
```

می‌توانید به جای آن بنویسید

```nix
./${foo}-${bar}.nix
```

### نام صفت (attribute)

<!--
FIXME: these examples are redundant with the main page on attribute sets.
figure out what to do about that
-->

نام‌های صفت (attribute) می‌توانند رشته‌های درون‌گذاری‌شده باشند.

> **مثال**
>
```nix
> let name = "foo"; in
> { ${name} = 123; }
> ```
>
> { foo = 123; }

صفت‌ها (attributes) را می‌توان با رشته‌های درون‌گذاری‌شده انتخاب کرد.

> **مثال**
>
```nix
> let name = "foo"; in
> { foo = 123; }.${name}
> ```
>
>     123

# عبارت درون‌گذاری‌شده

عبارتی که درون‌گذاری می‌شود باید به یکی از موارد زیر ارزیابی شود:

- یک [رشته]
- یک [مسیر]
- یک [مجموعه ویژگی] که دارای صفت `__toString` یا صفت `outPath` باشد

  - صفت `__toString` باید تابعی باشد که خود مجموعه ویژگی را به عنوان آرگومان گرفته و یک رشته برمی‌گرداند
  - صفت `outPath` باید یک رشته باشد

  این مورد شامل [عبارت‌های derivation](./derivations.md) یا [ورودی‌های فلیک](@docroot@/command-ref/new-cli/nix3-flake.md#flake-inputs) (آزمایشی) نیز می‌شود.

یک رشته به خودش درون‌گذاری می‌شود.

یک مسیر در یک عبارت درون‌گذاری‌شده ابتدا در انبار Nix کپی می‌شود، و رشته‌ی حاصل همان [مسیر انبار] [شیء انبار] (store object) تازه ایجادشده است (@docroot@/store/store-object.md).

[مسیر انبار]: @docroot@/store/store-path.md

> **مثال**
>
```console
> $ mkdir foo
> ```
>
> به پوشه خالی در یک عبارت درون‌گذاری‌شده ارجاع دهید:
>
```nix
> "${./foo}"
> ```
>
>     "/nix/store/2hhl2nz5v0khbn06ys82nrk99aa1xxdw-foo"

یک derivation هنگام درون‌گذاری به [مسیر انبار] نخستین [output](./derivations.md#attr-outputs) خود تبدیل می‌شود.

> **مثال**
>
```nix
> let
> pkgs = import <nixpkgs> {};
> in
> "${pkgs.hello}"
> ```
>
> "/nix/store/qnlr7906z0mrl2syrkdbpicffq02nw07-hello-2.12.1"

یک مجموعه ویژگی به مقدار بازگشتی تابع موجود در `__toString` که روی خودِ مجموعه ویژگی اعمال شده‌است، درون‌گذاری می‌شود.

> **مثال**
>
```nix
> let
>   a = {
>     value = 1;
>     __toString = self: toString (self.value + 1);
>   };
> in
> "${a}"
> ```
>
>     "2"

یک مجموعه ویژگی (attribute set) نیز به مقدار صفت `outPath` خود درون‌گذاری می‌شود.

> **مثال**
>
>
```nix
> let
> a = { outPath = "foo"; };
> in
> "${a}"
> ```
>
> "foo"

اگر هم `__toString` و هم `outPath` در یک مجموعه ویژگی حضور داشته باشند، `__toString` اولویت دارد.

> **مثال**
>
```nix
> let
>   a = { __toString = _: "yes"; outPath = throw "no"; };
> in
> "${a}"
> ```
>
>     "yes"

اگر هیچ‌کدام وجود نداشته باشد، خطایی پرتاب می‌شود.

> **مثال**
>
```nix
> let
> a = {};
> in
> "${a}"
> ```
>
> error: cannot coerce a set to a string: { }
>
> at «string» :4:2:
>
> 3| in
> 4| "${a}"
> | ^
