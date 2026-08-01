# Dotnet {#dotnet}

## گردش کار توسعه محلی {#local-development-workflow}

برای توسعه محلی، توصیه می‌شود از nix-shell برای ایجاد یک محیط dotnet استفاده کنید:

```nix
# shell.nix
with import <nixpkgs> { };

mkShell {
  name = "dotnet-env";
  packages = [ dotnet-sdk ];
}
```

### استفاده از چند SDK در یک گردش کار {#using-many-sdks-in-a-workflow}

بسیار محتمل است که در یک پروژه به بیش از یک SDK نیاز باشد. Dotnet چند چارچوب مختلف (مانند dotnetcore، aspnetcore و غیره) و همچنین نسخه‌های متعددی را برای یک چارچوب مشخص ارائه می‌دهد. به طور معمول، dotnet می‌تواند یک چارچوب را دریافت کرده و آن را نسبت به فایل اجرایی نصب کند. با این حال، این کار به معنای نوشتن در انبار نیکس (Nix store) در Nixpkgs خواهد بود که فقط‌خواندنی است. برای پشتیبانی از مورد استفاده چند SDK، می‌توان با استفاده از `dotnetCorePackages.combinePackages` یک محیط ایجاد کرد:

```nix
with import <nixpkgs> { };

mkShell {
  name = "dotnet-env";
  packages = [
    (
      with dotnetCorePackages;
      combinePackages [
        sdk_8_0
        sdk_9_0
      ]
    )
  ];
}
```

این کار یک نصب dotnet ایجاد خواهد کرد که دارای SDKهای dotnet 8.0 و 9.0 است. اولین SDK فهرست‌شده، ابزار رابط خط فرمان (CLI) خود را در محیط حاصل خواهد داشت. خروجی نمونه info:

```ShellSession
$ dotnet --info
.NET SDK:
 Version:           9.0.100
 Commit:            59db016f11
 Workload version:  9.0.100-manifests.3068a692
 MSBuild version:   17.12.7+5b8665660

Runtime Environment:
 OS Name:     nixos
 OS Version:  25.05
 OS Platform: Linux
 RID:         linux-x64
 Base Path:   /nix/store/a03c70i7x6rjdr6vikczsp5ck3v6rixh-dotnet-sdk-9.0.100/share/dotnet/sdk/9.0.100/

.NET workloads installed:
There are no installed workloads to display.
Configured to use loose manifests when installing new manifests.

Host:
  Version:      9.0.0
  Architecture: x64
  Commit:       9d5a6a9aa4

.NET SDKs installed:
  8.0.404 [/nix/store/6wlrjiy10wg766490dcmp6x64zb1vc8j-dotnet-core-combined/share/dotnet/sdk]
  9.0.100 [/nix/store/6wlrjiy10wg766490dcmp6x64zb1vc8j-dotnet-core-combined/share/dotnet/sdk]

.NET runtimes installed:
  Microsoft.AspNetCore.App 8.0.11 [/nix/store/6wlrjiy10wg766490dcmp6x64zb1vc8j-dotnet-core-combined/share/dotnet/shared/Microsoft.AspNetCore.App]
  Microsoft.AspNetCore.App 9.0.0 [/nix/store/6wlrjiy10wg766490dcmp6x64zb1vc8j-dotnet-core-combined/share/dotnet/shared/Microsoft.AspNetCore.App]
  Microsoft.NETCore.App 8.0.11 [/nix/store/6wlrjiy10wg766490dcmp6x64zb1vc8j-dotnet-core-combined/share/dotnet/shared/Microsoft.NETCore.App]
  Microsoft.NETCore.App 9.0.0 [/nix/store/6wlrjiy10wg766490dcmp6x64zb1vc8j-dotnet-core-combined/share/dotnet/shared/Microsoft.NETCore.App]

Other architectures found:
  None

Environment variables:
  Not set

global.json file:
  Not found

Learn more:
  https://aka.ms/dotnet/info

Download .NET:
  https://aka.ms/dotnet/download
```

## dotnet-sdk در برابر dotnetCorePackages.sdk {#dotnet-sdk-vs-dotnetcorepackages.sdk}

عبارت `dotnetCorePackages.sdk_X_Y` نسبت به `dotnet-sdk` قدیمی ترجیح داده می‌شود، زیرا هر دو نسخه اصلی (major) و فرعی (minor) برای یک محیط dotnet بسیار مهم هستند. اگر یک نسخه فرعی مشخص وجود نداشته باشد (یا تغییر کرده باشد)، به احتمال زیاد توانایی شما را برای ساخت یک پروژه مختل خواهد کرد.

## dotnetCorePackages.sdk در برابر dotnetCorePackages.runtime در برابر dotnetCorePackages.aspnetcore {#dotnetcorepackages.sdk-vs-dotnetcorepackages.runtime-vs-dotnetcorepackages.aspnetcore}

عبارت `dotnetCorePackages.sdk` شامل هر دو زمان اجرا (runtime) و sdk کامل از یک نسخه مشخص است. بسته‌های `runtime` و `aspnetcore` به منظور ارائه حداقل زمان اجرا جهت استقرار در کنار برنامه‌های ازقبل ساخته‌شده طراحی شده‌اند.

## بسته‌بندی یک برنامه Dotnet {#packaging-a-dotnet-application}

برای بسته‌بندی برنامه‌های Dotnet، می‌توانید از `buildDotnetModule` استفاده کنید. این تابع آرگومان‌های مشابهی با `stdenv.mkDerivation` دارد، همراه با موارد افزوده شده زیر:

* `projectFile` برای مشخص کردن فایل پروژه dotnet، نسبت به ریشه کد منبع استفاده می‌شود. این فایل‌ها دارای پسوند `.sln` (کل راهکار) یا `.csproj` (یک پروژه) هستند. این مورد می‌تواند لیستی از چندین پروژه نیز باشد. در صورت حذف، سعی خواهد شد راهکار (`.sln`) پیدا و ساخته شود. اگر با مشکل مواجه شدید، مطمئن شوید که آن را روی یک فایل (یا لیستی از فایل‌ها) با پسوند `.csproj` تنظیم کرده‌اید - ساخت برنامه‌ها به عنوان کل راهکار به طور کامل توسط CLI مربوط به .NET پشتیبانی نمی‌شود.
* `nugetDeps` باید یک مسیر به یک فایل JSON، یک مسیر به یک فایل nix (منسوخ‌شده)، یک درایویشن، یا لیستی از درایویشن‌ها باشد. یک فایل `deps.json` را می‌توان با استفاده از اسکریپت متصل به `passthru.fetch-deps` تولید کرد که روش ترجیحی است. تمام بسته‌های `nugetDeps` به `buildInputs` اضافه می‌شوند.
::: {.note}
برای جزییات بیشتر درباره مدیریت فایل `deps.json`، بخش [تولید و به‌روزرسانی وابستگی‌های NuGet](#generating-and-updating-nuget-dependencies) را ببینید.
:::

* `packNupkg` برای بسته‌بندی پروژه به عنوان یک `nupkg` استفاده می‌شود و آن را در `$out/share` نصب می‌کند. در صورت تنظیم روی `true`، درایویشن می‌تواند با افزودن به `buildInputs` به عنوان یک وابستگی برای پروژه dotnet دیگری استفاده شود.
* `buildInputs` می‌تواند برای حل موارد پروژه `ProjectReference` استفاده شود. پروژه‌های مورد ارجاع می‌توانند با `buildDotnetModule` با تنظیم صفت `packNupkg = true` و پاس دادن لیستی از درایویشن‌ها به `buildInputs` بسته‌بندی شوند. از آنجا که ما پروژه‌های مورد ارجاع را به عنوان NuGet به اشتراک می‌گذاریم، آن‌ها باید به فایل‌های csproj/fsproj به عنوان `PackageReference` نیز اضافه شوند.
 به عنوان مثال، پروژه شما یک وابستگی محلی دارد:
```xml
     <ProjectReference Include="../foo/bar.fsproj" />
 ```
برای فعال‌سازی شناسایی از طریق `buildInputs` باید موارد زیر را اضافه کنید:
```xml
     <ProjectReference Include="../foo/bar.fsproj" />
     <PackageReference Include="bar" Version="*" Condition=" '$(ContinuousIntegrationBuild)'=='true' "/>
  ```
* `executables` برای مشخص کردن این‌که کدام فایل‌های اجرایی نسبت به `$out/lib/$pname` در `$out/bin` قرار می‌گیرند (wrap می‌شوند) استفاده می‌شود. اگر این گزینه تنظیم نشود، تمام فایل‌های اجرایی تولیدشده نصب خواهند شد. اگر نمی‌خواهید هیچ‌کدام نصب شوند، آن را برابر `[]` قرار دهید. این کار در فاز `preFixup` انجام می‌شود.
* `runtimeDeps` برای قرار دادن کتابخانه‌ها در `LD_LIBRARY_PATH` استفاده می‌شود. این روشی است که dotnet معمولاً وابستگی‌های زمان اجرا را مدیریت می‌کند.
* `buildType` برای تغییر نوع ساخت استفاده می‌شود. مقادیر ممکن عبارتند از `Release`، `Debug` و غیره. به طور پیش‌فرض، این مقدار روی `Release` تنظیم شده است.
* `selfContainedBuild` امکان فعال‌سازی پرچم ساخت [self-contained](https://docs.microsoft.com/en-us/dotnet/core/deploying/#publish-self-contained) را فراهم می‌کند. به طور پیش‌فرض، روی false تنظیم شده است و برنامه‌های تولیدشده به زمان اجرای dotnet انتخاب‌شده وابستگی دارند. در صورت فعال شدن، زمان اجرای dotnet همراه با فایل اجرایی بسته‌بندی می‌شود و برنامه ساخته‌شده هیچ وابستگی به .NET ندارد.
* `useAppHost` ایجاد یک فایل اجرایی باینری را فعال می‌کند که برنامه .NET را با استفاده از ریشه مشخص‌شده اجرا می‌کند. اطلاعات بیشتر در [مستندات مایکروسافت](https://learn.microsoft.com/en-us/dotnet/core/deploying/#publish-framework-dependent). به طور پیش‌فرض فعال است.
* `useDotnetFromEnv` وراپر باینری را تغییر می‌دهد تا از .NET موجود در محیط استفاده کند. زمان اجرای مشخص‌شده توسط `dotnet-runtime` به عنوان حالت پشتیبان ارائه می‌شود تا در صورتی که هیچ .NETی در محیط کاربر نصب نشده باشد، استفاده شود. این گزینه بیشتر برای ابزارهای سراسری .NET و سرورهای LSP کاربرد دارد که اغلب CLI مربوط به .NET را گسترش می‌دهند و زمان اجرای آن‌ها باید با زمان اجرای .NET کاربر مطابقت داشته باشد.
* `dotnet-sdk` در مواردی مفید است که نیاز به تغییر SDK مورد استفاده dotnet دارید. همچنین اگر پروژه برای ساخت از چندین SDK استفاده می‌کند، می‌توانید این صفت را روی نتیجه `dotnetSdkPackages.combinePackages` تنظیم کنید.
* `dotnet-runtime` در مواردی مفید است که نیاز به تغییر زمان اجرای dotnet مورد استفاده دارید. این می‌تواند یک زمان اجرای معمولی dotnet یا aspnetcore باشد.
* `testProjectFile` در مواردی مفید است که فایل پروژه معمولی شامل تست‌های واحد نیست. این فایل بازیابی و ساخته می‌شود، اما نصب نمی‌گردد. ممکن است لازم باشد پس از تنظیم این صفت، فایل lockfile مربوط به nuget خود را دوباره تولید کنید. توجه داشته باشید که در صورت تنظیم، فقط تست‌های همین پروژه اجرا می‌شوند.
* `testFilters` برای غیرفعال کردن اجرای تست‌های واحد بر اساس [فیلترهای](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-test#filter-option-details) مختلف استفاده می‌شود. این مقدار به صورت `dotnet test --filter "{}"` ارسال می‌شود و هر فیلتر با استفاده از `"&"` الحاق می‌گردد.
* `disabledTests` برای غیرفعال کردن اجرای تست‌های واحد خاص استفاده می‌شود. این مقدار به صورت `dotnet test --filter "FullyQualifiedName!={}"` ارسال می‌شود تا از سازگاری با تمامی چارچوب‌های تست واحد اطمینان حاصل شود.
* `dotnetRestoreFlags` می‌تواند برای ارسال پرچم‌ها به `dotnet restore` استفاده شود.
* `dotnetBuildFlags` می‌تواند برای ارسال پرچم‌ها به `dotnet build` استفاده شود.
* `dotnetTestFlags` می‌تواند برای ارسال پرچم‌ها به `dotnet test` استفاده شود. تنها در صورتی استفاده می‌شود که `doCheck` روی `true` تنظیم شده باشد.
* `dotnetInstallFlags` می‌تواند برای ارسال پرچم‌ها به `dotnet install` استفاده شود.
* `dotnetPackFlags` می‌تواند برای ارسال پرچم‌ها به `dotnet pack` استفاده شود. تنها در صورتی استفاده می‌شود که `packNupkg` روی `true` تنظیم شده باشد.
* `dotnetFlags` می‌تواند برای ارسال پرچم‌ها به تمام فازهای بالا استفاده شود.

هنگام بسته‌بندی یک برنامه جدید، باید وابستگی‌های آن را دریافت کنید. یک `deps.json` خالی ایجاد کنید، `nugetDeps = ./deps.json` را تنظیم نمایید، سپس `nix-build -A package.fetch-deps` را اجرا کنید تا اسکریپتی تولید شود که lockfile را برای شما می‌سازد.

در ادامه یک نمونه `default.nix` آمده است که از برخی از آرگومان‌های بررسی‌شده در بالا استفاده می‌کند:
```nix
{
  lib,
  buildDotnetModule,
  dotnetCorePackages,
  ffmpeg,
}:

let
  referencedProject = import ../../bar {
    # ...
  };
in
buildDotnetModule rec {
  pname = "someDotnetApplication";
  version = "0.1";

  src = ./.;

  projectFile = "src/project.sln";
  nugetDeps = ./deps.json; # see "Generating and updating NuGet dependencies" section for details

  buildInputs = [
    referencedProject
  ]; # `referencedProject` must contain `nupkg` in the folder structure.

  dotnet-sdk = dotnetCorePackages.sdk_8_0;
  dotnet-runtime = dotnetCorePackages.runtime_8_0;

  executables = [ "foo" ]; # This wraps "$out/lib/$pname/foo" to `$out/bin/foo`.
  executables = [ ]; # Don't install any executables.

  packNupkg = true; # This packs the project as "foo-0.1.nupkg" at `$out/share`.

  runtimeDeps = [ ffmpeg ]; # This will wrap ffmpeg's library path into `LD_LIBRARY_PATH`.
}
```

به یاد داشته باشید که می‌توانید برای دریافت کمک و بررسی کد، تیم [`@NixOS/dotnet`](https://github.com/orgs/nixos/teams/dotnet) را تگ کنید.

## ابزارهای جهانی Dotnet {#dotnet-global-tools}

[ابزارهای جهانی .NET](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools) مکانیزمی ارائه‌شده توسط CLI مربوط به dotnet برای نصب باینری‌های .NET از بسته‌های Nuget هستند.

آن‌ها می‌توانند هم به عنوان یک ابزار جهانی برای کل سیستم، یا به عنوان یک ابزار محلی مخصوص به پروژه نصب شوند.

نصب محلی آسان‌ترین روش است و روی NixOS به همان روش سایر توزیع‌های Linux کار می‌کند.
برای اطلاعات بیشتر [مستندات dotnet را ببینید](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools#install-a-local-tool).

[روش نصب جهانی](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools#install-a-global-tool)
نیز بیشتر اوقات باید کار کند. باید به یاد داشته باشید که مقدار `PATH`
را به محلی که ابزارها در آن نصب شده‌اند به‌روزرسانی کنید (CLI در طول نصب این موضوع را به شما اطلاع می‌دهد) و همچنین
مقدار `DOTNET_ROOT` را تنظیم کنید تا ابزار بتواند بسته .NET SDK را پیدا کند.
می‌توانید با اجرای `nix eval --raw nixpkgs#dotnet-sdk` مسیر SDK را پیدا کنید (در صورت نیاز به نسخه متفاوتی از SDK، بسته `dotnet-sdk` را با بسته دیگری جایگزین کنید).

این روش در NixOS توصیه نمی‌شود، زیرا اعلانی (declarative) نیست و شامل نصب باینری‌هایی است که برای NixOS ساخته نشده‌اند،
که همیشه کار نخواهند کرد.

روش سوم و ترجیح داده شده، بسته‌بندی ابزار در یک derivation نیکس است.

### بسته‌بندی ابزارهای جهانی Dotnet {#packaging-dotnet-global-tools}

ابزارهای جهانی Dotnet باینری‌های استاندارد .NET هستند که فقط از طریق یک بسته ویژه
NuGet در دسترس قرار گرفته‌اند. بنابراین، آن‌ها مانند هر برنامه .NET دیگری می‌توانند
با استفاده از `buildDotnetModule` ساخته و بسته‌بندی شوند.

اگر با این حال کد منبع در دسترس نباشد یا ساخت آن دشوار باشد، می‌توان از
کمک‌رسان `buildDotnetGlobalTool` استفاده کرد که ابزار را
مستقیماً از بسته NuGet آن بسته‌بندی می‌کند.

این کمک‌رسان همان آرگومان‌های `buildDotnetModule` را دارد، با چند تفاوت:

* `pname` و `version` الزامی هستند و برای پیدا کردن بسته NuGet ابزار استفاده خواهند شد
* `nugetName` می‌تواند برای بازنشانی نام بسته NuGet که دانلود می‌شود (در صورتی که با `pname` متفاوت باشد) استفاده شود
* `nugetHash` هش بسته NuGet دریافت‌شده است. `nugetSha256` نیز پشتیبانی می‌شود، اما توصیه نمی‌شود. برای اولین ساخت، این مقدار را روی `lib.fakeHash` قرار دهید تا با خطا مواجه شده و هش مناسب را به شما بدهد. همچنین به یاد داشته باشید که در زمان ارتقای نسخه آن را به‌روزرسانی کنید (اگر فقط نسخه را تغییر دهید در حالی که بسته دریافت‌شده در `/nix/store` موجود باشد، خطایی رخ نخواهد داد)
* `dotnet-runtime` به طور پیش‌فرض روی `dotnet-sdk` تنظیم شده است. هنگام تغییر این مقدار، به یاد داشته باشید که ابزارهای .NET دریافت‌شده از NuGet به یک SDK نیاز دارند.

در ادامه یک نمونه از بسته‌بندی `pbm` (یک باینری غیرآزاد که کد منبع آن در دسترس نیست) آورده شده است:
```nix
{ buildDotnetGlobalTool, lib }:

buildDotnetGlobalTool {
  pname = "pbm";
  version = "1.3.1";

  nugetHash = "sha256-ZG2HFyKYhVNVYd2kRlkbAjZJq88OADe3yjxmLuxXDUo=";

  meta = {
    homepage = "https://cmd.petabridge.com/index.html";
    changelog = "https://cmd.petabridge.com/articles/RELEASE_NOTES.html";
    license = lib.licenses.unfree;
    platforms = lib.platforms.linux;
  };
}
```
## تولید و به‌روزرسانی وابستگی‌های NuGet {#generating-and-updating-nuget-dependencies}

هنگام نوشتن یک عبارت جدید، می‌توانید از اسکریپت تولیدشده‌ی `fetch-deps` برای مقداردهی اولیه lockfile استفاده کنید.
پس از تنظیم `nugetDeps` روی مسیر دلخواه lockfile (برای مثال `./deps.json`)،
اسکریپت را با `nix-build -A package.fetch-deps` بسازید و سپس نتیجه را اجرا کنید.
(وقتی صفت ریشه، بسته شما باشد، این دستور به‌سادگی `nix-build -A fetch-deps` است.)

یک روش دستی نیز وجود دارد:
نخست، بسته‌ها را در پوشه `out` بازیابی کنید، مطمئن شوید که مخزن بالادستی را کلون کرده‌اید و داخل آن هستید.

```bash
$ dotnet restore --packages out
  Determining projects to restore...
  Restored /home/ggg/git-credential-manager/src/shared/Git-Credential-Manager/Git-Credential-Manager.csproj (in 1.21 sec).
```

در ادامه، از ابزار `nuget-to-json` ارائه‌شده در Nixpkgs برای تولید لاک‌فایل در `deps.json` از بسته‌های داخل پوشه‌ی `out` استفاده کنید.

```bash
$ nuget-to-json out > deps.json
```
ابزار `nuget-to-json` خروجی مشابه نمونه زیر تولید خواهد کرد.
```json
[
  {
    "pname": "Avalonia",
    "version": "11.1.3",
    "hash": "sha256-kz+k/vkuWoL0XBvRT8SadMOmmRCFk9W/J4k/IM6oYX0="
  },
  {
    "pname": "Avalonia.Angle.Windows.Natives",
    "version": "2.1.22045.20230930",
    "hash": "sha256-RxPcWUT3b/+R3Tu5E5ftpr5ppCLZrhm+OTsi0SwW3pc="
  },
  {
    "pname": "Avalonia.BuildServices",
    "version": "0.0.29",
    "hash": "sha256-WPHRMNowRnYSCh88DWNBCltWsLPyOfzXGzBqLYE7tRY="
  },
  // ...
  {
    "pname": "System.Runtime.CompilerServices.Unsafe",
    "version": "6.0.0",
    "hash": "sha256-bEG1PnDp7uKYz/OgLOWs3RWwQSVYm+AnPwVmAmcgp2I="
  },
  {
    "pname": "System.Security.Cryptography.ProtectedData",
    "version": "4.5.0",
    "hash": "sha256-Z+X1Z2lErLL7Ynt2jFszku6/IgrngO3V1bSfZTBiFIc="
  },
  {
    "pname": "Tmds.DBus.Protocol",
    "version": "0.16.0",
    "hash": "sha256-vKYEaa1EszR7alHj48R8G3uYArhI+zh2ZgiBv955E98="
  }
]

```

در نهایت، فایل `deps.json` را به مکان مناسب منتقل می‌کنید تا توسط `nugetDeps` استفاده شود، و کار تمام است!

اگر زمانی نیاز به به‌روزرسانی وابستگی‌های یک بسته داشته باشید، در عوض این کارها را انجام می‌دهید:

* اجرای `nix-build -A package.fetch-deps` برای تولید اسکریپت به‌روزرسانی برای `package`
* اجرای `./result` برای تولید مجدد فایل قفل در مسیری که به `nugetDeps` داده شده است (در نظر داشته باشید اگر نتوان آن را به یک مسیر محلی ارزیابی کرد، اسکریپت در عوض در `$1` یا یک مسیر موقت خواهد نوشت)
* در نهایت، اطمینان حاصل کنید که فایل درست نوشته شده است و derivation قابل ساخت است.
