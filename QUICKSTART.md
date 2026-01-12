# Quick Start Guide

Get the VizAI Business Registry deployed to GitHub in 5 minutes.

## Step 1: Push to GitHub (2 minutes)

### 1.1 Create the Repository on GitHub

Go to: https://github.com/organizations/vizai-io/repositories/new

```
Repository name: business-registry
Description: The structured business database designed for AI systems
Visibility: Public

⚠️ DO NOT check any of the initialize options
   (We already have README, .gitignore, and LICENSE)
```

Click **"Create repository"**

### 1.2 Push Your Local Repository

```bash
cd C:\Users\Jrwes\business-registry

# Add GitHub as remote
git remote add origin https://github.com/vizai-io/business-registry.git

# Push everything
git push -u origin main

# Verify it worked
git remote -v
```

**Expected output:**
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
...
To https://github.com/vizai-io/business-registry.git
 * [new branch]      main -> main
```

## Step 2: Configure Repository (2 minutes)

### 2.1 Set Repository Description

On your GitHub repository page, click the ⚙️ **gear icon** next to "About"

```
Description: The structured business database designed for AI systems
Website: https://www.vizai.io

Topics (add these):
  business-data
  ai-training
  company-profiles
  structured-data
  business-registry
  json-schema
  open-data
```

### 2.2 Enable Features

Go to: **Settings → General → Features**

Check these boxes:
- ✅ Issues
- ✅ Discussions (recommended)
- ✅ Projects (optional)

### 2.3 Verify Workflows

Go to: **Actions tab**

You should see:
- ✅ Validate Business Profiles
- ✅ Check for Duplicate Entries
- ✅ Update Index Files (if you committed indexes)

If workflows are disabled, click **"I understand my workflows, go ahead and enable them"**

## Step 3: Test the Setup (1 minute)

### 3.1 Test Issue Templates

Click: **Issues → New Issue**

You should see 3 templates:
1. 📝 Business Submission
2. ✏️ Correction Request
3. ✔️ Verification Request

Plus links to:
- VizAI Website
- Get Verified
- Submit via Web Form

### 3.2 View Your First Profile

Navigate to: `data/verified/technology/vizai.json`

You should see VizAI's profile with proper syntax highlighting.

### 3.3 Check Index Files

Navigate to: `data/index.json`

You should see the master index showing 1 profile.

## Step 4: Optional Enhancements

### Enable Branch Protection (Recommended)

**Settings → Branches → Add rule**

```
Branch name pattern: main

Protection rules:
✅ Require a pull request before merging
  - Required approvals: 1
✅ Require status checks to pass
  - Add: validate-schema
✅ Require conversation resolution before merging
```

This ensures all submissions are reviewed and validated.

### Enable GitHub Pages (Optional)

**Settings → Pages**

```
Source: Deploy from a branch
Branch: main
Folder: / (root)
```

This makes your documentation browsable at:
`https://vizai-io.github.io/business-registry/`

### Set Up Discussions (Optional)

**Discussions tab → Set up Discussions**

Create categories:
- 💡 Ideas - Feature requests
- 🙋 Q&A - Questions about the registry
- 📣 Announcements - Updates and news
- 🗣️ General - Everything else

## Troubleshooting

### "remote: Repository not found"

**Problem:** The repository doesn't exist yet or you don't have access.

**Solution:**
1. Make sure you created the repository on GitHub first
2. Check you're using the correct organization (vizai-io)
3. Verify you have push access to the organization

### "failed to push some refs"

**Problem:** Remote has commits you don't have locally.

**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

### Workflows not running

**Problem:** GitHub Actions are disabled by default for some orgs.

**Solution:**
1. Go to Actions tab
2. Click "I understand my workflows, go ahead and enable them"
3. Or: Settings → Actions → General → Allow all actions

### Issue templates not showing

**Problem:** Templates need to be in the main branch.

**Solution:**
```bash
# Verify files exist
ls .github/ISSUE_TEMPLATE/

# If they're there but not showing, wait 1-2 minutes
# GitHub takes time to process them after push
```

## What's Next?

Now that your registry is live, here's what to do:

### Immediate (Week 1)
1. ✅ **Announce internally** - Share with VizAI team
2. ✅ **Add 5-10 profiles** - Populate with example companies
3. ✅ **Test submission flow** - Create a test issue
4. ✅ **Update website** - Link to registry from vizai.io

### Short term (Week 2-3)
1. 🔧 **Build submission form** - See DEPLOYMENT.md for serverless approach
2. 📊 **Set up analytics** - Track repository stars, clones, issues
3. 📝 **Write blog post** - Announce the registry publicly
4. 🤝 **Onboard first customers** - Get verified tier customers added

### Medium term (Month 2)
1. 🤖 **Automate profile creation** - GitHub Actions from approved issues
2. 📈 **Add monitoring** - Track data quality and growth
3. 🔍 **Build search interface** - Website for browsing registry
4. 📢 **Marketing push** - Social media, blog posts, outreach

## Getting Help

- **Documentation:** See /docs/ directory
- **Deployment details:** See DEPLOYMENT.md
- **Questions:** hello@vizai.io
- **Issues:** Open a GitHub issue

## Success Checklist

Before announcing publicly, verify:

- [ ] Repository is public and accessible
- [ ] README renders correctly on GitHub
- [ ] Issue templates work
- [ ] Workflows are enabled and passing
- [ ] VizAI profile validates successfully
- [ ] Index files are generated
- [ ] Links to vizai.io work
- [ ] All documentation is clear

## Quick Commands Reference

```bash
# Add a new profile
cp schema/examples/technology-company.json data/community/technology/newco.json
# Edit the file with your business info
python tools/validation/validate-profile.py data/community/technology/newco.json
git add data/community/technology/newco.json
git commit -m "Add NewCo to community registry"
git push

# Regenerate indexes
python tools/automation/generate-indexes.py
git add data/**/index.json
git commit -m "Update indexes"
git push

# Validate all profiles
find data -name "*.json" -not -name "index.json" | \
xargs -I {} python tools/validation/validate-profile.py {}

# Count total profiles
find data -name "*.json" -not -name "index.json" | wc -l
```

---

**You're now running the VizAI Business Registry!** 🎉

Next: Read DEPLOYMENT.md for scaling to millions of profiles.
