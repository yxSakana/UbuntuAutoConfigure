# -*- coding: utf-8 -*-
"""
Custom script installer for packages with custom installation logic
"""

import os
from typing import TYPE_CHECKING

from .base import BaseInstaller, InstallResult, InstallStatus

if TYPE_CHECKING:
    from ..config import PackageConfig


class CustomScriptInstaller(BaseInstaller):
    """Installer for packages with custom shell scripts"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package using custom script"""
        
        # Check if already installed
        if config.verify_command and self.check_installed(config.verify_command):
            current_version = self.get_version(config.verify_command)
            return self.create_install_result(
                InstallStatus.ALREADY_INSTALLED,
                f"{config.display_name} is already installed",
                current_version
            )
        
        # Check architecture support
        current_arch = self.get_architecture()
        if current_arch not in config.supported_architectures:
            return self.create_install_result(
                InstallStatus.SKIPPED,
                f"Package not supported on {current_arch} architecture"
            )
        
        if not config.custom_script_path:
            return self.create_install_result(
                InstallStatus.FAILED,
                "Custom script path not specified"
            )
        
        # Check if script file exists
        script_path = config.custom_script_path
        if not os.path.isabs(script_path):
            # Relative path, resolve from script directory
            script_path = os.path.join("script", script_path)
        
        if not os.path.exists(script_path):
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Custom script not found: {script_path}"
            )
        
        try:
            # Install dependencies first
            if config.dependencies:
                if not self.install_dependencies(config.dependencies):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Failed to install dependencies"
                    )
            
            # Execute the custom script
            self.logger.info(f"Executing custom script: {script_path}")
            
            # Make sure script is executable
            os.chmod(script_path, 0o755)
            
            # Run the script
            result = self.run_command(f"bash '{script_path}'", cwd=os.getcwd())
            
            if result.returncode != 0:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    f"Custom script failed: {result.stderr}",
                    logs=[result.stdout, result.stderr]
                )
            
            # Run post-install commands
            if not self.run_post_install_commands(config.post_install_commands):
                self.logger.warning("Some post-install commands failed")
            
            # Verify installation
            installed_version = None
            if config.verify_command:
                if not self.check_installed(config.verify_command):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Installation verification failed",
                        logs=[result.stdout, result.stderr]
                    )
                
                installed_version = self.get_version(config.verify_command)
            
            return self.create_install_result(
                InstallStatus.SUCCESS,
                f"{config.display_name} installed successfully via custom script",
                installed_version,
                [result.stdout]
            )
            
        except Exception as e:
            self.logger.error(f"Error installing {config.name} via custom script: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Custom script installation failed: {str(e)}"
            )
