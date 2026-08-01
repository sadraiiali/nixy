## `manifest.json`

فایل مانیفست، منشأ (provenance) بسته‌هایی را که در یک [پروفایل](./profiles.md) مدیریت‌شده توسط [`nix profile`](@docroot@/command-ref/new-cli/nix3-profile.md) (تجربی) نصب شده‌اند، ثبت می‌کند.

در ادامه نمونه‌ای از ظاهر این فایل پس از نصب `zoom-us` از Nixpkgs آورده شده است:

```json
{
  "version": 1,
  "elements": [
    {
      "active": true,
      "attrPath": "legacyPackages.x86_64-linux.zoom-us",
      "originalUrl": "flake:nixpkgs",
      "storePaths": [
        "/nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927"
      ],
      "uri": "github:NixOS/nixpkgs/13d0c311e3ae923a00f734b43fd1d35b47d8943a"
    },
    …
  ]
}
```

هر شیء در آرایهٔ `elements` نمایانگر یک بستهٔ نصب‌شده است و دارای فیلدهای زیر می‌باشد:

* `originalUrl`: [مرجع فلیک](@docroot@/command-ref/new-cli/nix3-flake.md) مشخص‌شده توسط کاربر در زمان نصب (به‌عنوان‌مثال `nixpkgs`). این همان مرجع فلیک است که توسط `nix profile upgrade` استفاده خواهد شد.

* `uri`: مرجع فلیک قفل‌شده‌ای که `originalUrl` به آن حل شده است.

* `attrPath`: صفت خروجی فلیک که این بسته را فراهم کرده است. توجه داشته باشید که این لزوماً همان صفتی نیست که کاربر مشخص کرده است، بلکه صفتی است که از اعمال مسیرهای صفت پیش‌فرض و پیشوندها حاصل می‌شود؛ برای نمونه، `hello` ممکن است به `packages.x86_64-linux.hello` و رشتهٔ خالی به `packages.x86_64-linux.default` حل شود.

* `storePath`: مسیرهای موجود در انبار نیکس که شامل بسته هستند.

* `active`: اینکه آیا پروفایل حاوی پیوندهای نمادین به فایل‌های این بسته است یا خیر. اگر روی false تنظیم شود، بسته در انبار نیکس نگه داشته می‌شود، اما در درخت پیوند نمادین پروفایل «قابل‌مشاهده» نیست.
