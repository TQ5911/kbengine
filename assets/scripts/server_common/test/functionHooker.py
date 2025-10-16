#!/usr/bin/env python3
"""
Enhanced Function Hook Tool
- Supports hooking specified classes and methods in modules
- Supports displaying call stack information (traceback)
- Supports multiple hook granularity controls
"""

import ast
import inspect
import sys
import importlib
import importlib.util
import traceback
from functools import wraps
from pathlib import Path
from types import FunctionType, ModuleType
from typing import Any, Dict, List, Set, Optional, Union, Callable
from KBEDebug import *

class FunctionHooker:
    def __init__(self, 
                 prefix: str = "",
                 show_traceback: bool = False,
                 traceback_depth: int = 5,
                 show_args: bool = True,
                 show_return: bool = True,
                 show_errors: bool = True,
                 verbose: bool = True):
        """
        Initialize enhanced hook tool
        
        Args:
            prefix: Log prefix
            show_traceback: Whether to show call stack information
            traceback_depth: Call stack display depth
            show_args: Whether to show argument information
            show_return: Whether to show return value
            show_errors: Whether to show error information
            verbose: Whether to show detailed logs
        """
        self.prefix = prefix
        self.show_traceback = show_traceback
        self.traceback_depth = traceback_depth
        self.show_args = show_args
        self.show_return = show_return
        self.show_errors = show_errors
        self.verbose = verbose
        
        self.hooked_functions: Set[FunctionType] = set()
        self.hooked_classes: Set[type] = set()
        self.hooked_methods: Set[tuple] = set()  # (class, method_name)
    
    def _format_traceback(self, limit: int = None) -> str:
        """Format call stack information"""
        if limit is None:
            limit = self.traceback_depth
            
        stack = inspect.stack()
        # Skip the call stack of the Hook tool itself
        relevant_stack = []
        for frame in stack[2:]:  # Skip current function and caller
            filename = frame.filename
            # Skip standard library and Hook tool's own files
            if 'site-packages' not in filename and 'hook_tool' not in filename:
                relevant_stack.append(frame)
            if len(relevant_stack) >= limit:
                break
        
        if not relevant_stack:
            return "  [not traceback available]"

        traceback_lines = ["traceback:"]
        for i, frame in enumerate(relevant_stack):
            filename = Path(frame.filename).name
            traceback_lines.append(f"  {i+1}. {filename}:{frame.lineno} ({frame.function})")
        
        return "\n".join(traceback_lines)
    
    def _format_function_call(self, func: FunctionType, args: tuple, kwargs: dict) -> str:
        """Format function call information"""
        lines = []
        
        # Show function information
        func_name = getattr(func, '__qualname__', func.__name__)
        module_name = getattr(func, '__module__', 'unknownModule')
        lines.append(f"Function call: {module_name}.{func_name}")
        
        # Show argument information
        if self.show_args:
            try:
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                lines.append(f"Argument mapping: {dict(bound_args.arguments)}")
            except Exception as e:
                lines.append(f"Argument parsing failed: {e}")
                lines.append(f"Positional args: {args}")
                lines.append(f"Keyword args: {kwargs}")
        
        # Show call stack
        if self.show_traceback:
            lines.append(self._format_traceback())
        
        return ", ".join(lines)
    
    def _format_function_return(self, func: FunctionType, result: Any) -> str:
        """Format function return information"""
        func_name = getattr(func, '__qualname__', func.__name__)
        lines = [f"Function return: {func_name} -> {result}"]
        return " ".join(lines)

    def _format_function_error(self, func: FunctionType, error: Exception) -> str:
        """Format function error information"""
        func_name = getattr(func, '__qualname__', func.__name__)
        lines = [f"Function exception: {func_name} -> {error}"]
        
        if self.show_traceback:
            # Show full exception stack
            lines.append("Exception stack:")
            tb_lines = traceback.format_exception(type(error), error, error.__traceback__)
            # Filter out hook tool's own stack
            filtered_tb = []
            for line in tb_lines:
                if 'hook_tool' not in line:
                    filtered_tb.append(line)
            lines.extend(filtered_tb)
        
        return "\n".join(lines)
    
    def _print(self, message: str) -> None:
        """Print log information"""
        message = f"{self.prefix}[hook] {message}"
        DEBUG_MSG(message)

    def hook_function(self, func: FunctionType) -> FunctionType:
        """Hook a single function"""
        if func in self.hooked_functions:
            return func
            
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Print call information
            self._print(self._format_function_call(func, args, kwargs))
            
            # Call the original function
            try:
                result = func(*args, **kwargs)
                if self.show_return:
                    self._print(self._format_function_return(func, result))
                return result
            except Exception as e:
                if self.show_errors:
                    self._print(self._format_function_error(func, e))
                raise
        
        self.hooked_functions.add(func)
        return wrapper
    
    def hook_method(self, cls: type, method_name: str) -> None:
        """Hook the specified method of the specified class"""
        if (cls, method_name) in self.hooked_methods:
            if self.verbose:
                self._print(f"Method {cls.__name__}.{method_name} is already hooked, skipping")
            return
        
        if not hasattr(cls, method_name):
            if self.verbose:
                self._print(f"Warning: Class {cls.__name__} has no method {method_name}")
            return
        
        method = getattr(cls, method_name)
        if not inspect.isfunction(method) and not inspect.ismethod(method):
            if self.verbose:
                self._print(f"Warning: {cls.__name__}.{method_name} is not a hookable method")
            return
        
        # Hook method
        hooked_method = self.hook_function(method)
        setattr(cls, method_name, hooked_method)
        self.hooked_methods.add((cls, method_name))
        
        if self.verbose:
            self._print(f"Hooked method: {cls.__name__}.{method_name}")
    
    def hook_class(self, cls: type, method_filter: Optional[Callable[[str], bool]] = None) -> None:
        """Hook all methods of the specified class"""
        if cls in self.hooked_classes:
            if self.verbose:
                self._print(f"Class {cls.__name__} is already hooked, skipping")
            return
        
        if self.verbose:
            self._print(f"Hooking class: {cls.__name__}")
        
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # Skip magic methods (optional)
            if name.startswith('__') and name.endswith('__'):
                continue
            
            # Apply method filter
            if method_filter and not method_filter(name):
                continue
            
            self.hook_method(cls, name)
        
        self.hooked_classes.add(cls)
    
    def hook_module(self, module: ModuleType, 
                   class_filter: Optional[Callable[[str], bool]] = None,
                   method_filter: Optional[Callable[[str], bool]] = None) -> None:
        """Hook all classes and functions in the module"""
        if self.verbose:
            self._print(f"Hooking module: {module.__name__}")
        
        # Hook module-level functions
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and obj.__module__ == module.__name__:
                if self.verbose:
                    self._print(f"  Hooking function: {name}")
                setattr(module, name, self.hook_function(obj))
        
        # Hook classes
        for name, obj in inspect.getmembers(module, predicate=inspect.isclass):
            if obj.__module__ == module.__name__:
                # Apply class filter
                if class_filter and not class_filter(name):
                    continue
                
                self.hook_class(obj, method_filter)

def hook_specific_class_method(module_name: str, 
                              class_name: str, 
                              method_name: str,
                              **hook_options) -> bool:
    """
    Hook the specified method of the specified class in the module
    
    Args:
        module_name: Module name
        class_name: Class name
        method_name: Method name
        **hook_options: Hook options
        
    Returns:
        bool: Whether hook succeeded
    """
    try:
        # Get module

        module = sys.modules.get(module_name)
        if not module:
            module = importlib.import_module(module_name)
        
        # Get class
        if not hasattr(module, class_name):
            DEBUG_MSG(f"Hook Error: Class {class_name} not found in module {module_name}")
            return False
        
        cls = getattr(module, class_name)
        
        # Create Hooker and hook specified method
        hooker = FunctionHooker(**hook_options)
        hooker.hook_method(cls, method_name)
        
        DEBUG_MSG(f"Hook succeeded: {module_name}.{class_name}.{method_name}")
        return True
        
    except Exception as e:
        DEBUG_MSG(f"Hook failed: {e}")
        return False

def hook_specific_class(module_name: str, 
                       class_name: str,
                       method_filter: Optional[Callable[[str], bool]] = None,
                       **hook_options) -> bool:
    """
    Hook all methods of the specified class in the module
    
    Args:
        module_name: Module name
        class_name: Class name
        method_filter: Method filter function
        **hook_options: Hook options
        
    Returns:
        bool: Whether hook succeeded
    """
    try:
        # Get module
        module = sys.modules.get(module_name)
        if not module:
            module = importlib.import_module(module_name)

        # Get class
        if not hasattr(module, class_name):
            DEBUG_MSG(f"Error: Class {class_name} not found in module {module_name}")
            return False
        
        cls = getattr(module, class_name)
        
        # Create Hooker and hook class
        hooker = FunctionHooker(**hook_options)
        hooker.hook_class(cls, method_filter)

        DEBUG_MSG(f"Hook succeeded: {module_name}.{class_name}")
        return True
        
    except Exception as e:
        DEBUG_MSG(f"Hook failed: {e}")
        return False

def hook_specific_module(module_name: str, 
                         class_filter: Optional[Callable[[str], bool]] = None,
                         method_filter: Optional[Callable[[str], bool]] = None,
                         **hook_options) -> bool:
    """
    Hook all classes and functions in the specified module
    
    Args:
        module_name: Module name
        class_filter: Class filter function
        method_filter: Method filter function
        **hook_options: Hook options
        
    Returns:
        bool: Whether hook succeeded
    """
    try:
        # Get module
        module = sys.modules.get(module_name)
        if not module:
            module = importlib.import_module(module_name)
        
        # Create Hooker and hook module
        hooker = FunctionHooker(**hook_options)
        hooker.hook_module(module, class_filter, method_filter)

        DEBUG_MSG(f"Hook succeeded: {module_name}")
        return True
        
    except Exception as e:
        DEBUG_MSG(f"Hook failed: {e}")
        return False
    
"""
    hook_specific_class_method(
        "test_module.py",
        "Calculator",
        "add",
        show_traceback=True,
        traceback_depth=3,
        verbose=True
    )

"""