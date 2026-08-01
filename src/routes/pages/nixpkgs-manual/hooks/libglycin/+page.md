# <a id="libglycin-hooks"></a> libglycin

[Glycin](https://gitlab.gnome.org/GNOME/glycin) یک کتابخانه برای بارگیری تصویر به‌صورت ایزوله شده (Sandboxed) و قابل گسترش است.

<a id="libglycin-setup-hook"></a> برای بیشتر برنامه‌هایی که از آن استفاده می‌کنند، قالب‌های مجزای تصویر از طریق باینری‌های ارائه‌شده توسط `glycin-loaders` بارگیری می‌شوند. مسیرهای این بارگذارها باید به محیط تزریق شوند، به‌عنوانی مثال با استفاده از [`wrapGAppsHook`](#ssec-gnome-hooks). `libglycin.setupHook` این کار را انجام می‌دهد.

<a id="libglycin-patch-vendor-hook"></a> علاوه بر این، برای پروژه‌های Rust، خود کریت Rust مربوط به `glycin` نیازمند یک پچ است تا به‌صورت خودمختار / مستقل درآید. `libglycin.patchVendorHook` این کار را انجام می‌دهد. این مورد برای پروژه‌هایی که از کتابخانه ELF موجود در بسته `libglycin` استفاده می‌کنند، لازم نیست.

## <a id="libglycin-hooks-example-code-snippet"></a> قطعه‌کد نمونه

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

## <a id="libglycin-hook-variables-controlling"></a> متغیرهای کنترل‌کننده glycin-loaders

### <a id="glycin-cargo-deps-path"></a> `glycinCargoDepsPath`

مسیر یک پوشه حاوی کریت `glycin` برای پچ کردن. مقدار پیش‌فرض آن برابر با پوشه کریت ایجادشده توسط `cargoSetupHook` یا `./vendor/` است.

### <a id="glycin-dont-wrap"></a> `dontWrapGlycinLoaders`

غیرفعال کردن افزودن مسیر بارگذارهای Glycin به `XDG_DATA_DIRS` با `wrapGAppsHook`.
