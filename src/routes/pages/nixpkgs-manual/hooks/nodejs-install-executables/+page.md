# <a id="nodejs-install-executables"></a> nodejsInstallExecutables

قلابی برای کپسوله‌سازی برنامه‌های اجرایی Node.js.
عمدتاً برای یک محیط چندزبانه ایجاد شده است.

## <a id="nodejs-install-executables-example"></a> مثال‌ها

[](#npm-build-hook-example-snippet)

## <a id="nodejs-install-executables-variables"></a> متغیرهای کنترل‌کننده `nodejsInstallExecutables`

### <a id="nodejs-install-executables-exclusive-variables"></a> متغیرهای اختصاصی `nodejsInstallExecutables`

#### <a id="nodejs-install-executables-wrapper-args"></a> `makeWrapperArgs`

پرچم‌هایی که به فراخوانی [`makeWrapper`](#fun-makeWrapper) ارسال می‌شوند.
برای جلوگیری از کپسوله‌سازی دوباره، این پرچم در Bash نیز قابل دسترسی است.

```nix
stdenv.mkDerivation (finalAttrs: {
  #...
  dontWrapGApps = true;

  postInstall = ''
    makeWrapperArgs+=("''${gappsWrapperArgs[@]}")
  '';
  #...
})
```
