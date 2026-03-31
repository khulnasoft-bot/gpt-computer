#!/bin/bash

# Process Cleaner Script for macOS
# Kills target processes and disables autorun services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. Be careful!"
        return 0
    else
        print_status "Running as user: $(whoami)"
        return 1
    fi
}

# Function to kill processes by name
kill_process() {
    local process_name="$1"
    print_status "Attempting to kill process: $process_name"

    # Find PIDs
    local pids=$(pgrep -f "$process_name" 2>/dev/null || true)

    if [[ -z "$pids" ]]; then
        print_warning "No processes found matching: $process_name"
        return
    fi

    print_status "Found PIDs: $pids"

    # Try graceful kill first
    for pid in $pids; do
        if kill "$pid" 2>/dev/null; then
            print_status "Sent SIGTERM to PID $pid"
        else
            print_error "Failed to kill PID $pid"
        fi
    done

    # Wait a moment
    sleep 2

    # Check if processes are still running and force kill if needed
    local remaining_pids=$(pgrep -f "$process_name" 2>/dev/null || true)
    if [[ -n "$remaining_pids" ]]; then
        print_warning "Some processes still running, force killing..."
        for pid in $remaining_pids; do
            if kill -9 "$pid" 2>/dev/null; then
                print_status "Force killed PID $pid"
            fi
        done
    fi

    print_status "Process cleanup completed for: $process_name"
}

# Function to disable launch agents
disable_launch_agent() {
    local agent_name="$1"
    print_status "Disabling Launch Agent: $agent_name"

    local user_agents="$HOME/Library/LaunchAgents"
    local system_agents="/Library/LaunchAgents"
    local global_agents="/System/Library/LaunchAgents"

    # Check user agents first
    if [[ -f "$user_agents/$agent_name.plist" ]]; then
        launchctl unload "$user_agents/$agent_name.plist" 2>/dev/null || true
        print_status "Disabled user agent: $agent_name"
    fi

    # Check system agents (requires sudo)
    if check_root; then
        if [[ -f "$system_agents/$agent_name.plist" ]]; then
            launchctl unload "$system_agents/$agent_name.plist" 2>/dev/null || true
            print_status "Disabled system agent: $agent_name"
        fi

        if [[ -f "$global_agents/$agent_name.plist" ]]; then
            launchctl unload "$global_agents/$agent_name.plist" 2>/dev/null || true
            print_status "Disabled global agent: $agent_name"
        fi
    fi
}

# Function to disable launch daemons (requires sudo)
disable_launch_daemon() {
    local daemon_name="$1"

    if ! check_root; then
        print_warning "Cannot disable system daemons without sudo. Skipping: $daemon_name"
        return
    fi

    print_status "Disabling Launch Daemon: $daemon_name"

    local system_daemons="/Library/LaunchDaemons"
    local global_daemons="/System/Library/LaunchDaemons"

    if [[ -f "$system_daemons/$daemon_name.plist" ]]; then
        launchctl unload "$system_daemons/$daemon_name.plist" 2>/dev/null || true
        print_status "Disabled system daemon: $daemon_name"
    fi

    if [[ -f "$global_daemons/$daemon_name.plist" ]]; then
        launchctl unload "$global_daemons/$daemon_name.plist" 2>/dev/null || true
        print_status "Disabled global daemon: $daemon_name"
    fi
}

# Function to clean memory
clean_memory() {
    print_status "Cleaning memory..."

    # Purge memory (requires sudo)
    if check_root; then
        purge 2>/dev/null || print_warning "Could not purge memory (requires sudo)"
    else
        print_warning "Memory purge requires sudo. Skipping."
    fi

    # Clear inactive memory
    sudo memory_pressure 2>/dev/null || true
}

# Function to show current status
show_status() {
    print_header "Current System Status"

    print_status "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
    print_status "Memory Usage: $(vm_stat | perl -ne '/page size of (\d+)/ and $ps=$1; /Pages\s+([^:]+)\s+(\d+)/ and printf("%-16s % 16.2f MB\n", $1, $2 * $ps / 1048576)')"

    print_header "Top CPU Processes"
    ps aux | sort -k3 -nr | head -10 | awk 'NR>1 {printf "%-10s %6s%% %s\n", $1, $3, $11}'

    print_header "Top Memory Processes"
    ps aux | sort -k4 -nr | head -10 | awk 'NR>1 {printf "%-10s %6s%% %s\n", $1, $4, $11}'
}

# Main function
main() {
    print_header "macOS Process Cleaner"

    # Show current status
    show_status

    echo
    read -p "Do you want to proceed with process cleanup? (y/N): " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cancelled by user"
        exit 0
    fi

    # Common problematic processes to clean
    print_header "Cleaning Common Problematic Processes"

    # Development tools
    kill_process "Windsurf Helper"
    kill_process "Code Helper"
    kill_process "node"
    kill_process "npm"
    kill_process "yarn"

    # System processes that often consume resources
    kill_process "mdworker"
    kill_process "mdworker_shared"
    kill_process "Spotlight"

    # Browser helpers
    kill_process "WebKit"
    kill_process "Chrome Helper"
    kill_process "Firefox"

    # Disable common autorun agents
    print_header "Disabling Common Launch Agents"

    disable_launch_agent "com.apple.metadata.mds"
    disable_launch_agent "com.apple.mdworker"
    disable_launch_agent "com.apple.Spotlight"

    # Clean memory
    print_header "Memory Cleanup"
    clean_memory

    # Show final status
    echo
    show_status

    print_header "Cleanup Complete"
    print_status "Process cleanup and autorun disabling completed!"
    print_warning "Some changes may require a restart to take full effect."
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
