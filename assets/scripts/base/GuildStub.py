# coding: utf-8

import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gameconst
import gametimer
import gamesql
import userType
import utils
import functools
import GuildJoinCondInfo
import redisUtils
import gameglobal
import gameengine
import iCycleEvent
import dataUtils

import LogTrackingMgr
import guild_guildConst as G_GCD
import _pickle as cPickle

class GuildCacheVal(userType.UserSingleType):
    def __init__(self, guildUUID, guildName, desc, guildBox, memberCnt, guildLevel,
                 dspFlag, guildScore=0, icon=0, memberMax=0, joinCond=None, leagueUUID=0):
        self.guildName = guildName
        self.desc = desc
        self.guildUUID = guildUUID
        self.guildBox = guildBox
        self.memberCnt = memberCnt
        self.guildLevel = guildLevel
        self.dspFlag = dspFlag
        self.guildScore = guildScore
        self.icon = icon
        self.memberMax = memberMax
        self.joinCond = joinCond
        self.leagueUUID = leagueUUID

    def toGuildListData(self):
        return {
            'guildUUID': self.guildUUID,
            'guildName': self.guildName,
            'dspFlag': self.dspFlag,
            'memberCnt': self.memberCnt,
            'guildLevel': self.guildLevel,
            'guildScore': self.guildScore,
            'icon': self.icon,
            'memberMax': self.memberMax,
            'joinCond': self.joinCond,
        }


class GuildStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCycleEvent.ICycleEventMixin):
    def __init__(self):
        iCycleEvent.ICycleEventMixin.__init__(self)
        self.guildDic = {}
        self.addTimerCB(0.1, '_loadGuildEntity', (), gametimer.TIMER_TAG_LOAD_GUILD_ENTITY)
        utils.subscribe(gameconst.UserEventTag.EVENT_ON_GUILD_UNION_CHANGE, self, 'onGuildUnionChangeToLog')

        # 帮会佣金周结算
        self.registerWeekEvent('_commissionWeeklyCalc')
        self.onDailyEvent()
        
    def _loadGuildEntity(self):
        gamesql.loadAllGuildEntityInfo(self._onLoadGuildEntity)

    def _onLoadGuildEntity(self, ret, num, insertId, err):
        if err:
            LOG_ERR("GuildStub::_onLoadGuildEntity: %s" % err)
            return

        for _dbid, _guildUUID, _guildName, _desc in ret:
            _dbid = int(_dbid)
            _guildUUID = int(_guildUUID)
            _desc = utils.bytesToString(_desc)
            _guildName = utils.bytesToString(_guildName)

            _gcVal = GuildCacheVal(_guildUUID, _guildName, _desc, None, 0, 0, 0, joinCond=GuildJoinCondInfo.GuildJoinCondVal())
            self.guildDic[_guildUUID] = _gcVal
            KBEngine.createEntityAnywhereFromDBID(
                'Guild',
                _dbid,
                functools.partial(self._onCreateGuildFromLoad, _guildUUID)
            )

    def getGuildsGbIdAndBox(self, guildUUIDs, box, func, args):
        _guilds = []
        if guildUUIDs:
            for _guildUUID in guildUUIDs:
                _gcVal = self.guildDic.get(_guildUUID)
                if not _gcVal:
                    continue

                if utils.checkBoxOffline(_gcVal.guildBox):
                    continue

                _guilds.append({
                    'guildUUID': _gcVal.guildUUID,
                    'box': _gcVal.guildBox,
                })
        else:
            for _gcVal in self.guildDic.values():
                if utils.checkBoxOffline(_gcVal.guildBox):
                    continue

                _guilds.append({
                    'guildUUID': _gcVal.guildUUID,
                    'box': _gcVal.guildBox,
                })

        getattr(box, func)(_guilds, *args)

    def doGetGuildList(self, box):
        _sendData = [_gcVal.toGuildListData() for _gcVal in self.guildDic.values()]
        LOG_INFO("GuildStub::doGetGuildList:", _sendData)
        box.client.onGetGuildListData(_sendData)

    def _onCreateGuildFromLoad(self, guildUUID, guildBox, dbid, wasActive):
        LOG_INFO('_onCreateGuildFromLoad:', guildBox, dbid, wasActive, guildUUID)
        if wasActive:
            LOG_ERR("GuildStub::_onCreateGuildFromLoad: guildBox is active.", guildUUID)
            return

        if guildBox is None:
            LOG_ERR("GuildStub::_onCreateGuildFromLoad: guildBox is None.", guildUUID)
            return

        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            LOG_ERR("GuildStub::_onCreateGuildFromLoad: guildUUID not in guildDic.", guildUUID)
            return

        _gcVal.guildBox = guildBox

    def doNext(self):
        super().doNext()

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        else:
            self._onTimerTrigger(tid, userArg)

    def doCreateGuild(self, createData, gbId, box, ctx):
        gameglobal.localBaseApp.getRedisClient().sadd(
            gameconst.RedisKey.GUILD_NAME_TBL,
            [createData['guildName']],
            functools.partial(self._onAddGuildName, createData, gbId, box, ctx))

    def _onAddGuildName(self, createData, gbId, box, ctx, cid, err, result):
        if err or not result:
            box.onCreateGuildResult(gameconst.CreateGuildResult.NAME_DUPLICATE, ctx)
            return

        _guildUUID = KBEngine.genUUID64()
        _cnt = 0
        while _guildUUID in self.guildDic:
            _guildUUID = KBEngine.genUUID64()
            _cnt += 1
            if _cnt > 10:
                box.onCreateGuildResult(gameconst.CreateGuildResult.UUID_GEN_FAILED, ctx)
                return

        gamesql.addGuildAvatar(
            _guildUUID,
            gbId,
            lambda *args: self._createGuildAfterInsertAvatar(_guildUUID, gbId, createData, box, ctx, *args)
        )

    def _createGuildAfterInsertAvatar(self, _guildUUID, gbId, createData, leaderBox, ctx, ret, num, insertId, err):
        if err:
            redisUtils.SetUtils.srem(gameconst.RedisKey.GUILD_NAME_TBL, createData['guildName'])
            leaderBox.onCreateGuildResult(gameconst.CreateGuildResult.MAYBE_HAS_GUILD, ctx)
            return

        _props = {
            'guildName': createData['guildName'],
            'desc': createData['desc'],
            'publicDesc': createData['publicDesc'],
            'dspFlag': createData['dspFlag'],
            'guildUUID': _guildUUID,
            'joinCond': createData['joinCond'],
        }

        KBEngine.createEntityAnywhere(
            'Guild',
            _props,
            lambda guildBox: self._onCreateGuildBox(guildBox, createData, gbId, _guildUUID, leaderBox, ctx)
        )

    def updateGuildCache(self, guildUUID, data):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            return

        _gcVal.guildName = data['guildName']
        _gcVal.desc = data['desc']
        _gcVal.dspFlag = data['dspFlag']
        _gcVal.guildLevel = data['guildLevel']
        _gcVal.memberCnt = data['memberCnt']
        _gcVal.memberMax = data['memberMax']
        _gcVal.icon = data['icon']
        _gcVal.joinCond = data['joinCond']
        _gcVal.guildScore = data['guildScore']

    def getGuildsCacheData(self, guildUUIDs, box, func, args):
        _gcVals = []
        for _guildUUID in guildUUIDs:
            _gcVal = self.guildDic.get(_guildUUID)
            if not _gcVal:
                _gcVals.append({
                    'guildUUID': _guildUUID
                })
            else:
                _gcVals.append(_gcVal.toGuildListData())

        getattr(box, func)(_gcVals, *args)

    def _onCreateGuildBox(self, guildBox, createData, gbId, guildUUID, leaderBox, ctx):
        LOG_INFO("GuildStub::_onCreateGuildBox:", guildBox)
        if not guildBox:
            LOG_ERR("GuildStub::_onCreateGuildBox: create guild guildBox failed.", createData, gbId, guildUUID)
            redisUtils.SetUtils.srem(gameconst.RedisKey.GUILD_NAME_TBL, createData['guildName'])
            leaderBox.onCreateGuildResult(gameconst.CreateGuildResult.CREATE_GUILD_FAILED, ctx)
            return

        _gcVal = GuildCacheVal(
            guildUUID,
            createData['guildName'],
            createData['desc'],
            guildBox,
            1,
            1,
            createData['dspFlag'],
            joinCond=GuildJoinCondInfo.GuildJoinCondVal()
        )

        self.guildDic[guildUUID] = _gcVal
        guildBox.onFirstCreateGuild(gbId, leaderBox, ctx)

    def getGuildBox(self, box, guildUUID, func, args):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            getattr(box, func)(None, *args)
            return

        getattr(box, func)(_gcVal.guildBox, *args)

    def guildWillDestroy(self, guildUUID, guildBox):
        _gcVal = self.guildDic.pop(guildUUID, None)
        if _gcVal:
            redisUtils.SetUtils.srem(gameconst.RedisKey.GUILD_NAME_TBL, _gcVal.guildName)

        guildBox.onStubRemoveSelf()

    def broadcastToAllGuild(self, func, args):
        for _gcVal in self.guildDic.values():
            if utils.checkBoxOffline(_gcVal.guildBox):
                continue

            getattr(_gcVal.guildBox, func)(*args)

    def checkGuildNameValid(self, guildBox, avatarBox, ctx, oldName):
        gameglobal.localBaseApp.getRedisClient().sadd(
            gameconst.RedisKey.GUILD_NAME_TBL,
            [ctx['name']],
            functools.partial(self._onCheckGuildNameValid, guildBox, avatarBox, ctx, oldName)
        )

    def _onCheckGuildNameValid(self, guildBox, avatarBox, ctx, oldName, cid, err, result):
        if err or not result:
            avatarBox.onMessagePre(G_GCD.datas['guild_guildNameOccupied_msg']['value'], [])
            avatarBox.modifyGuildNameResult(False, ctx)
            return

        redisUtils.SetUtils.srem(gameconst.RedisKey.GUILD_NAME_TBL, oldName)
        guildBox.renameGuild(avatarBox, ctx)

    def callOnGuild(self, guildUUID, func, args, failedBox, failedFunc, failedArgs):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            if failedBox:
                getattr(failedBox, failedFunc)(*failedArgs)
            return

        getattr(_gcVal.guildBox, func)(*args)

    def broadcastGuildMemberClient(self, guildUUIDs, func, args):
        for _guildUUID in guildUUIDs:
            _gcVal = self.guildDic.get(_guildUUID)
            if not _gcVal:
                continue

            _gcVal.guildBox.broadcastMemberClient(func, args)

    def doOnCrossGuild(self, guildUUID, func, args, uuid, senderServerId):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            if uuid:
                gameengine.getGlobalBase('CrossDataStub').doOnCrossGuildBack(
                    uuid,
                    senderServerId,
                    False,
                    None,
                )
            return

        args = cPickle.loads(args)
        getattr(_gcVal.guildBox, func)(uuid, senderServerId, *args)

    def syncGuildMineWarToSpaceMgr(self, guildUUID, box, onRegister, extra):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            box.onSyncGuildMineWarResult(guildUUID, '', 0, 0, '', {}, onRegister, extra)
            return

        _gcVal.guildBox.getGuildMineWarForRegister(box, onRegister, extra)

    def onGuildUnionChangeToLog(self, changeType, guildUUID1, guildUUID2, relationType, endTime):
        if guildUUID1 not in self.guildDic:
            return

        if changeType == 'add':
            if relationType == gameconst.GuildRelationType.UNION:
                _opr = gameconst.GUILD_UNION_FORGE
            else:
                _opr = gameconst.GUILD_HOSTILE_DECLARE

        else:
            if relationType == gameconst.GuildRelationType.UNION:
                _opr = gameconst.GUILD_UNION_BREAK
            else:
                _opr = gameconst.GUILD_HOSTILE_CEASE

        LogTrackingMgr.LogTrackingMgr.Guild_Relation(
            'GuildStub',
            '', 
            guildUUID1,
            guildUUID2,
            _opr,
            endTime
        )

    def statGuildData(self, dataType):
        LOG_INFO("GuildStub::statGuildData:", self.guildStatData)

        currentPoints = dataUtils.getGuildGamePlayPoints(dataType)
        self.guildStatData[dataType] = self.guildStatData.get(dataType, 0) + currentPoints

        self.gamePlayScoreLimit += currentPoints

    def _commissionWeeklyCalc(self, *args):
        LOG_INFO("GuildStub::_commissionWeeklyCalc:", self.guildStatData)
        totalPoints = 0
        for point in self.guildStatData.values():
            totalPoints += point
        self.broadcastToAllGuild('commissionWeeklyCalc', (totalPoints,))
        self.guildStatData.clear()
        self.gamePlayScoreLimit = 0

    def doGetGamePlayScoreLimit(self, gbId, playerBox, guildBox):
        guildBox.doSendGuildClientData(gbId, playerBox, self.gamePlayScoreLimit)

    def doGetGuildGamePlayData(self, playerBox, guildBox):
        guildBox.doGetGuildGamePlayData(playerBox, self.gamePlayScoreLimit)

    def checkGuildExists(self, guildId, uniqueId, checkCD):
        LOG_INFO("GuildStub::checkGuildExists: ", guildId, uniqueId, checkCD)
        ret = False
        _gcVal = self.guildDic.get(guildId)
        if _gcVal:
           ret = True 
           _gcVal.guildBox.onCheckGuild(uniqueId, ret, checkCD)
        else:
            gameengine.getGlobalBase('AllianceStub').onCheckGuildResult(guildId, '', uniqueId, ret, 0, checkCD)