(attribute)``
- override -> بازنویسی / بازنشانی
- installing -> نصب / نصب کردن
- packages -> بسته‌ها
- manual -> راهنما
- python -> Python (stays Latin as product name / language)

```nix
(pkgs.krita.override (old: {
  binaryPlugins = old.binaryPlugins ++ [ your-plugin ];
}))
```

### <a id="krita-binary-plugin-structure"></a> نمونه ساختار یک افزونه باینری

```
/nix/store/00000000000000000000000000000000-krita-plugin-example-1.2.3
└── lib
   └── kritaplugins
      └── krita_example.so
```
