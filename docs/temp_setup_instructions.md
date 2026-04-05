# Quick Setup Instructions for Sending Email

## 🔑 Step-by-Step Setup

### 1. **Enable 2-Step Verification**
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"

### 2. **Create App Password**
1. Go to: https://myaccount.google.com/apppasswords
2. Under "Select app", choose **Mail**
3. Under "Select device", choose **Other (Custom name)**
4. Enter: **OpenClaw Send**
5. Click **Generate**
6. Copy the **16-character password** (don't worry about spaces)

### 3. **Set Environment Variables**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export GMAIL_USER='wherdzik@gmail.com'
export GMAIL_APP_PASSWORD='your_16_char_password_here'
```
Then reload:
```bash
source ~/.bashrc
```

### 4. **Send Your Report**
```bash
python3 scripts/send_compensation_report.py
```

### 5. **Check Your Inbox!**
Look for the email with subject:
"Provider Compensation Report - 2026-04-05"
```
