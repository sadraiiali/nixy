# <a id="sec-php"></a> PHP

## <a id="ssec-php-user-guide"></a> راهنمای کاربر

### <a id="ssec-php-user-guide-overview"></a> نگاه کلی

چندین نسخه از PHP در Nix در دسترس است که هر کدام طیف گسترده‌ای از افزونه‌ها و کتابخانه‌ها را ارائه

```nix
php.withExtensions ({ enabled, all }: enabled ++ [ all.imagick ])
```

برای مستثنی کردن برخی از افزونه‌های پیش‌فرض (و نه همه آن‌ها)، می‌توانید فهرست `enabled` را به این صورت فیلتر کنید:

```nix
php.withExtensions (
  { enabled, all }: (lib.filter (e: e != php.extensions.opcache) enabled) ++ [ all.imagick ]
)
```

برای ساخت فهرست افزونه‌های خود از پایه، می‌توانید `enabled` را نادیده بگیرید:

```nix
php.withExtensions (
  { all, ... }:
  with all;
  [
    imagick
    opcache
  ]
)
```

`php.withExtensions` با پوشاندن یک بسته پایه حداقل php، افزونه‌ها را ارائه می‌دهد و یک فایل `php.ini` شامل فهرست تمام افزونه‌های قابل بارگیری را فراهم می‌کند. شما می‌توانید

```nix
php.buildEnv {
  extensions =
    { all, ... }:
    with all;
    [
      imagick
      opcache
    ];
  extraConfig = "memory_limit=256M";
}
```

#### <a id="ssec-php-user-guide-installing-with-extensions-phpfpm"></a> نمونه پیکربندی برای `phpfpm`

می‌توانید از مثال‌های قبلی در یک استخر `phpfpm` به نام `foo` به صورت زیر استفاده کنید:

```nix
let
  myPhp = php.withExtensions (
    { all, ... }:
    with all;
    [
      imagick
      opcache
    ]
  );
in
{
  services.phpfpm.pools."foo".phpPackage = myPhp;
}
```

```nix
let
  myPhp = php.buildEnv {
    extensions =
      { all, ... }:
      with all;
      [
        imagick
        opcache
      ];
    extraConfig = "memory_limit=256M";
  };
in
{
  services.phpfpm.pools."foo".phpPackage = myPhp;
}
```

#### <a id="ssec-php-user-guide-installing-with-extensions-nix-shell"></a> نمونه استفاده با `nix-shell`

این دستور یک محیط موقت را راه‌اندازی می‌کند که شامل یک مفسر PHP با افزونه‌های فعال‌شده‌ی `imagick` و `opcache` است:

```sh
nix-shell -p 'php.withExtensions ({ all, ... }: with all; [ imagick opcache ])'
```

### <a id="ssec-php-user-guide-installing-packages-with-extensions"></a> نصب بسته‌های PHP به همراه افزونه‌ها

تمام ابزارهای تعاملی از بسته PHP که از آن دریافت شده‌اند استفاده می‌کنند، بنابراین همه بسته‌ها در `php.packages.*` از بسته `php` به همراه افزونه‌های پیش‌فرض آن استفاده می‌کنند. گاهی اوقات این مجموعه پیش‌فرض از افزونه‌ها کافی نیست و ممکن است بخواهید آن را گسترش دهید. یک نمونه رایج از این موضوع، بسته `composer` است: یک پروژه ممکن است به افزونه‌های خاصی وابسته باشد و `composer` تا زمانی که آن افزونه‌ها بارگذاری نشوند، با آن پروژه کار نخواهد کرد.

مثالی از ساخت `composer` با افزونه‌های اضافی:

```nix
(php.withExtensions (
  { all, enabled }:
  enabled
  ++ (with all; [
    imagick
    redis
  ])
)).packages.composer
```

### <a id="ssec-php-user-guide-overriding-packages"></a> بازنشانی بسته‌های PHP

فایل `php-packages.nix` یک حوزه (scope) تشکیل می‌دهد که به ما اجازه می‌دهد بسته‌های تعریف‌شده در درون آن را بازنشانی کنیم. برای نمونه، جهت اعمال یک پچ به افزونه‌ی `mysqlnd`، می‌توانید یک تابع به سبک overlay به آرگومان `packageOverrides` مربوط به `php` پاس دهید:

```nix
php.override {
  packageOverrides = final: prev: {
    extensions = prev.extensions // {
      mysqlnd = prev.extensions.mysqlnd.overrideAttrs (attrs: {
        patches = attrs.patches or [ ] ++ [
          # ...
        ];
      });
    };
  };
}
```

### <a id="ssec-building-php-projects"></a> ساخت پروژه‌های PHP

با [Composer](https://getcomposer.org/)، می‌توانید با ساده‌سازی مدیریت وابستگی، پروژه‌های PHP را به‌طور مؤثری بسازید. Composer به عنوان مدیر بسته عملی و استاندارد برای PHP، به شما امکان می‌دهد کتابخانه‌هایی را که پروژه‌تان به آن‌ها وابسته است تعریف و مدیریت کنید، و از یک فر

```nix
{ php, fetchFromGitHub }:

php.buildComposerProject2 (finalAttrs: {
  pname = "php-app";
  version = "1.0.0";

  src = fetchFromGitHub {
    owner = "git-owner";
    repo = "git-repo";
    tag = finalAttrs.version;
    hash = "sha256-VcQRSss2dssfkJ+iUb5qT+FJ10GHiFDzySigcmuVI+8=";
  };

  # PHP version containing the `ast` extension enabled
  php = php.buildEnv {
    extensions = ({ enabled, all }: enabled ++ (with all; [ ast ]));
  };

  # The composer vendor hash
  vendorHash = "sha256-86s/F+/5cBAwBqZ2yaGRM5rTGLmou5//aLRK5SA0WiQ=";

  # If the composer.lock file is missing from the repository, add it:
  # composerLock = ./path/to/composer.lock;
})
```

در صورتی که فایل `composer.lock` در مخزن وجود نداشته باشد، مشخص کردن آن با استفاده از صفت (attribute) `composerLock` امکان‌پذیر است.

روش دیگر، استفاده از تمامی این روش‌ها و قلاب‌ها به صورت جداگانه است. این کار این مزیت را دارد که در صورت نیاز، ساخت یک کتابخانه PHP در داخل یک derivation / اشتقاق ساخت دیگر بسیار آسان می‌شود.

در ادامه یک نمونه کد عملیاتی برای ساخت یک کتابخانه PHP با استفاده از `mkDerivation` و توابع و قلاب‌های مجزا آورده شده است

```nix
{
  stdenvNoCC,
  fetchFromGitHub,
  php,
}:

stdenvNoCC.mkDerivation (
  finalAttrs:
  let
    src = fetchFromGitHub {
      owner = "git-owner";
      repo = "git-repo";
      tag = finalAttrs.version;
      hash = "sha256-VcQRSss2dssfkJ+iUb5qT+FJ10GHiFDzySigcmuVI+8=";
    };
  in
  {
    inherit src;
    pname = "php-app";
    version = "1.0.0";

    buildInputs = [ php ];

    nativeBuildInputs = [
      php.packages.composer
      # This hook will use the attribute `composerRepository`
      php.composerHooks.composerInstallHook
    ];

    composerRepository = php.mkComposerRepository {
      inherit (finalAttrs) pname version src;
      composerNoDev = true;
      composerNoPlugins = true;
      composerNoScripts = true;
      # Specifying a custom composer.lock since it is not present in the sources.
      composerLock = ./composer.lock;
      # The composer vendor hash
      vendorHash = "sha256-86s/F+/5cBAwBqZ2yaGRM5rTGLmou5//aLRK5SA0WiQ=";
    };
  }
)
```
