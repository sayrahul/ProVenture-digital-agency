# 🚀 Quick Vercel Deployment Steps

**Fast-track guide for deploying ProVenture to Vercel**

---

## ⚡ Quick Start (5 Minutes)

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Deploy

```bash
cd "c:\My Web Sites\ProVenture-digital-agency"
vercel
```

Follow prompts:
- Project name: `proventure-digital-agency`
- Directory: `./`
- Override settings: `N`

### 4. Deploy to Production

```bash
vercel --prod
```

---

## 🌐 Configure Domain

### In Vercel Dashboard:

1. Go to **Settings** → **Domains**
2. Add: `proventure.in`
3. Add: `www.proventure.in`
4. Copy the DNS records shown

### In Cloudflare:

1. Go to **DNS** settings
2. **Delete** old GoDaddy A records
3. **Add** Vercel records:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   Proxy: OFF (gray cloud)
   
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   Proxy: OFF (gray cloud)
   ```

4. **Important:** Turn OFF Cloudflare proxy (gray cloud icon)

---

## ✅ Verify

1. Wait 5-10 minutes for DNS propagation
2. Visit: https://proventure.in
3. Test contact form
4. Check Vercel logs: `vercel logs`

---

## 📝 Files Created

- ✅ `vercel.json` - Configuration
- ✅ `api/submit.py` - Serverless function
- ✅ `api/__init__.py` - Python package
- ✅ `api/requirements.txt` - Dependencies

---

## 🔧 Update Contact Form

The contact form will automatically use `/api/submit` endpoint.

No changes needed if using relative URLs!

---

## 📊 Monitor

View logs in real-time:
```bash
vercel logs --follow
```

---

## 🆘 Troubleshooting

**Domain not working?**
- Check Cloudflare proxy is OFF
- Wait 24 hours for DNS propagation
- Run: `nslookup proventure.in`

**API not working?**
- Check: `vercel logs`
- Test: `curl -X POST https://proventure.in/api/submit -d '{"email":"test@test.com"}'`

---

**Full guide:** See `VERCEL-DEPLOYMENT-GUIDE.md`
