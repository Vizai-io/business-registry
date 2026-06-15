# Generated Indexes

**Generated, not source-of-truth.** These files are produced by `tools/build_indexes.py` from the registry source records under `registry/`. Do not hand-edit — run the generator instead.

## Source

`registry/**/*.json`. Two record shapes are indexed and normalized (WP-13B / DEC-029):

| Shape | Where | Identifying fields |
|---|---|---|
| `entity-profile-v1.0` | `registry/<slug>/profile.json` (canonical Model C public profile) | `schemaVersion:"1.0"`, `entitySlug`, `businessIdentifier`, nested `profile`/`verification`/`category` |
| `registry-entry` (legacy) | `registry/<cc>/<region>/<city>/*.json` | top-level `domain`, `registryId`, `location`, `industry`, `services` |

Every grouped index record carries a `shape` field so consumers can distinguish entity profiles from legacy entries during the migration window.

## Files

- `by-domain.json` — domain → full clean entry (native shape)
- `by-location.json` — country → region → city → businesses (entity profiles are multi-location)
- `by-industry.json` — industry/category → businesses
- `by-service.json` — service → businesses
- `by-status.json` — verification status → businesses (e.g. `claimed_verified`, `verified`, `community`)
- `businesses.jsonl` — all entries, one JSON object per line

## Regenerate

```
python tools/build_indexes.py
```

## Notes

- `data/**` tier records are indexed separately by `tools/automation/generate-indexes.py` and are **not** the source for entity-profile indexes.
- The known VizAI dual-record (`data/verified/vizai.json` + `registry/ca/on/toronto/vizai.json`) is tracked for a future migration packet; only the `registry/` copy appears in these indexes.
