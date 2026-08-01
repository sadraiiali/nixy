# <a id="language-javascript"></a> Javascript

## <a id="javascript-introduction"></a> مقدمه

این بخش شامل دستورالعمل‌هایی درباره نحوه بسته‌بندی برنامه‌های JavaScript است.

ابزارهای مختلف موجود در [tools-overview](#javascript-tools-overview) فهرست خواهند شد.
سپس برخی از اصول عمومی برای بسته‌بندی ارائه می‌شود.
در نهایت، دستورالعمل‌های خاص هر ابزار داده خواهد شد.

## <a id="javascript-finding-examples"></a> برطرف کردن بن‌بست / یافتن نمونه‌های کد

اگر احساس می‌کنید برای بسته‌بندی برنامه‌های JavaScript ایده یا الهام کافی ندارید، لینک‌های زیر ممکن است مفید واقع شوند.
جستجوی آنلاین برای کارهای قبلاً انجام‌شده می‌تواند در صورت مواجهه با مشکلاتی که پیش‌تر حل شده‌اند، مفید باشد.

### Github {'{'}'{'{'}'{'}'}#javascript-

- گاهی اوقات مخزن بالادستی فرض می‌کند که برخی وابستگی‌ها باید به صورت سراسری نصب شوند. در این حالت، می‌توانید آن‌ها را به صورت دستی به `package.json` بالادستی اضافه کنید (`yarn add`
```sh
  yarn build:ui
  yarn build:server
  # OR
  npm run build:ui
  npm run build:server
  ```

های صریح روی آن ایده خوبی است. در ادامه یک مثال آورده شده است:

    Let's check spacing and sentence structure:

```nix
  {
    patchedPackageJSON = final.runCommand "package.json" { } ''
      ${jq}/bin/jq '.version = "0.4.0" |
        .devDependencies."@jsdoc/cli" = "^0.2.5"
        ${sonar-src}/package.json > $out
    '';
  }
  ```

همچنان لازم است نسخه تغییریافته فایل‌های قفل (lock files) را کامیت کنید، اما حداقل بازنشانی‌ها به‌طور صریح برای همگان قابل مشاهده است.

### <a id="javascript-using-node_modules"></a> استفاده مستقیم از node_modules

```nix
{
  lib,
  buildNpmPackage,
  fetchFromGitHub,
}:

buildNpmPackage (finalAttrs: {
  pname = "flood";
  version = "4.7.0";

  src = fetchFromGitHub {
    owner = "jesec";
    repo = "flood";
    tag = "v${finalAttrs.version}";
    hash = "sha256-BR+ZGkBBfd0dSQqAvujsbgsEPFYw/ThrylxUbOksYxM=";
  };

  npmDepsHash = "sha256-tuEfyePwlOy2/mOPdXbqJskO6IowvAP4DWg8xSZwbJw=";

  # The prepack script runs the build script, which we'd rather do in the build phase.
  npmPackFlags = [ "--ignore-scripts" ];

  NODE_OPTIONS = "--openssl-legacy-provider";

  meta = {
    description = "Modern web UI for various torrent clients with a Node.js backend and React frontend";
    homepage = "https://flood.js.org";
    license = lib.licenses.gpl3Only;
    maintainers = with lib.maintainers; [ winter ];
  };
})
```

در فاز نصب (installPhase) پیش‌فرض که توسط `buildNpmPackage` تنظیم می‌شود، از `npm pack --json --dry-run` برای تصمیم‌گیری درباره فایل‌های قابل نصب در `$out/lib/node_modules/$name/` استفاده می‌شود، که در آن `$name` همان رشته `name` تعریف‌شده در `package.json` متعلق به بسته است.
علاوه بر این، کلیدهای `bin` و `man` در `package.json` کد منبع برای تصمیم‌گیری در مورد این‌که چه باینری‌ها و صفحات راهنمایی (manpages) باید نصب شوند، استفاده می‌شوند.
اگر این موارد تعریف نشده باشند، ممکن است `npm pack` برخی از فایل‌ها را ندیده بگیرد و هیچ باینری تولید نشود.

#### <a id="javascript-buildNpmPackage-arguments"></a> آرگومان‌ها

* `npmDepsHash`: هش خروجی وابستگی‌ها برای این پروژه. می‌تواند از قبل با [`prefetch-npm-deps`](#javascript-buildNpmPackage-prefetch-npm-deps) محاسبه شود.
* `makeCacheWritable`: آیا کش پیش از نصب

```shell
$ ls
package.json package-lock.json index.js
$ prefetch-npm-deps package-lock.json
...
sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
```

#### <a id="javascript-buildNpmPackage-fetchNpmDeps"></a> fetchNpmDeps

`fetchNpmDeps` یک تابع Nix است که به آرگومان‌های اجباری زیر نیاز دارد:

- `src`: یک پوشه / تاربال دارای فایل `package-lock.json`
- `hash`: هش خروجی وابستگی‌های node تعریف‌شده در `package-lock.json`.

این تابع یک derivation / اشتقاق ساخت را برمی‌گرداند که تمام وابستگی‌های `package-lock.json` در `$out/` آن بارگیری شده‌اند و به عنوان کش npm قابل استفاده است.

#### <a id="javascript-buildNpmPackage-importNpmLock"></a> importNpmLock

این تابع ارجاعات وابستگی npm را در `package.json` و `package-lock.json` با مسیرهایی به انبار نیکس (Nix store) جایگزین می‌کند.
نحوه دریافت هر وابستگی را می‌توان با آرگومان `fetcherOpts` سفارشی‌سازی کرد.

این روش جایگزینی ساده‌تر و راحت‌تر برای [`fetchNpmDeps`](#javascript-buildNpmPackage-fetchNpmDeps) جهت مدیریت وابستگی‌های npm در Nixpkgs است.
نیازی به تعیین یک `hash` نیست، زیرا کاملاً به هش‌های یکپارچگی موجود در فایل `package-lock.json` متکی است.

##### ورودی‌ها {'{'}'{'{'}'{'}'}#javascript-build

```nix
{ buildNpmPackage, importNpmLock }:

buildNpmPackage {
  pname = "hello";
  version = "0.1.0";
  src = ./.;

  npmDeps = importNpmLock { npmRoot = ./.; };

  npmConfigHook = importNpmLock.npmConfigHook;
}
```

> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> ##### <a id="javascript-buildNpmPackage-example-fetcherOpts"></a> نمونه استفاده از `pkgs.importNpmLock` همراه با `fetcherOpts`
>
> `importNpmLock` از دریافت‌کننده‌های زیر استفاده می‌کند:
>
> - `pkgs.fetchurl` برای وابستگی‌های `http(s)`
> - `fetchGit` برای وابستگی‌های `git`
>
> در صورت نیاز، امکان ارائه آرگومان‌های اضافی به دریافت‌کننده‌های فردی وجود دارد:
>

> ```nix
> { buildNpmPackage, importNpmLock }:
>
> buildNpmPackage {
>   pname = "hello";
>   version = "0.1.0";
>   src = ./.;
>
>   npmDeps = importNpmLock {
>     npmRoot = ./.;
>     fetcherOpts = {
>       # Pass 'curlOptsList' to 'pkgs.fetchurl' while fetching 'axios'
>       "node_modules/axios" = {
>         curlOptsList = [ "--verbose" ];
>       };
>     };
>   };
>
>   npmConfigHook = importNpmLock.npmConfigHook;
> }
> ```

#### <a id="javascript-buildNpmPackage-importNpmLock.buildNodeModules"></a> importNpmLock.buildNodeModules

تابع `importNpmLock.buildNodeModules` یک درایویشن شامل یک پوشه `node_modules` پیش‌

```nix
pkgs.mkShell {
  packages = [
    importNpmLock.hooks.linkNodeModulesHook
    nodejs
  ];

  npmDeps = importNpmLock.buildNodeModules {
    npmRoot = ./.;
    inherit nodejs;
  };
}
```
، یک پوشه `node_modules` ساخته شده و بسته‌ها به انبار نیکس (Nix store) پیوند نمادین (symlink) داده می‌شوند.

> <span class="admonition-kind" data-kind="note"></span>
>
> **نکته**
>
> دستوراتی مانند `npm install` و `npm add` که بسته‌ها و فایل‌های اجر
>

> ```nix
> {
>   fetchPnpmDeps,
>   nodejs,
>   pnpm_11,
>   pnpmConfigHook,
>   stdenv,
> }:
> let
>   # It is recommended to pin pnpm to a major version, due to regular breaking changes in the store format
>   # The latest major version is always available under `pkgs.pnpm`
>   # Optionally override pnpm to use a custom nodejs version
>   # Make sure that the same nodejs version is referenced in nativeBuildInputs
>   # pnpm = pnpm_11.override { nodejs = nodejs_24; };
>   pnpm = pnpm_11;
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "foo";
>   version = "0-unstable-1980-01-01";
>
>   src = {
>     #...
>   };
>
>   nativeBuildInputs = [
>     nodejs # in case scripts are run outside of a pnpm call
>     pnpmConfigHook
>     pnpm # At least required by pnpmConfigHook, if not other (custom) phases
>   ];
>
>   pnpmDeps = fetchPnpmDeps {
>     inherit (finalAttrs) pname version src;
>     inherit pnpm;
>     fetcherVersion = 4;
>     hash = "...";
>   };
> })
> ```
>
> شدیداً توصیه می‌شود برای افزایش بازتولیدپذیری در آینده، از یک نسخه ثابت‌شده از pnpm (یعنی `pnpm_9` یا `pnpm_10`) استفاده کنید
>

> ```diff
>  {
>    fetchPnpmDeps,
>    nodejs,
> -  pnpm,
> +  pnpm_10,
>    pnpmConfigHook,
>    stdenv,
>  }:
> +let
> +  # Optionally override pnpm to use a custom nodejs version
> +  # Make sure that the same nodejs version is referenced in nativeBuildInputs
> +  # pnpm = pnpm_10.override { nodejs-slim = nodejs-slim_22; };
> +in
>  stdenv.mkDerivation (finalAttrs: {
>    pname = "foo";
>    version = "0-unstable-1980-01-01";
>
>    src = {
>      #...
>    };
>
>    nativeBuildInputs = [
>      nodejs # in case scripts are run outside of a pnpm call
>      pnpmConfigHook
> -    pnpm # At least required by pnpmConfigHook, if not other (custom) phases
> +    pnpm_10 # At least required by pnpmConfigHook, if not other (custom) phases
>    ];
>
>    pnpmDeps = fetchPnpmDeps {
>      inherit (finalAttrs) pname version src;
> +    pnpm = pnpm_10;
>      fetcherVersion = 4;
>      hash = "...";
>    };
>  })
> ```
>
> در صورتی که در حال پچ کردن `package.json` یا `pnpm-lock.yaml` هستید، حتماً `finalAttrs.patches`
>

> ```nix
> {
>   # ...
>   pnpmDeps = fetchPnpmDeps {
>     # ...
>     inherit (finalAttrs) pnpmInstallFlags;
>   };
>
>   pnpmInstallFlags = [ "--shamefully-hoist" ];
> }
> ```
>
> در صورت نیاز، می‌توان از `dontPnpmConfigure = true;` برای غیرفعال‌سازی کامل `pnpmConfigHook` بدون حذف دستی آن از ورودی‌ها استفاده کرد.
>
> ```
> .
> ├── frontend
> │   ├── ...
> │   ├── package.json
> │   └── pnpm-lock.yaml
> └── ...
> ```
>

> ```nix
> {
>   # ...
>   pnpmDeps = fetchPnpmDeps {
>     # ...
>     sourceRoot = "${finalAttrs.src.name}/frontend";
>   };
>
>   # by default the working directory is the extracted source
>   pnpmRoot = "frontend";
> }
> ```
>
> #### <a id="javascript-pnpm-workspaces"></a> فضاهای کاری PNPM
>
> اگر برای پروژه خود نیاز به استفاده از یک فضای کاری PNPM دارید، مقدار `pnpmWorkspaces = [ "&lt;workspace project name 1&gt;" "&lt;workspace project name 2&gt;" ]` و غیره را در فراخوانی `fetchPnpmDeps` خود تنظیم کنید، که باعث می‌شود PNPM فقط وابستگی‌ها را برای همان بسته‌های فضای کاری نصب کند.
>
> برای مثال:
>

> ```nix
> {
>   # ...
>   pnpmWorkspaces = [ "@astrojs/language-server" ];
>   pnpmDeps = fetchPnpmDeps {
>     #...
>     inherit (finalAttrs) pnpmWorkspaces;
>   };
> }
> ```
>
> ` کار نخواهد کرد. یک `buildPhase` بر اساس نمونه زیر احتمالاً برای اکثر پروژه‌های فضای کاری مناسب خواهد بود:`
>
> Wait, check `npmHooks.npmBuildHook`
>

> ```nix
> {
>   buildPhase = ''
>     runHook preBuild
>
>     pnpm --filter=@astrojs/language-server build
>
>     runHook postBuild
>   '';
> }
> ```
>
> #### <a id="javascript-pnpm-extraCommands"></a> دستورات و تنظیمات اضافی PNPM
>
> اگر به اعمال یک گزینه پیکربندی اضافی PNPM (مانند `dedupe-peer-dependents` یا موارد مشابه) نیاز دارید، `prePnpmInstall` را روی دستورات مناسب جهت اجرا تنظیم کنید. برای مثال:
>

> ```nix
> {
>   prePnpmInstall = ''
>     pnpm config set dedupe-peer-dependents false
>   '';
>   pnpmDeps = fetchPnpmDeps {
>     inherit (finalAttrs) prePnpmInstall;
>     # ...
>   };
> }
> ```
>
> در این مثال، `prePnpmInstall` هم توسط `pnpmConfigHook` و هم توسط سازنده `fetchPnpmDeps` اجرا خواهد شد.
>
> #### <a id="javascript-pnpm-fetcherVersion"></a> pnpm `fetcherVersion`
>
> این نسخهٔ خروجی `fetchPnpmDeps` است. بسته‌های جدید باید از `4` استفاده کنند:
>

> ```nix
> {
>   # ...
>   pnpmDeps = fetchPnpmDeps {
>     # ...
>     fetcherVersion = 4;
>     hash = "..."; # clear this hash and generate a new one
>   };
> }
> ```
>
> هنگام ارتقا به یک `fetcherVersion` جدیدتر، باید هش را دوباره تولید کنید.
>
> این متغیر تضمین می‌کند که می‌توانیم تغییراتی در خروجی `fetchPnpmDeps` ایجاد کنیم بدون اینکه هش‌های موجود شکسته شوند.
> تغییرات می‌توانند شامل راهکارهای مو
>

> ```nix
> {
>   lib,
>   stdenv,
>   fetchFromGitHub,
>   fetchYarnDeps,
>   yarnConfigHook,
>   yarnBuildHook,
>   yarnInstallHook,
>   nodejs,
> }:
>
> stdenv.mkDerivation (finalAttrs: {
>   pname = "...";
>   version = "...";
>
>   src = fetchFromGitHub {
>     owner = "...";
>     repo = "...";
>     tag = "v${finalAttrs.version}";
>     hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
>   };
>
>   yarnOfflineCache = fetchYarnDeps {
>     yarnLock = finalAttrs.src + "/yarn.lock";
>     hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
>   };
>
>   nativeBuildInputs = [
>     yarnConfigHook
>     yarnBuildHook
>     yarnInstallHook
>     # Needed for executing package.json scripts
>     nodejs
>   ];
>
>   meta = {
>     # ...
>   };
> })
> ```
>
> پیش از نصب را غیرفعال می‌کند.
>
> Section 4:
> #### <a id="javascript-yarn-v3-v4"></a> Yarn Berry v3/v4
> Yarn Berry (v3 / v4) have similar formats, they start with blocks like these:
>
> - #### Yarn Berry
>

> ```yaml
> __metadata:
>   version: 6
>   cacheKey: 8[cX]
> ```
>

> ```yaml
> __metadata:
>   version: 8
>   cacheKey: 10[cX]
> ```
>
> برای این بسته‌ها، برخی ابزارهای کمکی در زیر بسته‌های مربوطهٔ `yarn-berry_3` و `yarn-berry_4` ارائه شده‌اند:
>
> -
>

> ```nix
> {
>   stdenv,
>   nodejs,
>   yarn-berry_4,
> }:
>
> let
>   yarn-berry = yarn-berry_4;
>
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "foo";
>   version = "0-unstable-1980-01-01";
>
>   src = {
>     #...
>   };
>
>   nativeBuildInputs = [
>     nodejs
>     yarn-berry.yarnBerryConfigHook
>   ];
>
>   offlineCache = yarn-berry.fetchYarnBerryDeps {
>     inherit (finalAttrs) src;
>     hash = "...";
>   };
> })
> ```
>
> ##### <a id="javascript-fetchYarnBerryDeps"></a> `yarn-berry_X.fetchYarnBerryDeps`
>
> `fetchYarnBerryDeps` دستور `yarn-berry-fetcher fetch` را در یک derivation با خروجی ثابت (fixed-output derivation) اجرا می‌کند. این یک دریافت‌کننده سفارشی است که برای بارگیری بازتولیدپذیر تمام فایل‌های موجود در فایل `yarn.lock` و اعتبارسنجی هش‌های آن‌ها در طول این فرآیند طراحی شده است. برای وابستگی‌های git، یک چک‌اوت (checkout) در مسیر `${'{'}'{'{'}'{'}'}offlineCache{'{'}'{'}'}'{'}'}/checkouts/&lt;40-character-commit-hash>` ایجاد می‌کند (که برای توصیف محتوای چک‌اوت
>

> ```shell
> $ yarn-berry-fetcher prefetch </path/to/yarn.lock> [/path/to/missing-hashes.json]
> ```
>
> این خروجی، هش را در stdout چاپ می‌کند و می‌توان از آن در اسکریپت‌های به‌روزرسانی برای محاسبه‌ی مجدد هش برای نسخه جدیدی از `yarn.lock` استفاده کرد.
>
> ##### <a id="javascript-yarnBerryConfigHook"></a> `yarn-berry_X.yarnBerryConfigHook`
> `yarnBerryConfigHook` از مسیر انبار که `offlineCache` به آن اشاره دارد برای اجرای `yarn install` در طول ساخت استفاده می‌کند و یک پوشه `node_modules` قابل استفاده از وابستگی‌های دانلودشده تولید می‌نماید.
>
> به صورت داخلی، این ابزار از نسخه پچ‌شده‌ای از Yarn استفاده می‌کند تا مطمئن شود وابستگی‌های git دوباره بسته‌بندی می‌شوند و هرگونه تلاش برای دانلود بلافاصله با شکست مواجه می‌شود.
>
> ##### <a id="javascript-yarnBerry-patching"></a> پچ کردن فایل‌های `package.json` یا `yarn.lock` بالادستی
> در صورتی که به پچ کردن `package.json` یا `yarn.lock` بال
>

> ```nix
> {
>   stdenv,
>   nodejs,
>   yarn-berry_4,
> }:
>
> let
>   yarn-berry = yarn-berry_4;
>
> in
> stdenv.mkDerivation (finalAttrs: {
>   pname = "foo";
>   version = "0-unstable-1980-01-01";
>
>   src = {
>     #...
>   };
>
>   nativeBuildInputs = [
>     nodejs
>     yarn-berry.yarnBerryConfigHook
>   ];
>
>   missingHashes = ./missing-hashes.json;
>   offlineCache = yarn-berry.fetchYarnBerryDeps {
>     inherit (finalAttrs) src missingHashes;
>     hash = "...";
>   };
> })
> ```
>
> ## <a id="javascript-outside-nixpkgs"></a> خارج از Nixpkgs
>
> ابزارهای دیگری نیز در دسترس هستند که به زبان Nix نوشته شده‌اند.
> این ابزارها نمی‌توانند در داخل Nixpkgs استفاده شوند زیرا به [Import From Derivation](#ssec-import-from-derivation) نیاز دارند، که در Nixpkgs مجاز نیست.
>
> اگر در حال بسته‌بندی چیزی خارج از Nixpkgs هستید، موارد زیر را در نظر بگیرید:
>
> ### npmlock2nix {'{'}'{'{'}'{'}'}#javascript-
