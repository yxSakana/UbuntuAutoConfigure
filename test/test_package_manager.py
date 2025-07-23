#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Test cases for the package manager
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from package_manager import PackageManager, PackageConfig, InstallMethod, InstallStatus
from package_manager.github_api import GitHubAPI
from package_manager.config import PackageConfigManager


class TestPackageConfig(unittest.TestCase):
    """Test PackageConfig functionality"""
    
    def test_package_config_creation(self):
        """Test creating a package configuration"""
        config = PackageConfig(
            name="test_package",
            display_name="Test Package",
            description="A test package",
            install_method=InstallMethod.APT,
            package_name="test-pkg"
        )
        
        self.assertEqual(config.name, "test_package")
        self.assertEqual(config.display_name, "Test Package")
        self.assertEqual(config.install_method, InstallMethod.APT)
        self.assertEqual(config.package_name, "test-pkg")
    
    def test_package_config_serialization(self):
        """Test package configuration serialization"""
        config = PackageConfig(
            name="test_package",
            display_name="Test Package",
            install_method=InstallMethod.GITHUB_DEB,
            github_repo="owner/repo",
            github_asset_pattern="*.deb"
        )
        
        # Test to_dict
        data = config.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "test_package")
        self.assertEqual(data["install_method"], "github_deb")
        
        # Test from_dict
        restored_config = PackageConfig.from_dict(data)
        self.assertEqual(restored_config.name, config.name)
        self.assertEqual(restored_config.install_method, config.install_method)


class TestPackageConfigManager(unittest.TestCase):
    """Test PackageConfigManager functionality"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_manager = PackageConfigManager(self.temp_dir)
    
    def tearDown(self):
        """Cleanup test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_default_packages_loaded(self):
        """Test that default packages are loaded"""
        packages = self.config_manager.list_packages()
        self.assertGreater(len(packages), 0)
        
        # Check for some expected default packages
        expected_packages = ["bat", "starship", "neovim"]
        for package in expected_packages:
            self.assertIn(package, packages)
    
    def test_add_package(self):
        """Test adding a new package"""
        config = PackageConfig(
            name="custom_package",
            display_name="Custom Package",
            install_method=InstallMethod.APT
        )
        
        self.config_manager.add_package(config)
        
        # Verify package was added
        retrieved_config = self.config_manager.get_package("custom_package")
        self.assertIsNotNone(retrieved_config)
        self.assertEqual(retrieved_config.name, "custom_package")
    
    def test_get_nonexistent_package(self):
        """Test getting a package that doesn't exist"""
        config = self.config_manager.get_package("nonexistent_package")
        self.assertIsNone(config)


class TestGitHubAPI(unittest.TestCase):
    """Test GitHub API functionality"""
    
    def setUp(self):
        """Setup test environment"""
        self.github_api = GitHubAPI()
    
    def test_get_latest_release(self):
        """Test getting latest release information"""
        # Test with a known repository
        release = self.github_api.get_latest_release("sharkdp/bat")
        
        if release:  # Only test if we can connect to GitHub
            self.assertIsNotNone(release.tag_name)
            self.assertIsNotNone(release.name)
            self.assertIsInstance(release.assets, list)
    
    def test_find_asset_by_pattern(self):
        """Test finding assets by pattern"""
        release = self.github_api.get_latest_release("sharkdp/bat")
        
        if release:  # Only test if we can connect to GitHub
            asset = self.github_api.find_asset_by_pattern(release, "*amd64.deb")
            if asset:  # Asset might not exist for all releases
                self.assertIn("name", asset)
                self.assertIn("browser_download_url", asset)
    
    def test_get_download_url(self):
        """Test getting download URL"""
        result = self.github_api.get_download_url("sharkdp/bat", "*amd64.deb")
        
        if result:  # Only test if we can connect to GitHub and asset exists
            url, version = result
            self.assertIsInstance(url, str)
            self.assertIsInstance(version, str)
            self.assertTrue(url.startswith("https://"))


class TestPackageManager(unittest.TestCase):
    """Test PackageManager functionality"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.package_manager = PackageManager(config_dir=self.temp_dir)
    
    def tearDown(self):
        """Cleanup test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        if self.package_manager:
            self.package_manager.cleanup()
    
    def test_list_available_packages(self):
        """Test listing available packages"""
        packages = self.package_manager.list_available_packages()
        self.assertIsInstance(packages, list)
        self.assertGreater(len(packages), 0)
    
    def test_get_package_info(self):
        """Test getting package information"""
        # Test with a known package
        config = self.package_manager.get_package_info("bat")
        self.assertIsNotNone(config)
        self.assertEqual(config.name, "bat")
        self.assertEqual(config.install_method, InstallMethod.GITHUB_DEB)
        
        # Test with nonexistent package
        config = self.package_manager.get_package_info("nonexistent_package")
        self.assertIsNone(config)
    
    def test_add_package_config(self):
        """Test adding package configuration"""
        config = PackageConfig(
            name="test_package",
            display_name="Test Package",
            install_method=InstallMethod.APT
        )
        
        self.package_manager.add_package_config(config)
        
        # Verify package was added
        retrieved_config = self.package_manager.get_package_info("test_package")
        self.assertIsNotNone(retrieved_config)
        self.assertEqual(retrieved_config.name, "test_package")
    
    def test_get_system_info(self):
        """Test getting system information"""
        system_info = self.package_manager.get_system_info()
        self.assertIsInstance(system_info, dict)
        
        expected_keys = ["platform", "architecture", "python_version", "distribution"]
        for key in expected_keys:
            self.assertIn(key, system_info)
    
    def test_generate_install_script(self):
        """Test generating installation script"""
        script_file = os.path.join(self.temp_dir, "test_install.sh")
        
        self.package_manager.generate_install_script(["bat", "starship"], script_file)
        
        # Verify script was created
        self.assertTrue(os.path.exists(script_file))
        
        # Verify script is executable
        self.assertTrue(os.access(script_file, os.X_OK))
        
        # Verify script content
        with open(script_file, 'r') as f:
            content = f.read()
            self.assertIn("#!/bin/bash", content)
            self.assertIn("bat", content)
            self.assertIn("starship", content)


class TestInstallationMethods(unittest.TestCase):
    """Test different installation methods"""
    
    def setUp(self):
        """Setup test environment"""
        self.package_manager = PackageManager()
    
    def tearDown(self):
        """Cleanup test environment"""
        if self.package_manager:
            self.package_manager.cleanup()
    
    def test_apt_installer_creation(self):
        """Test creating APT installer"""
        installer = self.package_manager.get_installer(InstallMethod.APT)
        self.assertIsNotNone(installer)
    
    def test_github_deb_installer_creation(self):
        """Test creating GitHub DEB installer"""
        installer = self.package_manager.get_installer(InstallMethod.GITHUB_DEB)
        self.assertIsNotNone(installer)
    
    def test_script_installer_creation(self):
        """Test creating script installer"""
        installer = self.package_manager.get_installer(InstallMethod.SCRIPT_URL)
        self.assertIsNotNone(installer)
    
    def test_unsupported_installer(self):
        """Test handling unsupported installation method"""
        with self.assertRaises(ValueError):
            # Create a fake install method
            fake_method = "fake_method"
            self.package_manager.get_installer(fake_method)


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestPackageConfig,
        TestPackageConfigManager,
        TestGitHubAPI,
        TestPackageManager,
        TestInstallationMethods
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
