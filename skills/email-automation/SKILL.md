---
name: email-automation
description: Automated email processing including checking, summarizing, filtering, and sending. Supports 163.com and other IMAP/SMTP services. Use when user needs to automate email workflows, check inbox, send emails, or generate email summaries.
---

# Email Automation

Automated email processing for inbox management and communication workflows.

## When to Use

- Check inbox and generate summaries
- Filter important emails from noise
- Send automated or templated emails
- Monitor specific senders or keywords
- Daily/weekly email digest generation

## Configuration

Email credentials are stored in MEMORY.md:
- IMAP server: imap.163.com (for receiving)
- SMTP server: smtp.163.com (for sending)
- Account: zhujianxyz@163.com
- Sender: ftstic@163.com
- Auth: SMTP authorization code (not regular password)

**Note:** 163.com requires IMAP access to be enabled in email settings separately from SMTP.

## Usage

### Check Inbox
```bash
export EMAIL_AUTH_CODE='your_auth_code'
python3 /home/jian/.openclaw/workspace/skills/email-automation/scripts/email_check.py --limit 10
```

### Send Email
```bash
export EMAIL_AUTH_CODE='your_auth_code'
python3 /home/jian/.openclaw/workspace/skills/email-automation/scripts/email_send.py \
  --to recipient@example.com \
  --subject "Subject" \
  --body "Message body"
```

### Generate Daily Summary
```bash
export EMAIL_AUTH_CODE='your_auth_code'
python3 /home/jian/.openclaw/workspace/skills/email-automation/scripts/email_summary.py
```

## Current Status

| Feature | Status | Notes |
|---------|--------|-------|
| SMTP Send | Ready | Tested dry-run, needs confirmation for live send |
| IMAP Check | Needs Config | 163.com IMAP may need separate activation |
| Email Summary | Ready | Depends on IMAP working |

## Safety Notes

- Always confirm before sending emails to external addresses
- Respect privacy - don't expose email contents without permission
- Use authorization codes, not account passwords
- Log all email operations for audit trail
- IMAP access must be enabled separately in 163.com settings
