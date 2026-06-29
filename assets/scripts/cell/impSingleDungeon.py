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
import CollectionCheckContext

import message_Message_def as M_M_DD

import conflict_conflict_def as C_C_DD
import gamePlay_gamePlay as GP_GPD
import tutorConst_guideConfig as TCGCD

import complexTeleportOption
import dungeonSrc


class ImpSingleDungeon(impDungeonCommon.ImpDungeonCommon):

    # ===========================================
    # DUNGEON TRAP METHODS

    def _createSingleDungeonTrap(self, dunNo):
        self.addTimerCB(
            1, 
            '_singleDungeonTrapCallback', 
            (dunNo, self.DEFAULT_EXIT_COUNT_NUM), 
            gametimer.TIMER_TAG_SINGLE_DUNGEON_TRAP_CALLBACK)

    def _singleDungeonTrapCallback(self, dungeonNo, exitCount):
        if formula.fetchMapId(self.spaceNo) != dungeonNo:
            return
        
        _mapInfo = self._getMapInfoByDungeonNo(dungeonNo)
        if not _mapInfo:
            return

        if not self._isPlayerInMap(_mapInfo):
            if exitCount <= 0:
                self.showMsg(M_M_DD.datas.crossingDungeonArea, [])
                self.leaveSingleDungeon(self.id, dungeonNo)
                return

            if self.DEFAULT_EXIT_COUNT_NUM == exitCount:
                self.showMsg(M_M_DD.datas.leavingDungeonArea, [str(exitCount)])

            LOG_INFO('_singleDungeonTrapCallback::outside team dungeon range, '
                      'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT_NUM != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT_NUM

        self.addTimerCB(1, '_singleDungeonTrapCallback', (dungeonNo, exitCount), gametimer.TIMER_TAG_SINGLE_DUNGEON_TRAP_CALLBACK)

    # ===========================================

    @gamedecorator.limitcall(2, msgId=M_M_DD.datas.dungeonRefused)
    def selfEnterSingleDungeon(self, dungeonNo, src):
        LOG_INFO('selfEnterSingleDungeon:', dungeonNo, src)

        _targetSpaceNo = formula.combineLineSpaceNo(dungeonNo, 0)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        return self._enterSingleDungeon(dungeonNo, src)

    def gmEnterSingleDungeon(self, dungeonNo, src):
        if not self._checkEnterSingleDungeon(dungeonNo):
            LOG_ERR('gmEnterSingleDungeon', dungeonNo, src)
            return

        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("gmEnterSingleDungeon:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.acquireGlobalTeleportLock(now=_now)

        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE).applyCreateDungeon(
                self.base, self.gbId, self.teamId,
                {
                    'src': src, 
                    'dungeonNo': dungeonNo, 
                    'spaceLevel':self.level,
                })

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

    def onCheckSingleDungeonCondition(self, dungeonNo, result, reasonDic, extraData):
        LOG_INFO('onCheckSingleDungeonCondition::', dungeonNo, result, reasonDic)
        if not result:
            LOG_WARN('onCheckSingleDungeonCondition:: failed', dungeonNo, reasonDic)
            return

        _hasCast = extraData.get('hasCast', False)
        _spaceTemplateNo = gameconst.SpaceType.getSingleDungeonSpaceRange(dungeonNo)[0]
        if not _hasCast and utils.checkComplexTeleportNeedCast(self.spaceNo, _spaceTemplateNo, gameconst.ComplexTeleportEnum.ENTER, None, owner=self):
            self.enterSpaceCommonNeedCast('_enterSingleDungeonAfterCast', (dungeonNo, extraData))
            return

        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("onCheckSingleDungeonCondition:: teleport locked", self.teleportGlobalLockRlsT)
            return
        self.acquireGlobalTeleportLock(now=_now)
        _spaceUUID = 0
        if self.spaceMgr:
            _spaceUUID = self.spaceMgr.spaceUUID
        extraData['inSpaceUUID'] = _spaceUUID
        gameengine.getDungeonStubByDungeonNo(
            dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE).applyCreateDungeon(
            self.base, self.gbId, self.teamId, extraData)
        self.resetStatisticsData()

    def _checkEnterSingleDungeon(self, dunNo, src=None, checkSameDungeon=True):
        if dunNo not in GP_GPD.datas:
            LOG_INFO('{0} invalid'.format(dunNo))
            return False

        if checkSameDungeon and formula.parseDungeonNoBySpaceNo(self.spaceNo) == dunNo:
            LOG_WARN('_checkEnterSingleDungeon::repeat enter same dungeon', dunNo, self.spaceNo)
            return False

        if not self.checkCrtMapCanEnterDungeon():
            return False

        dungeonInfo = GP_GPD.datas[dunNo]
        if not gameconst.DungeonTypeJudge.isSingleDungeon(dungeonInfo['type'],
                                                     dungeonInfo['enterType']):
            LOG_INFO('{0} not single dungeon'.format(dunNo))
            # TODO()(DUNGEON_EXTEND): add message
            return False

        if not self.checkConflictState(C_C_DD.datas.teleport):
            LOG_INFO('checkConflictState error')
            return False

        # 【【任务】战斗状态&&进入副本判断】
        if not dungeonInfo["fightConflict"] and self.hasState(gameconst.StateEnum.Fighting):
            LOG_INFO("_checkEnterSingleDungeon:: fight state failed")
            self.showMsg(M_M_DD.datas.enterDunFailFightSingle, [])
            return False

        if not self.canDoCompleteTeleport(noErrorMsg=True, judgeLeaveSrc=src):
            LOG_WARN('_checkEnterSingleDungeon::can\'t enter space from current spaceNo', self.spaceNo)
            return False

        return True

    def onSingleDungeonSpaceReady(self, spaceBox, spaceMgrBox, spaceMgrId, spaceNo, playerBox, playerGbId, teamUUID, extraData):
        self.readyUseItemAndEnterSingleDungeon(
            0, spaceBox, spaceMgrBox, spaceMgrId,
            spaceNo, playerBox, playerGbId, teamUUID, extraData)

    def readyUseItemAndEnterSingleDungeon(self, state,
                                          spaceBox, spaceMgrBox, _, spaceNo, playerBox,
                                          playerGbId, teamUUID, extra):
        if state != 0:
            LOG_ERR('Enter singleDungeon Failed, use item error: code={}, spaceNo={}'.format(state, spaceNo))
            return

        eCtx = {'spaceMgrBox': spaceMgrBox,
                    'spaceBox': spaceBox,
                    'playerBox': playerBox,
                    'playerGbId': playerGbId,
                    'teamUUID': teamUUID,
                    'extra': extra}
        lCtx = {}
        src = extra.get('src')
        context = {'e': eCtx, 'l': lCtx, 'src': src, 'hasCheck': extra.get('hasCheck', False), 'hasCast': extra.get('hasCast', False)}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(lCtx, judgeLeaveSrc=src)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('readyUseItemAndEnterSingleDungeon::fatal error when try to enter single dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("readyUseItemAndEnterSingleDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return

        if spaceMgrBox:
            data = {
                'name': self.name,
                'school': self.school,
                'level': self.level,
                'sex': self.sex,
                'gbId': self.gbId,
                'eId': self.id,
            }
            spaceMgrBox.cell.doEnterSingleDungeon(self, playerGbId, extra.get('spaceUUID', 0), spaceBox, data)
        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    @gamedecorator.limitcall(5)
    def leaveSingleDungeon(self, exposed, dungeonNo):
        if not self._isMyself(exposed):
            return

        if not self.newbieAllowLeave():
            return

        _src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.doLeaveSingleDungeon(dungeonNo, _src, 'client leave')

    def leaveTutorialIsComplete(self, dungeonNo):
        LOG_INFO('leaveTutorialIsComplete:', dungeonNo)
        _src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.doLeaveSingleDungeon(dungeonNo, _src, 'client leave')

    def selfLeaveSingleDungeon(self, dungeonNo, src):
        LOG_INFO('selfLeaveSingleDungeon:', dungeonNo, src)
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("selfLeaveSingleDungeon:: teleport locked", dungeonNo, src, self.teleportGlobalLockRlsT)
            return
        self.acquireGlobalTeleportLock(now=_now)
        self.doLeaveSingleDungeon(dungeonNo, src, 'server leave')

    def doLeaveSingleDungeon(self, dungeonNo, src, reason):
        LOG_INFO('wl: doLeaveSingleDungeon', dungeonNo, src, reason)
        if not formula.inDungeonScene(self.spaceNo):
            return

        spaceType = self._getParamBydungeonNo(dungeonNo, 'type')
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

        _mMapId, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        lCtx = {'spaceMgrBox': self.spaceMgr.base, 'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID}
        eCtx = {}
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        if formula._isInnerDemonSpace(spaceNo):
            self.enterCubeByMapIds([formula.fetchMapId(spaceNo)], {'hasCheck': True, 'enterCubeType': gameconst.ENTER_CUBE_HAS_LEFT_TIME, 'hasCast': False})
            return
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)

        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        # gamelog.singleDungeonLogger.leaveDungeon(
        #     self.spaceMgr.dungeonPlayMode, self.gbId, dungeonNo=dungeonNo)

    def doLeaveSingleDungeonWithDstPos(self, dstNo, dstPos, dstDir):
        """task使用, 这个接口只用于从单人副本返回到大世界分线"""
        LOG_INFO('in doLeaveSingleDungeonWithDstPos: 1', self.spaceNo, dstNo, dstPos, dstDir)
        if not formula.inDungeonScene(self.spaceNo):
            LOG_INFO('in doLeaveSingleDungeonWithDstPos: 2', self.spaceNo, dstNo, dstPos, dstDir)
            return

        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        spaceType = self._getParamBydungeonNo(dungeonNo, 'type')
        if self.autoCombat and GP_GPD.datas[dungeonNo].get('leaveDungeonDisableAutoFight', 0):
            self.stopAutoCombat(self.id)

        lCtx = {
            'spaceUUID': self.spaceMgr.dungeonPlayMode.spaceUUID,
            'spaceMgrBox': self.spaceMgr.base, 
            'overwrite': {
                'position': dstPos, 
                'direction': dstDir,
            }
        }

        context = {'e': {}, 'l': lCtx}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)
        spaceNo = formula.combineLineSpaceNo(dstNo)
        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

    def isInSingleDungeon(self):
        if not formula.inDungeonScene(self.spaceNo):
            return False

        dungeonNo = formula.fetchMapId(self.spaceNo)

        if dungeonNo not in GP_GPD.datas:
            LOG_ERR("isInTeamDungeon::can't find dungeonNo in DLL sheet")
            return False

        dungeonSpaceType = GP_GPD.datas[dungeonNo]['type']
        dungeonEnterType = GP_GPD.datas[dungeonNo]['enterType']

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
        
        dungeonSpaceType = GP_GPD.datas[dstNo]['type']
        dungeonEnterType = GP_GPD.datas[dstNo]['enterType']

        if dstNo == formula.fetchMapId(self.spaceNo):
            self.telToPos(dstPos, _dir)
        
        elif gameconst.DungeonTypeJudge.isSingleDungeon(dungeonSpaceType, dungeonEnterType):
            src = dungeonSrc.DungeonFromFlowController(self.base, self.gbId)
            self._enterSingleDungeon(dstNo, src, {'position': (dstPos.x, dstPos.y, dstPos.z)})

    def checkChallengeInnerDemon(self, *args):
        LOG_DBG("checkChallengeInnerDemon", args)
        return CollectionCheckContext.CollectionCheckInnerDemon(*args)
    
    def checkChallengeInnerDemonCD(self):
        now = utils.curTS()
        nextTime = self.getPersistentMiscProp(gameconst.EntityPropsEnum.innerDemonCDTimestamp, 0)
        if nextTime > now:
            self.showMsg(M_M_DD.datas.cube_innerDemonCDMsg, [str(nextTime - now)])
            return False
        
        return True
