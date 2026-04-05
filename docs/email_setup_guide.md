# Email Setup Guide for Compensation Reports

## 📧 Setting Up Email Capability

This guide walks you through configuring email sending for the compensation research reports.

---

## 🔐 **Option 1: Gmail App Password (Recommended)**

### Step 1: Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification**
3. Click **Get Started** and follow the setup
4. Verify your phone number and enable 2-Step Verification

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Under "Select app", choose **Mail**
3. Under "Select device", choose **Other (Custom name)**
4. Enter: `OpenClaw Workspace`
5. Click **Generate**
6. **Copy the 16-character password** (format: `xxxx xxxx xxxx xxxx`)
   - ⚠️ **Important**: You won't see it again!

### Step 3: Set Environment Variables
Add to your `~/.bashrc` or `~/.profile`:

```bash
# Email configuration for OpenClaw
export GMAIL_USER='wherdzik@gmail.com'
export GMAIL_APP_PASSWORD='your_16_char_password_here'  # No spaces!
```

Then reload:
```bash
source ~/.bashrc
```

### Step 4: Test the Setup
```bash
cd /home/wherd/.openclaw/workspace
python3 scripts/send_compensation_report.py
```

---

## 📦 **Option 2: Install mailutils (Simple)**

If you prefer a simpler approach using system mail:

```bash
# Install mail utilities
sudo apt update
sudo apt install mailutils

# Configure (accept defaults during installation)

# Test sending
echo "Test" | mail -s "Test Subject" wherdzik@gmail.com
```

Then use the bash script:
```bash
./scripts/send_compensation_report.sh wherdzik@gmail.com
```

---

## 🧪 **Testing**

### Verify Files Exist
```bash
ls -lh ./research/*.md
```

Expected files:
- ✅ `physician_app_compensation_2026.md` (~9.6 KB)
- ✅ `compensation_data_summary.md` (~8.6 KB)
- ✅ `comp_research_findings.md` (~5.4 KB)
- ✅ `compensation_report_backup.md` (~5.5 KB)

### Test Python Script
```bash
# With environment variables set
python3 scripts/send_compensation_report.py

# Or specify recipient
python3 scripts/send_compensation_report.py --recipient your_test_email@gmail.com
```

### Test Bash Script
```bash
./scripts/send_compensation_report.sh wherdzik@gmail.com
```

---

## 🔒 **Security Best Practices**

### ✅ Do:
- Use App Passwords (not your regular Gmail password)
- Store credentials in environment variables
- Keep credentials out of git (add to `.gitignore`)
- Delete App Password when no longer needed

### ❌ Don't:
- Hardcode passwords in scripts
- Commit credentials to git
- Share App Passwords with others
- Use your regular Gmail password

### Check .gitignore
Ensure credentials aren't tracked:
```bash
# Add to .gitignore if not already present
echo "*.env" >> .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Update: Add .env to gitignore"
git push
```

---

## 📋 **Quick Start Commands**

```bash
# Navigate to workspace
cd /home/wherd/.openclaw/workspace

# Set credentials (one-time setup)
export GMAIL_USER='wherdzik@gmail.com'
export GMAIL_APP_PASSWORD='xxxx xxxx xxxx xxxx'

# Send report
python3 scripts/send_compensation_report.py

# Check your email!
```

---

## 🆘 **Troubleshooting**

### Error: "Authentication failed"
- ✅ Verify 2-Step Verification is enabled
- ✅ Use App Password (not regular password)
- ✅ Remove spaces from App Password
- ✅ Regenerate App Password if needed

### Error: "Connection refused"
- ✅ Check internet connection
- ✅ Verify Gmail SMTP is not blocked by firewall
- ✅ Try: `telnet smtp.gmail.com 587`

### Error: "File not found"
- ✅ Verify research files exist: `ls ./research/*.md`
- ✅ Run from workspace directory: `cd /home/wherd/.openclaw/workspace`

---

## 📞 **Need Help?**

If you encounter issues:
1. Check Gmail App Passwords: https://myaccount.google.com/apppasswords
2. Verify 2-Step Verification: https://myaccount.google.com/security
3. Check OpenClaw logs for detailed error messages

---

*Last Updated: April 5, 2026*
*Workspace: /home/wherd/.openclaw/workspace*