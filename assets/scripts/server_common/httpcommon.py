# -*- coding: utf-8 -*-


import KBEngine
from KBEDebug import *
import gameconfig
import utils
import hashlib
import urllib
import json
import uuid
import gameconfig
import gameconst

'''
常用http 接口
或者无处安放的 http接口...
'''


class AdultHttpErrCode(object):
    ADULT_OK = 1
    ADULT_NOT_ADULT = 2
    ADULT_HTTP_ERROR = 3
