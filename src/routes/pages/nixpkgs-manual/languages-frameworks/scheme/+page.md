# <a id="sec-scheme"></a> Scheme

## <a id="sec-scheme-package-management"></a> مدیریت بسته

### <a id="sec-scheme-package-management-akku"></a> Akku

حدود دویست کتابخانه R6RS و R

```nix
{
  buildInputs = [
    chez
    akkuPackages.chez-srfi
  ];
}
```

فهرست بسته‌ها در `pkgs/tools/package-management/akku` به عنوان `deps.toml` قرار دارد و باید گاهی با اجرای `./update.sh` در این پوشه به‌روزرسانی شود. انجام این کار، URLهای سورس را برای بسته‌های جدید و نسخه‌های جدیدتر دریافت کرده و سپس آن‌ها را در فایل TOML می‌نویسد.
