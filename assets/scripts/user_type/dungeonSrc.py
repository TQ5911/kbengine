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
        self.srcId = extra.pop('srcId', gameconst.DungeonSrcEnum.DEFAULT)   # 来源ID
        self._extra = extra                              # 其他属性

    def __str__(self):
        extra = ', '.join(['{}={}'.format(k, v) for k, v in self._extra.items()])
        return '{0}[{1}]({2})'.format(self.__class__.__name__, self.srcId, extra)

    def __repr__(self):
        return self.__str__()


class KickoutFromDungeon(BasicDungeonSrc):
    """被副本踢出下线"""

    def __init__(self, kickReason=gameconst.DungeonSrcKickReason.DEFAULT):
        super().__init__(
            srcId=gameconst.DungeonSrcEnum.FROM_KICKOUT_DUNGEON,
            kickReason=kickReason)

    @property
    def kickReason(self):
        return self._extra['kickReason']


class DungeonFromClientSrc(BasicDungeonSrc):
    """副本调用来源是客户端"""

    def __init__(self, playerBox, playerGBID):
        super(DungeonFromClientSrc, self).__init__(
            srcId=gameconst.DungeonSrcEnum.FROM_CLIENT,
            playerBox=playerBox,
            playerGBID=playerGBID)

    @property
    def playerBox(self):
        return self._extra['playerBox']

    @property
    def playerGBID(self):
        return self._extra['playerGBID']


class DungeonFromClientGMSrc(DungeonFromClientSrc):
    """GM指定调用"""
    def __init__(self, *args, **kwargs):
        super(DungeonFromClientGMSrc, self).__init__(*args, **kwargs)
        self.srcId = gameconst.DungeonSrcEnum.FROM_CLIENT_GM


class EnterGuildFromTeamCaptainSrc(BasicDungeonSrc):
    """跟随队长进帮会"""

    def __init__(self, *args, **kwargs):
        super(EnterGuildFromTeamCaptainSrc, self).__init__(*args, **kwargs)
        self.srcId = gameconst.DungeonSrcEnum.FROM_FOLLOW_CAPTAIN_ENTER_GUILD


class DungeonFromFlowController(BasicDungeonSrc):
    """副本流程控制节点"""

    def __init__(self, playerBox, playerGBID):
        super(DungeonFromFlowController, self).__init__(
            srcId=gameconst.DungeonSrcEnum.FROM_FLOW_CONTROLLER,
            playerBox=playerBox,
            playerGBID=playerGBID)

    @property
    def playerBox(self):
        return self._extra['playerBox']

    @property
    def playerGBID(self):
        return self._extra['playerGBID']
