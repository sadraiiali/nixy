# `haredo` {#haredo-hook}

این قلاب از [اجراکننده دستور `haredo`](https://sr.ht/~autumnull/haredo/) برای ساخت، بررسی و نصب بسته استفاده می‌کند. این قلاب به صورت پیش‌فرض `buildPhase`، `checkPhase` و `installPhase` را بازنویسی می‌کند.

اگر [`enableParallelBuilding`](#var-stdenv-enableParallelBuilding) روی `true` تنظیم شده باشد، این قلاب هدف‌های خود را به صورت موازی می‌سازد.

## `buildPhase` {#haredo-hook-buildPhase}

این فاز برای ساخت هدف پیش‌فرض تلاش می‌کند.

[]{#haredo-hook-haredoBuildTargets} هدف‌ها را می‌توان با افزودن یک رشته به فهرست `haredoBuildTargets` به طور صریح مشخص کرد.

[]{#haredo-hook-dontUseHaredoBuild} این رفتار را می‌توان با تنظیم `dontUseHaredoBuild` روی `true` غیرفعال کرد.

## `checkPhase` {#haredo-hook-checkPhase}

این فاز به دنبال هدف‌های `check.do` یا `test.do` می‌گردد و در صورت وجود، آن‌ها را اجرا می‌کند.

[]{#haredo-hook-haredoCheckTargets} هدف‌ها را می‌توان با افزودن یک رشته به فهرست `haredoCheckTargets` به طور صریح مشخص کرد.

[]{#haredo-hook-dontUseHaredoCheck} این رفتار را می‌توان با تنظیم `dontUseHaredoCheck` روی `true` غیرفعال کرد.

## `installPhase` {#haredo-hook-installPhase}

این فاز در صورت وجود هدف `install.do`، برای ساخت آن تلاش می‌کند.

[]{#haredo-hook-haredoInstallTargets} هدف‌ها را می‌توان با افزودن یک رشته به فهرست `haredoInstallTargets` به طور صریح مشخص کرد.

[]{#haredo-hook-dontUseHaredoInstall} این رفتار را می‌توان با تنظیم `dontUseHaredoInstall` روی `true` غیرفعال کرد.
