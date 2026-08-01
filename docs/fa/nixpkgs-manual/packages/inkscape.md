# Inkscape {#sec-inkscape}

[Inkscape](https://inkscape.org) یک ویرایشگر گرافیک برداری قدرتمند است.

## افزونه‌ها {#inkscape-plugins}
افزونه‌های Inkscape در مجموعه بسته‌های [`inkscape-extensions`](https://search.nixos.org/packages?channel=unstable&type=packages&query=cudaPackages) گردآوری شده‌اند.
برای فعال کردن آن‌ها، از یک بازنشانی روی `inkscape-with-extensions` استفاده کنید:

```nix
inkscape-with-extensions.override {
  inkscapeExtensions = with inkscape-extensions; [ inkstitch ];
}
```

به همین ترتیب، این در شل (Shell) نیز کار می‌کند:

```bash
$ nix-shell -p 'inkscape-with-extensions.override { inkscapeExtensions = with inkscape-extensions; [inkstitch]; }'
[nix-shell:~]$ # Ink/Stitch is now available via the extension menu
[nix-shell:~]$ inkscape
```

تمام افزونه‌های موجود را می‌توان با پاس دادن `inkscapeExtensions = null;` فعال کرد.

::: {.note}
بارگیری افزونه‌های Inkscape به صورت مستقل (بدون استفاده از `override`) هیچ تأثیری بر Inkscape نمی‌گذارد.
:::
