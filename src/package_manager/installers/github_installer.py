# -*- coding: utf-8 -*-
"""
GitHub-based installers for deb packages and source builds
"""

import os
import re
from typing import TYPE_CHECKING

from .base import BaseInstaller, InstallResult, InstallStatus
from ..github_api import get_cached_github_api

if TYPE_CHECKING:
    from ..config import PackageConfig


class GitHubDebInstaller(BaseInstaller):
    """Installer for GitHub deb packages"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package from GitHub deb release"""
        
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
        
        if not config.github_repo or not config.github_asset_pattern:
            return self.create_install_result(
                InstallStatus.FAILED,
                "GitHub repository or asset pattern not specified"
            )
        
        try:
            # Get GitHub API client
            github_api = get_cached_github_api()
            
            # Get download URL for the latest release
            result = github_api.get_download_url(
                config.github_repo,
                config.github_asset_pattern
            )
            
            if not result:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    f"No matching asset found for pattern: {config.github_asset_pattern}"
                )
            
            download_url, version = result
            
            # Download the deb package
            deb_file = self.download_file(download_url)
            
            # Install dependencies if specified
            if config.dependencies:
                if not self.install_dependencies(config.dependencies):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Failed to install dependencies"
                    )
            
            # Install the deb package
            install_command = f"sudo dpkg -i '{deb_file}'"
            if self.sudo_password:
                install_command = f"echo '{self.sudo_password}' | sudo -S dpkg -i '{deb_file}'"
            
            result = self.run_command(install_command)
            
            if result.returncode != 0:
                # Try to fix broken dependencies
                self.logger.info("Attempting to fix broken dependencies")
                fix_command = "sudo apt-get install -f -y"
                if self.sudo_password:
                    fix_command = f"echo '{self.sudo_password}' | sudo -S apt-get install -f -y"
                
                fix_result = self.run_command(fix_command)
                if fix_result.returncode != 0:
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        f"Failed to install deb package: {result.stderr}"
                    )
            
            # Run post-install commands
            if not self.run_post_install_commands(config.post_install_commands):
                self.logger.warning("Some post-install commands failed")
            
            # Verify installation
            if config.verify_command:
                if not self.check_installed(config.verify_command):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Installation verification failed"
                    )
                
                installed_version = self.get_version(config.verify_command)
            else:
                installed_version = version
            
            return self.create_install_result(
                InstallStatus.SUCCESS,
                f"{config.display_name} installed successfully",
                installed_version
            )
            
        except Exception as e:
            self.logger.error(f"Error installing {config.name}: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Installation failed: {str(e)}"
            )


class GitHubSourceInstaller(BaseInstaller):
    """Installer for GitHub source builds"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package from GitHub source"""
        
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
        
        if not config.github_repo:
            return self.create_install_result(
                InstallStatus.FAILED,
                "GitHub repository not specified"
            )
        
        try:
            # Install dependencies first
            if config.dependencies:
                if not self.install_dependencies(config.dependencies):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Failed to install dependencies"
                    )
            
            # Get GitHub API client for version info
            github_api = get_cached_github_api()
            release = github_api.get_latest_release(config.github_repo)
            version = release.version if release else "unknown"
            
            # Execute build commands
            if not config.build_commands:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    "No build commands specified"
                )
            
            logs = []
            
            for command in config.build_commands:
                # Replace placeholders in command
                if release and config.github_asset_pattern:
                    asset = github_api.find_asset_by_pattern(release, config.github_asset_pattern)
                    if asset:
                        command = command.replace("{download_url}", asset["browser_download_url"])
                
                # Replace other placeholders
                command = command.replace("{version}", version)
                command = command.replace("{repo}", config.github_repo)
                
                self.logger.info(f"Executing build command: {command}")
                result = self.run_command(command)
                
                logs.append(f"Command: {command}")
                logs.append(f"Return code: {result.returncode}")
                if result.stdout:
                    logs.append(f"STDOUT: {result.stdout}")
                if result.stderr:
                    logs.append(f"STDERR: {result.stderr}")
                
                if result.returncode != 0:
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        f"Build command failed: {command}",
                        logs=logs
                    )
            
            # Run post-install commands
            if not self.run_post_install_commands(config.post_install_commands):
                self.logger.warning("Some post-install commands failed")
            
            # Verify installation
            if config.verify_command:
                if not self.check_installed(config.verify_command):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Installation verification failed",
                        logs=logs
                    )
                
                installed_version = self.get_version(config.verify_command)
            else:
                installed_version = version
            
            return self.create_install_result(
                InstallStatus.SUCCESS,
                f"{config.display_name} built and installed successfully",
                installed_version,
                logs
            )
            
        except Exception as e:
            self.logger.error(f"Error building {config.name}: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Build failed: {str(e)}"
            )
