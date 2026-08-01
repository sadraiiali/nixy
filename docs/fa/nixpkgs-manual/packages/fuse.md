را بدون تعریف `FUSE_USE_VERSION` کامپایل کند.

    دو راه حل ممکن برای این مشکل در Nixpkgs وجود دارد:

    1. پاس دادن `FUSE_USE_VERSION` به اسکریپت configure با افزودن `CFLAGS=-DFUSE_USE_VERSION=25` در `configureFlags`. مقدار
