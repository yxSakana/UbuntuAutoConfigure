# -*- coding: utf-8 -*-
"""
Package Configuration System
Defines package installation configurations and methods
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
import json
import os


class InstallMethod(Enum):
    """Installation methods supported by the package manager"""
    GITHUB_DEB = "github_deb"          # Download deb package from GitHub releases
    GITHUB_SOURCE = "github_source"    # Clone and build from GitHub source
    SCRIPT_URL = "script_url"          # Download and execute installation script
    APT = "apt"                        # Use apt package manager
    SNAP = "snap"                      # Use snap package manager
    FLATPAK = "flatpak"               # Use flatpak package manager
    CUSTOM_SCRIPT = "custom_script"    # Execute custom shell script


@dataclass
class PackageConfig:
    """Configuration for a single package"""
    name: str
    display_name: str
    description: str = ""
    install_method: InstallMethod = InstallMethod.APT
    
    # GitHub specific
    github_repo: Optional[str] = None  # e.g., "sharkdp/bat"
    github_asset_pattern: Optional[str] = None  # e.g., "*amd64.deb"
    
    # APT/Snap/Flatpak specific
    package_name: Optional[str] = None
    
    # Script specific
    script_url: Optional[str] = None
    script_inputs: List[str] = field(default_factory=list)  # Automated inputs for interactive scripts
    
    # Source build specific
    build_commands: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    # Custom script specific
    custom_script_path: Optional[str] = None
    
    # General options
    requires_sudo: bool = True
    post_install_commands: List[str] = field(default_factory=list)
    verify_command: Optional[str] = None  # Command to verify installation
    
    # Architecture support
    supported_architectures: List[str] = field(default_factory=lambda: ["x86_64", "aarch64"])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "install_method": self.install_method.value,
            "github_repo": self.github_repo,
            "github_asset_pattern": self.github_asset_pattern,
            "package_name": self.package_name,
            "script_url": self.script_url,
            "script_inputs": self.script_inputs,
            "build_commands": self.build_commands,
            "dependencies": self.dependencies,
            "custom_script_path": self.custom_script_path,
            "requires_sudo": self.requires_sudo,
            "post_install_commands": self.post_install_commands,
            "verify_command": self.verify_command,
            "supported_architectures": self.supported_architectures
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PackageConfig':
        """Create from dictionary"""
        data = data.copy()
        data["install_method"] = InstallMethod(data["install_method"])
        return cls(**data)


class PackageConfigManager:
    """Manages package configurations"""
    
    def __init__(self, config_dir: str = "src/package_manager/configs"):
        self.config_dir = config_dir
        self.packages: Dict[str, PackageConfig] = {}
        self._load_default_configs()
    
    def _load_default_configs(self):
        """Load default package configurations"""
        # Create default configurations for common tools
        self._create_default_configs()
        
        # Load from config files if they exist
        if os.path.exists(self.config_dir):
            for filename in os.listdir(self.config_dir):
                if filename.endswith('.json'):
                    self._load_config_file(os.path.join(self.config_dir, filename))
    
    def _create_default_configs(self):
        """Create default configurations for popular tools"""
        default_configs = [
            PackageConfig(
                name="bat",
                display_name="bat (cat clone)",
                description="A cat clone with syntax highlighting and Git integration",
                install_method=InstallMethod.GITHUB_DEB,
                github_repo="sharkdp/bat",
                github_asset_pattern="*amd64.deb",
                verify_command="bat --version"
            ),
            PackageConfig(
                name="starship",
                display_name="Starship Prompt",
                description="Cross-shell prompt for astronauts",
                install_method=InstallMethod.SCRIPT_URL,
                script_url="https://starship.rs/install.sh",
                script_inputs=["y"],  # Auto-confirm installation
                post_install_commands=['echo \'eval "$(starship init bash)"\' >> ~/.bashrc'],
                verify_command="starship --version"
            ),
            PackageConfig(
                name="golang",
                display_name="Go Programming Language",
                description="Go programming language compiler and tools",
                install_method=InstallMethod.GITHUB_SOURCE,
                github_repo="golang/go",
                github_asset_pattern="go*.linux-amd64.tar.gz",
                build_commands=[
                    "wget -O /tmp/go.tar.gz {download_url}",
                    "sudo tar -xzf /tmp/go.tar.gz -C /usr/local",
                    "echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc"
                ],
                verify_command="go version"
            ),
            PackageConfig(
                name="neovim",
                display_name="Neovim",
                description="Hyperextensible Vim-based text editor",
                install_method=InstallMethod.GITHUB_SOURCE,
                github_repo="neovim/neovim",
                dependencies=["build-essential", "cmake", "gettext"],
                build_commands=[
                    "git clone --depth 1 https://github.com/neovim/neovim.git /tmp/neovim",
                    "cd /tmp/neovim && make CMAKE_BUILD_TYPE=Release",
                    "cd /tmp/neovim && sudo make install"
                ],
                verify_command="nvim --version"
            ),
            PackageConfig(
                name="btop",
                display_name="btop++",
                description="Resource monitor that shows usage and stats",
                install_method=InstallMethod.GITHUB_DEB,
                github_repo="aristocratos/btop",
                github_asset_pattern="*x86_64.deb",
                verify_command="btop --version"
            ),
            PackageConfig(
                name="lsd",
                display_name="LSDeluxe",
                description="Next gen ls command with colors and icons",
                install_method=InstallMethod.GITHUB_DEB,
                github_repo="lsd-rs/lsd",
                github_asset_pattern="*amd64.deb",
                verify_command="lsd --version"
            )
        ]
        
        for config in default_configs:
            self.packages[config.name] = config
    
    def _load_config_file(self, filepath: str):
        """Load configuration from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        config = PackageConfig.from_dict(item)
                        self.packages[config.name] = config
                else:
                    config = PackageConfig.from_dict(data)
                    self.packages[config.name] = config
        except Exception as e:
            print(f"Error loading config file {filepath}: {e}")
    
    def get_package(self, name: str) -> Optional[PackageConfig]:
        """Get package configuration by name"""
        return self.packages.get(name)
    
    def list_packages(self) -> List[str]:
        """List all available package names"""
        return list(self.packages.keys())
    
    def add_package(self, config: PackageConfig):
        """Add a new package configuration"""
        self.packages[config.name] = config
    
    def save_config(self, name: str, filepath: str):
        """Save package configuration to file"""
        config = self.packages.get(name)
        if config:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
    
    def save_all_configs(self):
        """Save all configurations to files"""
        os.makedirs(self.config_dir, exist_ok=True)
        for name, config in self.packages.items():
            filepath = os.path.join(self.config_dir, f"{name}.json")
            self.save_config(name, filepath)
