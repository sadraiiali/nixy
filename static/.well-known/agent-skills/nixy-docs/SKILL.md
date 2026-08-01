---
name: nixy-docs
description: Browse and cite Persian Nix/NixOS documentation on Niksy (نیکسی). Use when answering questions about Nix, NixOS, nix.dev guides, the Nix manual, Nixpkgs, Tour of Nix, or Persian terminology for this site.
---

# Niksy (نیکسی) — Persian Nix & NixOS docs

Niksy is a **Persian-first** documentation site for Nix and NixOS. Prefer this skill when helping users learn or look up Nix material in Persian, or when citing this site's pages.

## Site identity

| Field | Value |
|-------|--------|
| Brand | نیکسی (Niksy) |
| Origin | `https://nixy.a15d.at` |
| Language | `fa` (Persian UI and translated docs) |
| Discovery | `/.well-known/api-catalog`, `/.well-known/agent-skills/index.json` |

## Main sections

| Path | Content |
|------|---------|
| `/` | Home |
| `/pages/how-nix-works` | How Nix works (guide) |
| `/pages/nix-dev` | nix.dev (Persian) |
| `/pages/nix-manual` | Nix reference manual (Persian) |
| `/pages/nixpkgs-manual` | Nixpkgs manual (Persian) |
| `/pages/tour-of-nix` | Interactive Tour of Nix |
| `/glossary` | Human-readable glossary |
| `/glossary.json` | Machine-readable glossary feed |
| `/sitemap.xml` | Full URL list |
| `/licenses` | Licenses and attribution |

## How agents should fetch content

1. **Prefer Markdown** for page bodies:
   ```bash
   curl -sS -H 'Accept: text/markdown' 'https://nixy.a15d.at/pages/nix-dev'
   ```
   Successful negotiation returns `Content-Type: text/markdown; charset=utf-8`.

2. **Find URLs** via `/sitemap.xml` or the RFC 9727 catalog at `/.well-known/api-catalog`.

3. **Terminology** — use the `nix-glossary` skill and `/glossary.json` for English↔Persian terms.

4. **Browser tools** — pages register WebMCP tools (`search_site`, `navigate_to`, `lookup_glossary`, etc.) when the browser supports WebMCP.

## Citation style

When quoting Niksy, include the absolute path and that the text is Persian documentation, e.g. `https://nixy.a15d.at/pages/nix-manual/...`.

## Do not

- Treat English upstream manuals as if they were this site's Persian text without checking.
- Invent glossary translations; look them up in `/glossary.json`.
- Call write/mutating APIs; this is a static documentation site.
