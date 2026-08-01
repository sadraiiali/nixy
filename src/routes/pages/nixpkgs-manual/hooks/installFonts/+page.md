# <a id="installfonts"></a> `installFonts`

این قلاب، فرمت‌های رایج فونت را در مکان مناسب نصب می‌کند. در حالت پیش‌فرض، این قلاب به‌طور خودکار فرمت‌های ttf، ttc، otf، bdf و psf را مدیریت می‌کند. در صورت وجود خروجی `webfont`، فرمت‌های woff و woff2 تحت این خروجی نصب خواهند شد.

رفتار خودکار این قلاب را می‌توان با تنظیم متغیر `dontInstallFonts` روی true غیرفعال کرد.

علاوه بر این، تابع `installFont` را ارائه می‌دهد که می‌توان از آن در قلاب `postInstall` خود برای نصب فرمت‌های اضافی استفاده کرد:

## <a id="installfonts-installfont"></a> `installFont`

تابع `installFont` دو آرگومان می‌گیرد: یک پسوند فایل برای جابه‌جایی (*بدون* نقطه در ابتدای آن)، و مکان نصب.

### <a id="installfonts-installfont-exampleusage"></a> نمونه استفاده

```nix
{
  nativeBuildInputs = [ installFonts ];

  postInstall = ''
    installFont svg $out/share/fonts/svg
  '';
}
```
