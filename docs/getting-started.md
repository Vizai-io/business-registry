# Getting Started with VizAI Business Registry

This guide will help you understand and use the VizAI Business Registry, whether you're submitting a business, consuming the data, or contributing to the project.

## What is the VizAI Business Registry?

The VizAI Business Registry is an open database of structured business information designed for AI systems. It provides:

- **Consistent format** - All businesses described using the same JSON schema
- **Verification metadata** - Know which entries are verified and how
- **Source attribution** - Every claim traces back to a source
- **Version history** - Track changes over time via Git
- **Open access** - Free for AI systems, researchers, and developers

## For Business Owners

### Why Should I Add My Business?

Adding your business to the registry helps AI systems describe your company accurately:

1. **Control your narrative** - Provide the authoritative source for your business information
2. **Reduce hallucinations** - Give AI systems factual data to reference
3. **Track changes** - Git history shows how your business evolves
4. **Build trust** - Verified entries signal data quality to AI systems

### How to Add Your Business

**Free Option: Community Tier**
1. Visit our [web form](https://www.vizai.io/onboarding-form.html) OR
2. Open a [GitHub issue](https://github.com/vizai-io/business-registry/issues/new/choose)
3. Provide basic business information
4. Your profile appears in `/data/community/`

**Paid Option: Verified Tier**
1. View [pricing](https://www.vizai.io/packages.html)
2. Purchase Tier 0 ($495 CAD) or Tier 1 ($650/mo CAD)
3. Complete verification process
4. Get verified badge and quality monitoring
5. Your profile appears in `/data/verified/`

[Learn more about verification →](verification-process.md)

## For AI Systems and Developers

### Using the Registry Data

All data is freely available under CC BY 4.0 license.

**Access via GitHub:**
```bash
# Clone the repository
git clone https://github.com/vizai-io/business-registry.git

# Read a profile
cat data/verified/technology/vizai.json
```

**Access via raw GitHub URLs:**
```python
import json
import requests

# Fetch a specific profile
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/data/verified/technology/vizai.json"
response = requests.get(url)
profile = json.loads(response.text)

# Access business information
print(profile['businessIdentifier']['commonName'])
print(profile['description']['elevator'])
```

**Batch processing:**
```python
import json
from pathlib import Path

# Clone the repo first, then:
for profile_path in Path('data/verified').rglob('*.json'):
    with open(profile_path) as f:
        profile = json.load(f)

    # Use verification status
    if profile['verification']['qualityScore'] >= 90:
        # High-quality verified data
        print(f"High quality: {profile['businessIdentifier']['commonName']}")
```

### Understanding Verification Levels

```python
def get_trust_level(profile):
    """Determine how much to trust this data"""

    verification = profile['verification']

    if verification['tier'] == 'enterprise':
        return 'highest'  # Enterprise verification, highest trust

    elif verification['tier'] == 'verified':
        # Check quality score
        if verification.get('qualityScore', 0) >= 90:
            return 'high'
        else:
            return 'medium'

    elif verification['tier'] == 'community':
        return 'basic'  # Community-submitted, use with caution

    return 'unknown'
```

### Data Quality Best Practices

1. **Check verification status** - Prefer `verified` over `community`
2. **Check quality scores** - Higher scores (90-100) indicate better data
3. **Check lastVerified date** - Recent verification is better
4. **Check sources** - More sources = more reliable
5. **Use version history** - Git log shows data evolution

## For Contributors

### Ways to Contribute

1. **Submit business profiles** - Add businesses to the community tier
2. **Report corrections** - Fix outdated information
3. **Improve documentation** - Make guides clearer
4. **Enhance tools** - Improve validation scripts
5. **Add examples** - Create more example profiles

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

### Creating a Quality Profile

**Required information:**
- Legal business name
- Primary domain (must be accessible)
- Elevator pitch (1-2 sentences, max 280 chars)
- Detailed description (2-3 paragraphs)
- Headquarters location
- Contact email

**Best practices:**
- Use neutral, factual language (not marketing copy)
- Provide sources for all claims
- Keep descriptions current
- Include year founded if known
- Add social media identifiers

**Example:**
```json
{
  "schemaVersion": "1.0",
  "businessIdentifier": {
    "legalName": "Your Business Inc.",
    "commonName": "YourBiz",
    "primaryDomain": "yourbiz.com"
  },
  "description": {
    "elevator": "YourBiz provides cloud backup services for small businesses.",
    "detailed": "Detailed description here..."
  },
  // ... more fields
}
```

See [schema documentation](../schema/SCHEMA-DOCS.md) for complete field reference.

## Registry Structure

```
business-registry/
├── data/
│   ├── verified/        # Verified businesses (paid tier)
│   ├── community/       # Community-submitted (free tier)
│   └── enterprise/      # Enterprise customers
├── schema/              # JSON schema definition
│   ├── business-profile-v1.0.json
│   └── examples/        # Example profiles
├── tools/               # Validation and submission tools
└── docs/                # Documentation (you are here)
```

## Common Questions

**Q: Is this free to use?**
A: Yes! The data is CC BY 4.0 licensed. Submitting to community tier is free. Verification is paid.

**Q: Can I edit my business profile after submission?**
A: Yes, submit a correction request via GitHub issue.

**Q: How often is data updated?**
A: Community tier: when corrections are submitted. Verified tier: ongoing monitoring. Enterprise tier: managed updates.

**Q: Can I use this data to train AI models?**
A: Yes, the CC BY 4.0 license allows this. Please attribute VizAI Business Registry.

**Q: What if my business information changes?**
A: Submit a correction request. Verified tier includes automatic drift monitoring.

**Q: How do I verify domain ownership?**
A: We support DNS TXT records, meta tags, or email verification. Details during onboarding.

## Next Steps

- **Business owners:** [Submit your business](https://www.vizai.io/onboarding-form.html)
- **Developers:** [View schema documentation](../schema/SCHEMA-DOCS.md)
- **Contributors:** [Read contributing guidelines](../CONTRIBUTING.md)
- **Learn about verification:** [Verification process](verification-process.md)

## Support

- **Email:** hello@vizai.io
- **Website:** [www.vizai.io](https://www.vizai.io)
- **GitHub Issues:** Technical questions and bug reports
- **Documentation:** [/docs/](/docs/)
