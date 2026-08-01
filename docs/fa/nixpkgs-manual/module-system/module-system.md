(attribute)`)
- flakes -> فلیک‌ها (Flakes)
- virtual machine / VM -> ماشین مجازی
- configuration -> پیکربندی
- options -> گزینه‌ها
- option -> گزینه

All rule checks pass. Ready to output.# سیستم ماژول {#module-system}

## مقدمه {#module-system-introduction}

سیستم ماژول زبانی برای مدیریت پیکربندی است که به عنوان یک کتابخانه Nix پیاده

تعاریف گزینه‌ای که با این نوع مشخص می‌شوند، مجموعه‌ی فعلی ماژول‌ها را گسترش خواهند داد، مانند [`extendModules`](#module-system-lib-evalModules-return-value-extendModules).

با این حال، مقدار بازگردانده‌شده از این نوع، درست مانند هر ماژول فرعی، صرفاً همان [`config`](#module-system-lib-evalModules-return-value-config)

آن‌ها از این منابع سرچشمه می‌گیرند:
1. آرگومان‌های توکار (Built-in)
    - `lib`,
    - `config`,
    - `options`,
    - `_class`,
    - `_prefix`,
2. صفات مربوط به آرگومان [`specialArgs`] که به
