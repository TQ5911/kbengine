# -*- coding: utf-8 -*-
from KBEDebug import *

import KBEngine

import formula
import gamelog
import gameconst
import gameengine
import gamedecorator
import utils
import gametimer
import impDungeonCommon
import math

import message_Message_def as MMD
import conflict_conflict_def as CCD
import gamePlay_gamePlay as DDID
import tutorConst_guideConfig as TCGCD

import complexTeleportOption
import dungeonSrc


class ImpSingleDungeon(impDungeonCommon.ImpDungeonCommon):

    # ===========================================
    # DUNGEON TRAP METHODS

    def _createSingleDungeonTrap(self, dungeonNo):
        self.addTimerCB(1, '_singleDungeonTrapCallback', (dungeonNo, self.DEFAULT_EXIT_COUNT), gametimer.TIMER_TAG_SINGLE_DUNGEON_TRAP_CALLBACK)

    def _singleDungeonTrapCallback(self, dungeonNo, exitCount):
        if formula.fetchMapId(self.spaceNo) != dungeonNo:
            return
        
        mapInfo = self._getMapInfoByDungeonNo(dungeonNo)
        if not mapInfo:
            return

        if not self._isPlayerInMap(mapInfo):
            if exitCount <= 0:
                self.showMsg(MMD.datas.crossingDungeonArea, [])
                self.leaveSingleDungeon(self.id, dungeonNo)
                return

            if exitCount == self.DEFAULT_EXIT_COUNT:
                self.showMsg(MMD.datas.leavingDungeonArea, [str(exitCount)])

            LOG_IFO('_singleDungeonTrapCallback::outside team dungeon range, '
                      'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT

        self.addTimerCB(1, '_singleDungeonTrapCallback', (dungeonNo, exitCount), gametimer.TIMER_TAG_SINGLE_DUNGEON_TRAP_CALLBACK)

    # ===========================================

    @gamedecorator.limitcall(2, msgId=MMD.datas.dungeonRefused)
    def selfEnterSingleDungeon(self, dungeonNo, src):
        LOG_IFO('selfEnterSingleDungeon:', dungeonNo, src)

        _targetSpaceNo = formula.combineLineSpaceNo(dungeonNo, 0)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        return self._enterSingleDungeon(dungeonNo, src)

    def gmEnterSingleDungeon(self, dungeonNo, src):
        if not self._checkEnterSingleDungeon(dungeonNo):
            return

        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("gmEnterSingleDungeon:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)

        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE).applyCreateDungeon(
                self.base, self.gbId, self.teamId,
                {'dungeonNo': dungeonNo, 'src': src, 'spaceLevel':self.level})

    def _enterSingleDungeon(self, dungeonNo, src, extra=None):
        if not self._checkEnterSingleDungeon(dungeonNo, src):
            return

        extra = extra or {}
        extra.update({'dungeonNo': dungeonNo, 'src': src, 'spaceLevel':self.level})

        self.onCheckSingleDungeonCondition(dungeonNo, True, {}, extra)

    def _enterSingleDungeonAfterCast(self, dungeonNo, extra):
        LOG_ERR("_enterSingleDungeonAfterCast::", dungeonNo, extra)
        if not self._checkEnterSingleDungeon(dungeonNo, extra.get('src')):
            return

        extra.update({'hasCast': True})

        self.onCheckSingleDungeonCondition(dungeonNo, True, {}, extra)

    def onCheckSingleDungeonCondition(self, dungeonNo, result, reasonDic, extra):
        LOG_IFO('onCheckSingleDungeonCondition::', dungeonNo, result, reasonDic)
        if not result:
            LOG_WARN('onCheckSingleDungeonCondition:: failed', dungeonNo, reasonDic)
            return

        _hasCast = extra.get('hasCast', False)
        _spaceTemplateNo = gameconst.SpaceType.getSingleDungeonSpaceRange(dungeonNo)[0]
        if not _hasCast and utils.checkComplexTeleportNeedCast(self.spaceNo, _spaceTemplateNo, gameconst.ComplexTeleportType.ENTER, None, owner=self):
            self.enterSpaceCommonNeedCast('_enterSingleDungeonAfterCast', (dungeonNo, extra))
            return

        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("onCheckSingleDungeonCondition:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)
        spaceUUID = 0
        if self.spaceMgr:
            spaceUUID = self.spaceMgr.spaceUUID
        extra['inSpaceUUID'] = spaceUUID
        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE).applyCreateDungeon(
            self.base, self.gbId, self.teamId, extra)
        self.resetStatisticsData()

    def _checkEnterSingleDungeon(self, dungeonNo, src=None, checkSameDungeon=True):
        if dungeonNo not in DDID.datas:
            LOG_IFO('{0} invalid'.format(dungeonNo))
            return False

        if checkSameDungeon and formula.parseDungeonNoBySpaceNo(self.spaceNo) == dungeonNo:
            LOG_WARN('_checkEnterSingleDungeon::repeat enter same dungeon', dungeonNo, self.spaceNo)
            return False

        if not self.checkCrtMapCanEnterDungeon():
            return False

        dungeonInfo = DDID.datas[dungeonNo]
        if not gameconst.DungeonTypeJudge.isSingleDungeon(dungeonInfo['type'],
                                                     dungeonInfo['enterType']):
            LOG_IFO('{0} not single dungeon'.format(dungeonNo))
            # TODO()(DUNGEON_EXTEND): add message
            # self.showMsg(MMD.datas.CUSTOM_STRING6, ['该副本无法单人进入'])
            return False

        if not self.checkConflictState(CCD.datas.teleport):
            LOG_IFO('checkConflictState error')
            return False

        # 【【任务】战斗状态&&进入副本判断】
        if not dungeonInfo["fightConflict"] and self.hasState(gameconst.StateEnum.Fighting):
            LOG_IFO("_checkEnterSingleDungeon:: fight state failed")
            self.showMsg(MMD.datas.enterDunFailFightSingle, [])
            return False

        if not self.canDoCompleteTeleport(noErrorMsg=True, judgeLeaveSrc=src):
            LOG_WARN('_checkEnterSingleDungeon::can\'t enter space from current spaceNo', self.spaceNo)
            # self.showMsg(MMD.datas.dungeonEntryMustBeWorld, [])
            return False

        return True

    def onSingleDungeonSpaceReady(self, spaceBox, spaceMgrBox, spaceMgrId, spaceNo, playerBox, playerGbId, teamUUID, extra):
        self.readyUseItemAndEnterSingleDungeon(0, spaceBox, spaceMgrBox, spaceMgrId,
                                                   spaceNo, playerBox, playerGbId, teamUUID, extra)

    def readyUseItemAndEnterSingleDungeon(self, state,
                                          spaceBox, spaceMgrBox, spaceMgrId, spaceNo, playerBox,
                                          playerGbId, teamUUID, extra):
        if state != 0:
            LOG_ERR('Enter singleDungeon Failed, use item error: code={}, spaceNo={}'.format(state, spaceNo))
            return

        eContext = {'spaceMgrBox': spaceMgrBox,
                    'spaceBox': spaceBox,
                    'playerBox': playerBox,
                    'playerGbId': playerGbId,
                    'teamUUID': teamUUID,
                    'extra': extra}
        lContext = {}
        src = extra.get('src')
        context = {'e': eContext, 'l': lContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        canLeave = self.packageComplexTeleportLeaveData(lContext, judgeLeaveSrc=src)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailedReason.COLL_USEROPRERRNO:
                gameengine.panicStack('readyUseItemAndEnterSingleDungeon::fatal error when try to enter single dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("readyUseItemAndEnterSingleDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    @gamedecorator.limitcall(5)
    def leaveSingleDungeon(self, exposed, dungeonNo):
        if not self._isMyself(exposed):
            return

        if not self.newbieAllowLeave():
            return

        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.doLeaveSingleDungeon(dungeonNo, src, 'client leave')

    def leaveTutorialIsComplete(self, dungeonNo):
        LOG_IFO('leaveTutorialIsComplete:', dungeonNo)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.doLeaveSingleDungeon(dungeonNo, src, 'client leave')

    def selfLeaveSingleDungeon(self, dungeonNo, src):
        LOG_IFO('selfLeaveSingleDungeon:', dungeonNo, src)
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("selfLeaveSingleDungeon:: teleport locked", dungeonNo, src, self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)
        self.doLeaveSingleDungeon(dungeonNo, src, 'server leave')

    def doLeaveSingleDungeon(self, dungeonNo, src, reason):
        LOG_IFO('wl: doLeaveSingleDungeon', dungeonNo, src, reason)
        if not formula.inDungeonScene(self.spaceNo):
            return

        spaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        enterType = gameengine.getDungeonEnterTypeBySpaceNo(self.spaceNo)
        if enterType and enterType != gameconst.DungeonEnterTypeEnum.SINGLE:
            LOG_WARN('doLeaveSingleDungeon:: leave single but got team, auto change',
                        dungeonNo, self.spaceNo, enterType)
            if enterType == gameconst.DungeonEnterTypeEnum.TEAM:
                LOG_WARN('doLeaveSingleDungeon:: change to team dungeon leave', self.spaceNo)
                self.selfLeaveTeamDungeon(src)
            else:
                LOG_ERR('doLeaveSingleDungeon::unknown enterType', dungeonNo, enterType)
            return

        _m_mapId, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        lContext = {'spaceMgrBox': self.spaceMgr.base, 'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID}
        eContext = {}
        context = {'e': eContext, 'l': lContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)

        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        # gamelog.singleDungeonLogger.leaveDungeon(
        #     self.spaceMgr.dungeonPlayMode, self.gbId, dungeonNo=dungeonNo)

    def doLeaveSingleDungeonWithDstPos(self, dstNo, dstPos, dstDir):
        """task使用, 这个接口只用于从单人副本返回到大世界分线"""
        LOG_IFO('in doLeaveSingleDungeonWithDstPos: 1', self.spaceNo, dstNo, dstPos, dstDir)
        if not formula.inDungeonScene(self.spaceNo):
            LOG_IFO('in doLeaveSingleDungeonWithDstPos: 2', self.spaceNo, dstNo, dstPos, dstDir)
            return

        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        spaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        if self.autoCombat and DDID.datas[dungeonNo].get('leaveDungeonDisableAutoFight', 0):
            self.stopAutoCombat(self.id)

        lContext = {'spaceMgrBox': self.spaceMgr.base, 'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID,
                    'overwrite': {'position': dstPos, 'direction': dstDir}}
        context = {'e': {}, 'l': lContext}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        spaceNo = formula.combineLineSpaceNo(dstNo)
        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

    def isInSingleDungeon(self):
        if not formula.inDungeonScene(self.spaceNo):
            return False

        dungeonNo = formula.fetchMapId(self.spaceNo)

        if dungeonNo not in DDID.datas:
            LOG_ERR("isInTeamDungeon::can't find dungeonNo in DLL sheet")
            return False

        dungeonSpaceType = DDID.datas[dungeonNo]['type']
        dungeonEnterType = DDID.datas[dungeonNo]['enterType']

        if gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
            return True

        return False

    def canNewbieLeaveCurDungeon(self):
        return True

    #副本流程控制节点传送到其他场景（目前支持传到大世界or大世界副本）
    def transferToTheDesignatedMap(self, dstNo, dstPos, dstDir):
        _dir = (0, 0, dstDir * math.pi / 180)
        if formula.checkWorldLineType(dstNo):
            self.doLeaveSingleDungeonWithDstPos(dstNo, dstPos, _dir)
            return
        
        dungeonSpaceType = DDID.datas[dstNo]['type']
        dungeonEnterType = DDID.datas[dstNo]['enterType']

        if dstNo == formula.fetchMapId(self.spaceNo):
            self.telToPos(dstPos, _dir)
        
        elif gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
            src = dungeonSrc.DungeonFromFlowController(self.base, self.gbId)
            self._enterSingleDungeon(dstNo, src, {'position': (dstPos.x, dstPos.y, dstPos.z)})

