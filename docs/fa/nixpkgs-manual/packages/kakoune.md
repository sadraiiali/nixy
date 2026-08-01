# Kakoune {#sec-kakoune}

Kakoune را می‌توان به‌گونه‌ای ساخت که افزونه‌ها را به صورت خودکار بارگیری کند:

```nix
(kakoune.override { plugins = with pkgs.kakounePlugins; [ parinfer-rust ]; })
```
