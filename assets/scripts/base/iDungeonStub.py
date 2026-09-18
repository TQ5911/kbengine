# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import gameglobal
import gametimer
import gamesql
import utils
import userType
import formula
import itertools

import iBaseNoCell
import iGlobal
import iTimer
import math
import random
import sMath

import dungeonPlayMode

import gamePlay_gamePlay as DDI


class IDungeonStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    def __init__(self, **kwargs):
        super(IDungeonStub, self).__init__()
        self.crtGenSpaceNo = 0

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        raise Exception('not implemented')

    def _checkDungeonSpaceDestroy(self):
        raise Exception('not implemented')

    def applyCreateDungeon(self, box, gbId, dungeonUUID, extra):
        raise Exception('not implemented')

    def doEnterDungeon(self, box, gbId, dungeonUUID, spaceNo, extra):
        raise Exception('not implemented')
    
    def getDungeonSpaceRange(self):
        return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)

    def createDungeonSpaceRemote(self, box, gbId, dungeonUUID, extra):
        _spaceNoStart, spaceNoEnd = self.getDungeonSpaceRange()
        if self.crtGenSpaceNo < _spaceNoStart or self.crtGenSpaceNo >= spaceNoEnd:
            self.crtGenSpaceNo = _spaceNoStart
        for spaceNo in itertools.chain(range(self.crtGenSpaceNo, spaceNoEnd), range(_spaceNoStart, self.crtGenSpaceNo)):
            if spaceNo not in self.spaces:
                self._createSpaceRemote(spaceNo, box, gbId, dungeonUUID, extra)
                _crtGenSpaceNo = spaceNo + 1
                self.crtGenSpaceNo = _crtGenSpaceNo if _crtGenSpaceNo < spaceNoEnd else _spaceNoStart
                break
        else:
            LOG_ERR('cannot createDungeonSpaceRemote', len(self.spaces))
            self._onCreateDungeonSpaceFailed(dungeonUUID, extra)

    def _onCreateDungeonSpaceFailed(self, dungeonUUID, extra):
        # 建空间失败兜底：跨服组队副本需回报中心失败（本服各 stub 维持只记日志）；
        # 判定认 extra['crossTeamId']（本服模式空间 playMode 已落本服枚举，认 playMode 会漏报）
        if (extra or {}).get('crossTeamId'):
            gameengine.getCrossTeamStub(dungeonUUID).onCrossCrusadeSpaceReady(
                dungeonUUID,
                0,
                0,
                False,
                None,
                None
            )

    def _getDungeonSpaceWeight(self, enterNum=0) -> int:
        return enterNum

    def _getDungeonSpaceVal(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        raise Exception('not implemented')

    def _createSpaceRemote(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        # playerBox 可为 None（跨服讨伐由中心协调建空间，无发起玩家）
        LOG_INFO('zt: create home space', spaceNo, playerBox.id if playerBox else 0, playerGbId,dungeonUUID, extra)

        self.spaces[spaceNo]=self._getDungeonSpaceVal(spaceNo, playerBox, playerGbId, dungeonUUID, extra)

        _spaceProps = {
            'spaceno': spaceNo,
            'spaceNo': spaceNo,
            'position': gameconst.SPACE_FIX_POS,
        }
        spaceWeight = self._getDungeonSpaceWeight()
        if spaceWeight > 0:
            _spaceProps["spaceWeight"] = spaceWeight
        KBEngine.createEntityAnywhere('Space', _spaceProps,
                                      lambda spaceBox, spaceNo=spaceNo, playerBox=playerBox, playerGbId=playerGbId, dungeonUUID=dungeonUUID, extra=extra: \
                                          self._onCreateSpaceRemote(spaceBox, spaceNo, playerBox, playerGbId, dungeonUUID, extra)
                                      )

    def _onCreateSpaceRemote(self, spaceBox, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        LOG_INFO('_onCreateSpaceRemote', spaceBox, spaceNo, playerBox.id if playerBox else 0, playerGbId, dungeonUUID, extra)
        if not spaceBox:
            if spaceNo in self.spaces:
                self.spaces.pop(spaceNo)
            self._onCreateDungeonSpaceFailed(dungeonUUID, extra)
        else:
            spaceUUID=KBEngine.genUUID64()
            _sVal=self.spaces[spaceNo]
            _sVal.spaceBox=spaceBox
            _sVal.spaceUUID=spaceUUID
            self.argsCache[spaceNo]=(playerBox, playerGbId, dungeonUUID, extra)

    def onDungeonSpaceReady(self, spaceNo):
        if spaceNo not in self.spaces:
            LOG_ERR('zt: onDungeonSpaceReady cannot find space:', spaceNo)
            return

        self._createDungeonSpaceMgr(spaceNo)

    def _createDungeonSpaceMgr(self, spaceNo):
        _spaceVal = self.spaces[spaceNo]
        _props = {
            'position':gameconst.SPACE_FIX_POS,
            'spaceNo':spaceNo,
            'direction':(0,0,0),
        }

        *_, _extra = self.argsCache[spaceNo]
        dungeonPlayMode_ = _extra.get('dungeonPlayMode')
        dungeonStage = _extra.get('dungeonStage')
        if dungeonPlayMode_:
            if dungeonPlayMode_.playMode in gameconst.DungeonPlayModeEnum.COLL_SYNC_SPACELEVEL:
                dungeonPlayMode_.spaceLevel = _spaceVal.spaceLevel
        else:
            dungeonPlayMode_ = dungeonPlayMode.UnknownDungeonPlayMode()

        dungeonPlayMode_.spaceUUID = _spaceVal.spaceUUID
        _props['dungeonPlayMode'] = dungeonPlayMode_

        if dungeonStage is not None:
            _props['dungeonStage'] = dungeonStage

        tempMiscProps = {}
        if formula.inSingleDungeonScene(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.DSMPEnumsingleDungeonBelongPlayerGBID] = _spaceVal.ownerGbId
        elif formula.inTeamDungeonScene(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.DSMPEnumteamDungeonBelongTeamUUID] = _spaceVal.teamUUID
        elif formula.inRaidDungeonScene(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.DSMPEnumraidDungeonBelongRaidUUID] = _spaceVal.raidUUID
        elif formula.inGuildBossDungeonScene(spaceNo):
            tempMiscProps[gameconst.DungeonSpaceMgrProps.DSMPEnumguildBossDungeonBelongGuildUUID] = _spaceVal.guildUUID

        if tempMiscProps:
            _props.setdefault("tempMiscProps", {}).update(tempMiscProps)

        LOG_INFO('create DungeonSpaceMgr', _props)
        mgr = KBEngine.createEntityLocally('DungeonSpaceMgr', _props)
        if not mgr:
            # 这里先加个日志跟踪下吧，测试上机器人的过程中，出现过单人副本spaceMgr为空的情况
            LOG_ERR('create DungeonSpaceMgr failed', spaceNo, _props)
        _spaceVal.spaceMgr = mgr

    def _onCreateDungeonReady(self, spaceNo):

        args=self.argsCache.pop(spaceNo)
        if not args:
            return

        (playerBox, playerGbId, dungeonUUID, extra)=args

        self._loadDungeonSpaceEntities(spaceNo, playerBox, playerGbId, dungeonUUID, extra)

    def onDunSpaceMgrReady(self, spaceNo):
        self._onCreateDungeonReady(spaceNo)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        pass

    def enterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        pass

    def onAvatarDie(self, spaceNo, playerBox, playerGbId):
        pass

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        pass

    def createCellEntity(self, spaceNo, entityType, position, direction, props):
        if spaceNo not in self.spaces:
            LOG_ERR('zt: createCellEntity cannot find space:', spaceNo)
            return

        _spaceVal=self.spaces[spaceNo]
        _spaceVal.spaceBox.cell.createCellLocally(entityType, position, direction, props)

    def onAvatarOffline(self, spaceNo, playerGbId):
        raise NotImplementedError()

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        raise NotImplementedError()

    def _onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp=0):
        LOG_INFO('onReliveInDungeon::', spaceNo, playerBox, playerGbId, reliveType, reliveHp)
        if spaceNo not in self.spaces:
            LOG_ERR('wl: onReliveInDungeon cannot find space:', spaceNo)
            return

        dungeonInfo = DDI.datas.get(self.dungeonNo, None)
        dungeonSInfo = utils.getDunStructModData(self.dungeonNo)
        if not dungeonInfo:
            LOG_ERR('wl: onReliveInDungeon cannot find dungeonInfo:', self.dungeonNo)
            return

        dungeonSpaceType = dungeonInfo['type']
        if reliveType == gameconst.RELIVE_TYPE_TO_NEAR:
            rebornPosDict = {}
            if 'RebornPos' in dungeonSInfo:
                rebornPosDict = dungeonSInfo['RebornPos']
                
            if not rebornPosDict:
                gameengine.panicStack(
                    'Reborn position not defined in dungeon {0}, '
                    'please confirm dungeon RebornPos defined in dungeon-map client Editor '
                    '(check dungeon_{0}.py file and make sure RebornPos Class defined in file) '
                    'and dungeon_s_{0}.py file uploaded certainly.'.format(self.dungeonNo), dungeonSpaceType)
                return

            rebornD, *_ = rebornPosDict.values()
            rebornPos = formula.bornPosFromDunData(rebornD)
            rebornDir = (0.0, 0.0, rebornD['Dir'] * math.pi / 180)
            # 修改下复活点
            if spaceNo in self.rebornPosCache:
                posCache = self.rebornPosCache[spaceNo]
                LOG_INFO('relive use rebornPosCache', spaceNo, posCache)
                # 做个随机偏移
                angle = random.uniform(0, 2 * math.pi)
                radius = max(0, rebornD['Props']['Radius'])
                offsetX = math.cos(angle) * radius
                offsetZ = math.sin(angle) * radius
                rebornPos = (posCache[0] + offsetX, posCache[1], posCache[2] + offsetZ)
                # 计算方向
                # yaw = sMath.getYawFromPoints(posCache, rebornPos)
                # rebornDir = (0.0, 0.0, yaw)
            playerBox.cell.reliveToPos(rebornPos, rebornDir, reliveHp, None)

        elif reliveType == gameconst.RELIVE_TYPE_DIRECTLY:
            playerBox.cell.reliveToPos(None, None, 0, None)

        elif reliveType == gameconst.RELIVE_TYPE_LEAVE_IN_DUNGEON:
            # FEATURE()(DUNGEON): cal leave dungeon from client
            LOG_WARN('onReliveInDungeon::reliveType RELIVE_TYPE_LEAVE_IN_DUNGEON in dungeon is not valid')

        else:
            LOG_ERR('onReliveInDungeon::reliveType is not valid, got {}'.format(reliveType))

    def onCreateNewRebornPos(self, spaceNo, position):
        LOG_INFO('onCreateNewRebornPos', spaceNo, position)
        self.rebornPosCache[spaceNo] = position

    def onDungeonStarted(self, spaceNo, tCreate):
        """call when dungeon started"""

    def onDungeonStartChallenge(self, spaceNo, endTime):
        """call when dungeon challenge started"""

    def sendBigWorldDungeonProps(self, box, gbId, spaceNo):
        LOG_INFO('sendBigWorldDungeonProps::')
        if spaceNo not in self.spaces:
            LOG_ERR('spaceNo "{}" not found in spaces'.format(spaceNo))
            return

        _spaceVal = self.spaces[spaceNo]

        # calculate tDungeonLostTime to client
        endTime = int(_spaceVal.tCreate + DDI.datas[self.dungeonNo]['timeOut'] * 60 + 1)
        if _spaceVal.isCompleted():
            if _spaceVal.dungeonSpaceValType == gameconst.DungeonSpaceValType.RAID:
                _spaceVal.spaceMgr.cell.onRaidDungeonCompleted(spaceNo, _spaceVal.raidUUID, not _spaceVal.isFailed(), 0, _spaceVal.dungeonCreepBaseKillDic, _spaceVal.getAllPlayerGbidAndNamePair(), _spaceVal.getElapsedTime(), gbId, _spaceVal.completedReasonType)
            elif _spaceVal.dungeonSpaceValType == gameconst.DungeonSpaceValType.TEAM:
                _spaceVal.spaceMgr.cell.onTeamDungeonCompleted(spaceNo, _spaceVal.teamUUID, not _spaceVal.isFailed(), 0,  _spaceVal.getElapsedTime(), gbId, _spaceVal.completedReasonType)
            elif _spaceVal.dungeonSpaceValType == gameconst.DungeonSpaceValType.SINGLE:
                _spaceVal.spaceMgr.cell.onSingleDungeonCompleted(spaceNo, gbId, not _spaceVal.isFailed(), 0, _spaceVal.getElapsedTime())
            elif _spaceVal.dungeonSpaceValType == gameconst.DungeonSpaceValType.GUILD_BOSS:
                _spaceVal.spaceMgr.cell.onGuildBossDungeonCompleted(spaceNo, _spaceVal.guildUUID, not _spaceVal.isFailed(), 0, _spaceVal.getElapsedTime(), gbId, _spaceVal.completedReasonType)
        box.client.changeDungeonRemainTime(spaceNo, endTime)

    def getSpaceCell(self, spaceNo):
        return self.spaces[spaceNo].spaceBox.cell

    def requestSpaceCell(self, requestBox, spaceNo):
        requestBox.onRequestSpaceCell(self.spaces[spaceNo].spaceBox.cell, spaceNo)

    def getExtraData(self, spaceNo, gbId):
        return None

    def onDungeonSpaceGone(self, spaceNo, reason):
        pass
    
    def getSettlementRankList(self, rankType, spaceNo, uniqueID, playerBox, gbID, idx, offset):
        LOG_INFO("getSettlementRankList~ ", rankType, spaceNo, uniqueID, playerBox, gbID, idx, offset)
        if spaceNo not in self.spaces:
            LOG_WARN('getSettlementRankList:: failed, missing space data', spaceNo)
            return

        spaceVal = self.spaces[spaceNo]
        spaceVal.spaceMgr.cell.onGetSettlementRankList(rankType, spaceNo, uniqueID, playerBox, gbID, idx, offset)
 
