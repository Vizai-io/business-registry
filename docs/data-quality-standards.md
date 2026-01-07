# Data Quality Standards

The VizAI Business Registry maintains high data quality standards to ensure AI systems can trust and use the information effectively.

## Quality Principles

1. **Accuracy** - All information must be factual and current
2. **Verifiability** - Every claim must trace to a credible source
3. **Completeness** - Profiles should fill all applicable fields
4. **Objectivity** - Descriptions must be neutral, not marketing language
5. **Consistency** - Information must align across all sources

## Quality Scoring

Verified profiles receive a quality score (0-100) based on:

### Completeness (30 points)

**Required fields (baseline):**
- businessIdentifier (all fields)
- description (elevator + detailed)
- verification metadata
- registry metadata

**Scoring:**
- Required fields only: **15/30 points**
- + Recommended fields (location, contact, offerings): **25/30 points**
- + Optional fields (leadership, founding story, sources): **30/30 points**

**Recommended fields:**
- location.headquarters
- contact.email
- offerings.primary
- offerings.targetCustomers

**Optional but valuable:**
- description.founding
- description.yearFounded
- leadership (founders, CEO)
- businessIdentifier.identifiers (LinkedIn, etc.)

### Source Quality (25 points)

**Scoring criteria:**

| Sources | Quality | Points |
|---------|---------|--------|
| No sources | Poor | 0/25 |
| 1 source (website only) | Basic | 10/25 |
| 2-3 diverse sources | Good | 18/25 |
| 4+ authoritative sources | Excellent | 25/25 |

**Source quality hierarchy:**
1. **Official website** - Company's own content
2. **Regulatory filings** - SEC, business registrations
3. **Press releases** - Official announcements
4. **Verified platforms** - Crunchbase, LinkedIn verified
5. **News articles** - Credible media outlets
6. **Other** - Blog posts, third-party sites

### Accuracy (25 points)

**Verified through:**
- Cross-reference multiple sources
- Domain ownership verification
- Human analyst review
- Fact-checking against authoritative sources

**Scoring:**
- Unverified/community: **0/25 points**
- Email verified: **10/25 points**
- Domain ownership verified: **18/25 points**
- Domain + human review: **25/25 points**

**Common accuracy issues:**
- Outdated information (old product names, defunct locations)
- Conflicting information across sources
- Marketing language vs. factual descriptions
- Unverifiable claims (e.g., "best in industry")

### Recency (20 points)

**Scoring:**

| Last Verified | Points |
|---------------|--------|
| Within 30 days | 20/20 |
| Within 90 days | 15/20 |
| Within 180 days | 10/20 |
| Within 365 days | 5/20 |
| Over 1 year | 0/20 |

**Why recency matters:**
- Businesses change (products, leadership, locations)
- Sources become outdated
- Websites get restructured
- Information drifts over time

## Writing Quality Descriptions

### Elevator Pitch (280 characters max)

**Good examples:**
- ✅ "Acme provides cloud-based project management software for distributed teams."
- ✅ "Sterling Consulting advises mid-market companies on digital transformation strategy."
- ✅ "VizAI helps businesses control how AI systems describe them through visibility monitoring."

**Bad examples:**
- ❌ "We're revolutionizing the industry with cutting-edge AI-powered solutions!" (Marketing language)
- ❌ "A company that makes software." (Too vague)
- ❌ "Founded in 2020, Acme is a venture-backed SaaS company in the productivity space..." (Too much detail, save for detailed description)

**Best practices:**
- Start with company name or product
- State what you do clearly
- Mention who you serve
- Avoid superlatives ("best", "leading", "revolutionary")
- Use factual language

### Detailed Description (2-3 paragraphs)

**Structure:**

**Paragraph 1: What & Who**
- What does the business do?
- What products/services do you offer?
- Who do you serve?

**Paragraph 2: Context & Scale**
- How do you do it?
- What's your approach or methodology?
- Scale indicators (customer count, locations, etc.)

**Paragraph 3: Differentiation**
- What makes you unique?
- Key strengths or focus areas
- Notable achievements (if verifiable)

**Example (Good):**
```
Acme is a B2B SaaS company that provides project management and collaboration
software designed specifically for distributed teams. The platform includes task
management, video conferencing, document collaboration, and time tracking features
integrated into a single interface.

Founded by former remote workers frustrated with existing tools, Acme focuses on
asynchronous-first workflows that respect different time zones and work schedules.
The company serves over 5,000 teams across 40 countries.

Acme differentiates through its emphasis on async communication, deep integrations
with developer tools, and transparent pricing with no user limits.
```

**What to avoid:**
- ❌ Marketing buzzwords ("synergy", "paradigm shift", "game-changing")
- ❌ Unverifiable claims ("fastest growing", "industry-leading")
- ❌ Feature lists without context
- ❌ Comparison to competitors
- ❌ Future promises without current facts

## Source Documentation

### Required Source Metadata

For each source, provide:
- **type** - Category of source
- **url** - Direct link
- **accessed** - Date accessed (YYYY-MM-DD)
- **description** - What information came from this source

### Source Types

**official-website**
- Company's own website
- About page, product pages
- Highest credibility for basic facts

**press-release**
- Official company announcements
- Good for announcements, funding, launches

**linkedin**
- LinkedIn company page
- Good for employee count, locations

**crunchbase**
- Crunchbase company profile
- Good for funding, basics

**news-article**
- Credible news outlets
- Good for third-party validation

**other**
- Everything else
- Explain in description

### Example Source Documentation

```json
{
  "sources": [
    {
      "type": "official-website",
      "url": "https://acme.com/about",
      "accessed": "2025-01-06",
      "description": "Company description, team information, and product details"
    },
    {
      "type": "crunchbase",
      "url": "https://www.crunchbase.com/organization/acme",
      "accessed": "2025-01-06",
      "description": "Funding rounds, employee count, and founding date"
    },
    {
      "type": "press-release",
      "url": "https://acme.com/press/series-a",
      "accessed": "2025-01-06",
      "description": "Series A funding announcement and growth metrics"
    }
  ]
}
```

## Common Quality Issues

### Issue: Outdated Information

**Problem:**
- Profile says "50 employees" but company now has 200
- Lists old product that was discontinued
- Founder who left listed as current CEO

**Solution:**
- Submit correction request
- Provide source showing current information
- Verified tier: automatic drift monitoring catches this

### Issue: Marketing Language

**Problem:**
```json
{
  "description": {
    "elevator": "We're revolutionizing productivity with AI-powered innovation!"
  }
}
```

**Solution:**
```json
{
  "description": {
    "elevator": "Acme provides AI-assisted task management software for teams."
  }
}
```

### Issue: Vague Descriptions

**Problem:**
```json
{
  "description": {
    "detailed": "We help businesses succeed with technology solutions."
  }
}
```

**Solution:**
```json
{
  "description": {
    "detailed": "Acme provides cloud infrastructure management software for
    DevOps teams. Our platform automates server provisioning, monitoring, and
    scaling across AWS, Google Cloud, and Azure..."
  }
}
```

### Issue: Missing Sources

**Problem:**
- Claims about employee count, funding, or customers without sources

**Solution:**
- Add sources array with links to verify claims
- Link to About page, Crunchbase, press releases

### Issue: Inconsistent Information

**Problem:**
- Website says "founded 2020"
- Crunchbase says "founded 2019"
- Profile doesn't address discrepancy

**Solution:**
- Use most authoritative source (usually company's own statement)
- Note discrepancy in internal notes if needed
- Contact company for clarification

## Quality Review Checklist

Before submitting a profile, check:

**Schema Compliance:**
- [ ] Validates against schema (run `validate-profile.py`)
- [ ] All required fields present
- [ ] Dates in YYYY-MM-DD format
- [ ] URLs properly formatted

**Completeness:**
- [ ] Elevator pitch under 280 characters
- [ ] Detailed description is 2-3 substantial paragraphs
- [ ] Location information provided
- [ ] Contact email provided
- [ ] At least 1-2 products/services listed

**Accuracy:**
- [ ] All information is current (within last year)
- [ ] No conflicting information across fields
- [ ] Claims are verifiable
- [ ] Domain is accessible

**Sources:**
- [ ] At least 2 sources provided
- [ ] Sources are credible and accessible
- [ ] Each source has description of what it verifies
- [ ] Access dates are current

**Language Quality:**
- [ ] Neutral, factual tone (not marketing)
- [ ] No superlatives without proof
- [ ] Clear, specific descriptions
- [ ] Proper grammar and spelling

## Continuous Improvement

The VizAI Business Registry evolves based on:
- Feedback from AI systems using the data
- Quality metrics from verification process
- Community contributions and corrections
- Industry best practices

We regularly update these standards to improve data quality.

## Questions?

- **Data quality questions:** hello@vizai.io
- **Report quality issues:** [GitHub issues](https://github.com/vizai-io/business-registry/issues)
- **Request correction:** Use [correction template](/.github/ISSUE_TEMPLATE/correction-request.md)
