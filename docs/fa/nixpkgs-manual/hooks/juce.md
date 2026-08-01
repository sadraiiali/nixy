# `juce.projucerHook` {#juce-projucer-hook}

[Projucer](https://juce.com/tutorials/tutorial_new_projucer_project/) یک ابزار گرافیکی مدیریت پروژه و سیستم ساخت برای چارچوب برنامه‌نویسی صوتی [JUCE](https://juce.com/) است. این ابزار در Nixpkgs تحت بسته `juce` در دسترس است.

قلاب راه‌اندازی `juce.projucerHook` فازهای پیکربندی و فاز نصب (installPhase) را بازنشانی می‌کند. این قلاب تنها در Linux پشتیبانی می‌شود و مستلزم آن است که فایل `.jucer` پروژه شما شامل یک صادرکننده `LinuxMakefile` باشد.

## مثال {#juce-projucer-hook-example}

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

## متغیرهای کنترل‌کننده `juce.projucerHook` {#juce-projucer-hook-variables}

### `dontUseProjucerConfigure`

`projucerConfigurePhase` را غیرفعال می‌کند

### `dontUseProjucerInstall`

`projucerInstallPhase` را غیرفعال می‌کند
