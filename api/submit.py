from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    """
    Vercel Serverless Function for handling contact form submissions
    Endpoint: /api/submit
    """
    
    def do_POST(self):
        """Handle POST requests from contact form"""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read and parse POST data
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            if not data or not data.get('email'):
                self._send_error(400, "Email is required")
                return
            
            if not data.get('name'):
                self._send_error(400, "Name is required")
                return
            
            if not data.get('message'):
                self._send_error(400, "Message is required")
                return
            
            # Create submission entry with timestamp
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": {
                    "name": data.get('name', ''),
                    "email": data.get('email', ''),
                    "company": data.get('company', ''),
                    "phone": data.get('phone', ''),
                    "interest": data.get('interest', []),
                    "message": data.get('message', '')
                }
            }
            
            # Log submission (visible in Vercel logs)
            print(f"New submission from: {data.get('email')}")
            print(f"Submission data: {json.dumps(entry, indent=2)}")
            
            # TODO: In production, integrate with:
            # - Vercel KV for storage
            # - Email service (SendGrid, Resend, etc.)
            # - Database (Supabase, MongoDB, etc.)
            # - Airtable or Google Sheets
            
            # Send success response
            self._send_success({
                "ok": True,
                "message": "Thank you! Your message has been received successfully. We'll get back to you soon!"
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON data")
        except Exception as e:
            print(f"Error processing submission: {str(e)}")
            self._send_error(500, f"Server error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _send_success(self, data):
        """Send successful JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, code, message):
        """Send error JSON response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({
            "ok": False,
            "error": message
        }).encode())
    
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
