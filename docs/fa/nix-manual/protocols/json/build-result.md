{{#include build-result-v1-fixed.md}}

## مثال‌ها

### ساخت موفقیت‌آمیز

```json
{{#include schema/build-result-v1/success.json}}
```

### ساخت ناموفق (خروجی رد شد)

```json
{{#include schema/build-result-v1/output-rejected.json}}
```

### ساخت ناموفق (غیر قطعی)

```json
{{#include schema/build-result-v1/not-deterministic.json}}
```