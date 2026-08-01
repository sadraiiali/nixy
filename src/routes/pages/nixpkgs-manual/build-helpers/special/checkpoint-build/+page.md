# <a id="sec-checkpoint-build"></a> pkgs.checkpointBuildTools

`pkgs.checkpointBuildTools` روشی برای ساخت افزایشی درایویشن‌ها فراهم می‌کند. این ابزار از دو تابع تشکیل شده است تا امکان انجام ساخت‌های مبتنی بر نقطه بازرسی (checkpoint) را با استفاده از Nix فراهم کند.

جهت حفظ نفوذناپذیری (hermeticity)، درایویشن‌های Nix اجازه نمی‌دهند هیچ وضعیتی بین ساخت‌ها منتقل شود، که این امر ساخت افزایشی شفاف را در داخل یک درایویشن غیرممکن می‌سازد.

با این حال، می‌توانیم با نمایش وضعیت ساخت قبلی به عنوان خروجی درایویشن، به‌طور صریح وضعیت ساخت قبلی را به Nix اعلام کنیم. این کار امکان استفاده از وضعیت ساخت منتقل‌شده را برای یک ساخت افزایشی فراهم می‌آورد.

برای تغییر یک درایویشن معمولی به یک ساخت مبتنی بر نقطه بازرسی، باید این گام‌ها طی شوند:

```nix
  {
    checkpointArtifacts = (pkgs.checkpointBuildTools.prepareCheckpointBuild pkgs.virtualbox);
  }
  ```
  ```nix
  {
    changedVBox = pkgs.virtualbox.overrideAttrs (old: {
      src = path/to/vbox/sources;
    });
  }
  ```
- استفاده از `mkCheckpointBuild changedVBox checkpointArtifacts`
  - بهره‌مندی از زمان‌های ساخت کوتاه‌تر

## <a id="sec-checkpoint-build-example"></a> مثال

```nix
{
  pkgs ? import <nixpkgs> { },
}:
let
  inherit (pkgs.checkpointBuildTools) prepareCheckpointBuild mkCheckpointBuild;
  helloCheckpoint = prepareCheckpointBuild pkgs.hello;
  changedHello = pkgs.hello.overrideAttrs (_: {
    doCheck = false;
    postPatch = ''
      sed -i 's/Hello, world!/Hello, Nix!/g' src/hello.c
    '';
  });
in
mkCheckpointBuild changedHello helloCheckpoint
```
