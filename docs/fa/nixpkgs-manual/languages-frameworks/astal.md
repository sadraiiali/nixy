# Astal {#astal}

Astal مجموعه‌ای از بلوک‌های سازنده برای ایجاد پوسته‌های دسکتاپ سفارشی است.

## بسته‌بندی {#astal-bundling}

بسته‌بندی یک برنامه Astal با استفاده از ابزار `ags` انجام می‌شود. می‌توانید از آن به این صورت استفاده کنید:

```nix
ags.bundle {
  pname = "hyprpanel";
  version = "1.0.0";

  src = fetchFromGitHub {
    #...
  };

  # change your entry file (default is `app.ts`)
  entry = "app.ts";

  dependencies = [
    # list here astal modules that your package depends on
    # `astal3`, `astal4` and `astal.io` are automatically included
    astal.apps
    astal.battery
    astal.bluetooth

    # you can also list here other runtime dependencies
    hypridle
    hyprpicker
    hyprsunset
  ];

  # GTK 4 support is opt-in
  enableGtk4 = true;

  meta = {
    #...
  };
}
```

همچنین می‌توانید تمام آرگومان‌های دیگری را که توسط `stdenv.mkDerivation` پشتیبانی می‌شوند پاس دهید.
