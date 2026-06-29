# coding: utf-8
"""
     副本来源临时结构
"""
from KBEDebug import *
import KBEngine

import functools

import gameconst

import userType


class BasicDungeonSrc(userType.UserSingleType):
    """副本来源基类"""

    def __init__(self, **extra):
        self.srcId = extra.pop('srcId', gameconst.DunSrcEnum.DEFAULT)   # 来源ID
        self._extra = extra                              # 其他属性

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        _extra = ', '.join(['{}={}'.format(_k, v) for _k, v in self._extra.items()])
        return '{0}[{1}]({2})'.format(self.__class__.__name__, self.srcId, _extra)


class KickoutFromDungeon(BasicDungeonSrc):
    """被副本踢出下线"""

    def __init__(self, kickReason=gameconst.DungeonSrcKickReason.DEFAULT, **kwargs):
        super().__init__(
            srcId=gameconst.DunSrcEnum.FROM_KICKOUT_DUNGEON,
            kickReason=kickReason)

    @property
    def kickReason(self):
        return self._extra['kickReason']


class DungeonFromClientSrc(BasicDungeonSrc):
    """副本调用来源是客户端"""

    def __init__(self, playerBox, playerGBID, **kwargs):
        super(DungeonFromClientSrc, self).__init__(
            srcId=gameconst.DunSrcEnum.FROM_CLIENT,
            playerBox=playerBox,
            playerGBID=playerGBID,
        )

    @property
    def playerGBID(self):
        return self._extra['playerGBID']

    @property
    def playerBox(self):
        return self._extra['playerBox']


class DungeonFromClientGMSrc(DungeonFromClientSrc):
    """GM指定调用"""
    def __init__(self, *args, **keywardargs):
        super(DungeonFromClientGMSrc, self).__init__(*args, **keywardargs)
        self.srcId = gameconst.DunSrcEnum.FROM_CLIENT_GM



class DungeonFromFlowController(BasicDungeonSrc):
    """副本流程控制节点"""

    def __init__(self, playerBox, playerGBID):
        super(DungeonFromFlowController, self).__init__(
            srcId=gameconst.DunSrcEnum.FROM_FLOW_CONTROLLER,
            playerBox=playerBox,
            playerGBID=playerGBID)

    @property
    def playerGBID(self):
        return self._extra['playerGBID']

    @property
    def playerBox(self):
        return self._extra['playerBox']

