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
        self._callback(1, '_singleDungeonTrapCallback', (dungeonNo, self.DEFAULT_EXIT_COUNT), gametimer.TIMER_TAG_SINGLE_DUNGEON_TRAP_CALLBACK)

    def _singleDungeonTrapCallback(self, dungeonNo, exitCount):
        if formula.getMapId(self.spaceNo) != dungeonNo:
            return

        dungeonSpaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        mapInfo = self._getMapInfoByDungeonNo(dungeonNo)
        if not mapInfo:
            if gameconst.DungeonType.isGuildDungeon(dungeonSpaceType):
                # 【【任务】副本类型扩展-帮会副本】
                mapInfo = self._getMapInfoByDungeonNo(gameconst.MapIdDef.mapGuildSpace)

        if not mapInfo:
            return

        if not self._isPlayerInMap(mapInfo):
            if exitCount <= 0:
                self.showMsg(MMD.datas.crossingDungeonArea, [])
                self.leaveSingleDungeon(self.id, dungeonNo)
                return

            if exitCount == self.DEFAULT_EXIT_COUNT:
                self.showMsg(MMD.datas.leavingDungeonArea, [str(exitCount)])

            DEBUG_MSG('_singleDungeonTrapCallback::outside team dungeon range, '
                      'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT

        self._callback(1, '_singleDungeonTrapCallback', (dungeonNo, exitCount), gametimer.TIMER_TAG_SINGLE_DUNGEON_TRAP_CALLBACK)

    # ===========================================

    @gamedecorator.limitcall(2, msgId=MMD.datas.dungeonRefused)
    def selfEnterSingleDungeon(self, dungeonNo, src):
        DEBUG_MSG('selfEnterSingleDungeon:', dungeonNo, src)

        _targetSpaceNo = formula.getLineSpaceNo(dungeonNo, 0)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        return self._enterSingleDungeon(dungeonNo, src)

    def gmEnterSingleDungeon(self, dungeonNo, src):
        if not self._checkEnterSingleDungeon(dungeonNo):
            return

        _now = utils.getNow()
        if self.isGlobalTeleportLocked(now=_now):
            WARNING_MSG("gmEnterSingleDungeon:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)

        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterType.SINGLE).applyCreateDungeon(
                self.base, self.gbId, self.teamId,
                {'dungeonNo': dungeonNo, 'src': src, 'spaceLevel':self.level})

    def _enterSingleDungeon(self, dungeonNo, src, extra=None):
        if not self._checkEnterSingleDungeon(dungeonNo, src):
            return

        extra = extra or {}
        extra.update({'dungeonNo': dungeonNo, 'src': src, 'spaceLevel':self.level})

        self.onCheckSingleDungeonCondition(dungeonNo, True, {}, extra)

    def _enterSingleDungeonAfterCast(self, dungeonNo, extra):
        ERROR_MSG("_enterSingleDungeonAfterCast::", dungeonNo, extra)
        if not self._checkEnterSingleDungeon(dungeonNo, extra.get('src')):
            return

        extra.update({'hasCast': True})

        self.onCheckSingleDungeonCondition(dungeonNo, True, {}, extra)

    def onCheckSingleDungeonCondition(self, dungeonNo, result, reasonDic, extra):
        DEBUG_MSG('onCheckSingleDungeonCondition::', dungeonNo, result, reasonDic)
        if not result:
            WARNING_MSG('onCheckSingleDungeonCondition:: failed', dungeonNo, reasonDic)
            return

        _hasCast = extra.get('hasCast', False)
        _spaceTemplateNo = gameconst.SpaceType.getSingleDungeonSpaceNoRange(dungeonNo)[0]
        if not _hasCast and utils.isComplexTeleportNeedCast(self.spaceNo, _spaceTemplateNo, gameconst.ComplexTeleportType.ENTER, None, owner=self):
            self.enterSpaceCommonNeedCast('_enterSingleDungeonAfterCast', (dungeonNo, extra))
            return

        _now = utils.getNow()
        if self.isGlobalTeleportLocked(now=_now):
            WARNING_MSG("onCheckSingleDungeonCondition:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)
        spaceUUID = 0
        if self.spaceMgr:
            spaceUUID = self.spaceMgr.spaceUUID
        extra['inSpaceUUID'] = spaceUUID
        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterType.SINGLE).applyCreateDungeon(
            self.base, self.gbId, self.teamId, extra)
        self.resetStatisticsData()

    def _checkEnterSingleDungeon(self, dungeonNo, src=None, checkSameDungeon=True):
        if dungeonNo not in DDID.datas:
            INFO_MSG('{0} invalid'.format(dungeonNo))
            return False

        if checkSameDungeon and formula.getDungeonNoBySpaceNo(self.spaceNo) == dungeonNo:
            WARNING_MSG('_checkEnterSingleDungeon::repeat enter same dungeon', dungeonNo, self.spaceNo)
            return False

        if not self.checkCrtMapCanEnterDungeon():
            return False

        dungeonInfo = DDID.datas[dungeonNo]
        if not gameconst.DungeonType.isSingleDungeon(dungeonInfo['type'],
                                                     dungeonInfo['enterType']):
            INFO_MSG('{0} not single dungeon'.format(dungeonNo))
            # TODO()(DUNGEON_EXTEND): add message
            # self.showMsg(MMD.datas.CUSTOM_STRING6, ['该副本无法单人进入'])
            return False

        if not self.checkConflictState(CCD.datas.teleport):
            INFO_MSG('checkConflictState error')
            return False

        # 【【任务】战斗状态&&进入副本判断】
        if not dungeonInfo["fightConflict"] and self.hasState(gameconst.State.Fighting):
            INFO_MSG("_checkEnterSingleDungeon:: fight state failed")
            self.showMsg(MMD.datas.enterDunFailFightSingle, [])
            return False

        if not self.canDoCompleteTeleport(noErrorMsg=True, judgeLeaveSrc=src):
            WARNING_MSG('_checkEnterSingleDungeon::can\'t enter space from current spaceNo', self.spaceNo)
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
            ERROR_MSG('Enter singleDungeon Failed, use item error: code={}, spaceNo={}'.format(state, spaceNo))
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
                gameengine.reportCritical('readyUseItemAndEnterSingleDungeon::fatal error when try to enter single dungeon space', self.spaceNo, spaceNo, context)
            else:
                WARNING_MSG("readyUseItemAndEnterSingleDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return

        # 【【程序自主】单人副本进入时取消组队跟随】
        self.selfCancelFollowTeamCaptain('enter-single-dungeon')
        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

        # gamelog.singleDungeonLogger.enterDungeonSucc(
        #     extra.get('dungeonPlayMode'), self.gbId, src.srcId if src else 0,
        #     dungeonNo=formula.getDungeonNoBySpaceNo(spaceNo))

    @gamedecorator.limitcall(5)
    def leaveSingleDungeon(self, exposed, dungeonNo):
        if not self._isMyself(exposed):
            return

        if not self.newbieAllowLeave():
            return

        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.doLeaveSingleDungeon(dungeonNo, src, 'client leave')

    def leaveTutorialIsComplete(self, dungeonNo):
        DEBUG_MSG('leaveTutorialIsComplete:', dungeonNo)
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.doLeaveSingleDungeon(dungeonNo, src, 'client leave')

    def selfLeaveSingleDungeon(self, dungeonNo, src):
        DEBUG_MSG('selfLeaveSingleDungeon:', dungeonNo, src)
        _now = utils.getNow()
        if self.isGlobalTeleportLocked(now=_now):
            WARNING_MSG("selfLeaveSingleDungeon:: teleport locked", dungeonNo, src, self.teleportGlobalLockRlsT)
            return
        self.aquireGlobalTeleportLock(now=_now)
        self.doLeaveSingleDungeon(dungeonNo, src, 'server leave')

    def doLeaveSingleDungeon(self, dungeonNo, src, reason):
        DEBUG_MSG('wl: doLeaveSingleDungeon', dungeonNo, src, reason)
        if not formula.isDungeonSpace(self.spaceNo):
            return

        spaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        enterType = gameengine.getDungeonEnterTypeBySpaceNo(self.spaceNo)
        if enterType and enterType != gameconst.DungeonEnterType.SINGLE:
            WARNING_MSG('doLeaveSingleDungeon:: leave single but got team, auto change',
                        dungeonNo, self.spaceNo, enterType)
            if enterType == gameconst.DungeonEnterType.TEAM:
                WARNING_MSG('doLeaveSingleDungeon:: change to team dungeon leave', self.spaceNo)
                self.selfLeaveTeamDungeon(src)
            else:
                ERROR_MSG('doLeaveSingleDungeon::unknown enterType', dungeonNo, enterType)
            return

        _m_mapId, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.getLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        lContext = {'spaceMgrBox': self.spaceMgr.base, 'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID}
        eContext = {}
        context = {'e': eContext, 'l': lContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)

        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        # gamelog.singleDungeonLogger.leaveDungeon(
        #     self.spaceMgr.dungeonPlayMode, self.gbId, dungeonNo=dungeonNo)

    def doLeaveSingleDungeonWithDstPos(self, dstNo, dstPos, dstDir):
        """task使用, 这个接口只用于从单人副本返回到大世界分线"""
        DEBUG_MSG('in doLeaveSingleDungeonWithDstPos: 1', self.spaceNo, dstNo, dstPos, dstDir)
        if not formula.isDungeonSpace(self.spaceNo):
            DEBUG_MSG('in doLeaveSingleDungeonWithDstPos: 2', self.spaceNo, dstNo, dstPos, dstDir)
            return

        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        spaceType = self._getPrmBydungeonNo(dungeonNo, 'type')
        if self.autoCombat and DDID.datas[dungeonNo].get('leaveDungeonDisableAutoFight', 0):
            self.stopAutoCombat(self.id)

        lContext = {'spaceMgrBox': self.spaceMgr.base, 'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID,
                    'overwrite': {'position': dstPos, 'direction': dstDir}}
        context = {'e': {}, 'l': lContext}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        spaceNo = formula.getLineSpaceNo(dstNo)
        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

    def isInSingleDungeon(self):
        if not formula.isDungeonSpace(self.spaceNo):
            return False

        dungeonNo = formula.getMapId(self.spaceNo)

        if dungeonNo not in DDID.datas:
            ERROR_MSG("isInTeamDungeon::can't find dungeonNo in DLL sheet")
            return False

        dungeonSpaceType = DDID.datas[dungeonNo]['type']
        dungeonEnterType = DDID.datas[dungeonNo]['enterType']

        if gameconst.DungeonType.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
            return True

        return False

    def canNewbieLeaveCurDungeon(self):
        return True
