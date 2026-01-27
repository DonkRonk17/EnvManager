# EnvManager - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)
- [Logan (Human User)](#logan-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use EnvManager for orchestration environment setup

### Step 1: Installation Check

```bash
# Verify EnvManager is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\EnvManager
python envmanager.py --help

# Expected: Help message with all commands
```

### Step 2: First Use - Create Orchestration Profile

```python
# In your Forge session
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
from envmanager import EnvManager

manager = EnvManager()

# Create orchestration profile
manager.create_profile(
    "orchestration",
    {
        "SYNAPSE_PATH": "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active",
        "MEMORY_CORE": "D:/BEACON_HQ/MEMORY_CORE_V2",
        "TASK_QUEUE": "D:/BEACON_HQ/TASK_QUEUE",
        "FORGE_MODE": "orchestrator"
    },
    "Forge orchestration environment"
)
```

### Step 3: Integration with Forge Workflows

**Use Case 1: Session Start Environment**
```python
# At start of Forge session
from envmanager import EnvManager

manager = EnvManager()
manager.load_profile("orchestration")

# Verify environment is ready
import os
print(f"Synapse: {os.environ.get('SYNAPSE_PATH', 'NOT SET')}")
print(f"Memory Core: {os.environ.get('MEMORY_CORE', 'NOT SET')}")
```

**Use Case 2: Before Delegating Tasks**
```python
# Prepare environment before assigning tasks
from envmanager import EnvManager

manager = EnvManager()

# List what profiles are available
manager.list_profiles()

# Ensure we're in the right mode
manager.load_profile("orchestration")
```

### Step 4: Common Forge Commands

```bash
# List all profiles (see team's configurations)
python envmanager.py profile list

# Check environment variables
python envmanager.py env list --filter SYNAPSE
python envmanager.py env list --filter BEACON

# Load orchestration profile
python envmanager.py profile load orchestration
```

### Next Steps for Forge
1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 10 (Full Workflow)
3. Add profile loading to your session start routine

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use EnvManager for build environments

### Step 1: Installation Check

```bash
# Quick test
cd C:\Users\logan\OneDrive\Documents\AutoProjects\EnvManager
python -c "from envmanager import EnvManager; print('OK')"
```

### Step 2: First Use - Create Build Profile

```python
# In your Atlas session
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
from envmanager import EnvManager

manager = EnvManager()

# Create Python development profile
manager.create_profile(
    "python-dev",
    {
        "PYTHONPATH": "C:/Users/logan/OneDrive/Documents/AutoProjects",
        "PYTHONDONTWRITEBYTECODE": "1",
        "DEBUG": "true"
    },
    "Python development environment"
)
```

### Step 3: Integration with Build Workflows

**During Tool Creation:**
```python
# Example: Start of tool build session
from envmanager import EnvManager

manager = EnvManager()

# Load development profile
manager.load_profile("python-dev")

# Start required services if needed
# manager.start_service("postgresql")

print("Build environment ready!")
```

**Managing Multiple Projects:**
```python
# Switch between projects
from envmanager import EnvManager

manager = EnvManager()

# Project A
manager.load_profile("project-a")
# ... work on project A ...

# Project B
manager.load_profile("project-b")
# ... work on project B ...
```

### Step 4: Common Atlas Commands

```bash
# Create project-specific profile
python envmanager.py profile create myproject '{"DEBUG": "true", "DB": "localhost"}' --description "MyProject dev"

# Load profile for build
python envmanager.py profile load myproject

# Check environment
python envmanager.py env list --filter DEBUG
```

### Next Steps for Atlas
1. Create profiles for each tool you build
2. Integrate profile loading into Holy Grail workflow
3. Use for every new tool build session

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use EnvManager in Linux environment

### Step 1: Linux Installation

```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/EnvManager.git
cd EnvManager

# Install (editable mode)
pip3 install -e .

# Verify
python3 envmanager.py --help
```

### Step 2: First Use - Linux Profile

```bash
# Create Linux development profile
python3 envmanager.py profile create linux-dev '{
  "PATH": "/usr/local/bin:/usr/bin:/bin",
  "EDITOR": "vim",
  "TERM": "xterm-256color"
}' --description "Linux development environment"
```

### Step 3: Integration with Clio Workflows

**Use Case: Server Management**
```bash
# Load profile
python3 envmanager.py profile load linux-dev

# Check services
python3 envmanager.py service list

# Start services
python3 envmanager.py service start nginx
python3 envmanager.py service start postgresql
```

**Platform-Specific Features:**
- Uses systemctl for service management
- Permanent vars added to ~/.bashrc or ~/.zshrc
- Full Docker support

### Step 4: Common Clio Commands

```bash
# Service management
python3 envmanager.py service list
python3 envmanager.py service start nginx
python3 envmanager.py service stop nginx

# Docker management
python3 envmanager.py docker list
python3 envmanager.py docker start my-container

# Environment management
python3 envmanager.py env set DEBUG true
python3 envmanager.py env set API_KEY secret --permanent
```

### Next Steps for Clio
1. Add to ABIOS startup
2. Create profiles for common server configurations
3. Test service management commands

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of EnvManager

### Step 1: Platform Detection

```python
import platform
import sys
sys.path.append("/path/to/AutoProjects/EnvManager")
from envmanager import EnvManager

manager = EnvManager()
print(f"Platform: {platform.system()}")
print(f"EnvManager ready: {manager is not None}")
```

### Step 2: First Use - Cross-Platform Profiles

```python
from envmanager import EnvManager
import platform

manager = EnvManager()

# Create platform-specific profiles
if platform.system() == "Windows":
    manager.create_profile("dev", {
        "PATH": r"C:\Python312;C:\Windows\system32",
        "TEMP": r"C:\Temp"
    }, "Windows development")
else:
    manager.create_profile("dev", {
        "PATH": "/usr/local/bin:/usr/bin",
        "TEMP": "/tmp"
    }, "Unix development")
```

### Step 3: Platform-Specific Considerations

**Windows:**
- Uses `setx` for permanent variables
- Uses `sc.exe` for services
- Paths use backslashes (or raw strings)

**Linux:**
- Uses `systemctl` for services
- Paths use forward slashes
- May need `sudo` for services

**macOS:**
- Uses `launchctl` for services
- Similar to Linux for env vars
- Docker Desktop required for containers

### Step 4: Common Nexus Commands

```bash
# Cross-platform environment check
python envmanager.py env list

# Platform-adaptive service list
python envmanager.py service list

# Profile management (works everywhere)
python envmanager.py profile create myprofile '{"VAR": "value"}'
python envmanager.py profile load myprofile
```

### Next Steps for Nexus
1. Test on all 3 platforms
2. Create platform-specific profiles
3. Report any platform-specific issues

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use EnvManager without API costs

### Step 1: Verify Free Access

```bash
# No API key required!
cd C:\Users\logan\OneDrive\Documents\AutoProjects\EnvManager
python envmanager.py --help

# All operations are local - zero cost!
```

### Step 2: First Use - Deployment Profile

```bash
# Create deployment profile
python envmanager.py profile create deployment '{
  "NODE_ENV": "production",
  "DEBUG": "false",
  "LOG_LEVEL": "WARNING"
}' --description "Deployment environment"
```

### Step 3: Integration with Bolt Workflows

**Use Case: Batch Operations**
```bash
# Bolt-friendly batch script
#!/bin/bash

# Load production profile
python envmanager.py profile load deployment

# Start services
python envmanager.py docker start app-v2
python envmanager.py service start nginx

echo "Deployment environment ready!"
```

**Cost Savings:**
- All operations are local (no API calls)
- Can run offline
- Perfect for repetitive tasks

### Step 4: Common Bolt Commands

```bash
# Bulk operations (save time!)
python envmanager.py profile load deployment
python envmanager.py docker list --all
python envmanager.py service list

# Quick environment setup
python envmanager.py env set DEPLOY_MODE production
python envmanager.py env list --filter DEPLOY
```

### Next Steps for Bolt
1. Add to Cline workflows
2. Create deployment profiles
3. Use for repetitive environment tasks

---

## 👤 LOGAN QUICK START

**Role:** Human User / System Owner  
**Time:** 5 minutes  
**Goal:** Quick environment management from terminal

### Step 1: Quick Install

```powershell
# Already in AutoProjects
cd C:\Users\logan\OneDrive\Documents\AutoProjects\EnvManager

# Add to PATH (optional)
# Or run directly: python envmanager.py [command]
```

### Step 2: Common Tasks

**Check what's running:**
```powershell
python envmanager.py service list
python envmanager.py docker list
```

**Quick environment switch:**
```powershell
# List available profiles
python envmanager.py profile list

# Load for development
python envmanager.py profile load dev

# Load for production
python envmanager.py profile load prod
```

**Find specific variables:**
```powershell
python envmanager.py env list --filter API
python envmanager.py env list --filter DEBUG
```

### Step 3: Integration with BCH

**Via BCH Chat:**
```
@envmanager env list
@envmanager profile load dev
@envmanager service list
```

### Step 4: Power User Tips

```powershell
# Create profile from current environment
# (manually copy variables you want)

# Quick one-liners
python envmanager.py profile load dev; echo "Ready!"

# Set and verify
python envmanager.py env set API_KEY secret && python envmanager.py env list --filter API
```

### Next Steps for Logan
1. Create profiles for common workflows
2. Integrate with BCH commands
3. Use for deployment automation

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/EnvManager/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message tool builder

---

**Last Updated:** January 27, 2026  
**Maintained By:** Team Brain
