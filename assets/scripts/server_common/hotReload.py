# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
import types

def hotpatch_method(cls, method_name, new_func):
    """
    安全热更类的方法，保持堆栈清晰
    """
    # 绑定为实例方法（避免变成静态方法）
    setattr(cls, method_name, types.MethodType(new_func, cls))

def refreshCell():
    # --auto genterate mark--
    pass


def refreshBase():
    # --auto genterate mark--
    pass


def refreshInterface():
    # --auto genterate mark--
    pass
