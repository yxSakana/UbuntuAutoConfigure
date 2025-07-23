#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Example usage of the Package Manager
Demonstrates various ways to use the package manager programmatically
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from package_manager import PackageManager, PackageConfig, InstallMethod


def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Initialize package manager
    manager = PackageManager()
    
    # List available packages
    packages = manager.list_available_packages()
    print(f"Available packages: {', '.join(packages[:5])}...")
    
    # Get package information
    bat_config = manager.get_package_info("bat")
    if bat_config:
        print(f"Package: {bat_config.display_name}")
        print(f"Description: {bat_config.description}")
        print(f"Install method: {bat_config.install_method.value}")
    
    # Check if package is installed
    is_installed = manager.check_package_installed("bat")
    print(f"bat installed: {is_installed}")
    
    # Get system information
    system_info = manager.get_system_info()
    print(f"System: {system_info['platform']}")
    print(f"Architecture: {system_info['architecture']}")


def example_add_custom_package():
    """Example of adding a custom package configuration"""
    print("\n=== Custom Package Example ===")
    
    manager = PackageManager()
    
    # Create custom package configuration
    custom_config = PackageConfig(
        name="custom_tool",
        display_name="Custom Development Tool",
        description="A custom tool for development",
        install_method=InstallMethod.APT,
        package_name="custom-tool",
        verify_command="custom-tool --version",
        post_install_commands=[
            "echo 'Custom tool installed successfully'",
            "custom-tool --setup"
        ]
    )
    
    # Add to package manager
    manager.add_package_config(custom_config)
    
    # Verify it was added
    retrieved_config = manager.get_package_info("custom_tool")
    if retrieved_config:
        print(f"Added custom package: {retrieved_config.display_name}")
        print(f"Install method: {retrieved_config.install_method.value}")


def example_github_package():
    """Example of configuring a GitHub-based package"""
    print("\n=== GitHub Package Example ===")
    
    manager = PackageManager()
    
    # Create GitHub deb package configuration
    github_config = PackageConfig(
        name="ripgrep",
        display_name="ripgrep",
        description="Fast line-oriented search tool",
        install_method=InstallMethod.GITHUB_DEB,
        github_repo="BurntSushi/ripgrep",
        github_asset_pattern="*amd64.deb",
        verify_command="rg --version",
        supported_architectures=["x86_64"]
    )
    
    manager.add_package_config(github_config)
    
    # Show package info
    config = manager.get_package_info("ripgrep")
    if config:
        print(f"GitHub package: {config.display_name}")
        print(f"Repository: {config.github_repo}")
        print(f"Asset pattern: {config.github_asset_pattern}")


def example_script_package():
    """Example of configuring a script-based package"""
    print("\n=== Script Package Example ===")
    
    manager = PackageManager()
    
    # Create script-based package configuration
    script_config = PackageConfig(
        name="oh_my_zsh",
        display_name="Oh My Zsh",
        description="Framework for managing Zsh configuration",
        install_method=InstallMethod.SCRIPT_URL,
        script_url="https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh",
        script_inputs=["y"],  # Auto-confirm installation
        verify_command="test -d ~/.oh-my-zsh",
        post_install_commands=[
            "echo 'Oh My Zsh installed successfully'",
            "chsh -s $(which zsh)"
        ]
    )
    
    manager.add_package_config(script_config)
    
    config = manager.get_package_info("oh_my_zsh")
    if config:
        print(f"Script package: {config.display_name}")
        print(f"Script URL: {config.script_url}")
        print(f"Auto inputs: {config.script_inputs}")


def example_generate_script():
    """Example of generating installation script"""
    print("\n=== Generate Script Example ===")
    
    manager = PackageManager()
    
    # Select packages to install
    packages_to_install = ["bat", "starship", "htop", "tree"]
    
    # Generate installation script
    script_file = "example_install.sh"
    manager.generate_install_script(packages_to_install, script_file)
    
    print(f"Generated installation script: {script_file}")
    
    # Show script content (first few lines)
    if os.path.exists(script_file):
        with open(script_file, 'r') as f:
            lines = f.readlines()[:10]
            print("Script preview:")
            for line in lines:
                print(f"  {line.rstrip()}")
        
        # Clean up
        os.remove(script_file)


def example_installation_simulation():
    """Example of simulating package installation (without actually installing)"""
    print("\n=== Installation Simulation Example ===")
    
    manager = PackageManager()
    
    # Get packages that are likely to be available
    test_packages = ["tree", "curl", "wget"]  # Common packages
    
    for package_name in test_packages:
        config = manager.get_package_info(package_name)
        if config:
            print(f"\nPackage: {config.display_name}")
            print(f"Install method: {config.install_method.value}")
            
            # Check if already installed
            is_installed = manager.check_package_installed(package_name)
            print(f"Currently installed: {is_installed}")
            
            # Show what would be installed
            if config.install_method == InstallMethod.APT:
                pkg_name = config.package_name or config.name
                print(f"Would run: sudo apt install -y {pkg_name}")
            elif config.install_method == InstallMethod.GITHUB_DEB:
                print(f"Would download from: {config.github_repo}")
                print(f"Asset pattern: {config.github_asset_pattern}")


def example_error_handling():
    """Example of error handling"""
    print("\n=== Error Handling Example ===")
    
    manager = PackageManager()
    
    # Try to get info for non-existent package
    config = manager.get_package_info("nonexistent_package")
    if config is None:
        print("Package 'nonexistent_package' not found (expected)")
    
    # Try to check installation of non-configured package
    try:
        is_installed = manager.check_package_installed("nonexistent_package")
        print(f"Check result for non-existent package: {is_installed}")
    except Exception as e:
        print(f"Error checking non-existent package: {e}")
    
    # Simulate installation error handling
    print("In real usage, you would handle InstallResult status:")
    print("- InstallStatus.SUCCESS: Installation completed")
    print("- InstallStatus.FAILED: Installation failed")
    print("- InstallStatus.ALREADY_INSTALLED: Package already installed")
    print("- InstallStatus.SKIPPED: Installation skipped")


def main():
    """Run all examples"""
    print("Package Manager Usage Examples")
    print("=" * 50)
    
    try:
        example_basic_usage()
        example_add_custom_package()
        example_github_package()
        example_script_package()
        example_generate_script()
        example_installation_simulation()
        example_error_handling()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("\nTo actually install packages, use:")
        print("- GUI: python3 src/modern_app.py")
        print("- CLI: python3 src/cli_app.py install <package_names>")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
