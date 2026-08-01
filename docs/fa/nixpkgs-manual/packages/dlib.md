# DLib {#dlib}

[DLib](http://dlib.net/) یک مجموعه ابزار مدرن و مبتنی بر ++C است که الگوریتم‌های مختلفی برای یادگیری ماشین ارائه می‌دهد.

## کامپایل کردن بدون پشتیبانی از AVX {#compiling-without-avx-support}

به‌ویژه پردازنده‌های قدیمی‌تر از دستورالعمل‌های [AVX](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions) (افزونه‌های برداری پیشرفته) که DLib برای بهینه‌سازی الگوریتم‌های خود از آن‌ها استفاده می‌کند، پشتیبانی نمی‌کنند.

روی سخت‌افزار متأثر، خطاهایی مانند `Illegal instruction` رخ خواهد داد. در این موارد، پشتیبانی از AVX باید غیرفعال شود:

```nix
self: super: { dlib = super.dlib.override { avxSupport = false; }; }
```
