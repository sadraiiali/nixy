---
myst:
  html_meta:
    "description lang=fa": "ادغام مداوم با GitHub Actions و یک کش باینری"
    "keywords": "CI, ادغام مداوم, GitHub Actions, کش باینری, Nix"
---

(github-actions)=

# ادغام مداوم با GitHub Actions

پیکربندی [GitHub Actions](https://github.com/features/actions) به عنوان جریان کار ادغام مداوم (CI) برای کامیت‌ها و پول ریکوئست‌ها.

نیکس (Nix) به ادغام مداوم (CI) اجازه می‌دهد تا محیط‌های توسعه را برای هر پروژه و هر شاخه با استفاده از کش‌های باینری بسازد و ذخیره کند.

زمان ساخت یک متریک کلیدی در ادغام مداوم (CI) است. کاچیکس (Cachix) (در ادامه) ساده‌ترین گزینه برای کش کردن است.

## کش کردن ساخت‌ها با استفاده از Cachix

با استفاده از [Cachix](https://cachix.org/) هرگز مجبور نخواهید بود وقت خود را برای ساخت مجدد یک درایویشن تلف کنید، و درایویشن‌های ساخته‌شده را با تمام توسعه‌دهندگان خود به اشتراک خواهید گذاشت.

پس از هر کار (Job)، درایویشن‌های تازه‌ساخته‌شده به کش باینری شما ارسال (Push) می‌شوند.

پیش از هر کار، درایویشن‌هایی که باید ساخته شوند، ابتدا (در صورت وجود) از کش باینری شما جایگزین (substituted) می‌شوند.

### ۱. ایجاد نخستین کش باینری

توصیه می‌شود بسته به اینکه چه کسانی به آن دسترسی خواندن/نوشتن خواهند داشت، برای هر تیم کش‌های باینری متفاوتی داشته باشید.

فرم موجود در صفحه [ایجاد کش باینری](https://app.cachix.org/cache) را تکمیل کنید.

دستورالعمل‌های تب **Push binaries** را روی کش باینری تازه ایجادشدهٔ خود دنبال کنید.

### ۲. پیکربندی رمزها (Secrets)

در مخزن گیت‌هاب یا سازمان خود (برای استفاده در تمام مخازن):

۱. روی `Settings` کلیک کنید.
۲. روی `Secrets and variables` کلیک کرده و در فهرست کشویی روی `Actions` کلیک کنید.
۳. روی `New repository secret` کلیک کنید.
۴. رمزهای تولیدشدهٔ قبلی خود (`CACHIX_SIGNING_KEY` و/یا `CACHIX_AUTH_TOKEN`) را اضافه کنید.

### ۳. راه‌اندازی GitHub Actions

فایل `.github/workflows/test.yml` را با محتوای زیر ایجاد کنید:

```yaml
name: "Test"
on:
  pull_request:
  push:
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: cachix/install-nix-action@v25
      with:
        nix_path: nixpkgs=channel:nixos-unstable
    - uses: cachix/cachix-action@v14
      with:
        name: mycache
        # If you chose signing key for write access
        signingKey: '${{ secrets.CACHIX_SIGNING_KEY }}'
        # If you chose API tokens for write access OR if you have a private cache
        authToken: '${{ secrets.CACHIX_AUTH_TOKEN }}'
    - run: nix-build
    - run: nix-shell --run "echo OK"
```

هنگامی که تغییرات را کامیت کرده و به مخزن GitHub خود پوش (push) می‌کنید،
باید بررسی‌های وضعیت را روی کامیت‌ها و پول ریکوئست‌ها (PRها) مشاهده کنید.

## گام‌های بعدی

- [syntax مربوط به workflowهای GitHub Actions](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions) را ببینید.
- برای راه‌اندازی سریع یک پروژه Nix، [قالب شروع‌به‌کار Nix](https://github.com/nix-dot-dev/getting-started-nix-template) را مطالعه کنید.

[github-actions-caching-limits]: https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
