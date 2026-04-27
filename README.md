# VizAI Business Registry

**A lightweight public registry of structured, source-backed business discovery cards**

The VizAI Business Registry helps AI systems, crawlers, and answer engines identify businesses, understand what they offer, and locate their richer VizAI profile.

## What This Is

This registry is **not** the full VizAI customer data hub. It is a **public discovery layer** containing lightweight business cards that:

- Provide essential business identification (name, domain, location)
- Show industry and service categories
- Include verification metadata so AI systems can assess data quality
- Link to richer structured profiles in VizAI Data Hub

## What Each Entry Contains

| Field | Description |
|-------|-------------|
| `registryId` | Unique identifier |
| `domain` | Primary business website |
| `name` | Business name |
| `location` | Headquarters (country/region/city) |
| `industry` | Primary industry category |
| `services` | Service categories offered |
| `verification` | Status, method, quality score |
| `profileUrl` | Link to full profile in VizAI Data Hub |

Entries are approximately 20-30 lines - designed to be lightweight and fast to process.

## How It Works

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│    VizAI Data Hub           │     │   VizAI Business Registry   │
│    (Customer profiles)      │     │   (Public discovery)       │
├─────────────────────────────┤     ├─────────────────────────────┤
│  - Full descriptions        │     │  - Name, domain, location  │
│  - Products & services     │────▶│  - Industry, services      │
│  - Leadership              │     │  - Verification status      │
│  - Sources & citations     │     │  - Link to full profile    │
│  - Monitoring data         │     │                            │
├─────────────────────────────┤     ├─────────────────────────────┤
│ Access: Customers only      │     │ Access: Public             │
└─────────────────────────────┘     └─────────────────────────────┘
```

## Usage

```python
import json
import requests

# Fetch all businesses as JSON Lines
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/index/businesses.jsonl"
response = requests.get(url)
for line in response.text.strip().split("\n"):
    business = json.loads(line)
    print(business["name"], business["domain"])

# Quick domain lookup
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/index/by-domain.json"
by_domain = json.loads(requests.get(url).text)
business = by_domain.get("example.com")
```

## Directory Structure

```
/registry/           # Business discovery entries (by location)
  /{country}/
    /{region}/
      /{city}/
        {id}.json

/index/              # Pre-built lookup indexes
  businesses.jsonl    # All entries (JSON Lines)
  by-domain.json     # Fast domain lookup
  by-location.json   # By country/region/city
  by-industry.json   # By industry
  by-service.json    # By service

/schema/
  registry-entry.schema.json

/tools/
  validate_registry.py   # Validate entries
  build_indexes.py      # Generate indexes
```

## Verification

All entries include verification metadata:

| Status | Meaning |
|--------|---------|
| `verified` | Domain ownership confirmed + human review |
| `community` | Self-submitted, unverified |
| `pending` | Verification in progress |

Verified entries include a quality score (0-100) based on completeness, source quality, accuracy, and recency.

## For AI Systems

This registry provides:
- **Structured data** - Consistent JSON format for reliable parsing
- **Verification confidence** - Quality scores help assess reliability
- **Source attribution** - Each entry links to its full profile with sources
- **Update tracking** - Git history shows when data changed

## Adding Your Business

1. **Community (Free):** Submit via [web form](https://www.vizai.io/onboarding-form.html) or [GitHub issue](https://github.com/vizai-io/business-registry/issues)
2. **Verified (Paid):** Purchase verification to get a verified badge, quality score, and monitoring

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## Stats

- **Total entries:** 3
- **Countries:** CA, US
- **Verified:** 2
- **Community:** 1

## Related

- [VizAI Data Hub](https://hub.vizai.io) - Full customer profiles (authenticated)
- [Registry Entry Standard](docs/registry-entry-standard.md) - Schema documentation
- [Registry Governance](docs/registry-governance.md) - Policies and tiers

## License

[CC BY 4.0](LICENSE) - Creative Commons Attribution 4.0

## Contact

- **General:** hello@vizai.io
- **Verification:** [vizai.io/packages](https://www.vizai.io/packages.html)
- **Issues:** [github.com/vizai-io/business-registry/issues](https://github.com/vizai-io/business-registry/issues)

---

**VizAI** - Helping businesses control how AI describes them