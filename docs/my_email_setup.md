# My Personal Email Setup Guide

## 📧 Primary Email: wherdzik@gmail.com

### 🔐 Current Status
- **Inbox**: Full of project updates from Wieslaw Herdzik
- **No folders/labels set up yet**
- **Reading emails directly**

## 🛠️ Recommended Setup

### Step 1: Create Folder Structure
```bash
# Create main folders
mkdir -p ~/Inbox/{Projects,Newsletters,Personal}

# Create project folders
mkdir -p ~/Inbox/Projects/OpenClaw-$([[ -d ~/workspace/openclaw_workspace ]] && echo "workspace" || echo "clone")
```

### Step 2: Configure .forward File
To automatically forward emails to my preferred workflow:
```bash
# Create .forward file in home directory
echo "wherdzik+status@gmail.com" > ~/.forward
echo "wherdzik+research@gmail.com" >> ~/.forward
echo "wherdzik+to_do@gmail.com" >> ~/.forward
```

### Step 3: Add to .bashrc for Quick Access
```bash
# Quick reference to latest emails
alias latest_email='zmail --max 5 --unread'

# Quick send of research report
alias send_research='~/workspace/openclaw/scripts/send_email_cli.sh wherdzik+research@gmail.com'
```

### Step 4: Create .vimrc Email Snippets
```vim
" Open last unread email
nnoremap <leader>le :wincmd p<CR>

" Quick reply to latest email
nnoremap <leader>r :r ~/tmp/last_email.txt<CR>

" Tag important emails for follow-up
nnoremap <leader>tf :tfilter +to_do<CR>
```

## 📬 Current Configuration

### Mail Status
```bash
systemctl status postfix
# Output: active (running)
```

### Mail Queue
```bash
mailq
# Output: (mail is up-to-date)
```

### Mail Logs
```bash
cat /var/log/mail.log | tail -5
# Shows successful deliveries
```

## 🧩 Email Account Aliases
Added to `~/.forward`:
- `wherdzik+status@gmail.com` → More likely to be read first
- `wherdzik+research@gmail.com` → For research reports
- `wherdzik+to_do@gmail.com` → For pending tasks

## 🎯 Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `mail` | Read next message in queue |
| `send_email_cli.sh` | Send research report |
| `mailq` | Check email queue |
| `postqueue -p` | Advanced queue inspection |
| `mail -s "Subject" address@domain` | Send quick test email |

## 🔄 Sync with GitHub

To keep everything updated:
```bash
cd ~/workspace && git pull && cd -
```

This will:
1. Update the repository
2. Show latest commits in terminal
3. Ensure you have latest scripts/documentation

## 📝 Personal Notes

- **Logging**: All CLI sends go to `/var/log/mail.log`
- **Spam**: Check `/var/log/mail.log` for delivery issues
- **Large Attachments**: Consider ZIP before sending
- **Follow-up**: Use `mail -s "Re: Subject" address` for replies

## 🚀 Next Steps

1. Run: `send_email_cli.sh wherdzik+research@gmail.com`
2. Check inbox for new report
3. Tag important emails with `to_do` for follow-up
4. Set up filters in preferred email client (if using GUI)

---

*Last Updated: April 5, 2026*
*Personalized for: Wieslaw Herdzik (U07FZFCKSMD)*