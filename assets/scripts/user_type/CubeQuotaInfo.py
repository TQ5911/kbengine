
# coding: utf-8
from KBEDebug import *
import userType
import formula
import gameconfig
import gameconst
import utils
import LogTrackingMgr

import cube_room

class CubeQuotaVal(userType.UserSoleType):
    '''CUBE_QUOTA_DATA_INFO'''
    def __init__(self, leftTime=0, enterTime=0, cubeDurState=gameconst.CubeDurStatus.NORMAL):
        self.leftTime = leftTime
        self.enterTime = enterTime 
        # 这个时间可不是进入房间的时间，因为算经过多少时间需要靠于enterTime和leftTime的差值来计算
        # 但是如果enterTime一直不变的话，假设出现非法关服，会出现累计时间非常大的情况 
        self.cubeDurState = cubeDurState

    def __str__(self):
        return 'CubeQuotaVal(leftTime=%d, enterTime=%d, cubeDurState=%d)' % (self.leftTime, self.enterTime, self.cubeDurState)

    def toCubeQuotaSavedDict(self):
        return {
            'leftTime': self.leftTime,
            'enterTime': self.enterTime,
            'cubeDurState': self.cubeDurState
        }

    def calcLeftTime(self):
        """计算剩余时间, 不改变任何数据"""
        if self.cubeDurState == gameconst.CubeDurStatus.ENTER:
            _cost = utils.getNow() - self.enterTime
            return max(0, self.leftTime - _cost)

        return self.leftTime

    def refreshEnterTime(self):
        if self.cubeDurState != gameconst.CubeDurStatus.ENTER:
            return

        _now = utils.getNow()
        _cost = _now - self.enterTime
        self.leftTime = max(0, self.leftTime - _cost)
        self.enterTime = _now

    def setCubeEnterTime(self, avatar, enterTime):
        if self.cubeDurState == gameconst.CubeDurStatus.ENTER:
            ERROR_MSG('setCubeEnterTime error, cubeDurState is enter')

        self.enterTime = enterTime
        self.cubeDurState = gameconst.CubeDurStatus.ENTER
        avatar.client.onCubeRoomEndTime(self.calcLeftTime() + utils.getNow())

    def addLeftTime(self, avatar, delta):
        self.leftTime += delta

        self.refreshEnterTime()

        avatar.client.onCubeRoomEndTime(self.calcLeftTime() + utils.getNow())

        _mapId = formula.getMapId(avatar.spaceNo)
        _floor = cube_room.datas.get(_mapId, {}).get('floor', -1)
        LogTrackingMgr.LogTrackingMgr.Cube_Info(
            avatar.gbId,
            gameconfig.gameId(),
            _floor,
            _mapId,
            gameconst.CUBE_EVENT_ADD_TIME,
            self.calcLeftTime(),
        )

    def checkout(self):
        if self.cubeDurState != gameconst.CubeDurStatus.ENTER:
            ERROR_MSG('checkout error, cubeDurState is not enter')
            return

        _cost = utils.getNow() - self.enterTime
        self.leftTime = max(0, self.leftTime - _cost)
        self.enterTime = 0
        self.cubeDurState = gameconst.CubeDurStatus.NORMAL

    def resetOnLogin(self):
        # 走到这里说明出问题了，要不就是非法关服
        self.cubeDurState = gameconst.CubeDurStatus.NORMAL
        self.enterTime = 0


class CubeQuotaInfo(object):
    def createObjFromDict(self, dataDict):
        obj = CubeQuotaVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toCubeQuotaSavedDict()

    def isSameType(self, obj):
        return type(obj) is CubeQuotaVal


CubeQuotaInstance = CubeQuotaInfo()

