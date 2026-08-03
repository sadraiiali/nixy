# 5.2.7. مسیر جستجو

> **نحو**
>
> *lookup-path* = `&lt;` *identifier* [ `/` *identifier* ]... `>`

یک مسیر جستجو عبارت است از یک شناسه با یک پسوند مسیر اختیاری که اگر شناسه با یک ورودی مسیر جستجو در [`builtins.nixPath`](/pages/nix-manual/language/builtins#builtins-nixPath) مطابقت داشته باشد، به یک [مقدار مسیر](/pages/nix-manual/language/types#type-path) تفکیک می‌شود.
الگوریتم تفکیک مسیر جستجو در مستندات مربوط به [`builtins.findFile`](/pages/nix-manual/language/builtins#builtins-findFile) شرح داده شده است.

> **مثال**
>

> ```nix
> <nixpkgs>
> ```
>
>     /nix/var/nix/profiles/per-user/root/channels/nixpkgs

> **مثال**
>

> ```nix
> <nixpkgs/nixos>
> ```
>
>     /nix/var/nix/profiles/per-user/root/channels/nixpkgs/nixos
