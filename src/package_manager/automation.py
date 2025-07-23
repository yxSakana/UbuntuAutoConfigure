# -*- coding: utf-8 -*-
"""
Automation utilities for handling interactive installations
"""

import subprocess
import threading
import time
import re
from typing import List, Dict, Optional, Callable
import logging


class InteractiveHandler:
    """Handles interactive prompts during installation"""
    
    def __init__(self, responses: List[str], timeout: int = 30):
        """
        Initialize interactive handler
        
        Args:
            responses: List of responses to provide to prompts
            timeout: Timeout for each prompt in seconds
        """
        self.responses = responses
        self.timeout = timeout
        self.response_index = 0
        self.logger = logging.getLogger(__name__)
    
    def get_next_response(self) -> Optional[str]:
        """Get the next response from the list"""
        if self.response_index < len(self.responses):
            response = self.responses[self.response_index]
            self.response_index += 1
            return response
        return None
    
    def handle_process(self, process: subprocess.Popen) -> bool:
        """
        Handle interactive process by providing responses to prompts
        
        Args:
            process: The subprocess to handle
            
        Returns:
            True if successful, False otherwise
        """
        try:
            while process.poll() is None:
                # Check if process is waiting for input
                if process.stdout.readable():
                    # Read available output
                    output = process.stdout.read(1024).decode('utf-8', errors='ignore')
                    if output:
                        self.logger.debug(f"Process output: {output}")
                        
                        # Check if this looks like a prompt
                        if self._is_prompt(output):
                            response = self.get_next_response()
                            if response is not None:
                                self.logger.info(f"Sending response: {response}")
                                process.stdin.write(f"{response}\n".encode())
                                process.stdin.flush()
                            else:
                                self.logger.warning("No more responses available for prompt")
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
            
            return process.returncode == 0
            
        except Exception as e:
            self.logger.error(f"Error handling interactive process: {e}")
            return False
    
    def _is_prompt(self, text: str) -> bool:
        """
        Detect if text contains a prompt that needs a response
        
        Args:
            text: Text to analyze
            
        Returns:
            True if text appears to contain a prompt
        """
        prompt_patterns = [
            r'\[y/n\]',
            r'\[Y/n\]',
            r'\[y/N\]',
            r'Press.*continue',
            r'Do you want to.*\?',
            r'Continue\?',
            r'Proceed\?',
            r'Enter.*:',
            r'Password.*:',
            r'Username.*:',
            r'Please enter',
            r'Choose.*option',
            r'Select.*:',
            r'\(y/n\)',
            r'yes/no',
            r'confirm',
        ]
        
        text_lower = text.lower()
        for pattern in prompt_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False


class ExpectHandler:
    """Advanced handler using expect-like functionality"""
    
    def __init__(self):
        self.patterns: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def expect(self, pattern: str, response: str, timeout: int = 30):
        """
        Add an expect pattern and response
        
        Args:
            pattern: Regular expression pattern to match
            response: Response to send when pattern is matched
            timeout: Timeout for this pattern
        """
        self.patterns.append({
            'pattern': re.compile(pattern, re.IGNORECASE),
            'response': response,
            'timeout': timeout
        })
    
    def handle_command(self, command: str, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        """
        Run command with expect-like handling
        
        Args:
            command: Command to run
            cwd: Working directory
            
        Returns:
            CompletedProcess result
        """
        self.logger.info(f"Running command with expect handling: {command}")
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
            bufsize=0
        )
        
        output_lines = []
        current_output = ""
        
        try:
            while process.poll() is None:
                # Read character by character to catch prompts immediately
                char = process.stdout.read(1)
                if char:
                    current_output += char
                    
                    # Check patterns against current output
                    for pattern_info in self.patterns:
                        if pattern_info['pattern'].search(current_output):
                            response = pattern_info['response']
                            self.logger.info(f"Pattern matched, sending: {response}")
                            
                            process.stdin.write(f"{response}\n")
                            process.stdin.flush()
                            
                            # Clear current output after response
                            output_lines.append(current_output)
                            current_output = ""
                            break
                    
                    # If line is complete, add to output
                    if char == '\n':
                        output_lines.append(current_output)
                        current_output = ""
                
                time.sleep(0.01)  # Small delay
            
            # Get any remaining output
            remaining = process.stdout.read()
            if remaining:
                current_output += remaining
            
            if current_output:
                output_lines.append(current_output)
            
            # Wait for process to complete
            process.wait()
            
            full_output = ''.join(output_lines)
            
            return subprocess.CompletedProcess(
                args=command,
                returncode=process.returncode,
                stdout=full_output,
                stderr=""
            )
            
        except Exception as e:
            self.logger.error(f"Error in expect handling: {e}")
            process.terminate()
            raise
        finally:
            if process.stdin:
                process.stdin.close()
            if process.stdout:
                process.stdout.close()


def create_automation_config(package_name: str) -> Dict:
    """
    Create automation configuration for common packages
    
    Args:
        package_name: Name of the package
        
    Returns:
        Dictionary with automation configuration
    """
    
    # Common automation patterns for popular tools
    automation_configs = {
        'starship': {
            'responses': ['y'],  # Confirm installation
            'expect_patterns': [
                (r'Install Starship', 'y'),
                (r'Continue', 'y')
            ]
        },
        'rustup': {
            'responses': ['1'],  # Default installation
            'expect_patterns': [
                (r'Continue\? \(y/N\)', 'y'),
                (r'Proceed with installation', 'y')
            ]
        },
        'nvm': {
            'responses': ['y'],
            'expect_patterns': [
                (r'Continue', 'y'),
                (r'Press ENTER to continue', ''),
            ]
        },
        'oh-my-zsh': {
            'responses': ['y', 'y'],
            'expect_patterns': [
                (r'Do you want to change your default shell to zsh', 'y'),
                (r'Time to change your default shell to zsh', 'y')
            ]
        },
        'docker': {
            'responses': ['y'],
            'expect_patterns': [
                (r'Do you want to continue', 'y'),
                (r'Add user to docker group', 'y')
            ]
        }
    }
    
    return automation_configs.get(package_name, {
        'responses': ['y'],  # Default: just confirm
        'expect_patterns': [
            (r'\[y/n\]', 'y'),
            (r'\[Y/n\]', 'y'),
            (r'Continue', 'y'),
            (r'Proceed', 'y')
        ]
    })


def run_with_automation(command: str, package_name: str, 
                       cwd: Optional[str] = None,
                       custom_responses: Optional[List[str]] = None) -> subprocess.CompletedProcess:
    """
    Run command with automated responses
    
    Args:
        command: Command to run
        package_name: Package name for automation config
        cwd: Working directory
        custom_responses: Custom responses to use instead of defaults
        
    Returns:
        CompletedProcess result
    """
    
    # Get automation config
    config = create_automation_config(package_name)
    
    # Use custom responses if provided
    responses = custom_responses or config.get('responses', ['y'])
    
    # Create expect handler
    handler = ExpectHandler()
    
    # Add expect patterns
    for pattern, response in config.get('expect_patterns', []):
        handler.expect(pattern, response)
    
    # Add default patterns if none specified
    if not config.get('expect_patterns'):
        handler.expect(r'\[y/n\]', 'y')
        handler.expect(r'\[Y/n\]', 'y')
        handler.expect(r'Continue.*\?', 'y')
        handler.expect(r'Proceed.*\?', 'y')
    
    return handler.handle_command(command, cwd)


class ProgressMonitor:
    """Monitor installation progress and provide feedback"""
    
    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Initialize progress monitor
        
        Args:
            callback: Function to call with progress updates
        """
        self.callback = callback
        self.logger = logging.getLogger(__name__)
    
    def monitor_process(self, process: subprocess.Popen, package_name: str):
        """
        Monitor process output for progress information
        
        Args:
            process: Process to monitor
            package_name: Name of package being installed
        """
        
        progress_patterns = [
            (r'(\d+)%', 'Progress: {}%'),
            (r'Downloading.*', 'Downloading...'),
            (r'Installing.*', 'Installing...'),
            (r'Configuring.*', 'Configuring...'),
            (r'Building.*', 'Building...'),
            (r'Compiling.*', 'Compiling...'),
            (r'Extracting.*', 'Extracting...'),
            (r'Setting up.*', 'Setting up...'),
        ]
        
        def monitor_thread():
            try:
                while process.poll() is None:
                    line = process.stdout.readline()
                    if line:
                        line = line.strip()
                        self.logger.debug(f"Process output: {line}")
                        
                        # Check for progress patterns
                        for pattern, message_template in progress_patterns:
                            match = re.search(pattern, line, re.IGNORECASE)
                            if match:
                                if '{}' in message_template:
                                    message = message_template.format(match.group(1))
                                else:
                                    message = message_template
                                
                                self.logger.info(f"{package_name}: {message}")
                                if self.callback:
                                    self.callback(f"{package_name}: {message}")
                                break
            except Exception as e:
                self.logger.error(f"Error monitoring process: {e}")
        
        # Start monitoring in separate thread
        monitor_thread = threading.Thread(target=monitor_thread)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return monitor_thread
