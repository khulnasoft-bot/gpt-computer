#!/bin/bash

# Advanced Process Cleaner - Targeted Cleanup Script
# More aggressive cleanup with specific process targeting

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to safely kill processes
safe_kill() {
    local process="$1"
    local force="${2:-false}"

    print_status "Cleaning: $process"

    local pids=$(pgrep -f "$process" 2>/dev/null || true)

    if [[ -z "$pids" ]]; then
        print_warning "No processes found: $process"
        return
    fi

    echo "Found PIDs: $pids"

    for pid in $pids; do
        local cmd=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
        print_status "Killing PID $pid ($cmd)"

        if [[ "$force" == "true" ]]; then
            kill -9 "$pid" 2>/dev/null || true
        else
            kill "$pid" 2>/dev/null || true
        fi
    done

    sleep 1
}

# Function to disable startup items
disable_startup() {
    local app_name="$1"

    print_status "Disabling startup for: $app_name"

    # Remove from login items
    osascript -e "tell application \"System Events\" to delete every login item whose name is \"$app_name\"" 2>/dev/null || true

    # Disable launch agents
    launchctl list | grep -i "$app_name" | awk '{print $3}' | while read agent; do
        if [[ -n "$agent" ]]; then
            print_status "Disabling agent: $agent"
            launchctl unload "$HOME/Library/LaunchAgents/$agent.plist" 2>/dev/null || true
        fi
    done
}

# Main cleanup function
aggressive_cleanup() {
    print_header "Aggressive Process Cleanup"

    # Development tools
    safe_kill "Windsurf Helper"
    safe_kill "Code Helper"
    safe_kill "Electron"
    safe_kill "node"
    safe_kill "npm"
    safe_kill "yarn"
    safe_kill "pip"
    safe_kill "python"

    # Browser processes
    safe_kill "Chrome"
    safe_kill "Firefox"
    safe_kill "Safari"
    safe_kill "WebKit"

    # System resource hogs
    safe_kill "mdworker"
    safe_kill "mdworker_shared"
    safe_kill "Spotlight"
    safe_kill "Photos"
    safe_kill "iTunes"
    safe_kill "Music"

    # Force kill stubborn processes
    print_header "Force Killing Stubborn Processes"
    safe_kill "Windsurf" true
    safe_kill "Visual Studio Code" true
    safe_kill "Slack" true
    safe_kill "Discord" true
    safe_kill "Zoom" true

    # Disable startup items
    print_header "Disabling Startup Items"
    disable_startup "Windsurf"
    disable_startup "Slack"
    disable_startup "Discord"
    disable_startup "Zoom"
    disable_startup "Spotify"

    # Clean caches
    print_header "Cleaning Caches"

    # Clear user caches
    rm -rf ~/Library/Caches/* 2>/dev/null || true
    rm -rf ~/Library/Preferences/com.apple.LaunchServices.QuarantineApplicationsV2.plist 2>/dev/null || true

    # Clear system caches (requires sudo)
    if [[ $EUID -eq 0 ]]; then
        rm -rf /Library/Caches/* 2>/dev/null || true
        rm -rf /System/Library/Caches/* 2>/dev/null || true
    fi

    # Memory cleanup
    print_header "Memory Cleanup"
    if [[ $EUID -eq 0 ]]; then
        purge 2>/dev/null || true
    fi

    print_status "Aggressive cleanup completed!"
}

# Quick cleanup function
quick_cleanup() {
    print_header "Quick Cleanup"

    # Only kill the most problematic processes
    safe_kill "Windsurf Helper"
    safe_kill "mdworker"
    safe_kill "mdworker_shared"

    print_status "Quick cleanup completed!"
}

# Show menu
show_menu() {
    echo
    print_header "Process Cleaner Menu"
    echo "1) Quick Cleanup (recommended)"
    echo "2) Aggressive Cleanup"
    echo "3) Show Current Status"
    echo "4) Exit"
    echo
    read -p "Choose an option [1-4]: " choice

    case $choice in
        1)
            quick_cleanup
            ;;
        2)
            echo "This will aggressively kill many processes. Continue? (y/N)"
            read -r confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                aggressive_cleanup
            else
                print_status "Cancelled"
            fi
            ;;
        3)
            show_status
            ;;
        4)
            print_status "Goodbye!"
            exit 0
            ;;
        *)
            print_warning "Invalid option"
            show_menu
            ;;
    esac
}

show_status() {
    print_header "Current System Status"

    echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
    echo "Memory Usage:"
    vm_stat | perl -ne '/page size of (\d+)/ and $ps=$1; /Pages\s+([^:]+)\s+(\d+)/ and printf("%-16s % 16.2f MB\n", $1, $2 * $ps / 1048576)'

    echo
    echo "Top CPU Processes:"
    ps aux | sort -k3 -nr | head -10 | awk 'NR>1 {printf "%-10s %6s%% %s\n", $1, $3, $11}'

    echo
    echo "Top Memory Processes:"
    ps aux | sort -k4 -nr | head -10 | awk 'NR>1 {printf "%-10s %6s%% %s\n", $1, $4, $11}'
}

# Main execution
main() {
    print_header "macOS Process Cleaner"

    if [[ $# -eq 0 ]]; then
        show_menu
    else
        case "$1" in
            "quick")
                quick_cleanup
                ;;
            "aggressive")
                aggressive_cleanup
                ;;
            "status")
                show_status
                ;;
            *)
                echo "Usage: $0 [quick|aggressive|status]"
                exit 1
                ;;
        esac
    fi
}

# Run script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
