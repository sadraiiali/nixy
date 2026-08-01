# <a id="sec-language-hare"></a> Hare

## <a id="ssec-language-hare"></a> ساخت برنامه‌های Hare با `hareHook`

بسته `hareHook` محیط را برای ساخت برنامه‌های Hare با انجام موارد زیر آماده می‌کند:

1. تنظیم متغیرهای محیطی `HARECACHE` ،`HAREPATH` و `NIX_HAREFLAGS`؛
1. انتشار `harec` ،`qbe` و دو اسکریپت پوششی برای باینری hare.

این مانند برخی زبان‌های دیگر --- *برای مثال* Go یا Rust --- یک تابع نیست، بلکه بسته‌ای است که باید به `nativeBuildInputs` اضافه شود.

## <a id="hareHook-attributes"></a> صفات `hareHook`

صفات زیر توسط `hareHook` پذیرفته می‌شوند:

1. `hareBuildType`: یا `release` (پیش‌فرض) یا `debug`. این صفت کنترل می‌کند که آیا پرچم `-R` به `NIX_HAREFLAGS` اضافه می‌شود یا خیر.

## <a id="ex-hareHook"></a> مثالی برای `hareHook`

```nix
{
  hareHook,
  lib,
  stdenv,
}:
stdenv.mkDerivation {
  pname = "<name>";
  version = "<version>";
  src = "<src>";

  nativeBuildInputs = [ hareHook ];

  meta = {
    description = "<description>";
    inherit (hareHook) badPlatforms platforms;
  };
}
```

` را ارائه می‌دهد که یک wrapper به دور باینری hare برای استفاده از زنجیره‌ابزار نیتیو (`buildPlatform`) است.`

Wait, `hare-native` inside code back
