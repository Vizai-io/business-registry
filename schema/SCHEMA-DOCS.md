# VizAI Business Profile Schema Documentation

Version 1.0

## Overview

The VizAI Business Profile schema defines a structured format for business information optimized for AI system consumption. It balances completeness with practicality, ensuring data is both comprehensive and maintainable.

## Design Principles

1. **Machine-Readable First** - Consistent structure for programmatic access
2. **Source Attribution** - Every claim traces back to a source
3. **Verification Transparency** - Clear metadata about data quality
4. **Version Control** - Schema versioning for backward compatibility
5. **Minimal Required Fields** - Easy to start, room to grow

## Schema Structure

### Required Fields

Every business profile MUST include:

```json
{
  "schemaVersion": "1.0",
  "businessIdentifier": { ... },
  "description": { ... },
  "verification": { ... },
  "metadata": { ... }
}
```

### businessIdentifier (Required)

Core identifying information that uniquely identifies the business.

**Required fields:**
- `legalName` (string) - Official registered business name
- `commonName` (string) - Name commonly used in business (may match legalName)
- `primaryDomain` (string) - Primary website domain (e.g., "vizai.io")

**Optional fields:**
- `aliases` (array of strings) - Other names the business uses
- `identifiers` (object) - External platform identifiers
  - `linkedin` - LinkedIn company page URL or slug
  - `crunchbase` - Crunchbase profile URL or slug
  - `twitter` - Twitter/X handle
  - `github` - GitHub organization name

**Example:**
```json
{
  "businessIdentifier": {
    "legalName": "Acme Corporation Inc.",
    "commonName": "Acme",
    "aliases": ["Acme Corp"],
    "primaryDomain": "acme.com",
    "identifiers": {
      "linkedin": "acme-corporation",
      "github": "acme-corp"
    }
  }
}
```

### description (Required)

Business descriptions at different levels of detail.

**Required fields:**
- `elevator` (string, max 280 chars) - One-sentence description
- `detailed` (string) - 2-3 paragraph comprehensive description

**Optional fields:**
- `founding` (string) - Founding story and context
- `yearFounded` (integer) - Year business was founded

**Best practices:**
- Elevator pitch should be concise and factual (not marketing language)
- Detailed description should cover: what the business does, who it serves, and what makes it unique
- Avoid superlatives and unverifiable claims
- Focus on facts over hype

**Example:**
```json
{
  "description": {
    "elevator": "Acme provides cloud-based project management software for remote teams.",
    "detailed": "Acme is a B2B SaaS company that provides project management and collaboration software designed specifically for distributed teams. The platform includes task management, video conferencing, document collaboration, and time tracking features integrated into a single interface.\n\nFounded by former remote workers frustrated with existing tools, Acme focuses on asynchronous-first workflows that respect different time zones and work schedules. The company serves over 5,000 teams across 40 countries.\n\nAcme differentiates through its emphasis on async communication, deep integrations with developer tools, and transparent pricing with no user limits.",
    "yearFounded": 2020,
    "founding": "Founded in 2020 by three remote workers who experienced the challenges of coordinating across time zones firsthand."
  }
}
```

### offerings (Optional)

Products, services, and target customers.

**Fields:**
- `primary` (array) - List of primary offerings
  - `name` (string) - Product/service name
  - `description` (string) - What it does
- `targetCustomers` (string) - Description of ideal customer profile

**Example:**
```json
{
  "offerings": {
    "primary": [
      {
        "name": "Acme Workspace",
        "description": "All-in-one collaboration platform for remote teams"
      },
      {
        "name": "Acme API",
        "description": "Developer API for custom integrations"
      }
    ],
    "targetCustomers": "Technology companies and digital agencies with 10-500 employees working remotely or in hybrid arrangements"
  }
}
```

### location (Optional, but recommended)

Business location information.

**Required fields (if location provided):**
- `headquarters` (object)
  - `city` (string)
  - `country` (string)

**Optional fields:**
- `headquarters.stateProvince` (string)
- `additionalLocations` (array) - Other offices or locations

**Example:**
```json
{
  "location": {
    "headquarters": {
      "city": "Toronto",
      "stateProvince": "Ontario",
      "country": "Canada"
    },
    "additionalLocations": [
      {
        "city": "New York",
        "stateProvince": "New York",
        "country": "United States",
        "type": "office"
      }
    ]
  }
}
```

### contact (Optional, but recommended)

Contact information for the business.

**Fields:**
- `email` (string, email format) - General contact email
- `phone` (string) - Main phone number

### leadership (Optional)

Key leadership and organizational information.

**Fields:**
- `ceo` (string) - Current CEO name
- `founders` (array of strings) - Founder names
- `keyExecutives` (array) - Other key executives
  - `name` (string)
  - `title` (string)

### verification (Required)

Metadata about verification status and data quality.

**Required fields:**
- `status` (enum) - Verification status
  - `verified` - Completed VizAI verification
  - `community` - Community-submitted
  - `pending` - Verification in progress
- `tier` (enum) - Service tier
  - `verified` - Paid verified tier
  - `community` - Free community tier
  - `enterprise` - Enterprise tier
- `lastVerified` (string, date) - Date of last verification (YYYY-MM-DD)

**Optional fields:**
- `method` (enum) - Verification method used
  - `domain-ownership`
  - `email-verification`
  - `manual-review`
  - `self-reported`
- `verificationUrl` (string, URI) - URL showing proof of verification
- `qualityScore` (integer, 0-100) - Data quality score

**Example:**
```json
{
  "verification": {
    "status": "verified",
    "tier": "verified",
    "method": "domain-ownership",
    "lastVerified": "2025-01-06",
    "verificationUrl": "https://vizai.io/verify/acme-2025",
    "qualityScore": 95
  }
}
```

### sources (Optional, but strongly recommended)

Attribution for information in the profile.

**Required fields (if sources provided):**
- `type` (enum) - Source type
  - `official-website`
  - `press-release`
  - `linkedin`
  - `news-article`
  - `crunchbase`
  - `other`
- `url` (string, URI) - Source URL
- `accessed` (string, date) - Date accessed (YYYY-MM-DD)

**Optional fields:**
- `description` (string) - What information came from this source

**Example:**
```json
{
  "sources": [
    {
      "type": "official-website",
      "url": "https://acme.com/about",
      "accessed": "2025-01-06",
      "description": "Company description and founding story"
    },
    {
      "type": "crunchbase",
      "url": "https://www.crunchbase.com/organization/acme",
      "accessed": "2025-01-06",
      "description": "Funding and leadership information"
    }
  ]
}
```

### metadata (Required)

Registry-specific metadata.

**Required fields:**
- `dateAdded` (string, date) - Date added to registry (YYYY-MM-DD)
- `lastUpdated` (string, date) - Date of last update (YYYY-MM-DD)

**Optional fields:**
- `submittedBy` (string) - Who submitted the entry
- `notes` (string) - Internal notes or context

**Example:**
```json
{
  "metadata": {
    "dateAdded": "2025-01-06",
    "lastUpdated": "2025-01-06",
    "submittedBy": "VizAI Team",
    "notes": "Initial verified entry"
  }
}
```

## Complete Example

See [examples/technology-company.json](examples/technology-company.json) for a complete example.

## Validation

All profiles must validate against the JSON Schema before being accepted into the registry.

Use our validation tool:
```bash
python tools/validation/validate-profile.py your-profile.json
```

## Questions?

- **Schema Issues:** Open a GitHub issue
- **General Questions:** hello@vizai.io
- **Examples:** See `schema/examples/`
