#!/bin/bash
# OpenClaw Quick Tools - Calendar & Charts

echo "=== OpenClaw Quick Tools ==="
echo ""
echo "1. View Bitcoin Chart:"
echo "   xdg-open /home/wherd/.openclaw/workspace/bitcoin_chart.png"
echo ""
echo "2. View Bitcoin Report:"
echo "   xdg-open /home/wherd/.openclaw/workspace/bitcoin_report.html"
echo ""
echo "3. View Calendar Tasks:"
echo "   cat /home/wherd/.openclaw/workspace/calendar/tasks/april_2026_tasks.md"
echo ""
echo "4. Check Google Calendar API (if connected):"
echo "   gcloud auth list --format='value(core.project)' | xargs -I {} gcloud projects describe {} | grep 'Name\|State'"
echo ""
echo "All files are in: /home/wherd/.openclaw/workspace/"
echo "Ready to sync when Google Calendar OAuth is complete!"