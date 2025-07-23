# -*- coding: utf-8 -*-
"""
System package manager installers (apt, snap, flatpak)
"""

from typing import TYPE_CHECKING

from .base import BaseInstaller, InstallResult, InstallStatus

if TYPE_CHECKING:
    from ..config import PackageConfig


class AptInstaller(BaseInstaller):
    """Installer using apt package manager"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package using apt"""
        
        package_name = config.package_name or config.name
        
        # Check if already installed
        if self._is_apt_package_installed(package_name):
            version = self._get_apt_package_version(package_name)
            return self.create_install_result(
                InstallStatus.ALREADY_INSTALLED,
                f"{config.display_name} is already installed via apt",
                version
            )
        
        try:
            # Update package list
            self.logger.info("Updating apt package list")
            update_command = "sudo apt update"
            if self.sudo_password:
                update_command = f"echo '{self.sudo_password}' | sudo -S apt update"
            
            result = self.run_command(update_command)
            if result.returncode != 0:
                self.logger.warning(f"Failed to update package list: {result.stderr}")
            
            # Install the package
            install_command = f"sudo apt install -y {package_name}"
            if self.sudo_password:
                install_command = f"echo '{self.sudo_password}' | sudo -S apt install -y {package_name}"
            
            self.logger.info(f"Installing {package_name} via apt")
            result = self.run_command(install_command)
            
            if result.returncode != 0:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    f"Failed to install {package_name} via apt: {result.stderr}",
                    logs=[result.stdout, result.stderr]
                )
            
            # Run post-install commands
            if not self.run_post_install_commands(config.post_install_commands):
                self.logger.warning("Some post-install commands failed")
            
            # Get installed version
            installed_version = self._get_apt_package_version(package_name)
            
            # Verify installation if verify command is provided
            if config.verify_command:
                if not self.check_installed(config.verify_command):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Installation verification failed"
                    )
                
                # Use verify command version if available
                verify_version = self.get_version(config.verify_command)
                if verify_version:
                    installed_version = verify_version
            
            return self.create_install_result(
                InstallStatus.SUCCESS,
                f"{config.display_name} installed successfully via apt",
                installed_version,
                [result.stdout]
            )
            
        except Exception as e:
            self.logger.error(f"Error installing {package_name} via apt: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Apt installation failed: {str(e)}"
            )
    
    def _is_apt_package_installed(self, package_name: str) -> bool:
        """Check if apt package is installed"""
        try:
            result = self.run_command(f"dpkg -l | grep '^ii.*{package_name}'")
            return result.returncode == 0
        except:
            return False
    
    def _get_apt_package_version(self, package_name: str) -> str:
        """Get installed apt package version"""
        try:
            result = self.run_command(f"dpkg -l {package_name}")
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('ii'):
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2]
        except:
            pass
        return "unknown"


class SnapInstaller(BaseInstaller):
    """Installer using snap package manager"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package using snap"""
        
        package_name = config.package_name or config.name
        
        # Check if snap is available
        if not self.check_installed("snap --version"):
            return self.create_install_result(
                InstallStatus.FAILED,
                "Snap is not installed on this system"
            )
        
        # Check if already installed
        if self._is_snap_package_installed(package_name):
            version = self._get_snap_package_version(package_name)
            return self.create_install_result(
                InstallStatus.ALREADY_INSTALLED,
                f"{config.display_name} is already installed via snap",
                version
            )
        
        try:
            # Install the package
            install_command = f"sudo snap install {package_name}"
            if self.sudo_password:
                install_command = f"echo '{self.sudo_password}' | sudo -S snap install {package_name}"
            
            self.logger.info(f"Installing {package_name} via snap")
            result = self.run_command(install_command)
            
            if result.returncode != 0:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    f"Failed to install {package_name} via snap: {result.stderr}",
                    logs=[result.stdout, result.stderr]
                )
            
            # Run post-install commands
            if not self.run_post_install_commands(config.post_install_commands):
                self.logger.warning("Some post-install commands failed")
            
            # Get installed version
            installed_version = self._get_snap_package_version(package_name)
            
            # Verify installation if verify command is provided
            if config.verify_command:
                if not self.check_installed(config.verify_command):
                    return self.create_install_result(
                        InstallStatus.FAILED,
                        "Installation verification failed"
                    )
                
                verify_version = self.get_version(config.verify_command)
                if verify_version:
                    installed_version = verify_version
            
            return self.create_install_result(
                InstallStatus.SUCCESS,
                f"{config.display_name} installed successfully via snap",
                installed_version,
                [result.stdout]
            )
            
        except Exception as e:
            self.logger.error(f"Error installing {package_name} via snap: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Snap installation failed: {str(e)}"
            )
    
    def _is_snap_package_installed(self, package_name: str) -> bool:
        """Check if snap package is installed"""
        try:
            result = self.run_command(f"snap list {package_name}")
            return result.returncode == 0
        except:
            return False
    
    def _get_snap_package_version(self, package_name: str) -> str:
        """Get installed snap package version"""
        try:
            result = self.run_command(f"snap list {package_name}")
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:  # Skip header
                    parts = lines[1].split()
                    if len(parts) >= 2:
                        return parts[1]
        except:
            pass
        return "unknown"


class FlatpakInstaller(BaseInstaller):
    """Installer using flatpak package manager"""
    
    def install(self, config: 'PackageConfig') -> InstallResult:
        """Install package using flatpak"""
        
        package_name = config.package_name or config.name
        
        # Check if flatpak is available
        if not self.check_installed("flatpak --version"):
            return self.create_install_result(
                InstallStatus.FAILED,
                "Flatpak is not installed on this system"
            )
        
        # Check if already installed
        if self._is_flatpak_package_installed(package_name):
            version = self._get_flatpak_package_version(package_name)
            return self.create_install_result(
                InstallStatus.ALREADY_INSTALLED,
                f"{config.display_name} is already installed via flatpak",
                version
            )
        
        try:
            # Install the package
            install_command = f"flatpak install -y flathub {package_name}"
            
            self.logger.info(f"Installing {package_name} via flatpak")
            result = self.run_command(install_command)
            
            if result.returncode != 0:
                return self.create_install_result(
                    InstallStatus.FAILED,
                    f"Failed to install {package_name} via flatpak: {result.stderr}",
                    logs=[result.stdout, result.stderr]
                )
            
            # Run post-install commands
            if not self.run_post_install_commands(config.post_install_commands):
                self.logger.warning("Some post-install commands failed")
            
            # Get installed version
            installed_version = self._get_flatpak_package_version(package_name)
            
            return self.create_install_result(
                InstallStatus.SUCCESS,
                f"{config.display_name} installed successfully via flatpak",
                installed_version,
                [result.stdout]
            )
            
        except Exception as e:
            self.logger.error(f"Error installing {package_name} via flatpak: {e}")
            return self.create_install_result(
                InstallStatus.FAILED,
                f"Flatpak installation failed: {str(e)}"
            )
    
    def _is_flatpak_package_installed(self, package_name: str) -> bool:
        """Check if flatpak package is installed"""
        try:
            result = self.run_command(f"flatpak list | grep {package_name}")
            return result.returncode == 0
        except:
            return False
    
    def _get_flatpak_package_version(self, package_name: str) -> str:
        """Get installed flatpak package version"""
        try:
            result = self.run_command(f"flatpak list --app | grep {package_name}")
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split('\t')
                    if len(parts) >= 3:
                        return parts[2]
        except:
            pass
        return "unknown"
