#!/usr/bin/env python3
"""
Google Calendar OAuth 2.0 helper for OpenClaw workspace.

Prerequisites:
  - Google Cloud: OAuth client type **Web application** (not Desktop / iOS / Android)
  - Same project: enable **Google Calendar API**
  - Under that Web client, add **both** (exact strings, no trailing slash):
      Authorized JavaScript origins: http://localhost:8888
      Authorized redirect URIs:       http://localhost:8888/oauth
  - WSL + Windows browser: redirect must use **localhost** (not 127.0.0.1) so the
    callback reaches this script; listener binds 0.0.0.0 by default.

Usage:
  export GOOGLE_CLIENT_ID='....apps.googleusercontent.com'
  export GOOGLE_CLIENT_SECRET='....'
  python3 auth_grant.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import webbrowser
from datetime import date, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8888/oauth")
# Listen on all interfaces so Windows browser -> http://localhost:8888 reaches WSL (port forward).
CALLBACK_BIND = os.getenv("GOOGLE_OAUTH_CALLBACK_BIND", "0.0.0.0")
CALLBACK_PORT = int(os.getenv("GOOGLE_OAUTH_CALLBACK_PORT", "8888"))

# Must match Authorized redirect URIs in GCP (path /oauth)
SCOPE = " ".join(
    [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ]
)

CAL_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
TOKEN_FILE = Path.home() / ".openclaw" / "workspace" / "google-calendar-oauth-tokens.json"


class _OAuthState:
    code: str | None = None
    error: str | None = None
    error_description: str | None = None


_state = _OAuthState()
_done = threading.Event()


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.rstrip("/") != "/oauth" and parsed.path != "/oauth":
            self.send_error(404)
            return

        qs = parse_qs(parsed.query)
        if "error" in qs:
            _state.error = qs["error"][0]
            _state.error_description = (qs.get("error_description") or [""])[0]
            body = b"<html><body><h2>Google returned an error</h2><p>Check the terminal.</p></body></html>"
            self._send_html(200, body)
            _done.set()
            return

        if "code" not in qs:
            self._send_html(400, b"<html><body><p>Missing <code>code</code> query parameter.</p></body></html>")
            _done.set()
            return

        _state.code = qs["code"][0]
        msg = (
            "<html><body><h2>Authorization received</h2>"
            "<p>You can close this tab and return to the terminal.</p></body></html>"
        )
        self._send_html(200, msg.encode("utf-8"))
        _done.set()

    def _send_html(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def get_auth_url() -> str:
    # Google expects "scope" as a single space-separated string, not repeated keys from a list.
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)


def print_gcp_setup(redirect_uri: str) -> None:
    """Print values that must match Google Cloud Console (cannot be automated from here)."""
    try:
        origin = urlparse(redirect_uri)
        base = f"{origin.scheme}://{origin.netloc}"
    except Exception:
        base = "http://localhost:8888"
    print()
    print("┌" + "─" * 58 + "┐")
    print("│ Paste these into Google Cloud (same OAuth client ID you use above) │")
    print("└" + "─" * 58 + "┘")
    print("  APIs & Services → Credentials → your OAuth 2.0 Client ID → Edit")
    print("  Application type: **Web application**")
    print()
    print("  Authorized JavaScript origins → ADD:")
    print(f"    {base}")
    print()
    print("  Authorized redirect URIs → ADD (exactly one line, copy verbatim):")
    print(f"    {redirect_uri}")
    print()
    print("  Save. Wait 1–5 minutes if Google still shows errors.")
    print()
    if "127.0.0.1" in redirect_uri and _running_in_wsl():
        print(
            "  WARNING: You are using 127.0.0.1 in REDIRECT_URI. On WSL, the Windows\n"
            "  browser often cannot reach 127.0.0.1:8888 inside Linux. Prefer:\n"
            "    export GOOGLE_OAUTH_REDIRECT_URI='http://localhost:8888/oauth'\n"
            "  and register that exact URI in GCP.\n"
        )


def exchange_token(auth_code: str) -> dict:
    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": auth_code,
            "grant_type": "authorization_code",
        },
        timeout=60,
    )
    data = r.json()
    if r.status_code != 200:
        data["_http_status"] = r.status_code
    return data


def save_tokens(token_data: dict) -> None:
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "token_endpoint": "https://oauth2.googleapis.com/token",
        "client_id": CLIENT_ID,
        # Do not store client_secret on disk in production; handy for local refresh scripts only.
        "refresh_token": token_data.get("refresh_token"),
        "access_token": token_data.get("access_token"),
        "expires_in": token_data.get("expires_in"),
        "token_type": token_data.get("token_type"),
        "scope": token_data.get("scope"),
    }
    TOKEN_FILE.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except OSError:
        pass
    print(f"Tokens saved to: {TOKEN_FILE}")


def create_test_event(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    event = {
        "summary": "OpenClaw — OAuth test event",
        "description": "Created by auth_grant.py after successful Google Calendar OAuth.",
        "start": {"date": tomorrow},
        "end": {"date": tomorrow},
        "reminders": {"useDefault": True},
    }
    r = requests.post(CAL_EVENTS_URL, headers=headers, json=event, timeout=60)
    try:
        return r.json()
    except Exception:
        return {"error": "non_json_response", "text": r.text[:500], "status": r.status_code}


def _running_in_wsl() -> bool:
    if os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"):
        return True
    try:
        with open("/proc/version", encoding="utf-8") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


def open_auth_url(url: str) -> None:
    """Open default browser. WSL: avoid gio (often broken); use Windows or print URL."""
    print("Open this URL in your browser (copy if it does not open automatically):\n")
    print(url)
    print()

    if _running_in_wsl():
        cmd_exe = Path("/mnt/c/Windows/System32/cmd.exe")
        if cmd_exe.is_file():
            try:
                subprocess.Popen(
                    [str(cmd_exe), "/c", "start", "", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print("Launched via Windows (cmd.exe start).\n")
                return
            except OSError:
                pass
        for bin_name in ("wslview", "wsl-open"):
            try:
                subprocess.Popen([bin_name, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Launched via {bin_name}.\n")
                return
            except OSError:
                continue

    try:
        if webbrowser.open(url):
            print("Opened via webbrowser.\n")
            return
    except Exception:
        pass

    print("Could not open a browser automatically — paste the URL above into Edge/Chrome.\n")


def wait_for_callback(timeout_s: int = 300) -> None:
    server = HTTPServer((CALLBACK_BIND, CALLBACK_PORT), OAuthCallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        if not _done.wait(timeout=timeout_s):
            print("\nTimed out waiting for browser redirect. Paste the code manually.")
            return
    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    print("Google Calendar OAuth (OpenClaw workspace helper)")
    print("=" * 55)

    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Set environment variables:")
        print("  export GOOGLE_CLIENT_ID='....apps.googleusercontent.com'")
        print("  export GOOGLE_CLIENT_SECRET='....'")
        print("\nGCP: Web client + redirect URI must match exactly:")
        print(f"  {REDIRECT_URI}")
        return 1

    print(f"Redirect URI sent to Google (must match GCP): {REDIRECT_URI}")
    print(f"Callback listener: http://{CALLBACK_BIND}:{CALLBACK_PORT}/oauth (use localhost:{CALLBACK_PORT} in browser)")
    print(f"Client ID prefix: {CLIENT_ID[:24]}...")

    print_gcp_setup(REDIRECT_URI)

    auth_url = get_auth_url()
    print("\nSign in and allow Calendar access (browser should open; if not, use the URL below).\n")

    wait_thread = threading.Thread(target=wait_for_callback, kwargs={"timeout_s": 300}, daemon=True)
    wait_thread.start()
    open_auth_url(auth_url)

    wait_thread.join(timeout=310)

    if _state.error:
        print(f"\nOAuth error: {_state.error}")
        if _state.error_description:
            print(f"  {_state.error_description}")
        return 1

    code = _state.code
    if not code:
        code = input("\nPaste authorization code from the browser URL (code=...): ").strip()

    if not code:
        print("No code — exiting.")
        return 1

    print("\nExchanging code for tokens...")
    token_data = exchange_token(code)

    if "error" in token_data:
        print(f"Token error: {token_data.get('error')}")
        print(f"  {token_data.get('error_description', token_data)}")
        return 1

    access = token_data.get("access_token")
    if not access:
        print(f"Unexpected token response: {token_data}")
        return 1

    save_tokens(token_data)
    if not token_data.get("refresh_token"):
        print(
            "\nNote: No refresh_token in response. Revoke app access in Google Account "
            "settings and run again with prompt=consent if you need offline refresh."
        )

    print("\nCreating test event on primary calendar...")
    event = create_test_event(access)

    if event.get("id"):
        print(f"SUCCESS — event id: {event.get('id')}")
        print(f"  Summary: {event.get('summary')}")
        print(f"  Start: {event.get('start', {})}")
        return 0

    print(f"Calendar API error: {event}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
