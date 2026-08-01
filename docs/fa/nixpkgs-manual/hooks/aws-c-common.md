# `aws-c-common` {#aws-c-common}

این قلاب ماژول‌های [CMake](#cmake) خود را با تنظیم [`CMAKE_MODULE_PATH`](https://cmake.org/cmake/help/latest/variable/CMAKE_MODULE_PATH.html) روی پوشه غیراستاندارد `$out/lib/cmake` از طریق [متغیر `cmakeFlags`](#cmake-flags)، به عنوان راهکاری موقت برای [یک اشکال (Bug) بالادستی](https://github.com/awslabs/aws-c-common/issues/844) در دسترس قرار می‌دهد.
