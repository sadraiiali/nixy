# 8.3.3. nix-store

## نام

`nix-store` - دستکاری یا پرس‌وجو در انبار نیکس (Nix store)

## خلاصه دستور
`nix-store` *operation* [*options…*] [*arguments…*]
  [`--option` *name* *value*]
  [`--add-root` *path*]

## توضیحات
دستور `nix-store` عملیات‌های پایه‌ای را روی انبار نیکس (Nix store) انجام می‌دهد.
معمولاً نیازی نیست این دستور را به صورت دستی اجرا کنید.

دستور `nix-store` دقیقاً یک پرچم *operation* دریافت می‌کند که نشان‌دهنده‌ی زیردستوری است که باید اجرا شود. عملیات‌های زیر در دسترس هستند:

- [`--realise`](/pages/nix-manual/command-ref/nix-store/realise)
- [`--serve`](/pages/nix-manual/command-ref/nix-store/serve)
- [`--gc`](/pages/nix-manual/command-ref/nix-store/gc)
- [`--delete`](/pages/nix-manual/command-ref/nix-store/delete)
- [`--query`](/pages/nix-manual/command-ref/nix-store/query)
- [`--add`](/pages/nix-manual/command-ref/nix-store/add)
- [`--add-fixed`](/pages/nix-manual/command-ref/nix-store/add-fixed)
- [`--verify`](/pages/nix-manual/command-ref/nix-store/verify)
- [`--verify-path`](/pages/nix-manual/command-ref/nix-store/verify-path)
- [`--repair-path`](/pages/nix-manual/command-ref/nix-store/repair-path)
- [`--dump`](/pages/nix-manual/command-ref/nix-store/dump)
- [`--restore`](/pages/nix-manual/command-ref/nix-store/restore)
- [`--export`](/pages/nix-manual/command-ref/nix-store/export)
- [`--import`](/pages/nix-manual/command-ref/nix-store/import)
- [`--optimise`](/pages/nix-manual/command-ref/nix-store/optimise)
- [`--read-log`](/pages/nix-manual/command-ref/nix-store/read-log)
- [`--dump-db`](/pages/nix-manual/command-ref/nix-store/dump-db)
- [`--load-db`](/pages/nix-manual/command-ref/nix-store/load-db)
- [`--print-env`](/pages/nix-manual/command-ref/nix-store/print-env)
- [`--generate-binary-cache-key`](/pages/nix-manual/command-ref/nix-store/generate-binary-cache-key)

این صفحات را می‌توان به صورت آفلاین مشاهده کرد:

- `man nix-store-&lt;operation&gt;`.

  مثال: `man nix-store-realise`

- `nix-store --help --&lt;operation&gt;`

  مثال: `nix-store --help --realise`
