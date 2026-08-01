# اجرای بنچمارک‌ها

این راهنما نحوه ساخت و اجرای بنچمارک‌های کارایی را در codebase نیکس توضیح می‌دهد.

## نمای کلی

نیکس از چارچوب [Google Benchmark](https://github.com/google/benchmark) برای تست کارایی استفاده می‌کند. بنچمارک‌ها به اندازه‌گیری و ردیابی کارایی عملیات حیاتی مانند تجزیه درایویشن کمک می‌کنند.

## ساخت بنچمارک‌ها

بنچمارک‌ها به‌طور پیش‌فرض غیرفعال هستند و باید در طول پیکربندی ساخت به‌طور صریح فعال شوند. برای دستیابی به نتایج دقیق، از یک ساخت release بهینه‌سازی‌شده برای اشکال‌زدایی استفاده کنید.

### راه‌اندازی محیط توسعه

ابتدا وارد شل توسعه شوید که شامل وابستگی‌های لازم است:

```bash
nix develop .#native-ccacheStdenv
```

### پیکربندی ساخت با بنچمارک‌ها

از پوشه ریشه پروژه، ساخت را با فعال‌سازی بنچمارک‌ها و بهینه‌سازی پیکربندی کنید:

```bash
cd build
meson configure -Dbenchmarks=true -Dbuildtype=debugoptimized
```

نوع ساخت `debugoptimized` موارد زیر را فراهم می‌کند:
- بهینه‌سازی‌های کامپایلر برای اندازه‌گیری‌های عملکردی واقع‌گرایانه
- نمادهای دیباگ (Debug symbols) برای پروفایل‌بندی و تحلیل
- تعادل بین عملکرد و قابلیت اشکال‌زدایی

### ساخت بنچمارک‌ها

پروژه را به همراه بنچمارک‌ها بسازید:

```bash
ninja
```

این کار فایل‌های اجرایی بنچمارک را در پوشه build ایجاد خواهد کرد. در حال حاضر موارد زیر در دسترس هستند:
- `build/src/libstore-tests/nix-store-benchmarks` - بنچمارک‌های عملکردی مربوط به انبار

با افزوده شدن بنچمارک‌های بیشتر به پایگاه کد، فایل‌های اجرایی بنچمارک اضافی نیز ایجاد خواهند شد.

## اجرای بنچمارک‌ها

### استفاده‌ی پایه

فایل‌های اجرایی بنچمارک را مستقیماً اجرا کنید. برای مثال، جهت اجرای بنچمارک‌های انبار:

```bash
./build/src/libstore-tests/nix-store-benchmarks
```

با اضافه شدن فایل‌های اجرایی بنچمارک بیشتر، آن‌ها را به همین شکل از پوشه‌های ساخت مربوطه خود اجرا کنید.

### فیلتر کردن بنچمارک‌ها

اجرای بنچمارک‌های خاص با استفاده از الگوهای عبارات باقاعده (regex):

```bash
# Run only derivation parser benchmarks
./build/src/libstore-tests/nix-store-benchmarks --benchmark_filter="derivation.*"

# Run only benchmarks for hello.drv
./build/src/libstore-tests/nix-store-benchmarks --benchmark_filter=".*hello.*"
```

### قالب‌های خروجی

نتایج بنچمارک را در قالب‌های مختلف تولید کنید:

```bash
# JSON output
./build/src/libstore-tests/nix-store-benchmarks --benchmark_format=json > results.json

# CSV output
./build/src/libstore-tests/nix-store-benchmarks --benchmark_format=csv > results.csv
```

### گزینه‌های پیشرفته

```bash
# Run benchmarks multiple times for better statistics
./build/src/libstore-tests/nix-store-benchmarks --benchmark_repetitions=10

# Set minimum benchmark time (useful for micro-benchmarks)
./build/src/libstore-tests/nix-store-benchmarks --benchmark_min_time=2

# Compare against baseline
./build/src/libstore-tests/nix-store-benchmarks --benchmark_baseline=baseline.json

# Display time in custom units
./build/src/libstore-tests/nix-store-benchmarks --benchmark_time_unit=ms
```

## نوشتن بنچمارک‌های جدید

برای اضافه کردن بنچمارک‌های جدید:

1. یک فایل `.cc` جدید در پوشه‌ی `*-tests` مناسب ایجاد کنید.
2. هدر بنچمارک را اضافه کنید:
```cpp
   #include <benchmark/benchmark.h>
   ```

۳. نوشتن توابع بنچمارک:
```cpp
   static void BM_YourBenchmark(benchmark::State & state)
   {
       // Setup code here

       for (auto _ : state) {
           // Code to benchmark
       }
   }
   BENCHMARK(BM_YourBenchmark);
   ```

۴. فایل را به `meson.build` مربوطه اضافه کنید:
```meson
   benchmarks_sources = files(
       'your-benchmark.cc',
       # existing benchmarks...
   )
   ```

## پروفایل کردن با بنچمارک‌ها

برای تحلیل عمیق‌تر عملکرد، بنچمارک‌ها را با ابزارهای پروفایل کردن ترکیب کنید:

```bash
# Using Linux perf
perf record ./build/src/libstore-tests/nix-store-benchmarks
perf report
```

### استفاده از Valgrind Callgrind

ابزار callgrind مربوط به Valgrind اطلاعات پروفایل‌سازی دقیقی را فراهم می‌کند که می‌توان آن‌ها را با kcachegrind مصورسازی کرد:

```bash
# Profile with callgrind
valgrind --tool=callgrind ./build/src/libstore-tests/nix-store-benchmarks

# Visualize the results with kcachegrind
kcachegrind callgrind.out.*
```

این موارد را فراهم می‌کند:
- گراف‌های فراخوانی توابع
- پروفایل‌سازی در سطح دستورالعمل
- حاشیه‌نویسی کد منبع
- تجسم تعاملی گلوگاه‌های عملکردی

## تست مداوم عملکرد

```bash
# Save baseline results
./build/src/libstore-tests/nix-store-benchmarks --benchmark_format=json > baseline.json

# Compare against baseline in CI
./build/src/libstore-tests/nix-store-benchmarks --benchmark_baseline=baseline.json
```

## عیب‌یابی

### ساخته نشوید بنچمارک‌ها / عدم ساخت بنچمارک‌ها

مطمئن شوید که بنچمارک‌ها فعال هستند:
```bash
meson configure build | grep benchmarks
# Should show: benchmarks true
```

### نتایج ناسازگار

- اطمینان حاصل کنید که سیستم شما تحت بار پردازشی سنگین قرار ندارد
- مقیاس‌پذیری فرکانس پردازنده را غیرفعال کنید تا نتایج سازگار داشته باشید
- بنچ‌مارک‌ها را چندین بار با استفاده از `--benchmark_repetitions` اجرا کنید

## همچنین ببینید

- [مستندات Google Benchmark](https://github.com/google/benchmark/blob/main/docs/user_guide.md)
