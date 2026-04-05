#!/bin/bash
# System Health Check Script
# Designed to be run as part of heartbeat automation

echo "🖥️  OpenClaw System Health Check"
echo "==============================="
echo "🕐 Timestamp: $(date)"
echo ""

# System Information
echo "💻 SYSTEM INFO"
echo "-------------"
echo "Hostname: $(hostname)"
echo "OS: $(uname -s) $(uname -r) $(uname -v)"
echo "Uptime: $(uptime -p)"
echo ""

# Resource Usage
echo "📊 RESOURCE USAGE"
echo "----------------"
echo "CPU Load: $(uptime | awk -F'load average:' '{print $2}' | xargs)"
echo "Memory: $(free -h | awk 'NR==2{printf "%.2f/%.2f GB (%s%%)\n", $3/1024/1024, $2/1024/1024, $3*100/$2 }')"
echo "Swap: $(free -h | awk 'NR==3{printf "%.2f/%.2f GB (%s%%)\n", $3/1024/1024, $2/1024/1024, $3*100/$2 }')"
echo "Disk: $(df -h / | awk 'NR==2{printf "%s/%s (%s Used)\n", $3, $2, $5}')"
echo ""

# Process Information
echo "⚙️  PROCESS INFO"
echo "----------------"
echo "Total Processes: $(ps aux | wc -l)"
echo "Your Processes: $(ps -u $USER --no-headers | wc -l)"
echo "OpenClaw Sessions: $(ps aux | grep -i openclaw | grep -v grep | wc -l)"
echo ""

# Network Status (if applicable)
echo "🌐 NETWORK STATUS"
echo "----------------"
echo "Hostname Resolution: $(hostname -i)"
echo "Default Gateway: $(ip route show default 2>/dev/null | awk '{print $3}' || echo "None")"
echo ""

# WSL Specific (if applicable)
if [ -d "/mnt/c" ]; then
    echo "🐧 WSL STATUS"
    echo "------------"
    echo "WSL Distribution: $(grep -oP '(?<=^PRETTY_NAME=).*' /etc/os-release | tr -d '"')"
    echo "WSL Kernel: $(uname -r)"
    echo "Windows Drive Access: /mnt/c ($(df -h /mnt/c | awk 'NR==2{print $5}' | tr -d '%')% used)"
    echo ""
fi

# Service Status
echo "🔧 SERVICE STATUS"
echo "----------------"
echo "SSH Agent: $( [ -n "$SSH_AUTH_SOCK" ] && echo "Running" || echo "Not Running" )"
echo "Docker: $( [ -x "$(command -v docker)" ] && echo "Available" || echo "Not Available" )"
echo "Git: $( [ -x "$(command -v git)" ] && echo "Available (v$(git --version | cut -d' ' -f3))" || echo "Not Available" )"
echo ""

# Summary
echo "📋 SUMMARY"
echo "---------"
UPTIME_SECONDS=$(cat /proc/uptime | cut -d'.' -f1)
UPTIME_HOURS=$((UPTIME_SECONDS / 3600))
if [ $UPTIME_HOURS -lt 1 ]; then
    UPTIME_STATUS="🟢 Freshly booted"
elif [ $UPTIME_HOURS -lt 24 ]; then
    UPTIME_STATUS="🟢 Running normally"
else
    UPTIME_STATUS="🟡 Extended uptime - consider reboot"
fi

MEMORY_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2 }')
if [ "$MEMORY_USAGE" -lt 80 ]; then
    MEMORY_STATUS="🟢 Memory usage normal"
else
    MEMORY_STATUS="🔴 High memory usage"
fi

DISK_USAGE=$(df / | awk 'NR==2{printf "%.0f", $5}' | tr -d '%')
if [ "$DISK_USAGE" -lt 90 ]; then
    DISK_STATUS="🟢 Disk space OK"
else
    DISK_STATUS="🔴 Low disk space warning"
fi

echo "System: $UPTIME_STATUS"
echo "Memory: $MEMORY_STATUS"
echo "Disk:   $DISK_STATUS"
echo ""
echo "💡 This check can be automated to run every 20-30 minutes"
echo "   as part of your OpenClaw heartbeat system!"
echo "==============================="