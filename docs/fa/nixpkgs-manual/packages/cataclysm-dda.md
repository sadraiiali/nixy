# Cataclysm: Dark Days Ahead {#cataclysm-dark-days-ahead}

## نحوه نصب Cataclysm DDA {#how-to-install-cataclysm-dda}

برای

```nix
cataclysm-dda-git.override {
  version = "YYYY-MM-DD";
  rev = "YOUR_FAVORITE_REVISION";
  sha256 = "CHECKSUM_OF_THE_REVISION";
}
```

هش sha256 را می‌توان از طریق

```sh
nix-prefetch-url --unpack "https://github.com/CleverRaven/Cataclysm-DDA/archive/${YOUR_FAVORITE_REVISION}.tar.gz"
```

پوشه پیکربندی پیش‌فرض `~/.cataclysm-dda` است. اگر `$XDG_CONFIG_HOME/cataclysm-dda` را ترجیح می‌دهید، derivation را بازنشانی کنید:

```nix
cataclysm-dda.override { useXdgDir = true; }
```

## نکته مهم برای بازنشانی بسته‌ها {#important-note-for-overriding-packages}

پس از اعمال `overrideAttrs`، باید صفات `passthru.pkgs` و `passthru.withMods` را یا به صورت دستی یا با استفاده از `attachPkgs` اصلاح کنید:

```nix
let
  # You enabled parallel building.
  myCDDA = cataclysm-dda-git.overrideAttrs (_: {
    enableParallelBuilding = true;
  });

  # Unfortunately, this refers to the package before overriding and
  # parallel building is still disabled.
  badExample = myCDDA.withMods (_: [ ]);

  inherit (cataclysmDDA) attachPkgs pkgs wrapCDDA;

  # You can fix it by hand
  goodExample1 = myCDDA.overrideAttrs (old: {
    passthru = old.passthru // {
      pkgs = pkgs.override { build = goodExample1; };
      withMods = wrapCDDA goodExample1;
    };
  });

  # or by using a helper function `attachPkgs`.
  goodExample2 = attachPkgs pkgs myCDDA;

  # badExample                     # parallel building disabled
  # goodExample1.withMods (_: [])  # parallel building enabled
in
goodExample2.withMods (_: [ ]) # parallel building enabled
```

## سفارشی‌سازی با مودها {#customizing-with-mods}

برای نصب Cataclysm DDA با مودهای انتخابی خود، می‌توانید از صفت (attribute) `withMods` استفاده کنید:

```nix
cataclysm-dda.withMods (mods: with mods; [ tileset.UndeadPeople ])
```

همه‌ی مادها، بسته‌های صوتی و تایلت‌سِت‌های موجود در Nixpkgs در `cataclysmDDA.pkgs` یافت می‌شوند.

در اینجا مثالی برای تغییر مادهای موجود و/یا افزودن مادهای بیشتری که در Nixpkgs موجود نیستند آورده شده‌است:

```nix
let
  customMods =
    self: super:
    lib.recursiveUpdate super {
      # Modify existing mod
      tileset.UndeadPeople = super.tileset.UndeadPeople.overrideAttrs (old: {
        # If you like to apply a patch to the tileset for example
        patches = [ ./path/to/your.patch ];
      });

      # Add another mod
      mod.Awesome = cataclysmDDA.buildMod {
        modName = "Awesome";
        version = "0.x";
        src = fetchFromGitHub {
          owner = "Someone";
          repo = "AwesomeMod";
          rev = "...";
          hash = "...";
        };
        # Path to be installed in the unpacked source (default: ".")
        modRoot = "contents/under/this/path/will/be/installed";
      };

      # Add another soundpack
      soundpack.Fantastic = cataclysmDDA.buildSoundPack {
        # ditto
      };

      # Add another tileset
      tileset.SuperDuper = cataclysmDDA.buildTileSet {
        # ditto
      };
    };
in
cataclysm-dda.withMods (
  mods: with mods.extend customMods; [
    tileset.UndeadPeople
    mod.Awesome
    soundpack.Fantastic
    tileset.SuperDuper
  ]
)
```
