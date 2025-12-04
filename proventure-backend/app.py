# app.py
# Local Contact Form Handler
# Saves submissions to 'submissions.json' file instead of sending emails.
# Removes all Gmail/SMTP dependencies.

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# File to store submissions
DATA_FILE = 'submissions.json'

def save_submission(data):
    """Save the form data to a JSON file locally."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": data
    }
    
    submissions = []
    
    # Read existing data if file exists
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                submissions = json.load(f)
        except json.JSONDecodeError:
            submissions = [] # Start fresh if file is corrupted

    # Append new entry
    submissions.append(entry)
    
    # Write back to file
    with open(DATA_FILE, 'w') as f:
        json.dump(submissions, f, indent=4)
        
    return True

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.json
        
        # Basic validation
        if not data or not data.get('email'):
            return jsonify({"ok": False, "error": "Email is required"}), 400

        # Save to local file
        save_submission(data)
        
        logger.info(f"New submission saved from {data.get('email')}")
        
        return jsonify({
            "ok": True, 
            "message": "Message saved successfully to local file."
        }), 200

    except Exception as e:
        logger.error(f"Error processing submission: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == '__main__':
    print(f"Server running. Messages will be saved to: {os.path.abspath(DATA_FILE)}")
    app.run(debug=True, port=5000)
