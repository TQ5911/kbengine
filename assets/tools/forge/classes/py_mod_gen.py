import os
from common import utils

TEMP = """
# coding: utf-8

import userType


class {0}Val(userType.UserSoleType):
    '''{1}_DATA_INFO'''
    def __init__(self):
        pass

    def to{0}SavedDict(self):
        return {{
        }}


class {0}Info(object):
    def createObjFromDict(self, dataDict):
        obj = {0}Val(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.to{0}SavedDict()

    def isSameType(self, obj):
        return type(obj) is {0}Val


{0}Instance = {0}Info()

"""


class PyModGen(object):
    def __init__(self, mod_name):
        self.mod_name = mod_name

    def get_py_mod_path(self, mod_name):
        _mod_name = mod_name + 'Info.py'
        return os.path.join(os.environ['KBE_ASSETS'], 'scripts', 'user_type', _mod_name)

    def gen(self):
        _mod_path = self.get_py_mod_path(self.mod_name)
        with open(_mod_path, 'w') as _f:
            _data = TEMP.format(self.mod_name, utils.get_upper_name(self.mod_name))
            _f.write(_data)


