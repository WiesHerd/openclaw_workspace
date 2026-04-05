#!/bin/bash
# send_compensation_report.sh
# Sends compensation research files to specified email
# Usage: ./send_compensation_report.sh [recipient_email]

RECIPIENT="${1:-wherdzik@gmail.com}"
SUBJECT="Provider Compensation Research Report - $(date +%Y-%m-%d)"
BODY="Attached is the provider compensation research report generated on $(date)."
ATTACHMENTS=(
    "./research/physician_app_compensation_2026.md"
    "./research/compensation_data_summary.md"
    "./research/comp_research_findings.md"
)

# Check if mail command is available
if ! command -v mail &> /dev/null; then
    echo "❌ 'mail' command not found. Install with: sudo apt install mailutils"
    exit 1
fi

# Check if attachments exist
for file in "${ATTACHMENTS[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Attachment not found: $file"
        exit 1
    fi
done

# Create temporary zip file
ZIP_FILE="/tmp/compensation_report_$(date +%Y%m%d_%H%M%S).zip"
zip "$ZIP_FILE" "${ATTACHMENTS[@]}" 2>/dev/null

if [ -f "$ZIP_FILE" ]; then
    # Send email with attachment
    echo "$BODY" | mail -s "$SUBJECT" -a "$ZIP_FILE" "$RECIPIENT"
    
    if [ $? -eq 0 ]; then
        echo "✅ Report sent successfully to $RECIPIENT"
        echo "📎 Attachments: ${#ATTACHMENTS[@]} files compressed in $ZIP_FILE"
    else
        echo "❌ Failed to send email"
        exit 1
    fi
    
    # Clean up
    rm "$ZIP_FILE"
else
    echo "❌ Failed to create zip file"
    exit 1
fi