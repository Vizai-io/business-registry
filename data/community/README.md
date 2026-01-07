# Community Business Profiles

This directory contains business profiles submitted by the community. These are **free to submit** and provide a starting point for businesses to establish their presence in the registry.

## Community Tier

Community profiles are:

- ✅ **Free to submit** - No cost for basic listing
- ✅ **Self-verified** - Marked as community-contributed
- ✅ **Schema-compliant** - Follow the same structure as verified entries
- ✅ **Upgradeable** - Can be upgraded to verified status anytime

## Differences from Verified Tier

| Feature | Community | Verified |
|---------|-----------|----------|
| Cost | Free | From $495 CAD |
| Verification | Self-reported | Domain ownership + human review |
| Quality Score | Not assigned | 85-100 |
| Monitoring | None | Regular accuracy checks (Tier 1+) |
| Placement | `/data/community/` | `/data/verified/` |
| AI Trust Signal | Community-verified | VizAI-verified |

## How to Submit

**Option 1: Web Form (Easiest)**
Fill out our [onboarding form](https://www.vizai.io/onboarding-form.html)

**Option 2: GitHub Issue**
Use the [business submission template](/.github/ISSUE_TEMPLATE/business-submission.md)

**Option 3: Pull Request (Advanced)**
1. Fork this repository
2. Create your profile JSON in `/data/community/[category]/your-business.json`
3. Validate against schema: `python tools/validation/validate-profile.py your-file.json`
4. Submit pull request

## Submission Requirements

Required information:
- Legal business name
- Primary domain (must be accessible)
- Business description (elevator + detailed)
- Headquarters location
- Contact email

See [CONTRIBUTING.md](/CONTRIBUTING.md) for full guidelines.

## Upgrade to Verified

Benefits of upgrading:
- Professional verification badge
- Higher trust signal for AI systems
- Regular accuracy monitoring
- Priority placement
- Drift detection alerts

[View pricing and upgrade options →](https://www.vizai.io/packages.html)

## Directory Structure

Community profiles are organized by category:

```
community/
├── technology/
├── professional-services/
├── financial/
├── healthcare/
├── manufacturing/
├── retail/
└── other/
```

## Questions?

- **Submit Your Business:** [Web form](https://www.vizai.io/onboarding-form.html) | [GitHub issue](https://github.com/vizai-io/business-registry/issues/new/choose)
- **Email:** hello@vizai.io
- **Documentation:** [/docs/](/docs/)
