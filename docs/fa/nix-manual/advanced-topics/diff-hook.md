# بررسی بازتولیدپذیری ساخت

شما می‌توانید از تنظیم `diff-hook` در Nix برای مقایسه نتایج ساخت استفاده کنید. توجه داشته باشید که این قلاب تنها در صورتی اجرا می‌شود که نتایج با یکدیگر متفاوت باشند؛ و برای تعیین یکسان بودن نتایج استفاده نمی‌شود.

به‌منظور نمایش، از فایل Nix زیر، یعنی `deterministic.nix` برای آزمایش استفاده خواهیم کرد:

```nix
let
  inherit (import <nixpkgs> {}) runCommand;
in {
  stable = runCommand "stable" {} ''
    touch $out
  '';

  unstable = runCommand "unstable" {} ''
    echo $RANDOM > $out
  '';
}
```

علاوه بر این، `nix.conf` شامل موارد زیر است:

    diff-hook = /etc/nix/my-diff-hook
    run-diff-hook = true

که در آن `/etc/nix/my-diff-hook` یک فایل اجرایی است که شامل موارد زیر است:

```bash
#!/bin/sh
exec >&2
echo "For derivation $3:"
/run/current-system/sw/bin/diff -r "$1" "$2"
```

قلاب تفاوت (diff hook) توسط همان کاربر و گروهی اجرا می‌شود که ساخت را اجرا کرده‌اند.
با این حال، قلاب تفاوت به مسیر انبار که تازه ساخته شده‌است، دسترسی نوشتن ندارد.

# بررسی تصادفی قطعی بودن ساخت (Spot-Checking Build Determinism)

با ارسال پرچم `--check` به دستور ساخت، مسیری را که از قبل در انبار Nix وجود دارد، تأیید کنید.

اگر ساخت با موفقیت انجام شود و قطعی باشد، Nix با کد وضعیت 0 خارج می‌شود:

```console
$ nix-build ./deterministic.nix --attr stable
this derivation will be built:
  /nix/store/z98fasz2jqy9gs0xbvdj939p27jwda38-stable.drv
building '/nix/store/z98fasz2jqy9gs0xbvdj939p27jwda38-stable.drv'...
/nix/store/yyxlzw3vqaas7wfp04g0b1xg51f2czgq-stable

$ nix-build ./deterministic.nix --attr stable --check
checking outputs of '/nix/store/z98fasz2jqy9gs0xbvdj939p27jwda38-stable.drv'...
/nix/store/yyxlzw3vqaas7wfp04g0b1xg51f2czgq-stable
```

اگر ساخت قطعی نباشد، Nix با کد وضعیت ۱ خارج خواهد شد:

```console
$ nix-build ./deterministic.nix --attr unstable
this derivation will be built:
  /nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv
building '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv'...
/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable

$ nix-build ./deterministic.nix --attr unstable --check
checking outputs of '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv'...
error: derivation '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv' may
not be deterministic: output '/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable' differs
```

اکنون در لاگ خدمت پس‌زمینه (daemon) نیکس، موارد زیر را خواهیم دید:

```
For derivation /nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv:
1c1
< 8108
---
> 30204
```

استفاده از `--check` همراه با `--keep-failed` باعث می‌شود نیکس خروجی ساخت دوم را در یک مسیر خاص و با پسوند `.check` نگه دارد:

```console
$ nix-build ./deterministic.nix --attr unstable --check --keep-failed
checking outputs of '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv'...
note: keeping build directory '/tmp/nix-build-unstable.drv-0'
error: derivation '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv' may
not be deterministic: output '/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable' differs
from '/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable.check'
```

به‌ویژه، به خروجی `/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable.check` توجه کنید. نیکس نتایج ساخت را در آن پوشه کپی کرده‌است که می‌توانید آن را بررسی کنید.

> []{#check-dirs-are-unregistered} **نکته**
>
> مسیرهای بررسی در برابر جمع‌آوری زباله (garbage collection) محافظت نمی‌شوند و این مسیر در جریان جمع‌آوری زباله بعدی حذف خواهد شد.
>
> تضمین می‌شود که این مسیر در طول مدت زمان اجرای `diff-hook` زنده بماند، اما ممکن است پس از آن در هر زمانی حذف شود.
>
> اگر مقایسه به عنوان بخشی از ابزارهای خودکار انجام می‌شود، لطفاً از diff-hook استفاده کنید یا ابزار خود را به‌گونه‌ای بنویسید که حالتی را که در آن ساخت قطعی / reproducible از نظر نتیجه نبوده و مسیر بررسی نیز وجود ندارد، مدیریت کند.

سوئیچ `--check` تنها در صورتی قابل استفاده است که derivation از قبل روی سیستم ساخته شده باشد. اگر derivation ساخته نشده باشد، نیکس با خطای زیر متوقف خواهد شد:

    error: some outputs of '/nix/store/hzi1h60z2qf0nb85iwnpvrai3j2w7rr6-unstable.drv' 
    are not valid, so checking is not possible

فرآیند ساخت را بدون `--check` اجرا کنید و سپس دوباره با `--check` امتحان کنید.
