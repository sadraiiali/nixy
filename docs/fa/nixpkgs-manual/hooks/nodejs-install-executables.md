# nodejsInstallExecutables {#nodejs-install-executables}

قلابی برای کپسوله‌سازی برنامه‌های اجرایی Node.js.
عمدتاً برای یک محیط چندزبانه ایجاد شده است.

## مثال‌ها {#nodejs-install-executables-example}

[](#npm-build-hook-example-snippet)

## متغیرهای کنترل‌کننده `nodejsInstallExecutables` {#nodejs-install-executables-variables}

### متغیرهای اختصاصی `nodejsInstallExecutables` {#nodejs-install-executables-exclusive-variables}

#### `makeWrapperArgs` {#nodejs-install-executables-wrapper-args}

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
