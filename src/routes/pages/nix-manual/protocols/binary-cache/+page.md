# 10.4. کش باینری

فرمت کش باینری یک رابط است که برای انتشار یک انبار از طریق HTTP طراحی شده است.

یک کش باینری شامل موارد زیر است:

- یک فایل [`nix-cache-info`](/pages/nix-manual/protocols/binary-cache/nix-cache-info) در ریشه حاوی پیکربندی سمت راه دور.
- برای هر [شیء انبار](/pages/nix-manual/store/store-object):
  - یک فایل [`.narinfo`](/pages/nix-manual/protocols/binary-cache/narinfo) حاوی [متادیتای](/pages/nix-manual/store/store-object#metadata) شیء و یک URL (معمولاً نسبی) به فایل فشرده‌شده‌ی NAR متناظر.
  - یک [بایگانی نیکس](/pages/nix-manual/store/file-system-object/content-address#serial-nix-archive) احتمالاً فشرده‌شده که حاوی داده‌های سیستم‌فایل شیء انبار است.
- برای هر ورودی در [ردیابی ساخت](/pages/nix-manual/store/build-trace)، یک فایل JSON در مسیر `build-trace-v2/&lt;drvBaseName&gt;/&lt;outputName&gt;.doi`:
  - مسیر، [کلید](/pages/nix-manual/protocols/json/build-trace-entry#key) را کدگذاری می‌کند.
  - محتویات، [مقدار](/pages/nix-manual/protocols/json/build-trace-entry#value) هستند.

[انواع انبار](/pages/nix-manual/store/types) زیر از فرمت کش باینری استفاده می‌کنند:

- [انبار کش باینری HTTP](/pages/nix-manual/store/types/http-binary-cache-store) — ارائه شده از طریق HTTP(S)
- [انبار کش باینری محلی](/pages/nix-manual/store/types/local-binary-cache-store) — ذخیره‌شده روی سیستم‌فایل
- [انبار کش باینری S3](/pages/nix-manual/store/types/s3-binary-cache-store) — ذخیره‌شده در یک باکت AWS S3
