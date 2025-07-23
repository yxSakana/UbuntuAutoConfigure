#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Modern Package Manager Application
Enhanced version with new package manager integration
"""

import sys
import os
import logging

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.modern_package_ui import PackageManagerUI


def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('package_manager.log')
        ]
    )


def main():
    """Main application entry point"""
    try:
        setup_logging()
        
        # Create and run the GUI application
        app = PackageManagerUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Application error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
