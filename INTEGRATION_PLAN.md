# EnvManager - Integration Plan

**Goal:** 100% Utilization & Compliance  
**Target Date:** 1 week from deployment  
**Owner:** Team Brain  
**Version:** 1.0

---

## 🎯 INTEGRATION GOALS

| Goal | Target | Metric |
|------|--------|--------|
| AI Agent Adoption | 100% | 5/5 agents using |
| Daily Usage | 3+ uses/day | Session logs |
| BCH Integration | @mention support | Works in BCH chat |
| Profile Adoption | 10+ profiles | ~/.envmanager/profiles.json |

---

## 📦 BCH INTEGRATION

### Overview

EnvManager can be integrated into BCH (Beacon Command Hub) to allow environment management via chat commands. This is particularly useful for remote system management and deployment coordination.

### API Endpoints Needed

**Endpoint 1:** `/api/tools/envmanager/env/list`
```python
@router.get("/envmanager/env/list")
async def envmanager_list_env(filter: Optional[str] = None):
    """List environment variables."""
    import sys
    sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
    from envmanager import EnvManager
    
    manager = EnvManager()
    env_vars = dict(os.environ)
    
    if filter:
        env_vars = {k: v for k, v in env_vars.items() 
                    if filter.lower() in k.lower()}
    
    return {"status": "success", "variables": env_vars, "count": len(env_vars)}
```

**Endpoint 2:** `/api/tools/envmanager/profile/list`
```python
@router.get("/envmanager/profile/list")
async def envmanager_list_profiles():
    """List all environment profiles."""
    from envmanager import EnvManager
    
    manager = EnvManager()
    profiles = manager._load_profiles()
    
    return {"status": "success", "profiles": list(profiles.keys()), "count": len(profiles)}
```

**Endpoint 3:** `/api/tools/envmanager/profile/load`
```python
@router.post("/envmanager/profile/load")
async def envmanager_load_profile(profile_name: str):
    """Load an environment profile."""
    from envmanager import EnvManager
    
    manager = EnvManager()
    profiles = manager._load_profiles()
    
    if profile_name not in profiles:
        return {"status": "error", "message": f"Profile '{profile_name}' not found"}
    
    manager.load_profile(profile_name)
    return {"status": "success", "message": f"Loaded profile '{profile_name}'"}
```

### @mention Handler

**Pattern:** `@envmanager [command] [args]`

**Examples:**
```
User: @envmanager env list
BCH: [OK] Found 67 environment variables

User: @envmanager profile load dev
BCH: [OK] Loaded profile 'dev' with 4 variables

User: @envmanager profile list
BCH: [OK] Profiles: dev, prod, staging (3 total)
```

**Implementation:**
```python
# In app/services/mention_handler.py

async def handle_envmanager_mention(message: str) -> str:
    """Handle @envmanager mentions."""
    import sys
    sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
    from envmanager import EnvManager
    
    parts = message.replace("@envmanager", "").strip().split()
    if not parts:
        return "Usage: @envmanager env list | profile load NAME | profile list"
    
    manager = EnvManager()
    command = parts[0]
    
    if command == "env":
        if len(parts) > 1 and parts[1] == "list":
            count = len(os.environ)
            return f"[OK] Found {count} environment variables"
    
    elif command == "profile":
        if len(parts) > 1:
            if parts[1] == "list":
                profiles = manager._load_profiles()
                names = ", ".join(profiles.keys()) if profiles else "None"
                return f"[OK] Profiles: {names} ({len(profiles)} total)"
            elif parts[1] == "load" and len(parts) > 2:
                profile_name = parts[2]
                manager.load_profile(profile_name)
                return f"[OK] Loaded profile '{profile_name}'"
    
    return "Unknown command. Try: env list, profile list, profile load NAME"
```

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Orchestration environment setup | Python API | HIGH |
| **Atlas** | Tool build environment management | CLI + Python | HIGH |
| **Clio** | Linux environment configuration | CLI | HIGH |
| **Nexus** | Multi-platform env management | Python API | MEDIUM |
| **Bolt** | Deployment environment prep | CLI | MEDIUM |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Setting up environment before orchestrating multi-agent tasks

**Integration Steps:**
1. Import EnvManager at session start
2. Load appropriate profile for task type
3. Verify environment before delegating

**Example Workflow:**
```python
# Forge session start
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
from envmanager import EnvManager

manager = EnvManager()

# Load orchestration profile
manager.load_profile("orchestration")

# Verify critical env vars are set
import os
required = ["SYNAPSE_PATH", "MEMORY_CORE", "TASK_QUEUE"]
for var in required:
    if not os.environ.get(var):
        print(f"[!] Warning: {var} not set!")
```

#### Atlas (Executor / Builder)

**Primary Use Case:** Managing build environments for different tool projects

**Integration Steps:**
1. Create profiles for each project type (Python, Node, etc.)
2. Load profile when starting a build session
3. Use service/Docker commands to start dependencies

**Example Workflow:**
```python
# Atlas building a new tool
from envmanager import EnvManager

manager = EnvManager()

# Load Python development profile
manager.load_profile("python-dev")

# Start required services
manager.start_service("postgresql")

# Verify build environment
manager.list_env(filter_str="PYTHON")
```

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Linux environment configuration and service management

**Platform Considerations:**
- Uses systemctl for services
- Shell RC files for permanent env vars
- Docker common on Linux servers

**Example:**
```bash
# Clio CLI usage
cd ~/AutoProjects/EnvManager

# Create Linux-specific profile
envmanager profile create linux-dev '{"PATH": "/usr/local/go/bin:$PATH", "GOPATH": "/home/clio/go"}'

# Load and verify
envmanager profile load linux-dev
envmanager env list --filter GO

# Manage services
envmanager service list
envmanager service start nginx
```

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Managing environments across Windows, Linux, macOS

**Cross-Platform Notes:**
- EnvManager automatically detects platform
- Same commands work everywhere
- Profile format is universal

**Example:**
```python
# Nexus cross-platform script
from envmanager import EnvManager
import platform

manager = EnvManager()
system = platform.system()

# Load platform-appropriate profile
if system == "Windows":
    manager.load_profile("windows-dev")
elif system == "Linux":
    manager.load_profile("linux-dev")
else:
    manager.load_profile("macos-dev")

print(f"Loaded {system} profile successfully")
```

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Preparing deployment environments

**Cost Considerations:**
- All operations are local (no API costs)
- Can run offline
- Fast execution

**Example:**
```bash
# Bolt deployment workflow
cd ~/AutoProjects/EnvManager

# Load production profile
envmanager profile load production

# Verify critical settings
envmanager env list --filter API
envmanager env list --filter DATABASE

# Start deployment services
envmanager docker start app-v2
envmanager service start nginx
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With ConfigManager
**Configuration Use Case:** Centralize EnvManager settings

```python
from configmanager import ConfigManager
from envmanager import EnvManager

config = ConfigManager()
manager = EnvManager()

# Get default profile from centralized config
default_profile = config.get("envmanager.default_profile", "dev")
manager.load_profile(default_profile)

# Store preferred settings
config.set("envmanager.default_profile", "dev")
config.save()
```

### With TokenTracker
**Usage Logging Use Case:** Track environment changes for audit

```python
from tokentracker import TokenTracker
from envmanager import EnvManager

tracker = TokenTracker()
manager = EnvManager()

# Log profile changes
profile_name = "production"
manager.load_profile(profile_name)

tracker.log_usage(
    agent="ATLAS",
    model="local",
    input_tokens=0,
    output_tokens=0,
    task=f"EnvManager: Loaded profile '{profile_name}'"
)
```

### With SynapseLink
**Team Notification Use Case:** Announce environment changes

```python
from synapselink import quick_send
from envmanager import EnvManager

manager = EnvManager()

# Load production profile for deployment
manager.load_profile("production")

# Notify team
quick_send(
    "TEAM",
    "Environment Switch: Production",
    "EnvManager loaded production profile for deployment.\n"
    "All services ready. Starting deployment sequence.",
    priority="HIGH"
)
```

### With AgentHealth
**Health Monitoring Use Case:** Include environment info in health reports

```python
from agenthealth import AgentHealth
from envmanager import EnvManager
import os

health = AgentHealth()
manager = EnvManager()

# Include environment status in health check
profiles = manager._load_profiles()
config = manager._load_config()

health.log_metric("ATLAS", "envmanager_profiles", len(profiles))
health.log_metric("ATLAS", "envmanager_last_profile", config.get("last_used", "none"))
```

### With SessionReplay
**Debug Recording Use Case:** Log environment state for replay

```python
from sessionreplay import SessionReplay
from envmanager import EnvManager
import os

replay = SessionReplay()
manager = EnvManager()

session_id = replay.start_session("ATLAS", task="Deployment")

# Log environment state
replay.log_input(session_id, "Environment Variables:")
for key in ["API_URL", "DEBUG", "DATABASE_URL"]:
    value = os.environ.get(key, "NOT SET")
    replay.log_input(session_id, f"  {key}={value}")

# Perform operations
manager.load_profile("production")
replay.log_output(session_id, "Loaded production profile")
```

### With MemoryBridge
**Persistence Use Case:** Store environment history in memory core

```python
from memorybridge import MemoryBridge
from envmanager import EnvManager
from datetime import datetime

memory = MemoryBridge()
manager = EnvManager()

# Load profile
profile_name = "dev"
manager.load_profile(profile_name)

# Record in memory core
history = memory.get("envmanager_history", [])
history.append({
    "timestamp": datetime.now().isoformat(),
    "profile": profile_name,
    "agent": "ATLAS"
})

# Keep last 100 entries
memory.set("envmanager_history", history[-100:])
memory.sync()
```

### With ContextCompressor
**Large Config Compression Use Case:** Compress environment exports

```python
from contextcompressor import ContextCompressor
from envmanager import EnvManager
import json

compressor = ContextCompressor()
manager = EnvManager()

# Get all profiles
profiles = manager._load_profiles()
profile_json = json.dumps(profiles, indent=2)

# Compress for sharing
if len(profile_json) > 1000:
    compressed = compressor.compress_text(
        profile_json,
        query="environment profiles",
        method="summary"
    )
    print(f"Compressed profiles from {len(profile_json)} to {len(compressed.compressed_text)} chars")
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
- [ ] Day 1: Deploy to GitHub (if not already)
- [ ] Day 2: Send quick-start guides via Synapse
- [ ] Day 3: Each agent tests basic workflow
- [ ] Day 4: Collect feedback via Synapse
- [ ] Day 5: Address any issues

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported
- Basic profiles created

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
- [ ] Add to agent startup routines
- [ ] Create integration examples with existing tools
- [ ] Update agent-specific workflows
- [ ] Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested
- 10+ profiles created across team

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
- [ ] Collect efficiency metrics
- [ ] Implement v1.1 improvements
- [ ] Create advanced workflow examples
- [ ] Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time/cost savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
| Metric | Target | Track Via |
|--------|--------|-----------|
| Agents using | 5/5 (100%) | Synapse reports |
| Profiles created | 10+ | profiles.json |
| Daily usage | 3+ times | Session logs |

**Efficiency Metrics:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| Time saved per env switch | 2+ minutes | Manual comparison |
| Profile load time | <1 second | Performance test |
| Error reduction | 50%+ | Before/after comparison |

**Quality Metrics:**
| Metric | Target | Track Via |
|--------|--------|-----------|
| Bug reports | <3 | GitHub issues |
| Feature requests | 5+ | GitHub issues |
| User satisfaction | High | Synapse feedback |

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
from envmanager import EnvManager

# Direct file execution
python "C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager/envmanager.py" env list
```

### Configuration Integration

**EnvManager Config:** `~/.envmanager/`

**Shared Config Pattern:**
```json
{
  "envmanager": {
    "default_profile": "dev",
    "auto_load": true,
    "log_changes": true
  }
}
```

### Error Handling Integration

**Standardized Error Codes:**
- 0: Success
- 1: General error
- 2: Profile not found
- 3: Service operation failed
- 4: Docker operation failed
- 5: Permission denied

### Logging Integration

**Log Format:** Compatible with Team Brain standard

**Log Location:** Can output to session logs or dedicated file

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy
- Minor updates (v1.x): Monthly
- Major updates (v2.0+): Quarterly
- Bug fixes: As needed (ASAP)

### Support Channels
- GitHub Issues: Bug reports, feature requests
- Synapse: Team Brain discussions
- Direct to Builder: Complex issues

### Known Limitations
- Windows service management requires admin privileges
- Docker must be installed separately
- Permanent env vars require shell restart

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- GitHub: https://github.com/DonkRonk17/EnvManager

---

**Last Updated:** January 27, 2026  
**Maintained By:** Team Brain  
**For:** Logan Smith / Metaphy LLC
