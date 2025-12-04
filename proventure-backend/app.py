# app.py
# Production-ready Flask backend for ProVenture Digital Agency contact form
# Handles form submissions and sends emails via Gmail SMTP

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "rahuljadhav44@gmail.com, proventurein@gmail.com")
FLASK_ENV = os.getenv("FLASK_ENV", "production")

# Validate required environment variables (SMTP credentials still needed)
if not all([SMTP_EMAIL, SMTP_APP_PASSWORD]):
    raise RuntimeError("Missing required environment variables (SMTP_EMAIL, SMTP_APP_PASSWORD). Check .env file.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email):
    """Validate email format"""
    return EMAIL_REGEX.match(email) is not None

def sanitize_input(text, max_length=1000):
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    # Remove any potential HTML/script tags
    text = re.sub(r'<[^>]*>', '', str(text))
    # Limit length
    return text[:max_length].strip()

def send_contact_email(form_data):
    """
    Send contact form data via email
    
    Args:
        form_data: dict with keys name, email, company, phone, interest, message
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = f"ProVenture Contact Form - {sanitize_input(form_data.get('name', 'Unknown'), 50)}"
        msg['From'] = SMTP_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Reply-To'] = form_data.get('email', SMTP_EMAIL)

        # Create email body
        body_parts = [
            "=" * 50,
            "NEW CONTACT FORM SUBMISSION",
            "=" * 50,
            f"\nSubmitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\nName: {sanitize_input(form_data.get('name', 'N/A'), 100)}",
            f"Email: {sanitize_input(form_data.get('email', 'N/A'), 100)}",
            f"Company: {sanitize_input(form_data.get('company', 'N/A'), 100)}",
            f"Phone: {sanitize_input(form_data.get('phone', 'N/A'), 50)}",
            f"Interest: {sanitize_input(form_data.get('interest', 'N/A'), 100)}",
            "\n" + "-" * 50,
            "MESSAGE:",
            "-" * 50,
            sanitize_input(form_data.get('message', 'N/A'), 5000),
            "\n" + "=" * 50,
        ]
        
        msg.set_content("\n".join(body_parts))

        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
            smtp.send_message(msg)
        
        logger.info(f"Email sent successfully from {form_data.get('email')}")
        return True
        
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise

@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    """Handle contact form submissions"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    # Get JSON data
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"ok": False, "error": "Invalid JSON data"}), 400
    
    if not data:
        return jsonify({"ok": False, "error": "No data received"}), 400

    # Validate required fields
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if not data.get(field) or not data.get(field).strip():
            return jsonify({
                "ok": False, 
                "error": f"Missing required field: {field}"
            }), 400

    # Validate email format
    email = data.get('email', '').strip()
    if not validate_email(email):
        return jsonify({
            "ok": False, 
            "error": "Invalid email format"
        }), 400

    # Validate message length
    message = data.get('message', '').strip()
    if len(message) < 10:
        return jsonify({
            "ok": False, 
            "error": "Message is too short (minimum 10 characters)"
        }), 400
    
    if len(message) > 5000:
        return jsonify({
            "ok": False, 
            "error": "Message is too long (maximum 5000 characters)"
        }), 400

    # Send email
    try:
        send_contact_email(data)
        return jsonify({
            "ok": True, 
            "message": "Thank you! Your message has been sent successfully."
        }), 200
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return jsonify({
            "ok": False, 
            "error": "Failed to send message. Please try again later."
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ProVenture Contact API"}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"ok": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"ok": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    # Development server (NOT for production)
    # For production, use: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    is_debug = FLASK_ENV == 'development'
    app.run(host='0.0.0.0', port=5000, debug=is_debug)
