# <a id="juce-projucer-hook"></a> `juce.projucerHook`

[Projucer](https://juce.com/tutorials/tutorial_new_projucer_project/) یک ابزار گرافیکی مدیریت پروژه و سیستم ساخت برای چارچوب برنامه‌نویسی صوتی [JUCE](https://juce.com/) است. این ابزار در Nixpkgs تحت بسته `juce` در دسترس است.

قلاب راه‌اندازی `juce.projucerHook` فازهای پیکربندی و فاز نصب (installPhase) را بازنشانی می‌کند. این قلاب تنها در Linux پشتیبانی می‌شود و مستلزم آن است که فایل `.jucer` پروژه شما شامل یک صادرکننده `LinuxMakefile` باشد.

## <a id="juce-projucer-hook-example"></a> مثال

```nix
{
  juce,
  stdenv,
}:
stdenv.mkDerivation {
  # ...
  nativeBuildInputs = [ juce.projucerHook ];

  jucerFile = "Microbiome.jucer";

  dontUseProjucerInstall = true;
  # ...
}
```

## <a id="juce-projucer-hook-variables"></a> متغیرهای کنترل‌کننده `juce.projucerHook`

### `dontUseProjucerConfigure`

`projucerConfigurePhase` را غیرفعال می‌کند

### `dontUseProjucerInstall`

`projucerInstallPhase` را غیرفعال می‌کند
