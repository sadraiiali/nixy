# کش باینری

فرمت کش باینری یک رابط است که برای انتشار یک انبار از طریق HTTP طراحی شده‌است.

یک کش باینری شامل موارد زیر است:

- یک فایل [`nix-cache-info`](./nix-cache-info.md) در ریشه حاوی پیکربندی سمت راه دور.
- برای هر [شیء انبار](@docroot@/store/store-object.md):
  - یک فایل [`.narinfo`](./narinfo.md) حاوی [متادیتای](@docroot@/store/store-object.md#metadata) شیء و یک URL (معمولاً نسبی) به فایل فشرده‌شدهٔ NAR متناظر.
  - یک [بایگانی نیکس](@docroot@/store/file-system-object/content-address.md#serial-nix-archive) احتمالاً فشرده‌شده که حاوی داده‌های سیستم‌فایل شیء انبار است.
- برای هر ورودی در [ردیابی ساخت](@docroot@/store/build-trace.md)، یک فایل JSON در مسیر `build-trace-v2/<drvBaseName>/<outputName>.doi`:
  - مسیر، [کلید](@docroot@/protocols/json/build-trace-entry.md#key) را کدگذاری می‌کند.
  - محتویات، [مقدار](@docroot@/protocols/json/build-trace-entry.md#value) هستند.

[انواع انبار](@docroot@/store/types/index.md) زیر از فرمت کش باینری استفاده می‌کنند:

- [انبار کش باینری HTTP](@docroot@/store/types/http-binary-cache-store.md)، ارائه شده از طریق HTTP(S)
- [انبار کش باینری محلی](@docroot@/store/types/local-binary-cache-store.md)، ذخیره‌شده روی سیستم‌فایل
- [انبار کش باینری S3](@docroot@/store/types/s3-binary-cache-store.md)، ذخیره‌شده در یک باکت AWS S3
