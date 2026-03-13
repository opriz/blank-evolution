#!/usr/bin/env python3
"""
PR #44998 状态监控脚本
使用 GitHub HTTP API (无需认证，但有速率限制)
"""

import json
import os
import smtplib
import sys
import urllib.request
import urllib.error
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Configuration
PR_NUMBER = 44998
REPO = "openclaw/openclaw"
STATE_FILE = os.path.expanduser("~/.config/pr-monitor/pr-44998-state.json")
CREDENTIALS_FILE = os.path.expanduser("~/.config/email/credentials.json")
GITHUB_TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/.github-token")


def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load credentials: {e}")
        return None


def load_previous_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load previous state: {e}")
    return None


def save_state(state):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save state: {e}")


def load_github_token():
    """Load GitHub token from file"""
    try:
        with open(GITHUB_TOKEN_FILE, 'r') as f:
            content = f.read()
            # Extract token from format: `ghp_...` or just the token
            import re
            match = re.search(r'ghp_[a-zA-Z0-9]{36}', content)
            if match:
                return match.group(0)
    except Exception as e:
        print(f"⚠️ Failed to load GitHub token: {e}")
    return None


def fetch_pr_data():
    """Fetch PR data from GitHub API"""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PR-Monitor-Script"
    }
    
    # Add authentication if token available
    token = load_github_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"❌ HTTP Error 403: rate limit exceeded")
        else:
            print(f"❌ HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"❌ Failed to fetch PR data: {e}")
        return None


def send_notification(changes, pr_data):
    creds = load_credentials()
    if not creds:
        print("❌ Cannot send notification: no credentials")
        return False
    
    SMTP_SERVER = "smtp.163.com"
    SMTP_PORT = 465
    FROM_EMAIL = creds['sender_email']
    TO_EMAIL = creds['email']
    AUTH_CODE = creds['smtp_auth_code']
    
    subject = f"🔔 PR #{PR_NUMBER} 状态变更通知"
    
    body_lines = [
        f"PR #{PR_NUMBER} 有更新！",
        f"",
        f"PR 标题: {pr_data.get('title', 'N/A')}",
        f"当前状态: {pr_data.get('state', 'N/A')}",
        f"",
        f"变更内容:",
        f"-" * 40,
    ]
    
    for change in changes:
        body_lines.append(f"• {change}")
    
    body_lines.extend([
        f"",
        f"-" * 40,
        f"",
        f"查看 PR: https://github.com/{REPO}/pull/{PR_NUMBER}",
        f"",
        f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"",
        f"---",
        f"来自 PR 监控脚本",
    ])
    
    body = "\n".join(body_lines)
    
    msg = MIMEMultipart()
    msg['From'] = Header(f"PR Monitor <{FROM_EMAIL}>", 'utf-8')
    msg['To'] = Header(TO_EMAIL, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(FROM_EMAIL, AUTH_CODE)
        server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        server.quit()
        print(f"✅ Notification sent to {TO_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def detect_changes(prev_state, current_data):
    """Detect changes between previous and current state"""
    changes = []
    
    if prev_state is None:
        # 首次运行，只记录状态，不发送通知
        return changes
    
    # Check state changes (open/closed)
    prev_state_val = prev_state.get('state')
    curr_state_val = current_data.get('state')
    if prev_state_val != curr_state_val:
        changes.append(f"状态变更: {prev_state_val} → {curr_state_val}")
    
    # Check if merged (merged 从 false 变成 true)
    prev_merged = prev_state.get('merged', False)
    curr_merged = current_data.get('merged', False)
    if not prev_merged and curr_merged:
        changes.append("🎉 PR 已被合并！")
    
    # Check title changes
    prev_title = prev_state.get('title', '')
    curr_title = current_data.get('title', '')
    if prev_title != curr_title:
        changes.append(f"标题变更: '{prev_title}' → '{curr_title}'")
    
    # Check comment count (只增不减)
    prev_comments = prev_state.get('comments_count', 0)
    curr_comments = current_data.get('comments', 0)
    if curr_comments > prev_comments:
        new_count = curr_comments - prev_comments
        changes.append(f"💬 新增 {new_count} 条评论 (总计 {curr_comments})")
    
    # Check review comment count (只增不减)
    prev_review_comments = prev_state.get('review_comments_count', 0)
    curr_review_comments = current_data.get('review_comments', 0)
    if curr_review_comments > prev_review_comments:
        new_count = curr_review_comments - prev_review_comments
        changes.append(f"🔍 新增 {new_count} 条代码审查评论 (总计 {curr_review_comments})")
    
    # Check for new commits (只增不减)
    prev_commits = prev_state.get('commits_count', 0)
    curr_commits = current_data.get('commits', 0)
    if curr_commits > prev_commits:
        new_count = curr_commits - prev_commits
        changes.append(f"📝 新增 {new_count} 个提交 (总计 {curr_commits})")
    
    # Check for mergeability changes (只关注 true <-> false)
    # GitHub 的 mergeable 有时会是 null（正在计算），忽略这种变化
    prev_mergeable = prev_state.get('mergeable')
    curr_mergeable = current_data.get('mergeable')
    
    if prev_mergeable is False and curr_mergeable is True:
        changes.append("✅ PR 现在可以合并了")
    elif prev_mergeable is True and curr_mergeable is False:
        changes.append("⚠️ PR 现在有冲突，需要解决")
    # 忽略 null -> true 或 true -> null 的变化
    
    # Check labels (集合比较)
    prev_labels = set(prev_state.get('labels', []))
    curr_labels = set(label['name'] for label in current_data.get('labels', []))
    added_labels = curr_labels - prev_labels
    removed_labels = prev_labels - curr_labels
    if added_labels:
        changes.append(f"🏷️ 新增标签: {', '.join(added_labels)}")
    if removed_labels:
        changes.append(f"🏷️ 移除标签: {', '.join(removed_labels)}")
    
    return changes


def extract_state(pr_data):
    """Extract relevant state from PR data"""
    return {
        'state': pr_data.get('state'),
        'title': pr_data.get('title'),
        'merged': pr_data.get('merged', False),
        'mergeable': pr_data.get('mergeable'),  # 可能是 null/true/false
        'comments_count': pr_data.get('comments', 0),
        'review_comments_count': pr_data.get('review_comments', 0),
        'commits_count': pr_data.get('commits', 0),
        'additions': pr_data.get('additions', 0),
        'deletions': pr_data.get('deletions', 0),
        'changed_files': pr_data.get('changed_files', 0),
        'labels': [label['name'] for label in pr_data.get('labels', [])],
        'last_updated': pr_data.get('updated_at'),
        'checked_at': datetime.now().isoformat(),
    }


def main():
    print(f"🔍 Checking PR #{PR_NUMBER} status...")
    print(f"   Repository: {REPO}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load previous state
    prev_state = load_previous_state()
    
    # Fetch current PR data
    pr_data = fetch_pr_data()
    if not pr_data:
        print("❌ Failed to fetch PR data, exiting")
        sys.exit(1)
    
    # Extract current state
    current_state = extract_state(pr_data)
    
    # Detect changes
    changes = detect_changes(prev_state, pr_data)
    
    if changes:
        print("🔄 Changes detected:")
        for change in changes:
            print(f"   • {change}")
        print()
        
        # Send notification
        if send_notification(changes, pr_data):
            print("✅ Notification sent successfully")
        else:
            print("❌ Failed to send notification")
    else:
        print("✅ No changes detected")
    
    # Save current state
    save_state(current_state)
    print(f"💾 State saved to {STATE_FILE}")


if __name__ == "__main__":
    main()
