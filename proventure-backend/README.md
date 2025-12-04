# ProVenture Backend API

Flask-based backend for handling contact form submissions.

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Update with your Gmail credentials:
     ```
     SMTP_EMAIL=your-email@gmail.com
     SMTP_APP_PASSWORD=your-app-password
     RECEIVER_EMAIL=your-email@gmail.com
     ```
   - Get Gmail app password: https://myaccount.google.com/apppasswords

## Development

Run development server:
```bash
python app.py
```

API will be available at: http://localhost:5000

## Production Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using systemd (Linux)

Create `/etc/systemd/system/proventure-api.service`:

```ini
[Unit]
Description=ProVenture Contact API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/proventure-backend
Environment="PATH=/path/to/proventure-backend/venv/bin"
ExecStart=/path/to/proventure-backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable proventure-api
sudo systemctl start proventure-api
```

### Nginx Configuration

Add to your nginx config:

```nginx
location /api {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## API Endpoints

### POST /submit
Submit contact form data.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Inc",
  "phone": "+1234567890",
  "interest": "Web Design",
  "message": "I'm interested in your services..."
}
```

**Response (Success):**
```json
{
  "ok": true,
  "message": "Thank you! Your message has been sent successfully."
}
```

**Response (Error):**
```json
{
  "ok": false,
  "error": "Error message here"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "ProVenture Contact API"
}
```

## Security

- Never commit `.env` file
- Use strong app passwords
- Enable HTTPS in production
- Consider rate limiting for production
- Regularly update dependencies

## Troubleshooting

**Email not sending:**
- Check Gmail app password is correct
- Verify 2FA is enabled on Gmail account
- Check SMTP settings in `.env`

**CORS errors:**
- Ensure flask-cors is installed
- Check allowed origins in production

## License

Proprietary - ProVenture Digital Agency
