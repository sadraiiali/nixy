# <a id="chap-interop-cyclonedx"></a> CycloneDX

[OWASP](https://owasp.org/) [CycloneDX](https://cyclonedx.org/) یک استاندارد [صورت مواد تشکیل‌دهنده نرم‌افزار](https://en.wikipedia.org/wiki/Bill_of_materials) (SBOM) است.
استانداردهای توصیف‌شده در این‌جا برای گنجاندن اطلاعات مختص Nix درون SBOMها به گونه‌ای است که با ابزارهای SBOM خارجی تعامل‌پذیر باشد.

## <a id="sec-interop.cylonedx-nix"></a> طبقه‌بندی ویژگی‌های فضای نام `nix`

جداول زیر فضاهای نام را برای [ویژگی‌ها](https://cyclonedx.org/docs/1.6/json/#components_items_properties) که می‌توانند به کامپوننت‌ها درون SBOMها ضمیمه شوند، توصیف می‌کنند.
ویژگی‌های کامپوننت، فهرست‌هایی از جفت‌های نام-مقدار هستند که مقادیر آن‌ها باید رشته باشند.
ویژگی‌های با نام یکسان ممکن است بیش از یک بار ظاهر شوند.
نام‌ها و مقادیر به حروف کوچک و بزرگ حساس هستند.

| ویژگی | توضیحات |
|---|---|
| `nix:store_path` | یک مسیر انبار Nix برای کامپوننت داده‌شده. این ویژگی باید با ویژگی‌های اضافی که تولید مسیر انبار را توصیف می‌کنند، مانند ویژگی‌های فضاهای نام `nix:narinfo:` و `nix:fod` بسترسازی و مکمل شود. |

| فضای نام | توضیحات |
|---|---|
| [`nix:narinfo`](#sec-interop.cylonedx-narinfo) | فضای نام برای ویژگی‌هایی که مختص نحوه ذخیره‌سازی یک کامپوننت به عنوان یک [آرشیو Nix](https://nixos.org/manual/nix/stable/glossary#gloss-nar) (NAR) در یک [کش باینری](https://nixos.org/manual/nix/stable/glossary#gloss-binary-cache) هستند. |
| [`nix:fod`](#sec-interop.cylonedx-fod) | فضای نام برای ویژگی‌هایی که یک [derivation / اشتقاق ساخت با خروجی ثابت](https://nixos.org/manual/nix/stable/glossary#gloss-fixed-output-derivation) را توصیف می‌کنند. |

### <a id="sec-interop.cylonedx-narinfo"></a> `nix:narinfo`

ویژگی‌های Narinfo آرشیوهای کامپوننتی را توصیف می‌کنند که ممکن است از کش‌های باینری در دسترس باشند.
ویژگی‌های `nix:narinfo` باید همراه با یک ویژگی `nix:store_path` درون همان فهرست ویژگی ارائه شوند.

| ویژگی | توضیحات |
|---|---|
| `nix:narinfo:store_path` | مسیر انبار برای کامپوننت انبار داده‌شده. |
| `nix:narinfo:url` | بخش مسیر URL. |
| `nix:narinfo:nar_hash` | هش بخش شیء سیستم‌فایل کامپوننت هنگام سریال‌سازی به عنوان یک آرشیو Nix. |
| `nix:narinfo:nar_size` | اندازه کامپوننت هنگام سریال‌سازی به عنوان یک آرشیو Nix. |
| `nix:narinfo:compression` | قالب فشرده‌سازی که آرشیو کامپوننت در آن قرار دارد. |
| `nix:narinfo:file_hash` | یک خلاصه (digest) برای خودِ آرشیو فشرده‌شده کامپوننت، برعکس داده‌های درون آن. |
| `nix:narinfo:file_size` | اندازه خودِ آرشیو فشرده‌شده کامپوننت. |
| `nix:narinfo:deriver` | مسیر به derivation / اشتقاق ساخت که این کامپوننت از آن تولید شده است. |
| `nix:narinfo:system` | پلتفرم سخت‌افزاری و نرم‌افزاری که این کامپوننت روی آن تولید شده است. |
| `nix:narinfo:sig` | امضاها که ادعا می‌کنند این کامپوننت همان چیزی است که ادعا می‌کند. |
| `nix:narinfo:ca` | آدرس محتوایی (Content address) شیء سیستم‌فایل این شیء انبار، که برای محاسبه مسیر انبار آن استفاده می‌شود. |
| `nix:narinfo:references` | آرایه‌ای جداشده با فاصله از مسیرهای انبار که این کامپوننت به آن‌ها ارجاع می‌دهد. |

### <a id="sec-interop.cylonedx-fod"></a> `nix:fod`

ویژگی‌های FOD یک [fixed-output derivation](https://nixos.org/manual/nix/stable/glossary#gloss-fixed-output-derivation) را توصیف می‌کنند.
ویژگی `nix:fod:method` الزامی است و باید همراه با یک ویژگی `nix:store_path` در همان فهرست ویژگی‌ها قرار گیرد.
تمام ویژگی‌های دیگر در این فضای نام، مختص همان متد هستند.
برای بازتولید ساخت یک کامپوننت، مقدار `nix:fod:method` به یک [تابع مناسب](#chap-pkgs-fetchers) در Nixpkgs نگاشته می‌شود که آرگومان‌های آن با ویژگی‌های داده‌شده اشتراک دارند.
هنگام تولید ویژگی‌های `nix:fod`، متد انتخاب‌شده باید یک تابع پایدار با حداقل تعداد آرگومان‌ها باشد.
به عنوان مثال، `fetchFromGitHub` معمولاً در Nixpkgs استفاده می‌شود اما باید به فراخوانی تابعی که توسط آن پیاده‌سازی شده است، یعنی `fetchzip` کاهش یابد.

| ویژگی | توضیحات |
|------------------|-------------|
| `nix:fod:method` | تابع Nixpkgs که این FOD را تولید می‌کند. الزامی. نمونه‌ها: `"fetchzip"`، `"fetchgit"` |
| `nix:fod:name` | نام derivation، در صورت استفاده از متد `"fetchzip"` موجود است |
| `nix:fod:ref` | [Git ref](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefrefaref)، در صورت استفاده از متد `"fetchgit"` موجود است |
| `nix:fod:rev` | [Git rev](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefrevisionarevision)، در صورت استفاده از متد `"fetchgit"` موجود است |
| `nix:fod:sha256` | هش FOD |
| `nix:fod:url` | آدرس URL برای دریافت |

ویژگی‌های `nix:fod` ممکن است استخراج شده و با فرض وجود یک تابع ساختگی `filterPropertiesToAttrs` با استفاده از کدی مشابه زیر، به یک derivation ارزیابی شوند:

```nix
{
  pkgs,
  filterPropertiesToAttrs,
  properties,
}:
let
  fodProps = filterPropertiesToAttrs "nix:fod:" properties;

  methods = {
    fetchzip =
      {
        name,
        url,
        sha256,
        ...
      }:
      pkgs.fetchzip { inherit name url sha256; };
  };

in
methods.${fodProps.method} fodProps
```
