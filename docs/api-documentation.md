# Registry Data Access

The VizAI Business Registry is distributed through canonical JSON files and
generated indexes in GitHub. There is currently no separate hosted REST API.

## Canonical URLs

Repository:

```text
https://github.com/Vizai-io/business-registry
```

Canonical profile:

```text
https://raw.githubusercontent.com/Vizai-io/business-registry/main/registry/<entity-slug>/profile.json
```

Domain index:

```text
https://raw.githubusercontent.com/Vizai-io/business-registry/main/index/by-domain.json
```

Bulk JSON Lines:

```text
https://raw.githubusercontent.com/Vizai-io/business-registry/main/index/businesses.jsonl
```

## Exact Domain Lookup

```python
import requests

url = (
    "https://raw.githubusercontent.com/Vizai-io/business-registry/"
    "main/index/by-domain.json"
)
by_domain = requests.get(url, timeout=30).json()
profile = by_domain.get("vizai.io")

if profile:
    print(profile["entitySlug"])
    print(profile["verification"]["status"])
```

```javascript
const url =
  "https://raw.githubusercontent.com/Vizai-io/business-registry/" +
  "main/index/by-domain.json";

const response = await fetch(url);
const byDomain = await response.json();
const profile = byDomain["vizai.io"];
```

## Fetch a Canonical Profile

```python
import requests

entity_slug = "wills-transfer"
url = (
    "https://raw.githubusercontent.com/Vizai-io/business-registry/"
    f"main/registry/{entity_slug}/profile.json"
)
profile = requests.get(url, timeout=30).json()

identifier = profile["businessIdentifier"]
print(identifier["commonName"], identifier["primaryDomain"])
```

## Process the Bulk Index

```python
import json
import requests

url = (
    "https://raw.githubusercontent.com/Vizai-io/business-registry/"
    "main/index/businesses.jsonl"
)
response = requests.get(url, timeout=30)
response.raise_for_status()

profiles = [
    json.loads(line)
    for line in response.text.splitlines()
    if line.strip()
]
```

For large or repeated workloads, clone the repository and update it
periodically:

```bash
git clone https://github.com/Vizai-io/business-registry.git
git -C business-registry pull --ff-only
```

## Discovery Indexes

| File | Use |
|---|---|
| `index/by-domain.json` | Exact primary-domain lookup |
| `index/by-location.json` | Country, region, and city discovery |
| `index/by-industry.json` | Canonical category discovery |
| `index/by-service.json` | Public service discovery |
| `index/by-status.json` | Verification-state filtering |
| `index/businesses.jsonl` | Bulk profile processing |

## Verification Handling

Consumers should inspect `verification.status`:

- `claimed_verified`
- `unclaimed_observed`
- `verification_pending`
- `disputed`

There is no public storage or service tier. Do not infer trust from a removed
`data/verified`, `data/community`, or `data/enterprise` path.

## Caching and Attribution

- Cache generated indexes and refresh them based on your application needs.
- Preserve `entitySlug`, verification metadata, and update dates.
- Use Git commit history when change history matters.
- Attribute the VizAI Business Registry under the repository license.

## Schema

- [Entity Profile Standard](entity-profile-standard.md)
- [Entity Profile Schema](../schema/entity-profile-v1.0.schema.json)
- [BR-02 Migration](migrations/br-02-model-convergence.md)
