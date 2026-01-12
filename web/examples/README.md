# Web Form Examples

This directory contains example web forms for submitting businesses to the VizAI Registry.

## Files

### intake-form.html

A complete, standalone HTML form for business submissions.

**Features:**
- All required and optional fields
- Client-side validation
- Character counter for elevator pitch
- Responsive design
- Ready to integrate with your API

**Usage:**

1. **Host on your website:**
   ```
   Copy to: www.vizai.io/onboarding-form.html
   ```

2. **Update the API endpoint:**
   In the JavaScript section, change:
   ```javascript
   const response = await fetch('https://api.vizai.io/registry/submit', {
   ```
   To your actual API endpoint.

3. **Deploy backend:**
   See `/web/examples/api-handler.js` for a serverless function example.

## Integration Options

### Option 1: Direct to GitHub Issues (Simplest)

Modify the form to create GitHub issues directly:

```javascript
// Create GitHub issue via Octokit
const octokit = new Octokit({ auth: 'YOUR_TOKEN' });

await octokit.issues.create({
  owner: 'vizai-io',
  repo: 'business-registry',
  title: `[SUBMISSION] ${data.legalName}`,
  body: generateIssueBody(data),
  labels: ['submission', 'community']
});
```

**Pros:** Simple, no backend needed
**Cons:** Exposes GitHub token, limited customization

### Option 2: Serverless Function (Recommended)

Use a serverless function to process submissions:

**Deploy to Vercel:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy function
cd web/examples
vercel --prod
```

**Deploy to Netlify:**
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy function
cd web/examples
netlify deploy --prod
```

**Pros:** Secure, scalable, free tier available
**Cons:** Requires deploying function

### Option 3: Full Backend (For Scale)

Build a complete API with:
- Express.js / Fastify
- PostgreSQL for staging
- Email notifications
- Admin dashboard

See `DEPLOYMENT.md` for full architecture.

## Customization

### Branding

Update the CSS to match your brand:

```css
/* Change primary color */
button {
    background: #YOUR_BRAND_COLOR;
}

h1 {
    color: #YOUR_BRAND_COLOR;
}
```

### Fields

Add custom fields by:

1. Adding HTML input:
```html
<div class="form-group">
    <label for="customField">Custom Field</label>
    <input type="text" id="customField" name="customField">
</div>
```

2. Including in submission data:
```javascript
const data = {
    // ... other fields
    customField: formData.get('customField')
};
```

### Validation

Add custom validation:

```javascript
form.addEventListener('submit', function(e) {
    // Custom validation
    const domain = formData.get('primaryDomain');
    if (!domain.includes('.')) {
        alert('Please enter a valid domain');
        e.preventDefault();
        return;
    }

    // Continue with submission...
});
```

## Testing

### Test Locally

1. Open `intake-form.html` in a browser
2. Fill out the form
3. Open browser console to see submission data
4. Mock the API response to test success/error states

### Mock API for Testing

```javascript
// Add to the fetch section
if (window.location.hostname === 'localhost') {
    // Mock response for local testing
    console.log('Submission data:', data);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate delay
    // Simulate success
    // throw new Error('Test error'); // Simulate error
} else {
    // Real API call
    const response = await fetch('https://api.vizai.io/registry/submit', {
        // ...
    });
}
```

## Security Considerations

1. **Rate Limiting:** Implement rate limiting on your API
2. **CAPTCHA:** Add reCAPTCHA to prevent spam
3. **Input Sanitization:** Sanitize all inputs server-side
4. **Domain Verification:** Verify domain ownership for paid tiers
5. **Email Verification:** Send confirmation email with verify link

## Analytics

Track form usage:

```javascript
// Google Analytics
gtag('event', 'form_start', {
    'event_category': 'registry_submission'
});

gtag('event', 'form_submit', {
    'event_category': 'registry_submission',
    'event_label': data.legalName
});
```

## Questions?

- **Email:** hello@vizai.io
- **Documentation:** /docs/
- **GitHub:** https://github.com/vizai-io/business-registry
