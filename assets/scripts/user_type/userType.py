# -*- coding: utf-8 -*-
import traceback
import random
import copy
import heapq


class UserType(object):
    def __str__(self):
        return str(vars(self))

    @classmethod
    def _checkIgnores_(cls):
        return ()


class UserSoleType(UserType):
    def reloadScript(self):
        import utils
        utils.resetCls(self)

        self._lateReload()
        return

    def _lateReload(self):
        return


class UserListType(list, UserType):
    def reloadScript(self):
        import utils
        utils.resetCls(self)

        self._lateReload()
        return

    def _lateReload(self):
        return

    def __str__(self):
        s = str(self.__class__.__name__) + " "
        s + str(vars(self)) + "&&&&[["

        for l in self:
            s += ',,' + str(l)

        s += "]]"
        return s


class UserDictType(dict, UserType):
    def reloadScript(self):
        import utils
        utils.resetCls(self)

        self._lateReload()

        return

    def _lateReload(self):
        return

    def __str__(self):
        s = str(vars(self)) + "&&&&{{"

        for key, value in self.items():
            s += str(key) + '::' + str(value) + '\n'

        s += "}}"
        return s

    def __bool__(self):
        return True


class UserDefinedType(UserType):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class SampleDict(dict, UserType):
    def __init__(self, *arga, **kwargs):
        super(SampleDict, self).__init__(*arga, **kwargs)
        self.keylist = list(self.keys())

    def __setitem__(self, key, value):
        if key not in self:
            self.keylist.append(key)
        super(SampleDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(SampleDict, self).__delitem__(key)
        self.keylist.remove(key)

    def pop(self, key, *args):
        super(SampleDict, self).pop(key, *args)
        self.keylist.remove(key)

    def update(self, m, **kwargs):
        for k in m.keys():
            if k not in self:
                self.keylist.append(k)
        super(SampleDict, self).update(m, **kwargs)

    def setdefault(self, key, default):
        if key not in self:
            self.keylist.append(key)
        super(SampleDict, self).setdefault(key, default)

    def popitem(self):
        key, v = super(SampleDict, self).popitem()
        self.keylist.remove(key)

    def clear(self):
        super(SampleDict, self).clear()
        self.keylist = []

    def sample(self, count):
        if count >= len(self.keylist):
            chose = list(self.keylist)
        else:
            chose = random.sample(self.keylist, count)
        return chose

    def reloadScript(self):
        import utils
        utils.resetCls(self)

        self._lateReload()

        return

    def _lateReload(self):
        return


class ABCInfo(object):
    def createObjFromDict(self, dict):
        raise NotImplementedError

    def getDictFromObj(self, obj):
        raise NotImplementedError

    def isSameType(self, obj):
        raise NotImplementedError


class UserSTDSoleType(UserSoleType):

    def initFromDict(self, dataDic):
        raise NotImplementedError

    def toSavedDict(self):
        raise NotImplementedError


class UserSTDSoleInfo(ABCInfo):

    @property
    def cls(self):
        raise NotImplementedError

    def createObjFromDict(self, dic):
        obj = self.cls()
        return obj.initFromDict(dic)

    def getDictFromObj(self, obj: UserSTDSoleType):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) == self.cls


class Error(UserSoleType, BaseException):
    def __init__(self, errno, errbody=None, errmsg=''):
        self.errno = errno
        self.errbody = errbody
        self.errmsg = errmsg
        self.errtrace = ''
        self._basic = True  # basic error flag
        BaseException.__init__(self, errmsg)

    @property
    def basic(self):
        return self._basic

    @basic.setter
    def basic(self, newBasic):
        self._basic = bool(newBasic)

    def __call__(self, **errargs):
        if self._basic:
            raise TypeError('Error basic obj does not support call')
        if 'errbody' in errargs:
            self.errbody = errargs['errbody']
        if 'errmsg' in errargs:
            self.errmsg = errargs['errmsg']
        self.errtrace = ''.join(traceback.format_stack(limit=5))
        return self

    def initkvbody(self, **kw):
        newSelf = Error(self.errno, self.errbody, self.errmsg) if self._basic else self
        if not isinstance(newSelf.errbody, dict):
            newSelf.errbody = {}
        newSelf.errbody.update(kw)
        newSelf._basic = False
        return newSelf

    def __repr__(self):
        return str(self.errno)

    def __format__(self, formatstr):
        return '{}(errno={}, errbody={}, errmsg="{}")'.format(
            self.__class__.__name__, self.errno, self.errbody, self.errmsg)

    def __eq__(self, other):
        return self.errno == other

    def __ne__(self, other):
        return self.errno != other

    def __lt__(self, other):
        return self.errno < other

    def __gt__(self, other):
        return self.errno > other

    def __le__(self, other):
        return self.errno <= other

    def __ge__(self, other):
        return self.errno >= other


class UserPriQueueTypeIterator(object):
    def __init__(self, queue):
        self._queue = queue
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self._queue):
            obj = self._queue[self.index]
            self.index += 1
            if obj.key:
                return obj

        raise StopIteration

class UserPriQueueType(UserSoleType):
    def __init__(self, maxCount, popCallBack=None):
        super(UserPriQueueType, self).__init__()

        self._finders = {}
        self._priorityQueue = []
        self._maxCount = maxCount
        self._popCallBack = popCallBack

    def __iter__(self):
        return UserPriQueueTypeIterator(heapq.nsmallest(len(self._priorityQueue), self._priorityQueue))

    def __len__(self):
        return len(self._finders)

    def isEmpty(self):
        return not self._finders

    def priRemoveObj(self, key):
        obj = self._finders.pop(key, None)
        if obj:
            obj.key = 0

    def getSmallest(self):
        if not self._finders:
            return None

        while self._priorityQueue:
            obj = heapq.nsmallest(1, self._priorityQueue)[0]
            if obj.key:
                return obj

            heapq.heappop(self._priorityQueue)

    def priGet(self, key):
        return self._finders.get(key)

    def priPush(self, obj):
        if obj.key == 0:
            import gameengine
            gameengine.reportCritical('priPush but key invalid')
            return

        if obj.key in self._finders:
            self.priRemoveObj(obj.key)

        heapq.heappush(self._priorityQueue, obj)
        self._finders[obj.key] = obj
        if len(self._finders) > self._maxCount:
            self.priPop()

    def priPop(self):
        while self._priorityQueue:
            obj = heapq.heappop(self._priorityQueue)
            if obj.key != 0:
                del self._finders[obj.key]
                if self._popCallBack:
                    self._popCallBack(obj.key)

                return obj

        return None

    def getAllPriQueVal(self):
        return self._finders.values()

    def _lateReload(self):
        super(UserPriQueueType, self)._lateReload()
        for pqVal in self._priorityQueue:
            pqVal.reloadScript()


