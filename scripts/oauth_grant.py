#!/usr/bin/env python3
"""
Google Calendar OAuth 2.0 Authorization Script
Automates credentials loading, browser launch, and token exchange
"""

import os
import sys
import json
import webbrowser
import urllib.request
import urllib.parse
import http.client
import threading
import http.server
import socketserver
from urllib.parse import parse_qs
from datetime import datetime, timedelta
from google.oauth2 import