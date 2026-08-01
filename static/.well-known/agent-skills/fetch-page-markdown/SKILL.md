---
name: fetch-page-markdown
description: Fetch Niksy HTML pages as Markdown via HTTP content negotiation (Accept: text/markdown). Use when reading documentation from this site for agent context.
---

# Fetch page as Markdown

Niksy supports **Markdown for Agents** content negotiation on HTML document URLs (Cloudflare Pages Function middleware).

## Request

```http
GET /pages/nix-dev HTTP/1.1
Host: nixy.a15d.at
Accept: text/markdown
```

```bash
curl -sS -D- -H 'Accept: text/markdown' 'https://nixy.a15d.at/pages/how-nix-works'
```

### Accept rules (origin middleware)

- `text/markdown` must be present and not outranked by `text/html` (compare `q` values).
- Browsers that send `Accept: text/html,...` continue to receive HTML.

## Successful response

| Header | Typical value |
|--------|----------------|
| `Content-Type` | `text/markdown; charset=utf-8` |
| `Vary` | includes `Accept` |
| `x-markdown-tokens` | rough token estimate of Markdown body |
| `x-original-tokens` | rough token estimate of original HTML |
| `Content-Signal` | `ai-train=yes, search=yes, ai-input=yes` (when not already set) |

Body: Markdown with optional YAML front matter (`title`, `description`, `image`) derived from page meta tags, then the main content (chrome/nav/footer stripped). JSON-LD blocks may appear in a trailing fenced `json` code block.

## When not to use

- Binary/static assets (`/glossary.json`, images, fonts) are not converted.
- Prefer `/glossary.json` for terminology and `/sitemap.xml` for URL discovery.
- Very large HTML responses may fall back to HTML (size guard in middleware).

## Related discovery

- Skills index: `/.well-known/agent-skills/index.json`
- API catalog: `/.well-known/api-catalog`
- Homepage Link relations also point at the catalog and glossary feed.
