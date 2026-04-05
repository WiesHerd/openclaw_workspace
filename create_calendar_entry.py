#!/usr/bin/env python3
# Calendar entry creator
import os
from datetime import datetime, timedelta

TOMORROW = datetime.now().date() + timedelta(days=1)

# Task markdown file
task_entry = """# Calendar Entry
## Event: Open Claw Test
**Date:** {date}
**Time:** 2:00 PM (PDT)

---

### Notes:
- Test calendar entry created by OpenClaw
- Verify synchronization with Google Calendar API
- Confirm OAuth authentication is working

---
*Created by OpenClaw Assistant*
""".format(date=TOMORROW.strftime("%A, %B %d, %Y"))

# Write to file (if you're using file-based calendar)
os.makedirs('/home/wherd/.openclaw/workspace/calendar/tasks', exist_ok=True)
with open('/home/wherd/.openclaw/workspace/calendar/tasks/tomorrow_entry.txt', 'w') as f:
    f.write(task_entry)

print(f"Calendar entry created!")
print(f"  File: /home/wherd/.openclaw/workspace/calendar/tasks/tomorrow_entry.txt")
print(f"  Date: {TOMORROW.strftime('%A, %B %d, %Y')}")
print(f"  Event: Open Claw Test")