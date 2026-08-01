# <a id="sec-language-lean4"></a> Lean 4

زبان Lean 4 یک زبان تابعی اکید با نوع‌های وابسته است. `leanPackages` زنجیره ابزار و مجموعه‌ای دست‌چین‌شده از کتابخانه‌ها — شامل کل درخت وابستگی mathlib — را به همراه زنجیره ابزار Lean اختصاصی خود ارائه می‌دهد. یک کامپایلر مستقل نیز به عنوان `pkgs.lean4` برای استفاده در خارج از مجموعه بسته در دسترس است.

## <a id="lean4-buildLakePackage"></a> ساخت پروژه‌های Lean 4 با `buildLakePackage`

```nix
leanPackages.buildLakePackage {
  pname = "my-project";
  version = "0.1.0";
  src = ./.;
  leanDeps = with leanPackages; [ mathlib ];
  lakeHash = null; # all deps nix-managed; set to lib.fakeHash for Lake-managed deps
}
```

وابستگی‌ها برای Lake در lakefile و برای Nix در عبارت نیکس (Nix expression) اعلام می‌شوند. `leanDeps` کتابخانه‌های مدیریت‌شده توسط Nix را ارائه می‌دهد که فایل‌های `.olean` آن‌ها — فرآوردهٔ ساخت پیش‌فرض جنبه‌ی (facet

```json
{"version":"1.1.0","packagesDir":".lake/packages","packages":[]}
```

## <a id="lean4-dev-shells"></a> شل‌های توسعه

در `nix develop`، مقادیر داخل اسکوپ `lean4` و `buildLakePackage` همان زنجیره ابز

```nix
leanPackages.overrideScope (
  self: super: {
    lean4 = myCustomLean4;
  }
)
```

<a id="lean4-history"></a>

Paragraph 4:
Users familiar with the per-module derivation approach (2020–2025) should note that `buildLakePackage` follows a different architecture. The earlier integration discovered dependencies at evaluation time via import-from-derivation — an ambitious attempt to reconcile declarative package management with fine
