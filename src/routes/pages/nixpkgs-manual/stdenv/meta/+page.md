# <a id="chap-meta"></a> صفات متاداده

بسته‌های Nix می‌توانند *صفات متاداده* را اظهار کنند که حاوی اطلاعاتی درباره یک بسته مانند توضیحات، صفحه خانگی،

```nix
{
  meta = {
    description = "Program that produces a familiar, friendly greeting";
    longDescription = ''
      GNU Hello is a program that prints "Hello, world!" when you run it.
      It is fully customizable.
    '';
    homepage = "https://www.gnu.org/software/hello/manual/";
    license = lib.licenses.gpl3Plus;
    maintainers = with lib.maintainers; [ eelco ];
    platforms = lib.platforms.all;
  };
}
```

متا-صفت‌ها به سازنده (Builder) بسته ارسال نمی‌شوند. بنابراین، تغییر در یک متا-صفت باعث کامپایل مجدد بسته نمی‌شود.

## <a id="sec-standard-meta-attributes"></a> متا-صفت‌های استاندارد

اگر قرار است بسته به Nixpkgs ارسال شود، لطفاً [الزامات مربوط به متا-صفت‌ها](https://github.com/NixOS/nixpkgs/tree/master/pk

اجرا می‌کند تاثیر می‌گذارد. مثال: `"rg"`

### <a id="var-meta-priority"></a> `priority`

"The *priority* of the package, used by `nix-env` to resolve file name conflicts between packages. See the [manual page for `nix-env`](https://n

```nix
{ meta.platforms = lib.platforms.linux; }
```

مجموعه ویژگی `lib.platforms` [فهرست‌های متداول گوناگونی](https://github.com/NixOS/nixpkgs/blob/master/lib/systems/doubles.

```nix
{
  meta.platforms = lib.platforms.all;
  meta.badPlatforms = [ lib.systems.inspect.platformPatterns.isStatic ];
}
```

فهرست انواع پلتفرم‌های Nix که [نمونه‌ی Hydra](https://github.com/nixos/hydra) [در `hydra.nixos.org`](https://nixos.org/hydra) بسته را برای آن‌ها خواهد ساخت. (Hydra سیستم ساخت مداوم مبتنی بر Nix است.) مقدار پیش‌فرض آن

```nix
{
  meta.platforms = lib.platforms.linux;
  meta.hydraPlatforms = [ ];
}
```

توجه داشته باشید که این موضوع بر ساخته شدن یا نشدن وابستگی‌های معکوس بسته در Hydra تأثیری ندارد.

### <a id="var-meta-broken"></a> `broken`

اگر

```nix
  { meta.broken = !(stdenv.buildPlatform.canExecute stdenv.hostPlatform); }
  ```

- معیوب است در صورتی که تمامی وابستگی‌های مجموعهٔ مشخصی از آن معیوب باشند

```nix
  {
    meta.broken = lib.all (
      map (p: p.meta.broken) [
        glibc
        musl
      ]
    );
  }
  ```

این امر باعث می‌شود `broken` کاملاً قدرتمندتر از `meta.badPlatforms` باشد.
با این حال، `meta.availableOn` در حال حاضر فقط `meta.platforms` و `meta.badPlatforms` را بررسی می‌کند، بنابراین `meta.broken` تاثیری بر مقادیر پیش‌فرض وابستگی‌های اختیاری ندارد.

در زیر، `;meta.broken = true` با عبارت زیر برابر است:

```nix
{
  meta.problems.broken.message = "This package is broken.";
}
```

با تعیین دستی این مورد، می‌توان پیام خطا را سفارشی‌سازی کرد.

## <a id="var-meta-knownVulnerabilities"></a> `knownVulnerabilities`

فهرستی از آسیب‌پذیری‌های شناخته‌شده که بسته را تحت تأثیر قرار می‌دهند، که معمولاً با شناساگرهای CVE مشخص می‌شوند.

این متاداده به کاربران و ابزارها اجازه می‌دهد تا پیش از استفاده از بسته، از مشکلات امنیتی حل‌نشده مطلع شوند، برای مثال:

```nix
{
  meta.knownVulnerabilities = [
    "CVE-2024-3094: Malicious backdoor allowing unauthorized remote code execution"
  ];
}
```

اگر این لیست خالی نباشد، بسته به عنوان "ناامن" علامت‌گذاری می‌شود، به این معنی که قابل ساخت یا نصب نخواهد بود مگر اینکه متغیر محیطی [`NIXPKGS_ALLOW_INSECURE`](#sec-allow-insecure) تنظیم شده باشد.

## <a id="sec-meta-license"></a> مجوزها

صفت (attribute) `meta.license` ترجیحاً باید حاوی مقداری از `lib.licenses` تعریف‌شده در [`n`

### <a id="lib.sourceTypes.binaryNativeCode"></a> `lib.sourceTypes.binaryNativeCode`

کد بومی ساخته‌شده توسط شخص ثالث که باید روی پردازنده سیستم هدف اجرا شود. این شامل بسته‌هایی می‌شود که یک AppImage یا بسته Debian بارگیری‌شده را در بر می‌گیرند.

### <a id="lib.sourceTypes.binaryFirmware"></a> `lib.sourceTypes.binaryFirmware`

کدی که باید روی یک دستگاه جانبی یا کنترل‌کننده نهفته اجرا شود و توسط شخص ثالث ساخته شده است.

### <a id="lib.sourceTypes.binaryBytecode"></a> `lib.sourceTypes.binaryBytecode`

کدی که روی یک مفسر ماشین مجازی (VM) اجرا می‌شود یا توسط شخص ثالث به صورت JIT به بایت‌کد کامپایل شده است. این شامل بسته‌هایی می‌شود که فایل‌های `.jar` جاوا را از منبع دیگری بارگیری می‌کنند.

### <a id="lib.sourceTypes.obfuscatedCode"></a> `lib.sourceTypes.obfuscatedCode`

کدی که به عمد توسط شخص ثالث مبهم‌سازی شده است، به عنوان مثال با استفاده از یک مبهم‌ساز کد یا توزیع شدن به صورت مبهم‌سازی‌شده.

## <a id="sec-meta-identifiers"></a> شناسه‌های نرم‌افزار

صفت `meta.identifiers` بسته، اطلاعات مربوط به شناسه‌های نرم‌افزاری مرتبط با این بسته را مشخص می‌کند. شناسه‌های نرم‌افزاری به عنوان مثال برای موارد زیر استفاده می‌شوند:
* برای تولید صورت‌حساب مواد نرم‌افزاری (SBOM) که تمامی کامپوننت‌های استفاده‌شده برای ساخت نرم‌افزار را فهرست می‌کند، که بعداً می‌توان از آن برای انجام تحلیل آسیب‌پذیری یا مجوز نرم‌افزار حاصل استفاده کرد؛
* برای جستجوی نرم‌افزار در پایگاه‌های داده آسیب‌پذیری مختلف یا گزارش آسیب‌پذیری‌های جدید به آن‌ها.

بازنشانی صفت `meta.identifiers` پیش‌فرض اختیاری است، اما توصیه می‌شود بخش‌های آن را پر کنید تا به ابزارهای ذکرشده در بالا برای دریافت داده‌های دقیق کمک شود.
به عنوان مثال، می‌توانیم در آینده اعلان‌های

```
cpe:2.3:a:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>
```

برخی از آن‌ها به شرح زیر است:

* *نسخه CPE* - نسخه فعلی CPE برابر با `2.3` است
* *part* - معمولاً در Nixpkgs مقدار `a` برای "برنامه"، همچنین می‌تواند `o` برای "سیستم‌عامل" یا `h` برای "سخت‌افزار" باشد
*

```nix
{
  # ...
  meta.identifiers.cpeParts = lib.meta.cpeFullVersionWithVendor vendor version;
}
```

#### <a id="var-meta-identifiers-cpe"></a> `meta.identifiers.cpe`

یک صفت (attribute) فقط‌خواندنی که تمام بخش‌های CPE را در یک رشته الحاق می‌کند.

#### <a id="var-meta-identifiers-possibleCPEs"></a> `meta.identifiers.possibleCPEs`

یک صفت (attribute) فقط‌خواندنی شامل فهرستی از حدس‌ها درباره این‌که CPE برای این بسته چگونه می‌تواند باشد. این صفت شامل تمامی گونه‌های مدیریت نسخه اشاره‌شده در بالا است. هر عنصر یک attrset با صفات `cpeParts` و ``
