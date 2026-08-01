# نام

`nix-store` - دستکاری یا پرس‌وجو در انبار نیکس (Nix store)

# خلاصه دستور

`nix-store` *operation* [*options…*] [*arguments…*]
  [`--option` *name* *value*]
  [`--add-root` *path*]

# توضیحات

دستور `nix-store` عملیات‌های پایه‌ای را روی انبار نیکس (Nix store) انجام می‌دهد.
معمولاً نیازی نیست این دستور را به صورت دستی اجرا کنید.

دستور `nix-store` دقیقاً یک پرچم *operation* دریافت می‌کند که نشان‌دهندهٔ زیردستوری است که باید اجرا شود. عملیات‌های زیر در دسترس هستند:

- [`--realise`](./nix-store/realise.md)
- [`--serve`](./nix-store/serve.md)
- [`--gc`](./nix-store/gc.md)
- [`--delete`](./nix-store/delete.md)
- [`--query`](./nix-store/query.md)
- [`--add`](./nix-store/add.md)
- [`--add-fixed`](./nix-store/add-fixed.md)
- [`--verify`](./nix-store/verify.md)
- [`--verify-path`](./nix-store/verify-path.md)
- [`--repair-path`](./nix-store/repair-path.md)
- [`--dump`](./nix-store/dump.md)
- [`--restore`](./nix-store/restore.md)
- [`--export`](./nix-store/export.md)
- [`--import`](./nix-store/import.md)
- [`--optimise`](./nix-store/optimise.md)
- [`--read-log`](./nix-store/read-log.md)
- [`--dump-db`](./nix-store/dump-db.md)
- [`--load-db`](./nix-store/load-db.md)
- [`--print-env`](./nix-store/print-env.md)
- [`--generate-binary-cache-key`](./nix-store/generate-binary-cache-key.md)

این صفحات را می‌توان به صورت آفلاین مشاهده کرد:

- `man nix-store-<operation>`.

  مثال: `man nix-store-realise`

- `nix-store --help --<operation>`

  مثال: `nix-store --help --realise`
