# libglycin {#libglycin-hooks}

[Glycin](https://gitlab.gnome.org/GNOME/glycin) یک کتابخانه برای بارگیری تصویر به‌صورت ایزوله شده (Sandboxed) و قابل گسترش است.

[]{#libglycin-setup-hook} برای بیشتر برنامه‌هایی که از آن استفاده می‌کنند، قالب‌های مجزای تصویر از طریق باینری‌های ارائه‌شده توسط `glycin-loaders` بارگیری می‌شوند. مسیرهای این بارگذارها باید به محیط تزریق شوند، به‌عنوانی مثال با استفاده از [`wrapGAppsHook`](#ssec-gnome-hooks). `libglycin.setupHook` این کار را انجام می‌دهد.

[]{#libglycin-patch-vendor-hook} علاوه بر این، برای پروژه‌های Rust، خود کریت Rust مربوط به `glycin` نیازمند یک پچ است تا به‌صورت خودمختار / مستقل درآید. `libglycin.patchVendorHook` این کار را انجام می‌دهد. این مورد برای پروژه‌هایی که از کتابخانه ELF موجود در بسته `libglycin` استفاده می‌کنند، لازم نیست.

## قطعه‌کد نمونه {#libglycin-hooks-example-code-snippet}

```nix
{
  lib,
  rustPlatform,
  libglycin,
  glycin-loaders,
  wrapGAppsHook4,
}:

rustPlatform.buildRustPackage {
  # ...

  cargoHash = "...";

  nativeBuildInputs = [
    wrapGAppsHook4
    libglycin.patchVendorHook
  ];

  buildInputs = [
    libglycin.setupHook
    glycin-loaders
  ];

  # ...
}
```

## متغیرهای کنترل‌کننده glycin-loaders {#libglycin-hook-variables-controlling}

### `glycinCargoDepsPath` {#glycin-cargo-deps-path}

مسیر یک پوشه حاوی کریت `glycin` برای پچ کردن. مقدار پیش‌فرض آن برابر با پوشه کریت ایجادشده توسط `cargoSetupHook` یا `./vendor/` است.

### `dontWrapGlycinLoaders` {#glycin-dont-wrap}

غیرفعال کردن افزودن مسیر بارگذارهای Glycin به `XDG_DATA_DIRS` با `wrapGAppsHook`.
