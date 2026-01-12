# Automation Tools

This directory contains automation scripts for managing the VizAI Business Registry at scale.

## Scripts

### generate-profile.py

Generates a complete business profile JSON from submission data.

**Usage:**
```bash
python generate-profile.py --input submission.json --output data/community/technology/company.json
```

**Input format (submission.json):**
```json
{
  "legalName": "Acme Corporation",
  "commonName": "Acme",
  "primaryDomain": "acme.com",
  "elevator": "Acme provides cloud services for businesses.",
  "detailed": "Full detailed description...",
  "headquarters": {
    "city": "San Francisco",
    "stateProvince": "California",
    "country": "United States"
  },
  "email": "hello@acme.com",
  "submittedBy": "Community"
}
```

### generate-indexes.py

Generates index files for fast discovery and querying.

**Usage:**
```bash
# Generate all indexes
python generate-indexes.py

# Runs automatically via GitHub Actions when profiles are added
```

**Output:**
- `data/verified/technology/index.json` - Index for verified tech companies
- `data/community/retail/index.json` - Index for community retail businesses
- `data/index.json` - Master index across all tiers

**Index format:**
```json
{
  "tier": "verified",
  "category": "technology",
  "lastUpdated": "2025-01-06",
  "count": 42,
  "profiles": [
    {
      "file": "technology/vizai.json",
      "domain": "vizai.io",
      "commonName": "VizAI",
      "legalName": "VizAI",
      "lastVerified": "2025-01-06",
      "qualityScore": 100
    }
  ]
}
```

## GitHub Actions Integration

These tools are designed to be called from GitHub Actions workflows:

### Example: Auto-generate profile from approved issue

```yaml
- name: Generate profile
  run: |
    python tools/automation/generate-profile.py \
      --input /tmp/submission.json \
      --output data/community/technology/company.json
```

### Example: Update indexes after merge

```yaml
- name: Update indexes
  run: python tools/automation/generate-indexes.py
```

## Future Tools

Planned automation scripts:

- `validate-bulk.py` - Validate multiple profiles in parallel
- `migrate-tier.py` - Move profiles between tiers (community → verified)
- `check-drift.py` - Detect when business information has changed
- `export-snapshot.py` - Export registry snapshot for training
- `sync-crunchbase.py` - Enrich profiles with Crunchbase data
- `monitor-sources.py` - Check if source URLs are still accessible

## Development

### Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Test profile generation
python generate-profile.py --input test/sample-submission.json --output test/output.json

# Test index generation
python generate-indexes.py
```

### Adding new automation

1. Create new Python script in this directory
2. Follow existing patterns for argument parsing
3. Add error handling and logging
4. Document in this README
5. Create GitHub Action workflow if needed
6. Test locally before deploying

## Questions?

- **Technical issues:** Open a GitHub issue
- **Email:** hello@vizai.io
