# EnvManager - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

EnvManager is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: EnvManager + ConfigManager](#pattern-1-envmanager--configmanager)
2. [Pattern 2: EnvManager + SynapseLink](#pattern-2-envmanager--synapselink)
3. [Pattern 3: EnvManager + TokenTracker](#pattern-3-envmanager--tokentracker)
4. [Pattern 4: EnvManager + MemoryBridge](#pattern-4-envmanager--memorybridge)
5. [Pattern 5: EnvManager + SessionReplay](#pattern-5-envmanager--sessionreplay)
6. [Pattern 6: EnvManager + AgentHealth](#pattern-6-envmanager--agenthealth)
7. [Pattern 7: EnvManager + TaskQueuePro](#pattern-7-envmanager--taskqueuepro)
8. [Pattern 8: EnvManager + ContextCompressor](#pattern-8-envmanager--contextcompressor)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: EnvManager + ConfigManager

**Use Case:** Centralize EnvManager settings with ConfigManager

**Why:** Share default profiles and settings across tools and agents

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ConfigManager")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from configmanager import ConfigManager
from envmanager import EnvManager

# Initialize both tools
config = ConfigManager()
manager = EnvManager()

# Get default profile from centralized config
default_profile = config.get("envmanager.default_profile", "dev")

# Load the default profile
try:
    manager.load_profile(default_profile)
    print(f"[OK] Loaded default profile: {default_profile}")
except Exception as e:
    print(f"[!] Profile not found, using system defaults: {e}")

# Store preferences for future sessions
config.set("envmanager.default_profile", "dev")
config.set("envmanager.auto_load", True)
config.save()

print("[OK] Configuration saved for next session")
```

**Result:** Default profile loaded automatically, settings persist across sessions

---

## Pattern 2: EnvManager + SynapseLink

**Use Case:** Notify Team Brain when environment changes

**Why:** Keep team informed of environment switches for coordination

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from synapselink import quick_send
from envmanager import EnvManager
import os

manager = EnvManager()

# Load production profile for deployment
profile_name = "production"
manager.load_profile(profile_name)

# Get critical variable values (masked for security)
api_url = os.environ.get("API_URL", "NOT SET")
debug = os.environ.get("DEBUG", "NOT SET")

# Notify team via Synapse
quick_send(
    "FORGE,CLIO,ATLAS",
    f"Environment Switch: {profile_name.upper()}",
    f"EnvManager loaded {profile_name} profile.\n\n"
    f"Environment Status:\n"
    f"- API_URL: {api_url}\n"
    f"- DEBUG: {debug}\n\n"
    f"Ready for deployment operations.",
    priority="HIGH"
)

print(f"[OK] Profile loaded and team notified")
```

**Result:** Team stays informed of environment changes without manual notifications

---

## Pattern 3: EnvManager + TokenTracker

**Use Case:** Track environment operations for audit/logging

**Why:** Understand resource usage patterns and environment changes over time

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from tokentracker import TokenTracker
from envmanager import EnvManager

tracker = TokenTracker()
manager = EnvManager()

# Perform environment operations
profile_name = "dev"
manager.load_profile(profile_name)

# Log the operation (uses 0 tokens since local, but tracks activity)
tracker.log_usage(
    agent="ATLAS",
    model="local",
    input_tokens=0,
    output_tokens=0,
    task=f"EnvManager: Loaded profile '{profile_name}'"
)

# List services
manager.list_services()
tracker.log_usage(
    agent="ATLAS",
    model="local",
    input_tokens=0,
    output_tokens=0,
    task="EnvManager: Listed system services"
)

print("[OK] Operations logged to TokenTracker")
```

**Result:** Complete audit trail of environment management activities

---

## Pattern 4: EnvManager + MemoryBridge

**Use Case:** Persist environment history to Memory Core

**Why:** Maintain long-term record of environment configurations

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/MemoryBridge")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from memorybridge import MemoryBridge
from envmanager import EnvManager
from datetime import datetime
import os

memory = MemoryBridge()
manager = EnvManager()

# Load profile
profile_name = "production"
manager.load_profile(profile_name)

# Record in memory core
history = memory.get("envmanager_history", [])
history.append({
    "timestamp": datetime.now().isoformat(),
    "profile": profile_name,
    "agent": "ATLAS",
    "variables_count": len(manager._load_profiles().get(profile_name, {}).get("env_vars", {})),
    "action": "load"
})

# Keep last 100 entries
memory.set("envmanager_history", history[-100:])
memory.sync()

print(f"[OK] Profile change recorded to Memory Core")
print(f"[OK] History entries: {len(history)}")
```

**Result:** Historical data of environment changes persisted across sessions

---

## Pattern 5: EnvManager + SessionReplay

**Use Case:** Record environment state for debugging sessions

**Why:** Replay environment conditions when issues occur

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SessionReplay")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from sessionreplay import SessionReplay
from envmanager import EnvManager
import os

replay = SessionReplay()
manager = EnvManager()

# Start recording session
session_id = replay.start_session("ATLAS", task="Environment Setup")

# Log initial state
replay.log_input(session_id, "=== Environment State ===")
for key in ["API_URL", "DEBUG", "DATABASE_URL", "LOG_LEVEL"]:
    value = os.environ.get(key, "NOT SET")
    replay.log_input(session_id, f"{key}={value}")

# Load profile
profile_name = "dev"
manager.load_profile(profile_name)
replay.log_output(session_id, f"Loaded profile: {profile_name}")

# Log new state
replay.log_input(session_id, "=== After Profile Load ===")
for key in ["API_URL", "DEBUG", "DATABASE_URL", "LOG_LEVEL"]:
    value = os.environ.get(key, "NOT SET")
    replay.log_output(session_id, f"{key}={value}")

# End session
replay.end_session(session_id, status="COMPLETED")

print(f"[OK] Session recorded: {session_id}")
```

**Result:** Full session replay available for debugging environment issues

---

## Pattern 6: EnvManager + AgentHealth

**Use Case:** Include environment info in health reports

**Why:** Correlate environment state with agent performance

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/AgentHealth")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from agenthealth import AgentHealth
from envmanager import EnvManager
import os

health = AgentHealth()
manager = EnvManager()

# Get environment statistics
profiles = manager._load_profiles()
config = manager._load_config()
last_profile = config.get("last_used", "none")

# Start health monitoring session
health.start_session("ATLAS")

# Log environment metrics
health.log_metric("ATLAS", "envmanager_profiles_count", len(profiles))
health.log_metric("ATLAS", "envmanager_last_profile", last_profile)

# Check if critical variables are set
critical_vars = ["API_URL", "DATABASE_URL", "SECRET_KEY"]
missing = [v for v in critical_vars if not os.environ.get(v)]

if missing:
    health.log_warning("ATLAS", f"Missing critical env vars: {missing}")
else:
    health.log_metric("ATLAS", "envmanager_critical_vars", "all_set")

# Heartbeat
health.heartbeat("ATLAS", status="active")

print(f"[OK] Health metrics logged")
print(f"[OK] Profiles: {len(profiles)}, Last used: {last_profile}")
```

**Result:** Environment state included in agent health monitoring

---

## Pattern 7: EnvManager + TaskQueuePro

**Use Case:** Prepare environment before task execution

**Why:** Ensure correct environment for each task type

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TaskQueuePro")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from taskqueuepro import TaskQueuePro
from envmanager import EnvManager

queue = TaskQueuePro()
manager = EnvManager()

# Get next task from queue
task = queue.get_next_task()

if task:
    # Determine environment based on task type
    if "production" in task.get("tags", []) or "deploy" in task.get("title", "").lower():
        profile = "production"
    elif "test" in task.get("tags", []):
        profile = "testing"
    else:
        profile = "dev"
    
    # Load appropriate environment
    manager.load_profile(profile)
    
    # Mark task in progress
    queue.start_task(task["id"])
    
    print(f"[OK] Loaded {profile} environment for task: {task['title']}")
    
    # ... execute task ...
    
    # Complete task
    queue.complete_task(task["id"], result="Environment setup successful")
else:
    print("[!] No tasks in queue")
```

**Result:** Automatic environment setup based on task requirements

---

## Pattern 8: EnvManager + ContextCompressor

**Use Case:** Compress large environment configurations for sharing

**Why:** Share environment setups efficiently without bloating context

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ContextCompressor")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")

from contextcompressor import ContextCompressor
from envmanager import EnvManager
import json

compressor = ContextCompressor()
manager = EnvManager()

# Get all profiles
profiles = manager._load_profiles()
profile_json = json.dumps(profiles, indent=2)

print(f"Original size: {len(profile_json)} characters")

# Compress for efficient sharing
if len(profile_json) > 500:
    compressed = compressor.compress_text(
        profile_json,
        query="environment profiles summary",
        method="summary"
    )
    
    print(f"Compressed size: {len(compressed.compressed_text)} characters")
    print(f"Savings: {compressed.estimated_token_savings} tokens")
    
    # Share the compressed version
    summary = compressed.compressed_text
else:
    summary = profile_json

print(f"\n[OK] Profile Summary:\n{summary}")
```

**Result:** Efficient sharing of environment configurations

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete deployment workflow using multiple tools

**Why:** Demonstrate real production scenario

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/EnvManager")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SessionReplay")

from envmanager import EnvManager
from synapselink import quick_send
from tokentracker import TokenTracker
from sessionreplay import SessionReplay

# Initialize tools
manager = EnvManager()
tracker = TokenTracker()
replay = SessionReplay()

# Start recording
session_id = replay.start_session("ATLAS", task="Deployment workflow")

try:
    # Step 1: Load production environment
    replay.log_input(session_id, "Loading production environment...")
    manager.load_profile("production")
    replay.log_output(session_id, "Production profile loaded")
    tracker.log_usage("ATLAS", "local", 0, 0, "Loaded production profile")
    
    # Step 2: Verify environment
    replay.log_input(session_id, "Verifying critical variables...")
    import os
    critical = ["API_URL", "DATABASE_URL"]
    for var in critical:
        value = os.environ.get(var, "NOT SET")
        replay.log_output(session_id, f"{var}: {'SET' if value != 'NOT SET' else 'MISSING'}")
    
    # Step 3: Start services
    replay.log_input(session_id, "Starting services...")
    manager.start_service("nginx")
    replay.log_output(session_id, "Services started")
    
    # Step 4: Notify team
    quick_send(
        "FORGE,CLIO",
        "Deployment Complete",
        "Production environment active.\nServices started.\nReady for traffic.",
        priority="NORMAL"
    )
    replay.log_output(session_id, "Team notified via Synapse")
    
    # Success
    replay.end_session(session_id, status="COMPLETED")
    print("[OK] Deployment workflow complete")
    
except Exception as e:
    # Failure handling
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    
    quick_send(
        "FORGE",
        "Deployment FAILED",
        f"Error: {e}\nCheck session replay for details.",
        priority="HIGH"
    )
    
    print(f"[X] Deployment failed: {e}")
```

**Result:** Fully instrumented, coordinated deployment workflow

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation

**Code:**

```python
import sys

# Add all tool paths
tools_path = "C:/Users/logan/OneDrive/Documents/AutoProjects"
sys.path.append(f"{tools_path}/EnvManager")
sys.path.append(f"{tools_path}/ConfigManager")
sys.path.append(f"{tools_path}/SynapseLink")
sys.path.append(f"{tools_path}/TokenTracker")
sys.path.append(f"{tools_path}/AgentHealth")
sys.path.append(f"{tools_path}/SessionReplay")
sys.path.append(f"{tools_path}/MemoryBridge")

from envmanager import EnvManager
from configmanager import ConfigManager
from synapselink import quick_send
from tokentracker import TokenTracker
from agenthealth import AgentHealth
from sessionreplay import SessionReplay
from memorybridge import MemoryBridge
from datetime import datetime

def full_stack_session(agent_name: str, task_description: str):
    """
    Example of running a fully instrumented agent session.
    """
    # Initialize all tools
    env_manager = EnvManager()
    config = ConfigManager()
    tracker = TokenTracker()
    health = AgentHealth()
    replay = SessionReplay()
    memory = MemoryBridge()
    
    # Start session
    session_id = replay.start_session(agent_name, task=task_description)
    health.start_session(agent_name, session_id=session_id)
    
    try:
        # Load environment from config
        default_profile = config.get("envmanager.default_profile", "dev")
        env_manager.load_profile(default_profile)
        replay.log_output(session_id, f"Loaded {default_profile} environment")
        
        # Log environment state
        health.log_metric(agent_name, "environment", default_profile)
        
        # Execute task
        replay.log_input(session_id, f"Executing: {task_description}")
        
        # ... actual task execution here ...
        
        # Record to memory
        memory.set("last_session", {
            "agent": agent_name,
            "task": task_description,
            "environment": default_profile,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        })
        memory.sync()
        
        # Log completion
        tracker.log_usage(agent_name, "local", 0, 0, task_description)
        health.heartbeat(agent_name, status="active")
        
        # End session successfully
        replay.end_session(session_id, status="COMPLETED")
        health.end_session(agent_name, session_id=session_id, status="success")
        
        # Notify if significant
        quick_send(
            "FORGE",
            f"Session Complete: {agent_name}",
            f"Task: {task_description}\nEnvironment: {default_profile}\nStatus: Success",
            priority="NORMAL"
        )
        
        return True
        
    except Exception as e:
        # Error handling
        replay.log_error(session_id, str(e))
        replay.end_session(session_id, status="FAILED")
        health.log_error(agent_name, str(e))
        health.end_session(agent_name, session_id=session_id, status="failed")
        
        quick_send(
            "FORGE,LOGAN",
            f"Session FAILED: {agent_name}",
            f"Task: {task_description}\nError: {e}",
            priority="HIGH"
        )
        
        return False

# Usage
if __name__ == "__main__":
    success = full_stack_session("ATLAS", "Tool build session")
    print(f"Session {'succeeded' if success else 'failed'}")
```

**Result:** Complete Team Brain integration with full instrumentation

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✅ ConfigManager - Load default profiles
2. ✅ SynapseLink - Notify environment changes
3. ✅ SessionReplay - Debug environment issues

**Week 2 (Productivity):**
4. ☐ TokenTracker - Audit trail
5. ☐ MemoryBridge - History persistence
6. ☐ AgentHealth - Health monitoring

**Week 3 (Advanced):**
7. ☐ TaskQueuePro - Task-based env setup
8. ☐ ContextCompressor - Efficient sharing
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
tools_path = Path.home() / "OneDrive/Documents/AutoProjects"
sys.path.append(str(tools_path / "EnvManager"))

# Then import
from envmanager import EnvManager
```

**Profile Not Found:**
```python
# Check available profiles first
from envmanager import EnvManager
manager = EnvManager()
manager.list_profiles()  # Shows all available

# Then load
manager.load_profile("existing_profile")
```

**Permission Issues:**
```python
# Service management may need elevation
# On Linux, prefix with sudo
# On Windows, run terminal as Administrator
```

---

**Last Updated:** January 27, 2026  
**Maintained By:** Team Brain
