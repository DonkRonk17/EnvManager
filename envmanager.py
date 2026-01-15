#!/usr/bin/env python3
"""
EnvManager - Cross-Platform Environment and Service Manager
A comprehensive CLI tool for managing environment variables, services, Docker containers, and processes.

Author: Logan Smith / Metaphy LLC
License: MIT
Version: 1.0.0
"""

import os
import sys
import json
import subprocess
import platform
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class EnvManager:
    """Main EnvManager class for managing environments and services"""
    
    def __init__(self):
        self.system = platform.system()
        self.config_dir = Path.home() / ".envmanager"
        self.config_file = self.config_dir / "config.json"
        self.profiles_file = self.config_dir / "profiles.json"
        self._ensure_config()
        
    def _ensure_config(self):
        """Ensure configuration directory and files exist"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.config_file.write_text(json.dumps({
                "default_profile": None,
                "last_used": None
            }, indent=2))
        if not self.profiles_file.exists():
            self.profiles_file.write_text(json.dumps({}, indent=2))
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        return json.loads(self.config_file.read_text())
    
    def _save_config(self, config: Dict):
        """Save configuration"""
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def _load_profiles(self) -> Dict:
        """Load environment profiles"""
        return json.loads(self.profiles_file.read_text())
    
    def _save_profiles(self, profiles: Dict):
        """Save environment profiles"""
        self.profiles_file.write_text(json.dumps(profiles, indent=2))
    
    # ================== ENVIRONMENT VARIABLE MANAGEMENT ==================
    
    def list_env(self, filter_str: Optional[str] = None):
        """List current environment variables"""
        print("\n[OK] Current Environment Variables:")
        print("-" * 70)
        
        env_vars = sorted(os.environ.items())
        if filter_str:
            env_vars = [(k, v) for k, v in env_vars if filter_str.lower() in k.lower()]
        
        for key, value in env_vars:
            # Truncate long values
            display_value = value if len(value) < 50 else value[:47] + "..."
            print(f"{key:30} = {display_value}")
        
        print(f"\nTotal: {len(env_vars)} variable(s)")
    
    def set_env(self, key: str, value: str, permanent: bool = False):
        """Set environment variable"""
        # Set for current session
        os.environ[key] = value
        
        if permanent:
            if self.system == "Windows":
                self._set_windows_env(key, value)
            else:
                self._set_unix_env(key, value)
            print(f"[OK] Set {key}={value} (permanent)")
        else:
            print(f"[OK] Set {key}={value} (session only)")
    
    def _set_windows_env(self, key: str, value: str):
        """Set permanent Windows environment variable"""
        try:
            subprocess.run(
                ['setx', key, value],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"[X] Failed to set permanent variable: {e}")
    
    def _set_unix_env(self, key: str, value: str):
        """Set permanent Unix environment variable"""
        shell_rc = Path.home() / ".bashrc"
        if (Path.home() / ".zshrc").exists():
            shell_rc = Path.home() / ".zshrc"
        
        export_line = f'\nexport {key}="{value}"  # Added by EnvManager\n'
        
        with open(shell_rc, "a") as f:
            f.write(export_line)
        
        print(f"[OK] Added to {shell_rc} (restart shell or source file)")
    
    def unset_env(self, key: str):
        """Unset environment variable"""
        if key in os.environ:
            del os.environ[key]
            print(f"[OK] Unset {key} (session only)")
        else:
            print(f"[X] Variable {key} not found")
    
    # ================== PROFILE MANAGEMENT ==================
    
    def create_profile(self, name: str, env_vars: Dict[str, str], description: str = ""):
        """Create environment profile"""
        profiles = self._load_profiles()
        
        profiles[name] = {
            "description": description,
            "env_vars": env_vars,
            "created": datetime.now().isoformat(),
            "last_used": None
        }
        
        self._save_profiles(profiles)
        print(f"[OK] Created profile '{name}' with {len(env_vars)} variable(s)")
    
    def list_profiles(self):
        """List all environment profiles"""
        profiles = self._load_profiles()
        
        if not profiles:
            print("\n[X] No profiles found. Create one with 'envmanager profile create'")
            return
        
        print("\n[OK] Environment Profiles:")
        print("-" * 70)
        
        for name, data in sorted(profiles.items()):
            desc = data.get("description", "No description")
            var_count = len(data.get("env_vars", {}))
            last_used = data.get("last_used", "Never")
            if last_used and last_used != "Never":
                last_used = datetime.fromisoformat(last_used).strftime("%Y-%m-%d %H:%M")
            
            print(f"\n  {name}")
            print(f"    Description: {desc}")
            print(f"    Variables: {var_count}")
            print(f"    Last Used: {last_used}")
    
    def load_profile(self, name: str):
        """Load environment profile"""
        profiles = self._load_profiles()
        
        if name not in profiles:
            print(f"[X] Profile '{name}' not found")
            return
        
        profile = profiles[name]
        for key, value in profile["env_vars"].items():
            os.environ[key] = value
        
        # Update last used
        profile["last_used"] = datetime.now().isoformat()
        self._save_profiles(profiles)
        
        config = self._load_config()
        config["last_used"] = name
        self._save_config(config)
        
        print(f"[OK] Loaded profile '{name}' ({len(profile['env_vars'])} variables)")
    
    def delete_profile(self, name: str):
        """Delete environment profile"""
        profiles = self._load_profiles()
        
        if name not in profiles:
            print(f"[X] Profile '{name}' not found")
            return
        
        del profiles[name]
        self._save_profiles(profiles)
        print(f"[OK] Deleted profile '{name}'")
    
    # ================== SERVICE MANAGEMENT ==================
    
    def list_services(self):
        """List system services"""
        print("\n[OK] System Services:")
        print("-" * 70)
        
        if self.system == "Windows":
            self._list_windows_services()
        elif self.system == "Linux":
            self._list_systemd_services()
        elif self.system == "Darwin":
            self._list_launchd_services()
        else:
            print(f"[X] Service management not supported on {self.system}")
    
    def _list_windows_services(self):
        """List Windows services"""
        try:
            result = subprocess.run(
                ['sc', 'query', 'state=', 'all'],
                capture_output=True,
                text=True,
                check=True
            )
            
            services = []
            current_service = {}
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line.startswith('SERVICE_NAME:'):
                    if current_service:
                        services.append(current_service)
                    current_service = {'name': line.split(':', 1)[1].strip()}
                elif line.startswith('STATE'):
                    state = line.split(':', 1)[1].strip().split()[0]
                    current_service['state'] = state
            
            if current_service:
                services.append(current_service)
            
            # Show first 20 services
            for svc in services[:20]:
                status = "[OK]" if "RUNNING" in svc.get('state', '') else "[ ]"
                print(f"  {status} {svc.get('name', 'Unknown'):<40} {svc.get('state', 'Unknown')}")
            
            print(f"\nShowing 20 of {len(services)} total services")
            
        except Exception as e:
            print(f"[X] Failed to list services: {e}")
    
    def _list_systemd_services(self):
        """List systemd services (Linux)"""
        try:
            result = subprocess.run(
                ['systemctl', 'list-units', '--type=service', '--no-pager', '--no-legend'],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')
            for line in lines[:20]:  # Show first 20
                parts = line.split(None, 4)
                if len(parts) >= 4:
                    name = parts[0]
                    status = "[OK]" if parts[2] == "active" else "[ ]"
                    state = parts[3]
                    print(f"  {status} {name:<40} {state}")
            
            print(f"\nShowing 20 of {len(lines)} total services")
            
        except Exception as e:
            print(f"[X] Failed to list services: {e}")
    
    def _list_launchd_services(self):
        """List launchd services (macOS)"""
        try:
            result = subprocess.run(
                ['launchctl', 'list'],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines[:20]:  # Show first 20
                parts = line.split(None, 2)
                if len(parts) >= 3:
                    pid = parts[0]
                    status = "[OK]" if pid != "-" else "[ ]"
                    name = parts[2]
                    print(f"  {status} {name:<50} PID: {pid}")
            
            print(f"\nShowing 20 of {len(lines)} total services")
            
        except Exception as e:
            print(f"[X] Failed to list services: {e}")
    
    def start_service(self, name: str):
        """Start a service"""
        if self.system == "Windows":
            cmd = ['sc', 'start', name]
        elif self.system == "Linux":
            cmd = ['systemctl', 'start', name]
        elif self.system == "Darwin":
            cmd = ['launchctl', 'start', name]
        else:
            print(f"[X] Service management not supported on {self.system}")
            return
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[OK] Started service '{name}'")
        except subprocess.CalledProcessError as e:
            print(f"[X] Failed to start service: {e}")
    
    def stop_service(self, name: str):
        """Stop a service"""
        if self.system == "Windows":
            cmd = ['sc', 'stop', name]
        elif self.system == "Linux":
            cmd = ['systemctl', 'stop', name]
        elif self.system == "Darwin":
            cmd = ['launchctl', 'stop', name]
        else:
            print(f"[X] Service management not supported on {self.system}")
            return
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[OK] Stopped service '{name}'")
        except subprocess.CalledProcessError as e:
            print(f"[X] Failed to stop service: {e}")
    
    # ================== DOCKER MANAGEMENT ==================
    
    def list_containers(self, all_containers: bool = False):
        """List Docker containers"""
        print("\n[OK] Docker Containers:")
        print("-" * 70)
        
        try:
            cmd = ['docker', 'ps']
            if all_containers:
                cmd.append('-a')
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            
        except FileNotFoundError:
            print("[X] Docker not installed or not in PATH")
        except subprocess.CalledProcessError as e:
            print(f"[X] Failed to list containers: {e}")
    
    def start_container(self, name: str):
        """Start Docker container"""
        try:
            subprocess.run(['docker', 'start', name], check=True, capture_output=True)
            print(f"[OK] Started container '{name}'")
        except subprocess.CalledProcessError as e:
            print(f"[X] Failed to start container: {e}")
    
    def stop_container(self, name: str):
        """Stop Docker container"""
        try:
            subprocess.run(['docker', 'stop', name], check=True, capture_output=True)
            print(f"[OK] Stopped container '{name}'")
        except subprocess.CalledProcessError as e:
            print(f"[X] Failed to stop container: {e}")

# ================== CLI INTERFACE ==================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="EnvManager - Cross-Platform Environment and Service Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  envmanager env list                          # List environment variables
  envmanager env set API_KEY abc123 --permanent # Set permanent env var
  envmanager profile create dev '{"PATH": "/usr/local/bin"}' # Create profile
  envmanager profile load dev                  # Load profile
  envmanager service list                      # List system services
  envmanager docker list --all                 # List all containers
  
For more information, visit: https://github.com/DonkRonk17/EnvManager
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Environment commands
    env_parser = subparsers.add_parser('env', help='Environment variable management')
    env_sub = env_parser.add_subparsers(dest='subcommand')
    
    env_list = env_sub.add_parser('list', help='List environment variables')
    env_list.add_argument('--filter', help='Filter by variable name')
    
    env_set = env_sub.add_parser('set', help='Set environment variable')
    env_set.add_argument('key', help='Variable name')
    env_set.add_argument('value', help='Variable value')
    env_set.add_argument('--permanent', action='store_true', help='Make change permanent')
    
    env_unset = env_sub.add_parser('unset', help='Unset environment variable')
    env_unset.add_argument('key', help='Variable name')
    
    # Profile commands
    profile_parser = subparsers.add_parser('profile', help='Profile management')
    profile_sub = profile_parser.add_subparsers(dest='subcommand')
    
    profile_list = profile_sub.add_parser('list', help='List profiles')
    
    profile_create = profile_sub.add_parser('create', help='Create profile')
    profile_create.add_argument('name', help='Profile name')
    profile_create.add_argument('env_vars', help='Environment variables (JSON format)')
    profile_create.add_argument('--description', default='', help='Profile description')
    
    profile_load = profile_sub.add_parser('load', help='Load profile')
    profile_load.add_argument('name', help='Profile name')
    
    profile_delete = profile_sub.add_parser('delete', help='Delete profile')
    profile_delete.add_argument('name', help='Profile name')
    
    # Service commands
    service_parser = subparsers.add_parser('service', help='Service management')
    service_sub = service_parser.add_subparsers(dest='subcommand')
    
    service_list = service_sub.add_parser('list', help='List services')
    
    service_start = service_sub.add_parser('start', help='Start service')
    service_start.add_argument('name', help='Service name')
    
    service_stop = service_sub.add_parser('stop', help='Stop service')
    service_stop.add_argument('name', help='Service name')
    
    # Docker commands
    docker_parser = subparsers.add_parser('docker', help='Docker container management')
    docker_sub = docker_parser.add_subparsers(dest='subcommand')
    
    docker_list = docker_sub.add_parser('list', help='List containers')
    docker_list.add_argument('--all', action='store_true', help='Show all containers')
    
    docker_start = docker_sub.add_parser('start', help='Start container')
    docker_start.add_argument('name', help='Container name or ID')
    
    docker_stop = docker_sub.add_parser('stop', help='Stop container')
    docker_stop.add_argument('name', help='Container name or ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = EnvManager()
    
    try:
        if args.command == 'env':
            if args.subcommand == 'list':
                manager.list_env(args.filter)
            elif args.subcommand == 'set':
                manager.set_env(args.key, args.value, args.permanent)
            elif args.subcommand == 'unset':
                manager.unset_env(args.key)
                
        elif args.command == 'profile':
            if args.subcommand == 'list':
                manager.list_profiles()
            elif args.subcommand == 'create':
                env_vars = json.loads(args.env_vars)
                manager.create_profile(args.name, env_vars, args.description)
            elif args.subcommand == 'load':
                manager.load_profile(args.name)
            elif args.subcommand == 'delete':
                manager.delete_profile(args.name)
                
        elif args.command == 'service':
            if args.subcommand == 'list':
                manager.list_services()
            elif args.subcommand == 'start':
                manager.start_service(args.name)
            elif args.subcommand == 'stop':
                manager.stop_service(args.name)
                
        elif args.command == 'docker':
            if args.subcommand == 'list':
                manager.list_containers(args.all)
            elif args.subcommand == 'start':
                manager.start_container(args.name)
            elif args.subcommand == 'stop':
                manager.stop_container(args.name)
                
    except KeyboardInterrupt:
        print("\n\n[X] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[X] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
