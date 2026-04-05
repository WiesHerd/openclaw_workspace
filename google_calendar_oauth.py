#!/usr/bin/env python3
"""
OpenClaw Google Calendar Integration via OAuth 2.0
"""
import os
import sys
import webbrowser
import urllib.parse

# OAuth 2.0 endpoint URLs
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CAL_API = "https://www.googleapis.com/calendar/v3/"

# OAuth scopes
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]

client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")

def get_authorization_url():
    """Generate the OAuth authorization URL"""
    params = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:8080/callback",
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return auth_url

def main():
    print("=== OpenClaw Google Calendar OAuth ===")
    
    if not client_id or not client_secret:
        print("ERROR: Google OAuth credentials not found!")
        print("Set environment variables:")
        print("  export GOOGLE_CLIENT_ID='your-client-id'")
        print("  export GOOGLE_CLIENT_SECRET='your-client-secret'")
        return
    
    print("Your credentials are loaded.")
    print("Opening browser for authorization...")
    
    try:
        auth_url = get_authorization_url()
        webbrowser.open(auth_url)
        print(f"Please allow Calendar access in your browser, then paste the AUTHORIZATION CODE here.")
        auth_code = input("Enter authorization code: ").strip()
        
        # Exchange authorization code for access token
        token_data = exchange_code_for_token(auth_code)
        
        print("\n✓ SUCCESS! Access token obtained")
        print("Token (valid for 1 hour):")
        print(token_data['access_token'][:50] + "...")
        
        # Create the calendar event
        print("\nCreating 'Easter Egg Hunt' event for April 5, 2026...")
        create_event(token_data['access_token'], "Easter Egg Hunt", "2026-04-05T00:00:00")
        
        print("\n✅ Calendar event created successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    import json
    import urllib.request
    
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost:8080/callback",
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    
    req = urllib.request.Request(
        TOKEN_URL,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def create_event(access_token, event_title, event_date):
    """Create a Google Calendar event"""
    import json
    import urllib.request
    
    events_url = f"{CAL_API}events"
    
    # Event details
    event = {
        "summary": event_title,
        "start": {"dateTime": event_date, "timeZone": "America/Phoenix"},
        "end": {"dateTime": event_date + ':05:00', "timeZone": "America/Phoenix"},
        "description": "OpenClaw-created calendar event",
        "谁的": "true"
    }
    
    req = urllib.request.Request(
        events_url,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        data=json.dumps(event).encode()
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"Event ID: {result.get('id', 'N/A')}")
        print(f"Status: Created successfully!")

if __name__ == "__main__":
    main()