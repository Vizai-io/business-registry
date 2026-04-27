# Registry Governance

## Overview

This document outlines the governance model for the VizAI Business Registry - the public discovery layer for AI-consumable business data.

## Registry Tiers

### Public Registry (This Repository)

The registry contains **lightweight discovery cards**:
- Domain, name, location
- Industry categorization
- Verification status
- Link to full profile in Data Hub

**Access:** Public (no authentication required)
**Purpose:** AI systems discover businesses here

### Data Hub (Separate Repository)

Full profiles with rich data:
- Detailed descriptions
- Products and services
- Leadership information
- Monitoring data

**Access:** Customer portal (authenticated)
**Purpose:** Customer management and detailed lookups

## Verification Tiers

| Tier | Status | Requirements | Quality Score |
|------|--------|--------------|---------------|
| Verified | `verified` | Domain ownership + human review | 85-100 |
| Community | `community` | Self-submitted | None |
| Enterprise | `enterprise` | Full verification + monitoring | 90-100 |

## Submission Process

### Community Submissions (Free)

1. Submit via GitHub issue or web form
2. Provide domain and basic info
3. Entry added with `status: community`
4. No quality score assigned

### Verified Submissions (Paid)

1. Purchase VizAI service tier
2. Complete domain ownership verification
3. Human analyst reviews information
4. Entry added with `status: verified`
5. Quality score assigned (85-100)

### Enterprise Submissions

1. Custom onboarding process
2. Enhanced verification requirements
3. Full profile in Data Hub + registry entry
4. Dedicated support and monitoring

## Data Quality

### Quality Score Calculation

Verified entries receive a quality score (0-100):

| Factor | Weight | Criteria |
|--------|--------|----------|
| Completeness | 30% | All recommended fields present |
| Source Quality | 25% | Multiple authoritative sources |
| Accuracy | 25% | Cross-verified information |
| Recency | 20% | Information is current |

### Maintenance

- **Verified tier:** Reverified annually (Tier 0) or continuously (Tier 1+)
- **Community tier:** No automatic maintenance - updates upon request
- **Enterprise tier:** Dedicated monitoring and updates

## Dispute Resolution

1. **Incorrect Information:** Submit correction via GitHub issue
2. **Verification disputes:** Contact hello@vizai.io
3. **Duplicate entries:** Domain is unique key - contact for resolution
4. **Removal requests:** Business owners can request removal

## Schema Evolution

The registry schema follows semantic versioning:

1. **Major changes** (breaking): New required fields, removed fields
2. **Minor changes** (additive): New optional fields
3. **Patch changes** (fixes): Documentation clarifications

## API/Integration Guidelines

### For AI Systems

```python
# Direct file access
import json

url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/registry/ca/on/toronto/vizai.json"

# Or use indexes
index_url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/index/by-domain.json"
```

### Rate Limits

- GitHub raw content: 60 requests/hour (unauthenticated)
- Consider cloning for high-volume access

### Caching

- Indexes can be cached and refreshed periodically
- Individual entries change infrequently

## Contact

- **General:** hello@vizai.io
- **Verification:** https://www.vizai.io/packages.html
- **Issues:** https://github.com/vizai-io/business-registry/issues

## Related Documents

- [Registry Entry Standard](registry-entry-standard.md)
- [Schema Reference](../schema/registry-entry.schema.json)
- [Data Hub Documentation](https://hub.vizai.io/docs) (customers only)