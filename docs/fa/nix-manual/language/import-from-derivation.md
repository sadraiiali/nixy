# درون‌ریزی از In-Derivation (Import From Derivation)

مقدار یک عبارت Nix می‌تواند به محتویات یک [شیء انبار] وابسته باشد.

[شیء انبار]: @docroot@/store/store-object.md

پاس دادن عبارتی مانند `expr` که به یک [مسیر انبار](@docroot@/store/store-path.md) ارزیابی می‌شود به هر تابع توکاری که از سیستم‌فایل خوانش انجام دهد، «درون‌ریزی از In-Derivation (IFD)» نامیده می‌شود:

- [`import`](./builtins.md#builtins-import)` expr`
- [`builtins.readFile`](./builtins.md#builtins-readFile)` expr`
- [`builtins.readFileType`](./builtins.md#builtins-readFileType)` expr`
- [`builtins.readDir`](./builtins.md#builtins-readDir)` expr`
- [`builtins.pathExists`](./builtins.md#builtins-pathExists)` expr`
- [`builtins.filterSource`](./builtins.md#builtins-filterSource)` f expr`
- [`builtins.path`](./builtins.md#builtins-path)` { path = expr; }`
- [`builtins.hashFile`](./builtins.md#builtins-hashFile)` t expr`
- `builtins.scopedImport x drv`

هنگامی که نیاز به دسترسی به مسیر انبار باشد، ارزیابی متوقف شده، شیء انبار متناظر [realised] (محقق) می‌شود و سپس ارزیابی از سر گرفته خواهد شد.

[realised]: @docroot@/glossary.md#gloss-realise

این مسئله پیامدهایی روی کارایی دارد:
ارزیابی تنها زمانی می‌تواند به پایان برسد که تمام اشیاء انبار موردنیاز محقق شده باشند.
از آنجا که ارزیاب زبان Nix ترتیبی (sequential) است، مسیرهای انبار را برای خواندن، یکی پس از دیگری پیدا می‌کند.
اگرچه تحقق‌بخشی همیشه به صورت موازی انجام می‌شود، در این حالت نمی‌توان آن را برای تمام مسیرهای انبار موردنیاز به صورت همزمان انجام داد و در نتیجه بسیار کندتر از حالت عادی خواهد بود.

با قرار دادن [`allow-import-from-derivation`](../command-ref/conf-file.md#conf-allow-import-from-derivation) روی مقدار `false` می‌توان تحقق‌بخشی اشیاء انبار را در طول ارزیابی غیرفعال کرد.
بدون IFD تضمین می‌شود که ارزیابی کامل شده و Nix می‌تواند پیش از آغاز هرگونه تحقق‌بخشی، یک طرح ساخت تولید کند.

## مثال

در عبارت Nix زیر، درایویشن داخلی `drv` فایلی با محتوای `hello` تولید می‌کند.

```nix
# IFD.nix
let
  drv = derivation {
    name = "hello";
    builder = "/bin/sh";
    args = [ "-c" "echo -n hello > $out" ];
    system = builtins.currentSystem;
  };
in "${builtins.readFile drv} world"
```

```shellSession
nix-instantiate IFD.nix --eval --read-write-mode
```

```
building '/nix/store/348q1cal6sdgfxs8zqi9v8llrsn4kqkq-hello.drv'...
"hello world"
```

محتوای خروجی derivation باید پیش از آنکه با [`readFile`](./builtins.md#builtins-readFile) خوانده شود، [realised] (تحقق) یابد.
تنها در این صورت است که ارزیابی می‌تواند برای تولید نتیجه نهایی ادامه پیدا کند.

## تصویرسازی

به عنوان یک تقریب اولیه، گراف جریان دادهٔ زیر نشان می‌دهد که اگر مقدار یک عبارت Nix به تحقق یک [store object] وابسته باشد، چگونه ارزیابی و ساخت (build) با یکدیگر در هم آمیخته می‌شوند.
جعبه‌ها ساختارهای داده هستند و برچسب پیکان‌ها تبدیل‌ها را نشان می‌دهند.

```
+----------------------+             +------------------------+
| Nix evaluator        |             | Nix store              |
|  .----------------.  |             |                        |
|  | Nix expression |  |             |                        |
|  '----------------'  |             |                        |
|          |           |             |                        |
|       evaluate       |             |                        |
|          |           |             |                        |
|          V           |             |                        |
|    .------------.    |             |                        |
|    | derivation |    |             |  .------------------.  |
|    | expression |----|-instantiate-|->| store derivation |  |
|    '------------'    |             |  '------------------'  |
|                      |             |           |            |
|                      |             |        realise         |
|                      |             |           |            |
|                      |             |           V            |
|  .----------------.  |             |    .--------------.    |
|  | Nix expression |<-|----read-----|----| store object |    |
|  '----------------'  |             |    '--------------'    |
|          |           |             |                        |
|       evaluate       |             |                        |
|          |           |             |                        |
|          V           |             |                        |
|    .------------.    |             |                        |
|    |   value    |    |             |                        |
|    '------------'    |             |                        |
+----------------------+             +------------------------+
```

به طور مفصل‌تر، نمودار توالی زیر نشان می‌دهد که عبارت چگونه گام‌به‌گام ارزیابی می‌شود و ارزیابی در کجا متوقف می‌شود تا منتظر ظاهر شدن خروجی ساخت بماند.

```
.-------.     .-------------.                        .---------.
|Nix CLI|     |Nix evaluator|                        |Nix store|
'-------'     '-------------'                        '---------'
    |                |                                    |
    |evaluate IFD.nix|                                    |
    |--------------->|                                    |
    |                |                                    |
    |  evaluate `"${readFile drv} world"`                 |
    |                |                                    |
    |    evaluate `readFile drv`                          |
    |                |                                    |
    |   evaluate `drv` as string                          |
    |                |                                    |
    |                |instantiate /nix/store/...-hello.drv|
    |                |----------------------------------->|
    |                :                                    |
    |                :  realise /nix/store/...-hello.drv  |
    |                :----------------------------------->|
    |                :                                    |
    |                                                     |--------.
    |                :                                    |        |
    |      (evaluation blocked)                           |  echo hello > $out
    |                :                                    |        |
    |                                                     |<-------'
    |                :        /nix/store/...-hello        |
    |                |<-----------------------------------|
    |                |                                    |
    |  resume `readFile /nix/store/...-hello`             |
    |                |                                    |
    |                |   readFile /nix/store/...-hello    |
    |                |----------------------------------->|
    |                |                                    |
    |                |               hello                |
    |                |<-----------------------------------|
    |                |                                    |
    |      resume `"${"hello"} world"`                    |
    |                |                                    |
    |        resume `"hello world"`                       |
    |                |                                    |
    | "hello world"  |                                    |
    |<---------------|                                    |
.-------.     .-------------.                        .---------.
|Nix CLI|     |Nix evaluator|                        |Nix store|
'-------'     '-------------'                        '---------'
```
