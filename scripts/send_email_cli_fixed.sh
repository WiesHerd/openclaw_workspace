#!/bin/bash
# Fixed version that handles mailbox creation
RECIPIENT="${1:-wherdzik@gmail.com}"
SUBJECT="CLI Email Test - $(date +%Y-%m-%d)"

# First, try to force mailbox creation (Postfix will create it on first delivery attempt)
postconf -e "mailbox_size_limit=0" 2>/dev/null
postconf -e "mailbox_command=" 2>/dev/null

# Send simple message
echo "Test from OpenClaw at $(date)" | /usr/bin/mail -s "$SUBJECT" "$RECIPIENT"
MAIL_STATUS=$?

if [ $MAIL_STATUS -eq 0 ]; then
    echo "✅ Email sent to $RECIPIENT"
    echo "📧 Subject: $SUBJECT"
else
    echo "❌ Email send failed with status $MAIL_STATUS"
    echo "Try: 1) Wait 1 minute for mailbox creation 2) Check Postfix status 3) Try again"
fi