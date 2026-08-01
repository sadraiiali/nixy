# Local icons & emoji

## Lucide

SVG files from [Lucide](https://lucide.dev) (ISC license), downloaded into this project — **no CDN**.

| Path | Purpose |
|------|---------|
| `static/icons/lucide/*.svg` | On-disk copies |
| `src/lib/icons/lucide/*.svg` | Imported by the app (`?raw`) |
| `src/lib/components/Icon.svelte` | `<Icon name="arrow-right" dir />` |

## Fluent UI Emoji

Microsoft [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) (**MIT**).

| Path | Purpose |
|------|---------|
| `static/icons/smiley.webp` | Home lead smiley (Slightly smiling face, 64px WebP) |
| `static/icons/fluentui-emoji/` | Fluent assets (smiley, light-bulb, memo, …) + `NOTICE.md` |

See `/licenses` in the site for full attribution.

Add more icons:

```bash
curl -sL "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/NAME.svg" \
  -o static/icons/lucide/NAME.svg
# normalize + copy into src/lib/icons/lucide, register in registry.ts
```
