# <a id="how-channels-work"></a> کانال‌ها چگونه کار می‌کنند

Nixpkgs از [قابلیت کانال‌ها](https://nixos.org/nix/manual/#sec-channels) در Nix استفاده می‌کند.

Nixpkgs برای کاربران Nix روی توزیع‌های غیر NixOS از طریق کانال `nixpkgs-unstable` توزیع می‌شود. کاربران NixOS عموماً از یکی از کانال‌های `nixos-*` استفاده می‌کنند، برای مثال `nixos-22.11` که شامل تمام بسته‌ها و ماژول‌ها برای نسخه پایدار NixOS 22.11 است. انتشارهای پایدار NixOS عموماً فقط به‌روزرسانی‌های امنیتی دریافت می‌کنند. بسته‌ها و ماژول‌های به‌روزتر از طریق کانال `nixos-unstable` در دسترس هستند.

هر دو کانال `nixos-unstable` و `nixpkgs-unstable` از شاخه `master` در مخزن Nixpkgs پیروی می‌کنند، اگرچه هر دو به طور کلی [چند روز](https://status.nixos.org/) از شاخه `master` عقب‌تر هستند. به‌روزرسانی‌های یک کانال به محض قبولی همه تست‌ها برای آن کانال توزیع می‌شوند؛ برای مثال [این جدول](https://hydra.nixos.org/job/nixpkgs/trunk/unstable#tabs-constituents) وضعیت تست‌ها را برای کانال `nixpkgs-unstable` نشان می‌دهد.

تست‌ها توسط کلاستری به نام [Hydra](https://nixos.org/hydra/) انجام می‌شوند که بسته‌های باینری را نیز از عبارت‌های Nix موجود در Nixpkgs برای `x86_64-linux`، `aarch64-linux`، `x86_64-darwin` و `aarch64-darwin` می‌سازد. باینری‌ها از طریق یک [کش باینری](https://cache.nixos.org) در دسترس قرار می‌گیرند.

عبارت‌های Nix فعلی کانال‌ها در [مخزن Nixpkgs](https://github.org/NixOS/nixpkgs) در شاخه‌هایی که متناظر با نام کانال‌ها هستند (مانند `nixos-22.11-small`) در دسترس قرار دارند.
