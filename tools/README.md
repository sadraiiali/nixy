# Python tooling (`tools/`)

Offline pipeline for this site: **download → glossary → translate → publish**.
The SvelteKit app under `src/` does not import these modules at runtime.

All secrets and paths live in the project-root `.env` (see `.env.example`).
Prefer Make targets from the repo root (`make download-nix-manual`, …).

## Layout

| Path | Role |
|------|------|
| `lib/` | Shared helpers (`envutil`, glossary I/O, tech lexicon, `fa_orthography` / `fa_bot`) |
| `download/` | Fetch nix.dev, Nix manual, Nixpkgs manual, Tour of Nix, single HTML pages |
| `glossary/` | Build / API-suggest / approve glossary terms |
| `translate/` | EN→FA Markdown (fenced code never sent to the model) |
| `publish/` | Write cleaned FA into `src/routes/pages/*`, tour JSON, page source map |

## Run as modules

From the project root (after `uv sync`):

```bash
uv run python -m tools.download.nix_manual
uv run python -m tools.glossary.build
uv run python -m tools.translate.docs
uv run python -m tools.publish.site_docs
uv run python -m tools.publish.page_source_map
uv run python -m tools.publish.tour_fa_json
```

### Persian orthography (`fa_bot`)

Port of fa.wikipedia [fa_bot.js `persianTools`](https://fa.wikipedia.org/wiki/ویکی‌پدیا:ویرایشگر_خودکار/ابرابزار/fa_bot.js), adapted for Markdown (code fences, inline code, URLs, and link targets are left alone). Wired into every translation path via `apply_fa_orthography`.

```bash
# fix docs/fa in place (default target)
uv run python -m tools.lib.fa_orthography

# dry-run / single file
uv run python -m tools.lib.fa_orthography --dry-run docs/fa
uv run python -m tools.lib.fa_orthography docs/fa/index.md
```

Project rules kept on top of the bot: always `ترجمه‌ی` (ZWNJ+yeh), and strip em/en dashes. Western digits are **not** converted (tech docs).

### Section-level re-translate (partial FA pages)

When a FA page is only partly translated, re-run **only** the English sections
without rewriting the whole file:

```bash
# list sections that still look English
uv run python -m tools.translate.docs --force --list-untranslated \
  --auto-untranslated docs/en/tutorials/packaging-existing-software.md

# auto-patch untranslated sections (Gemini 3.5 Flash Lite by default)
uv run python -m tools.translate.docs --force \
  --jobs-json tools/translate/jobs/packaging-existing-software.json

# or explicit EN heading titles:
uv run python -m tools.translate.docs --force --no-skip-existing \
  --model google/gemini-3.5-flash-lite \
  --sections "Missing dependencies,Finding packages,installPhase" \
  docs/en/tutorials/packaging-existing-software.md
```

Jobs JSON schema: `tools/translate/jobs.example.json`.
Then publish: `make publish-site` (or `uv run python -m tools.publish.site_docs`).

### Page source map

`tools/publish/page_source_map.py` builds a large JSON map of every site route
to its upstream GitHub blob and published web URL:

| Section | GitHub | Web |
|---------|--------|-----|
| `nix-dev` | [NixOS/nix.dev](https://github.com/NixOS/nix.dev) `source/` | https://nix.dev |
| `nix-manual` | [NixOS/nix](https://github.com/NixOS/nix) `doc/manual/source/` | https://nix.dev/manual/nix/stable |
| `nixpkgs-manual` | [NixOS/nixpkgs](https://github.com/NixOS/nixpkgs) `doc/` | https://nixos.org/manual/nixpkgs/stable |
| `how-nix-works` | — | https://nixos.org/guides/how-nix-works/ |

```bash
make page-source-map
# → src/lib/page-source-map.json  (~440 pages, route → { github, web, rel, … })
```

Or: `make help`.
