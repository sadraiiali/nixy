# Nixy

Persian (Farsi) documentation site for [Nix](https://nixos.org/) and NixOS.

Nixy gathers official English material, runs it through a staged EN→FA translation pipeline, and publishes a fully Persian reading experience in the browser.

**Live site:** [nixy.a15d.at](https://nixy.a15d.at)  
**Repository:** [github.com/sadraiiali/nixy](https://github.com/sadraiiali/nixy)

## What’s included

| Section | Upstream | On the site |
|---------|----------|-------------|
| **nix.dev** | [NixOS/nix.dev](https://github.com/NixOS/nix.dev) | `/pages/nix-dev/…` |
| **Nix reference manual** | [NixOS/nix](https://github.com/NixOS/nix) `doc/manual` | `/pages/nix-manual/…` |
| **Nixpkgs manual** | [NixOS/nixpkgs](https://github.com/NixOS/nixpkgs) `doc/` | `/pages/nixpkgs-manual/…` |
| **How Nix works** | nixos.org guide | `/pages/how-nix-works` |
| **Tour of Nix** | [nixcloud/tour_of_nix](https://github.com/nixcloud/tour_of_nix) | `/pages/tour-of-nix` |
| **Blog** | local notes | `/blog/…` |
| **Glossary** | built from docs | `/glossary` |

The UI is **RTL Persian**. Upstream source links and contributor info appear on doc pages where mapped.

## Stack

Two main pieces live in this repo:

1. **SvelteKit + mdsvex site** (`src/`) — static site (Cloudflare Pages), Markdown routes, glossary, blog, agent discovery under `/.well-known/`.
2. **Python content pipeline** (`tools/`, via [`uv`](https://github.com/astral-sh/uv)) — download English sources, glossary, translate, publish into `src/routes/pages/`.

Orchestration is via the root **`Makefile`**. Secrets and paths go in **`.env`** (see `.env.example`).

## Website (dev & deploy)

```bash
npm install
npm run dev          # http://localhost:5173
```

Useful routes while developing:

| URL | Content |
|-----|---------|
| `/` | Home |
| `/pages/how-nix-works` | How Nix works |
| `/pages/nix-dev/…` | nix.dev (FA) |
| `/glossary` | Public glossary |
| `/glossary-dev` | Glossary review (dev) |
| `/settings` | Reader settings |
| `/licenses` | Licenses & attribution |

Production build (static output → `build/`):

```bash
npm run build
npm run preview
```

### Cloudflare Pages

Config: `wrangler.jsonc` (project `nixy`, output `build/`).

```bash
npx wrangler login    # once
npm run deploy        # build + deploy
# or after a local build:
npm run pages:deploy
npm run pages:dev     # serve build/ locally via Wrangler
```

Git-connected Pages: build command `npm run build`, output directory `build`, Node 20+.

Optional offline pack:

```bash
npm run build:webxdc   # → build-webxdc/
```

## Content pipeline

Full documents are **not** bulk-translated until the glossary is reviewed.

```text
1. Download English Markdown (nix.dev, manuals, tour, …)
2. Extract tech terms → glossary
3. API suggests FA for words only (pending)
4. Human review / approve (site /glossary-dev or CLI)
5. Translate Markdown (approved glossary; fenced code never sent to the model)
6. Publish FA into src/routes/pages/*
```

```bash
make install              # uv sync + npm install
make help                 # all targets
make env-check            # non-secret config status

# Staged flow (example: nix.dev)
make download-nix-dev
make glossary
make glossary-suggest
make glossary-approve     # or review in the browser
make translate-docs
make publish-site
```

Common targets:

| Target | Role |
|--------|------|
| `download-nix-dev` / `download-nix-manual` / `download-nixpkgs-manual` / `download-tour` | Fetch EN sources → `docs/en/…` |
| `glossary` / `glossary-suggest` / `glossary-approve` | Term list + API suggestions + approve |
| `translate-docs` / `translate-nix-manual` / `translate-nixpkgs-manual` | EN→FA → `docs/fa/…` |
| `publish-site` / `publish-tour` | Write into site routes / tour JSON |
| `page-source-map` | Route → GitHub + published web URL map |
| `pipeline-full` | Bulk 1–6 (long API run) |
| `dev` / `build` / `deploy` | Site |

Section-level re-translate (partial FA pages), jobs, and module layout: **`tools/README.md`**.

### Configuration

```bash
cp .env.example .env
# set OPENAI_API_KEY, model, paths, …
make env-check
```

Typical variables: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` / `TRANSLATE_MODEL`, glossary paths, download/translate I/O dirs. CLI flags override paths when provided.

## Repository layout

| Path | Purpose |
|------|---------|
| `src/` | SvelteKit app (routes, components, styles) |
| `src/routes/pages/` | Published FA Markdown pages |
| `docs/en/`, `docs/fa/` | English sources and FA translations |
| `tools/` | Download, glossary, translate, publish |
| `scripts/` | Build helpers (sitemap, avatars, agent skills, …) |
| `static/` | Static assets, `/.well-known/`, tour runtime |
| `Makefile` | Pipeline + site targets |
| `glossary.json` | Term store used by translate & site |
| `.env` | Local secrets (gitignored) |

## License

This project is free software under the [GNU General Public License v3 or later](LICENSE).
