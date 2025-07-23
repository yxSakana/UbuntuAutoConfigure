# -*- coding: utf-8 -*-
"""
Script-based installer for packages that provide installation scripts
"""

import os
import stat
from typing import TYPE_CHECKING

from .base import BaseInstaller, InstallResult, InstallStatus

if TYPE_CHECKING:
    from ..config import PackageConfig


class ScriptInstaller(BaseInstaller):
    """Installer for packages that provide installation scripts"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package using installation script"""
        
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
        
        if not config.script_url:
            return self.create_install_result(
                InstallStatus.FAILED,
                "Script URL not specified"
            )
        
        try:
            # Install dependencies first
            if config.dependencies:
                if not self.install_dependencies(config.dependencies):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Failed to install dependencies"
                    )
            
            # Download the installation script
            script_file = self.download_file(config.script_url, "install_script.sh")
            
            # Make script executable
            os.chmod(script_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
            
            # Prepare input for interactive script
            script_input = None
            if config.script_inputs:
                script_input = "\n".join(config.script_inputs) + "\n"
            
            # Execute the installation script
            self.logger.info(f"Executing installation script: {script_file}")
            
            # Some scripts need to be run with bash explicitly
            command = f"bash '{script_file}'"
            
            result = self.run_command(
                command,
                input_text=script_input,
                timeout=600  # 10 minutes timeout for scripts
            )
            
            if result.returncode != 0:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    f"Installation script failed: {result.stderr}",
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
                f"{config.display_name} installed successfully via script",
                installed_version,
                [result.stdout]
            )
            
        except Exception as e:
            self.logger.error(f"Error installing {config.name} via script: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Script installation failed: {str(e)}"
            )
