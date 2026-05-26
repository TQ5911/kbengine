# -*- coding: utf-8 -*-
import traceback
import random
import heapq


class UserTypeBase(object):
    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def _checkIgnores_(cls):
        return ()


class UserSingleType(UserTypeBase):
    def reloadScript(self):
        import utils
        utils.resetClass(self)
        self._lateReload()

    def _lateReload(self):
        return

    def classname(self):
        return self.__class__.__name__


class UserListType(list, UserTypeBase):
    def reloadScript(self):
        import utils
        utils.resetClass(self)
        self._lateReload()

    def _lateReload(self):
        pass

    def __str__(self):
        _s = str(self.__class__.__name__) + " "
        _s + str(vars(self)) + "&&&&[["

        for l in self:
            _s += ',,' + str(l)

        _s += "]]"
        return _s


class UserDictType(dict, UserTypeBase):
    def reloadScript(self):
        import utils
        utils.resetClass(self)
        self._lateReload()

    def _lateReload(self):
        pass

    def __str__(self):
        _s = str(vars(self)) + "&&&&{{"

        for key, value in self.items():
            _s += str(key) + '::' + str(value) + '\n'

        _s += "}}"
        return _s

    def __bool__(self):
        return True


class ABCInfo(object):
    def createObjFromDict(self, dict):
        raise NotImplementedError
        return

    def getDictFromObj(self, obj):
        raise NotImplementedError
        return

    def isSameType(self, obj):
        raise NotImplementedError
        return


class UserSTSoleType(UserSingleType):

    def initFromDict(self, dataDic):
        raise NotImplementedError
        return

    def toSavedDict(self):
        raise NotImplementedError
        return


class UserSTSoleInfo(ABCInfo):

    @property
    def cls(self):
        raise NotImplementedError
        return

    def createObjFromDict(self, dic):
        _obj = self.cls()
        return _obj.initFromDict(dic)

    def getDictFromObj(self, objec: UserSTSoleType):
        return objec.toSavedDict()

    def isSameType(self, objec):
        return type(objec) == self.cls


class Error(UserSingleType, BaseException):
    def __init__(self, errno, errbody=None, errmsg=''):
        self.errbody = errbody
        self.errno = errno
        self.errmsg = errmsg
        self._basic = True  # basic error flag
        self.errtrace = ''
        BaseException.__init__(self, errmsg)

    @property
    def basic(self):
        return self._basic

    @basic.setter
    def basic(self, newVal):
        self._basic = bool(newVal)

    def __call__(self, **errargs):
        if self._basic:
            raise TypeError('Error basic obj does not support call')

        if 'errmsg' in errargs:
            self.errmsg = errargs['errmsg']

        if 'errbody' in errargs:
            self.errbody = errargs['errbody']

        self.errtrace = ''.join(traceback.format_stack(limit=5))
        return self

    def initkvbody(self, **kwargs):
        if self._basic:
            newSelf = Error(self.errno, self.errbody, self.errmsg) 
        else:
            newSelf = self

        if not isinstance(newSelf.errbody, dict):
            newSelf.errbody = {}

        newSelf.errbody.update(kwargs)
        newSelf._basic = False
        return newSelf

    def __format__(self, formatstr):
        return '{}(errno=[{}], errbody=[{}], errmsg="{}")'.format(
            self.__class__.__name__, self.errno, self.errbody, self.errmsg)

    def __repr__(self):
        return str(self.errno)

    def __eq__(self, o):
        return self.errno == o

    def __ne__(self, o):
        return self.errno != o

    def __lt__(self, o):
        return self.errno < o

    def __gt__(self, o):
        return self.errno > o

    def __le__(self, o):
        return self.errno <= o

    def __ge__(self, o):
        return self.errno >= o


