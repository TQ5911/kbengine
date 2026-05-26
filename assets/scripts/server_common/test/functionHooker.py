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


CALL_FUNC_GET_PROP = "get_props"

class FunctionHooker:

    _instance = None
    
    def __init__(self, 
                 prefix: str = "",
                 show_traceback: bool = False,
                 traceback_depth: int = 5,
                 show_args: bool = True,
                 show_return: bool = True,
                 show_errors: bool = True,
                 show_variables: bool = True,
                 pre_call_func_type: Optional[str] = None,
                 post_call_func_type: Optional[str] = None,
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
        self.show_variables = show_variables
        self.pre_call_func_type = pre_call_func_type
        self.post_call_func_type = post_call_func_type
        self.verbose = verbose
        
        self.pre_call_map = {}
        self.post_call_map = {}
        self.hooked_functions: Set[FunctionType] = set()
        self.hooked_classes: Set[type] = set()
        self.hooked_methods: Set[tuple] = set()  # (class, method_name)
    
        # 预设一些函数调用
        def get_props(*args, **kwargs):
            self_props = {}
            target_props = {}
            if hasattr(args[0], 'getFightProps'):
                self_props = {k:v for k,v in args[0].getFightProps().items() if v != 0}
            if hasattr(args[1], 'getFightProps'):
                target_props = {k:v for k,v in args[1].getFightProps().items() if v != 0}
            return {'selfProps': self_props, 'targetProps': target_props}
        self.call_funcs = {
            CALL_FUNC_GET_PROP: get_props
        }

    # 一次性用，需要重置
    def reset_call_func_type(self):
        self.pre_call_func_type = None
        self.post_call_func_type = None

    @classmethod
    def get_instance(cls, **kwargs):
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        else:
            # 更新现有实例的参数
            for key, value in kwargs.items():
                if hasattr(cls._instance, key) and value is not None:
                    setattr(cls._instance, key, value)
        return cls._instance


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
        lines.append(f"Function call: {func_name}")
        
        # Show argument information
        if self.show_args:
            try:
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                args_str = str({k: str(v) for k,v in dict(bound_args.arguments).items()}) # 把自定义str的类都展开一下
                if len(args_str) > 1300: # 防止参数过长导致日志被截断
                    args_str = str(dict(bound_args.arguments))
                lines.append(f"Argument mapping: {args_str}")
            except Exception as e:
                lines.append(f"Argument parsing failed: {e}")
                lines.append(f"Positional args: {args}")
                lines.append(f"Keyword args: {kwargs}")
        
        # Show call stack
        if self.show_traceback:
            lines.append(self._format_traceback())
        
        return ", ".join(lines)
    
    def _format_function_other_call(self, func: FunctionType, func_type: str, ret: Any) -> str:
        """Format other function call information"""
        func_name = getattr(func, '__qualname__', func.__name__)
        return f"Function other call: {func_name}, {func_type}: {ret}"

    def _format_function_return(self, func: FunctionType, result: Any) -> str:
        """Format function return information"""
        func_name = getattr(func, '__qualname__', func.__name__)
        result_str = str(result)
        if isinstance(result, (list, set, tuple)):
            result_str = str([str(item) for item in result])
        elif isinstance(result, dict):
            result_str = str({k: str(v) for k,v in result.items()})
        if len(result_str) > 1300: # 防止返回值过长导致日志被截断
            result_str = str(result)
        result_str = f"Function return: {func_name}, {result_str}"
        return result_str

    def _format_function_variables(self, func: FunctionType, local_vars: Dict[str, Any]) -> str:
        """Format function local variables information"""
        func_name = getattr(func, '__qualname__', func.__name__)
        lines = [f"Function variables: {func_name}"]
        for var_name, var_value in local_vars.items():
            lines.append(f"{var_name}: {var_value}")
        return ", ".join(lines)

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
    
    def _print(self, message: str, args=None) -> None:
        """Print log information"""
        if not self.verbose:
            return
        if args and len(args) > 0:
            message = f"[{getattr(args[0], 'name', '')}]{self.prefix}[hook] {message}"
        else:
            message = f"{self.prefix}[hook] {message}"
        LOG_DBG(message)

    def hook_function(self, func: FunctionType) -> FunctionType:
        """Hook a single function"""
        func_name = getattr(func, '__qualname__', func.__name__)
        if func_name in self.hooked_functions:
            if self.verbose:
                self._print(f"Function {func_name} is already hooked, skipping")
            return func
        # 这两个逻辑要放在外面， 否则等到函数具体执行的时候再赋值，就被reset清掉了
        if self.pre_call_func_type and self.pre_call_func_type in self.call_funcs:
            self.pre_call_map[func_name] = self.pre_call_func_type

        if self.post_call_func_type and self.post_call_func_type in self.call_funcs:
            self.post_call_map[func_name] = self.post_call_func_type

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Print call information
            self._print(self._format_function_call(func, args, kwargs), args)
            captured_vars = {}
            old_trace = None
            if self.show_variables:
                # 获取函数源代码并解析AST
                import dis
                # 获取函数的字节码
                bytecode = dis.Bytecode(func)
                
                # 分析字节码，找出所有STORE_*操作的目标变量
                local_var_names = set()
                
                for instruction in bytecode:
                    # 查找存储操作 (STORE_FAST, STORE_NAME, STORE_DEREF等)
                    # if instruction.opname in ('STORE_FAST', 'STORE_NAME', 'STORE_DEREF'):
                    # STORE_FAST 操作的操作数是局部变量名
                    if instruction.opname == 'STORE_FAST':
                        local_var_names.add(instruction.argval)
                    # 对于其他存储操作，我们需要更复杂的分析
                # 定义跟踪函数以捕获局部变量
                def trace_func(frame, event, arg):
                    if event == 'return' and frame.f_code == func.__code__:
                        # 只捕获在函数内部定义的变量
                        for var_name in local_var_names:
                            if var_name in frame.f_locals:
                                captured_vars[var_name] = frame.f_locals[var_name]
                    return trace_func
                    # 设置跟踪函数
                old_trace = sys.gettrace()
                sys.settrace(trace_func)

            # Call the original function
            try:
                
                pre_call_func_type=  self.pre_call_map.get(func_name)
                if pre_call_func_type:
                    ret = self.call_funcs[pre_call_func_type](*args, **kwargs)
                    self._print(self._format_function_other_call(func, pre_call_func_type, ret), args)

                result = func(*args, **kwargs)
                
                post_call_func_type = self.post_call_map.get(func_name)
                if post_call_func_type:
                    ret = self.call_funcs[post_call_func_type](*args, **kwargs)
                    self._print(self._format_function_other_call(func, post_call_func_type, ret), args)

                # 变量要放return前输出，不然函数解析器那边无法匹配
                if self.show_variables:
                    self._print(self._format_function_variables(func, captured_vars.copy()), args)
                if self.show_return:
                    self._print(self._format_function_return(func, result), args)
            except Exception as e:
                if self.show_errors:
                    self._print(self._format_function_error(func, e), args)
                raise
            finally:
                if old_trace:
                    sys.settrace(old_trace)
            return result
        self.hooked_functions.add(func_name)
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
            LOG_DBG(f"Hook Error: Class {class_name} not found in module {module_name}")
            return False
        
        cls = getattr(module, class_name)
        
        # Create Hooker and hook specified method
        hooker = FunctionHooker.get_instance(**hook_options)
        hooker.hook_method(cls, method_name)
        hooker.reset_call_func_type()
        LOG_DBG(f"Hook succeeded: {module_name}.{class_name}.{method_name}")
        return True
        
    except Exception as e:
        LOG_DBG(f"Hook failed: {e}")
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
            LOG_DBG(f"Error: Class {class_name} not found in module {module_name}")
            return False
        
        cls = getattr(module, class_name)
        
        # Create Hooker and hook class
        hooker = FunctionHooker.get_instance(**hook_options)
        hooker.hook_class(cls, method_filter)
        hooker.reset_call_func_type()
        LOG_DBG(f"Hook succeeded: {module_name}.{class_name}")
        return True
        
    except Exception as e:
        LOG_DBG(f"Hook failed: {e}")
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
        hooker = FunctionHooker.get_instance(**hook_options)
        hooker.hook_module(module, class_filter, method_filter)
        hooker.reset_call_func_type()
        LOG_DBG(f"Hook succeeded: {module_name}")
        return True
        
    except Exception as e:
        LOG_DBG(f"Hook failed: {e}")
        return False

def hook_print_open(is_print: bool):
    hooker = FunctionHooker.get_instance()
    hooker.verbose = is_print
    LOG_DBG(f"Hook print is open: {is_print}")
    return True

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
