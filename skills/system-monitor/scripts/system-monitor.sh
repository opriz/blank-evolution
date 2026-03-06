#!/bin/bash
# System Monitor Script - Quick system health check for Linux/Raspberry Pi
# Usage: ./system-monitor.sh [full|basic]

MODE="${1:-basic}"

echo "=========================================="
echo "         系统监控报告 $(date)"
echo "=========================================="
echo ""

# Basic Info
echo "=== 系统信息 ==="
echo "主机名: $(hostname)"
echo "内核: $(uname -r)"
echo "架构: $(uname -m)"
echo ""

# OS Info
if [ -f /etc/os-release ]; then
    echo "=== 操作系统 ==="
    grep -E '^(PRETTY_NAME|NAME|VERSION)=' /etc/os-release | cut -d= -f2 | tr -d '"'
    echo ""
fi

# CPU Info
echo "=== CPU 信息 ==="
if command -v lscpu &>/dev/null; then
    lscpu | grep -E "Model name|Architecture|CPU\(s\)|Thread|Core" 2>/dev/null | head -10
else
    cat /proc/cpuinfo | grep "model name" | head -1
    echo "CPU核心数: $(nproc)"
fi
echo ""

# Hardware Model (for Raspberry Pi)
if [ -f /proc/device-tree/model ]; then
    echo "=== 硬件型号 ==="
    cat /proc/device-tree/model 2>/dev/null
    echo ""
fi

# Memory
echo "=== 内存使用 ==="
free -h
echo ""

# Disk
echo "=== 磁盘使用 ==="
df -h | grep -E "Filesystem|/dev" | head -10
echo ""

# Load & Uptime
echo "=== 系统负载 ==="
uptime
echo ""

# Temperature (Raspberry Pi / Linux with thermal zone)
echo "=== 温度 ==="
if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
    TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo "CPU温度: $(echo "scale=1; $TEMP/1000" | bc)°C"
else
    echo "无法读取温度"
fi
echo ""

# Throttled status (Raspberry Pi specific)
if command -v vcgencmd &>/dev/null; then
    echo "=== 电源状态 ==="
    vcgencmd get_throttled 2>/dev/null || echo "N/A"
    echo ""
fi

# Process count
echo "=== 进程统计 ==="
echo "总进程数: $(ps aux | wc -l)"
echo ""

# Network (if full mode)
if [ "$MODE" = "full" ]; then
    echo "=== 网络信息 ==="
    ip addr | grep -E "^[0-9]|inet " | head -15
    echo ""
    
    echo "=== Top 10 CPU 进程 ==="
    ps aux --sort=-%cpu | head -11
    echo ""
    
    if command -v systemd-analyze &>/dev/null; then
        echo "=== 启动时间 ==="
        systemd-analyze 2>/dev/null
        echo ""
    fi
fi

echo "=========================================="
echo "报告完成"
echo "=========================================="
