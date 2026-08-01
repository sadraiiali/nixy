# فرمت `nix-cache-info`

فایل `nix-cache-info` یک فایل فراداده (metadata) در ریشه یک [کش باینری](@docroot@/protocols/binary-cache/index.md) است (مثلاً `https://cache.example.com/nix-cache-info`).

نوع MIME: `text/x-nix-cache-info`

## فرمت

فرمت نام-مقدار خط‌گرا:

```
Key: value
```

فضای خالی ابتدا و انتهای مقادیر حذف می‌شود.
خطوط فاقد علامت دونقطه (colon) نادیده گرفته می‌شوند.
کلیدهای ناشناخته بدون سر و صدا نادیده گرفته می‌شوند.

## فیلدها

### `StoreDir`

مسیر پوشه انبار Nix که این کش برای آن ساخته شده‌است (به‌عنوان مثال، `/nix/store`).

در صورت وجود، Nix بررسی می‌کند که این مقدار با پوشه انبار کاربر (Client) مطابقت داشته باشد:

```
error: binary cache 'https://example.com' is for Nix stores with prefix '/nix/store', not '/home/user/nix/store'
```

### `WantMassQuery`

`1` یا `0`. مقدار پیش‌فرض را برای [`want-mass-query`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-want-mass-query) تنظیم می‌کند.

### `Priority`

عدد صحیح. مقدار پیش‌فرض را برای [`priority`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-priority) تنظیم می‌کند.

## مثال

```
StoreDir: /nix/store
WantMassQuery: 1
Priority: 30
```

## رفتار کش

نکیس (`nix`) اطلاعات `nix-cache-info` را در [پوشه کش](@docroot@/command-ref/env-common.md#env-NIX_CACHE_HOME) با مدت‌زمان اعتبار (TTL) ۷ روزه کش می‌کند.

## هم چنین ببینید

- [انبار کش باینری HTTP](@docroot@/store/types/http-binary-cache-store.md)
- [سرو کردن یک انبار Nix از طریق HTTP](@docroot@/package-management/binary-cache-substituter.md)
- [`substituters`](@docroot@/command-ref/conf-file.md#conf-substituters)
