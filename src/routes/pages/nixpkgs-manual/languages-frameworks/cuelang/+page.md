# <a id="cuelang"></a> Cue (Cuelang)

[Cuelang](https://cuelang.org/) زبانی است برای:

- توصیف اسکیماها و اعتبارسنجی سازگاری رو به عقب (backward-compatibility)
- تولید کد و اسکیما در قالب‌های مختلف (مانند JSON Schema، OpenAPI)
- انجام پیکربندی شبیه به [Dhall Lang](https://dhall-lang.org/)
- انجام اعتبارسنجی داده‌ها

## <a id="cuelang-quickstart"></a> راهنمای سریع اسکیمای Cuelang

اسکیماهای Cuelang مشابه JSON هستند؛ در ادامه یک برگه تقلب سریع ارائه شده است:

- انواع پیش‌فرض عبارتند از: `null`، `string`، `bool`، `bytes`، `number`، `int`، `float`، و لیست‌ها به صورت `[...T]` که در آن `T` یک نوع است.
- تمام ساختارهایی که با `myStructName: {'{'}'{'{'}'{'}'} &lt;fields&gt; {'{'}'{'}'}'{'}'}` تعریف می‌شوند **باز** (open) هستند -- آن‌ها فیلدهایی را که مشخص نشده‌اند می‌پذیرند.
- ساختارهای بسته را می‌توان با `myStructName: close({'{'}'{'{'}'{'}'} &lt;fields&gt; {'{'}'{'}'}'{'}'})` ساخت -- آن‌ها در آنچه می‌پذیرند سخت‌گیرانه رفتار می‌کنند.
- موارد `#X` **تعاریف** هستند؛ تعاریف ارجاع‌شده **به‌صورت بازگشتی بسته** می‌شوند، یعنی تمام ساختارهای فرزند آن‌ها **بسته** هستند.
- عملگر `&` [عملگر یکسان‌سازی](https://cuelang.org/docs/references/spec/#unification) است (مشابه عملگر ادغام در سطح نوع)، و `|` [عملگر فصل](https://cuelang.org/docs/references/spec/#disjunction) است (مشابه عملگر اجتماع در سطح نوع).
- مقادیر خود نوع **هستند**، به عنوان مثال `myStruct: {'{'}'{'{'}'{'}'} a: 3 {'{'}'{'}'}'{'}'}` یک تعریف نوع معتبر است که تنها مقدار `3` را مجاز می‌داند.

- برای کسب اطلاعات بیشتر درباره معناشناسی، &lt;https://cuelang.org/docs/concepts/logic/&gt; را بخوانید.
- برای آشنایی با مشخصات زبان، &lt;https://cuelang.org/docs/references/spec/&gt; را بخوانید.

## <a id="cuelang-writeCueValidator"></a> `writeCueValidator`

مجموعه‌ی بسته‌های نیکس (Nixpkgs) یک کمک‌کننده `pkgs.writeCueValidator` ارائه می‌دهد که بر اساس اسکیمای Cuelang ارائه‌شده، یک اسکریپت اعتبارسنجی می‌نویسد.

در ادامه یک مثال آورده شده است:

```nix
pkgs.writeCueValidator (pkgs.writeText "schema.cue" ''
  #Def1: {
    field1: string
  }
'') { document = "#Def1"; }
```

- پارامتر اول، فایل اسکیمای Cue است.
- پارامتر دوم، یک پارامتر گزینه‌ها است؛ در حال حاضر، فقط `document` را می‌توان ارسال کرد.

`document`: داده‌های ورودی خود را با این بخش از ساختار یا تعریف تطبیق دهید؛ به عنوان مثال، ممکن است بر اساس داده‌هایی که در حال اعتبارسنجی آن‌ها هستید، از همان فایل اسکیما اما `document`های متفاوتی استفاده کنید.

مثالی دیگر، با توجه به `validator.nix` زیر:

```nix
{
  pkgs ? import <nixpkgs> { },
}:
let
  genericValidator =
    version:
    pkgs.writeCueValidator (pkgs.writeText "schema.cue" ''
      #Version1: {
        field1: string
      }
      #Version2: #Version1 & {
        field1: "unused"
      }'') { document = "#Version${toString version}"; };
in
{
  validateV1 = genericValidator 1;
  validateV2 = genericValidator 2;
}
```

نتیجه اسکریپتی است که فایلی را که به‌عنوان اولین آرگومان ارسال می‌کنید، در برابر اسکیمای ارائه‌شده به `writeCueValidator` اعتبارسنجی می‌کند.

این فایل می‌تواند هر فرمتی باشد که `cue vet` از آن پشتیبانی می‌کند، برای مثال YAML یا JSON.

در ادامه یک مثال به نام `example.json` با توجه به JSON زیر آورده شده است:
```
{ "field1": "abc" }
```

می‌توانید اسکریپت نتیجه (با نام `validate`) را به صورت زیر اجرا کنید:

```shell
$ nix-build validator.nix
$ ./result example.json
$ ./result-2 example.json
field1: conflicting values "unused" and "abc":
    ./example.json:1:13
    ../../../../../../nix/store/v64dzx3vr3glpk0cq4hzmh450lrwh6sg-schema.cue:5:11
$ sed -i 's/"abc"/3/' example.json
$ ./result example.json
field1: conflicting values 3 and string (mismatched types int and string):
    ./example.json:1:13
    ../../../../../../nix/store/v64dzx3vr3glpk0cq4hzmh450lrwh6sg-schema.cue:5:11
```

**محدودیت‌های شناخته‌شده**

* اسکریپت مقادیر **مشخص** را الزام خواهد کرد و تبدیل‌های با افت اطلاعات (سخت‌گیری) را نخواهد پذیرفت. در صورت نیاز می‌توانید این گزینه‌ها را اضافه کنید.
