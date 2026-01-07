# Submission Tools

This directory contains tools to help create and submit business profiles to the VizAI Business Registry.

## Available Tools

### Profile Validator
Located in `../validation/validate-profile.py`

Validates a business profile JSON file against the VizAI schema.

**Usage:**
```bash
# Install dependencies
pip install -r ../validation/requirements.txt

# Validate a profile
python ../validation/validate-profile.py path/to/profile.json
```

## Creating a Profile

### Method 1: Use the Web Form (Recommended)
The easiest way to submit a business is through our web form:
https://www.vizai.io/onboarding-form.html

### Method 2: Manual JSON Creation

1. **Start with an example**
   Copy one of the examples from `schema/examples/`:
   - `technology-company.json` - Tech/SaaS company
   - `professional-services.json` - Consulting/services firm
   - `enterprise-example.json` - Large enterprise

2. **Edit the fields**
   Replace example data with your business information:
   - Required: businessIdentifier, description, verification, metadata
   - Recommended: location, contact, offerings

3. **Validate the profile**
   ```bash
   python tools/validation/validate-profile.py your-profile.json
   ```

4. **Submit via Pull Request**
   - Fork the repository
   - Add your profile to appropriate directory:
     - Community: `data/community/[category]/your-business.json`
     - Verified: (VizAI will place after verification)
   - Submit pull request

### Method 3: GitHub Issue
Use our issue template:
https://github.com/vizai-io/business-registry/issues/new/choose

## Directory Categories

Place your profile in the appropriate category:

- `technology/` - Software, SaaS, hardware companies
- `professional-services/` - Consulting, legal, accounting
- `financial/` - Banks, fintech, investment firms
- `healthcare/` - Medical, pharmaceutical, health tech
- `manufacturing/` - Industrial, consumer goods
- `retail/` - E-commerce, brick-and-mortar retail
- `other/` - Businesses not fitting above categories

## File Naming

Use lowercase with hyphens:
- ✅ `acme-software.json`
- ✅ `sterling-consulting.json`
- ❌ `AcmeSoftware.json`
- ❌ `acme_software.json`

## Common Errors

### "Missing required field"
Ensure all required fields are present:
- `schemaVersion`
- `businessIdentifier.legalName`
- `businessIdentifier.commonName`
- `businessIdentifier.primaryDomain`
- `description.elevator`
- `description.detailed`
- `verification.status`
- `verification.tier`
- `verification.lastVerified`
- `metadata.dateAdded`
- `metadata.lastUpdated`

### "Invalid date format"
Dates must be in YYYY-MM-DD format:
- ✅ `2025-01-06`
- ❌ `01/06/2025`
- ❌ `January 6, 2025`

### "Elevator pitch too long"
The elevator pitch must be 280 characters or less.

### "Invalid domain format"
Primary domain should be just the domain name:
- ✅ `acme.com`
- ❌ `https://acme.com`
- ❌ `www.acme.com`

## Need Help?

- **Documentation:** [/docs/getting-started.md](/docs/getting-started.md)
- **Schema Docs:** [/schema/SCHEMA-DOCS.md](/schema/SCHEMA-DOCS.md)
- **Examples:** [/schema/examples/](/schema/examples/)
- **Email:** hello@vizai.io
