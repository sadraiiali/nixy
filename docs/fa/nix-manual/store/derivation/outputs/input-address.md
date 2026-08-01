# خروجی‌های derivation با آدرس‌دهی ورودی

[input addressing]: #input-addressing

«آدرس‌دهی ورودی» (Input addressing) به این معناست که شیء انبار بر اساس *نحوه ساخته‌شدنش* آدرس‌دهی می‌شود تا *چیزی که واقعاً هست*.
به عبارت دیگر، مسیر انبار یک خروجی با آدرس‌دهی ورودی، تابع خود خروجی نیست، بلکه تابع derivation تولیدکننده آن است.
حتی اگر دو مسیر انبار محتوای کاملاً یکسانی داشته باشند، اما به روش‌های متفاوتی تولید شده باشند و یکی از آن‌ها دارای آدرس‌دهی ورودی باشد، مسیرهای انبار متفاوتی خواهند داشت؛ بنابراین تضمین می‌شود که آن‌ها یک شیء انبار یکسان نیستند.

## خروجی‌های derivation با آدرس‌دهی محتوایی پیمانه‌ای (Modulo) {#hash-quotient-drv}

یک پیاده‌سازی ساده‌انگارانه برای محاسبه هش خروجی در خروجی‌های با آدرس‌دهی ورودی، این است که هش derivation و خروجی را با هم هش کنیم.
این روش به‌وضوح ویژگی‌های یکتایی موردنظر ما را برای خروجی‌های با آدرس‌دهی ورودی فراهم می‌کند، اما از یک ناکارآمدی رنج می‌برد.
به‌طور خاص، هر زمان تغییری در یک derivation با خروجی ثابت (fixed-output derivation) ایجاد شود، ساخت‌های (builds) جدیدی مورد نیاز خواهد بود؛ با وجود اینکه از نظر اثبات‌پذیر هیچ تفاوتی در ورودی‌های derivation جدید نسبت به حالت قبلی آن وجود ندارد.
به‌طور ملموس، این امر باعث ایجاد یک «ساخت مجدد انبوه» (mass rebuild) در هر زمان که هر جزئیات مربوط به دریافت (fetching)، از جمله فهرست‌های آینه‌ها (mirror lists)، گواهی‌های مرجع صادرکننده گواهی (CA) و غیره تغییر کند، می‌شود.

برای حل این مشکل، ما هش‌های خروجی را به شکل متفاوتی محاسبه می‌کنیم تا برخی از هش‌های خروجی یکسان شوند.
ما این مفهوم را هش کردن خارج‌قسمتی (quotient hashing) می‌نامیم که برگرفته از انواع یا مجموعه‌های خارج‌قسمتی (quotient types or sets) است.

بنابراین، [بخش هش](@docroot@/store/store-path.md#digest) مسیرهای خروجی یک derivation با آدرس‌دهی ورودی را چگونه محاسبه می‌کنیم؟
این کار توسط تابع `hashQuotientDerivation` که در ادامه نشان داده شده‌است، انجام می‌شود.

ابتدا، نکته‌ای درباره‌ی ورودی‌ها.
تابع `hashQuotientDerivation` تنها روی derivationهایی تعریف می‌شود که [ورودی‌هایشان](@docroot@/store/derivation/index.md#inputs) شکل مرتبه اول (first-order) داشته باشند:
```typescript
type ConstantPath = {
  path: StorePath;
};

type FirstOrderOutputPath = {
  drvPath: StorePath;
  output: OutputName;
};

type FirstOrderDerivingPath = ConstantPath | FirstOrderOutputPath;

type Inputs = Set<FirstOrderDerivingPath>;
```

برای الگوریتم زیر، ما یک derivation را در نظر می‌گیریم که در آن دو نوع مسیر مشتق‌شده (مرتبه اول) به دو مجموعه به شرح زیر تقسیم می‌شوند:
```typescript
type Derivation = {
  // inputs: Set<FirstOrderDerivingPath>; // replaced
  inputSrcs: Set<ConstantPath>; // new instead
  inputDrvOutputs: Set<FirstOrderOutputPath>; // new instead
  // ...other fields...
};
```

در حالت مرتبه بالاتر [که در حال حاضر آزمایشی است][xp-feature-dynamic-derivations] و در آن خروجی‌های خروجی‌ها به عنوان [مسیرهای اشتقاق ساخت][deriving-path] و در نتیجه ورودی‌های derivation مجاز هستند، آن دسته از derivationهایی که از این عمومیت‌بخشی استفاده می‌کنند، آرگومان‌های معبری برای این تابع نیستند.
آن دسته از derivationها باید ابتدا به اندازه کافی (تا حدودی) [رزولوشن یا حل شوند](@docroot@/store/resolution.md)، تا حدی که هیچ‌گونه ورودی مرتبه بالای این‌چنینی باقی نماند.
سپس، و فقط در آن صورت است که می‌توان آدرس‌های ورودی را اختصاص داد.

```
function hashQuotientDerivation(drv) -> Hash:
    assert(drv.outputs are input-addressed)
    drv′ ← drv with {
        inputDrvOutputs = ⋃(
            assert(drvPath is store path)
            case hashOutputsOrQuotientDerivation(readDrv(drvPath)) of
                drvHash : Hash →
                    (drvHash.toBase16(), output)
                outputHashes : Map[String, Hash] →
                    (outputHashes[output].toBase16(), "out")
            | (drvPath, output) ∈ drv.inputDrvOutputs
        )
    }
    return hashSHA256(printDrv(drv′))

function hashOutputsOrQuotientDerivation(drv) -> Map[String, Hash] | Hash:
    if drv.outputs are content-addressed:
        return {
            outputName ↦ hashSHA256(
                "fixed:out:" + ca.printMethodAlgo() +
                ":" + ca.hash.toBase16() +
                ":" + ca.makeFixedOutputPath(drv.name, outputName))
            | (outputName ↦ output) ∈ drv.outputs
            , ca = output.contentAddress // or get from build trace if floating
        }
    else: // drv.outputs are input-addressed
        return hashQuotientDerivation(drv)
```

### `hashQuotientDerivation`

ما هر عنصر را در `inputDrvOutputs` درایویشن با استفاده از داده‌های حاصل از فراخوانی `hashOutputsOrQuotientDerivation` روی `drvPath` آن عنصر جایگزین می‌کنیم.
هنگامی که `hashOutputsOrQuotientDerivation` یک هش درایویشن تکی را برمی‌گرداند (زیرا درایویشن ورودی مورد نظر از نوع آدرس‌دهی‌شده بر اساس ورودی است)، ما به سادگی `drvPath` را با آن هش جابه‌جا می‌کنیم و نام خروجی را ثابت نگه می‌داریم.
هنگامی که `hashOutputsOrQuotientDerivation` نقشه‌ای از آدرس‌های محتوا به ازای هر خروجی را برمی‌گرداند، ما خروجی مورد نظر را جستجو کرده و آن را با نام خروجی `out` جفت می‌کنیم.

درایویشن شبه‌مانند حاصل (که به جای مسیرهای انبار در `inputDrvs` دارای هش‌ها است) سپس چاپ می‌شود (در [فرمت "ATerm"](@docroot@/protocols/derivation-aterm.md)) و هش می‌شود، و این به عنوان هش «درایویشن خارج‌قسمتی» (quotient derivation) در نظر گرفته می‌شود.

هنگام محاسبه هش‌های خروجی، `hashOutputsOrQuotientDerivation` روی یک درایویشن آدرس‌دهی‌شده بر اساس ورودی و تقریباً کامل فراخوانی می‌شود که صرفاً مسیرهای خروجی آدرس‌دهی‌شده بر اساس ورودی آن مفقود هستند.
سپس از هش درایویشن برای محاسبه مسیرهای خروجی برای هر خروجی استفاده می‌شود.
<!-- TODO describe how this is done. -->
سپس می‌توان آن مسیرهای خروجی را در درایویشن آدرس‌دهی‌شده بر اساس ورودیِ تقریباً کامل جایگذاری کرد تا کامل شود.

> **نکته**
>
> ممکن است در حالت `(outputHashes[output].toBase16(), "out")` انحراف ناخواسته‌ای از مشخصات فنی (Specification) پیاده‌سازی شده باشد.
> این موضوع مهلک نیست زیرا این انحراف فقط برای درایویشن‌های آدرس‌دهی‌شده بر اساس محتوا با بیش از یک خروجی اعمال می‌شود و این اتفاق تنها در حالت شناور رخ می‌دهد که یک [ویژگی آزمایشی][xp-feature-ca-derivations] است.
> پس از رفع این اشکال، این نکته حذف خواهد شد.

### `hashOutputsOrQuotientDerivation`

تابع `hashOutputsOrQuotientDerivation` چگونه کار می‌کند؟
این تابع بر اساس اینکه خروجی‌های درایویشن قرار است بر اساس ورودی یا محتوا آدرس‌دهی شوند، از دو حالت اصلی تشکیل شده‌است.

#### حالت خروجی‌های آدرس‌دهی‌شده بر اساس ورودی

در حالت آدرس‌دهی‌شده بر اساس ورودی، این تابع صرفاً `hashQuotientDerivation` را فراخوانی کرده و آن هش درایویشن را برمی‌گرداند.
این باعث می‌شود که `hashQuotientDerivation` و `hashOutputsOrQuotientDerivation` به صورت متقابل بازگشتی (mutually-recursive) باشند.

> **نکته**
>
> در این حالت، `hashQuotientDerivation` روی یک درایویشن آدرس‌دهی‌شده بر اساس ورودیِ *کامل* فراخوانی می‌شود که مسیرهای خروجی آن از پیش محاسبه شده‌اند.
> جایگزین‌سازی `inputDrvs` به هر حال انجام می‌شود.

#### حالت خروجی‌های آدرس‌دهی‌شده بر اساس محتوا

اگر خروجی‌ها [آدرس‌دهی‌شده بر اساس محتوا](./content-address.md) باشند، آنگاه برای هر خروجی، هشی مشتق‌شده از آدرس محتوای آن خروجی محاسبه می‌شود.

> **نکته**
>
> در حالت آدرس‌دهی‌شده بر اساس محتوای [ثابت](./content-address.md#fixed)، آدرس‌های محتوای خروجی‌ها از پیش به صورت ایستا مشخص می‌شوند، بنابراین این کار همیشه به درستی انجام می‌شود.
> (حالت ثابت همان چیزی است که شبه‌کد نشان می‌دهد.)
>
> در حالت [شناور](./content-address.md#floating)، آدرس‌های محتوا از پیش مشخص نمی‌شوند.
> این همان چیزی است که نظر «یا در صورت شناور بودن، دریافت از [ردیابی ساخت](@docroot@/store/build-trace.md)» به آن اشاره دارد.
> در این حالت، الگوریتم تا زمانی که ورودی مورد نظر ساخته نشود و محتوای واقعی خروجی مورد نظر را ندانیم، *متوقف* می‌ماند.
>
> با این حال، این مشکلی ندارد؛ زیرا تاخیر در انتساب آدرس‌های ورودی (که به یاد داشته باشید هدف نهایی `hashQuotientDerivation` همین است) تا زمانی که همه ورودی‌ها شناخته شوند، هیچ مشکلی ایجاد نمی‌کند.

### کارایی

بازگشت (recursion) در الگوریتم به‌طور بالقوه ناکارآمد است:
ممکن است به ازای هر مسیری که از طریق آن می‌توان به یک زیردرایویشن (subderivation) رسید، خودش را فراخوانی کند؛ یعنی برای یک گراف درایویشن با `V` درایویشن و درجه‌ی خروجی حداکثر `k`، به میزان `O(V^k)` بار فراخوانی شود.
در پیاده‌سازی واقعی، از [ذخیره‌سازی نتایج یا همان مموایزیشن (memoisation)](https://en.wikipedia.org/wiki/Memoization) استفاده می‌شود تا این هزینه متناسب با تعداد کل `inputDrvOutputs`های مواجه‌شده کاهش یابد.

### خصوصیات معنایی

*پیوست این فصل را درباره‌ی قراردادهای گرامر و متاوریاست‌ها (metavariables) در [@docroot@/store/math-notation.md ببینید](@docroot@/store/math-notation.md).*

در اصل، تابع `hashQuotientDerivation` درایویشن‌های مبتنی بر ورودی را به کلاس‌های هم‌ارزی تقسیم می‌کند: هر درایویشن در آن کلاس هم‌ارزی به همان هش درایویشن نگاشت می‌شود.
ما می‌توانیم این رابطه‌ی هم‌ارزی را مستقیماً و با کار کردن از پایین به بالا مشخص کنیم.

ما با تعریف یک رابطه‌ی هم‌ارزی روی مسیرهای اشتقاق خروجی مرتبه اول شروع می‌کنیم که به خروجی‌های درایویشن محتوا-محور (content-addressed) ارجاع می‌دهند. دو مسیر از این دست معادل هستند اگر به یک شیء انبار یکسان ارجاع دهند:

\\[
\\begin{prooftree}
\\AxiomC{$d\_1$ محتوا-محور (content-addressing) است}
\\AxiomC{$d\_2$ محتوا-محور (content-addressing) است}
\\AxiomC{$
  {}^\*(\text{path}(d\_1), o\_1)
  \=
  {}^\*(\text{path}(d\_2), o\_2)
$}
\\TrinaryInfC{$(\text{path}(d\_1), o\_1) \\,\\sim_{\\mathrm{CA}}\\, (d\_2, o\_2)$}
\\end{prooftree}
\\]

که در آن \\({}^*(s, o)\\) نشان‌دهنده‌ی شیء انباری است که مسیر اشتقاق خروجی به آن ارجاع می‌دهد.

ما همچنین به ساختار زیر نیاز خواهیم داشت تا هر رابطه‌ی هم‌ارزی روی \\(X\\) را به یک رابطه‌ی هم‌ارزی روی مجموعه‌های (متناهی) از \\(X\\) (به‌طور خلاصه، \\(\\mathcal{P}(X)\\)) ارتقا دهیم:

\\[
\\begin{prooftree}
\\AxiomC{$\\forall a \\in A. \\exists b \\in B. a \\,\\sim\_X\\, b$}
\\AxiomC{$\\forall b \\in B. \\exists a \\in A. b \\,\\sim\_X\\, a$}
\\BinaryInfC{$A \\,\\sim_{\\mathcal{P}(X)}\\, B$}
\\end{prooftree}
\\]

اکنون می‌توانیم رابطه‌ی هم‌ارزی \\(\\sim_\\mathrm{IA}\\) را روی خروجی‌های درایویشن مبتنی بر ورودی تعریف کنیم. دو خروجی مبتنی بر ورودی معادل هستند اگر درایویشن‌هایشان معادل باشند (از طریق رابطه‌ی هنوز تعریف‌نشده‌ی \\(\\sim_{\\mathrm{IADrv}}\\)) و نام‌های خروجی آن‌ها یکسان باشد:

\\[
\\begin{prooftree}
\\AxiomC{$d\_1$ مبتنی بر ورودی است}
\\AxiomC{$d\_2$ مبتنی بر ورودی است}
\\AxiomC{$d\_1 \\,\\sim_{\\mathrm{IADrv}}\\, d\_2$}
\\AxiomC{$o\_1 = o\_2$}
\\QuaternaryInfC{$(\text{path}(d\_1), o\_1) \\,\\sim_{\\mathrm{IA}}\\, (\text{path}(d\_2), o\_2)$}
\\end{prooftree}
\\]

و اکنون می‌توانیم \\(\\sim_{\\mathrm{IADrv}}\\) را تعریف کنیم.
دو درایویشن مبتنی بر ورودی معادل هستند اگر ورودی‌های محتوا-محور آن‌ها معادل باشند، ورودی‌های مبتنی بر ورودی آن‌ها نیز معادل باشند و در غیر این صورت برابر باشند:

<!-- cheating a bit with the semantics to get a good layout that fits on the page -->

\\[
\\begin{prooftree}
\\alwaysNoLine
\\AxiomC{$
  \\mathrm{caInputs}(d\_1)
  \\,\\sim_{\\mathcal{P}(\\mathrm{CA})}\\,
  \\mathrm{caInputs}(d\_2)
$}
\\AxiomC{$
  \\mathrm{iaInputs}(d\_1)
  \\,\\sim_{\\mathcal{P}(\\mathrm{IA})}\\,
  \\mathrm{iaInputs}(d\_2)
$}
\\BinaryInfC{$
  d\_1\left[\\mathrm{inputDrvOutputs} := \\{\\}\right]
  \=
  d\_2\left[\\mathrm{inputDrvOutputs} := \\{\\}\right]
$}
\\alwaysSingleLine
\\UnaryInfC{$d\_1 \\,\\sim_{\\mathrm{IADrv}}\\, d\_2$}
\\end{prooftree}
\\]

که در آن \\(\\mathrm{caInputs}(d)\\) ورودی‌های محتوا-محور \\(d\\) را برمی‌گرداند و \\(\\mathrm{iaInputs}(d)\\) ورودی‌های مبتنی بر ورودی را برمی‌گرداند.

> **نکته**
>
> یک خواننده زیرک ممکن است متوجه شود که `inputSrcs` در هیچ‌کدام از این تعاریف وارد نمی‌شود.
> این بدان معناست که جایگزین کردن یک درایویشن ورودی با خروجی‌های آن که مستقیماً به `inputSrcs` اضافه شده‌اند، همیشه منجر به یک درایویشن در کلاس هم‌ارزی متفاوتی می‌شود، علی‌رغم اینکه بستار ورودی حاصل (همان‌طور که در زمان ساخت در انبار مانت می‌شود) یکسان است.
> [موضوع شماره ۹۲۵۹](https://github.com/NixOS/nix/issues/9259) مربوط به ایجاد یک رابطه هم‌ارزی درشت‌تر برای حل این مسئله است.
>
> \\(\\sim_\mathrm{Drv}\\) از [رزولوشن درایویشن](@docroot@/store/resolution.md) چنین رابطه هم‌ارزشی است.
> این رابطه از این مورد درشت‌تر است: هر دو درایویشنی که با «درایویشن خارج‌قسمت هش» هم‌ارز هستند (\\(\\sim_\mathrm{IADrv}\\))، «هم‌ارز رزولوشن» نیز هستند (\\(\\sim_\mathrm{Drv}\\)).
> همچنین درایویشن‌هایی را که `inputDrvOutputs` آن‌ها به `inputSrcs` بازنویسی شده‌است، به یکدیگر مرتبط می‌کند.

[deriving-path]: @docroot@/store/derivation/index.md#deriving-path
[xp-feature-dynamic-derivations]: @docroot@/development/experimental-features.md#xp-feature-dynamic-derivations
[xp-feature-ca-derivations]: @docroot@/development/experimental-features.md#xp-feature-ca-derivations
