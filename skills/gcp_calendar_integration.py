#!/usr/bin/env python3
"""
Google Calendar Integration for OpenClaw
Peter Steinberger-style proactive memory management
"""

import os
import json
from datetime import datetime


def load_secret_key():
    """Load client secrets safely"""
    secret_file = "/home/wherd/.openclaw/workspace/skills/client_secret_*.json"
    
    # Find and load the secret file safely
    secret_files = [f for f in os.listdir("/home/wherd/.openclaw/workspace/skills") 
                    if "client_secret" in f]
    
    if not secret_files:
        print("ERROR: No client secret file found in skills folder")
        return None
    
    secret_filename = secret_files[0]
    secret_path = os.path.join("/home/wherd/.openclaw/workspace/skills", secret_filename)
    
    try:
        with open(secret_path, 'r') as f:
            # Only extract necessary fields
            data = json.load(f)
            # Securely store only what's needed
            return {
                "client_id": data.get("client_id"),
                "redirect_uris": data.get("redirect_uris", ["http://localhost:8080/callback"])
            }
    except Exception as e:
        print(f"Warning: Could not load secret file: {e}")
        return None


def setup_calendar_config():
    """Create calendar configuration template"""
    config_dir = "/home/wherd/.openclaw/gcp_service"
    os.makedirs(config_dir, exist_ok=True)
    
    config = {
        "created_at": datetime.now().isoformat(),
        "service_name": "google_calendar_monitor",
        "monitoring": {
            "enabled": True,
            "alert_threshold_minutes": 30,
            "auto_sync": True
        },
        "memory_integration": {
            "calendar_states_file": "/home/wherd/.openclaw/memory/calendar-state.json",
            "task_queue_file": "/home/wherd/.openclaw/memory/calendar-tasks.json"
        }
    }
    
    config_path = os.path.join(config_dir, "calendar_config.json")
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Set restrictive permissions (owner only)
    os.chmod(config_path, 0o600)
    
    return config_path, config


if __name__ == "__main__":
    print("🚀 Google Calendar Integration Setup")
    print("=" * 50)
    
    # Load credentials
    secret = load_secret_key()
    if secret:
        print(f"✅ Client ID loaded: {secret['client_id'][:30]}...")
        
        # Setup configuration
        config_path, config = setup_calendar_config()
        print(f"✅ Calendar config created: {config_path}")
        print(f"✅ Permissions set (600 - owner only)")
        
        print("\n📋 Next steps:")
        print("1. Authenticate with Google OAuth 2.0 flow")
        print("2. Store access token in memory tracker")
        print("3. Enable calendar monitoring via heartbeat")
    else:
        print("⚠️  Credentials not loaded successfully")
        print("   Manual setup required in ~/.bashrc")
        
    print("\n📌 Integration Status: Ready for OAuth Auth")
