/xcrun`, `xcrun`, etc.)
- headers/APIs/libc++/LLVM/Darwin/Nixpkgs preserved correctly.

Everything looks solid and precise. Outputting Persian translation only.# نکات مربوط به پلتفرم {#chap-platform-notes}

## Darwin (macOS) {#sec-darwin}

`stdenv` در Darwin با بیشتر موارد دیگر در Nixpkgs در چند جنبه کلیدی تفاوت دارد.

##### استفاده از یک deployment target جدیدتر {#sec-darwin-libcxx-deployment-targets}

برای نحوه استفاده از یک deployment target جدیدتر، به ادامه متن مراجعه کنید.
به عنوان مثال، `std::print` به ویژگی‌هایی وابسته است که تنها در macOS 13.3 یا جدیدتر در دسترس هستند.
برای در دسترس قرار دادن آن‌ها، deployment target را با استفاده از `darwin

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  # ...
  buildInputs = [ apple-sdk_14 ];
}
```

#### «مقصد استقرار» (یا حداقل نسخه) چیست؟ {#sec-darwin-troubleshooting-using-deployment-targets}

«مقصد استقرار» به حداقل نسخه‌ای از macOS اشاره دارد که انتظار می‌رود برنامه‌ای را

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3"; # Upstream specifies the minimum supported version as 12.5.
  buildInputs = [ (darwinMinVersionHook "12.5") ];
}
```

نکته: امکان دارد چندین نمونه‌ی مختلف از `darwinMinVersionHook` در ورودی‌های شما وجود داشته باشد.
در این حالت، همواره نمونه‌ای که بالاترین نسخه را دارد استفاده می‌شود.

#### انتخاب یک نسخه SDK {#sec-darwin-troubleshooting-picking-sdk-version}

در ادامه فهرستی از

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  # ...
  nativeBuildInputs = [ bison ];
  buildCommand = ''
    xcrun bison foo.y # produces foo.tab.c
    # ...
  '';
}
```

#### بسته به `xcodebuild` نیاز دارد {#sec-darwin-troubleshooting-xcodebuild}

بسته xcbuild یک دستور `xcodebuild` برای بسته‌هایی که واقعاً

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  xcbuildFlags = [
    "-configuration"
    "Release"
    "-project"
    "libfoo-project.xcodeproj"
    "-scheme"
    "libfoo Package (macOS only)"
  ];
  __structuredAttrs = true;
}
```

##### اصلاح مسیرهای مطلق به `xcodebuild`، `xcrun` و `PlistBuddy` {#sec-darwin-troubleshooting-xcodebuild-absolute-paths}

بسیاری از سیستم‌های ساخت، مسیرهای مطلق به `xcodebuild`، `xcrun` و `PlistBuddy` را به ترتیب به صورت `/usr/bin/xcodebuild`، `/usr/bin/xcrun` و `/usr/libexec/PlistBuddy` به صورت هاردکدشده (hardcode) در نظر می‌گیرند.
در صورت استفاده از `xcodebuild` یا `PListBuddy`، این مسیرها باید با مسیرهای نسبی و بسته xcbuild جایگزین شوند.

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  postPatch = ''
    substituteInPlace Makefile \
      --replace-fail '/usr/bin/xcodebuild' 'xcodebuild' \
      --replace-fail '/usr/bin/xcrun' 'xcrun' \
      --replace-fail '/usr/bin/PListBuddy' 'PListBuddy'
  '';
}
```

` (Wait! NO! Never translate code inside backticks!) -> `iconv`
- `libiconv` -> `libiconv`
- `nativeBuildInputs` -> `nativeBuildInputs`
- `

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  # ...
  makeFlags = lib.optional stdenv.hostPlatform.isDarwin "LDFLAGS=-Wl,-install_name,$(out)/lib/libfoo.dylib";
}
```

##### تنظیم install name با استفاده از `install_name_tool` {#sec-darwin-troubleshooting-install-name-install_name_tool}

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  # ...
  postFixup = ''
    # `-id <install_name>` takes the install name. The last parameter is the path to the library.
    ${stdenv.cc.targetPrefix}install_name_tool -id "$out/lib/libfoo.dylib" "$out/lib/libfoo.dylib"
  '';
}
```

حتی اگر کتابخانه‌ها با استفاده از مسیرهای مطلق پیوند داده شده و از طریق install name خود به درستی حل و فصل شوند، تست‌ها در `checkPhase` گاهی اوقات ممکن است در اجرای باینری‌ها با شکست مواجه شوند، زیرا به کتابخانه‌هایی پیوند داده شده‌اند که هنوز نصب نشده‌اند.
این مشکل معمولاً با اجرای تست‌ها پس از `installPhase` یا با استفاده از `DYLD_LIBRARY_PATH`

- cross-compilation -> کامپایل متقاطع
- Linux -> Linux (rule 6: Product names stay Latin: Linux, macOS, etc.)
- dependencies -> وابستگی‌ها
- transitive dependencies -> وابستگی‌های متعدی
- compiler -> کامپایلر

```nix
stdenv.mkDerivation {
  name = "libfoo-1.2.3";
  # ...
  depsBuildBuild = [ buildPackages.stdenv.cc ];
  nativeBuildInputs = [ apple-sdk_12 ];
  buildInputs = [ apple-sdk_13 ];
  depsTargetTargetPropagated = [ apple-sdk_14 ];
}
# The build-build `clang` will use the 12.3 SDK while the package build itself will use the 13.3 SDK.
# Derivations that add this package as an input will have the 14.4 SDK propagated to them.
```

checking glossary again:
`host → هاست`
So "host platform" -> پلتفرم هاست
Let's check `build`:
`build → ساخت (Build)` (wait
