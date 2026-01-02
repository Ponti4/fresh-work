#!/bin/bash
# Mac/Linux System Information Auto Detection Script
# Purpose: Automatic collection of user system information for setup-workspace step
# Usage: bash ./02-detect-system-macos.sh

set -e

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

OS_TYPE=$(detect_os)

# JSON output preparation
declare -A system_info
system_info["os_type"]=$OS_TYPE
system_info["timestamp"]=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# 1. Detect Python
echo -e "${CYAN}Checking Python version...${NC}"
python_installed="false"
python_version="Not installed"
python_path=""

if command -v python3 &> /dev/null; then
    python_installed="true"
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    python_path=$(command -v python3)
elif command -v python &> /dev/null; then
    python_installed="true"
    python_version=$(python --version 2>&1 | awk '{print $2}')
    python_path=$(command -v python)
fi

# 2. OS Information
echo -e "${CYAN}Checking OS information...${NC}"
if [[ "$OS_TYPE" == "macos" ]]; then
    os_name=$(sw_vers -productName)
    os_version=$(sw_vers -productVersion)
    os_build=$(sw_vers -buildVersion)
    architecture=$(uname -m)
elif [[ "$OS_TYPE" == "linux" ]]; then
    if [[ -f /etc/os-release ]]; then
        os_name=$(grep "^NAME=" /etc/os-release | cut -d'"' -f2)
        os_version=$(grep "^VERSION_ID=" /etc/os-release | cut -d'"' -f2)
    else
        os_name=$(lsb_release -ds 2>/dev/null || echo "Unknown Linux")
        os_version=$(lsb_release -rs 2>/dev/null || echo "Unknown")
    fi
    os_build=$(uname -r)
    architecture=$(uname -m)
fi

# 3. CPU Information
echo -e "${CYAN}Checking CPU information...${NC}"
if [[ "$OS_TYPE" == "macos" ]]; then
    cpu_name=$(sysctl -n machdep.cpu.brand_string)
    cpu_cores=$(sysctl -n hw.phycpu_max)
    cpu_logical=$(sysctl -n hw.logicalcpu_max)
    cpu_speed=$(sysctl -n hw.cpufrequency_max | awk '{print int($1/1000000000)"."substr(int($1/1000000)%1000,1,2)" GHz"}')
elif [[ "$OS_TYPE" == "linux" ]]; then
    cpu_name=$(grep "model name" /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs)
    cpu_cores=$(grep -c "^processor" /proc/cpuinfo)
    cpu_logical=$cpu_cores
    cpu_speed=$(grep "cpu MHz" /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs | awk '{printf "%.2f GHz", $1/1000}')
fi

# 4. RAM Information
echo -e "${CYAN}Checking RAM information...${NC}"
if [[ "$OS_TYPE" == "macos" ]]; then
    total_ram=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}" GB"}')
    available_ram=$(vm_stat | grep "Pages free" | awk '{print int($3*4096/1024/1024/1024)}" GB"}')
elif [[ "$OS_TYPE" == "linux" ]]; then
    total_ram=$(free -h | grep "^Mem:" | awk '{print $2}')
    available_ram=$(free -h | grep "^Mem:" | awk '{print $7}')
fi

# 5. GPU Information
echo -e "${CYAN}Checking GPU information...${NC}"
gpu_count=0
gpu_devices=()

if [[ "$OS_TYPE" == "macos" ]]; then
    gpu_info=$(system_profiler SPDisplaysDataType 2>/dev/null)
    if echo "$gpu_info" | grep -q "Chipset Model"; then
        gpu_devices=$(echo "$gpu_info" | grep "Chipset Model:" | awk -F': ' '{print $2}')
        gpu_count=$(echo "$gpu_devices" | wc -l)
    fi
elif [[ "$OS_TYPE" == "linux" ]]; then
    if command -v lspci &> /dev/null; then
        gpu_devices=$(lspci | grep -E "VGA|3D|Display" | cut -d':' -f3- | sed 's/^[[:space:]]*//')
        gpu_count=$(echo "$gpu_devices" | wc -l)
    fi
    if command -v nvidia-smi &> /dev/null; then
        nvidia_gpu=$(nvidia-smi --query-gpu=name --format=csv,noheader)
        gpu_devices="$gpu_devices
$nvidia_gpu"
        gpu_count=$((gpu_count + 1))
    fi
fi

# 6. Disk Information
echo -e "${CYAN}Checking disk information...${NC}"
if [[ "$OS_TYPE" == "macos" ]]; then
    disk_info=$(df -h / | tail -1)
    total_disk=$(echo $disk_info | awk '{print $2}')
    free_disk=$(echo $disk_info | awk '{print $4}')
elif [[ "$OS_TYPE" == "linux" ]]; then
    disk_info=$(df -h / | tail -1)
    total_disk=$(echo $disk_info | awk '{print $2}')
    free_disk=$(echo $disk_info | awk '{print $4}')
fi

# Console output (human-readable format)
echo ""
echo -e "${CYAN}=====================================================.${NC}"
echo -e "${CYAN}Collected System Information:${NC}"
echo -e "${CYAN}=====================================================.${NC}"

echo ""
echo -e "${YELLOW}OS Information${NC}"
echo "   OS: $os_name"
echo "   Version: $os_version"
[[ ! -z "$os_build" ]] && echo "   Build: $os_build"
echo "   Architecture: $architecture"

echo ""
echo -e "${YELLOW}Python${NC}"
if [[ "$python_installed" == "true" ]]; then
    echo "   Status: Installed"
    echo "   Version: $python_version"
    echo "   Path: $python_path"
else
    echo "   Status: Not Installed"
fi

echo ""
echo -e "${YELLOW}CPU${NC}"
echo "   Name: $cpu_name"
echo "   Cores: $cpu_cores cores / $cpu_logical threads"
[[ ! -z "$cpu_speed" ]] && echo "   Speed: $cpu_speed"

echo ""
echo -e "${YELLOW}RAM${NC}"
echo "   Total: $total_ram"
echo "   Available: $available_ram"

if [[ $gpu_count -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}GPU${NC}"
    while IFS= read -r device; do
        [[ ! -z "$device" ]] && echo "   - $device"
    done <<< "$gpu_devices"
fi

echo ""
echo -e "${YELLOW}Disk${NC}"
echo "   Total: $total_disk"
echo "   Free: $free_disk"

echo ""
echo -e "${CYAN}=====================================================.${NC}"

# JSON file output
echo ""
echo -e "${GREEN}System information collection completed!${NC}"

output_file="$(dirname "$0")/system-info.json"
cat > "$output_file" << EOF
{
  "os_type": "$OS_TYPE",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "os": {
    "name": "$os_name",
    "version": "$os_version",
    "build": "$os_build",
    "architecture": "$architecture"
  },
  "python": {
    "installed": $python_installed,
    "version": "$python_version",
    "path": "$python_path"
  },
  "cpu": {
    "name": "$cpu_name",
    "cores": $cpu_cores,
    "logical_processors": $cpu_logical,
    "speed": "$cpu_speed"
  },
  "memory": {
    "total": "$total_ram",
    "available": "$available_ram"
  },
  "gpu": {
    "count": $gpu_count,
    "devices": [
$(for device in $gpu_devices; do echo "      \"$device\","; done | sed '$ s/,$//')
    ]
  },
  "disk": {
    "total": "$total_disk",
    "free": "$free_disk"
  }
}
EOF

echo -e "${GREEN}Information saved to: $output_file${NC}"
