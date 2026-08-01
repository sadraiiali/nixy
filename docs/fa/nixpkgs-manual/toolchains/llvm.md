# زنجیره‌ابزار LLVM {#chap-toolchains}

LLVM یک بهینه‌ساز و مولد کد مستقل از هدف است و به عنوان پایه و اساس بسیاری از کامپایلرها مانند

```nix
import <nixpkgs> {
  localSystem = {
    system = "x86_64-linux";
  };
  crossSystem = {
    useLLVM = true;
    linker = "lld";
  };
}
```

توجه داشته باشید که ما `linker` را روی `lld` تنظیم می‌کنیم. علت این امر آن است که LLVM لینکر اختصاصی خود به نام «lld» را دارد. با تنظیم آن، از Clang و lld در این نمونه‌ی جدید از Nixpkgs استفاده می‌کنیم. یک روش میان‌بر برای ساخت همه‌چیز با LLVM وجود دارد: `pkgsLLVM`. استفاده از این روش همراه با `nix-build` (یا `nix build`) ساده‌تر است:

```bash
nix-build -A pkgsLLVM.hello
```

این کار بسته GNU hello را با LLVM و لینک‌کننده lld همان‌طور که قبلاً اشاره شد، کامپایل خواهد کرد.

#### استفاده از `clangStdenv` {#sec
