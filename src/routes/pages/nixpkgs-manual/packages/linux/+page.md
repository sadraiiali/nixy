قابلیت‌های اضافی کمتری دارد، همان‌طور که در ادامه توضیح داده شده است.

Both functions have an argument `kernelPatches` which should be a list of `{'{'}'{'{'}'{'}'}name, patch, extraConfig{'{'}'{'}'}'{'}'}` attribute sets, where `name` is the name of the patch (which is included in the kernel’s `meta.description` attribute), `patch`

```nix
pkgs.linux_latest.override {
  ignoreConfigErrors = true;
  autoModules = false;
  kernelPreferBuiltin = true;
  structuredExtraConfig = with lib.kernel; {
    DEBUG_KERNEL = yes;
    FRAME_POINTER = yes;
    KGDB = yes;
    KGDB_SERIAL_CONSOLE = yes;
    DEBUG_INFO = yes;
  };
}
```

## <a id="sec-manual-kernel-configuration"></a> پیکربندی دستی هسته (kernel)

گاهی اوقات ممکن است استفاده از هسته‌های ساخته‌شده با `pkgs.buildLinux` مطلوب نباشد، به‌ویژه اگر لازم باشد اکثر پیکربندی‌های رایج تغییر داده شوند یا غیرفعال شوند تا هسته‌ای مطابق با مورد استفادهٔ هدف به دست آید.
یک نمونه از این دست، ساخت یک هسته (kernel) برای استفاده در یک ماشین مجازی (VM) یا میکرو VM است. در این موارد می‌توانید از `pkgs.linuxPackages_custom` استفاده کنید. این ویژگی مستلزم مشخص شدن صفات `src`، `version` و `configfile` است.

<a id="ex-using-linux-manual-config"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # استفاده از `pkgs.linuxPackages_custom` با کد منبع، نسخه و فایل پیکربندی مشخص
>

> ```nix
> { pkgs, ... }:
> pkgs.linuxPackages_custom {
>   version = "6.1.55";
>   src = pkgs.fetchurl {
>     url = "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${version}.tar.xz";
>     hash = "sha256-qH4kHsFdU0UsTv4hlxOjdp2IzENrW5jPbvsmLEr/FcA=";
>   };
>   configfile = ./path_to_config_file;
> }
> ```
>
> در صورت لزوم، می‌توان رشته نسخه را اندکی تغییر داد تا صراحتاً به عنوان یک نسخه سفارشی نشانه‌گذاری شود. در صورت انجام این کار، اطمینان حاصل کنید که صفت (attribute) `modDirVersion` با نسخه کد منبع مطابقت داشته باشد، در غیر این صورت ساخت (Build) با شکست مواجه خواهد شد.
>

> ```nix
> { pkgs, ... }:
> pkgs.linuxPackages_custom {
>   version = "6.1.55-custom";
>   modDirVersion = "6.1.55";
>   src = pkgs.fetchurl {
>     url = "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${modDirVersion}.tar.xz";
>     hash = "sha256-qH4kHsFdU0UsTv4hlxOjdp2IzENrW5jPbvsmLEr/FcA=";
>   };
>   configfile = ./path_to_config_file;
> }
> ```

برای سفارشی‌سازی بیشتر، می‌توان صفت‌های اضافی را به جای `linuxPackages_custom` همراه با `linuxManualConfig` استفاده کرد. توصیه می‌شود [کد منبع `pkgs.linuxManualConfig`](https://github.com/NixOS/nixpkgs/blob/d77bda728d5

```ShellSession
$ nix-shell '<nixpkgs>' -A linuxKernel.kernels.linux_X_Y.configEnv
$ unpackPhase
$ cd linux-*
$ make nconfig
```

## <a id="sec-linux-kernel-developing-modules"></a> توسعهٔ ماژول‌های هسته

هنگام توسعهٔ ماژول‌های هسته، اغلب بسیار مناسب است که چرخهٔ ویرایش-کامپایل-اجرا را در سریع‌ترین زمان ممکن انجام دهید.
قطعه‌کد زیر را به عنوان یک مثال ببینید.

<a id="ex-edit-compile-run-kernel-modules"></a>
> <span class="admonition-kind" data-kind="example"></span>
>
> **مثال**
>
> # چرخهٔ ویرایش-کامپایل-اجرا هنگام توسعهٔ درایورهای `mellanox`
>

> ```ShellSession
> $ nix-build '<nixpkgs>' -A linuxPackages.kernel.dev
> $ nix-shell '<nixpkgs>' -A linuxPackages.kernel
> $ unpackPhase
> $ cd linux-*
> $ make -C $dev/lib/modules/*/build M=$(pwd)/drivers/net/ethernet/mellanox modules
> # insmod ./drivers/net/ethernet/mellanox/mlx5/core/mlx5_core.ko
> ```

## <a id="sec-linux-kernel-maintainer-information"></a> اطلاعات نگه‌دارنده

### <a id="sec-linux-updates"></a> به‌روزرسانی هسته‌ها

به‌روزرسانی تمامی هسته‌ها با اسکریپت زیر قابل انجام است:

```ShellSession
$ pkgs/os-specific/linux/kernel/update.sh
```

تغییر به این صورت ارسال می‌شود:

* یک PR در برابر `staging-nixos` ثبت کنید.
  * برچسب `backport staging-nixos-XX.XX` را برای بک‌پورت خودکار اضافه کنید.
    با استفاده از یک PR اضافی، بک‌پورت خودکار به نسخه پایدار را بدون چری‌پیک دستی دریافت می‌کنیم.
* در `staging-nixos` یا `staging-nixos-XX.XX` ادغام کنید.
* یک PR از ``
```nix
    {
      linux_X_Y = callPackage ../os-specific/linux/kernel/mainline.nix {
        branch = "X.Y";
        kernelPatches = [
          # any new patches required (it makes to look which patches are used by its predecessor)
        ];
      };
    }
    ```
* نمونه‌سازی مجموعه بسته‌ها در `vanillaPackages`:

```nix
    {
      linux_X_Y = recurseIntoAttrs (packagesFor kernels.linux_X_Y);
    }
    ```
. این موضوع شامل هسته‌هایی که از درخت سورس اصلی (mainline) استفاده می‌کنند، اما پیکربندی متفاوتی دارند نیز می‌شود. هسته‌ها برای پشتیبانی سخت‌افز
