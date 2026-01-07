# API Documentation

The VizAI Business Registry is primarily accessed as a Git repository and through raw file access. This document explains how to programmatically access and use the data.

## Access Methods

### 1. Git Clone (Recommended for bulk access)

Clone the entire repository to get all profiles:

```bash
git clone https://github.com/vizai-io/business-registry.git
cd business-registry
```

**Advantages:**
- Full access to all profiles
- Version history included
- Works offline after cloning
- Can track updates with `git pull`

**Use cases:**
- Training AI models
- Building search/directory applications
- Research and analysis
- Offline access needed

### 2. Raw GitHub API (Individual files)

Access individual profiles via raw GitHub URLs:

```python
import requests
import json

# Fetch a specific business profile
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/data/verified/technology/vizai.json"
response = requests.get(url)
profile = json.loads(response.text)

print(profile['businessIdentifier']['commonName'])
# Output: VizAI
```

**Advantages:**
- No cloning needed
- Always get latest version
- Simple HTTP requests
- Good for individual lookups

**Use cases:**
- Real-time lookups
- Web applications
- Lightweight integrations

### 3. GitHub API (Metadata access)

Use GitHub's API to list and discover profiles:

```python
import requests

# List all files in verified/technology directory
url = "https://api.github.com/repos/vizai-io/business-registry/contents/data/verified/technology"
response = requests.get(url)
files = response.json()

for file in files:
    if file['name'].endswith('.json'):
        print(f"Found: {file['name']}")
        # Fetch the file using file['download_url']
```

**Rate limits:** GitHub API has rate limits (60 requests/hour unauthenticated, 5000/hour authenticated)

## Data Structure

### Repository Layout

```
data/
├── verified/           # Verified businesses
│   ├── technology/
│   ├── professional-services/
│   ├── financial/
│   ├── healthcare/
│   ├── manufacturing/
│   ├── retail/
│   └── other/
├── community/          # Community-submitted
│   └── [same structure]
└── enterprise/         # Enterprise tier
    └── [same structure]
```

### Profile Schema

All profiles follow the Business Profile v1.0 schema.

**Key fields:**
```json
{
  "schemaVersion": "1.0",
  "businessIdentifier": {
    "legalName": "string",
    "commonName": "string",
    "primaryDomain": "string",
    "identifiers": { ... }
  },
  "description": {
    "elevator": "string (max 280 chars)",
    "detailed": "string",
    "yearFounded": "integer"
  },
  "offerings": {
    "primary": [ ... ],
    "targetCustomers": "string"
  },
  "verification": {
    "status": "verified|community|pending",
    "tier": "verified|community|enterprise",
    "qualityScore": "integer (0-100)"
  }
}
```

[Full schema documentation →](../schema/SCHEMA-DOCS.md)

## Code Examples

### Python: Load All Verified Profiles

```python
import json
from pathlib import Path

def load_all_profiles(tier='verified'):
    """Load all profiles from a specific tier"""
    profiles = []

    base_path = Path('data') / tier

    for profile_path in base_path.rglob('*.json'):
        with open(profile_path) as f:
            profile = json.load(f)
            profile['_file_path'] = str(profile_path)
            profiles.append(profile)

    return profiles

# Usage
verified_profiles = load_all_profiles('verified')
print(f"Loaded {len(verified_profiles)} verified profiles")

# Filter high-quality profiles
high_quality = [
    p for p in verified_profiles
    if p.get('verification', {}).get('qualityScore', 0) >= 90
]
```

### Python: Search by Domain

```python
def find_by_domain(domain, profiles):
    """Find a business by its primary domain"""
    for profile in profiles:
        if profile['businessIdentifier']['primaryDomain'] == domain:
            return profile
    return None

# Usage
acme = find_by_domain('acme.com', verified_profiles)
if acme:
    print(acme['description']['elevator'])
```

### Python: Filter by Category

```python
from pathlib import Path

def get_profiles_by_category(category, tier='verified'):
    """Get all profiles in a specific category"""
    profiles = []

    category_path = Path('data') / tier / category

    if not category_path.exists():
        return []

    for profile_path in category_path.glob('*.json'):
        with open(profile_path) as f:
            profiles.append(json.load(f))

    return profiles

# Usage
tech_companies = get_profiles_by_category('technology')
print(f"Found {len(tech_companies)} technology companies")
```

### JavaScript: Fetch Remote Profile

```javascript
// Fetch a specific profile
async function getBusinessProfile(tier, category, filename) {
  const url = `https://raw.githubusercontent.com/vizai-io/business-registry/main/data/${tier}/${category}/${filename}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Profile not found: ${filename}`);
  }

  return await response.json();
}

// Usage
getBusinessProfile('verified', 'technology', 'vizai.json')
  .then(profile => {
    console.log(profile.businessIdentifier.commonName);
    console.log(profile.description.elevator);
  });
```

### JavaScript: List All Profiles in Category

```javascript
async function listProfiles(tier, category) {
  const url = `https://api.github.com/repos/vizai-io/business-registry/contents/data/${tier}/${category}`;

  const response = await fetch(url);
  const files = await response.json();

  return files
    .filter(file => file.name.endsWith('.json'))
    .map(file => ({
      name: file.name,
      downloadUrl: file.download_url
    }));
}

// Usage
listProfiles('verified', 'technology')
  .then(profiles => {
    console.log(`Found ${profiles.length} profiles`);
    profiles.forEach(p => console.log(p.name));
  });
```

## Filtering and Quality Checks

### Filter by Quality Score

```python
def filter_by_quality(profiles, min_score=85):
    """Filter profiles by minimum quality score"""
    return [
        p for p in profiles
        if p.get('verification', {}).get('qualityScore', 0) >= min_score
    ]

# Only use highest quality data
high_quality = filter_by_quality(verified_profiles, min_score=90)
```

### Filter by Verification Status

```python
def filter_by_verification(profiles, status='verified'):
    """Filter by verification status"""
    return [
        p for p in profiles
        if p.get('verification', {}).get('status') == status
    ]

# Only verified businesses
verified_only = filter_by_verification(all_profiles, 'verified')
```

### Check Data Freshness

```python
from datetime import datetime, timedelta

def is_fresh(profile, max_age_days=90):
    """Check if profile was verified recently"""
    last_verified = profile.get('verification', {}).get('lastVerified')
    if not last_verified:
        return False

    verified_date = datetime.fromisoformat(last_verified)
    age = datetime.now() - verified_date

    return age.days <= max_age_days

# Only recently verified profiles
fresh_profiles = [p for p in verified_profiles if is_fresh(p)]
```

## Tracking Updates

### Watch for Changes (Git)

```bash
# Clone and setup tracking
git clone https://github.com/vizai-io/business-registry.git
cd business-registry

# Check for updates
git fetch origin
git log HEAD..origin/main --oneline

# Pull latest changes
git pull origin main
```

### Automated Sync Script

```python
import subprocess
from pathlib import Path

def sync_registry(repo_path):
    """Pull latest changes from registry"""
    result = subprocess.run(
        ['git', 'pull'],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Registry updated successfully")
        return True
    else:
        print(f"Update failed: {result.stderr}")
        return False

# Run daily
sync_registry('/path/to/business-registry')
```

## Best Practices

### 1. Respect Verification Tiers

```python
def get_trust_level(profile):
    """Determine data trust level"""
    verification = profile.get('verification', {})

    tier = verification.get('tier')
    quality_score = verification.get('qualityScore', 0)

    if tier == 'enterprise':
        return 'highest'
    elif tier == 'verified' and quality_score >= 90:
        return 'high'
    elif tier == 'verified':
        return 'medium'
    else:
        return 'basic'

# Use trust level to decide how to use data
for profile in profiles:
    trust = get_trust_level(profile)
    if trust in ['highest', 'high']:
        # Use with high confidence
        pass
```

### 2. Cache Appropriately

```python
import json
from datetime import datetime, timedelta

class ProfileCache:
    def __init__(self, cache_duration_hours=24):
        self.cache = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)

    def get(self, domain):
        if domain in self.cache:
            profile, timestamp = self.cache[domain]
            if datetime.now() - timestamp < self.cache_duration:
                return profile
        return None

    def set(self, domain, profile):
        self.cache[domain] = (profile, datetime.now())

# Usage
cache = ProfileCache(cache_duration_hours=24)

def get_business_profile(domain):
    # Check cache first
    cached = cache.get(domain)
    if cached:
        return cached

    # Fetch if not cached
    profile = fetch_from_registry(domain)
    cache.set(domain, profile)
    return profile
```

### 3. Attribution

When using registry data, please attribute:

```python
# In your application
attribution = """
Business data from VizAI Business Registry
https://github.com/vizai-io/business-registry
Licensed under CC BY 4.0
"""

# Or in API responses
{
  "data": { ... },
  "attribution": {
    "source": "VizAI Business Registry",
    "url": "https://github.com/vizai-io/business-registry",
    "license": "CC BY 4.0"
  }
}
```

## Rate Limits and Fair Use

### Git Clone
- No rate limits
- Please don't clone excessively (once per day is reasonable)

### Raw GitHub URLs
- No official rate limit
- Be respectful (cache, don't hammer the servers)

### GitHub API
- 60 requests/hour (unauthenticated)
- 5,000 requests/hour (authenticated)
- Use authentication for production apps

## Future API Plans

We're considering building a dedicated API with:
- REST endpoints for querying profiles
- Search and filtering
- Webhooks for updates
- Higher rate limits
- Real-time updates

Interested? Email hello@vizai.io

## Support

- **Technical questions:** hello@vizai.io
- **Report issues:** [GitHub Issues](https://github.com/vizai-io/business-registry/issues)
- **API requests:** hello@vizai.io
- **Examples:** [/docs/](/docs/)
