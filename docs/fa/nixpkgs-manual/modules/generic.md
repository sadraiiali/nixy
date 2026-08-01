
# عمومی {#modules-generic}

ماژول‌های عمومی می‌توانند برای گسترش پیکربندی‌های هر [کلاس] درون‌ریزی شوند.

## `meta-maintainers.nix` {#modules-generic-meta-maintainers}

گزینه‌های زیر هنگام استفاده از `imports = [ (nixpkgs + "/modules/generic/meta-maintainers.nix") ];` در دسترس قرار می

```{=include=} options
id-prefix: opt-modules-generic-meta-maintainers-
list-id: configuration-variable-list
source: ../options-modules-generic-meta-maintainers.json
```

[class]: https://nixos.org/manual/nixpkgs/unstable/#module-system-lib-evalModules-param-class
