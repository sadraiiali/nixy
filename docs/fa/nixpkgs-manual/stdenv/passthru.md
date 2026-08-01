، اما چند [الگوی مرسوم](#sec-common-passthru-attributes) وجود دارد.
:::

Wait:
"follow no particular schema" -> "از هیچ اسکیما یا

```nix
{ stdenv, fetchGit }:
let
  hello = stdenv.mkDerivation {
    pname = "hello";
    src = fetchGit {
      # ...
    };

    passthru = {
      foo = "bar";
      baz = {
        value1 = 4;
        value2 = 5;
      };
    };
  };
in
hello.baz.value1
```

```
4
```
` -> Nixpkgs

Everything aligns nicely and follows all constraints.:::

## صفات `passthru` رایج {#sec-common-passthru-attributes}

بسیاری از صفات `passthru` موقعیتی هستند، بنابراین این بخش فقط الگو

```ShellSession
$ cd path/to/nixpkgs
$ nix-build -A your-package.tests
```

" for derivations.
- attribute -> صفت (attribute)
- profile -> پروفایل
- system configuration -> پیکربندی سیستم
- build -> ساخت (Build)
- builds -> ساخت‌ها
- package -> بسته
- packages -> بسته‌ها
- debug -> دیباگ (اشکال‌زدایی)
- PR -> PR
- commit -> کامیت
- argument -> آرگومان

Check all links and markdown syntax preserve:
- `::

```nix
{ nixosTests, ... }:
{
  # ...
  passthru.tests = {
    basic-functionality-and-dovecot-integration = nixosTests.opensmtpd;
  };
}
```

تست‌های NixOS در یک ماشین مجازی (VM) اجرا می‌شوند، بنابراین نسبت به تست‌های معمولی بسته کندتر هستند.
برای اطلاعات بیشتر، راهنمای NixOS دربارهٔ [تست‌های ماژول NixOS](https://nixos.org/manual/nixos/stable/#sec-nixos-tests)
