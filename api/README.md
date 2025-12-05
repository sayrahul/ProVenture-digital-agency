# ProVenture API - Vercel Serverless Functions

This directory contains serverless functions for the ProVenture website deployed on Vercel.

## 📁 Structure

```
api/
├── submit.py          # Contact form submission handler
├── __init__.py        # Python package marker
└── requirements.txt   # Python dependencies
```

## 🚀 Endpoints

### POST /api/submit

Handles contact form submissions.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Inc",
  "phone": "+1234567890",
  "interest": ["Web Design", "Digital Marketing"],
  "message": "I'm interested in your services..."
}
```

**Response (Success):**
```json
{
  "ok": true,
  "message": "Thank you! Your message has been received successfully."
}
```

**Response (Error):**
```json
{
  "ok": false,
  "error": "Email is required"
}
```

## 🔧 Local Testing

Vercel CLI provides local development:

```bash
# Install Vercel CLI
npm install -g vercel

# Run local dev server
vercel dev
```

Visit: http://localhost:3000/api/submit

## 📝 Adding Email Notifications

To add email notifications, update `requirements.txt`:

### Option 1: Resend (Recommended)

```txt
resend==0.7.0
```

Update `submit.py`:
```python
import os
from resend import Resend

resend = Resend(os.environ.get('RESEND_API_KEY'))

# In handler:
resend.emails.send({
    "from": "contact@proventure.in",
    "to": "rahuljadhav44@gmail.com",
    "subject": "New Contact Form Submission",
    "html": f"<p><strong>Name:</strong> {data['name']}</p>"
})
```

Add environment variable in Vercel:
```bash
vercel env add RESEND_API_KEY
```

### Option 2: SendGrid

```txt
sendgrid==6.11.0
```

### Option 3: Mailgun

```txt
requests==2.31.0
```

## 💾 Adding Database Storage

### Option 1: Vercel KV (Key-Value Store)

```bash
npm install @vercel/kv
```

### Option 2: Supabase

```txt
supabase==2.0.3
```

### Option 3: MongoDB Atlas

```txt
pymongo==4.6.1
```

## 🔐 Environment Variables

Set in Vercel Dashboard or via CLI:

```bash
vercel env add RESEND_API_KEY
vercel env add DATABASE_URL
```

## 📊 Monitoring

View logs:
```bash
vercel logs
vercel logs --follow  # Real-time
```

## 🐛 Debugging

Common issues:

**Function timeout:**
- Vercel free tier: 10s timeout
- Optimize database queries
- Use async operations

**CORS errors:**
- Check `Access-Control-Allow-Origin` headers
- Verify OPTIONS handler

**Import errors:**
- Ensure all dependencies in `requirements.txt`
- Test locally with `vercel dev`

## 📚 Resources

- [Vercel Serverless Functions](https://vercel.com/docs/functions)
- [Python on Vercel](https://vercel.com/docs/functions/runtimes/python)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
