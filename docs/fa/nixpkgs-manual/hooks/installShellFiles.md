# `installShellFiles` {#installshellfiles}

این قلاب کمک‌رسان‌هایی را اضافه می‌کند که فرآورده‌های ساخت مانند فایل‌های اجرایی، صفحات راهنما (manpages) و تکمیل‌کننده‌های شل (shell completions) را نصب می‌کنند.

این قلاب توابع زیر را ارائه می‌دهد که می‌توان از آن‌ها در قلاب `postInstall` خود استفاده کرد:

## `installBin` {#installshellfiles-installbin}

تابع `installBin` یک یا چند مسیر به فایل‌ها را برای نصب به عنوان فایل‌های اجرایی دریافت می‌کند.

این تابع آن‌ها را درون [`outputBin`](#outputbin) قرار می‌دهد.

### نمونه استفاده {#installshellfiles-installbin-exampleusage}

```nix
{
  nativeBuildInputs = [ installShellFiles ];

  # Sometimes the file has an undesirable name. It should be renamed before
  # being installed via installBin
  postInstall = ''
    mv a.out delmar
    installBin foobar delmar
  '';
}
```

## `installManPage` {#installshellfiles-installmanpage}

تابع `installManPage` یک یا چند مسیر به صفحات راهنما (manpages) را برای نصب دریافت می‌کند.

صفحات راهنما باید دارای پسوند بخش باشند و به‌طور اختیاری می‌توانند فشرده‌شده باشند (با پسوند `.gz`). این تابع آن‌ها را در پوشه‌ی صحیح `share/man/man<section>/` در [`outputMan`](#outputman) قرار می‌دهد.

### نمونه استفاده {#installshellfiles-installmanpage-exampleusage}

```nix
{
  nativeBuildInputs = [ installShellFiles ];

  # Sometimes the manpage file has an undesirable name; e.g., it conflicts with
  # another software with an equal name. To install it with a different name,
  # the installed name must be provided before the path to the file.
  #
  # Below install a manpage "foobar.1" from the source file "./foobar.1", and
  # also installs the manpage "fromsea.3" from the source file "./delmar.3".
  postInstall = ''
    installManPage \
        foobar.1 \
        --name fromsea.3 delmar.3
  '';
}
```

صفحه راهنما ممکن است حاصل یک ورودی پایپ‌شده (مثلاً `<(cmd)`) باشد؛ در این صورت، نام آن باید قبل از پایپ با پرچم `--name` ارائه شود.

```nix
{
  nativeBuildInputs = [ installShellFiles ];

  postInstall = ''
    installManPage --name foobar.1 <($out/bin/foobar --manpage)
  '';
}
```

اگر تجزیه‌ی آرگومان‌ها مورد نظر نیست، برای انصراف از تمامی آرگومان‌های بعدی `--` را پاس دهید.

```nix
{
  nativeBuildInputs = [ installShellFiles ];

  # Installs a manpage from a file called "--name"
  postInstall = ''
    installManPage -- --name
  '';
}
```

## `installShellCompletion` {#installshellfiles-installshellcompletion}

تابع `installShellCompletion` یک یا چند مسیر به فایل‌های تکمیل شل را می‌پذیرد.

به‌طور پیش‌فرض، نوع شل از روی پسوند فایل تکمیل به‌صورت خودکار تشخیص داده می‌شود، اما می‌توانید با پاس دادن یکی از پرچم‌های `--bash`، `--fish`، `--zsh` یا `--nushell` نیز آن را مشخص کنید. این پرچم‌ها بر روی تمام مسیرهای درج‌شده بعد از خود (تا زمانی که پرچم شل دیگری قرار گیرد) اعمال می‌شوند. همچنین می‌توان برای هر مسیر با قرار دادن پرچم `--name NAME` قبل از آن، یک نام نصب سفارشی تعیین کرد. اگر این پرچم ارائه نشود، تکمیل‌های zsh به‌طور خودکار تغییر نام می‌یابند به‌طوری که `foobar.zsh` به `_foobar` تبدیل می‌شود. می‌توان با استفاده از پرچم `--cmd NAME` یک نام ریشه برای تمام مسیرها تعیین کرد؛ این کار نام مناسب را بسته به شل می‌سازد (به عنوان مثال `--cmd foo` نام `foo.bash` را برای bash و `_foo` را برای zsh می‌سازد).

### نمونه استفاده {#installshellfiles-installshellcompletion-exampleusage}

```nix
{
  nativeBuildInputs = [ installShellFiles ];
  postInstall = ''
    # explicit behavior
    installShellCompletion --bash --name foobar.bash share/completions.bash
    installShellCompletion --fish --name foobar.fish share/completions.fish
    installShellCompletion --nushell --name foobar share/completions.nu
    installShellCompletion --zsh --name _foobar share/completions.zsh
    # implicit behavior
    installShellCompletion share/completions/foobar.{bash,fish,zsh,nu}
  '';
}
```

مسیر همچنین می‌تواند نتیجه‌ی جایگزینی فرآیند (به‌عنوان مثال `<(cmd)`) باشد، که در این صورت شل و نام باید ارائه شوند (زیر را ببینید).

اگر فایل تکمیل شل مقصد واقعاً موجود نباشد یا پس از فراخوانی `installShellCompletion` دارای صفر بایت باشد، این حالت به عنوان شکست ساخت در نظر گرفته می‌شود. به‌طور خاص، اگر فایل‌های تکمیل به‌صورت همراه با سورس (vendored) عرضه نشده باشند، بلکه با اجرای یک فایل قابل‌اجرا تولید شوند، این امر احتمالاً در سناریوهای کامپایل متقاطع با شکست مواجه خواهد شد. نتیجه، یک فایل تکمیل صفر بایتی و در نتیجه شکست ساخت خواهد بود. برای جلوگیری از این مسئله، دستورات تولید تکمیل را محافظت (guard) کنید.

### نمونه استفاده {#installshellfiles-installshellcompletion-exampleusage-guarded}

```nix
{
  nativeBuildInputs = [ installShellFiles ];
  postInstall = lib.optionalString (stdenv.buildPlatform.canExecute stdenv.hostPlatform) ''
    # using process substitution
    installShellCompletion --cmd foobar \
      --bash <($out/bin/foobar --bash-completion) \
      --fish <($out/bin/foobar --fish-completion) \
      --nushell <($out/bin/foobar --nushell-completion) \
      --zsh <($out/bin/foobar --zsh-completion)
  '';
}
```
