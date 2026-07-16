# Generated Registry Indexes

These files are deterministic distribution artifacts generated from:

```text
registry/<entity-slug>/profile.json
```

Run:

```bash
python tools/build_indexes.py
```

Do not edit index files manually.

## Files

| File | Contents |
|---|---|
| `businesses.jsonl` | Every canonical profile, one JSON object per line |
| `by-domain.json` | Primary domain to complete canonical profile |
| `by-location.json` | Country, region, and city to profile summaries |
| `by-industry.json` | Canonical category to profile summaries |
| `by-service.json` | Public service name to profile summaries |
| `by-status.json` | Verification status to identity summaries |

Grouped summaries expose `entitySlug`, `domain`, `name`, canonical profile
`file`, and location data where relevant. A record-shape discriminator is no
longer emitted because entity-profile v1 is the sole production contract.

CI rebuilds every index and fails when committed output has drifted.
