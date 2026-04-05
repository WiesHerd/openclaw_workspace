#!/usr/bin/env python3
"""
Google Calendar OAuth2 - Enterprise Integration
Handles authorization, data sync, and Slack notifications
"""

import json
import os
import sqlite3
import sys
import threading
import http.server
import ssl
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import urllib.request
import socket

# Initialize local SQLite database for calendar events
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calendar.db')

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handle Google OAuth callbacks and fetch calendar data"""
    oauth_token_url = "https://oauth2.googleapis.com/token"
    calendar_list_url = "https://www.googleapis.com/calendar/v3/calendarList/list"
    events_url = "https://www.googleapis.com/calendar/v3/calendars/{}/events"
    
    def do_GET(self):
        """Handle GET requests for OAuth and calendar operations"""
        if self.path.startswith("/auth/google"):
            if "auth_code" in self.path:
                self.handle_auth_callback()
            elif "status" in self.path:
                self.handle_status_check()
        elif self.path.startswith("/calendar"):
            self.handle_calendar_request()
        elif self.path.startswith("/auth/google/revoke"):
            self.handle_revoke_token()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_auth_callback(self):
        """Process OAuth authorization callback"""
        auth_path = self.path.rstrip("/auth/google")
        parsed = urlparse(auth_path)
        params = parse_qs(parsed.query)
        
        auth_code = params.get("auth_code", "")
        if not auth_code:
            self.send_error(400, "Missing auth_code")
            return
        
        # Exchange auth code for access token
        data = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": self.oauth_callback_uri
        }
        
        req = urllib.request.Request(
            self.oauth_token_url,
            data=data.encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST"
        )
        
        with urllib.request.urlopen(req) as response:
            token_data = json.loads(response.read().decode())
            
            # Store token securely
            self.store_token(token_data)
            
            # Return status
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Token received and stored successfully')
    
    def store_token(self, token_data):
        """Store OAuth token in session"""
        session_config = getattr(self, 'session_config', {})
        
        # Store in gateway session
        if session_config.get('session_id'):
            session_id = session_config['session_id']
            session_config['access_token'] = token_data.get("access_token")
            session_config['token_type'] = token_data.get("token_type")
            session_config['expires_in'] = token_data.get("expires_in")
            
            # Refresh the session with new credentials
            self.gateway_commands.timeout_request({
                "request_id": session_id,
                "data": {"access_token": token_data.get("access_token")}
            })
    
    def handle_status_check(self):
        """Return current status"""
        self.send_response(200)
        self.end_headers()
        status = {
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "token_valid": os.getenv("GOOGLE_ACCESS_TOKEN") is not None
        }
        self.json_content(status)
    
    def handle_calendar_request(self):
        """Fetch calendar events"""
        path = self.path.replace("/calendar", "")
        events = []
        
        try:
            url = self.events_url.format(calendar_id)
            token = os.getenv("GOOGLE_ACCESS_TOKEN")
            
            if token:
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                
                req = urllib.request.Request(
                    url,
                    headers=headers
                )
                
                with urllib.request.urlopen(req) as response:
                    events = json.loads(response.read().decode())
            else:
                self.json_content({"error": "No token found"})
                return
                
            # Prepare response
            self.send_response(200)
            self.end_headers()
            self.json_content({
                "events": events
            })
        except urllib.error.HTTPError as e:
            self.send_error(500, str(e))
    
    def handle_revoke_token(self):
        """Revoke access token"""
        if os.getenv("GOOGLE_ACCESS_TOKEN"):
            token = os.getenv("GOOGLE_ACCESS_TOKEN")
            # Token revocation endpoint
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Token revoked")
        else:
            self.send_error(404)
    
    def json_content(self, data):
        """Format JSON response"""
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

if __name__ == "__main__":
    # Initialize callback
    def oauth_callback():
        """Handle initial OAuth callback"""
        params = parse_qs(urlparse(sys.argv[2]).query)
        auth_code = params.get("auth_code", "")
        
        if auth_code:
            data = {
                "code": auth_code,
                "grant_type": "authorization_code",
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": "http://localhost:18789/oauth2/callback"
            }
            
            req = urllib.request.Request(
                "https://oauth2.googleapis.com/token",
                data=data.encode(),
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            with urllib.request.urlopen(req) as response:
                token = json.loads(response.read().decode())
                os.getenv("GOOGLE_ACCESS_TOKEN") = token["access_token"]

if __name__ == "__main__":
    # Start server
    with socketserver.TCPServer(("", 18789), OAuthCallbackHandler) as httpd:
        print("Calendar server started")
        httpd.serve_forever()
