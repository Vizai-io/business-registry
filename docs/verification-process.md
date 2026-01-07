# Verification Process

This document explains how VizAI verifies business profiles and the differences between verification tiers.

## Overview

The VizAI Business Registry has three verification tiers:

1. **Community Tier (Free)** - Self-reported information
2. **Verified Tier (Paid)** - Domain ownership verification + human review
3. **Enterprise Tier (Custom)** - Comprehensive verification + managed service

## Community Tier (Free)

### Process

1. **Submission**
   - Submit via web form, GitHub issue, or pull request
   - Provide required business information
   - No payment required

2. **Basic Validation**
   - Schema validation (correct format)
   - Domain accessibility check
   - No duplicate detection
   - Basic information review

3. **Publication**
   - Profile added to `/data/community/`
   - Status: `"status": "community"`
   - Tier: `"tier": "community"`
   - No quality score assigned

### What's Included

✅ Free listing in the registry
✅ Schema-compliant profile
✅ Publicly accessible
✅ Version history via Git
❌ No verification badge
❌ No quality score
❌ No monitoring
❌ No guaranteed review time

### Timeline
- **5-7 business days** for review and publication

## Verified Tier (Paid)

### Pricing
- **Tier 0:** $495 CAD (one-time snapshot + verified entry)
- **Tier 1:** $650 CAD/month (verified entry + ongoing monitoring)

[View full pricing →](https://www.vizai.io/packages.html)

### Process

#### 1. Purchase & Onboarding
- Purchase Tier 0 or Tier 1 service
- Receive onboarding email
- Complete detailed onboarding form
- Provide authoritative sources

#### 2. Domain Verification
Choose one method:

**Option A: DNS TXT Record**
```
Type: TXT
Name: _vizai-verify
Value: vizai-verification=[provided-code]
TTL: 3600
```

**Option B: Meta Tag**
Add to your website's `<head>`:
```html
<meta name="vizai-verification" content="[provided-code]" />
```

**Option C: Email Verification**
Receive verification code at email from your business domain.

#### 3. Human Review
VizAI analyst reviews:
- Domain ownership proof
- Information accuracy
- Source documentation
- Completeness
- Consistency across sources

#### 4. Quality Scoring
Profile receives quality score (0-100) based on:
- **Completeness** (30 points) - All recommended fields filled
- **Source quality** (25 points) - Multiple authoritative sources
- **Accuracy** (25 points) - Cross-verified information
- **Recency** (20 points) - Information is current

Score requirements:
- **90-100:** Comprehensive, exemplary profile
- **85-89:** Complete, well-documented
- **75-84:** Solid information with minor gaps
- **Below 75:** Does not meet verified standards

#### 5. Publication
- Profile added to `/data/verified/[category]/`
- Status: `"status": "verified"`
- Tier: `"tier": "verified"`
- Quality score: 85-100
- Verification date recorded

### What's Included

**Tier 0 ($495 CAD one-time):**
✅ Domain ownership verification
✅ Human analyst review
✅ Quality score (85-100)
✅ Verified badge
✅ Premium placement
✅ Source documentation
✅ AI Visibility Snapshot report

**Tier 1 ($650 CAD/month):**
✅ Everything in Tier 0, plus:
✅ Monthly drift monitoring
✅ Automatic accuracy checks
✅ Priority updates
✅ Quarterly reports
✅ Ongoing optimization

### Timeline
- **1-2 business days** after purchase and domain verification

## Enterprise Tier (Custom Pricing)

### When You Need Enterprise

- Multiple business units or subsidiaries
- Complex organizational structure
- Global operations with many locations
- Regulatory compliance requirements
- Executive reporting needs
- Dedicated account management

### Process

#### 1. Consultation
- Initial needs assessment call
- Review requirements and complexity
- Determine custom pricing
- Define success criteria

#### 2. Custom Verification
Tailored verification process may include:
- Multi-stakeholder verification
- Legal department review
- Custom verification methods
- Compliance documentation
- Audit trail requirements

#### 3. Enhanced Profile Creation
- Comprehensive profile with extended fields
- Multiple business units
- Detailed location tracking
- Acquisition/merger history
- Custom metadata

#### 4. Ongoing Management
- Dedicated account manager
- White-glove service
- Priority support
- Custom monitoring rules
- Quarterly executive reports

### What's Included

✅ Everything in Tier 1, plus:
✅ Dedicated account manager
✅ Custom verification workflow
✅ Multi-stakeholder support
✅ Enhanced profile fields
✅ Executive reporting
✅ SLA guarantees
✅ Priority support
✅ Custom monitoring rules
✅ Compliance documentation
✅ Team training

### Timeline
- **Custom** based on complexity
- Typically 1-2 weeks for initial setup

## Verification Methods Explained

### Domain Ownership

**Purpose:** Prove you control the domain you claim

**Methods:**
1. DNS TXT record - Best for technical teams
2. Meta tag - Easy for marketing teams
3. Email verification - Alternative if above aren't feasible

**Why it matters:**
- Prevents impersonation
- Confirms authorization
- Validates business legitimacy

### Human Review

**What we check:**
- Information accuracy vs. sources
- Consistency across different sources
- Completeness of profile
- Quality of descriptions (factual, not marketing)
- Source credibility
- Recent-ness of information

**Sources we prefer:**
- Official company website
- Press releases
- Regulatory filings
- Crunchbase (verified)
- LinkedIn company pages
- News articles from credible outlets

### Ongoing Monitoring (Tier 1+)

**How it works:**
- Monthly automated checks
- Domain still accessible
- Information drift detection
- Source link validation
- AI representation scanning

**What triggers alerts:**
- Website content changes significantly
- Sources become unavailable
- AI systems describe business differently
- Domain changes or expires
- Major business changes detected

## Maintaining Your Verified Status

### For Tier 0 (One-time)
- Verification valid for 12 months
- Submit update request if information changes
- Re-verification required annually (can upgrade to Tier 1)

### For Tier 1+ (Ongoing)
- Automatic monitoring included
- Updates processed monthly
- Drift alerts sent to you
- Quarterly accuracy reports
- Profile always current

### Making Updates

**Small changes** (contact info, description tweaks):
- Submit via GitHub issue
- Processed within 3-5 business days
- No re-verification needed

**Major changes** (rebrand, acquisition, restructure):
- Contact your account manager (Enterprise)
- Submit detailed update request (Verified)
- May require re-verification
- Updated within 1 week

## Common Questions

**Q: How long does verification take?**
A: 1-2 business days after you complete domain verification and provide required information.

**Q: What if I can't add DNS records or meta tags?**
A: Contact us at hello@vizai.io. We can arrange email verification or other methods.

**Q: Can I verify a subsidiary's profile?**
A: Yes, if you control the subsidiary's domain. Enterprise tier is best for multi-subsidiary verification.

**Q: What happens if my verification expires?**
A: Profile moves to community tier. You can re-verify anytime.

**Q: Can I upgrade from Community to Verified?**
A: Yes! Purchase Tier 0 or 1 and we'll upgrade your existing profile.

**Q: What if information in my profile becomes outdated?**
A: Tier 1+ includes automatic monitoring. Otherwise, submit a correction request.

**Q: Do you verify businesses outside the US?**
A: Yes, VizAI verifies businesses globally.

## Next Steps

- **Get Verified:** [View pricing](https://www.vizai.io/packages.html)
- **Submit for Free:** [Community tier](https://www.vizai.io/onboarding-form.html)
- **Enterprise Inquiry:** Email hello@vizai.io
- **Questions:** hello@vizai.io
