# <a id="modules-generic"></a> عمومی

ماژول‌های عمومی می‌توانند برای گسترش پیکربندی‌های هر [کلاس] درون‌ریزی شوند.

## <a id="modules-generic-meta-maintainers"></a> `meta-maintainers.nix`

گزینه‌های زیر هنگام استفاده از `imports = [ (nixpkgs + "/modules/generic/meta-maintainers.nix") ];` در دسترس قرار می‌

- `id-prefix: opt-modules-generic-meta-maintainers-`
- `list-id: configuration-variable-list`
- `options-modules-generic-meta-maintainers`

[class]: https://nixos.org/manual/nixpkgs/unstable/#module-system-lib-evalModules-param-class
