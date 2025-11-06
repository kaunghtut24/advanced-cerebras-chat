"""
Code Execution Service for Cerebras Chat
Provides secure Python code execution with sandboxing and output capture
"""

import sys
import io
import traceback
import contextlib
import ast
import time
import signal
from typing import Dict, Any, Optional
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import pandas as pd

class CodeExecutor:
    """Secure Python code executor with output capture and timeout"""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize code executor
        
        Args:
            timeout: Maximum execution time in seconds (default: 30)
        """
        self.timeout = timeout
        self.allowed_modules = {
            'math', 'random', 'datetime', 'json', 'collections',
            'itertools', 'functools', 'operator', 're', 'string',
            'numpy', 'pandas', 'matplotlib', 'scipy', 'statistics',
            'decimal', 'fractions', 'time'
        }
        
    def _timeout_handler(self, signum, frame):
        """Handle timeout signal"""
        raise TimeoutError(f"Code execution exceeded {self.timeout} seconds")
    
    def _validate_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate code for dangerous operations
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        
        # Check for dangerous operations
        dangerous_patterns = [
            'import os', 'import subprocess', 'import sys',
            'open(', '__import__', 'eval(', 'exec(',
            'compile(', 'globals(', 'locals(',
            'import shutil', 'import socket', 'import requests'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                return False, f"Forbidden operation detected: {pattern}"
        
        return True, None
    
    def _create_safe_globals(self) -> Dict[str, Any]:
        """Create a safe globals dictionary with allowed modules"""
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'type': type,
                'isinstance': isinstance,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'dir': dir,
                'help': help,
                'Exception': Exception,
                'ValueError': ValueError,
                'TypeError': TypeError,
                'KeyError': KeyError,
                'IndexError': IndexError,
                'AttributeError': AttributeError,
                'ZeroDivisionError': ZeroDivisionError,
            },
            'np': np,
            'pd': pd,
            'plt': plt,
            'math': __import__('math'),
            'random': __import__('random'),
            'datetime': __import__('datetime'),
            'json': __import__('json'),
            'collections': __import__('collections'),
            'itertools': __import__('itertools'),
            'functools': __import__('functools'),
            're': __import__('re'),
            'statistics': __import__('statistics'),
        }
        return safe_globals
    
    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code and capture output
        
        Args:
            code: Python code to execute
            
        Returns:
            Dictionary containing:
                - success: bool
                - output: str (stdout)
                - error: str (stderr/exceptions)
                - result: Any (last expression result)
                - plots: list of base64 encoded plot images
                - execution_time: float (seconds)
        """
        # Validate code
        is_valid, error_msg = self._validate_code(code)
        if not is_valid:
            return {
                'success': False,
                'output': '',
                'error': error_msg,
                'result': None,
                'plots': [],
                'execution_time': 0
            }
        
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        # Track plots
        plots = []
        
        start_time = time.time()
        
        try:
            # Set timeout (Unix-like systems only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, self._timeout_handler)
                signal.alarm(self.timeout)
            
            # Create safe execution environment
            safe_globals = self._create_safe_globals()
            safe_locals = {}
            
            # Redirect stdout and stderr
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                
                # Execute code
                exec(code, safe_globals, safe_locals)
                
                # Capture any matplotlib plots
                if plt.get_fignums():
                    for fig_num in plt.get_fignums():
                        fig = plt.figure(fig_num)
                        buf = BytesIO()
                        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
                        buf.seek(0)
                        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
                        plots.append(plot_base64)
                        plt.close(fig)
            
            # Cancel timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
            execution_time = time.time() - start_time
            
            # Get the last expression result if any
            result = None
            if safe_locals:
                # Try to get the last assigned variable
                last_var = list(safe_locals.keys())[-1] if safe_locals else None
                if last_var and not last_var.startswith('_'):
                    result = safe_locals[last_var]
            
            return {
                'success': True,
                'output': stdout_capture.getvalue(),
                'error': stderr_capture.getvalue(),
                'result': str(result) if result is not None else None,
                'plots': plots,
                'execution_time': execution_time
            }
            
        except TimeoutError as e:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            return {
                'success': False,
                'output': stdout_capture.getvalue(),
                'error': str(e),
                'result': None,
                'plots': plots,
                'execution_time': time.time() - start_time
            }
            
        except Exception as e:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            error_trace = traceback.format_exc()
            return {
                'success': False,
                'output': stdout_capture.getvalue(),
                'error': error_trace,
                'result': None,
                'plots': plots,
                'execution_time': time.time() - start_time
            }

# Global executor instance
executor = CodeExecutor(timeout=30)

def execute_code(code: str) -> Dict[str, Any]:
    """
    Execute Python code safely
    
    Args:
        code: Python code to execute
        
    Returns:
        Execution result dictionary
    """
    return executor.execute(code)

