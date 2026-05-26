# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst

import userType


class ComplexTeleportOpt(userType.UserSingleType):
    def __init__(self,
                 beforeEnterFirst=False,
                 afterLeaveFirst=True,
                 teleportType=gameconst.ComplexTeleportEnum.UNKNOWN):
        """

        :param beforeEnterFirst:  场景切换前置 进入方法优先调用关系设置
        :param afterLeaveFirst:   场景切换后置 离开方法优先调用关系设置
        """
        self._beforeEnterFirst = beforeEnterFirst
        self._afterLeaveFirst = afterLeaveFirst
        self._teleportType = teleportType

    def __str__(self):
        return '{classname}(' \
               'beforeEnterFirst={beforeEnterFirst}, ' \
               'afterLeaveFirst={afterLeaveFirst}, ' \
               'teleportType={teleportType})'.format(
                    classname=self.__class__.__name__,
                    beforeEnterFirst=self._beforeEnterFirst,
                    afterLeaveFirst=self._afterLeaveFirst,
                    teleportType=self._teleportType)

    @property
    def beforeEnterFirst(self):
        return bool(self._beforeEnterFirst)

    @property
    def beforeLeaveFirst(self):
        return not bool(self._beforeEnterFirst)

    @property
    def afterEnterFirst(self):
        return not bool(self._afterLeaveFirst)

    @property
    def afterLeaveFirst(self):
        return bool(self._afterLeaveFirst)

    @property
    def teleportType(self):
        return self._teleportType
