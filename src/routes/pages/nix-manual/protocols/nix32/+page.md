# 10.6. کدگذاری Nix32

کدگذاری Nix32 گونه‌ای از کدگذاری [Base32](https://en.wikipedia.org/wiki/Base32) در نیکس است که برای [خلاصه‌های مسیر انبار](/pages/nix-manual/protocols/store-path)، خروجی هش از طریق [`nix hash`](/pages/nix-manual/command-ref/new-cli/nix3-hash) و صفت درایویشن [`outputHash`](/pages/nix-manual/language/advanced-attributes#adv-attr-outputHash) استفاده می‌شود.

## الفبا

الفبای Nix32 از ۳۲ کاراکتر زیر تشکیل شده است:

```
0 1 2 3 4 5 6 7 8 9 a b c d f g h i j k l m n p q r s v w x y z
```

حروف `e`، `o`، `u` و `t` حذف شده‌اند.

## ترتیب بایت‌ها

کدگذاری Nix32 بایت‌های هش را از انتها (اولین بایت از آخر) پردازش می‌کند، در حالی که کدگذاری base-16 از ابتدا (اولین بایت از اول) پردازش را انجام می‌دهد.

در نتیجه، ترتیب مرتب‌سازی رشته‌ها در base-16 عمدتاً توسط بایت‌های اول و در Nix32 توسط بایت‌های آخر تعیین می‌شود.
