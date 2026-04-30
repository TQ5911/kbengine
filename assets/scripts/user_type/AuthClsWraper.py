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


def onlyHost(fn):
    @wraps(fn)
    def __(self, exposed, *args, **kwargs):
        if not self.isHostAccount(exposed):
            return

        return fn(self, exposed, *args, **kwargs)

    return __


def onlyMainChannel(fn):
    @wraps(fn)
    def __(self, exposed, *args, **kwargs):
        if exposed < 0:
            return

        return fn(self, exposed, *args, **kwargs)

    return __



def authWithPermission(permission):
    def _decorator(fn):
        @wraps(fn)
        def __(self, exposed, *args, **kwargs):
            if not self.isHostAccount(exposed):
                if not self.hasAuthPermission(permission):
                    return

            return fn(self, exposed, *args, **kwargs)
        return __

    return _decorator
