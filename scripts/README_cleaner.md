# Process Cleaner Scripts

This directory contains scripts to clean up processes and disable autorun services on macOS.

## Scripts

### 1. `clean_processes.sh`
A comprehensive process cleaner that:
- Kills target processes (development tools, system processes, browser helpers)
- Disables Launch Agents and Daemons
- Cleans memory
- Shows system status before and after cleanup

**Usage:**
```bash
./scripts/clean_processes.sh
```

### 2. `advanced_cleaner.sh`
An advanced cleaner with menu interface:
- Quick cleanup (recommended for daily use)
- Aggressive cleanup (kills many processes)
- System status display
- Interactive menu

**Usage:**
```bash
# Interactive mode
./scripts/advanced_cleaner.sh

# Direct commands
./scripts/advanced_cleaner.sh quick      # Quick cleanup
./scripts/advanced_cleaner.sh aggressive # Aggressive cleanup
./scripts/advanced_cleaner.sh status     # Show status
```

## Features

### Process Killing
- Development tools: Windsurf, VS Code, Node.js, npm, yarn
- System processes: mdworker, Spotlight, WebKit helpers
- Browser processes: Chrome, Firefox, Safari helpers
- Communication apps: Slack, Discord, Zoom

### Autorun Disabling
- Launch Agents (user and system)
- Login Items
- Startup applications
- System services (requires sudo)

### Memory Cleanup
- Memory purging (requires sudo)
- Cache cleaning
- Inactive memory clearing

## Safety Features

- **Colored output** for easy reading
- **Confirmation prompts** for aggressive actions
- **Graceful shutdown** before force killing
- **Status monitoring** before and after cleanup
- **Root detection** for privileged operations

## Common Use Cases

### 1. High CPU Usage
```bash
./scripts/advanced_cleaner.sh quick
```

### 2. System Sluggishness
```bash
./scripts/clean_processes.sh
```

### 3. Aggressive Cleanup (when system is very slow)
```bash
./scripts/advanced_cleaner.sh aggressive
```

### 4. Check System Status
```bash
./scripts/advanced_cleaner.sh status
```

## What Gets Cleaned

### Development Tools
- Windsurf Helper processes
- VS Code Helper processes
- Node.js processes
- npm/yarn processes
- Python processes

### System Processes
- mdworker (Spotlight indexing)
- mdworker_shared
- WebKit helpers
- Core services

### Communication Apps
- Slack
- Discord
- Zoom
- Teams

### Browser Helpers
- Chrome Helper
- Firefox
- Safari WebKit processes

## Autorun Items Disabled

### Launch Agents
- com.apple.metadata.mds
- com.apple.mdworker
- com.apple.Spotlight
- Application-specific agents

### Login Items
- Development tools
- Communication apps
- Browser helpers

## Requirements

- macOS
- Bash shell
- sudo access (for some operations)

## Warnings

- **Aggressive cleanup** will terminate many applications
- **Some changes** require restart to take full effect
- **Save your work** before running aggressive cleanup
- **Test with quick cleanup** first

## Troubleshooting

### Permission Denied
```bash
chmod +x scripts/clean_processes.sh
chmod +x scripts/advanced_cleaner.sh
```

### Processes Restarting
Some system processes may restart automatically. This is normal behavior.

### Changes Not Persisting
Some autorun items may reappear after updates. Run the script periodically.

## Customization

You can modify the scripts to:
- Add specific processes to target
- Change the order of cleanup
- Add custom status checks
- Include additional system maintenance tasks
