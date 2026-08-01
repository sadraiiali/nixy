# ساخت Nix

این بخش یادداشت‌هایی را درباره‌ی نحوه شروع توسعه و مشارکت در Nix ارائه می‌دهد.
برای دریافت جدیدترین نسخه Nix از گیت‌هاب:

> **نکته**
>
> هنگام دریافت (Check out) مخزن روی ویندوز، پیش از کلون کردن، مطمئن شوید که تنظیم گیت `core.symlinks` فعال است؛ زیرا در مخزن پیوندهای نمادین وجود دارد.

```console
$ git clone https://github.com/NixOS/nix.git
$ cd nix
```

> **نکته**
>
> دستورالعمل‌های زیر فرض می‌کنند که شما از قبل نسخه‌ای از Nix را به صورت محلی نصب کرده‌اید تا بتوانید از آن برای راه‌اندازی محیط توسعه استفاده کنید.
> اگر آن را نصب نکرده‌اید، دستورالعمل‌های [نصب](../installation/index.md) را دنبال کنید.

برای ساخت تمام وابستگی‌ها و شروع یک شل (shell) که در آن تمام متغیرهای محیطی به گونه‌ای تنظیم شده‌اند که بتوان آن وابستگی‌ها را پیدا کرد:

```console
$ nix-shell
```

برای دریافت یک شل با یکی دیگر از [محیط‌های کامپایل پشتیبانی‌شده](#compilation-environments):

```console
$ nix-shell --attr devShells.x86_64-linux.native-clangStdenv
```

> **نکته**
>
> می‌توانید برای بهبود چشمگیر زمان ساخت مجدد (rebuild) از `native-ccacheStdenv` استفاده کنید.
> به‌طور پیش‌فرض، [ccache](https://ccache.dev) فرآورده‌های ساخت را در `~/.cache/ccache/` نگه می‌دارد.

برای ساخت خود Nix در این شل:

```console
[nix-shell]$ out="$(pwd)/outputs/out" dev=$out debug=$out mesonFlags+=" --prefix=${out}"
[nix-shell]$ dontAddPrefix=1 configurePhase
[nix-shell]$ buildPhase
```

برای تست آن:

```console
[nix-shell]$ checkPhase
```

برای نصب آن در `$(pwd)/outputs`:

```console
[nix-shell]$ installPhase
[nix-shell]$ ./outputs/out/bin/nix --version
nix (Nix) 2.12
```

برای ساخت یک نسخه انتشار (release) از Nix برای سیستم‌عامل فعلی و معماری پردازنده:

```console
$ nix-build
```

همچنین می‌توانید Nix را برای یکی از [پلتفرم‌های پشتیبانی‌شده](#platforms) بسازید.

## ساخت Nix با فلیک‌ها

این بخش فرض می‌کند که شما از Nix با ویژگی‌های آزمایشی فعال [`flakes`] و [`nix-command`] استفاده می‌کنید.

[`flakes`]: @docroot@/development/experimental-features.md#xp-feature-flakes
[`nix-command`]: @docroot@/development/experimental-features.md#xp-feature-nix-command

برای ساخت تمام وابستگی‌ها و راه‌اندازی یک شل که در آن تمام متغیرهای محیطی به گونه‌ای پیکربندی شده‌اند که بتوان آن وابستگی‌ها را پیدا کرد:

```console
$ nix develop
```

این شل همچنین `./outputs/bin/nix` را به `$PATH` شما اضافه می‌کند تا بتوانید بلافاصله پس از ساختن `nix`، آن را اجرا کنید.

برای دریافت یک شل با یکی دیگر از [محیط‌های کامپایل پشتیبانی‌شده](#compilation-environments):

```console
$ nix develop .#native-clangStdenv
```

> **نکته**
>
> برای بهبود چشمگیر زمان ساخت مجدد، از `ccacheStdenv` استفاده کنید.
> به طور پیش‌فرض، [ccache](https://ccache.dev) فرآورده‌های ساخت را در `~/.cache/ccache/` نگه می‌دارد.

برای ساختن خود Nix در این شل:

```console
[nix-shell]$ configurePhase
[nix-shell]$ buildPhase
```

برای تست آن:

```console
[nix-shell]$ checkPhase
```

برای نصب آن در `$(pwd)/outputs`:

```console
[nix-shell]$ installPhase
[nix-shell]$ nix --version
nix (Nix) 2.12
```

برای کسب اطلاعات بیشتر درباره‌ی اجرا و فیلتر کردن تست‌ها، به [`testing.md`](./testing.md) مراجعه کنید.

برای ساخت نسخه انتشار (Release) از Nix برای سیستم‌عامل فعلی و معماری پردازنده:

```console
$ nix build
```

همچنین می‌توانید Nix را برای یکی از [پلتفرم‌های پشتیبانی‌شده](#platforms) بسازید.

## پلتفرم‌ها

Nix را می‌توان برای پلتفرم‌های مختلفی ساخت، همان‌طور که در [`flake.nix`] مشخص شده‌است:

[`flake.nix`]: https://github.com/nixos/nix/blob/master/flake.nix

- `x86_64-linux`
- `x86_64-darwin`
- `i686-linux`
- `aarch64-linux`
- `aarch64-darwin`
- `armv6l-linux`
- `armv7l-linux`
- `riscv64-linux`

برای ساخت Nix روی پلتفرمی متفاوت از پلتفرمی که در حال حاضر روی آن هستید، به روشی نیاز دارید تا نصب فعلی Nix شما بتواند کد را برای آن پلتفرم بسازد. راه‌حل‌های متداول شامل [ماشین‌های ساخت راه دور] و [شبیه‌سازی فرمت باینری] (فقط در NixOS پشتیبانی می‌شود) هستند.

[remote builders]: @docroot@/language/derivations.md#attr-builder
[binary format emulation]: https://nixos.org/manual/nixos/stable/options.html#opt-boot.binfmt.emulatedSystems

با داشتن چنین راه‌اندازی‌ای، اجرای ساخت فقط مستلزم انتخاب صفت مربوطه است.
برای مثال، جهت کامپایل برای `aarch64-linux`:

```console
$ nix-build --attr packages.aarch64-linux.default
```

یا برای Nix با قابلیت‌های آزمایشی [`flakes`] و [`nix-command`] فعال‌شده:

```console
$ nix build .#packages.aarch64-linux.default
```

ساخت‌های کامپایل‌متقاطع برای موارد زیر در دسترس هستند:
- `armv6l-linux`
- `armv7l-linux`
- `riscv64-linux`
برای راه‌اندازی (bootstrap) نیکس روی پلتفرم‌های پشتیبانی‌نشده، [انواع سیستم](#system-type) بیشتری را به `crossSystems` در `flake.nix` اضافه کنید.

### ساخت برای چند پلتفرم به صورت هم‌زمان

انجام چندین ساخت بومی و کامپایل‌متقاطع روی یک درخت کد منبع واحد بسیار مفید است،
برای مثال جهت اطمینان از اینکه بهبود پشتیبانی از یک پلتفرم، ساخت را برای پلتفرمی دیگر خراب نکند.
خوشبختانه Meson با محدود کردن تمام فرآورده‌های ساخت به پوشه ساخت، این کار را بسیار ساده می‌کند، به سادگی می‌توانید پوشه کد منبع را بین چندین پوشه ساخت به اشتراک بگذارید که هر کدام شامل ساخت نیکس برای یک پلتفرم متفاوت هستند.

در ادامه روش انجام این کار آمده‌است:

1. به زیرساخت Nixpkgs اعلام کنید که می‌خواهیم Meson پوشه ساخت خود را کجا قرار دهد
```bash
   mesonBuildDir=build-my-variant-name
   ```

1. طبق معمول پیکربندی کنید
```bash
   configurePhase
   ```

3. به روال معمول بسازید (Build)
```bash
   buildPhase
   ```

## نوع سیستم

نکیس از رشته‌ای با فرمت زیر برای شناسایی *نوع سیستم* یا *پلتفرم* اجرایی خود استفاده می‌کند:

```
<cpu>-<os>[-<abi>]
```

هنگامی که Nix برای سیستم مشخصی کامپایل می‌شود، این مقدار تنظیم می‌گردد و بر اساس خروجی اطلاعات [`host_machine`ی Meson](https://mesonbuild.com/Reference-manual_builtin_host_machine.html) است.

به دلایل تاریخی و سازگاری با نسخه‌های پیشین، برخی از شناسه‌های پردازنده و سیستم‌عامل به شرح زیر ترجمه می‌شوند:

| `host_machine.cpu_family()` | `host_machine.endian()` | نیکس |
|-----------------------------|-------------------------|---------------------|
| `x86`                       |                         | `i686`              |
| `arm`                       |                         | `host_machine.cpu()`|
| `ppc`                       | `little`                | `powerpcle`         |
| `ppc64`                     | `little`                | `powerpc64le`       |
| `ppc`                       | `big`                   | `powerpc`           |
| `ppc64`                     | `big`                   | `powerpc64`         |
| `mips`                      | `little`                | `mipsel`            |
| `mips64`                    | `little`                | `mips64el`          |
| `mips`                      | `big`                   | `mips`              |
| `mips64`                    | `big`                   | `mips64`            |

هنگام کامپایل متقاطع کردن Nix با Meson برای توسعه محلی، لازم است با استفاده از گزینه `--cross-file` یک [فایل متقاطع](https://mesonbuild.com/Cross-compilation.html) (cross-file) مشخص کنید. فایل‌های متقاطع، معماری هدف و ابزارهای ساخت (toolchain) را تعریف می‌کنند. هنگام کامپایل متقاطع کردن Nix با نیکس، مجموعه‌ی بسته‌های نیکس (Nixpkgs) این کار را برای شما انجام می‌دهد.

در فلیک nix نیز برخی از اهداف کامپایل متقاطع در دسترس ما هستند:

```
nix build .#nix-everything-riscv64-unknown-linux-gnu
nix build .#nix-everything-armv7l-unknown-linux-gnueabihf
nix build .#nix-everything-armv7l-unknown-linux-gnueabihf
nix build .#nix-everything-x86_64-unknown-freebsd
nix build .#nix-everything-x86_64-w64-mingw32
```

## محیط‌های کامپایل

نیکس را می‌توان با استفاده از چندین محیط کامپایل کرد:

- `stdenv`: پیش‌فرض؛ `gccStdenv`: اجبار به استفاده از کامپایلر `gcc`؛ `clangStdenv`: اجبار به استفاده از کامپایلر `clang`؛ `ccacheStdenv`: فعال‌سازی [ccache]، یک کش کامپایلر برای سرعت بخشیدن به فرآیند ساخت.

برای ساخت با یکی از این محیط‌ها، می‌توانید از استفاده کنید

```console
$ nix build .#nix-cli-ccacheStdenv
```

برای فلیک‌محور Nix، یا

```console
$ nix-build --attr nix-cli-ccacheStdenv
```

برای Nix کلاسیک.

شما می‌توانید به جای `nix-cli-ccacheStdenv` از هر یک از محیط‌های پشتیبانی‌شده‌ی دیگر استفاده کنید.

## یکپارچه‌سازی با ویرایشگر

سرور LSP به نام `clangd` به طور پیش‌فرض روی `devShell`های مبتنی بر `clang` نصب می‌شود.
[محیط‌های کامپایل پشتیبانی‌شده](#compilation-environments) و دستورالعمل‌های نحوه راه‌اندازی شل [با فلیک‌ها](#building-nix-with-flakes) یا در [Nix کلاسیک](#building-nix) را مشاهده کنید.

برای استفاده از LSP با ویرایشگر خود، به یک فایل `compile_commands.json` نیاز دارید که به `clangd` بگوید چگونه کد را کامپایل می‌کنیم.
پیکربندی Meson همواره این فایل را در داخل پوشه ساخت تولید می‌کند.

ویرایشگر خود را به گونه‌ای پیکربندی کنید که از `clangd` موجود در شل `.#native-clangStdenv` استفاده کند.
می‌توانید این کار را یا با اجرای آن در داخل محیط توسعه، یا با استفاده از [nix-direnv](https://github.com/nix-community/nix-direnv) و [افزونه‌ی مناسب ویرایشگر](https://github.com/direnv/direnv/wiki#editor-integration) انجام دهید.

> **نکته**
>
> برای برخی از ویرایشگرها (مانند Visual Studio Code)، ممکن است نیاز باشد یک [افزونه‌ی خاص](https://open-vsx.org/extension/llvm-vs-code-extensions/vscode-clangd) نصب کنید تا ویرایشگر بتواند با `clangd` تعامل داشته باشد.
> برخی دیگر از ویرایشگرها (مانند Emacs، Vim) به یک پلاگین نیاز دارند تا به طور کلی از سرورهای LSP پشتیبانی کنند (مانند [lsp-mode](https://github.com/emacs-lsp/lsp-mode) برای Emacs و [vim-lsp](https://github.com/prabirshrestha/vim-lsp) برای vim).
> راه‌اندازی مختص هر ویرایشگر معمولاً سلیقه‌ای است، بنابراین در اینجا جزئیات بیشتری درباره‌ی آن ارائه نمی‌دهیم.

## قالب‌بندی و قلاب‌های پس از ساخت

ممکن است بخواهید ابزارهای قالب‌بندی را به صورت تک‌اجرا با دستور زیر اجرا کنید:

```console
./maintainers/format.sh
```

### قلاب‌های پیش از کامیت (Pre-commit hooks)

اگر می‌خواهید قالب‌بندها را پیش از هر کامیت اجرا کنید، قلاب‌ها را نصب کنید:

```
pre-commit-hooks-install
```

این کار [pre-commit](https://pre-commit.com) را با استفاده از [cachix/git-hooks.nix](https://github.com/cachix/git-hooks.nix) نصب می‌کند.

هنگام انجام یک کامیت، به خروجی کنسول توجه کنید.
اگر با خطا مواجه شد، دستور `git add --patch` را اجرا کنید تا پیشنهادها تایید شوند _و مجدداً کامیت کنید_.

برای به‌روزرسانی فایل پیکربندی قلاب pre-commit، اقدامات زیر را انجام دهید:
1. از شل توسعه خارج شده و با اجرای دستور `nix develop` دوباره آن را راه‌اندازی کنید.
2. اگر از قلاب pre-commit نیز استفاده می‌کنید، دستور `pre-commit-hooks-install` را نیز دوباره اجرا کنید.

### VSCode

کد JSON زیر را در فایل `.vscode/settings.json` خود قرار دهید تا `nixfmt` پیکربندی شود.
این تنظیمات توسط دستور _Format Document_، گزینه `"editor.formatOnSave"` و غیره شناسایی خواهند شد.

```json
{
  "nix.formatterPath": "nixfmt",
  "nix.serverSettings": {
    "nixd": {
      "formatting": {
        "command": [
          "nixfmt"
        ],
      },
    },
    "nil": {
      "formatting": {
        "command": [
          "nixfmt"
        ],
      },
    },
  },
}
```
