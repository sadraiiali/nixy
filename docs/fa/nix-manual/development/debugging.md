# دیباگ (اشکال‌زدایی) Nix

این بخش نحوه ساخت و دیباگ (اشکال‌زدایی) Nix را با فعال بودن نمادهای دیباگ نشان می‌دهد.

علاوه بر این، برای دستورالعمل‌های بیشتر دربارهٔ نحوه دیباگ (اشکال‌زدایی) Nix در زمینه یک تست واحد یا تست کاربردی، به [آزمایش Nix](./testing.md) مراجعه کنید.

## ساخت Nix با نمادهای دیباگ

در شل توسعه، گزینه `mesonBuildType` به طور خودکار روی `debugoptimized` تنظیم می‌شود. این کار Nix را با نمادهای دیباگ می‌سازد که برای دیباگ (اشکال‌زدایی) مؤثر ضروری هستند.

همچنین امکان ساخت بدون بهینه‌سازی برای ساخت سریع‌تر وجود دارد:

```console
[nix-shell]$ NIX_HARDENING_ENABLE=$(printLines $NIX_HARDENING_ENABLE | grep -v fortify)
[nix-shell]$ export mesonBuildType=debug
```

(اولین خط به این دلیل لازم است که سخت‌سازی `fortify` حداقل به مقداری بهینه‌سازی نیاز دارد.)

## ساخت Nix با ابزارهای پاکسازی (Sanitizers)

Nix را می‌توان با استفاده از LLVM یا GCC همراه با ابزارهای پاکسازی [Address](https://clang.llvm.org/docs/AddressSanitizer.html) و [UB](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) ساخت. این کار هنگام اشکال‌زدایی مسائل مربوط به خرابی حافظه مفید است.

```console
[nix-shell]$ export mesonBuildType=debugoptimized
[nix-shell]$ appendToVar mesonFlags "-Dlibexpr:gc=disabled" # Disable Boehm
[nix-shell]$ appendToVar mesonFlags "-Db_sanitize=address,undefined"
```

## اشکال‌زدایی باینری Nix

دیباگر مورد علاقه خود را درون شل توسعه دریافت کنید:

```console
[nix-shell]$ nix-shell -p gdb
```

در macOS، از `lldb` استفاده کنید:

```console
[nix-shell]$ nix-shell -p lldb
```

### راه‌اندازی دیباگر

برای اشکال‌زدایی باینری Nix، دستور زیر را اجرا کنید:

```console
[nix-shell]$ gdb --args ../outputs/out/bin/nix
```

در macOS، از `lldb` استفاده کنید:

```console
[nix-shell]$ lldb -- ../outputs/out/bin/nix
```

### استفاده از دیباگر

در داخل دیباگر، می‌توانید نقاط شکست (breakpoints) را تنظیم کنید، برنامه را اجرا کنید و متغیرها را بازرسی کنید.

```gdb
(gdb) break main
(gdb) run <arguments>
```

برای دستورالعمل‌های جامع استفاده، به [مستندات GDB](https://www.gnu.org/software/gdb/documentation/) مراجعه کنید.

در macOS، از `lldb` استفاده کنید:

```lldb
(lldb) breakpoint set --name main
(lldb) process launch -- <arguments>
```

برای دستورالعمل‌های استفاده جامع، به [آموزش LLDB](https://lldb.llvm.org/use/tutorial.html) مراجعه کنید.
