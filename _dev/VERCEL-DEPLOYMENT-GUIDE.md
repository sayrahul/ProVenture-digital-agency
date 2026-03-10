# 🚀 ProVenture - Vercel Deployment Guide

**Complete guide to migrate from GoDaddy cPanel to Vercel**

**Date:** December 5, 2025  
**Current Setup:** GoDaddy cPanel + Cloudflare DNS  
**Target Setup:** Vercel Hosting + Cloudflare DNS

---

## 📋 Pre-Deployment Checklist

- [ ] Git repository is up to date
- [ ] All files committed to Git
- [ ] Vercel account created (https://vercel.com)
- [ ] Cloudflare account access available
- [ ] Subdomain already working on Vercel

---

## 🎯 Deployment Strategy

Since your **subdomain is already on Vercel**, we'll deploy the main domain alongside it.

### Architecture:
```
proventure.in (Main site) → Vercel
work.proventure.in (Portfolio) → Vercel (already deployed)
Backend API → Vercel Serverless Functions
```

---

## 📦 STEP 1: Prepare Your Project for Vercel

### 1.1 Create `vercel.json` Configuration

Create this file in your project root:

```json
{
  "version": 2,
  "name": "proventure-digital-agency",
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    },
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    }
  ]
}
```

### 1.2 Update `.gitignore` for Vercel

Add these lines to your `.gitignore`:

```
# Vercel
.vercel
.vercel/

# Local development
.env.local
.env.production.local
```

### 1.3 Create Backend API for Vercel

Since Vercel doesn't support long-running Flask apps, we'll convert to serverless functions.

**Create folder structure:**
```
api/
  submit.py
  __init__.py
```

---

## 📝 STEP 2: Convert Backend to Vercel Serverless

### 2.1 Create `api/submit.py`

```python
from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get content length
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate email
            if not data or not data.get('email'):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": False,
                    "error": "Email is required"
                }).encode())
                return
            
            # Create submission entry
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": data
            }
            
            # For Vercel, we'll use environment variables or external storage
            # For now, we'll just return success
            # In production, integrate with a database or external service
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "message": "Message received successfully!"
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": False,
                "error": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
```

### 2.2 Create `api/__init__.py`

```python
# Empty file to make it a Python package
```

### 2.3 Update `requirements.txt` (for Vercel)

Create `api/requirements.txt`:

```
# No additional requirements needed for basic serverless function
```

---

## 🌐 STEP 3: Deploy to Vercel

### Method 1: Deploy via Vercel CLI (Recommended)

#### 3.1 Install Vercel CLI

```bash
npm install -g vercel
```

#### 3.2 Login to Vercel

```bash
vercel login
```

#### 3.3 Deploy

```bash
# Navigate to your project directory
cd "c:\My Web Sites\ProVenture-digital-agency"

# Deploy to Vercel
vercel
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? **Select your account**
- Link to existing project? **N**
- What's your project's name? **proventure-digital-agency**
- In which directory is your code located? **./**
- Want to override settings? **N**

#### 3.4 Deploy to Production

```bash
vercel --prod
```

---

### Method 2: Deploy via Vercel Dashboard (Alternative)

#### 3.1 Push to GitHub

```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

#### 3.2 Import to Vercel

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your Git repository
4. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (leave empty)
   - **Output Directory:** ./
5. Click **"Deploy"**

---

## 🔧 STEP 4: Configure Custom Domain on Vercel

### 4.1 Add Domain in Vercel

1. Go to your project in Vercel Dashboard
2. Click **"Settings"** → **"Domains"**
3. Add domain: `proventure.in`
4. Add domain: `www.proventure.in`

### 4.2 Get Vercel DNS Records

Vercel will provide you with:
- **A Record** or **CNAME Record**
- **TXT Record** for verification

Example:
```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

---

## ☁️ STEP 5: Update Cloudflare DNS

### 5.1 Login to Cloudflare

1. Go to https://dash.cloudflare.com
2. Select your domain: `proventure.in`

### 5.2 Update DNS Records

**Remove old GoDaddy records:**
- Delete existing A records pointing to GoDaddy
- Delete existing CNAME records for www

**Add Vercel records:**

1. **For Root Domain (@):**
   - Type: `A`
   - Name: `@`
   - IPv4 address: `76.76.21.21` (Vercel's IP)
   - Proxy status: **DNS only** (gray cloud) ⚠️ IMPORTANT
   - TTL: Auto

2. **For WWW:**
   - Type: `CNAME`
   - Name: `www`
   - Target: `cname.vercel-dns.com`
   - Proxy status: **DNS only** (gray cloud) ⚠️ IMPORTANT
   - TTL: Auto

3. **Add Verification TXT Record** (if required by Vercel):
   - Type: `TXT`
   - Name: `@` or `_vercel`
   - Content: (provided by Vercel)
   - TTL: Auto

### 5.3 Important Cloudflare Settings

⚠️ **Critical:** Set Proxy Status to **DNS only** (gray cloud)
- Vercel needs direct DNS resolution
- Orange cloud (proxied) will cause SSL issues

**SSL/TLS Settings:**
1. Go to **SSL/TLS** → **Overview**
2. Set encryption mode to: **Full** or **Full (strict)**

**Page Rules (Optional):**
- Redirect `www` to non-www or vice versa
- Force HTTPS

---

## 🔐 STEP 6: Configure SSL Certificate

### 6.1 Vercel SSL (Automatic)

Vercel automatically provisions SSL certificates via Let's Encrypt.

**Wait for SSL:**
- Usually takes 5-10 minutes
- Check status in Vercel Dashboard → Domains

### 6.2 Verify HTTPS

Once deployed, verify:
- https://proventure.in ✅
- https://www.proventure.in ✅

---

## 📧 STEP 7: Handle Contact Form Submissions

Since we're using serverless, you have options:

### Option 1: Use Vercel KV (Key-Value Storage)

```bash
# Install Vercel KV
npm install @vercel/kv
```

Update `api/submit.py` to use Vercel KV for storage.

### Option 2: Use External Service

**Recommended services:**
- **Airtable** - Free tier, easy API
- **Google Sheets** - Via Google Apps Script
- **Supabase** - PostgreSQL database
- **MongoDB Atlas** - NoSQL database
- **EmailJS** - Send emails directly

### Option 3: Email Notifications (Recommended)

Use **SendGrid**, **Resend**, or **Mailgun** for email notifications.

**Example with Resend:**

```python
# api/submit.py
import os
from resend import Resend

resend = Resend(os.environ.get('RESEND_API_KEY'))

# In your handler:
resend.emails.send({
    "from": "contact@proventure.in",
    "to": "rahuljadhav44@gmail.com",
    "subject": "New Contact Form Submission",
    "html": f"<p><strong>Name:</strong> {data['name']}</p>..."
})
```

---

## 🧪 STEP 8: Testing

### 8.1 Test Deployment

```bash
# Test your Vercel deployment URL
curl https://proventure-digital-agency.vercel.app
```

### 8.2 Test Custom Domain

```bash
# Check DNS propagation
nslookup proventure.in

# Test HTTPS
curl -I https://proventure.in
```

### 8.3 Test Contact Form

1. Visit https://proventure.in/contact.html
2. Fill out and submit the form
3. Check Vercel logs: `vercel logs`

---

## 🔄 STEP 9: Update Contact Form API Endpoint

### 9.1 Update `contact.html`

Find the form submission JavaScript and update the API endpoint:

**Before (local):**
```javascript
fetch('http://localhost:5000/submit', {
```

**After (Vercel):**
```javascript
fetch('/api/submit', {
```

Or use environment-based URL:
```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/submit'
  : '/api/submit';

fetch(API_URL, {
```

---

## 📊 STEP 10: Monitor & Optimize

### 10.1 Vercel Analytics

Enable in Vercel Dashboard:
- Go to **Analytics** tab
- Enable Web Analytics
- Add analytics script to your HTML

### 10.2 Performance Optimization

**Vercel automatically handles:**
- ✅ Global CDN
- ✅ Automatic compression
- ✅ Image optimization
- ✅ Edge caching

**Additional optimizations:**
```json
// vercel.json
{
  "headers": [
    {
      "source": "/images/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## 🚨 Troubleshooting

### Issue: Domain not working

**Solution:**
1. Check DNS propagation: https://dnschecker.org
2. Verify Cloudflare proxy is **OFF** (gray cloud)
3. Wait 24-48 hours for full DNS propagation

### Issue: SSL Certificate Error

**Solution:**
1. Ensure Cloudflare SSL mode is **Full** or **Full (strict)**
2. Wait for Vercel to provision certificate (5-10 min)
3. Check Vercel Dashboard → Domains → SSL status

### Issue: API not working

**Solution:**
1. Check Vercel logs: `vercel logs`
2. Verify `api/submit.py` exists
3. Test API directly: `curl -X POST https://proventure.in/api/submit`

### Issue: 404 on pages

**Solution:**
1. Ensure all HTML files are in root directory
2. Check `vercel.json` routes configuration
3. Redeploy: `vercel --prod`

---

## 📝 Post-Deployment Checklist

- [ ] Main domain (proventure.in) working
- [ ] WWW redirect working
- [ ] HTTPS enabled and working
- [ ] Contact form submitting successfully
- [ ] All pages loading correctly
- [ ] Images and assets loading
- [ ] Custom CSS/JS working
- [ ] Analytics tracking
- [ ] Subdomain still working
- [ ] Old GoDaddy hosting can be cancelled

---

## 💰 Cost Comparison

### GoDaddy cPanel:
- ~$5-15/month
- Limited bandwidth
- Manual SSL renewal
- No CDN

### Vercel:
- **FREE** for hobby projects
- Unlimited bandwidth
- Automatic SSL
- Global CDN included
- **Pro:** $20/month (if needed)

---

## 🎯 Quick Command Reference

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy preview
vercel

# Deploy production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# Remove deployment
vercel rm [deployment-url]
```

---

## 📞 Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Vercel Support:** https://vercel.com/support
- **Cloudflare Docs:** https://developers.cloudflare.com

---

## ✅ Final Notes

1. **Keep GoDaddy active** for 1-2 weeks during transition
2. **Monitor traffic** to ensure smooth migration
3. **Update Google Search Console** with new hosting
4. **Test thoroughly** before cancelling GoDaddy
5. **Backup everything** before making changes

---

**Deployment Date:** _____________  
**Vercel URL:** _____________  
**Status:** ⬜ In Progress | ⬜ Completed

---

**Good luck with your deployment! 🚀**
