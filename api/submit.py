from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

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
            
            # Prepare data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = [
                timestamp,
                data.get('name', ''),
                data.get('email', ''),
                data.get('phone', ''),
                data.get('company', ''),
                ", ".join(data.get('interest', [])),
                data.get('message', '')
            ]

            # Google Sheets Integration
            try:
                # Check for credentials
                creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
                if creds_json:
                    # Parse credentials
                    creds_dict = json.loads(creds_json)
                    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
                    client = gspread.authorize(creds)
                    
                    # Open the spreadsheet
                    # Using the ID from the URL provided: https://docs.google.com/spreadsheets/d/1hFMI0gSCBxSKw8gI3nwl0qNK97n5jeeUN7ZwkNF7svs/edit
                    sheet_id = '1hFMI0gSCBxSKw8gI3nwl0qNK97n5jeeUN7ZwkNF7svs'
                    sheet = client.open_by_key(sheet_id).sheet1
                    
                    # Append the row
                    sheet.append_row(row_data)
                    print("Successfully appended to Google Sheet")
                else:
                    print("GOOGLE_SHEETS_CREDENTIALS not found in environment variables. Skipping Sheet append.")

            except Exception as e:
                print(f"Google Sheets Error: {str(e)}")
                # Continue execution to still return success to the user, but log the error on the backend
            
            # Send success response
            self._send_success({
                "ok": True,
                "message": "Thank you! Your message has been received successfully."
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
        self.send_header('Access-Control-Allow-Origin', 'https://proventure.in')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
