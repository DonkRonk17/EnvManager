<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/8b9355da-e79c-42f8-8feb-06dfaff55426" />

# 🔧 EnvManager - Cross-Platform Environment and Service Manager

**Version:** 1.0.0  
**Author:** Logan Smith / Metaphy LLC  
**License:** MIT  
**GitHub:** https://github.com/DonkRonk17/EnvManager

---

## Overview

**EnvManager** is a comprehensive command-line tool for managing environment variables, system services, and Docker containers across Windows, Linux, and macOS. It combines multiple dev ops workflows into a single, easy-to-use interface with **zero external dependencies**.

Perfect for developers who need to quickly switch between development environments, manage system services, and control Docker containers without memorizing platform-specific commands.

---

## Origin Story

**Requested By:** Team Brain collective initiative  
**Initial Request Date:** January 2026  
**Repair Date:** January 27, 2026  

### The Problem

Developers and AI agents constantly struggle with:
- **Platform-specific commands** - Different syntax for Windows (`setx`), Linux (`export`), macOS (`launchctl`)
- **Environment switching** - Manually setting/unsetting dozens of variables when switching projects
- **Service management complexity** - Remembering systemd vs launchd vs Windows services commands
- **Docker overhead** - Opening Docker Desktop just to start/stop containers
- **Configuration persistence** - Losing environment setups between sessions

### The Solution

EnvManager provides a **unified interface** that abstracts away platform differences. Whether you're on Windows, Linux, or macOS, the commands are identical. Environment profiles let you save and instantly restore complete configurations.

---

## Features

### Environment Variable Management
- **List Variables** - View all or filtered environment variables
- **Set/Unset** - Temporary or permanent variable changes
- **Cross-Platform** - Works on Windows (setx), Linux/macOS (shell RC files)
- **Unicode Support** - Handle international characters in values

### Profile System
- **Create Profiles** - Save environment configurations with descriptions
- **Quick Switch** - Load entire environments with one command
- **Profile History** - Track when profiles were last used
- **JSON Storage** - Human-readable profile files

### Service Management
- **List Services** - View all system services (systemd, launchd, Windows services)
- **Start/Stop** - Control services across platforms
- **Status Monitoring** - See which services are running
- **Filter Support** - Find services by name

### Docker Integration
- **Container List** - View running or all containers
- **Quick Control** - Start/stop containers by name or ID
- **Status Viewing** - See container states at a glance
- **Graceful Fallback** - Works even if Docker not installed

### Core Advantages
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Windows, Linux, macOS support
- **Single Interface** - One command for all platforms
- **Fast & Lightweight** - Instant startup, minimal resource usage
- **Persistent Config** - Profiles saved to `~/.envmanager/`
- **Team Brain Compatible** - Integrates with SynapseLink, ConfigManager, etc.

---

## Installation

### Option 1: Direct Installation (Recommended)

```bash
# Clone or download
git clone https://github.com/DonkRonk17/EnvManager.git
cd EnvManager

# Install
pip install .

# Or install in development mode
pip install -e .
```

### Option 2: Manual Setup

```bash
# Make executable (Linux/macOS)
chmod +x envmanager.py

# Run directly
python3 envmanager.py --help

# Or add to PATH
sudo ln -s $(pwd)/envmanager.py /usr/local/bin/envmanager
```

### Option 3: Windows Portable

```powershell
# Add to PATH or run directly
python envmanager.py --help

# Optional: Create alias
Set-Alias envmanager "python C:\path\to\envmanager.py"
```

### Verify Installation

```bash
# Check version
envmanager --version

# Get help
envmanager --help
```

---

## Quick Start

```bash
# 1. Create a development profile
envmanager profile create dev '{"API_URL": "http://localhost:8000", "DEBUG": "true"}'

# 2. List profiles
envmanager profile list

# 3. Load the profile
envmanager profile load dev

# 4. Verify variables are set
envmanager env list --filter API

# 5. Create a production profile
envmanager profile create prod '{"API_URL": "https://api.example.com", "DEBUG": "false"}'

# 6. Switch to production
envmanager profile load prod

# Done! Environment switching in seconds!
```

---

## Usage

### Environment Variables

**List all environment variables:**

```bash
envmanager env list

# Filter by name
envmanager env list --filter PATH
envmanager env list --filter API
```

**Set environment variable:**

```bash
# Temporary (current session only)
envmanager env set API_KEY abc123

# Permanent (survives restart)
envmanager env set API_KEY abc123 --permanent
```

**Unset variable:**

```bash
envmanager env unset API_KEY
```

---

### Profiles

**Create a profile:**

```bash
# Simple profile
envmanager profile create dev '{"API_URL": "http://localhost:8000", "DEBUG": "true"}'

# With description
envmanager profile create prod '{"API_URL": "https://api.example.com"}' --description "Production environment"

# Complex profile
envmanager profile create python-dev '{
  "PYTHONPATH": "/usr/local/lib/python3.9",
  "VIRTUAL_ENV": "/home/user/.venvs/myproject",
  "PATH": "/home/user/.venvs/myproject/bin:$PATH"
}'
```

**List profiles:**

```bash
envmanager profile list
```

**Load a profile:**

```bash
envmanager profile load dev
# All variables from 'dev' profile are now active
```

**Delete profile:**

```bash
envmanager profile delete dev
```

---

### System Services

**List services:**

```bash
# Shows running services (first 20)
envmanager service list
```

**Start/stop services:**

```bash
# Linux (systemd)
envmanager service start nginx
envmanager service stop postgresql

# Windows
envmanager service start "World Wide Web Publishing Service"

# macOS (launchd)
envmanager service start com.apple.music.server
```

---

### Docker Containers

**List containers:**

```bash
# Running containers only
envmanager docker list

# All containers (including stopped)
envmanager docker list --all
```

**Start/stop containers:**

```bash
envmanager docker start my-app
envmanager docker stop my-database
```

---

## Use Cases

### Development Environment Switching

```bash
# Create profiles for different projects
envmanager profile create project-a '{"DB_HOST": "localhost", "API_KEY": "dev-key-a"}'
envmanager profile create project-b '{"DB_HOST": "192.168.1.100", "API_KEY": "dev-key-b"}'

# Switch instantly
envmanager profile load project-a  # Work on project A
envmanager profile load project-b  # Switch to project B
```

### Service Management

```bash
# Check what's running
envmanager service list

# Start development stack
envmanager service start postgresql
envmanager service start redis-server
envmanager docker start my-app-container

# Stop everything
envmanager service stop postgresql
envmanager docker stop my-app-container
```

### CI/CD Scripts

```bash
#!/bin/bash
# deploy.sh

# Load production environment
envmanager profile load production

# Restart services
envmanager service stop nginx
envmanager docker start app-v2
envmanager service start nginx

echo "Deployment complete!"
```

### Multi-Environment Testing

```bash
#!/bin/bash
# test-all-envs.sh

for env in dev staging production; do
    echo "Testing $env environment..."
    envmanager profile load $env
    pytest tests/
    echo "$env tests complete"
done
```

### AI Agent Environment Setup

```python
# Example: AI agent loading correct environment
from envmanager import EnvManager

manager = EnvManager()

# Load environment based on task type
if task.requires_production:
    manager.load_profile("production")
else:
    manager.load_profile("dev")
```

---

## Configuration

EnvManager stores configuration in `~/.envmanager/`:

```
~/.envmanager/
    config.json         # Global configuration
    profiles.json       # Environment profiles
```

### Configuration Format

**config.json:**

```json
{
  "default_profile": null,
  "last_used": "dev"
}
```

**profiles.json:**

```json
{
  "dev": {
    "description": "Development environment",
    "env_vars": {
      "API_URL": "http://localhost:8000",
      "DEBUG": "true"
    },
    "created": "2026-01-15T10:30:00",
    "last_used": "2026-01-15T14:25:00"
  }
}
```

---

## Platform-Specific Notes

### Windows
- Uses `setx` for permanent environment variables
- Manages Windows Services via `sc` command
- Requires administrator privileges for service management
- PowerShell recommended for best experience

### Linux
- Permanent env vars added to `~/.bashrc` or `~/.zshrc`
- Uses `systemctl` for systemd service management
- May require `sudo` for service operations
- Tested on Ubuntu, Debian, Fedora, Arch

### macOS
- Permanent env vars added to `~/.zshrc` or `~/.bashrc`
- Uses `launchctl` for service management
- Docker must be installed separately (Docker Desktop)
- Tested on macOS Monterey, Ventura, Sonoma

---

## API Reference

### EnvManager Class

```python
from envmanager import EnvManager

manager = EnvManager()
```

**Environment Methods:**

| Method | Description |
|--------|-------------|
| `list_env(filter_name=None)` | List environment variables |
| `set_env(name, value, permanent=False)` | Set environment variable |
| `unset_env(name)` | Remove environment variable |

**Profile Methods:**

| Method | Description |
|--------|-------------|
| `create_profile(name, env_vars, description=None)` | Create new profile |
| `list_profiles()` | List all profiles |
| `load_profile(name)` | Load profile variables |
| `delete_profile(name)` | Delete a profile |

**Service Methods:**

| Method | Description |
|--------|-------------|
| `list_services()` | List system services |
| `start_service(name)` | Start a service |
| `stop_service(name)` | Stop a service |

**Docker Methods:**

| Method | Description |
|--------|-------------|
| `list_containers(all_containers=False)` | List Docker containers |
| `start_container(name)` | Start a container |
| `stop_container(name)` | Stop a container |

---

## Troubleshooting

### Common Issues

**"Permission denied" when managing services:**

```bash
# Linux/macOS - use sudo
sudo envmanager service start nginx

# Windows - Run terminal as Administrator
```

**Profile not loading:**

```bash
# Check profile exists
envmanager profile list

# Verify JSON syntax in profiles.json
cat ~/.envmanager/profiles.json | python -m json.tool
```

**Permanent variables not persisting:**

```bash
# Check RC file was modified
cat ~/.bashrc | grep -A5 "EnvManager"

# Reload shell
source ~/.bashrc
```

**Docker commands failing:**

```bash
# Ensure Docker is running
docker ps

# Check if Docker is in PATH
which docker
```

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Profile 'X' not found` | Profile doesn't exist | Create with `profile create` |
| `Failed to start service` | Permission denied | Use sudo/Run as Admin |
| `Docker not available` | Docker not running | Start Docker Desktop |
| `Invalid JSON` | Profile JSON syntax error | Check JSON formatting |

---

## Testing

### Run Test Suite

```bash
cd EnvManager
python test_envmanager.py
```

### Manual Testing

```bash
# Test environment commands
envmanager env list
envmanager env set TEST_VAR hello
envmanager env list --filter TEST

# Test profiles
envmanager profile create test '{"VAR1": "value1"}' --description "Test profile"
envmanager profile list
envmanager profile load test

# Test services (platform-specific)
envmanager service list

# Test Docker (if installed)
envmanager docker list
```
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/fa32ad3f-0d5a-42f5-b712-4bb2b47a8bf7" />

---

## Team Brain Integration

EnvManager is designed to work seamlessly with the Team Brain toolkit:

- **SynapseLink** - Notify team of environment changes
- **ConfigManager** - Store default profile preferences
- **TokenTracker** - Log environment operations
- **MemoryBridge** - Persist environment history
- **SessionReplay** - Record environment state for debugging

See `INTEGRATION_EXAMPLES.md` for detailed integration code.

---

## Related Documentation

| File | Description |
|------|-------------|
| `EXAMPLES.md` | 10+ working examples with output |
| `CHEAT_SHEET.txt` | Quick reference guide |
| `INTEGRATION_PLAN.md` | Team Brain integration architecture |
| `QUICK_START_GUIDES.md` | Agent-specific quick start guides |
| `INTEGRATION_EXAMPLES.md` | Code examples for integrations |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-27 | Professional repair - full documentation, tests, integration |
| 0.5.0 | 2026-01-15 | Initial release - core functionality |

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/DonkRonk17/EnvManager.git
cd EnvManager
pip install -e .
python test_envmanager.py
```

---

## License

MIT License - see LICENSE file for details

---

## 🙏 Credits

Created by **Randell Logan Smith and Team Brain** at [Metaphy LLC](https://metaphysicsandcomputing.com)

Part of the HMSS (Heavenly Morning Star System) ecosystem.

---

## Links

- **GitHub:** https://github.com/DonkRonk17/EnvManager
- **Issues:** https://github.com/DonkRonk17/EnvManager/issues
- **Author:** https://github.com/DonkRonk17
- **AutoProjects:** https://github.com/DonkRonk17?tab=repositories

---

## Support

**Found a bug?** Open an issue on GitHub  
**Feature request?** Open an issue with the "enhancement" label  
**Question?** Check existing issues or start a discussion

---

**EnvManager** - One tool to manage them all!

*Part of the AutoProjects collection - professional CLI tools for developers.*

*Built with care by Team Brain. For the Maximum Benefit of Life.*
