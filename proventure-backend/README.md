# ProVenture Backend API

Flask-based backend for handling contact form submissions.

**✅ No Email Dependencies Required** - All submissions are saved locally to a JSON file.

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

4. **Configure environment (Optional):**
   - Copy `.env.example` to `.env` if you want to customize settings
   - The backend works out-of-the-box without any configuration
   - Submissions are saved to `submissions.json` in the backend directory

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

- Never commit `.env` file (already in .gitignore)
- Protect `submissions.json` - contains user data
- Enable HTTPS in production
- Consider rate limiting for production
- Regularly update dependencies
- Backup `submissions.json` regularly
- Set proper file permissions on production server

## Troubleshooting

**Submissions not saving:**
- Check write permissions in the backend directory
- Verify `submissions.json` can be created/modified
- Check application logs for errors

**CORS errors:**
- Ensure flask-cors is installed
- Check allowed origins in production
- Update CORS_ORIGINS in `.env` if needed

**File not found errors:**
- Ensure you're running the app from the `proventure-backend` directory
- Check that `DATA_FILE` path is correct

## License

Proprietary - ProVenture Digital Agency
