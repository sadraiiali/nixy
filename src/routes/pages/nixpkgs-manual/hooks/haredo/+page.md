# <a id="haredo-hook"></a> `haredo`

این قلاب از [اجراکننده دستور `haredo`](https://sr.ht/~autumnull/haredo/) برای ساخت، بررسی و نصب بسته استفاده می‌کند. این قلاب به صورت پیش‌فرض `buildPhase`، `checkPhase` و `installPhase` را بازنویسی می‌کند.

اگر [`enableParallelBuilding`](#var-stdenv-enableParallelBuilding) روی `true` تنظیم شده باشد، این قلاب هدف‌های خود را به صورت موازی می‌سازد.

## <a id="haredo-hook-buildPhase"></a> `buildPhase`

این فاز برای ساخت هدف پیش‌فرض تلاش می‌کند.

<a id="haredo-hook-haredoBuildTargets"></a> هدف‌ها را می‌توان با افزودن یک رشته به فهرست `haredoBuildTargets` به طور صریح مشخص کرد.

<a id="haredo-hook-dontUseHaredoBuild"></a> این رفتار را می‌توان با تنظیم `dontUseHaredoBuild` روی `true` غیرفعال کرد.

## <a id="haredo-hook-checkPhase"></a> `checkPhase`

این فاز به دنبال هدف‌های `check.do` یا `test.do` می‌گردد و در صورت وجود، آن‌ها را اجرا می‌کند.

<a id="haredo-hook-haredoCheckTargets"></a> هدف‌ها را می‌توان با افزودن یک رشته به فهرست `haredoCheckTargets` به طور صریح مشخص کرد.

<a id="haredo-hook-dontUseHaredoCheck"></a> این رفتار را می‌توان با تنظیم `dontUseHaredoCheck` روی `true` غیرفعال کرد.

## <a id="haredo-hook-installPhase"></a> `installPhase`

این فاز در صورت وجود هدف `install.do`، برای ساخت آن تلاش می‌کند.

<a id="haredo-hook-haredoInstallTargets"></a> هدف‌ها را می‌توان با افزودن یک رشته به فهرست `haredoInstallTargets` به طور صریح مشخص کرد.

<a id="haredo-hook-dontUseHaredoInstall"></a> این رفتار را می‌توان با تنظیم `dontUseHaredoInstall` روی `true` غیرفعال کرد.
