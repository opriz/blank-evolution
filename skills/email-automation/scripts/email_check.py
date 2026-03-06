#!/usr/bin/env python3
"""
Email inbox checker for 163.com
Supports IMAP protocol with SSL
"""

import imaplib
import email
from email.header import decode_header
import argparse
import os
import sys
from datetime import datetime

def decode_str(s):
    """Decode email subject/sender"""
    if not s:
        return ""
    value, charset = decode_header(s)[0]
    if isinstance(value, bytes):
        if charset:
            value = value.decode(charset)
        else:
            value = value.decode('utf-8', errors='ignore')
    return value

def get_email_body(msg):
    """Extract email body text"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            pass
    return body[:500] + "..." if len(body) > 500 else body

def check_inbox(limit=10, email_account=None):
    """Check inbox and return recent emails"""
    
    # Configuration - read from environment or fallback
    IMAP_SERVER = "imap.163.com"
    # Use provided email or fall back to sender email (ftstic@163.com)
    EMAIL_ACCOUNT = email_account or os.environ.get('EMAIL_ACCOUNT', 'ftstic@163.com')
    # Note: For 163.com, we need the IMAP authorization code
    # This should be set via environment variable for security
    AUTH_CODE = os.environ.get('EMAIL_AUTH_CODE', '')
    
    if not AUTH_CODE:
        print("Error: EMAIL_AUTH_CODE environment variable not set")
        print("Set it with: export EMAIL_AUTH_CODE='your_auth_code'")
        return []
    
    emails = []
    
    try:
        # Connect to IMAP server using TLS (more compatible with 163.com)
        mail = imaplib.IMAP4(IMAP_SERVER, 143)
        mail.starttls()
        mail.login(EMAIL_ACCOUNT, AUTH_CODE)
        
        # Select inbox
        status, messages = mail.select("INBOX")
        if status != 'OK':
            print("Error: Could not select inbox")
            return []
        
        # Search for all emails
        status, data = mail.search(None, 'ALL')
        if status != 'OK':
            print("Error: Could not search emails")
            return []
        
        # Get email IDs (most recent first)
        email_ids = data[0].split()
        email_ids = email_ids[-limit:]  # Get last 'limit' emails
        
        for e_id in reversed(email_ids):
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            if status != 'OK':
                continue
                
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract info
            subject = decode_str(msg["Subject"])
            from_addr = decode_str(msg["From"])
            date = msg["Date"]
            body_preview = get_email_body(msg)
            
            emails.append({
                'id': e_id.decode(),
                'subject': subject,
                'from': from_addr,
                'date': date,
                'preview': body_preview
            })
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"Error checking inbox: {e}")
        return []
    
    return emails

def classify_importance(email_data):
    """Simple heuristic to classify email importance"""
    subject = email_data['subject'].lower()
    sender = email_data['from'].lower()
    
    # High importance indicators
    urgent_keywords = ['urgent', 'important', 'action required', 'alert', '验证', '重要', '紧急']
    if any(kw in subject for kw in urgent_keywords):
        return 'HIGH'
    
    # Known important senders
    important_domains = ['github.com', 'gitlab.com', 'notion.so', 'feishu.cn']
    if any(domain in sender for domain in important_domains):
        return 'MEDIUM'
    
    # Low importance (newsletters, notifications)
    low_keywords = ['newsletter', 'unsubscribe', 'digest', 'promotion', '营销', '推广']
    if any(kw in subject for kw in low_keywords):
        return 'LOW'
    
    return 'NORMAL'

def main():
    parser = argparse.ArgumentParser(description='Check email inbox')
    parser.add_argument('--limit', type=int, default=10, help='Number of emails to fetch')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--email', default='ftstic@163.com', help='Email account to check (default: ftstic@163.com)')
    args = parser.parse_args()
    
    emails = check_inbox(args.limit, args.email)
    
    if args.json:
        import json
        print(json.dumps(emails, ensure_ascii=False, indent=2))
    else:
        print(f"\n📧 Found {len(emails)} recent emails:\n")
        for i, e in enumerate(emails, 1):
            importance = classify_importance(e)
            importance_icon = {'HIGH': '🔴', 'MEDIUM': '🟡', 'NORMAL': '⚪', 'LOW': '⚫'}.get(importance, '⚪')
            
            print(f"{i}. {importance_icon} [{importance}] {e['subject']}")
            print(f"   From: {e['from']}")
            print(f"   Date: {e['date']}")
            if e['preview']:
                print(f"   Preview: {e['preview'][:100]}...")
            print()

if __name__ == '__main__':
    main()
