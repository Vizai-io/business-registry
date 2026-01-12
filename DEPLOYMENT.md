# Deployment & Scaling Guide

This guide covers deploying the VizAI Business Registry to GitHub and scaling it to support millions of business profiles.

## Phase 1: Initial GitHub Deployment

### Step 1: Create GitHub Repository

1. **Go to GitHub:**
   - Navigate to https://github.com/organizations/vizai-io/repositories/new
   - (Or create under your personal account first, then transfer)

2. **Repository Settings:**
   ```
   Repository name: business-registry
   Description: The structured business database designed for AI systems
   Visibility: Public

   DO NOT initialize with:
   - README (we already have one)
   - .gitignore (we already have one)
   - License (we already have one)
   ```

3. **Click "Create repository"**

### Step 2: Push Local Repository

```bash
cd C:\Users\Jrwes\business-registry

# Add the remote
git remote add origin https://github.com/vizai-io/business-registry.git

# Push to GitHub
git push -u origin main

# Verify it worked
git remote -v
```

### Step 3: Configure Repository Settings

**Go to: Settings → General**

1. **Features:**
   - ✅ Issues
   - ✅ Projects (optional)
   - ✅ Discussions (recommended for community)
   - ✅ Sponsorships (if you want GitHub Sponsors)

2. **Pull Requests:**
   - ✅ Allow squash merging
   - ✅ Allow auto-merge
   - ✅ Automatically delete head branches

3. **Social Preview:**
   - Upload a preview image (create one with registry logo/concept)

**Go to: Settings → Pages**

4. **GitHub Pages (optional):**
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)
   - This will make documentation browsable

**Go to: Repository main page**

5. **About section (click gear icon):**
   - Website: https://www.vizai.io
   - Topics: `business-data` `ai-training` `company-profiles` `structured-data` `business-registry` `json-schema` `open-data`
   - ✅ Use your repository topics

### Step 4: Set Up Issue Templates

Issue templates are already in `.github/ISSUE_TEMPLATE/`, but we need a config file:

Create `.github/ISSUE_TEMPLATE/config.yml`:
```yaml
blank_issues_enabled: false
contact_links:
  - name: VizAI Website
    url: https://www.vizai.io
    about: Visit our website to learn more about VizAI services
  - name: Get Verified
    url: https://www.vizai.io/packages.html
    about: Purchase professional verification for your business
  - name: Submit via Web Form
    url: https://www.vizai.io/onboarding-form.html
    about: Submit your business using our guided web form
```

### Step 5: Set Up Branch Protection (Recommended)

**Go to: Settings → Branches → Add branch protection rule**

```
Branch name pattern: main

Protection rules:
✅ Require a pull request before merging
  - Required approvals: 1
✅ Require status checks to pass before merging
  - Add: validate-schema
  - Add: check-duplicates
✅ Require conversation resolution before merging
✅ Do not allow bypassing the above settings (for team members)
```

This ensures all submissions go through validation.

## Phase 2: Scaling Architecture

### Directory Structure for Scale

Current structure works up to ~10,000 profiles. For millions, we need hierarchical organization:

```
data/
├── verified/
│   ├── technology/
│   │   ├── a/              # Companies starting with 'a'
│   │   │   ├── acme.json
│   │   │   ├── apple.json
│   │   ├── b/
│   │   ├── c/
│   │   └── ...
│   ├── professional-services/
│   │   ├── a/
│   │   ├── b/
│   └── ...
```

**Implementation:**
- Organize by first letter of filename
- Keeps directories under 1,000 files each
- Scales to millions without git performance issues

### File Naming Convention

For 1M+ profiles, enforce consistent naming:

```
Format: {domain-without-tld}.json

Examples:
✅ acme.json         (for acme.com)
✅ vizai.json        (for vizai.io)
✅ bank-of-america.json  (for bankofamerica.com)

Avoid:
❌ acme-com.json
❌ Acme.json
❌ acme_inc.json
```

### Index Files for Discovery

Generate index files for faster querying:

```
data/verified/technology/index.json
```

```json
{
  "category": "technology",
  "tier": "verified",
  "lastUpdated": "2025-01-06",
  "count": 1245,
  "profiles": [
    {
      "file": "a/acme.json",
      "domain": "acme.com",
      "commonName": "Acme",
      "lastVerified": "2025-01-06"
    }
  ]
}
```

Auto-generate these via GitHub Actions.

## Phase 3: Automated Intake System

### Architecture Overview

```
Web Form → API Gateway → Validation → GitHub API → Repository
              ↓
         Email Queue
              ↓
        Notification
```

### Option A: Serverless (Recommended for Start)

**Stack:**
- **Form:** Typeform / Google Forms / Custom React form
- **Backend:** Vercel Functions / Netlify Functions / AWS Lambda
- **Storage:** GitHub API (for submissions)
- **Queue:** GitHub Issues (simple) or AWS SQS (robust)

**Flow:**
1. User fills form at vizai.io/onboarding-form.html
2. Form submits to serverless function
3. Function validates data
4. Creates GitHub issue with submission
5. Human reviews and approves
6. Manual or automated PR creation

### Option B: Full Application (For Scale)

**Stack:**
- **Frontend:** Next.js app hosted on Vercel
- **Backend:** Node.js API (Express/Fastify)
- **Database:** PostgreSQL (staging submissions)
- **Queue:** Bull/BullMQ with Redis
- **Storage:** GitHub API + S3 backup

**Flow:**
1. User submits form
2. API validates and stores in PostgreSQL
3. Creates review queue entry
4. Admin dashboard for review
5. Approved submissions → automated PR to GitHub
6. Merge triggers index rebuild

### Implementation: Simple Serverless Form

I'll create a basic implementation you can deploy:

**File: `web/submit-business.html`** (host on vizai.io)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Submit Business - VizAI Registry</title>
</head>
<body>
    <h1>Submit Your Business to VizAI Registry</h1>
    <form id="businessForm">
        <!-- Form fields matching schema -->
        <button type="submit">Submit</button>
    </form>

    <script>
    document.getElementById('businessForm').onsubmit = async (e) => {
        e.preventDefault();
        // Collect form data
        const formData = {/* ... */};

        // Submit to API
        await fetch('https://api.vizai.io/registry/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
    };
    </script>
</body>
</html>
```

**File: `api/submit.js`** (Vercel/Netlify function)
```javascript
const { Octokit } = require('@octokit/rest');

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({error: 'Method not allowed'});
    }

    const submission = req.body;

    // Validate basic structure
    if (!submission.legalName || !submission.domain) {
        return res.status(400).json({error: 'Missing required fields'});
    }

    // Create GitHub issue
    const octokit = new Octokit({
        auth: process.env.GITHUB_TOKEN
    });

    await octokit.issues.create({
        owner: 'vizai-io',
        repo: 'business-registry',
        title: `[SUBMISSION] ${submission.legalName}`,
        body: generateIssueBody(submission),
        labels: ['submission', 'community']
    });

    // Send confirmation email (optional)

    return res.status(200).json({
        success: true,
        message: 'Submission received. You will be notified when processed.'
    });
}
```

## Phase 4: Automation & Workflows

### GitHub Actions for Profile Generation

**File: `.github/workflows/create-profile.yml`**

```yaml
name: Create Profile from Issue

on:
  issues:
    types: [labeled]

jobs:
  create-profile:
    if: contains(github.event.issue.labels.*.name, 'approved')
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Parse issue body
      id: parse
      run: |
        # Extract data from issue body
        python tools/automation/parse-submission.py "${{ github.event.issue.body }}"

    - name: Generate profile JSON
      run: |
        python tools/automation/generate-profile.py \
          --output "data/community/technology/company.json"

    - name: Validate profile
      run: |
        python tools/validation/validate-profile.py \
          data/community/technology/company.json

    - name: Create Pull Request
      uses: peter-evans/create-pull-request@v5
      with:
        commit-message: "Add profile: ${{ steps.parse.outputs.companyName }}"
        title: "New Community Profile: ${{ steps.parse.outputs.companyName }}"
        body: "Automatically generated from issue #${{ github.event.issue.number }}"
        branch: "profile/${{ steps.parse.outputs.slug }}"
```

### Automated Index Generation

**File: `.github/workflows/update-indexes.yml`**

```yaml
name: Update Index Files

on:
  push:
    branches: [main]
    paths:
      - 'data/**/*.json'
  workflow_dispatch:

jobs:
  update-indexes:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Generate indexes
      run: python tools/automation/generate-indexes.py

    - name: Commit indexes
      run: |
        git config user.name "VizAI Bot"
        git config user.email "bot@vizai.io"
        git add data/**/index.json
        git commit -m "Update indexes [skip ci]" || echo "No changes"
        git push
```

## Phase 5: Performance Optimization

### Git LFS for Large Scale

When you reach 100k+ profiles, consider Git LFS:

```bash
# Install Git LFS
git lfs install

# Track JSON files
git lfs track "data/**/*.json"

# Commit .gitattributes
git add .gitattributes
git commit -m "Enable Git LFS for profile data"
```

### Alternative: Hybrid Storage

**GitHub:** Store metadata and index
**S3/Cloud Storage:** Store full profiles

```json
// data/verified/technology/index.json
{
  "profiles": [
    {
      "domain": "acme.com",
      "fullProfile": "https://registry-data.vizai.io/verified/technology/acme.json"
    }
  ]
}
```

### Database Replication

For AI training and bulk access:

- **BigQuery:** Upload snapshots monthly
- **Snowflake:** Sync for analytics
- **PostgreSQL:** Public read replica
- **API:** REST API for real-time queries

## Phase 6: Monitoring & Maintenance

### Metrics to Track

1. **Registry growth:** Profiles added per week
2. **Validation pass rate:** % of submissions that validate
3. **Quality scores:** Average quality score trend
4. **API usage:** Downloads, clones, API calls
5. **Issue response time:** Time to process submissions

### Automated Health Checks

```yaml
# .github/workflows/health-check.yml
name: Registry Health Check

on:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Validate all profiles
      run: |
        find data -name "*.json" -type f | \
        xargs -I {} python tools/validation/validate-profile.py {}

    - name: Check for broken links
      run: python tools/monitoring/check-sources.py

    - name: Generate health report
      run: python tools/monitoring/health-report.py
```

## Phase 7: Community Management

### Review Queue Management

Use GitHub Projects to manage submissions:

1. **Create Project Board:**
   - Columns: Submitted → Under Review → Approved → Published

2. **Automation:**
   - New issues → "Submitted"
   - Labeled "approved" → "Approved"
   - PR merged → "Published"

### Documentation Site

Consider building a dedicated docs site:

- **Docusaurus:** https://docusaurus.io
- **GitBook:** https://gitbook.com
- **VitePress:** https://vitepress.dev

Host schema browser, search, and guides.

## Quick Start Commands

### Push to GitHub (Do this now)

```bash
cd C:\Users\Jrwes\business-registry

# Create repository on GitHub first, then:
git remote add origin https://github.com/vizai-io/business-registry.git
git push -u origin main
```

### Verify Deployment

```bash
# Check workflows
git log --oneline
git remote -v

# Test validation locally
python tools/validation/validate-profile.py data/verified/technology/vizai.json
```

### Monitor After Push

- Check Actions tab: Workflows should be visible
- Create a test issue: Should show templates
- Star your own repo: Verify it's public

## Next Steps Priority

**Week 1:**
1. ✅ Push to GitHub
2. ✅ Configure repository settings
3. ✅ Create 5-10 more example profiles
4. ✅ Test issue templates

**Week 2:**
1. Build simple submission form
2. Set up serverless function
3. Create automation scripts
4. Test end-to-end flow

**Week 3:**
1. Add monitoring
2. Generate indexes
3. Create documentation site
4. Announce publicly

## Questions?

Email: hello@vizai.io
