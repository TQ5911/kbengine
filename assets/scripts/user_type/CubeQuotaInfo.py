
# coding: utf-8
from KBEDebug import *
import userType
import formula
import gameconfig
import gameconst
import utils
import LogTrackingMgr

import cube_room

class CubeQuotaVal(userType.UserSingleType):
    '''CUBE_QUOTA_DATA_INFO'''
    # 混沌回廊试炼峰共用同一个数据结构
    def __init__(self, leftTime=0, enterTime=0, quotaDurState=gameconst.QuotaDurStatus.NORMAL):
        self.leftTime = leftTime
        self.enterTime = enterTime 
        # 这个时间可不是进入房间的时间，因为算经过多少时间需要靠于enterTime和leftTime的差值来计算
        # 但是如果enterTime一直不变的话，假设出现非法关服，会出现累计时间非常大的情况 
        self.quotaDurState = quotaDurState

    def __str__(self):
        return 'CubeQuotaVal(leftTime=%d, enterTime=%d, quotaDurState=%d)' % (self.leftTime, self.enterTime, self.quotaDurState)

    def toCubeQuotaSavedDict(self):
        return {
            'leftTime': self.leftTime,
            'enterTime': self.enterTime,
            'quotaDurState': self.quotaDurState
        }

    def calcLeftTime(self):
        """计算剩余时间, 不改变任何数据"""
        if self.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            _cost = utils.curTS() - self.enterTime
            return max(0, self.leftTime - _cost)

        return self.leftTime

    def refreshEnterTime(self):
        if self.quotaDurState != gameconst.QuotaDurStatus.ENTER:
            return

        _now = utils.curTS()
        _cost = _now - self.enterTime
        self.leftTime = max(0, self.leftTime - _cost)
        self.enterTime = _now

    def setCubeEnterTime(self, avatar, enterTime):
        """cube"""
        LOG_DBG('setCubeEnterTime from ', self.quotaDurState)
        if self.quotaDurState != gameconst.QuotaDurStatus.PROTECT:
            LOG_ERR('setCubeEnterTime error, quotaDurState is enter')

        self.enterTime = enterTime
        self.quotaDurState = gameconst.QuotaDurStatus.ENTER
        avatar.client.onCubeRoomEndTime(self.calcLeftTime() + utils.curTS(), gameconst.CubeRoomEndTimeReason.ENTER)

    def setWonderLandEnterTime(self, avatar, enterTime):
        """wonderLand"""
        if self.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('setCubeEnterTime error, quotaDurState is enter')

        self.enterTime = enterTime
        self.quotaDurState = gameconst.QuotaDurStatus.ENTER
        avatar.client.onWonderLandLeftTime(self.calcLeftTime() + utils.curTS())

    def setAbyssEnterTime(self, avatar, enterTime):
        """abyss"""
        if self.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('setCubeEnterTime error, quotaDurState is enter')

        self.enterTime = enterTime
        self.quotaDurState = gameconst.QuotaDurStatus.ENTER
        avatar.client.onAbyssLeftTime(self.calcLeftTime() + utils.curTS())
    
    #跨服同步归墟剩余时间
    def onCrossServerSyncAbyssData(self, leftTime, enterTime):
        self.leftTime = leftTime
        self.enterTime = enterTime

    def addWonderLandLeftTime(self, avatar, delta):
        """wonderLand"""
        self.leftTime += delta
        self.refreshEnterTime()

        avatar.client.onWonderLandLeftTime(self.calcLeftTime() + utils.curTS())

        _mapId = formula.fetchMapId(avatar.spaceNo)
        _floor = cube_room.datas.get(_mapId, {}).get('floor', -1)
        LogTrackingMgr.LogTrackingMgr.Wonderland_Info(
            avatar.gbId,
            avatar.clientDistinctIdCell,
            avatar.gbId,
            gameconfig.gameId(),
            _floor,
            gameconst.WONDER_LAND_EVENT_ADDTIME,
            self.calcLeftTime(),
        )

    def addCubeLeftTime(self, avatar, delta):
        """cube"""
        self.leftTime += delta
        self.refreshEnterTime()

        avatar.client.onCubeRoomEndTime(self.calcLeftTime() + utils.curTS(), gameconst.CubeRoomEndTimeReason.ADD_TIME)

        _mapId = formula.fetchMapId(avatar.spaceNo)
        _floor = cube_room.datas.get(_mapId, {}).get('floor', -1)
        LogTrackingMgr.LogTrackingMgr.Cube_Info(
            avatar.gbId,
            avatar.clientDistinctIdCell,
            avatar.gbId,
            gameconfig.gameId(),
            _floor,
            _mapId,
            gameconst.CUBE_EVENT_ADD_TIME,
            self.calcLeftTime(),
        )

    def addAbyssLeftTime(self, avatar, delta):
        LOG_INFO('addAbyssLeftTime: delta: {}'.format(delta))
        """abyss"""
        self.leftTime += delta
        self.refreshEnterTime()

        avatar.client.onAbyssLeftTime(self.calcLeftTime() + utils.curTS())

        _mapId = formula.fetchMapId(avatar.spaceNo)
        _floor = cube_room.datas.get(_mapId, {}).get('floor', -1)
        # TODO abyss
        # LogTrackingMgr.LogTrackingMgr.Abyss_Info(
            # avatar.gbId,
            # avatar.clientDistinctIdCell,
        #     avatar.gbId,
        #     gameconfig.gameId(),
        #     _floor,
        #     gameconst.ABYSS_EVENT_ADDTIME,
        #     self.calcLeftTime(),
        # )

    def changeProtect(self):
        LOG_DBG('changeProtect from ', self.quotaDurState)
        if self.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            self.checkout()
            self.quotaDurState = gameconst.QuotaDurStatus.PROTECT

        elif self.quotaDurState == gameconst.QuotaDurStatus.PROTECT:
            pass

        else:
            self.quotaDurState = gameconst.QuotaDurStatus.PROTECT

    def checkout(self):
        LOG_DBG('checkout from ', self.quotaDurState)
        if self.quotaDurState == gameconst.QuotaDurStatus.PROTECT:
            self.quotaDurState = gameconst.QuotaDurStatus.NORMAL
            return

        elif self.quotaDurState == gameconst.QuotaDurStatus.NORMAL:
            return

        _cost = utils.curTS() - self.enterTime
        self.leftTime = max(0, self.leftTime - _cost)
        self.enterTime = 0
        self.quotaDurState = gameconst.QuotaDurStatus.NORMAL

    def reset(self):
        self.checkout()
        self.leftTime = 0
        self.enterTime = 0
        self.quotaDurState = gameconst.QuotaDurStatus.NORMAL

    def resetOnLogin(self):
        # 走到这里说明出问题了，要不就是非法关服
        self.quotaDurState = gameconst.QuotaDurStatus.NORMAL
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

