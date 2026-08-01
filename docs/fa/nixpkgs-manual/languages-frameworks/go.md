# Go {#sec-language-go}

## ساخت ماژول‌های Go با `buildGoModule` {#ssec-language-go}

تابع `buildGoModule` برنامه‌های Go مدیریت‌شده با ماژول‌های Go را می‌سازد. این تابع [Go Modules](https://go.dev/wiki/Modules) را طی یک ساخت دو مرحله‌ای می‌سازد:

- یک derivation دریافت‌کننده (fetcher) میانی به نام `goModules`. این derivation برای دریافت تمامی وابستگی‌های ماژول Go استفاده خواهد شد.

```nix
{
  pet = buildGoModule (finalAttrs: {
    pname = "pet";
    version = "0.3.4";

    src = fetchFromGitHub {
      owner = "knqyf263";
      repo = "pet";
      tag = "v${finalAttrs.version}";
      hash = "sha256-Gjw1dRrgM8D3G7v6WIM2+50r4HmTXvx0Xxme2fH9TlQ=";
    };

    vendorHash = "sha256-ciBIR+a1oaYH+H1PcC8cD8ncfJczk1IiJ8iYNM+R6aA=";

    meta = {
      description = "Simple command-line snippet manager, written in Go";
      homepage = "https://github.com/knqyf263/pet";
      license = lib.licenses.mit;
      maintainers = with lib.maintainers; [ kalbasit ];
    };
  });
}
```

## صفات `buildGoModule` {#buildgomodule-parameters}

بسیاری از صفات [کنترل‌کننده فاز ساخت](#variables-controlling-the-build-phase) توسط `buildGoModule` پشتیبانی می‌شوند. توجه داشته باشید که `buildGoModule` صفات زیر را هنگام ساخت درایویشن با خروجی ثابت `vendor/` goModules نیز می‌خواند:

- [`sourceRoot`](#var-stdenv-sourceRoot)
- [`prePatch`](#var-stdenv-prePatch)
- [`patches`](#var-stdenv-patches)
- [`patchFlags`](#var-stdenv-patchFlags)
- [`postPatch`](#var-stdenv-postPatch)
- [`preBuild`](#var-stdenv-preBuild)
- `env`: برای

```sh
cd path/to/nixpkgs
nix-prefetch -E "{ sha256 }: ((import ./. { }).my-package.overrideAttrs { vendorHash = sha256; }).goModules"
```

می‌توان `vendorHash` را با `overrideAttrs` بازنشانی کرد. نمونه بالا را به این شکل بازنشانی کنید:

```nix
{
  pet_0_4_0 = pet.overrideAttrs (
    finalAttrs: previousAttrs: {
      version = "0.4.0";
      src = fetchFromGitHub {
        inherit (previousAttrs.src) owner repo;
        tag = "v${finalAttrs.version}";
        hash = "sha256-gVTpzmXekQxGMucDKskGi+e+34nJwwsXwvQTjRO6Gdg=";
      };
      vendorHash = "sha256-dUvp7FEW09V0xMuhewPGw3TuAic/sD7xyXEYviZ2Ivs=";
    }
  );
}
```

### `proxyVendor` {#var-go-proxyVendor}

اگر `true` باشد، دریافت‌کنندهٔ واسط به جای وندور کردن (vendoring) وابستگی‌ها، آن‌ها را از [Go module proxy](https://go.dev/ref/mod#module-proxy)

```nix
{
  ldflags = [
    "-X main.Version=${version}"
    "-X main.Commit=${version}"
  ];
}
```

### `tags` {#var-go-tags}

یک فهرست رشته‌ای از [تگ‌های ساخت Go (که محدودیت‌های ساخت نیز نامیده می‌شوند)](https://pkg.go.dev/cmd/go#hdr-Build_constraints) که از طریق آرگومان `-tags` مربوط به `go build` پاس داده می‌شوند. این محدودیت‌ها کنترل می‌کنند که آیا فایل‌های Go از کد منبع باید در ساخت گنجانده شوند یا خیر. برای مثال:

```nix
{
  tags = [
    "production"
    "sqlite"
  ];
}
```

برچسب‌ها را نیز می‌توان به‌صورت شرطی تنظیم کرد:

```nix
{ tags = [ "production" ] ++ lib.optionals withSqlite [ "sqlite" ]; }
```

### `deleteVendor` {#var-go-deleteVendor}

اگر روی `true` تنظیم شود، پوشه vendor ازپیش‌موجود را حذف می‌کند. این گزینه تنها باید زمانی استفاده شود که وابستگی‌های موجود در پوشه vendor خراب یا ناقص باشند.

### `subPackages` {#var-go-subPackages}

به صورت یک رشته یا لیستی از رشته‌ها مشخص می‌شود. سازنده را از ساخت بسته‌های فرزندی که فهرست نشده‌اند محدود می‌کند. اگر `subPackages` مشخص نشود، تمامی بسته‌های فرزند ساخته خواهند شد.

بسیاری از پروژه‌های Go بسته اصلی را در پوشه `cmd` نگه می‌دارند.
مثال زیر می‌تواند تنها برای ساخت باینری‌های example-cli و example-server استفاده شود:

```nix
{
  subPackages = [
    "cmd/example-cli"
    "cmd/example-server"
  ];
}
```

### `excludedPackages` {#var-go-excludedPackages}

به صورت یک رشته یا فهرستی از رشته‌ها مشخص می‌شود. باعث می‌شود سازنده (Builder) از ساخت بسته‌های فرزندی که با هر یک از مقادیر ارائه‌شده مطابقت دارند، صرف‌نظر کند.

### `enableParallelBuilding` {#var-go-enableParallelBuilding}

اینکه آیا ساخت‌ها و تست‌ها باید به صورت

```nix
{
  pet-overridden = pet.overrideAttrs (
    finalAttrs: previousAttrs: {
      passthru = previousAttrs.passthru // {
        # If the original package has an `overrideModAttrs` attribute set, you'd
        # want to extend it, and not replace it. Hence we use
        # `lib.composeExtensions`. If you are sure the `overrideModAttrs` of the
        # original package trivially does nothing, you can safely replace it
        # with your own by not using `lib.composeExtensions`.
        overrideModAttrs = lib.composeExtensions previousAttrs.passthru.overrideModAttrs (
          finalModAttrs: previousModAttrs: {
            # goModules-specific overriding goes here
            postBuild = ''
              # Here you have access to the `vendor` directory.
              substituteInPlace vendor/github.com/example/repo/file.go \
                --replace-fail "panic(err)" ""
            '';
          }
        );
      };
    }
  );
}
```

-Name_Resolution) و [os/user](https://pkg.go.dev/os/user#pkg-overview) را ببینید. توجه داشته باشید که تصمیم دربارهٔ اینکه آیا این بسته‌ها باید از پیاده‌سازی بومی Go استفاده کنند یا خیر را می‌توان در سطح هر

```nix
{
  buildInputs = [
    libvirt
    libxml2
  ];
}
```

مقدار پیش‌فرض `env.CGO_ENABLED` برابر با `1` است.

## صرف‌نظر کردن از تست‌ها {#ssec-skip-go-tests}

```nix
{
  # -run and -skip accept regular expressions
  checkFlags = [ "-run=^Test(Simple|Fast)$" ];
}
```

اگر باید تعداد بیشتری از تست‌ها نادیده گرفته شوند، می‌توان از الگوی زیر استفاده کرد:

```nix
{
  checkFlags =
    let
      # Skip tests that require network access
      skippedTests = [
        "TestNetwork"
        "TestDatabase/with_mysql" # exclude only the subtest
        "TestIntegration"
      ];
    in
    [ "-skip=^${builtins.concatStringsSep "$|^" skippedTests}$" ];
}
```

برای غیرفعال کردن کامل تست‌ها، `doCheck = false;` را تنظیم کنید.

## مهاجرت از `buildGoPackage` به `buildGoModule` {#buildGoPackage-migration}

::: {.warning}
`buildGoPackage` برای انتشار
