# Autoconf {#setup-hook-autoconf}

درایویشن `autoreconfHook` فاز `autoreconfPhase` را اضافه می‌کند که ابزارهای autoreconf، libtoolize و automake را اجرا کرده و اساساً اسکریپت configure را در ساخت‌های مبتنی بر autotools آماده می‌سازد. اکثر بسته‌های مبتنی بر autotools همراه با اسکریپت configure از‌پیش‌تولیدشده عرضه می‌شوند، اما این قلاب برای برخی از بسته‌ها و هنگامی که نیاز به پچ کردن اسکریپت‌های configure بسته دارید، ضروری است.
