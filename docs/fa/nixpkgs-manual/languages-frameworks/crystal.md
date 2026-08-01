# Crystal {#crystal}

## ساخت یک بسته Crystal {#building-a-crystal-package}

این بخش از [Mint](https://github.com/mint-lang/mint) به عنوان مثالی برای نحوه ساخت یک بسته Crystal استفاده می‌کند.

اگر پروژه Crystal دارای هرگونه وابستگی باشد، اولین گام به دست آوردن یک فایل `shards.nix` است که آن وابستگی‌ها را کدگذاری کند. نسخه‌ای از پروژه را دریافت کرده و به پوشه ریشه آن بروید، به طوری که فایل `shard.lock` آن در پوشه فعلی قرار داشته باشد. پروژه‌های قابل اجرا معمولاً باید فایل `shard.lock` را کامیت کنند، اما گاهی اوقات این‌طور نیست، که یعنی خودتان باید آن را تولید کنید. با وجود یک فایل `shard.lock` موجود، می‌توان `crystal2nix` را اجرا کرد.
```bash
$ git clone https://github.com/mint-lang/mint
$ cd mint
$ git checkout 0.5.0
$ if [ ! -f shard.lock ]; then nix-shell -p shards --run "shards lock"; fi
$ nix-shell -p crystal2nix --run crystal2nix
```

این کار باید یک فایل `shards.nix` تولید کرده باشد.

سپس یک فایل Nix برای derivation خود ایجاد کرده و به شکل زیر از `pkgs.crystal.buildCrystalPackage` استفاده کنید:

```nix
with import <nixpkgs> { };
crystal.buildCrystalPackage rec {
  pname = "mint";
  version = "0.5.0";

  src = fetchFromGitHub {
    owner = "mint-lang";
    repo = "mint";
    tag = version;
    hash = "sha256-dFN9l5fgrM/TtOPqlQvUYgixE4KPr629aBmkwdDoq28=";
  };

  # Insert the path to your shards.nix file here
  shardsFile = ./shards.nix;

  # ...
}
```

این هنوز چیزی را نخواهد ساخت، زیرا هنوز به آن نگفته‌ایم چه فایل‌هایی ساخته شوند. ما می‌توانیم نگاشتی از نام‌های باینری به فایل‌های سورس را با صفت (attribute) `crystalBinaries` مشخص کنیم. دستورالعمل‌های کامپایل کردن پروژه باید این موضوع را نشان دهند. برای Mint، باینری "mint" نامیده می‌شود که از فایل سورس `src/mint.cr` کامپایل می‌شود، بنابراین این را به شکل زیر مشخص می‌کنیم:

```nix
{
  crystalBinaries.mint.src = "src/mint.cr";

  # ...
}
```

علاوه بر این، می‌توانید گزینه‌های پیش‌فرض `crystal build` (که در حال حاضر `--release --progress --no-debug --verbose` هستند) را با

```nix
{
  crystalBinaries.mint.options = [
    "--release"
    "--verbose"
  ];
}
```

بسته به پروژه، ممکن است برای کامپایل کردن موفقیت‌آمیز آن به گام‌های اضافی نیاز داشته باشید. در مورد Mint، ما باید به openssl لینک دهیم، بنابراین در نهایت فایل Nix به صورت زیر خواهد بود:

```nix
with import <nixpkgs> { };
crystal.buildCrystalPackage rec {
  version = "0.5.0";
  pname = "mint";
  src = fetchFromGitHub {
    owner = "mint-lang";
    repo = "mint";
    tag = version;
    hash = "sha256-dFN9l5fgrM/TtOPqlQvUYgixE4KPr629aBmkwdDoq28=";
  };

  shardsFile = ./shards.nix;
  crystalBinaries.mint.src = "src/mint.cr";

  buildInputs = [ openssl ];
}
```
