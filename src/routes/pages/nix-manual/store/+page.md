# 4. انبار Nix

*انبار نیکس* (*Nix store*) انتزاعی برای ذخیره‌سازی داده‌های تغییرناپذیر سیستم‌فایل (مانند بسته‌های نرم‌افزاری) است که می‌توانند به سایر داده‌های مشابه وابستگی داشته باشند.

به‌طور مشخص، هرچند با استفاده از مفاهیمی که تنها در ادامه این فصل تعریف می‌شوند، یک انبار شامل موارد زیر است:

- مجموعه‌ای از [اشیای انبار][store object]، که همان داده‌های تغییرناپذیر سیستم‌فایل هستند.

  همچنین می‌توان به این مورد به چشم نگاشتی از [مسیرهای انبار][store path] به اشیای انبار نگاه کرد.

- مجموعه‌ای از [درایویشن‌ها][derivation]، که دستورالعمل‌هایی برای ساخت اشیای انبار هستند.

  همچنین می‌توان به این مورد به چشم نگاشتی از [مسیرهای انبار][store path] به درایویشن‌ها نگاه کرد.
  از آنجا که مسیرهای انبار مربوط به درایویشن‌ها همیشه به `.drv` ختم می‌شوند و مسیرهای انبار مربوط به سایر اشیای انبار هرگز این‌گونه نیستند، این دو نگاشت را می‌توان با یکدیگر ترکیب کرد.
  درایویشن‌ها را نیز می‌توان به عنوان اشیای انبار کدگذاری کرد.

- یک [ردپای ساخت][build trace]، که سوابقی از درایویشن‌های ساخته‌شده و خروجی‌های آن‌هاست.

  > **هشدار**
  >
  > مفهوم ردپای ساخت در حال حاضر
  > [**آزمایشی**](/pages/nix-manual/development/experimental-features#xp-feature-ca-derivations)
  > است و ممکن است تغییر کند.

انواع مختلفی از [انبارهای نیکس][store type] با قابلیت‌های گوناگون وجود دارند؛ مانند انبار پیش‌فرض روی [سیستم‌فایل محلی][local store] (`/nix/store`) یا [کش‌های باینری][binary cache].

[store object]: /pages/nix-manual/store/store-object
[store path]: /pages/nix-manual/store/store-path
[derivation]: /pages/nix-manual/store/derivation
[build trace]: /pages/nix-manual/store/build-trace
[store type]: /pages/nix-manual/store/types
[local store]: /pages/nix-manual/store/types/local-store
[binary cache]: /pages/nix-manual/store/types/http-binary-cache-store
