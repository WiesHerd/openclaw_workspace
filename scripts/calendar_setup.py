#!/usr/bin/env python3
"""
Google Calendar Setup - Device Flow (No Browser Required)
Creates test event + stores tokens for future use
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# === CONFIG ===
CLIENT_ID = "59362936288-cnp3637l2teibgdntvi35ecp57lcmqr7.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_URI = "https://oauth2.googleapis.com/token"
DEVICE_AUTH_URI = "https://oauth2.googleapis.com/device/code"
CALENDAR_API = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
TOKEN_FILE = os.path.expanduser("~/.openclaw/google_calendar_token.json")

def device_authorization():
    """Step 1: Get device code from Google"""
    print("\n🔑 Step 1: Getting authorization code from Google...")
    
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "scope": "https://www.googleapis.com/auth/calendar",
    }).encode()
    
    req = urllib.request.Request(DEVICE_AUTH_URI, data=data)
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            return result
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to get device code: {e.read().decode()}")
        sys.exit(1)

def wait_for_user_approval(device_code, interval, expires_in):
    """Step 2: Poll until user approves on their device"""
    print(f"\n📱 Step 2: Approve on your phone/computer")
    print(f"   Go to: google.com/device")
    print(f"   Enter code: {user_code}")
    print(f"\n⏳ Waiting for approval (expires in {expires_in} seconds)...")
    print(f"   (I'll poll every {interval}s - you have up to {expires_in}s)")
    
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }).encode()
    
    start = time.time()
    
    while time.time() - start < expires_in:
        time.sleep(interval)
        
        req = urllib.request.Request(TOKEN_URI, data=data)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                print("\n✅ Approved! Got tokens.")
                return result
        except urllib.error.HTTPError as e:
            body = json.loads(e.read())
            error = body.get("error", "")
            
            if error == "authorization_pending":
                print(f"   ⏳ Still waiting... ({int(time.time() - start)}s elapsed)")
                continue
            elif error == "slow_down":
                interval += 5
                print(f"   ⏳ Slowing down... polling every {interval}s")
                continue
            elif error == "expired_token":
                print("❌ Code expired. Please run script again.")
                sys.exit(1)
            else:
                print(f"❌ Error: {error}")
                sys.exit(1)
    
    print("❌ Timed out waiting for approval")
    sys.exit(1)

def save_tokens(tokens):
    """Save tokens to file for future use"""
    token_data = {
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token"),
        "token_type": tokens.get("token_type"),
        "expires_in": tokens.get("expires_in"),
        "scope": tokens.get("scope"),
        "created_at": datetime.now().isoformat(),
    }
    
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    
    os.chmod(TOKEN_FILE, 0o600)
    print(f"\n💾 Tokens saved to: {TOKEN_FILE}")
    return token_data

def create_test_event(access_token):
    """Step 3: Create calendar event"""
    print("\n📅 Step 3: Creating test calendar event...")
    
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=13, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)
    
    event = {
        "summary": "🥚 Egg Hunt - OpenClaw Test",
        "description": "Test event created by OpenClaw to verify Google Calendar integration.\n\nGenerated: " + datetime.now().isoformat(),
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Phoenix",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/Phoenix",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 30},
                {"method": "popup", "minutes": 10},
            ]
        },
        "colorId": "10",  # Green color
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    req = urllib.request.Request(
        CALENDAR_API,
        data=json.dumps(event).encode(),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            print(f"\n✅ Calendar event created!")
            print(f"   Title: {result.get('summary')}")
            print(f"   When: {start_time.strftime('%B %d, %Y at %I:%M %p')}")
            print(f"   Event ID: {result.get('id')}")
            print(f"   Link: {result.get('htmlLink')}")
            return result
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to create event: {e.read().decode()}")
        sys.exit(1)

def main():
    print("=" * 60)
    print("📅 Google Calendar Setup - Device Flow")
    print("=" * 60)
    print("This script uses device authorization - NO browser needed!")
    print("You'll approve on your phone or another device.\n")
    
    # Step 1: Get device code
    device_info = device_authorization()
    
    device_code = device_info["device_code"]
    user_code = device_info["user_code"]
    verification_url = device_info["verification_url"]
    interval = device_info["interval"]
    expires_in = device_info["expires_in"]
    
    print(f"\n📱 YOUR AUTHORIZATION CODE: {user_code}")
    print(f"\n👉 Go to: {verification_url}")
    print(f"👉 Enter the code: {user_code}")
    print(f"👉 Sign in with: wherdzik@gmail.com")
    print(f"👉 Click 'Allow' for Calendar access")
    print(f"\n⏳ You have {expires_in} seconds to complete this.\n")
    print("I'll poll for confirmation in the background...")
    print("Just approve it and I'll continue automatically!\n")
    
    # Step 2: Wait for user to approve
    tokens = wait_for_user_approval(device_code, interval, expires_in)
    
    # Step 3: Save tokens
    save_tokens(tokens)
    
    # Step 4: Create test event
    event = create_test_event(tokens["access_token"])
    
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("✅ OAuth tokens saved")
    print("✅ Test calendar event created")
    print("✅ Check your phone/Google Calendar for the event!")
    print(f"\n📅 Event details:")
    print(f"   Title: {event.get('summary')}")
    print(f"   When: {event.get('start', {}).get('dateTime', 'N/A')}")
    print(f"   Link: {event.get('htmlLink', 'N/A')}")
    print("\nGoing forward, I can create calendar events without any prompts!")

if __name__ == "__main__":
    main()
