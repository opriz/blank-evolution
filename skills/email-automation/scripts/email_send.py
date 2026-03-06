#!/usr/bin/env python3
"""
Email sender for 163.com
Supports SMTP with SSL
"""

import smtplib
import argparse
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_email(to_addr, subject, body, html_body=None):
    """Send email via 163.com SMTP"""
    
    # Configuration
    SMTP_SERVER = "smtp.163.com"
    SMTP_PORT = 465  # SSL port
    FROM_EMAIL = "ftstic@163.com"
    AUTH_CODE = os.environ.get('EMAIL_AUTH_CODE', '')
    
    if not AUTH_CODE:
        print("Error: EMAIL_AUTH_CODE environment variable not set")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = Header(f"Blank <{FROM_EMAIL}>", 'utf-8')
        msg['To'] = Header(to_addr, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        
        # Attach plain text
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Attach HTML if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        # Connect and send
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(FROM_EMAIL, AUTH_CODE)
        server.sendmail(FROM_EMAIL, [to_addr], msg.as_string())
        server.quit()
        
        print(f"✅ Email sent successfully to {to_addr}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Send email')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body (plain text)')
    parser.add_argument('--html', help='HTML body (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be sent without sending')
    args = parser.parse_args()
    
    if args.dry_run:
        print(f"\n📧 Dry Run - Would send:\n")
        print(f"To: {args.to}")
        print(f"Subject: {args.subject}")
        print(f"Body:\n{args.body}")
        return
    
    # Confirm before sending (unless overridden)
    print(f"\n📧 Ready to send email:\n")
    print(f"To: {args.to}")
    print(f"Subject: {args.subject}")
    print(f"Body preview: {args.body[:100]}...")
    
    confirm = input("\nSend? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    send_email(args.to, args.subject, args.body, args.html)

if __name__ == '__main__':
    main()
