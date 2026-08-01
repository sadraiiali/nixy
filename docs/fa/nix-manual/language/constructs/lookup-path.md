# مسیر جستجو

> **نحو**
>
> *lookup-path* = `<` *identifier* [ `/` *identifier* ]... `>`

یک مسیر جستجو عبارت است از یک شناسه با یک پسوند مسیر اختیاری که اگر شناسه با یک ورودی مسیر جستجو در [`builtins.nixPath`](@docroot@/language/builtins.md#builtins-nixPath) مطابقت داشته باشد، به یک [مقدار مسیر](@docroot@/language/types.md#type-path) تفکیک می‌شود.
الگوریتم تفکیک مسیر جستجو در مستندات مربوط به [`builtins.findFile`](@docroot@/language/builtins.md#builtins-findFile) شرح داده شده‌است.

> **مثال**
>
```nix
> <nixpkgs>
>```
>
>     /nix/var/nix/profiles/per-user/root/channels/nixpkgs

> **مثال**
>
```nix
> <nixpkgs/nixos>
>```
>
> /nix/var/nix/profiles/per-user/root/channels/nixpkgs/nixos
