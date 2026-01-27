# EnvManager - Usage Examples

**10+ Real-World Examples with Expected Output**

---

## Quick Navigation

- [Example 1: List All Environment Variables](#example-1-list-all-environment-variables)
- [Example 2: Filter Environment Variables](#example-2-filter-environment-variables)
- [Example 3: Set Temporary Environment Variable](#example-3-set-temporary-environment-variable)
- [Example 4: Set Permanent Environment Variable](#example-4-set-permanent-environment-variable)
- [Example 5: Create Development Profile](#example-5-create-development-profile)
- [Example 6: Create Production Profile](#example-6-create-production-profile)
- [Example 7: Switch Between Profiles](#example-7-switch-between-profiles)
- [Example 8: List System Services](#example-8-list-system-services)
- [Example 9: Manage Docker Containers](#example-9-manage-docker-containers)
- [Example 10: Full Workflow - Project Setup](#example-10-full-workflow---project-setup)
- [Example 11: CI/CD Pipeline Integration](#example-11-cicd-pipeline-integration)
- [Example 12: Multi-Project Environment Management](#example-12-multi-project-environment-management)

---

## Example 1: List All Environment Variables

**Scenario:** You want to see all current environment variables in your shell.

**Command:**
```bash
envmanager env list
```

**Expected Output:**
```
[OK] Current Environment Variables:
----------------------------------------------------------------------
APPDATA                        = C:\Users\logan\AppData\Roaming
COMPUTERNAME                   = WORKSTATION
HOME                           = C:\Users\logan
PATH                           = C:\Python312\;C:\Windows\system32;...
TEMP                           = C:\Users\logan\AppData\Local\Temp
USERNAME                       = logan
...

Total: 67 variable(s)
```

**What You Learned:**
- Variables are displayed alphabetically
- Long values are truncated for readability
- Total count shown at the bottom

---

## Example 2: Filter Environment Variables

**Scenario:** You want to find all PATH-related environment variables.

**Command:**
```bash
envmanager env list --filter PATH
```

**Expected Output:**
```
[OK] Current Environment Variables:
----------------------------------------------------------------------
PATH                           = C:\Python312\;C:\Windows\system32;...
PATHEXT                        = .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE
PSModulePath                   = C:\Users\logan\Documents\PowerShell\Mo...

Total: 3 variable(s)
```

**What You Learned:**
- Filter is case-insensitive
- Searches within variable NAMES (not values)
- Great for finding related variables quickly

---

## Example 3: Set Temporary Environment Variable

**Scenario:** You need to set an API key for the current terminal session only.

**Command:**
```bash
envmanager env set API_KEY sk-test-12345
```

**Expected Output:**
```
[OK] Set API_KEY=sk-test-12345 (session only)
```

**Verification:**
```bash
envmanager env list --filter API_KEY
```

Output:
```
[OK] Current Environment Variables:
----------------------------------------------------------------------
API_KEY                        = sk-test-12345

Total: 1 variable(s)
```

**What You Learned:**
- Temporary variables only persist for the current session
- Closing the terminal removes the variable
- Perfect for testing without permanent changes

---

## Example 4: Set Permanent Environment Variable

**Scenario:** You want to add a permanent environment variable that persists across reboots.

**Command:**
```bash
# Windows
envmanager env set JAVA_HOME "C:\Program Files\Java\jdk-17" --permanent

# Linux/macOS
envmanager env set JAVA_HOME /usr/lib/jvm/java-17 --permanent
```

**Expected Output (Windows):**
```
[OK] Set JAVA_HOME=C:\Program Files\Java\jdk-17 (permanent)
```

**Expected Output (Linux/macOS):**
```
[OK] Added to /home/user/.bashrc (restart shell or source file)
```

**What You Learned:**
- `--permanent` flag makes the change persist
- On Windows, uses `setx` command
- On Linux/macOS, adds to shell RC file (.bashrc or .zshrc)

---

## Example 5: Create Development Profile

**Scenario:** You want to save your development environment configuration for quick loading.

**Command:**
```bash
envmanager profile create dev '{
  "API_URL": "http://localhost:8000",
  "DEBUG": "true",
  "LOG_LEVEL": "DEBUG",
  "DATABASE_URL": "postgresql://localhost:5432/dev_db"
}' --description "Local development environment"
```

**Expected Output:**
```
[OK] Created profile 'dev' with 4 variable(s)
```

**Verification:**
```bash
envmanager profile list
```

Output:
```
[OK] Environment Profiles:
----------------------------------------------------------------------

  dev
    Description: Local development environment
    Variables: 4
    Last Used: Never
```

**What You Learned:**
- Profiles store environment variable configurations
- JSON format for specifying variables
- Description helps identify profile purpose

---

## Example 6: Create Production Profile

**Scenario:** You want to create a production profile with secure settings.

**Command:**
```bash
envmanager profile create prod '{
  "API_URL": "https://api.example.com",
  "DEBUG": "false",
  "LOG_LEVEL": "WARNING",
  "DATABASE_URL": "postgresql://prod-server:5432/prod_db"
}' --description "Production environment"
```

**Expected Output:**
```
[OK] Created profile 'prod' with 4 variable(s)
```

**What You Learned:**
- Multiple profiles for different environments
- Easy to switch between dev/staging/prod
- Keep sensitive values out of code

---

## Example 7: Switch Between Profiles

**Scenario:** You're switching from development to production for a deployment test.

**Commands:**
```bash
# Load development profile
envmanager profile load dev

# Verify dev settings
envmanager env list --filter API_URL

# Switch to production
envmanager profile load prod

# Verify prod settings
envmanager env list --filter API_URL
```

**Expected Output:**
```
[OK] Loaded profile 'dev' (4 variables)

[OK] Current Environment Variables:
----------------------------------------------------------------------
API_URL                        = http://localhost:8000
Total: 1 variable(s)

[OK] Loaded profile 'prod' (4 variables)

[OK] Current Environment Variables:
----------------------------------------------------------------------
API_URL                        = https://api.example.com
Total: 1 variable(s)
```

**What You Learned:**
- Profile loading is instant
- All variables in profile are set at once
- Last used time is tracked automatically

---

## Example 8: List System Services

**Scenario:** You want to see what services are running on your system.

**Command:**
```bash
envmanager service list
```

**Expected Output (Windows):**
```
[OK] System Services:
----------------------------------------------------------------------
  [OK] AdobeARMservice                            RUNNING
  [OK] AudioEndpointBuilder                       RUNNING
  [OK] Audiosrv                                   RUNNING
  [OK] BFE                                        RUNNING
  [ ] BITS                                        STOPPED
  [OK] BrokerInfrastructure                       RUNNING
  ...

Showing 20 of 187 total services
```

**Expected Output (Linux):**
```
[OK] System Services:
----------------------------------------------------------------------
  [OK] nginx.service                              running
  [OK] postgresql.service                         running
  [ ] redis.service                               inactive
  [OK] ssh.service                                running
  ...

Showing 20 of 89 total services
```

**What You Learned:**
- Services displayed with status indicators
- `[OK]` = running, `[ ]` = stopped/inactive
- Shows first 20 services (most relevant)

---

## Example 9: Manage Docker Containers

**Scenario:** You want to manage your Docker development containers.

**Commands:**
```bash
# List running containers
envmanager docker list

# List ALL containers (including stopped)
envmanager docker list --all

# Start a stopped container
envmanager docker start my-postgres

# Stop a running container
envmanager docker stop my-app
```

**Expected Output:**
```
[OK] Docker Containers:
----------------------------------------------------------------------
CONTAINER ID   IMAGE         COMMAND                  STATUS
a1b2c3d4e5f6   postgres:14   "docker-entrypoint..."   Up 2 hours
f6e5d4c3b2a1   redis:7       "docker-entrypoint..."   Up 2 hours

[OK] Started container 'my-postgres'

[OK] Stopped container 'my-app'
```

**What You Learned:**
- Quick Docker management without memorizing commands
- `--all` shows stopped containers too
- Start/stop by container name or ID

---

## Example 10: Full Workflow - Project Setup

**Scenario:** Starting work on a new project that requires specific environment setup.

**Complete Workflow:**
```bash
# Step 1: Create a profile for this project
envmanager profile create myproject '{
  "PROJECT_NAME": "myproject",
  "API_KEY": "proj-secret-key-123",
  "DATABASE_URL": "postgresql://localhost:5432/myproject",
  "REDIS_URL": "redis://localhost:6379/0",
  "DEBUG": "true",
  "PYTHON_ENV": "development"
}' --description "MyProject local development"

# Step 2: Load the profile
envmanager profile load myproject

# Step 3: Verify the environment
envmanager env list --filter PROJECT
envmanager env list --filter API

# Step 4: Start required services
envmanager service start postgresql
envmanager docker start myproject-redis

# Step 5: Begin development!
echo "Environment ready for development"
```

**Expected Output:**
```
[OK] Created profile 'myproject' with 6 variable(s)
[OK] Loaded profile 'myproject' (6 variables)

[OK] Current Environment Variables:
----------------------------------------------------------------------
PROJECT_NAME                   = myproject

Total: 1 variable(s)

[OK] Current Environment Variables:
----------------------------------------------------------------------
API_KEY                        = proj-secret-key-123

Total: 1 variable(s)

[OK] Started service 'postgresql'
[OK] Started container 'myproject-redis'
Environment ready for development
```

**What You Learned:**
- Complete project setup in one workflow
- Profiles + services + Docker all managed together
- Reproducible environment setup every time

---

## Example 11: CI/CD Pipeline Integration

**Scenario:** Using EnvManager in a deployment script.

**Script: deploy.sh**
```bash
#!/bin/bash
# CI/CD Deployment Script using EnvManager

echo "=== Starting Deployment ==="

# Step 1: Load production profile
envmanager profile load production
if [ $? -ne 0 ]; then
    echo "Failed to load production profile!"
    exit 1
fi

# Step 2: Verify critical variables are set
python3 -c "
import os
required = ['API_URL', 'DATABASE_URL', 'SECRET_KEY']
for var in required:
    if not os.environ.get(var):
        print(f'Missing required variable: {var}')
        exit(1)
print('All required variables present')
"

# Step 3: Stop old services
envmanager docker stop app-old || true

# Step 4: Start new services
envmanager docker start app-v2
envmanager service start nginx

echo "=== Deployment Complete ==="
```

**Expected Output:**
```
=== Starting Deployment ===
[OK] Loaded profile 'production' (5 variables)
All required variables present
[OK] Stopped container 'app-old'
[OK] Started container 'app-v2'
[OK] Started service 'nginx'
=== Deployment Complete ===
```

**What You Learned:**
- EnvManager works great in scripts
- Profile loading returns exit codes for error handling
- Combine with other tools for robust deployments

---

## Example 12: Multi-Project Environment Management

**Scenario:** You work on multiple projects that require different environment setups.

**Setup Multiple Profiles:**
```bash
# Project A: Python Flask API
envmanager profile create project-a '{
  "FLASK_APP": "app.py",
  "FLASK_ENV": "development",
  "DATABASE_URL": "postgresql://localhost:5432/project_a",
  "PORT": "5000"
}' --description "Project A - Flask API"

# Project B: Node.js Express App
envmanager profile create project-b '{
  "NODE_ENV": "development",
  "DATABASE_URL": "mongodb://localhost:27017/project_b",
  "PORT": "3000",
  "JWT_SECRET": "dev-secret-key"
}' --description "Project B - Express App"

# Project C: Django Application
envmanager profile create project-c '{
  "DJANGO_SETTINGS_MODULE": "config.settings.development",
  "DATABASE_URL": "postgresql://localhost:5432/project_c",
  "DEBUG": "True",
  "PORT": "8000"
}' --description "Project C - Django App"
```

**Switching Between Projects:**
```bash
# Morning: Work on Project A
cd ~/projects/project-a
envmanager profile load project-a
flask run

# Afternoon: Switch to Project B
cd ~/projects/project-b
envmanager profile load project-b
npm start

# Evening: Quick fix on Project C
cd ~/projects/project-c
envmanager profile load project-c
python manage.py runserver
```

**List All Profiles:**
```bash
envmanager profile list
```

**Output:**
```
[OK] Environment Profiles:
----------------------------------------------------------------------

  project-a
    Description: Project A - Flask API
    Variables: 4
    Last Used: 2026-01-27 09:30

  project-b
    Description: Project B - Express App
    Variables: 4
    Last Used: 2026-01-27 14:15

  project-c
    Description: Project C - Django App
    Variables: 4
    Last Used: 2026-01-27 18:45
```

**What You Learned:**
- Manage unlimited project environments
- Instant context switching between projects
- Never mix up dev/prod settings again

---

## Quick Reference

| Task | Command |
|------|---------|
| List env vars | `envmanager env list` |
| Filter env vars | `envmanager env list --filter NAME` |
| Set temp var | `envmanager env set KEY value` |
| Set permanent var | `envmanager env set KEY value --permanent` |
| Unset var | `envmanager env unset KEY` |
| List profiles | `envmanager profile list` |
| Create profile | `envmanager profile create NAME '{"K":"V"}'` |
| Load profile | `envmanager profile load NAME` |
| Delete profile | `envmanager profile delete NAME` |
| List services | `envmanager service list` |
| Start service | `envmanager service start NAME` |
| Stop service | `envmanager service stop NAME` |
| List containers | `envmanager docker list` |
| List all containers | `envmanager docker list --all` |
| Start container | `envmanager docker start NAME` |
| Stop container | `envmanager docker stop NAME` |

---

## Troubleshooting Examples

### Error: Permission Denied (Services)
```bash
# On Linux, some services require sudo
sudo envmanager service start nginx

# Or run with appropriate permissions
```

### Error: Docker Not Found
```bash
# Docker must be installed and in PATH
envmanager docker list

# Output:
# [X] Docker not installed or not in PATH
```

### Error: Profile Not Found
```bash
envmanager profile load nonexistent

# Output:
# [X] Profile 'nonexistent' not found

# Fix: Create the profile first
envmanager profile create nonexistent '{"VAR": "value"}'
```

---

**More Help:**
- Full Documentation: [README.md](README.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- Integration Guide: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)

---

**Built by:** Team Brain  
**For:** Logan Smith / Metaphy LLC  
**Last Updated:** January 27, 2026
