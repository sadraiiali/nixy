---
name: nix-glossary
description: Look up Nix/NixOS terms in Niksy's Persian glossary JSON. Use when translating or explaining terminology (English or Persian) for Nix, NixOS, flakes, derivations, nixpkgs, etc.
---

# Nix glossary (Persian)

Machine-readable glossary for Niksy (نیکسی).

## Endpoint

```
GET https://nixy.a15d.at/glossary.json
Content-Type: application/json
```

Human UI: `https://nixy.a15d.at/glossary`

Also listed in `/.well-known/api-catalog` as `service-desc` / `item`.

## Response shape (summary)

```json
{
  "version": "...",
  "docs": [],
  "entries": [
    {
      "term": "derivation",
      "suggestion": "...",
      "translation": "...",
      "notes": "...",
      "sources": [],
      "count": 0,
      "is_tech": true,
      "status": "..."
    }
  ]
}
```

| Field | Use |
|-------|-----|
| `term` | Canonical English (or source) term |
| `suggestion` | Preferred wording / variant |
| `translation` | Persian translation |
| `notes` | Extra context |
| `status` | Editorial status when present |

## Lookup procedure

1. `GET /glossary.json` (cache for the session; it is large but static).
2. Match the user query case-insensitively against `term`, `suggestion`, `translation`, and `notes`.
3. Prefer exact `term` matches, then substring matches.
4. Return up to ~10 best hits with `term`, `translation`, and `notes`.

### Example

```bash
curl -sS 'https://nixy.a15d.at/glossary.json' | jq '
  .entries
  | map(select((.term // "" | ascii_downcase) | contains("flake")))
  | .[0:5]
  | map({term, translation, notes})
'
```

## WebMCP

In a WebMCP-capable browser on this origin, call tool `lookup_glossary` with `{ "query": "..." }`.

## Guidance

- Prefer glossary translations over inventing Persian equivalents for established Nix terms.
- If no entry matches, say so and fall back to careful English explanation plus a suggested Persian paraphrase marked as unofficial.
