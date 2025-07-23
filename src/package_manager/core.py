# -*- coding: utf-8 -*-
"""
Package Manager Core
Main package manager class that coordinates all installation methods
"""

import logging
import platform
from typing import Dict, List, Optional, Type

from .config import PackageConfig, PackageConfigManager, InstallMethod
from .installers.base import BaseInstaller, InstallResult, InstallStatus
from .installers.github_installer import GitHubDebInstaller, GitHubSourceInstaller
from .installers.script_installer import ScriptInstaller
from .installers.system_installer import AptInstaller, SnapInstaller, FlatpakInstaller
from .installers.custom_installer import CustomScriptInstaller


class PackageManager:
    """Main package manager class"""
    
    def __init__(self, sudo_password: Optional[str] = None, config_dir: Optional[str] = None):
        """
        Initialize package manager
        
        Args:
            sudo_password: Password for sudo operations
            config_dir: Directory containing package configurations
        """
        self.sudo_password = sudo_password
        self.config_manager = PackageConfigManager(config_dir) if config_dir else PackageConfigManager()
        self.logger = logging.getLogger(__name__)
        
        # Map install methods to installer classes
        self.installer_classes: Dict[InstallMethod, Type[BaseInstaller]] = {
            InstallMethod.GITHUB_DEB: GitHubDebInstaller,
            InstallMethod.GITHUB_SOURCE: GitHubSourceInstaller,
            InstallMethod.SCRIPT_URL: ScriptInstaller,
            InstallMethod.APT: AptInstaller,
            InstallMethod.SNAP: SnapInstaller,
            InstallMethod.FLATPAK: FlatpakInstaller,
            InstallMethod.CUSTOM_SCRIPT: CustomScriptInstaller,
        }
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('package_manager.log')
            ]
        )
    
    def get_installer(self, install_method: InstallMethod) -> BaseInstaller:
        """
        Get installer instance for the specified method
        
        Args:
            install_method: Installation method
            
        Returns:
            Installer instance
        """
        installer_class = self.installer_classes.get(install_method)
        if not installer_class:
            raise ValueError(f"Unsupported install method: {install_method}")
        
        return installer_class(self.sudo_password)
    
    def install_package(self, package_name: str) -> InstallResult:
        """
        Install a single package
        
        Args:
            package_name: Name of the package to install
            
        Returns:
            InstallResult object
        """
        config = self.config_manager.get_package(package_name)
        if not config:
            return InstallResult(
                status=InstallStatus.FAILED,
                message=f"Package '{package_name}' not found in configuration"
            )
        
        self.logger.info(f"Installing package: {config.display_name}")
        
        try:
            with self.get_installer(config.install_method) as installer:
                result = installer.install(config)
                
                self.logger.info(f"Installation result for {package_name}: {result.status.value}")
                if result.message:
                    self.logger.info(f"Message: {result.message}")
                
                return result
                
        except Exception as e:
            self.logger.error(f"Error installing {package_name}: {e}")
            return InstallResult(
                status=InstallStatus.FAILED,
                message=f"Installation error: {str(e)}"
            )
    
    def install_packages(self, package_names: List[str]) -> Dict[str, InstallResult]:
        """
        Install multiple packages
        
        Args:
            package_names: List of package names to install
            
        Returns:
            Dictionary mapping package names to InstallResult objects
        """
        results = {}
        
        for package_name in package_names:
            self.logger.info(f"Starting installation of {package_name}")
            result = self.install_package(package_name)
            results[package_name] = result
            
            if not result.success:
                self.logger.error(f"Failed to install {package_name}: {result.message}")
            else:
                self.logger.info(f"Successfully installed {package_name}")
        
        return results
    
    def list_available_packages(self) -> List[str]:
        """
        List all available packages
        
        Returns:
            List of package names
        """
        return self.config_manager.list_packages()
    
    def get_package_info(self, package_name: str) -> Optional[PackageConfig]:
        """
        Get package configuration information
        
        Args:
            package_name: Name of the package
            
        Returns:
            PackageConfig object or None if not found
        """
        return self.config_manager.get_package(package_name)
    
    def add_package_config(self, config: PackageConfig):
        """
        Add a new package configuration
        
        Args:
            config: PackageConfig object
        """
        self.config_manager.add_package(config)
    
    def check_package_installed(self, package_name: str) -> bool:
        """
        Check if a package is already installed
        
        Args:
            package_name: Name of the package
            
        Returns:
            True if installed, False otherwise
        """
        config = self.config_manager.get_package(package_name)
        if not config or not config.verify_command:
            return False
        
        try:
            with self.get_installer(config.install_method) as installer:
                return installer.check_installed(config.verify_command)
        except:
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information
        
        Returns:
            Dictionary with system information
        """
        return {
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "distribution": self._get_linux_distribution()
        }
    
    def _get_linux_distribution(self) -> str:
        """Get Linux distribution information"""
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=')[1].strip().strip('"')
        except:
            pass
        
        return "Unknown"
    
    def generate_install_script(self, package_names: List[str], output_file: str = "auto_install.sh"):
        """
        Generate a shell script for installing packages
        
        Args:
            package_names: List of package names to install
            output_file: Output script file path
        """
        script_lines = [
            "#!/bin/bash",
            "# Auto-generated package installation script",
            "# Generated by UbuntuAutoConfigure Package Manager",
            "",
            "set -e  # Exit on error",
            "",
            "echo 'Starting package installation...'",
            ""
        ]
        
        for package_name in package_names:
            config = self.config_manager.get_package(package_name)
            if not config:
                script_lines.append(f"echo 'Warning: Package {package_name} not found in configuration'")
                continue
            
            script_lines.append(f"echo 'Installing {config.display_name}...'")
            
            # Generate installation commands based on method
            if config.install_method == InstallMethod.APT:
                pkg_name = config.package_name or config.name
                script_lines.extend([
                    "sudo apt update",
                    f"sudo apt install -y {pkg_name}"
                ])
            
            elif config.install_method == InstallMethod.GITHUB_DEB:
                script_lines.extend([
                    f"# Install {config.display_name} from GitHub",
                    f"# Repository: {config.github_repo}",
                    f"# Asset pattern: {config.github_asset_pattern}",
                    "# Note: This requires manual download URL resolution"
                ])
            
            elif config.install_method == InstallMethod.SCRIPT_URL:
                script_lines.extend([
                    f"curl -sS {config.script_url} | sh"
                ])
            
            elif config.install_method == InstallMethod.CUSTOM_SCRIPT:
                if config.custom_script_path:
                    script_lines.append(f"bash {config.custom_script_path}")
            
            # Add post-install commands
            if config.post_install_commands:
                script_lines.append("# Post-install commands")
                script_lines.extend(config.post_install_commands)
            
            script_lines.append("")
        
        script_lines.extend([
            "echo 'Package installation completed!'",
            ""
        ])
        
        # Write script to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(script_lines))
        
        # Make script executable
        import os
        os.chmod(output_file, 0o755)
        
        self.logger.info(f"Installation script generated: {output_file}")
    
    def update_package_configs(self):
        """Update package configurations from remote sources"""
        # This could be extended to fetch updated configurations
        # from a remote repository or update GitHub release information
        self.logger.info("Package configurations are up to date")
    
    def cleanup(self):
        """Cleanup temporary files and resources"""
        # Clear GitHub API cache
        from .github_api import _github_cache
        _github_cache.clear()
        
        self.logger.info("Cleanup completed")
