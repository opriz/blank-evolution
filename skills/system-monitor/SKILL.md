---
name: system-monitor
description: System health monitoring and resource reporting for Linux systems including Raspberry Pi. Use when user asks about system status, CPU/memory/disk usage, temperature monitoring, or wants a system health report. Supports quick basic checks and full detailed reports.
---

# System Monitor Skill

Quickly check system health and resource utilization on Linux systems, with special support for Raspberry Pi hardware monitoring.

## When to Use

- User asks "查看系统状态" / "系统资源怎么样" / "CPU使用率多少"
- Need to check Raspberry Pi temperature, throttling status
- Generate periodic system health reports
- Monitor disk space, memory usage, load average

## Usage

### Quick Basic Check
```bash
bash /home/jian/.openclaw/workspace/skills/system-monitor/scripts/system-monitor.sh
```

### Full Detailed Report
```bash
bash /home/jian/.openclaw/workspace/skills/system-monitor/scripts/system-monitor.sh full
```

## What Gets Reported

**Basic Mode:**
- System info (hostname, kernel, architecture)
- OS version
- CPU model and core count
- Hardware model (Raspberry Pi detection)
- Memory usage (total/used/free)
- Disk usage (all mounted filesystems)
- System load and uptime
- CPU temperature
- Power throttling status (Pi only)
- Process count

**Full Mode** (adds):
- Network interface details
- Top 10 CPU-consuming processes
- System boot time analysis

## Notes

- Script automatically detects Raspberry Pi hardware
- Temperature reading falls back gracefully if not available
- Works on any Linux system with standard tools (lscpu, free, df, ps)
