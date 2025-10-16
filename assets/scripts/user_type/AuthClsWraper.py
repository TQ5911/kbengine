# coding: utf-8

import KBEngine
from functools import wraps, partial

def _make_validator(orig, name):
    """工厂函数：只捕获 orig 与 name，其余作用域立即销毁"""
    @wraps(orig)
    def _wrapper(self, *args, **kwargs):
        # ===== 统一校验逻辑 =====
        if abs(args[0]) != self.id:
            raise ValueError(f'exposed invalid : {args}')

        # ========================
        return orig(self, *args, **kwargs)
    return _wrapper


def authClsWraper(clsName):
    def _decorator(cls):
        for name in KBEngine.getExposedMethods(clsName):
            orig = getattr(cls, name)
            if not callable(orig):
                raise TypeError(f'{cls.__name__}.{name} 不是可调用方法')
            # 用工厂函数生成新函数，避免循环闭包
            setattr(cls, name, _make_validator(orig, name))
        return cls
    return _decorator


def onlyHost(fn):
    @wraps(fn)
    def __(self, exposed, *args, **kwargs):
        if not self.isHost(exposed):
            return

        return fn(self, exposed, *args, **kwargs)

    return __


def authWithPermission(permission):
    def _decorator(fn):
        @wraps(fn)
        def __(self, exposed, *args, **kwargs):
            if not self.isHost(exposed):
                if not self.hasAuthPermission(permission):
                    return

            return fn(self, exposed, *args, **kwargs)
        return __

    return _decorator
