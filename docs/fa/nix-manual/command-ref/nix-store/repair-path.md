# نام

`nix --repair-path` - بارگذاری مجدد مسیر از جایگزین (substituter)

# خلاصه

`nix-store` `--repair-path` *paths…*

# توصیف

عملیات `--repair-path` تلاش می‌کند تا مسیرهای مشخص‌شده را با بارگذاری مجدد آن‌ها با استفاده از جایگزین‌های موجود «تعمیر» کند. اگر هیچ جایگزینی در دسترس نباشد، تعمیر امکان‌پذیر نیست.

> **هشدار**
>
> در طول فرآیند تعمیر، بازه زمانی بسیار کوچکی وجود دارد که طی آن مسیر قدیمی (در صورت وجود) به سمت دیگری منتقل شده و با مسیر جدید جایگزین می‌شود. اگر تعمیر در این بین متوقف شود، ممکن است سیستم در وضعیتی خراب رها شود (مثلاً اگر مسیر حاوی یک کامپوننت حیاتی سیستم مانند GNU C Library باشد).

# مثال

```console
$ nix-store --verify-path /nix/store/dj7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13
path `/nix/store/dj7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13' was modified!
  expected hash `2db57715ae90b7e31ff1f2ecb8c12ec1cc43da920efcbe3b22763f36a1861588',
  got `481c5aa5483ebc97c20457bb8bca24deea56550d3985cda0027f67fe54b808e4'

$ nix-store --repair-path /nix/store/dj7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13
fetching path `/nix/store/d7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13'...
…
```

