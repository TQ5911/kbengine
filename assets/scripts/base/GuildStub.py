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
import guild_guildConst as G_GCD
import _pickle as cPickle


class GuildCacheVal(userType.UserSoleType):
    def __init__(self, guildUUID, guildName, desc, guildBox, memberCnt, guildLevel,
                 dspFlag, guildScore=0, icon=0, memberMax=0, joinCond=None):
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


class GuildStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        self.guildDic = {}
        self._callback(0.1, '_loadGuildEntity', (), gametimer.TIMER_TAG_LOAD_GUILD_ENTITY)

    def _loadGuildEntity(self):
        gamesql.loadAllGuildEntityInfo(self._onLoadGuildEntity)

    def _onLoadGuildEntity(self, ret, num, insertId, err):
        if err:
            ERROR_MSG("GuildStub::_onLoadGuildEntity: %s" % err)
            return

        for _dbid, _guildUUID, _guildName, _desc in ret:
            _dbid = int(_dbid)
            _guildUUID = int(_guildUUID)
            _desc = utils.getStringFromBytes(_desc)
            _guildName = utils.getStringFromBytes(_guildName)

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

                if utils.isBoxOffline(_gcVal.guildBox):
                    continue

                _guilds.append({
                    'guildUUID': _gcVal.guildUUID,
                    'box': _gcVal.guildBox,
                })
        else:
            for _gcVal in self.guildDic.values():
                if utils.isBoxOffline(_gcVal.guildBox):
                    continue

                _guilds.append({
                    'guildUUID': _gcVal.guildUUID,
                    'box': _gcVal.guildBox,
                })

        getattr(box, func)(_guilds, *args)

    def doGetGuildList(self, box):
        _sendData = [_gcVal.toGuildListData() for _gcVal in self.guildDic.values()]
        DEBUG_MSG("GuildStub::doGetGuildList:", _sendData)
        box.client.onGetGuildListData(_sendData)

    def _onCreateGuildFromLoad(self, guildUUID, guildBox, dbid, wasActive):
        DEBUG_MSG('_onCreateGuildFromLoad:', guildBox, dbid, wasActive, guildUUID)
        if wasActive:
            ERROR_MSG("GuildStub::_onCreateGuildFromLoad: guildBox is active.", guildUUID)
            return

        if guildBox is None:
            ERROR_MSG("GuildStub::_onCreateGuildFromLoad: guildBox is None.", guildUUID)
            return

        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            ERROR_MSG("GuildStub::_onCreateGuildFromLoad: guildUUID not in guildDic.", guildUUID)
            return

        _gcVal.guildBox = guildBox

    def doNext(self):
        super().doNext()

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            self._onTimer(tid, userArg)

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
        DEBUG_MSG("GuildStub::_onCreateGuildBox:", guildBox)
        if not guildBox:
            ERROR_MSG("GuildStub::_onCreateGuildBox: create guild guildBox failed.", createData, gbId, guildUUID)
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
            if utils.isBoxOffline(_gcVal.guildBox):
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

    def syncGuildMineWarToSpaceMgr(self, guildUUID, box, onRegister):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            box.onSyncGuildMineWarResult(guildUUID, '', 0, 0, '', {}, onRegister)
            return

        _gcVal.guildBox.getJunxuQiXieLevel(guildUUID, box, onRegister)
        
    def addMineWarScoreFromGuild(self, mapId, guildUUID, playerGbId, playerName, score, scoreType):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            return

        gameengine.getGlobalBase('MineWarStub').addMineWarScore(mapId, playerGbId, playerName, _gcVal.guildName, _gcVal.icon, _gcVal.dspFlag, score, scoreType)

    def onMineWarFlagBeKillFromGuild(self, mapId, guildUUID, killerName):
        _gcVal = self.guildDic.get(guildUUID)
        if not _gcVal:
            return

        gameengine.getGlobalBase('MineWarStub').onMineWarFlagBeKill(mapId, _gcVal.guildName, killerName)