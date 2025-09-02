# coding: utf-8

from KBEDebug import *

import sStack


class AIControllerPool(object):
    def __init__(self, defaultPoolSize=64, controllerType=None):
        self._defaultPoolSize = defaultPoolSize
        self._bufferedPoolSize = self._defaultPoolSize * 2
        self._pools = sStack.SStackMgr()
        self._polType = controllerType or object

    def pushAIController(self, key, controller, callFunc: str=None):
        if not isinstance(controller, self._polType):
            WARNING_MSG('Drop controller because controller type not match, '
                        'need {}, got {}'.format(self._polType.__name__,
                                                 controller.__class__.__name__)
                        )
            return

        if key not in self._pools:
            pool = self._pools.createStack(key, [],
                                           maximum=self._defaultPoolSize)
        else:
            pool = self._pools[key]

        if pool.is_full():
            _exSize = self._defaultPoolSize / 2
            r = self._extendPoolSize(pool, _exSize)

            if not r:
                DEBUG_MSG('AI Pool "{}" is full, '
                          'drop income Object'.format(key))
                return
            else:
                INFO_MSG('AI pool "{}" extend size: {}'.format(key, _exSize))

        if callFunc:
            getattr(controller, callFunc, lambda _: None)()

        pool.push(controller)

    def popAIController(self, key, callFunc: str=None):
        pool = self._pools.getStack(key)

        if pool:
            crl = pool.pop()

            if callFunc:
                getattr(crl, callFunc, lambda _: None)()

            return crl
        else:
            DEBUG_MSG('AI Pool "{}" is empty or not exist, '
                      'nothing to pop'.format(key))

    def clearAllPool(self):
        self._pools.clear()

    def _extendPoolSize(self, pool: sStack.SStack, extendSize):
        if pool.depth >= self._bufferedPoolSize:
            return False

        pool.resize(pool.maximum + extendSize)
        return True


# set default controller pool
aiControllerPool = pool = AIControllerPool(defaultPoolSize=128)
