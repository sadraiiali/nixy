# <a id="chap-platform-support"></a> پشتیبانی از پلتفرم

بسته‌ها درجه‌های مختلفی از پشتیبانی را دریافت می‌کنند، هم از نظر توجه نگه‌دارنده و تیم امنیت و هم از نظر منابع محاسباتی موجود برای ادغام مداوم (CI). ما ۷ سطح تعریف‌شده داریم که نشان می‌دهد هر پلتفرم تا چه حد پشتیبانی می‌شود.

## <a id="sec-platform-tiers"></a> سطح‌ها

### <a id="sec-platform-tier1"></a> سطح ۱

پلتفرم‌های [سطح ۱](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-1) بالاترین سطح پشتیبانی را دریافت می‌کنند که در آن مشکلات می‌توانند مانع انتشار به‌روزرسانی‌ها شوند، با اصلاحات امنیتی با فوریت برخورد می‌شود، پچ‌های مخصوص پلتفرم به‌راحتی اعمال می‌شوند و انتظار می‌رود اکثر بسته‌ها کار کنند.

### <a id="sec-platform-tier2"></a> سطح ۲

انتظار می‌رود پلتفرم‌های [سطح ۲](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-2) با دریافت به‌روزرسانی‌ها همچنان کاربردی و امن باقی بمانند، پچ‌های مخصوص پلتفرم را در صورت نیاز دریافت کنند و بسته‌های زیادی از آن‌ها توسط Hydra با پشتیبانی کامل ofBorg ساخته شوند.

### <a id="sec-platform-tier3"></a> سطح ۳

پلتفرم‌های [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) ممکن است اصلاحات غیرمزاحم مخصوص پلتفرم را دریافت کنند، ابزارهای بوت‌استرپ بومی را به همراه زنجیره‌ابزارهای ساخت متقاطع در کش باینری در دسترس داشته باشند، اما ممکن است به‌روزرسانی‌ها موجب شکست ساخت‌ها روی این پلتفرم‌ها شوند.

### <a id="sec-platform-tier4-7"></a> سطح ۴ تا ۷

سطوح پلتفرم [۴ تا ۷](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-4) نشان‌دهنده سطوح مختلفی از حداقل پشتیبانی هستند؛ از دریافت تنها اصلاحات محدود گرفته تا پلتفرم‌های بدون پشتیبانی، اما دارای مسیری مشخص برای دستیابی به پشتیبانی.

## <a id="sec-platform-breakdown"></a> تفکیک

| سه‌تایی | سطح پشتیبانی | مسدودکننده‌های کانال | پشتیبانی Hydra | پشتیبانی امنیتی | پشتیبانی Ofborg | تاربال‌های بوت‌استرپ | پشتیبانی کامپایل متقاطع |
|---------------------------------------|------------------------------------------------------------------------------------------------|------------------|---------------|------------------|----------------|--------------------|-------------------------|
| `x86_64-unknown-linux-gnu`            | [سطح ۱](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-1) | زیاد             | ✔️             | ✔️                | ✔️              | ✔️                  | ✔️                       |
| `aarch64-unknown-linux-gnu`           | [سطح ۲](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-2) | برخی             | ✔️             | ✔️                | ✔️              | ✔️                  | ✔️                       |
| `x86_64-unknown-linux-musl`           | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | محدود       | ❌               | ❌             | ✔️                  | ✔️                       |
| `aarch64-unknown-linux-musl`          | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | محدود       | ❌               | ❌             | ✔️                  | ✔️                       |
| `x86_64-unknown-unknown-freebsd`      | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `arm64-apple-darwin`                  | [سطح ۲](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-2) | برخی             | ✔️             | ✔️                | ✔️              | ✔️                  | ❌                      |
| `i686-unknown-linux-gnu`              | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | محدود       | ❌               | ❌             | ✔️                  | ✔️                       |
| `riscv32-unknown-linux-gnu`           | [سطح ۴](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-4) | هیچ             | ❌            | ❌               | ❌             | ❌                 | ✔️                       |
| `riscv64-unknown-linux-gnu`           | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `loongarch64-unknown-linux-gnu`       | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `armv6l-unknown-linux-gnueabihf`      | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `armv6l-unknown-linux-musleabihf`     | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `armv7l-unknown-linux-gnueabihf`      | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `armv5tel-unknown-linux-gnueabi`      | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `mips64el-unknown-linux-gnuabi64`     | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `mips64el-unknown-linux-gnuabin32`    | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `mipsel-unknown-linux-gnu`            | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `powerpc64-unknown-linux-gnuabielfv2` | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `powerpc64le-unknown-linux-gnu`       | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
| `s390x-unknown-linux-gnu`             | [سطح ۳](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md#tier-3) | هیچ             | ❌            | ❌               | ❌             | ✔️                  | ✔️                       |
