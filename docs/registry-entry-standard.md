# Registry Entry Standard

Version 1.0

## Overview

The VizAI Registry Entry is a **lightweight discovery card** that provides just enough information for AI systems to identify and locate a business. Each entry points to the full profile in VizAI Data Hub for detailed information.

## Design Principles

1. **Minimal** - Only essential identification fields
2. **Discoverable** - Organized by location for geographic queries  
3. **Referential** - Points to full profile, doesn't duplicate data
4. **Versioned** - Schema follows semantic versioning

## Entry Structure

### Required Fields

```json
{
  "registryId": "example-co",
  "domain": "exampleco.ca",
  "name": "Example Company",
  "location": { "country": "CA", "region": "ON", "city": "Perth" },
  "profileUrl": "https://hub.vizai.io/p/example-co",
  "verification": { "status": "verified", "lastVerified": "2025-01-06" },
  "metadata": { "dateAdded": "2025-01-06", "lastUpdated": "2025-01-06" }
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `registryId` | string | Yes | Unique slug identifier |
| `domain` | hostname | Yes | Primary business domain (unique) |
| `name` | string | Yes | Common business name |
| `location` | object | Yes | Geographic location |
| `location.country` | string | Yes | ISO 3166-1 code (e.g., "CA", "US") |
| `location.region` | string | Yes | State/province (e.g., "ON", "California") |
| `location.city` | string | Yes | City name |
| `industry` | enum | No | Primary industry category |
| `services` | array | No | Service categories offered |
| `profileUrl` | uri | Yes | URL to full profile in Data Hub |
| `verification` | object | Yes | Verification metadata |
| `verification.status` | enum | Yes | One of: verified, community, pending |
| `verification.tier` | enum | No | verified, community, enterprise |
| `verification.method` | enum | No | How verified |
| `verification.lastVerified` | date | Yes | Last verification date |
| `verification.qualityScore` | integer | No | 0-100 quality score |
| `metadata` | object | Yes | Registry metadata |
| `metadata.dateAdded` | date | Yes | When added to registry |
| `metadata.lastUpdated` | date | Yes | Last modification |

### Industry Values

- `technology`
- `professional-services`
- `financial`
- `healthcare`
- `manufacturing`
- `retail`
- `construction`
- `hospitality`
- `transportation`
- `education`
- `real-estate`
- `other`

### Service Values

Common services (not limited to):
- `software-development`
- `consulting`
- `accounting`
- `legal-services`
- `marketing`
- `project-management`
- `data-analytics`
- `cloud-services`
- `cybersecurity`
- `ai-governance`

## Directory Structure

Entries are organized geographically:

```
registry/
  /{country}/
    /{region}/
      /{city}/
        {registryId}.json
```

Examples:
```
registry/ca/on/toronto/vizai.json
registry/ca/on/perth/example-co.json
registry/us/ca/san-francisco/acme.json
registry/gb/london/beta-ltd.json
```

## Index Files

The `/index/` directory contains pre-built lookup indexes:

| File | Purpose |
|------|---------|
| `businesses.jsonl` | All entries as JSON Lines (streaming) |
| `by-domain.json` | Fast domain lookup |
| `by-location.json` | Hierarchical by country/region/city |
| `by-service.json` | Grouped by services |
| `by-industry.json` | Grouped by industry |

## Access Patterns

### Find by Domain
```python
import json

with open("index/by-domain.json") as f:
    by_domain = json.load(f)
    
business = by_domain.get("exampleco.ca")
```

### Find by Location
```python
with open("index/by-location.json") as f:
    by_location = json.load(f)
    
# Find all businesses in Toronto, ON, Canada
toronto_businesses = by_location.get("CA", {}).get("ON", {}).get("Toronto", [])
```

### Find by Industry
```python
with open("index/by-industry.json") as f:
    by_industry = json.load(f)
    
tech_companies = by_industry.get("technology", [])
```

## Validation

All entries must validate against the schema:

```bash
python tools/validate_registry.py
```

## Relationship to Data Hub

```
┌─────────────────────────────────────────────────────────────┐
│                     VizAI Platform                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────┐     ┌─────────────────────┐     │
│   │   Data Hub (private)│     │   Registry (public) │     │
│   │                     │     │                     │     │
│   │  Full profile:      │◄────│  Discovery card:    │     │
│   │  - descriptions    │     │  - domain           │     │
│   │  - offerings        │     │  - location         │     │
│   │  - leadership      │     │  - profileUrl ──────┘     │
│   │  - sources         │     │  - verification    │     │
│   │  - monitoring      │     │                     │     │
│   └─────────────────────┘     └─────────────────────┘     │
│                                                             │
│   Customer portal            Public / AI access            │
└─────────────────────────────────────────────────────────────┘
```

The `profileUrl` field links from the public registry entry to the full profile in Data Hub (which requires authentication).

## Version History

- **1.0** - Initial release
  - Core fields: registryId, domain, name, location
  - Optional: industry, services
  - Verification metadata
  - Multi-format indexes