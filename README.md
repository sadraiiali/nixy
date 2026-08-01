# Nix notes

Two things live in this folder:

1. **Python pipeline** (`tools/`) — download, glossary, translate, and publish Markdown (via `uv`)
2. **SvelteKit + mdsvex site** (`src/`) — serves those notes in the browser

> Note: there is no npm package named `mdxserve`. This site uses **[mdsvex](https://mdsvex.pngwn.io/)** (Markdown / MDX preprocessor for Svelte), which is the usual Svelte equivalent.

## Website

```bash
npm install
npm run dev
```

Open (سایت **فقط فارسی** است):

| URL | Content |
|-----|---------|
| http://localhost:5173/ | خانه |
| http://localhost:5173/pages/how-nix-works | راهنمای «نیکس چگونه کار می‌کند» |

Production build (static → `build/`, for Cloudflare Pages):

```bash
npm run build
npm run preview
```

### Deploy to Cloudflare Pages

Requires [Wrangler](https://developers.cloudflare.com/workers/wrangler/) (installed as a devDependency) and a Cloudflare account.

```bash
npx wrangler login          # once
npm run deploy              # vite build → build/ then wrangler pages deploy
# or after a local build:
npm run pages:deploy
```

Config lives in `wrangler.jsonc`:

| Field | Value |
|-------|--------|
| Project name | `nix-notes` |
| Output dir | `build` |
| Framework | SvelteKit + `@sveltejs/adapter-static` |

**Git-connected Pages** (dashboard): Build command `npm run build`, build output directory `build`, Node version 20+.

**Local Pages preview** (after build):

```bash
npm run pages:dev
```

Webxdc offline packs stay separate (`npm run build:webxdc` → `build-webxdc/`).

The page is a mdsvex route:

`src/routes/pages/how-nix-works/+page.md`

(source copy of root `how-nix-works.md`).

## Makefile

```bash
make install     # uv sync + npm install
make download    # fetch English guide
make translate   # EN → FA (fenced code never sent to the model)
make dev         # SvelteKit dev server
make build
```

## Configuration (`.env`)

**All keys and settings** for download/translate live in `.env` (gitignored).

```bash
cp .env.example .env
# edit OPENAI_API_KEY, OPENAI_MODEL, paths, …
make env-check   # prints non-secret config
```

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | API secret (OpenRouter / OpenAI) |
| `OPENAI_BASE_URL` | API base URL |
| `OPENAI_MODEL` | e.g. `google/gemini-3.5-flash-lite` |
| `OPENAI_TEMPERATURE` | sampling temperature |
| `DOWNLOAD_URL` / `DOWNLOAD_OUTPUT` | scrape source & output path |
| `TRANSLATE_INPUT` / `TRANSLATE_OUTPUT` / `TRANSLATE_SITE` | translation paths |
| `TRANSLATE_TARGET_LANG` | default `fa` |

CLI flags still override paths when passed; otherwise scripts read only from `.env`.

## Staged pipeline (required order)

Full documents are **not** translated until you review the word list.

```text
1. Download docs (GitHub nix.dev first-steps)
2. Build unique tech glossary (no code)
3. API translates WORDS only → pending suggestions
4. YOU review/approve on /glossary-dev (dev only)
5. Full Markdown translation (approved glossary + no code to model)
```

```bash
make pipeline-words      # steps 1–3
make dev                 # http://localhost:5173/glossary-dev  → تأیید + ذخیره
                         # http://localhost:5173/glossary      → واژه‌نامهٔ نهایی (عمومی)
make translate-docs      # step 5 — docs/fa/first-steps/
```

| Make target | What it does |
|-------------|--------------|
| `download-first-steps` | `NixOS/nix.dev` → `docs/en/first-steps/` |
| `glossary` | tech terms → `glossary.json` |
| `glossary-suggest` | API fills term translations only (`status` stays pending) |
| `translate-docs` | full MD; uses **approved** glossary only; skips code fences |
| `translate` | legacy single-file helper |

### Gate

`translate-docs` needs at least `TRANSLATE_MIN_APPROVED` approved terms (default 1).
Set `TRANSLATE_REQUIRE_NO_PENDING=true` to require zero pending tech terms.

### Sources

- Web: https://nix.dev/tutorials/first-steps/
- Repo: https://github.com/NixOS/nix.dev (`source/tutorials/first-steps`)

## Re-download the guide

```bash
make download
# or:
uv sync
uv run python -m tools.download.page
cp how-nix-works.md src/routes/pages/how-nix-works/+page.md
```

## Layout

| Path | Purpose |
|------|---------|
| `Makefile` | install / download / translate / dev / build |
| `tools/` | Python pipeline (download → glossary → translate → publish); see `tools/README.md` |
| `docs/` | English + Farsi Markdown sources |
| `src/` | SvelteKit website |
| `how-nix-works.md` | English source (legacy single page) |
| `how-nix-works.fa.md` | Farsi translation (legacy) |
| `context/` | python-markdownify reference (not a dependency) |
| `.env` | API key (gitignored) |
