# <a id="julec-hook"></a> julec.hook

[Jule](https://jule.dev) یک زبان برنامه‌نویسی کارآمد است که برای ساخت نرم‌افزارهای کارآمد، سریع، قابل اعتماد و امن در عین حفظ سادگی طراحی شده است.

در Nixpkgs، `jule.hook` فازهای پیش‌فرض ساخت، بررسی و نصب را بازنشانی می‌کند.

## <a id="julec-hook-example-code-snippet"></a> قطعه‌کد نمونه

```nix
{
  julec,
  clangStdenv,
}:

clangStdenv.mkDerivation (finalAttrs: {
  # ...

  nativeBuildInputs = [ julec.hook ];

  # Customize filenames if needed
  JULE_SRC_DIR = "./src";
  JULE_OUT_DIR = "./bin";
  JULE_OUT_NAME = "hello-jule";
  JULE_TEST_DIR = "./tests";
  JULE_TEST_OUT_DIR = "./test-bin";
  JULE_TEST_OUT_NAME = "hello-jule-test";

  # ...
})
```

## <a id="julec-hook-variables"></a> متغیرهای کنترل‌کننده julec.hook

### <a id="julec-hook-variable-jule-src-dir"></a> `JULE_SRC_DIR`

پوشه سورس شامل `main.jule` را مشخص می‌کند.
مقدار پیش‌فرض `./src` است.

### <a id="julec-hook-variable-jule-out-dir"></a> `JULE_OUT_DIR`

پوشه خروجی را برای باینری کامپایل‌شده مشخص می‌کند.
مقدار پیش‌فرض `./bin` است.

### <a id="julec-hook-variable-jule-out-name"></a> `JULE_OUT_NAME`

نام باینری کامپایل‌شده را مشخص می‌کند.
مقدار پیش‌فرض `output` است.

### <a id="julec-hook-variable-jule-test-dir"></a> `JULE_TEST_DIR`

پوشه شامل فایل‌های تست را مشخص می‌کند.
مقدار پیش‌فرض، مقدار [`JULE_SRC_DIR`](#julec-hook-variable-jule-src-dir) است.

### <a id="julec-hook-variable-jule-test-out-dir"></a> `JULE_TEST_OUT_DIR`

پوشه خروجی را برای باینری‌های تست کامپایل‌شده مشخص می‌کند.
مقدار پیش‌فرض، مقدار [`JULE_OUT_DIR`](#julec-hook-variable-jule-out-dir) است.

### <a id="julec-hook-variable-jule-test-out-name"></a> `JULE_TEST_OUT_NAME`

نام باینری تست کامپایل‌شده را مشخص می‌کند.
مقدار پیش‌فرض، مقدار [`JULE_OUT_NAME`](#julec-hook-variable-jule-out-name) به همراه پسوند `-test` است.

### <a id="julec-hook-variable-dontusejulecbuild"></a> `dontUseJulecBuild`

وقتی روی true تنظیم شود، از `julecBuildHook` از‌پیش‌تعریف‌شده استفاده نمی‌کند.
مقدار پیش‌فرض false است.

### <a id="julec-hook-variable-dontusejuleccheck"></a> `dontUseJulecCheck`

وقتی روی true تنظیم شود، از `julecCheckHook` از‌پیش‌تعریف‌شده استفاده نمی‌کند.
مقدار پیش‌فرض false است.

### <a id="julec-hook-variable-dontusejulecinstall"></a> `dontUseJulecInstall`

وقتی روی true تنظیم شود، از `julecInstallHook` از‌پیش‌تعریف‌شده استفاده نمی‌کند.
مقدار پیش‌فرض false است.
