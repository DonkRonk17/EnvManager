<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/8b9355da-e79c-42f8-8feb-06dfaff55426" />

# 🔧 EnvManager - Cross-Platform Environment and Service Manager

**Version:** 1.0.0  
**Author:** Logan Smith / Metaphy LLC  
**License:** MIT  
**GitHub:** https://github.com/DonkRonk17/EnvManager

---

## 📖 Overview

**EnvManager** is a comprehensive command-line tool for managing environment variables, system services, and Docker containers across Windows, Linux, and macOS. It combines multiple dev ops workflows into a single, easy-to-use interface with **zero external dependencies**.

Perfect for developers who need to quickly switch between development environments, manage system services, and control Docker containers without memorizing platform-specific commands.

---

## ✨ Features

### 🌍 Environment Variable Management
- **List Variables** - View all or filtered environment variables
- **Set/Unset** - Temporary or permanent variable changes
- **Cross-Platform** - Works on Windows (setx), Linux/macOS (shell RC files)

### 📦 Profile System
- **Create Profiles** - Save environment configurations
- **Quick Switch** - Load entire environments with one command
- **Profile History** - Track when profiles were last used

### ⚙️ Service Management
- **List Services** - View all system services (systemd, launchd, Windows services)
- **Start/Stop** - Control services across platforms
- **Status Monitoring** - See which services are running

### 🐳 Docker Integration
- **Container List** - View running or all containers
- **Quick Control** - Start/stop containers by name or ID
- **Status Viewing** - See container states at a glance

### 🎯 Core Advantages
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Windows, Linux, macOS support
- **Single Interface** - One command for all platforms
- **Fast & Lightweight** - Instant startup, minimal resource usage
- **Persistent Config** - Profiles saved to `~/.envmanager/`

---

## 🚀 Installation

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
```

---

## 📚 Usage

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

## 💡 Use Cases

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

---

## 🗂️ Configuration

EnvManager stores configuration in `~/.envmanager/`:

```
~/.envmanager/
├── config.json         # Global configuration
└── profiles.json       # Environment profiles
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

## 🔧 Platform-Specific Notes

### Windows
- Uses `setx` for permanent environment variables
- Manages Windows Services via `sc` command
- Requires administrator privileges for service management

### Linux
- Permanent env vars added to `~/.bashrc` or `~/.zshrc`
- Uses `systemctl` for systemd service management
- May require `sudo` for service operations

### macOS
- Permanent env vars added to `~/.zshrc` or `~/.bashrc`
- Uses `launchctl` for service management
- Docker must be installed separately (Docker Desktop)

---

## 🧪 Testing

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

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built with ❤️ by Logan Smith / Metaphy LLC

Part of the AutoProjects collection - professional CLI tools for developers.

---

## 🔗 Links

- **GitHub:** https://github.com/DonkRonk17/EnvManager
- **Issues:** https://github.com/DonkRonk17/EnvManager/issues
- **Author:** https://github.com/DonkRonk17

---

**EnvManager** - One tool to manage them all! 🚀
