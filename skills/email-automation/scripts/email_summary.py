#!/usr/bin/env python3
"""
Generate daily/periodic email summaries
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from email_check import check_inbox, classify_importance
from datetime import datetime
import json

def generate_summary(hours=24, limit=50):
    """Generate email summary for recent period"""
    
    print(f"\n📧 Email Summary")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Period: Last {hours} hours\n")
    print("=" * 60)
    
    # Fetch recent emails
    emails = check_inbox(limit)
    
    if not emails:
        print("\nNo emails found or error accessing inbox.\n")
        return
    
    # Classify all emails
    categorized = {'HIGH': [], 'MEDIUM': [], 'NORMAL': [], 'LOW': []}
    for e in emails:
        importance = classify_importance(e)
        categorized[importance].append(e)
    
    # Summary stats
    total = len(emails)
    print(f"\n📊 Statistics:")
    print(f"   Total emails: {total}")
    print(f"   🔴 High priority: {len(categorized['HIGH'])}")
    print(f"   🟡 Medium priority: {len(categorized['MEDIUM'])}")
    print(f"   ⚪ Normal: {len(categorized['NORMAL'])}")
    print(f"   ⚫ Low/Newsletter: {len(categorized['LOW'])}")
    
    # High priority emails
    if categorized['HIGH']:
        print(f"\n🔴 HIGH PRIORITY ({len(categorized['HIGH'])}):\n")
        for e in categorized['HIGH']:
            print(f"   📨 {e['subject']}")
            print(f"      From: {e['from']}")
            print(f"      Preview: {e['preview'][:150]}...")
            print()
    
    # Medium priority
    if categorized['MEDIUM']:
        print(f"\n🟡 MEDIUM PRIORITY ({len(categorized['MEDIUM'])}):\n")
        for e in categorized['MEDIUM']:
            print(f"   📨 {e['subject']}")
            print(f"      From: {e['from']}")
            print()
    
    # Other emails (just list)
    if categorized['NORMAL']:
        print(f"\n⚪ OTHER EMAILS ({len(categorized['NORMAL'])}):\n")
        for e in categorized['NORMAL'][:10]:  # Limit to 10
            print(f"   • {e['subject']} - {e['from']}")
        if len(categorized['NORMAL']) > 10:
            print(f"   ... and {len(categorized['NORMAL']) - 10} more")
    
    print("\n" + "=" * 60)
    
    # Save summary to file
    summary_file = f"/tmp/email_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Email Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {total} emails\n\n")
        f.write("HIGH PRIORITY:\n")
        for e in categorized['HIGH']:
            f.write(f"- {e['subject']} (from: {e['from']})\n")
    
    print(f"\n💾 Summary saved to: {summary_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate email summary')
    parser.add_argument('--hours', type=int, default=24, help='Hours to look back')
    parser.add_argument('--limit', type=int, default=50, help='Max emails to check')
    args = parser.parse_args()
    
    generate_summary(args.hours, args.limit)

if __name__ == '__main__':
    main()
