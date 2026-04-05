#!/usr/bin/env python3
import requests
import urllib.parse
import webbrowser
import os

# Your credentials
CLIENT_ID = "59362936288-cnp3637l2teibgdntvi35ecp57lcmqr7.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# OAuth URLs
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CALENDAR_API = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

def get_authorization_url():
    """Generate Google OAuth URL"""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

def get_access_token(auth_code):
    """Exchange authorization code for access token"""
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob"
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()

def create_calendar_event(access_token):
    """Create the test event"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    event = {
        "summary": "Test Event - OpenClaw Verification",
        "description": "Automated test event created by OpenClaw to verify Google Calendar API access.",
        "start": {
            "date": "2026-04-05"
        },
        "end": {
            "date": "2026-04-05"
        },
        "reminders": {
            "useDefault": False
        }
    }
    
    response = requests.post(CALENDAR_API, headers=headers, json=event)
    return response.json()

def main():
    print("🔐 OpenClaw Google Calendar Authorization")
    print("=" * 50)
    
    # Step 1: Show auth URL
    auth_url = get_authorization_url()
    print(f"Step 1: Please open this URL in your browser:")
    print(f"   {auth_url}")
    print()
    print("Step 2: Sign in with your Google account and click 'Allow'")
    print("Step 3: Google will show you an authorization code. Copy it.")
    print()
    
    # Step 2: Get code from user
    auth_code = input("Step 3: Paste the authorization code here: ").strip()
    
    if not auth_code:
        print("❌ No code provided. Exiting.")
        return
    
    # Step 3: Exchange code for token
    print("\nStep 4: Exchanging code for access token...")
    try:
        token_data = get_access_token(auth_code)
        access_token = token_data['access_token']
        print(f"✅ Success! Got access token: {access_token[:20]}...")
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
        return
    
    # Step 4: Create event
    print("\nStep 5: Creating test event in your Google Calendar...")
    try:
        result = create_calendar_event(access_token)
        print("✅ SUCCESS! Event created in Google Calendar!")
        print(f"   Event ID: {result.get('id', 'N/A')}")
        print(f"   Summary: {result.get('summary')}")
        print(f"   Start: {result.get('start', {}).get('date')}")
        print()
        print("🎉 Check your Google Calendar for 'Test Event - OpenClaw Verification' on April 5, 2026!")
    except Exception as e:
        print(f"❌ Failed to create event: {e}")

if __name__ == "__main__":
    main()