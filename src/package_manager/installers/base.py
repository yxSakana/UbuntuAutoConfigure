# -*- coding: utf-8 -*-
"""
Base installer class and common utilities
"""

import subprocess
import os
import tempfile
import shutil
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from ..config import PackageConfig


class InstallStatus(Enum):
    """Installation status"""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    ALREADY_INSTALLED = "already_installed"


@dataclass
class InstallResult:
    """Result of an installation attempt"""
    status: InstallStatus
    message: str
    version: Optional[str] = None
    logs: List[str] = None
    
    def __post_init__(self):
        if self.logs is None:
            self.logs = []
    
    @property
    def success(self) -> bool:
        return self.status in [InstallStatus.SUCCESS, InstallStatus.ALREADY_INSTALLED]


class BaseInstaller(ABC):
    """Base class for all installers"""
    
    def __init__(self, sudo_password: Optional[str] = None):
        self.sudo_password = sudo_password
        self.logger = logging.getLogger(self.__class__.__name__)
        self.temp_dir = None
    
    def __enter__(self):
        """Context manager entry"""
        self.temp_dir = tempfile.mkdtemp(prefix="pkg_installer_")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup temp directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @abstractmethod
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install a package based on its configuration"""
        pass
    
    def run_command(self, command: str, cwd: Optional[str] = None, 
                   input_text: Optional[str] = None, 
                   timeout: int = 300) -> subprocess.CompletedProcess:
        """
        Run a shell command with proper error handling
        
        Args:
            command: Command to run
            cwd: Working directory
            input_text: Input to send to the command
            timeout: Command timeout in seconds
            
        Returns:
            CompletedProcess object
        """
        self.logger.info(f"Running command: {command}")
        
        # Replace password placeholder if needed
        if self.sudo_password and "%{PWD}" in command:
            command = command.replace("%{PWD}", self.sudo_password)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.temp_dir,
                input=input_text,
                text=True,
                capture_output=True,
                timeout=timeout
            )
            
            if result.stdout:
                self.logger.debug(f"STDOUT: {result.stdout}")
            if result.stderr:
                self.logger.debug(f"STDERR: {result.stderr}")
            
            return result
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Command timed out: {command}")
            raise
        except Exception as e:
            self.logger.error(f"Error running command '{command}': {e}")
            raise
    
    def download_file(self, url: str, filename: Optional[str] = None) -> str:
        """
        Download a file to the temp directory
        
        Args:
            url: URL to download
            filename: Optional filename, will be extracted from URL if not provided
            
        Returns:
            Path to downloaded file
        """
        if not filename:
            filename = os.path.basename(url.split('?')[0])  # Remove query parameters
        
        filepath = os.path.join(self.temp_dir, filename)
        
        self.logger.info(f"Downloading {url} to {filepath}")
        
        # Use wget for downloading with progress
        result = self.run_command(f"wget -O '{filepath}' '{url}'")
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to download {url}: {result.stderr}")
        
        return filepath
    
    def check_installed(self, command: str) -> bool:
        """
        Check if a package is already installed by running a command
        
        Args:
            command: Command to check (e.g., "bat --version")
            
        Returns:
            True if command succeeds, False otherwise
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def get_version(self, command: str) -> Optional[str]:
        """
        Get version string from a command
        
        Args:
            command: Command to run (e.g., "bat --version")
            
        Returns:
            Version string or None if failed
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def install_dependencies(self, dependencies: List[str]) -> bool:
        """
        Install system dependencies using apt
        
        Args:
            dependencies: List of package names
            
        Returns:
            True if successful, False otherwise
        """
        if not dependencies:
            return True
        
        self.logger.info(f"Installing dependencies: {dependencies}")
        
        # Update package list first
        result = self.run_command("sudo apt update")
        if result.returncode != 0:
            self.logger.warning("Failed to update package list")
        
        # Install dependencies
        deps_str = " ".join(dependencies)
        command = f"sudo apt install -y {deps_str}"
        
        if self.sudo_password:
            command = f"echo '{self.sudo_password}' | sudo -S apt install -y {deps_str}"
        
        result = self.run_command(command)
        
        if result.returncode != 0:
            self.logger.error(f"Failed to install dependencies: {result.stderr}")
            return False
        
        return True
    
    def run_post_install_commands(self, commands: List[str]) -> bool:
        """
        Run post-installation commands
        
        Args:
            commands: List of commands to run
            
        Returns:
            True if all commands succeeded, False otherwise
        """
        if not commands:
            return True
        
        self.logger.info("Running post-install commands")
        
        for command in commands:
            result = self.run_command(command)
            if result.returncode != 0:
                self.logger.error(f"Post-install command failed: {command}")
                self.logger.error(f"Error: {result.stderr}")
                return False
        
        return True
    
    def get_architecture(self) -> str:
        """Get system architecture"""
        result = subprocess.run(
            "uname -m",
            shell=True,
            capture_output=True,
            text=True
        )
        
        arch = result.stdout.strip()
        
        # Normalize architecture names
        arch_map = {
            "x86_64": "x86_64",
            "amd64": "x86_64", 
            "aarch64": "aarch64",
            "arm64": "aarch64"
        }
        
        return arch_map.get(arch, arch)
    
    def create_install_result(self, status: InstallStatus, message: str, 
                            version: Optional[str] = None, 
                            logs: Optional[List[str]] = None) -> InstallResult:
        """Helper to create InstallResult"""
        return InstallResult(
            status=status,
            message=message,
            version=version,
            logs=logs or []
        )
