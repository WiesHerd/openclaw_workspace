#!/bin/bash
# send_email_cli.sh
# Simple email sender using mailutils
# Usage: ./send_email_cli.sh [recipient_email]

RECIPIENT="${1:-wherdzik@gmail.com}"
SUBJECT="Provider Compensation Report - $(date +%Y-%m-%d)"
BODY="Attached is the compensation research report generated on $(date)."

# Check if any arguments were passed
if [ $# -eq 0 ]; then
    echo "Usage: $0 [email_address]"
    echo "Example: $0 wherzdik@gmail.com"
    exit 1
fi

# Check if we can send at all
if ! command -v mail &> /dev/null; then
    echo "❌ 'mail' command not found. Install with: sudo apt install mailutils"
    exit 1
fi

# Send email directly (no attachment support with plain mail)
# Compose a simple message with the content
{
    echo "From: OpenClaw <$(whoami)@$(hostname)>"
    echo "To: $RECIPIENT"
    echo "Subject: $SUBJECT"
    echo
    echo "Provider Compensation Research Report"
    echo "Generated: $(date)"
    echo
    echo "Attached research files available at:"
    echo "  - ./research/physician_app_compensation_2026.md"
    echo "  - ./research/compensation_data_summary.md" 
    echo "  - ./research/comp_research_findings.md"
    echo "If you need attachments, use the Python script instead."
} | /usr/bin/mail -s "$SUBJECT" "$RECIPIENT"

if [ $? -eq 0 ]; then
    echo "✅ Email sent successfully to $RECIPIENT"
    echo "Subject: $SUBJECT"
else
    echo "❌ Failed to send email"
    exit 1
fi