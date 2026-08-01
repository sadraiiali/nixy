# pkgs.makeSetupHook {#sec-pkgs.makeSetupHook}

`pkgs.makeSetupHook` یک کمک‌رسان ساخت است که قلاب‌هایی تولید می‌کند که درون `nativeBuildInputs` قرار می‌گیرند.

## نحوه استفاده {#sec-pkgs.makeSetupHook-usage}

```nix
pkgs.makeSetupHook {
  name = "something-hook";
  propagatedBuildInputs = [ pkgs.commandsomething ];
  depsTargetTargetPropagated = [ pkgs.libsomething ];
} ./script.sh
```

### قلاب راه‌اندازی که به بسته hello وابسته است و hello را اجرا می‌کند و @shell@ با مسیر Bash جایگزین می‌شود {#sec-pkgs.makeSetupHook-usage-example}

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

## صفات {#sec-pkgs.makeSetupHook-attributes}

* `name` نام قلاب را تنظیم می‌کند.
* `propagatedBuildInputs` وابستگی‌های زمان اجرا (مانند باینری‌ها) برای قلاب.
* `depsTargetTargetPropagated` وابستگی‌های غیرباینری.
* `meta`
* `passthru`
* `substitutions` متغیرها برای `substituteAll`
