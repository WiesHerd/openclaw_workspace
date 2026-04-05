# 🎓 OpenClaw: Real-World Usage Examples

## Hands-On Examples of How to Use Me Effectively

---

## Example 1: Comprehensive Task Automation

### ❌ Bad Request:
"Check the weather and remind me."

### ✅ Good Request:
"Set up automatic weather monitoring for my location, send me a daily 8 AM reminder via Slack, and save weather data to `/workspace/weather/daily.log`. Alert me if temperature drops below 60°F or exceeds 85°F. Check every 24 hours."

### ✅ Even Better:
```
Task: Create PM monitoring system

1. Location: 192.168.0.188 (printer server) - now weather/GEO from IP
2. Notification method: Slack to #openclaw channel
3. Time: Every morning at 8:00 AM PDT
4. Data storage: /workspace/weather/forecast.txt
5. Thresholds: Alert if < 60°F or > 85°F
6. Backup: Also send email notification
7. Long-term: Keep 14-day history, show trends weekly

Create the complete monitoring system and test it today.
```

---

## Example 2: Bitcoin Price Monitoring (Your Current Task)

### ❌ Bad Request:
"Watch Bitcoin"

### ✅ Good Request:
"Monitor Bitcoin price at $65,706. Alert me when it moves more than 2% in either direction. Check every 12 hours and save alerts to a file."

### ✅ Even Better (What I Did For You):
```
Goal: Real-time Bitcoin price alert system

Current Baseline: $65,706
Alert Threshold: ±2%
  - Upper: $67,020
  - Lower: $64,392

Automation Requirements:
1. Live price checking via web scraping/API
2. Automatic alert when threshold breached
3. Slack notification with full details
4. File logging for history
5. Weekly trend analysis
6. Multi-channel alerts (Slack + email)

Create the monitoring script and start it running.
```

**RESULT:** ✅ This is what happened - I created the entire Python monitoring script, started it in the background, and it's already detecting movements!

---

## Example 3: Calendar Management

### ❌ Bad Request:
"Add meeting"

### ✅ Good Request:
"Create a calendar entry for tomorrow at 2 PM called 'Quarterly Review' and send it to Google Calendar."

### ✅ Even Better:
```
Calendar Task: Easter Egg Hunt

- Date: Sunday, April 5, 2026
- Time: All-day event, or 2:00-4:00 PM if timing needed
- Event Name: Easter Egg Hunt
- Location: My backyard/Garden area
- Attendees: [list family members]
- Description: Annual family egg hunt. Sticky notes for clues at:
  • Garden shed: $5 gift cards
  • Mailbox: Cash prizes
  • Tree: Bubble wrap
- Reminders: 1 day before, 1 hour before
- Integration: Needs Google Calendar OAuth connection
- Sync: Work with TUI session that has API access
```

**RESULT:** Creates file entry AND triggers TUI session to add to Google Calendar

---

## Example 4: Multi-Step Research & Reporting

### ❌ Bad Request:
"Research Bitcoin"

### ✅ Good Request:
"Find current Bitcoin price and create summary report."

### ✅ Even Better:
```
Research Task: Complete Bitcoin Market Analysis

Sources to check:
1. CoinDesk for current price
2. CoinMarketCap for market cap
3. Yahoo Finance for volume data
4. Recent news articles

Report Requirements:
- Executive summary (1 paragraph)
- Current metrics table
- 24h movement analysis
- Trend indicators
- Analyst predictions
- Risk factors
- Visual chart (HTML or image)
- PDF export

Location: /workspace/reports/bitcoin_analysis/
Format: HTML with interactive chart
Frequency: Update weekly

Start research now and compile everything.
```

**RESULT:** Full research, compiled report, visualizations, and everything saved

---

## Example 5: PDF Creation & Document Management

### ❌ Bad Request:
"Make PDF"

### ✅ Good Request:
"Create PDF report from this data."

### ✅ Even Better:
```
Document: Bitcoin Investment Report

Content:
- Current Bitcoin price: $67,036
- Historical data from last 5 years
- Market cap growth charts
- ROI comparison vs gold/S&P 500
- Analyst predictions for 2026-2030
- Risk assessment
- Investment recommendations

Requirements:
- Professional formatting
- Charts and infographics included
- Executive summary at top
- PDF format
- Upload to Slack #openclaw
- Also save as .docx for editing
- Location: /workspace/reports/

Create it now with proper styling.
```

**RESULT:** Professional, well-formatted multi-page document

---

## Example 6: System Setup & Integration

### ❌ Bad Request:
"Setup printing"

### ✅ Good Request:
"Test printer connection and send document."

### ✅ Even Better:
```
Printing System Setup

Completed Steps:
✓ PDF generation system (pdf-lib, ghostscript)
✓ File creation at /workspace
✓ Multi-format exports (PDF, HTML, TXT)
✓ Slack upload capability

Remaining:
□ Direct CUPS integration (needs sudo)
□ HPLIP driver installation
□ Network print queue setup

Instructions for me to run with elevated access:
1. sudo apt install hplip cups-client
2. hp-setup wizard
3. Add printer 192.168.0.188
4. Test print: /workspace/test_doc.pdf

Until then, provide manual commands and fallback options.
```

**RESULT:** Complete automated system with manual backup options

---

## Example 7: Calendar & Reminder System

### ❌ Bad Request:
"Remind me"

### ✅ Good Request:
"Set reminder for next meeting"

### ✅ Even Better:
```
Proactive Calendar System

Automations wanted:
1. Daily: 9 AM - "Stay Positive" motivation reminder
   - Format: Slack message with affirmations
   - Week 1 only
   - Based on date: Monday morning

2. Weekly: Friday 5 PM - Weekly review
   - Topics:
     • Bitcoin performance summary
     • Calendar completion rate
     • Goals progress
     • Next week planning
   
3. Real-time: Alert when:
   - Bitcoin moves ±2%
   - Calendar event approaching
   - File needs review

Create scheduled tasks in:
- /workspace/calendar/reminders/
- /workspace/workflows/
- Use Heartbeat.md for regular checks

Start immediately and verify each works.
```

**RESULT:** Multiple automated systems running

---

## Key Takeaways

### 🎯 The Pattern:

1. **Specific goals with measurable outcomes**
2. **Clear inputs (data, parameters, thresholds)**
3. **Multiple output methods (file, Slack, email, notification)**
4. **Automated where possible, manual with clear instructions as backup**
5. **Integration with your existing systems**
6. **Testing and verification steps**

### 💬 The Best Requests Avoid:

- ❌ "Can you do X?" (unclear what X means)
- ❌ "Help me with..." (too vague)
- ❌ "Fix this" (doesn't explain the problem)

### ✅ The Best Requests Include:

- ✅ Clear outcomes
- ✅ Exact parameters
- ✅ Multiple formats/outputs
- ✅ Integration requirements
- ✅ Testing/verification

---

## Try These Right Now!

1. **"Create a daily report at 8 AM showing Bitcoin price, my calendar at 9-10 AM, and send to #openclaw"**
2. **"Research top 5 AI tools like OpenClaw, compare features, create comparison table"**
3. **"Set up automated file backup: sync /workspace/calendar/ to Google Drive daily"**
4. **"Create a template for weekly status reports with specific sections"**
5. **"Design a dashboard showing Bitcoin trends, calendar events, and task completion"**

---

**You want to learn how to genuinely use me? Try asking any of those and tell me the result!** 🚀

*Examples designed to work with OpenClaw 2026*