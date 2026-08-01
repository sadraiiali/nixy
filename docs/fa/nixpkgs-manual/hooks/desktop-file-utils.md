# desktop-file-utils {#desktop-file-utils}

این قلاب راه‌اندازی (setup hook)، کش MIME (واقع در `$out/share/applications/mimeinfo.cache`) را در `preFixupPhase` حذف می‌کند.

این قلاب به این دلیل ضروری است که با استفادهٔ یک بسته از `desktop-file-utils` ممکن است `mimeinfo.cache` ایجاد شود؛ در نتیجه اگر چند بستهٔ حاوی این فایل نصب شوند، باعث تداخل می‌شود (مانند آنچه در [#48295](https://github.com/NixOS/nixpkgs/issues/48295) آمده‌است).
