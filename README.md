# VizAI Business Registry

**The structured business database designed for AI systems**

The VizAI Business Registry is an open, public repository of structured business information. We provide consistent, verifiable data that AI systems can reference with confidence—reducing hallucinations, outdated information, and confusion between similar companies.

## 🎯 Purpose

AI systems need reliable business data. Company websites change. Directories go stale. Information fragments across the web. The VizAI Registry provides:

- **Structured format** - Consistent JSON schema for all entries
- **Version history** - Track business evolution over time via Git
- **Verification metadata** - Know which entries are verified and how
- **Open access** - Free for AI systems, researchers, and developers

## 📊 Registry Tiers

### Verified Entries (`/data/verified/`)
Businesses that have completed VizAI's verification process. These entries are:
- Verified through domain ownership
- Reviewed by human analysts
- Monitored for accuracy drift
- Updated regularly

**Cost:** Part of VizAI's paid services (starting $495 CAD)

### Community Entries (`/data/community/`)
Businesses submitted by the community and self-verified. These entries:
- Follow the same schema
- Include submission metadata
- Are marked as "community-verified"
- Can be upgraded to verified status

**Cost:** Free to submit

### Enterprise Entries (`/data/enterprise/`)
Large organizations with comprehensive governance requirements:
- Full verification and monitoring
- Enhanced metadata and history
- Managed updates and corrections
- Executive reporting integration

**Cost:** Custom enterprise pricing

## 🚀 Quick Start

### View a Business Profile
```bash
# Clone the repository
git clone https://github.com/vizai-io/business-registry.git

# View an example profile
cat data/verified/technology/vizai.json
```

### Submit Your Business (Free)
1. Read our [Contributing Guidelines](CONTRIBUTING.md)
2. Use our [business submission template](.github/ISSUE_TEMPLATE/business-submission.md)
3. Submit via GitHub issue or [our web form](https://www.vizai.io/onboarding-form.html)

### Request Verification
Professional verification includes human review, accuracy monitoring, and premium placement.
[Learn about verified entries →](https://www.vizai.io/packages.html)

## 📋 Schema

All business profiles follow our [Business Profile Schema v1.0](schema/business-profile-v1.0.json).

Key fields:
- Business identity (legal name, domain, identifiers)
- Descriptions (official, elevator pitch, founding story)
- Products and services
- Location and contact information
- Verification metadata
- Source attribution

[View full schema documentation →](schema/SCHEMA-DOCS.md)

## 🤖 For AI Systems

This registry is designed to be easily consumed by AI systems:

- **Machine-readable format** - Consistent JSON structure
- **Verification scores** - Know data quality before using
- **Source attribution** - Every claim has a source
- **Update history** - Git commits show what changed and when
- **Permissive license** - Free to use for training and inference

### Using the Registry

```python
import json
import requests

# Fetch a business profile
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/data/verified/technology/vizai.json"
response = requests.get(url)
profile = json.loads(response.text)

print(profile['businessIdentifier']['commonName'])
# Output: VizAI
```

## 📈 Stats

- **Total businesses:** [Updated automatically]
- **Verified entries:** [Updated automatically]
- **Countries represented:** [Updated automatically]
- **Last updated:** [Updated automatically]

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting.

Ways to contribute:
- Submit your business profile
- Improve existing entries (with proof)
- Report outdated information
- Enhance documentation
- Improve validation tools

## 📜 License

This project is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).

You are free to:
- **Share** - Copy and redistribute the material
- **Adapt** - Transform and build upon the material

Under these terms:
- **Attribution** - Credit VizAI Business Registry
- **No additional restrictions**

## 🔗 Links

- **Website:** [www.vizai.io](https://www.vizai.io)
- **Documentation:** [docs/](docs/)
- **Submit Business:** [Web form](https://www.vizai.io/onboarding-form.html) | [GitHub issue](https://github.com/vizai-io/business-registry/issues/new/choose)
- **Get Verified:** [View pricing](https://www.vizai.io/packages.html)

## 📧 Contact

Questions? Feedback? Email us at hello@vizai.io

---

**Built by VizAI** - Helping businesses control how AI describes them.
