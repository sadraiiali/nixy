# CUDA {#cuda}

معماری یکپارچه محاسباتی دستگاه (CUDA) یک پلتفرم پردازش موازی و مدل رابط برنامه‌نویسی کاربرد (API) است که توسط NVIDIA ساخته شده است. این فناوری معمولاً برای شتاب‌بخشی به مسائل با محاسبات سنگین استفاده می‌شود و به‌طور گسترده در برنامه‌های کاربردی رایانش با کارایی بالا (HPC) و یادگیری ماشین (ML) به کار گرفته شده است.

## راهنمای کاربر {#cuda-user-guide}

بسته‌های ارائه‌شده توسط NVIDIA که به CUDA نیاز دارند، معمولاً در مجموعه‌های بسته‌ی CUDA ذخیره می‌شوند.

Nixpkgs تعدادی مجموعه بسته‌ی CUDA ارائه می‌دهد که هرکدام بر اساس یک انتشار متفاوت CUDA هستند. صفات (attribute) سطح بالا که دسترسی به مجموعه‌های بسته‌ی CUDA را فراهم می‌کنند، از این قراردادهای نام‌گذاری پیروی می‌کنند:

- `cudaPackages_x_y`: یک مجموعه بسته‌ی دارای نسخه اصلی-فرعی برای یک انتشار خاص CUDA، که در آن `x` و `y` نسخه‌های اصلی و فرعی آن انتشار CUDA هستند.
- `cudaPackages_x`: یک نام مستعار دارای نسخه اصلی به مجموعه بسته‌ی CUDA دارای نسخه اصلی-فرعی با آخرین انتشار اصلی CUDA که به‌طور گسترده پشتیبانی می‌شود.
- `cudaPackages`: یک نام مستعار بدون نسخه به نام مستعار دارای نسخه اصلی برای آخرین انتشار CUDA که به‌طور گسترده پشتیبانی می‌شود. مجموعه بسته‌ای که توسط این نام مستعار ارجاع داده می‌شود، مجموعه بسته‌ی CUDA «پیش‌فرض» نیز نامیده می‌شود.

توصیه می‌شود از صفت (attribute) بدون نسخه `cudaPackages` استفاده کنید. اگرچه مجموعه‌های بسته‌ی دارای نسخه (مانند `cudaPackages_12_8`) در دسترس هستند، اما به صورت دوره‌ای حذف می‌شوند.

در ادامه دو مثال برای روشن شدن قراردادهای نام‌گذاری آورده شده است:

- اگر `cudaPackages_12_9` آخرین انتشار در سری 12.x باشد، اما کتابخانه‌های اصلی مانند OpenCV یا ONNX Runtime در ساخت با آن شکست بخورند، `cudaPackages_12` ممکن است به جای `cudaPackages_12_9` نام مستعاری برای `cudaPackages_12_8` باشد.
- اگر `cudaPackages_13_1` آخرین انتشار باشد، اما کتابخانه‌های اصلی مانند PyTorch یا Torch Vision در ساخت با آن شکست بخورند، `cudaPackages` ممکن است به جای `cudaPackages_13` نام مستعاری برای `cudaPackages_12` باشد.

تمام مجموعه‌های بسته‌ی CUDA شامل بسته‌های رایج CUDA مانند `libcublas`، `cudnn`، `tensorrt` و `nccl` هستند.

### پیکربندی Nixpkgs برای CUDA {#cuda-configuring-nixpkgs-for-cuda}

پشتیبانی از CUDA به صورت پیش‌فرض در Nixpkgs فعال نیست. برای فعال‌سازی پشتیبانی CUDA، اطمینان حاصل کنید که Nixpkgs با یک پیکربندی مشابه زیر درون‌ریزی می‌شود:

```nix
{ pkgs }:
{
  allowUnfreePredicate = pkgs._cuda.lib.allowUnfreeCudaPredicate;
  cudaCapabilities = [ <target-architectures> ];
  cudaForwardCompat = true;
  cudaSupport = true;
}
```

اکثریت بسته‌های CUDA غیرآزاد (unfree) هستند، بنابراین باید یا `allowUnfreePredicate` یا `allowUnfree` تنظیم شود.

گزینه پیکربندی `cudaSupport` توسط بسته‌ها برای فعال‌سازی شرطی قابلیت‌های مخصوص CUDA استفاده می‌شود. این گزینه پیکربندی معمولاً توسط بسته‌هایی استفاده می‌شود که می‌توانند با یا بدون پشتیبانی از CUDA ساخت (Build) شوند.

گزینه پیکربندی `cudaCapabilities` فهرستی از قابلیت‌های CUDA را مشخص می‌کند. بسته‌ها ممکن است از این گزینه برای کنترل تولید کد دستگاه استفاده کنند تا از قابلیت‌های مخصوص معماری بهره‌مند شوند، زمان‌های کامپایل را با تولید کد کمتر برای دستگاه سرعت بخشند، یا حجم closure بسته‌ها را کاهش دهند. به عنوان مثال، می‌توانید برای پردازنده‌های گرافیکی Ada Lovelace با `cudaCapabilities = [ "8.9" ];` اقدام به ساخت کنید. اگر `cudaCapabilities` ارائه نشود، مقدار پیش‌فرض به‌ازای هر مجموعه بسته محاسبه می‌شود که از فهرست پردازنده‌های گرافیکی پشتیبانی‌شده توسط آن نسخه CUDA به‌دست می‌آید. لطفاً برای کارت‌های خاص به [supported GPUs](https://en.wikipedia.org/wiki/CUDA#GPUs_supported) مراجعه کنید. نگه‌دارندگان کتابخانه باید به [NVCC Docs](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/) و یادداشت‌های انتشار آن مراجعه کنند.

::: {.caution}
برخی از قابلیت‌های CUDA به طور پیش‌فرض هدف‌گیری نمی‌شوند، از جمله قابلیت‌های متعلق به خانواده دستگاه‌های Jetson (به عنوان مثال `8.7` که مربوط به Jetson Orin است) یا مجموعه‌ویژگی‌های غیر پایه (به عنوان مثال `9.0a` که مربوط به مجموعه ویژگی‌های اختصاصی Hopper است). اگر نیاز دارید این قابلیت‌ها را هدف‌گیری کنید، باید به صراحت `cudaCapabilities` را طوری تنظیم کنید که آن‌ها را شامل شود.
:::

گزینه پیکربندی بولین `cudaForwardCompat` تعیین می‌کند که آیا پشتیبانی PTX برای سخت‌افزارهای آینده فعال است یا خیر.

### تغییر مجموعه‌های بسته CUDA {#cuda-modifying-cuda-package-sets}

مجموعه‌های بسته CUDA در `pkgs/top-level/cuda-packages.nix` تعریف شده‌اند. یک مجموعه بسته CUDA با فراخوانی `callPackage` روی `pkgs/development/cuda-modules/default.nix` همراه با یک مجموعه ویژگی به نام `manifests` ایجاد می‌شود که شامل مانیفست‌های NVIDIA برای هر فایل قابل توزیع مجدد است. مانیفست‌های مربوط به موارد قابل توزیع مجددِ پشتیبانی‌شده از طریق `_cuda.manifests` در دسترس هستند و در مسیر `pkgs/development/cuda-modules/_cuda/manifests` قرار دارند.

اکثریت ابزارهای مجموعه بسته CUDA از طریق مجموعه ویژگی سطح بالای `_cuda` در دسترس هستند، که یک نقطه ثابت (fixed-point) تعریف‌شده در خارج از مجموعه‌های بسته CUDA است. به عنوان یک نقطه ثابت، `_cuda` باید از طریق صفت `extend` خود تغییر داده شود.

::: {.caution}
همان‌طور که از پیشوند خط زیرین مشخص است، `_cuda` جزئیات پیاده‌سازی است و هیچ تضمینی در رابطه با پایداری یا API آن ارائه نمی‌شود. مجموعه ویژگی `_cuda` صرفاً برای تسهیل ایجاد یا تغییر مجموعه‌های بسته CUDA توسط کاربران متخصص خارج از درخت (out-of-tree) ارائه شده است.
:::

تغییرات خارج از درخت بسته‌ها باید از `overrideAttrs` برای اعمال هرگونه تغییر لازم در عبارت بسته استفاده کنند.

::: {.note}
مجموعه ویژگی `_cuda` قبلاً `fixups` را ارائه می‌داد، که یک مجموعه ویژگی برای نگاشت نام بسته (`pname`) به یک عبارت سازگار با `callPackage` بود و آن را به `overrideAttrs` روی نتیجه یک سازنده (builder) عمومی قابل توزیع مجدد ارائه می‌داد. این قابلیت به نفع گنجاندن عبارت‌های کامل بسته برای هر بسته قابل توزیع مجدد حذف شده است تا از عضویت سازگار در مجموعه ویژگی در سراسر نسخه‌ها، پلتفرم‌ها و پیکربندی‌های پشتیبانی‌شده CUDA اطمینان حاصل شود.
:::

### گسترش مجموعه‌های بسته CUDA {#cuda-extending-cuda-package-sets}

مجموعه‌های بسته CUDA دارای اسکوپ (scope) هستند و صفت معمول `overrideScope` را برای بازنشانی صفات بسته ارائه می‌دهند (یادداشت مربوط به `_cuda` در [پیکربندی مجموعه‌های بسته CUDA](#cuda-modifying-cuda-package-sets) را ببینید).

با الهام از `pythonPackagesExtensions`، صفت `_cuda.extensions` فهرستی از افزونه‌ها است که روی تمامی نسخه‌های مجموعه بسته‌های CUDA اعمال می‌شود، و امکان تغییر همهٔ نسخه‌های مجموعه بسته‌های CUDA را بدون نیاز به دانستن نام آن‌ها یا شمارش و تغییر صریح آن‌ها فراهم می‌سازد. به‌عنوان مثال، غیرفعال کردن `cuda_compat` در تمامی مجموعه بسته‌های CUDA با این اورلی امکان‌پذیر است:

```nix
final: prev: {
  _cuda = prev._cuda.extend (
    _: prevAttrs: {
      extensions = prevAttrs.extensions ++ [ (_: _: { cuda_compat = null; }) ];
    }
  );
}
```

بسته‌های قابل توزیع مجدد توسط کمک‌رسان ساخت `buildRedist` ساخته می‌شوند؛ برای مشاهده‌ی پیاده‌سازی، `pkgs/development/cuda-modules/buildRedist/default.nix` را ببینید.

### استفاده از `cudaPackages` {#cuda-using-cudapackages}

::: {.caution}
مقدار غیربدیهی از قابلیت کشف و قابلیت استفاده‌ی بسته‌های CUDA به قلاب‌های راه‌اندازی (setup hooks) گوناگونی متکی است که توسط یک مجموعه بسته‌ی CUDA استفاده می‌شوند. در نتیجه، کاربران احتمالاً هنگام تلاش برای انجام ساخت‌ها درون یک `devShell` بدون فراخوانی دستی فازها، با مشکل مواجه خواهند شد.
:::

برای استفاده از یک یا چند بسته CUDA در یک عبارت، یک پارامتر `cudaPackages` به عبارت بدهید و در صورتی که پشتیبانی از CUDA اختیاری باشد، پارامترهای `config` و `cudaSupport` را اضافه کنید:

```nix
{
  config,
  cudaSupport ? config.cudaSupport,
  cudaPackages,
}:
<package-expression>
```

در آرگومان‌های derivation بسته‌تان، _اکیداً_ توصیه می‌شود که موارد زیر تنظیم شوند:

```nix
{
  __structuredAttrs = true;
  strictDeps = true;
}
```

این تنظیمات تضمین می‌کنند که قلاب‌های راه‌اندازی CUDA طبق انتظار عمل کنند.

هنگام استفاده از `callPackage`، می‌توانید گونه‌ی دیگری را پاس دهید؛ برای مثال زمانی که یک بسته به نسخه خاصی از CUDA نیاز دارد:

```nix
{ mypkg = callPackage { cudaPackages = cudaPackages_12_6; }; }
```

::: {.caution}
بازنشانی مجموعه بسته‌ CUDA برای یک بسته ممکن است باعث ناسازگاری شود، زیرا این بازنشانی بر وابستگی‌های مستقیم یا گذرای آن تأثیری نمی‌گذارد. در نتیجه، به‌سادگی ممکن است بسته‌ای داشته باشید که از مجموعه بسته CUDA متفاوتی نسبت به وابستگی‌های خود استفاده می‌کند. در صورت امکان، توصیه می‌شود مجموعه بسته CUDA پیش‌فرض را به صورت سرتاسری تغییر دهید تا از یک محیط سازگار مطمئن شوید.
:::

### گونه‌های CUDA در Nixpkgs {#cuda-nixpkgs-cuda-variants}

گونه‌های CUDA در Nixpkgs در درجه اول برای سهولت در انتخاب بسته‌های دارای پشتیبانی از CUDA بر اساس مسیر صفت ارائه شده‌اند. به عنوان مثال، مجموعه گونه‌های CUDA Nixpkgs در `pkgsForCudaArch` به شما امکان می‌دهد با استفاده از مسیر صفت `pkgsForCudaArch.sm_89.opencv` به نمونه‌ای از OpenCV با پشتیبانی CUDA برای پردازنده گرافیکی Ada Lovelace دسترسی پیدا کنید، بدون اینکه نیازی به تغییر `config` ارائه‌شده هنگام درون‌ریزی Nixpkgs داشته باشید.

::: {.caution}
گونه‌های Nixpkgs بدون هزینه نیستند: آن‌ها نیاز به ارزیابی مجدد Nixpkgs دارند. در صورت امکان، Nixpkgs را یک‌بار با پیکربندی دلخواه درون‌ریزی کنید.
:::

#### استفاده از `cudaPackages.pkgs` {#cuda-using-cudapackages-pkgs}

هر مجموعه بسته CUDA دارای صفت `pkgs` است که گونه‌ای از Nixpkgs محسوب می‌شود که در آن مجموعه بسته CUDA دربرگیرنده به پیش‌فرض تبدیل می‌شود. این کار عمدتاً برای جلوگیری از نشت مجموعه بسته انجام شده است؛ جایی که یکی از اعضای مجموعه بسته CUDA غیرپیش‌فرض، وابستگی (احتمالاً گذرایی) به عضوی از مجموعه بسته CUDA پیش‌فرض داشته باشد.

::: {.note}
نشت مجموعه بسته یک مشکل رایج در Nixpkgs است و به مجموعه‌های بسته CUDA محدود نمی‌شود.
:::

به عنوان یک مزیت اضافی برای این نوع پیکربندی `pkgs`، ساخت یک بسته با نسخه‌ای غیرپیش‌فرض از CUDA به سادگیِ دسترسی به یک صفت (attribute) است. به عنوان مثال، `cudaPackages_12_8.pkgs.opencv` بسته OpenCV ساخت‌شده در برابر CUDA 12.8 را ارائه می‌دهد.

#### استفاده از `pkgsCuda` {#cuda-using-pkgscuda}

مجموعه ویژگی `pkgsCuda` گونه‌ای از Nixpkgs است که با `cudaSupport = true;` و `rocmSupport = false` پیکربندی شده است. این روش، راهکاری راحت برای دسترسی به گونه‌ای از Nixpkgs است که با مجموعه قابلیت‌های پیش‌فرض CUDA پیکربندی شده است.

#### استفاده از `pkgsForCudaArch` {#cuda-using-pkgsforcudaarch}

مجموعه ویژگی `pkgsForCudaArch` معمار‌ی‌های CUDA (مانند `sm_89` برای Ada Lovelace یا `sm_90a` برای معماری خاص Hopper) را به گونه‌های Nixpkgs نگاشت می‌کند که دقیقاً برای پشتیبانی از همان معماری پیکربندی شده‌اند. به عنوان مثال، `pkgsForCudaArch.sm_89` گونه‌ای از Nixpkgs است که `pkgs` را گسترش داده و مقادیر زیر را در `config` تنظیم می‌کند:

```nix
{
  cudaSupport = true;
  cudaCapabilities = [ "8.9" ];
  cudaForwardCompat = false;
}
```

::: {.note}
در `pkgsForCudaArch`، گزینهٔ `cudaForwardCompat` روی `false` تنظیم شده است زیرا واریانت مربوطه در Nixpkgs دقیقاً از یک معماری CUDA پشتیبانی می‌کند. به‌علاوه، برخی از معماری‌ها، از جمله مجموعه‌ویژگی‌های مختص به معماری مانند `sm_90a`، نمی‌توانند با قابلیت سازگاری رو به جلو (forward compatibility) ساخته شوند.
:::

::: {.caution}
همهٔ نسخه‌های CUDA از تمامی معماری‌ها پشتیبانی نمی‌کنند!

برای توضیح بیشتر: پشتیبانی از Blackwell (برای مثال `sm_100`) در CUDA 12.8 اضافه شد. فرض کنید مجموعه بسته‌های پیش‌فرض CUDA در Nixpkgs ما روی CUDA 12.6 باشد. در این صورت، واریانت Nixpkgs موجود از طریق `pkgsForCudaArch.sm_100` بی‌استفاده خواهد بود، زیرا بسته‌هایی مانند `pkgsForCudaArch.sm_100.opencv` و `pkgsForCudaArch.sm_100.python3Packages.torch` تلاش خواهند کرد کدی برای `sm_100` تولید کنند، معماری‌ای که برای CUDA 12.6 ناشناخته است. در آن صورت، باید در عوض از `pkgsForCudaArch.sm_100.cudaPackages_12_8.pkgs` استفاده کنید (برای جزئیات بیشتر به [استفاده از `cudaPackages.pkgs`](#cuda-using-cudapackages-pkgs) مراجعه کنید).
:::

مجموعه ویژگی `pkgsForCudaArch` دسترسی به بسته‌های ساخته‌شده برای یک معماری خاص را بدون نیاز به فراخوانی دستی `pkgs.extend` و ارائهٔ یک `config` جدید امکان‌پذیر می‌سازد. به عنوان نمونه، `pkgsForCudaArch.sm_89.python3Packages.torch` نرم‌افزار PyTorch ساخته‌شده برای پردازنده‌های گرافیکی Ada Lovelace را ارائه می‌دهد.

### اجرای کانتینرهای Docker یا Podman با پشتیبانی از CUDA {#cuda-docker-podman}

امکان اجرای کانتینرهای Docker یا Podman با پشتیبانی از CUDA وجود دارد. سازوکار پیشنهادی برای انجام این کار، استفاده از [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) است.

ابزار NVIDIA Container Toolkit را می‌توان در NixOS به صورت زیر فعال کرد:

```nix
{ hardware.nvidia-container-toolkit.enable = true; }
```

این کار به‌طور خودکار سرویسی را فعال می‌کند که بر اساس سخت‌افزار خودکار شناسایی‌شده‌ی ماشین شما، یک مشخصات CDI (واقع در `/var/run/cdi/nvidia-container-toolkit.json`) ایجاد می‌کند. می‌توانید این سرویس را با اجرای دستور زیر بررسی کنید:

```ShellSession
$ systemctl status nvidia-container-toolkit-cdi-generator.service
```

::: {.note}
بسته به تنظیماتی که قبلاً در سیستم خود فعال کرده‌اید، ممکن است لازم باشد ماشین خود را راه‌اندازی مجدد کنید تا NVIDIA Container Toolkit یک مشخصات CDI معتبر برای ماشین شما تولید کند.
:::

هنگامی که یک مشخصات CDI معتبر در زمان راه‌اندازی (بوت) برای ماشین شما تولید شد، هر دو Podman و Docker (> 25) در صورت ارائه‌ی پرچم `--device` از این مشخصات استفاده خواهند کرد:

```ShellSession
$ podman run --rm -it --device=nvidia.com/gpu=all ubuntu:latest nvidia-smi -L
GPU 0: NVIDIA GeForce RTX 4090 (UUID: <REDACTED>)
GPU 1: NVIDIA GeForce RTX 2080 SUPER (UUID: <REDACTED>)
```

```ShellSession
$ docker run --rm -it --device=nvidia.com/gpu=all ubuntu:latest nvidia-smi -L
GPU 0: NVIDIA GeForce RTX 4090 (UUID: <REDACTED>)
GPU 1: NVIDIA GeForce RTX 2080 SUPER (UUID: <REDACTED>)
```

می‌توانید با بررسی محتوای فایل `/var/run/cdi/nvidia-container-toolkit.json`، تمامی شناسه‌های ایجادشده برای سخت‌افزارِ به طور خودکار شناسایی‌شده‌ی خود را بررسی کنید:

```ShellSession
$ nix run nixpkgs#jq -- -r '.devices[].name' < /var/run/cdi/nvidia-container-toolkit.json
0
1
all
```

#### مشخص کردن دستگاه‌های قابل دسترس برای کنتینر {#cuda-specifying-what-devices-to-expose-to-the-container}

شما می‌توانید با استفاده از شناسه موجود در مشخصات CDI تولیدشده، انتخاب کنید که چه دستگاه‌هایی در معرض کنتینرهای شما قرار گیرند. به صورت زیر:

```ShellSession
$ podman run --rm -it --device=nvidia.com/gpu=0 ubuntu:latest nvidia-smi -L
GPU 0: NVIDIA GeForce RTX 4090 (UUID: <REDACTED>)
```

اگر چندین GPU دارید و می‌خواهید مشخص کنید کدام‌یک در دسترس کنتینر قرار گیرند، می‌توانید آرگومان `--device` را به هر تعداد که لازم است تکرار کنید:

```ShellSession
$ podman run --rm -it --device=nvidia.com/gpu=0 --device=nvidia.com/gpu=1 ubuntu:latest nvidia-smi -L
GPU 0: NVIDIA GeForce RTX 4090 (UUID: <REDACTED>)
GPU 1: NVIDIA GeForce RTX 2080 SUPER (UUID: <REDACTED>)
```

::: {.note}
به‌طور پیش‌فرض، NVIDIA Container Toolkit از اندیس GPU برای شناسایی دستگاه‌های مشخص استفاده می‌کند. شما می‌توانید نحوهٔ شناسایی دستگاه‌هایی که قرار است در دسترس قرار گیرند را با استفاده از صفت (attribute) NixOS به نام `hardware.nvidia-container-toolkit.device-name-strategy` تغییر دهید.
:::

#### استفاده از docker-compose {#cuda-using-docker-compose}

همچنین امکان در دسترس قرار دادن GPUها برای یک محیط `docker-compose` نیز وجود دارد. با یک فایل `docker-compose.yaml` مانند زیر:

```yaml
services:
  some-service:
    image: ubuntu:latest
    command: sleep infinity
    deploy:
      resources:
        reservations:
          devices:
          - driver: cdi
            device_ids:
            - nvidia.com/gpu=all
```

به همین ترتیب، می‌توانید دستگاه‌های خاصی را انتخاب کنید که در دسترس کنتینر قرار می‌گیرند:

```yaml
services:
  some-service:
    image: ubuntu:latest
    command: sleep infinity
    deploy:
      resources:
        reservations:
          devices:
          - driver: cdi
            device_ids:
            - nvidia.com/gpu=0
            - nvidia.com/gpu=1
```

## مشارکت {#cuda-contributing}

::: {.warning}
این بخش از مستندات هنوز به‌شدت در حال تکمیل است. بازخوردها در بخش GitHub Issues با تگ کردن @NixOS/cuda-maintainers یا در [Matrix](https://matrix.to/#/#cuda:nixos.org) پذیرفته می‌شود.
:::

### نگهداری مجموعه‌ی بسته‌ها {#cuda-package-set-maintenance}

مجموعه‌ابزار CUDA Toolkit مجموعه‌ای از کتابخانه‌ها و نرم‌افزارهای CUDA است که برای ارائه محیط توسعه جهت برنامه‌های شتاب‌یافته با CUDA در نظر گرفته شده است. تا پیش از انتشار CUDA 11.4، شرکت NVIDIA مجموعه CUDA Toolkit را تنها به صورت یک نصاب runfile چندگیگابایتی ارائه می‌کرد. از نسخه CUDA 11.4 به بعد، NVIDIA توزیع‌پذیرهای CUDA موسوم به («CUDA-redist») را نیز ارائه کرده است: قطعات مستقل بسته‌بندی‌شده از CUDA Toolkit که هدف آن‌ها تسهیل بازتوزیع و گنجاندن در پروژه‌های پایین‌دستی است. این بسته‌ها در مجموعه‌ی بسته‌های [`cudaPackages`](https://search.nixos.org/packages?channel=unstable&type=packages&query=cudaPackages) در دسترس هستند.

اگرچه نصاب یکپارچه runfile برای CUDA Toolkit دیگر ارائه نمی‌شود، [`cudaPackages.cudatoolkit`](https://search.nixos.org/packages?channel=unstable&type=packages&query=cudaPackages.cudatoolkit) یک تقریب پیوندیافته با `symlinkJoin` از کتابخانه‌های رایج را ارائه می‌دهد. استفاده از [`cudaPackages.cudatoolkit`](https://search.nixos.org/packages?channel=unstable&type=packages&query=cudaPackages.cudatoolkit) توصیه نمی‌شود: همه پروژه‌های جدید باید به جای آن از توزیع‌پذیرهای CUDA موجود در [`cudaPackages`](https://search.nixos.org/packages?channel=unstable&type=packages&query=cudaPackages) استفاده کنند، زیرا نگهداری و به‌روزرسانی آن‌ها بسیار آسان‌تر است.

#### به‌روزرسانی توزیع‌پذیرها {#cuda-updating-redistributables}

هر زمان که نسخه جدیدی از مانیفست توزیع‌پذیرها در دسترس قرار گرفت:

1. برای آدرس URL مورد استفاده هنگام vendor کردن مانیفست‌ها، فایل README.md مربوطه در `pkgs/development/cuda-modules/_cuda/manifests` را بررسی کنید.
2. نسخه مانیفست استفاده‌شده در ساخت هر مجموعه‌ی بسته‌های CUDA در `pkgs/top-level/cuda-packages.nix` را به‌روزرسانی کنید.
3. عبارت‌های بسته را در `pkgs/development/cuda-modules/packages` به‌روزرسانی کنید.

به‌روزرسانی عبارت‌های بسته شامل موارد زیر است:

- افزودن اصلاحات مشروط به انتشار نسخه‌های جدیدتر، مانند وابستگی‌های اضافه یا حذف شده
- افزودن عبارت‌های بسته برای بسته‌های جدید
- به‌روزرسانی `passthru.brokenConditions` و `passthru.badPlatformsConditions` با محدودیت‌های مختلف (به عنوان مثال، نسخه‌های جدیدی که پشتیبانی از معماری‌های مختلف را حذف می‌کنند)

#### به‌روزرسانی کامپایلرها و پردازنده‌های گرافیکی پشتیبانی‌شده {#cuda-updating-supported-compilers-and-gpus}

1. مقدار `nvccCompatibilities` در `pkgs/development/cuda-modules/_cuda/db/bootstrap/nvcc.nix` را به‌روزرسانی کنید تا شامل جدیدترین نسخه NVCC و همچنین هر کامپایلر هاستِ جدیداً پشتیبانی‌شده باشد.
2. مقدار `cudaCapabilityToInfo` در `pkgs/development/cuda-modules/_cuda/db/bootstrap/cuda.nix` را به‌روزرسانی کنید تا شامل هر GPU جدیدی باشد که توسط نسخه جدید CUDA پشتیبانی می‌شود.

#### به‌روزرسانی مجموعه‌ی بسته‌های CUDA {#cuda-updating-the-cuda-package-set}

::: {.note}
تغییر مجموعه‌ی بسته‌های پیش‌فرض CUDA باید در یک PR جداگانه انجام شود تا زمان کافی برای تست‌های اضافی فراهم باشد.
:::

::: {.warning}
همان‌طور که در [استفاده از `cudaPackages.pkgs`](#cuda-using-cudapackages-pkgs) توضیح داده شده است، راهکار پیاده‌سازی فعلی برای نشت مجموعه‌ی بسته‌ها شامل ایجاد یک نمونه جدید برای هر یک از مجموعه‌های بسته‌های غیرپیش‌فرض CUDA است. به همین دلیل، باید تعداد مجموعه‌بسته‌های CUDA که مقدار `recurseForDerivations` در آن‌ها برابر با true است را محدود کنیم: `lib.recurseIntoAttrs` تنها باید روی مجموعه‌ی بسته‌های پیش‌فرض CUDA اعمال شود.
:::

1. یک مجموعه بسته جدید `cudaPackages_<major>_<minor>` را در `pkgs/top-level/cuda-packages.nix` قرار داده و آن را در `pkgs/top-level/all-packages.nix` به ارث ببرید (inherit کنید).
2. بستار (closure) مجموعه بسته جدید را با موفقیت بسازید، و عبارت‌ها را در `pkgs/development/cuda-modules/packages` بر حسب نیاز به‌روزرسانی کنید. در ادامه برخی از خطاهای رایج آمده است:

| عدم توانایی در ... | در هنگام ... | علت | راه حل | نکته |
| -------------- | -------------------------------- | ------------------------------------------------ | -------------------------- | ------------------------------------------------------------ |
| یافتن هدرها | `configurePhase` یا `buildPhase` | نبود وابستگی به یک خروجی `dev` | افزودن وابستگی مفقود | خروجی `dev` معمولاً شامل هدرها است |
| یافتن کتابخانه‌ها | `configurePhase` | نبود وابستگی به یک خروجی `dev` | افزودن وابستگی مفقود | خروجی `dev` معمولاً شامل فایل‌های پیکربندی CMake است |
| یافتن کتابخانه‌ها | `buildPhase` یا `patchelf` | نبود وابستگی به یک خروجی `lib` یا `static` | افزودن وابستگی مفقود | خروجی `lib` یا `static` معمولاً شامل کتابخانه‌ها است |

::: {.note}
دو درایویشن کاربردی، تست به‌روزرسانی‌های مجموعه بسته را آسان‌تر می‌کنند:

- `cudaPackages.tests.redists-unpacked`: مقدار `src` هر بسته قابل توزیع مجدد که از حالت فشرده خارج شده و با `symlinkJoin` پیوند یافته است
- `cudaPackages.tests.redists-installed`: هر خروجی از هر بسته قابل توزیع مجدد که با `symlinkJoin` پیوند یافته است
:::

عدم موفقیت در اجرای باینری حاصل، معمولاً دشوارترین مورد برای دیباگ (اشکال‌زدایی) است، زیرا ممکن است ترکیبی از مشکلات ذکرشده در بالا باشد. این نوع شکست معمولاً زمانی رخ می‌دهد که یک کتابخانه تلاش می‌کند کتابخانه‌ای را که به آن وابسته است اما در بخش `DT_NEEDED` خود اعلام نکرده، بارگذاری یا باز کند. مراحل دیباگ (اشکال‌زدایی) زیر را امتحان کنید:

1. ابتدا مطمئن شوید که وابستگی‌ها با [`autoAddDriverRunpath`](https://search.nixos.org/packages?channel=unstable&type=packages&query=autoAddDriverRunpath) پچ شده‌اند.
2. در صورت عدم موفقیت، تلاش کنید برنامه را با [`nixGL`](https://github.com/guibou/nixGL) یا یک ابزار پوشش‌دهنده (wrapper) مشابه اجرا کنید.
3. اگر این کار جواب داد، احتمالاً به این معنی است که برنامه تلاش می‌کند کتابخانه‌ای را بارگذاری کند که در `RPATH` یا `RUNPATH` باینری وجود ندارد.

### نوشتن تست‌ها {#cuda-writing-tests}

::: {.caution}
وجود `passthru.testers` و `passthru.tests` باید به عنوان جزئیات پیاده‌سازی در نظر گرفته شود -- قرار نیست آن‌ها یک رابط عمومی یا پایدار باشند.
:::

به طور کلی، دو مجموعه صفت (attribute set) در `passthru` وجود دارد که برای ساخت و اجرای تست‌های بسته‌های CUDA استفاده می‌شوند: `passthru.testers` و `passthru.tests`. هر مجموعه صفت ممکن است شامل یک مجموعه صفت به نام `cuda` باشد که حاوی درایویشن‌های مخصوص CUDA است. مجموعه صفت `cuda` برای جداسازی درایویشن‌های مخصوص CUDA از درایویشن‌هایی استفاده می‌شود که از پیاده‌سازی‌های متعدد پشتیبانی می‌کنند (مانند OpenCL ،ROCm و غیره) یا مجوزهای متفاوتی دارند. برای نمونه‌ای از این درایویشن‌های عمومی، بسته `magma` را ببینید.

::: {.note}
درایویشن‌ها به دلیل یکی از رفتارهای عجیب OfBorg زیر صفت `cuda` قرار می‌گیرند: اگر ارزیابی شکست بخورد (مثلاً به دلیل مجوزهای غیرآزاد)، کل مجموعه صفت دربرگیرنده کنار گذاشته می‌شود. این امر از کشف، ارزیابی یا ساخت سایر صفات موجود در مجموعه جلوگیری می‌کند.
:::

#### `passthru.testers` {#cuda-passthru-testers}

صفات اضافه‌شده به `passthru.testers` درایویشن‌هایی هستند که یک فایل قابل اجرا برای انجام یک تست تولید می‌کنند. فایل قابل اجرای تولیدشده باید:

- تنظیم محیط، ایجاد پوشه‌های موقت و مواردی از این دست را انجام دهد.
- به‌عنوان `meta.mainProgram` درایویشن ثبت شود تا بتوان آن را مستقیماً اجرا کرد.

::: {.note}
تسترهایی که همیشه به CUDA نیاز دارند باید در `passthru.testers.cuda` قرار گیرند، در حالی که موارد عمومی باید در `passthru.testers` قرار داده شوند.
:::

مجموعه صفات `passthru.testers` امکان اجرای تست‌ها در خارج از محیط ایزوله (sandbox) Nix را فراهم می‌کند. دلایل متعددی برای مفید بودن این قابلیت وجود دارد، زیرا چنین تستی:

- هنگام استفاده در کنار ابزارهایی مانند `nixGL` یا `nix-gl-host` می‌تواند روی سیستم‌های غیر NixOS اجرا شود.
- دارای الگوهای دسترسی به شبکه است که ایزوله‌سازی آن‌ها دشوار یا غیرممکن است.
- می‌تواند خروجی‌هایی تولید کند که قطعی نیستند، مانند اطلاعات زمان‌بندی.

#### `passthru.tests` {#cuda-passthru-tests}

صفات اضافه‌شده به `passthru.tests` درایویشن‌هایی هستند که تست‌ها را داخل محیط ایزوله (sandbox) Nix اجرا می‌کنند. تست‌ها باید:

- در صورت امکان، از فایل‌های قابل اجرای تولیدشده توسط `passthru.testers` استفاده کنند تا از تکرار منطق تست جلوگیری شود.
- شامل `requiredSystemFeatures = [ "cuda" ];` باشند (اگر عمومی هستند، ترجیحاً مشروط به مقدار `cudaSupport`) تا اطمینان حاصل شود که فقط روی سیستم‌های دارای پردازنده گرافیکی با قابلیت پشتیبانی از CUDA اجرا می‌شوند.

::: {.note}
تست‌هایی که همیشه به CUDA نیاز دارند باید در `passthru.tests.cuda` قرار گیرند، در حالی که موارد عمومی باید در `passthru.tests` قرار داده شوند.
:::

این موضوع برای تست‌هایی مفید است که قطعی هستند (به عنوان مثال، بررسی کدهای خروج) و می‌توان تمام منابع لازم را در محیط ایزوله (sandbox) در اختیار آن‌ها قرار داد.
