# julec.hook {#julec-hook}

[Jule](https://jule.dev) یک زبان برنامه‌نویسی کارآمد است که برای ساخت نرم‌افزارهای کارآمد، سریع، قابل اعتماد و امن در عین حفظ سادگی طراحی شده است.

در Nixpkgs، `jule.hook` فازهای پیش‌فرض ساخت، بررسی و نصب را بازنشانی می‌کند.

## قطعه‌کد نمونه {#julec-hook-example-code-snippet}

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

## متغیرهای کنترل‌کننده julec.hook {#julec-hook-variables}

### `JULE_SRC_DIR` {#julec-hook-variable-jule-src-dir}

پوشه سورس شامل `main.jule` را مشخص می‌کند.
مقدار پیش‌فرض `./src` است.

### `JULE_OUT_DIR` {#julec-hook-variable-jule-out-dir}

پوشه خروجی را برای باینری کامپایل‌شده مشخص می‌کند.
مقدار پیش‌فرض `./bin` است.

### `JULE_OUT_NAME` {#julec-hook-variable-jule-out-name}

نام باینری کامپایل‌شده را مشخص می‌کند.
مقدار پیش‌فرض `output` است.

### `JULE_TEST_DIR` {#julec-hook-variable-jule-test-dir}

پوشه شامل فایل‌های تست را مشخص می‌کند.
مقدار پیش‌فرض، مقدار [`JULE_SRC_DIR`](#julec-hook-variable-jule-src-dir) است.

### `JULE_TEST_OUT_DIR` {#julec-hook-variable-jule-test-out-dir}

پوشه خروجی را برای باینری‌های تست کامپایل‌شده مشخص می‌کند.
مقدار پیش‌فرض، مقدار [`JULE_OUT_DIR`](#julec-hook-variable-jule-out-dir) است.

### `JULE_TEST_OUT_NAME` {#julec-hook-variable-jule-test-out-name}

نام باینری تست کامپایل‌شده را مشخص می‌کند.
مقدار پیش‌فرض، مقدار [`JULE_OUT_NAME`](#julec-hook-variable-jule-out-name) به همراه پسوند `-test` است.

### `dontUseJulecBuild` {#julec-hook-variable-dontusejulecbuild}

وقتی روی true تنظیم شود، از `julecBuildHook` از‌پیش‌تعریف‌شده استفاده نمی‌کند.
مقدار پیش‌فرض false است.

### `dontUseJulecCheck` {#julec-hook-variable-dontusejuleccheck}

وقتی روی true تنظیم شود، از `julecCheckHook` از‌پیش‌تعریف‌شده استفاده نمی‌کند.
مقدار پیش‌فرض false است.

### `dontUseJulecInstall` {#julec-hook-variable-dontusejulecinstall}

وقتی روی true تنظیم شود، از `julecInstallHook` از‌پیش‌تعریف‌شده استفاده نمی‌کند.
مقدار پیش‌فرض false است.
