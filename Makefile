# Nix notes — staged pipeline: download → glossary → suggest words → YOU review → full translate
# All secrets/config: `.env` (see `.env.example`).

.PHONY: help install py-install download download-nix-dev download-nix-manual download-nixpkgs-manual download-tour glossary glossary-suggest glossary-approve \
	translate translate-docs translate-nix-manual translate-nixpkgs-manual translate-tour publish-site page-source-map publish-tour site-install dev build build-webxdc preview check clean env-check \
	pipeline-words pipeline-full pipeline-tour pipeline-nix-manual pipeline-nixpkgs-manual tour-json deploy pages-dev pages-deploy

UV ?= uv
NPM ?= npm
# Prefer bun if available (wrangler/vite), else npm
BUN ?= $(shell command -v bun 2>/dev/null)
PYTHON := $(UV) run python
XDC_NAME ?= nix-notes.xdc
XDC_OUT ?= $(XDC_NAME)

# Cloudflare Pages
PAGES_PROJECT ?= nixy
PUBLIC_SITE_URL ?= https://nixy.a15d.at
PAGES_BRANCH ?= main

help:
	@echo "═══════════════════════════════════════════════════════════"
	@echo "  Staged translation pipeline (IMPORTANT order)"
	@echo "═══════════════════════════════════════════════════════════"
	@echo "  1) make download-nix-dev       # FULL nix.dev source/ → docs/en/"
	@echo "  2) make glossary               # tech words from all docs"
	@echo "  3) make glossary-suggest       # API: words only"
	@echo "  4) make glossary-approve       # approve terms that have FA text"
	@echo "     (or make dev → /glossary for manual review)"
	@echo "  5) make translate-docs         # translate ALL MD → docs/fa/"
	@echo "  6) make publish-site           # FA → /pages/nix-dev/* (+ nix-manual if present)"
	@echo "  make page-source-map           # big route→GitHub/web map → src/lib/page-source-map.json"
	@echo ""
	@echo "  Nix reference manual (NixOS/nix):"
	@echo "  make download-nix-manual       # doc/manual/source → docs/en/nix-manual/"
	@echo "  make translate-nix-manual      # EN→FA → docs/fa/nix-manual/"
	@echo "  make pipeline-nix-manual       # download + translate + publish"
	@echo ""
	@echo "  Nixpkgs manual (NixOS/nixpkgs doc/):"
	@echo "  make download-nixpkgs-manual   # doc/ → docs/en/nixpkgs-manual/"
	@echo "  make translate-nixpkgs-manual  # EN→FA → docs/fa/nixpkgs-manual/"
	@echo "  make pipeline-nixpkgs-manual  # download + translate + publish"
	@echo ""
	@echo "  Tour of Nix (nixcloud):"
	@echo "  make download-tour             # questions.json → docs/en/tour-of-nix/"
	@echo "  make translate-tour            # EN→FA → docs/fa/tour-of-nix/"
	@echo "  make publish-tour / tour-json  # FA JSON for interactive tour"
	@echo "  make pipeline-tour             # download + translate + JSON"
	@echo ""
	@echo "  make build                     # static site → build/ (Cloudflare Pages)"
	@echo "  make deploy                    # build + deploy to $(PAGES_PROJECT) ($(PUBLIC_SITE_URL))"
	@echo "  make pages-dev                 # serve build/ via wrangler pages dev"
	@echo "  make build-webxdc              # offline .xdc (no CDN; copy-link modal)"
	@echo "  make pipeline-full             # 1–6 bulk (long API run)"
	@echo "  make env-check | install | dev"
	@echo ""
	@echo "Config: .env  (OPENAI_API_KEY, NIX_DEV_*, NIX_MANUAL_*, GLOSSARY_*, TRANSLATE_*)"
	@echo "Cloudflare: wrangler.jsonc (project $(PAGES_PROJECT), output build/)"
	@echo "  login once: bunx wrangler login   (or npx wrangler login)"

install: py-install site-install

py-install:
	$(UV) sync

site-install:
	$(NPM) install

env-check:
	$(PYTHON) -c "from tools.lib.envutil import load_dotenv, env_str; from tools.lib.glossary import glossary_review_stats, load_glossary; \
load_dotenv(); \
print('OPENAI_MODEL=', env_str('OPENAI_MODEL')); \
print('OPENAI_API_KEY=', '[set]' if env_str('OPENAI_API_KEY') else '[missing]'); \
print('NIX_DEV_PATH=', env_str('NIX_DEV_PATH')); \
print('NIX_DEV_OUTPUT=', env_str('NIX_DEV_OUTPUT')); \
print('GLOSSARY_PATH=', env_str('GLOSSARY_PATH')); \
print('TRANSLATE_OUT_DIR=', env_str('TRANSLATE_OUT_DIR')); \
s=glossary_review_stats(load_glossary()); \
print('glossary tech/approved/pending=', s['tech'], s['approved'], s['pending'])"

# Legacy single HTML page
download:
	$(PYTHON) -m tools.download.page

# Full nix.dev documentation from GitHub
download-nix-dev download-first-steps:
	$(PYTHON) -m tools.download.nix_dev

# Official Nix reference manual (NixOS/nix) + fix @nix-*@ placeholders on overview
download-nix-manual:
	$(PYTHON) -m tools.download.nix_manual

# Nixpkgs manual (NixOS/nixpkgs doc/) via GitHub API
download-nixpkgs-manual:
	$(PYTHON) -m tools.download.nixpkgs_manual

glossary:
	$(PYTHON) -m tools.glossary.build

glossary-suggest:
	$(PYTHON) -m tools.glossary.suggest

glossary-approve:
	$(PYTHON) -m tools.glossary.approve --use-suggestion

pipeline-words: download-nix-dev glossary glossary-suggest glossary-approve
	@echo ">>> Glossary ready. Review /glossary if you want, then: make translate-docs"

# Full bulk: download → glossary → translate → website (long)
pipeline-full: pipeline-words translate-docs publish-site
	@echo ">>> Full nix.dev FA published under /pages/nix-dev"

# Legacy single-file translate
translate:
	$(PYTHON) -m tools.translate.fa

# Full multi-doc translate (gated on approved glossary)
translate-docs:
	$(PYTHON) -m tools.translate.docs

# Nix reference manual only (skip files already translated)
translate-nix-manual:
	$(PYTHON) -m tools.translate.docs --force --skip-existing $$(find docs/en/nix-manual -name '*.md' ! -name 'manifest.json' | sort)

pipeline-nix-manual: download-nix-manual translate-nix-manual publish-site
	@echo ">>> Nix reference manual FA at /pages/nix-manual"

# Nixpkgs manual only (skip files already translated)
translate-nixpkgs-manual:
	$(PYTHON) -m tools.translate.docs --force --skip-existing --model google/gemini-3.5-flash-lite \
		$$(find docs/en/nixpkgs-manual -name '*.md' ! -name 'manifest.json' | sort)

pipeline-nixpkgs-manual: download-nixpkgs-manual translate-nixpkgs-manual publish-site
	@echo ">>> Nixpkgs manual FA at /pages/nixpkgs-manual"

# Copy cleaned FA markdown into the website
publish-site:
	$(PYTHON) -m tools.publish.site_docs

# Route → GitHub blob + published web URL map (src/lib/page-source-map.json)
page-source-map:
	$(PYTHON) -m tools.publish.page_source_map

# ── Tour of Nix (https://github.com/nixcloud/tour_of_nix) ──
download-tour:
	$(PYTHON) -m tools.download.tour_of_nix

translate-tour:
	$(PYTHON) -m tools.translate.docs --force --skip-existing $$(find docs/en/tour-of-nix -name '*.md' | sort)

# FA question JSON for the interactive tour UI
tour-json:
	$(PYTHON) -m tools.publish.tour_fa_json

publish-tour: tour-json
	@echo ">>> Interactive tour uses static/tour-of-nix (questions.fa.json + nix-instantiate)"

pipeline-tour: download-tour translate-tour tour-json
	@echo ">>> Tour of Nix FA ready at /pages/tour-of-nix"

dev:
	$(NPM) run dev

build:
	$(NPM) run build

# Cloudflare Pages → https://nixy.a15d.at (project: nixy)
# Login once: bunx wrangler login
deploy:
	@echo ">>> Building static site (PUBLIC_SITE_URL=$(PUBLIC_SITE_URL))…"
	PUBLIC_SITE_URL=$(PUBLIC_SITE_URL) $(NPM) run build
	@test -f build/index.html || (echo "missing build/index.html" >&2; exit 1)
	@echo ">>> Deploying build/ → Cloudflare Pages project '$(PAGES_PROJECT)'…"
ifneq ($(BUN),)
	$(BUN)x wrangler pages deploy build \
		--project-name=$(PAGES_PROJECT) \
		--branch=$(PAGES_BRANCH) \
		--commit-dirty=true
else
	$(NPM) exec -- wrangler pages deploy build \
		--project-name=$(PAGES_PROJECT) \
		--branch=$(PAGES_BRANCH) \
		--commit-dirty=true
endif
	@echo ">>> Live: $(PUBLIC_SITE_URL)  (also *.pages.dev from wrangler output)"

# Upload existing build/ without rebuilding
pages-deploy:
ifneq ($(BUN),)
	$(BUN)x wrangler pages deploy build \
		--project-name=$(PAGES_PROJECT) \
		--branch=$(PAGES_BRANCH) \
		--commit-dirty=true
else
	$(NPM) exec -- wrangler pages deploy build \
		--project-name=$(PAGES_PROJECT) \
		--branch=$(PAGES_BRANCH) \
		--commit-dirty=true
endif

pages-dev: build
ifneq ($(BUN),)
	$(BUN)x wrangler pages dev build
else
	$(NPM) run pages:dev
endif

# Fully offline Webxdc package:
#  - adapter-static → build-webxdc/
#  - local fonts + tour assets only (no CDN)
#  - external links → copy-link modal (VITE_WEBXDC=1)
#  - zip as .xdc (manifest.toml + icon.png included from static/)
build-webxdc: tour-json
	@echo ">>> Building offline Webxdc (static, no CDN)…"
	WEBXDC=1 VITE_WEBXDC=1 $(NPM) run build:webxdc
	@test -f build-webxdc/index.html || (echo "missing build-webxdc/index.html" >&2; exit 1)
	@test -f build-webxdc/manifest.toml || (echo "missing manifest.toml in build" >&2; exit 1)
	@# refuse if built HTML still points at common CDNs
	@if rg -n 'https?://(cdn\.|unpkg\.|jsdelivr|fonts\.googleapis|fonts\.gstatic|cdnjs)' build-webxdc -g '*.{html,js,css}' >/dev/null 2>&1; then \
		echo "ERROR: CDN URLs found in build-webxdc — aborting" >&2; \
		rg -n 'https?://(cdn\.|unpkg\.|jsdelivr|fonts\.googleapis|fonts\.gstatic|cdnjs)' build-webxdc -g '*.{html,js,css}' | head -20 >&2; \
		exit 1; \
	fi
	@rm -f $(XDC_OUT)
	@# webxdc = zip of build root (store paths relative to package root)
	cd build-webxdc && zip -9 -r -q ../$(XDC_OUT) . \
		-x '*.map' -x '**/.DS_Store'
	@ls -lh $(XDC_OUT)
	@echo ">>> Packed $(XDC_OUT) (offline Webxdc). External links open a copy modal."

preview:
	$(NPM) run preview

check:
	$(NPM) run check

clean:
	rm -rf .svelte-kit build build-webxdc .output node_modules/.vite $(XDC_NAME)
	@echo "Kept node_modules, .venv, docs/, glossary.json."
