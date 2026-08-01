# <a id="sec-pkgs.makeSetupHook"></a> pkgs.makeSetupHook

`pkgs.makeSetupHook` یک کمک‌رسان ساخت است که قلاب‌هایی تولید می‌کند که درون `nativeBuildInputs` قرار می‌گیرند.

## <a id="sec-pkgs.makeSetupHook-usage"></a> نحوه استفاده

```nix
pkgs.makeSetupHook {
  name = "something-hook";
  propagatedBuildInputs = [ pkgs.commandsomething ];
  depsTargetTargetPropagated = [ pkgs.libsomething ];
} ./script.sh
```

### <a id="sec-pkgs.makeSetupHook-usage-example"></a> قلاب راه‌اندازی که به بسته hello وابسته است و hello را اجرا می‌کند و @shell@ با مسیر Bash جایگزین می‌شود

```nix
pkgs.makeSetupHook
  {
    name = "run-hello-hook";
    # Put dependencies here if they have hooks or necessary dependencies propagated
    # otherwise prefer direct paths to executables.
    propagatedBuildInputs = [
      pkgs.hello
      pkgs.cowsay
    ];
    substitutions = {
      shell = "${pkgs.bash}/bin/bash";
      cowsay = "${pkgs.cowsay}/bin/cowsay";
    };
  }
  (
    writeScript "run-hello-hook.sh" ''
      #!@shell@
      # the direct path to the executable has to be here because
      # this will be run when the file is sourced
      # at which point '$PATH' has not yet been populated with inputs
      @cowsay@ cow

      _printHelloHook() {
        hello
      }
      preConfigureHooks+=(_printHelloHook)
    ''
  )
```

## <a id="sec-pkgs.makeSetupHook-attributes"></a> صفات

* `name` نام قلاب را تنظیم می‌کند.
* `propagatedBuildInputs` وابستگی‌های زمان اجرا (مانند باینری‌ها) برای قلاب.
* `depsTargetTargetPropagated` وابستگی‌های غیرباینری.
* `meta`
* `passthru`
* `substitutions` متغیرها برای `substituteAll`
