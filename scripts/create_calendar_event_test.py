#!/usr/bin/env python3
"""
Direct Google Calendar Insert Test
Events: 2026-04-05 1:00 PM - Egg Hunt
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

# Configuration from credentials.json
SECRET_FILE = "/home/wherd/.openclaw/workspace/skills/client_secret_59362936288-cnp3637l2teibgdntvi35ecp57lcmqr7.apps.googleusercontent.com.json"

def load_credentials():
    """Load OAuth credentials from JSON file"""
    with open(SECRET_FILE, 'r') as f:
        creds = json.load(f)
    return creds

def get_auth_url(creds):
    """Build OAuth 2.0 authorization URL"""
    # Use Safe Styled URL format for localhost redirect
    auth_url = creds['auth_uri'] + f"?client_id={creds['client_id']}"
    auth_url += "&redirect_uri=http://127.0.0.1:8888/oauth2callback"
    auth_url += "&response_type=code"
    auth_url += "&scope=https://www.googleapis.com/auth/calendar"
    return auth_url

def exchange_code_for_token(code, creds):
    """Exchange the auth code for an access token"""
    token_data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'redirect_uri': 'http://127.0.0.1:8888/oauth2callback'
    }
    
    req = urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        data=urllib.parse.urlencode(token_data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode())

def insert_calendar_event(creds, token_data):
    """Create calendar event directly via API"""
    # Token info
    access_token = token_data['access_token']
    token_type = token_data['token_type']
    
    # Event details
    events = {
        'summary': 'Egg Hunt Event',
        'description': 'Test event from OpenClaw calendar system',
        'start': {
            'date': '2026-04-05'
        },
        'end': {
            'date': '2026-04-05'
        }
    }
    
    # Headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': creds.get('key')  # if available
    }
    
    # Standard Gmail API endpoint for calendar
    url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
    
    req = urllib.request.Request(
        url,
        data=json.dumps(events).encode(),
        headers=headers,
        method='POST'
    )
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        status = result['status']
        
        if status == {
                'error': result.get('error', 'Unknown')
            }
        else:
            # Success - save event details for verification
            event_id = result.items()
            event_url = f"https://calendar.google.com/calendar/render?eid={event_id}"
            
            # Save event status to file for verification
            event_status = {
                'event_id': event_id,
                'created_at': datetime.now().isoformat(),
                'title': 'Egg Hunt Event',
                'status': 'SUCCESS',
                'api_url': event_url
            }
            
            with open('/tmp/calendar_append.json', 'w') as f:
                json.dump(event_status, f, indent=2)
            
            return event_status
    
    except urllib.error.HTTPError as e:
        return {
            'status': 'ERROR',
            'error': str(e),
            'message': 'Calendar event creation failed'
        }

def main():
    print("📅 Creating Google Calendar Entry: Egg Hunt")
    print("=" * 60)
    
    # Step 1: Load credentials
    creds = load_credentials()
    print(f"✅ Loaded credentials: {creds['client_id']}...")
    
    # Step 2: Build auth URL
    auth_url = get_auth_url(creds)
    print(f"🔗 Authorization URL: {auth_url}")
    print(f"📱 QR Code: https://accounts.google.com/o/oauth2/auth?client_id={creds['client_id']}&redirect_uri=http://127.0.0.1:8888/oauth2callback&response_type=code&scope=https%3A//www.googleapis.com/auth/calendar")
    print(f"🌐 Browser URL: {auth_url}")
    print()
    
    # Step 3: Launch browser
    print("🚀 Browser will open now for authentication...")
    try:
        webbrowser.open(auth_url)
    except:
        print("⚠️ Browser launch failed. Please open authorization URL manually in browser.")
        print(f"URL: {auth_url}")
        return None
    
    # Step 4: Exchange code after browser opens
    print()
    print("⏳ Waiting for browser to redirect after OAuth approval...")
    print("📍 Follow these steps:")
    print("  1. Approve Calendar access in browser popup")
    print("  2. You'll see code that should be:", "**CODE**")
    print("  3. Copy it: **CODE**")
    print("  4. Paste in this terminal or send to this chat")
    print()
    
    # Wait for code (in real scenario would poll for it)
    print()
    print("👉 Please send me the **CODE** from browser after granting access...")
    print()
    print("Status: WAITING_USER_INPUT_TO_VALIDATE")
    return "Code received"

if __name__ == "__main__":
    # Check if code was already provided
    if len(sys.argv) > 1 and sys.argv[1] == "EXECUTE_CODE":
        # Run the full flow with code provided
        code = "…"  # Replace with the actual code
        if code:
            creds = load_credentials()
            token_data = exchange_code_for_token(code, creds)
            event = insert_calendar_event(creds, token_data)
            
            if event['status'] == 'SUCCESS' and 'event_url' in event:
                print(f"✅ CALENDAR EVENT CREATED SUCCESSFULLY!")
                print(f"🎯 Event URL: {event['event_url']}")
                print(f"📅 Verify this exists at: {event['event_url']}")
                print()
                print("📱 Mobile verification:")
                print("1. Open Google Calendar app")
                print("2. Search for 'Egg Hunt'")
                print("3. Date: 2026-04-05 1:00 PM")
                print("4. Should see the event marked ✅")
            else:
                print(f"❌ Event Creation Failed")
                print(f"Error: {event}")
        else:
            print("No code provided - run oauth_grant.py script manually")
    elif len(sys.argv) > 1 and sys.argv[1] == "TERMINATE":
        print("Session terminated successfully")
    else:
        main()