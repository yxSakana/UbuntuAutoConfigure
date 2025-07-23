# -*- coding: utf-8 -*-
"""
Modern Package Manager UI
Enhanced GUI interface for the new package manager
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from typing import Dict, List, Optional
import platform

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from package_manager import PackageManager, PackageConfig, InstallResult, InstallStatus
from ui.pwd_entry import PasswordEntry


class PackageManagerUI:
    """Modern GUI for the package manager"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.package_manager: Optional[PackageManager] = None
        self.sudo_password: Optional[str] = None
        
        # UI Components
        self.package_vars: Dict[str, tk.BooleanVar] = {}
        self.package_checkboxes: Dict[str, ttk.Checkbutton] = {}
        self.progress_var = tk.StringVar()
        self.log_text: Optional[scrolledtext.ScrolledText] = None
        
        # Installation state
        self.installation_running = False
        self.installation_results: Dict[str, InstallResult] = {}
        
        self.setup_ui()
        self.setup_logging()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("Ubuntu Auto Configure - Package Manager")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Create main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Package selection tab
        self.create_package_tab(notebook)
        
        # Installation log tab
        self.create_log_tab(notebook)
        
        # System info tab
        self.create_info_tab(notebook)
        
        # Bottom frame for controls
        self.create_control_frame()
    
    def create_package_tab(self, parent):
        """Create package selection tab"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Package Selection")
        
        # Create scrollable frame for packages
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add package selection controls
        self.create_package_controls(scrollable_frame)
    
    def create_package_controls(self, parent):
        """Create package selection controls"""
        # Architecture info
        arch_frame = ttk.LabelFrame(parent, text="System Information")
        arch_frame.pack(fill=tk.X, padx=5, pady=5)
        
        arch = platform.machine()
        ttk.Label(arch_frame, text=f"Architecture: {arch}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(arch_frame, text=f"Platform: {platform.platform()}").pack(anchor=tk.W, padx=5, pady=2)
        
        # Package categories
        categories = {
            "Development Tools": ["bat", "starship", "neovim", "golang"],
            "System Monitoring": ["btop", "lsd"],
            "Package Managers": [],  # Will be populated dynamically
        }
        
        # Initialize package manager to get available packages
        try:
            temp_manager = PackageManager()
            available_packages = temp_manager.list_available_packages()
            
            # Categorize packages
            dev_tools = ["bat", "starship", "neovim", "golang", "btop", "lsd"]
            
            for package_name in available_packages:
                if package_name not in dev_tools:
                    categories["Package Managers"].append(package_name)
            
            # Create UI for each category
            for category, packages in categories.items():
                if not packages:
                    continue
                    
                category_frame = ttk.LabelFrame(parent, text=category)
                category_frame.pack(fill=tk.X, padx=5, pady=5)
                
                for package_name in packages:
                    self.create_package_checkbox(category_frame, package_name, temp_manager)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize package manager: {e}")
    
    def create_package_checkbox(self, parent, package_name: str, manager: PackageManager):
        """Create checkbox for a package"""
        config = manager.get_package_info(package_name)
        if not config:
            return
        
        # Create frame for package
        package_frame = ttk.Frame(parent)
        package_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Create checkbox variable
        var = tk.BooleanVar()
        self.package_vars[package_name] = var
        
        # Create checkbox
        checkbox = ttk.Checkbutton(
            package_frame,
            text=config.display_name,
            variable=var
        )
        checkbox.pack(side=tk.LEFT)
        self.package_checkboxes[package_name] = checkbox
        
        # Add description label
        if config.description:
            desc_label = ttk.Label(
                package_frame,
                text=f"- {config.description}",
                foreground="gray"
            )
            desc_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Add install method info
        method_label = ttk.Label(
            package_frame,
            text=f"[{config.install_method.value}]",
            foreground="blue"
        )
        method_label.pack(side=tk.RIGHT)
    
    def create_log_tab(self, parent):
        """Create installation log tab"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Installation Log")
        
        # Create scrolled text widget for logs
        self.log_text = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=30
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add clear button
        clear_btn = ttk.Button(
            frame,
            text="Clear Log",
            command=self.clear_log
        )
        clear_btn.pack(pady=5)
    
    def create_info_tab(self, parent):
        """Create system information tab"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="System Info")
        
        # Create text widget for system info
        info_text = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            state=tk.DISABLED
        )
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Populate system info
        try:
            temp_manager = PackageManager()
            system_info = temp_manager.get_system_info()
            
            info_text.config(state=tk.NORMAL)
            info_text.insert(tk.END, "System Information:\n")
            info_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for key, value in system_info.items():
                info_text.insert(tk.END, f"{key.title()}: {value}\n")
            
            info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            info_text.config(state=tk.NORMAL)
            info_text.insert(tk.END, f"Error getting system info: {e}")
            info_text.config(state=tk.DISABLED)
    
    def create_control_frame(self):
        """Create control buttons frame"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            control_frame,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Progress label
        progress_label = ttk.Label(control_frame, textvariable=self.progress_var)
        progress_label.pack(pady=2)
        
        # Button frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Select all button
        select_all_btn = ttk.Button(
            button_frame,
            text="Select All",
            command=self.select_all_packages
        )
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Deselect all button
        deselect_all_btn = ttk.Button(
            button_frame,
            text="Deselect All",
            command=self.deselect_all_packages
        )
        deselect_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Generate script button
        script_btn = ttk.Button(
            button_frame,
            text="Generate Script",
            command=self.generate_script
        )
        script_btn.pack(side=tk.LEFT, padx=5)
        
        # Install button
        self.install_btn = ttk.Button(
            button_frame,
            text="Install Selected",
            command=self.start_installation
        )
        self.install_btn.pack(side=tk.RIGHT, padx=5)
    
    def setup_logging(self):
        """Setup logging to display in the log tab"""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                if self.text_widget:
                    self.text_widget.insert(tk.END, msg + "\n")
                    self.text_widget.see(tk.END)
        
        if self.log_text:
            handler = TextHandler(self.log_text)
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            
            # Add handler to package manager logger
            logger = logging.getLogger('src.package_manager')
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def select_all_packages(self):
        """Select all packages"""
        for var in self.package_vars.values():
            var.set(True)
    
    def deselect_all_packages(self):
        """Deselect all packages"""
        for var in self.package_vars.values():
            var.set(False)
    
    def get_selected_packages(self) -> List[str]:
        """Get list of selected packages"""
        return [
            package_name for package_name, var in self.package_vars.items()
            if var.get()
        ]
    
    def clear_log(self):
        """Clear the log text"""
        if self.log_text:
            self.log_text.delete(1.0, tk.END)
    
    def generate_script(self):
        """Generate installation script"""
        selected = self.get_selected_packages()
        if not selected:
            messagebox.showwarning("Warning", "No packages selected")
            return
        
        try:
            manager = PackageManager()
            manager.generate_install_script(selected, "auto_install.sh")
            messagebox.showinfo("Success", "Installation script generated: auto_install.sh")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate script: {e}")
    
    def start_installation(self):
        """Start package installation"""
        if self.installation_running:
            messagebox.showwarning("Warning", "Installation already running")
            return
        
        selected = self.get_selected_packages()
        if not selected:
            messagebox.showwarning("Warning", "No packages selected")
            return
        
        # Get sudo password
        PasswordEntry(self.root, "Enter sudo password", self.install_packages)
    
    def install_packages(self, password: str):
        """Install selected packages"""
        self.sudo_password = password
        selected = self.get_selected_packages()
        
        # Start installation in separate thread
        self.installation_running = True
        self.install_btn.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Starting installation...")
        
        thread = threading.Thread(
            target=self._install_packages_thread,
            args=(selected,)
        )
        thread.daemon = True
        thread.start()
    
    def _install_packages_thread(self, packages: List[str]):
        """Installation thread"""
        try:
            self.package_manager = PackageManager(self.sudo_password)
            
            for i, package_name in enumerate(packages):
                self.progress_var.set(f"Installing {package_name} ({i+1}/{len(packages)})")
                
                result = self.package_manager.install_package(package_name)
                self.installation_results[package_name] = result
                
                # Log result
                if self.log_text:
                    status_color = "green" if result.success else "red"
                    self.log_text.insert(tk.END, f"\n{package_name}: {result.message}\n")
                    if result.version:
                        self.log_text.insert(tk.END, f"Version: {result.version}\n")
                    self.log_text.see(tk.END)
            
            # Show completion message
            self.root.after(0, self._installation_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self._installation_error(str(e)))
    
    def _installation_complete(self):
        """Handle installation completion"""
        self.installation_running = False
        self.install_btn.config(state=tk.NORMAL)
        self.progress_bar.stop()
        
        # Count results
        success_count = sum(1 for r in self.installation_results.values() if r.success)
        total_count = len(self.installation_results)
        
        self.progress_var.set(f"Installation complete: {success_count}/{total_count} successful")
        
        # Show summary
        summary = f"Installation Summary:\n\n"
        for package, result in self.installation_results.items():
            status = "✓" if result.success else "✗"
            summary += f"{status} {package}: {result.message}\n"
        
        messagebox.showinfo("Installation Complete", summary)
    
    def _installation_error(self, error_msg: str):
        """Handle installation error"""
        self.installation_running = False
        self.install_btn.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.progress_var.set("Installation failed")
        
        messagebox.showerror("Installation Error", f"Installation failed: {error_msg}")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    app = PackageManagerUI()
    app.run()
