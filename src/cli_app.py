#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Command Line Interface for Package Manager
Provides CLI access to the package manager functionality
"""

import sys
import os
import argparse
import getpass
import logging
from typing import List

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from package_manager import PackageManager, InstallStatus


def setup_logging(verbose: bool = False):
    """Setup logging for CLI"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def list_packages(manager: PackageManager):
    """List all available packages"""
    packages = manager.list_available_packages()
    
    print("Available packages:")
    print("=" * 50)
    
    for package_name in sorted(packages):
        config = manager.get_package_info(package_name)
        if config:
            status = "✓" if manager.check_package_installed(package_name) else " "
            print(f"[{status}] {config.display_name}")
            print(f"    Method: {config.install_method.value}")
            if config.description:
                print(f"    Description: {config.description}")
            print()


def show_package_info(manager: PackageManager, package_name: str):
    """Show detailed information about a package"""
    config = manager.get_package_info(package_name)
    if not config:
        print(f"Package '{package_name}' not found")
        return
    
    print(f"Package Information: {config.display_name}")
    print("=" * 50)
    print(f"Name: {config.name}")
    print(f"Display Name: {config.display_name}")
    print(f"Description: {config.description}")
    print(f"Install Method: {config.install_method.value}")
    print(f"Requires Sudo: {config.requires_sudo}")
    print(f"Supported Architectures: {', '.join(config.supported_architectures)}")
    
    if config.github_repo:
        print(f"GitHub Repository: {config.github_repo}")
    if config.package_name:
        print(f"Package Name: {config.package_name}")
    if config.verify_command:
        print(f"Verify Command: {config.verify_command}")
    
    # Check if installed
    installed = manager.check_package_installed(package_name)
    print(f"Installed: {'Yes' if installed else 'No'}")


def install_packages(manager: PackageManager, package_names: List[str], 
                    generate_script: bool = False):
    """Install packages"""
    
    if generate_script:
        # Generate installation script
        script_file = "auto_install.sh"
        manager.generate_install_script(package_names, script_file)
        print(f"Installation script generated: {script_file}")
        print("Run the script with: ./auto_install.sh")
        return
    
    # Interactive installation
    print(f"Installing {len(package_names)} packages...")
    print("Packages to install:", ", ".join(package_names))
    
    # Confirm installation
    confirm = input("Continue? (y/N): ").lower().strip()
    if confirm != 'y':
        print("Installation cancelled")
        return
    
    # Install packages
    results = manager.install_packages(package_names)
    
    # Show results
    print("\nInstallation Results:")
    print("=" * 50)
    
    success_count = 0
    for package_name, result in results.items():
        status_symbol = "✓" if result.success else "✗"
        print(f"{status_symbol} {package_name}: {result.message}")
        if result.version:
            print(f"   Version: {result.version}")
        
        if result.success:
            success_count += 1
    
    print(f"\nSummary: {success_count}/{len(results)} packages installed successfully")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Ubuntu Auto Configure - Package Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          # List all packages
  %(prog)s info bat                      # Show package info
  %(prog)s install bat starship         # Install packages
  %(prog)s install --script bat lsd     # Generate install script
  %(prog)s system-info                   # Show system information
        """
    )
    
    parser.add_argument(
        'command',
        choices=['list', 'info', 'install', 'system-info'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'packages',
        nargs='*',
        help='Package names (for info and install commands)'
    )
    
    parser.add_argument(
        '--script',
        action='store_true',
        help='Generate installation script instead of installing directly'
    )
    
    parser.add_argument(
        '--password',
        help='Sudo password (will prompt if not provided)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    try:
        # Get sudo password if needed
        sudo_password = None
        if args.command == 'install' and not args.script:
            if args.password:
                sudo_password = args.password
            else:
                sudo_password = getpass.getpass("Enter sudo password: ")
        
        # Initialize package manager
        manager = PackageManager(sudo_password)
        
        # Execute command
        if args.command == 'list':
            list_packages(manager)
            
        elif args.command == 'info':
            if not args.packages:
                print("Error: Package name required for info command")
                sys.exit(1)
            
            for package_name in args.packages:
                show_package_info(manager, package_name)
                if len(args.packages) > 1:
                    print()  # Separator for multiple packages
        
        elif args.command == 'install':
            if not args.packages:
                print("Error: Package names required for install command")
                sys.exit(1)
            
            install_packages(manager, args.packages, args.script)
        
        elif args.command == 'system-info':
            system_info = manager.get_system_info()
            print("System Information:")
            print("=" * 50)
            for key, value in system_info.items():
                print(f"{key.title()}: {value}")
        
        # Cleanup
        manager.cleanup()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"CLI error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
