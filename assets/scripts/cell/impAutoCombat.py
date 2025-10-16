import random

from KBEDebug import *
import KBEngine

import formula
import gameconst
import gameengine
import utils
import gamedecorator
import gametimer
import Math
import sMath
import dataUtils
import math

import message_Message_def as MMD
import conflict_conflict_def as CCD
import gamePlay_gamePlay as DDID
import const_const as CONST
import teamMatch_matchConfig as TMMCD
import skill_skill as SSD

class AutoCombatRet(object):
    FAIL_SKILL = 0
    FAIL_TARGET = 1
    FAIL_USE_SKILL = 2
    SUCCESS_USE_SKILL = 3
    SUCCESS_FIGHT = 4

class DoAutoCombatReason(object):
    TICK = 1
    USE_SKILL = 2
    CHANGE_TARGET = 3
    MOVE_OVER = 4

class ImpAutoCombat(object):
    def __init__(self):
        self.autoCombat = gameconst.AutoCombatState.Idle
        self.followtSuspendReason = gameconst.SuspendFollowReason.Default
        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReason.Default
        self.autoCombatInfo['aiVars'] = {}
        self.autoCombatInfo['moveController'] = 0
        self.autoCombatInfo['targetEnemyId'] = 0
        self.controlledByReasonDic = {}
        self.pyAddTimer(1, 5, gametimer.AVATAR_CHECK_AVERAGE_LOAD_TIMER)

    def sendAutoCombat(self):
        DEBUG_MSG("sendAutoCombat")
        if self.autoCombat and self.autoCombatInfo.get('timer', 0):
            self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

    def captainEnterFightingStateChangeAutoCombat(self):
        self._tryChangeCombatStateFollowTeamCaptain(gameconst.AutoCombatState.Fighting, gameconst.ChangeAutoCombatReason.CaptainEnterFightingState)

    def enterTeamCaptainTrap(self, captainCombatState):
        self._tryChangeCombatStateFollowTeamCaptain(captainCombatState, gameconst.ChangeAutoCombatReason.CaptainTrap)

    def tryChangeCombatStateFollowTeamCaptain(self, captainCombatState):
        self._tryChangeCombatStateFollowTeamCaptain(captainCombatState, gameconst.ChangeAutoCombatReason.CaptainChange)

    def _tryChangeCombatStateFollowTeamCaptain(self, captainCombatState, changeReason):
        DEBUG_MSG("tryChangeCombatStateFollowTeamCaptain ", captainCombatState, changeReason)
        if self.gbId == self.getCaptainGBID():
            return
        if self.autoCombat == captainCombatState:
            return
        if self.followCaptain == gameconst.TeamFollowState.Idle:
            return
        if self.isDie():
            return

        if changeReason == gameconst.ChangeAutoCombatReason.CaptainChange:
            dstPos = self.getCaptainPosition()
            if dstPos and sMath.distance2D(self.position, dstPos) > gameconst.DEFAULT_AOI + gameconst.DEFAULT_HYST:
                return
            if captainCombatState == gameconst.AutoCombatState.Fighting:
                DEBUG_MSG("_tryChangeCombatStateFollowTeamCaptain  _startAutoCombat")
                self._startAutoCombat()
            if captainCombatState == gameconst.AutoCombatState.Suspending:
                DEBUG_MSG("_tryChangeCombatStateFollowTeamCaptain  _startAutoCombat")
                self._startAutoCombat()
            elif captainCombatState == gameconst.AutoCombatState.Idle and self.autoCombat == gameconst.AutoCombatState.Fighting:
                DEBUG_MSG("_tryChangeCombatStateFollowTeamCaptain  removeState")
                self.removeState(gameconst.State.autoFight)
            elif captainCombatState == gameconst.AutoCombatState.Idle and self.autoCombat == gameconst.AutoCombatState.Suspending:
                DEBUG_MSG("_tryChangeCombatStateFollowTeamCaptain  removeState")
                self.removeState(gameconst.State.autoFight)

        elif changeReason == gameconst.ChangeAutoCombatReason.CaptainEnterFightingState:
            dstPos = self.getCaptainPosition()
            captainSpaceNo = self.getCaptainSpaceNo()
            if captainSpaceNo != self.spaceNo or not dstPos or \
                    sMath.distance2D(self.position, dstPos) > gameconst.DEFAULT_AOI + gameconst.DEFAULT_HYST:
                return
            if captainCombatState == gameconst.AutoCombatState.Fighting:
                DEBUG_MSG("_tryChangeCombatStateFollowTeamCaptain  _startAutoCombat CaptainEnterFightingState")
                self._startAutoCombat()

        elif changeReason == gameconst.ChangeAutoCombatReason.CaptainTrap and self.checkFollowCaptain():
            self._startAutoCombat(True, gameconst.SuspendAutoCombatReason.ForceFollow)

    def checkFollowCaptain(self):
        if self.followCaptain == gameconst.TeamFollowState.Follow:
            return True
        return False

    @gamedecorator.crossServer
    @utils.isMyself
    def startAutoCombat(self, exposed, isSuspend):
        DEBUG_MSG('startAutoCombat', exposed, isSuspend)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())

        dstPos = self.getCaptainPosition()
        if self.followCaptain in (gameconst.TeamFollowState.Follow, gameconst.TeamFollowState.Suspending) and \
                dstPos and sMath.distance2D(self.position, dstPos) > gameconst.DEFAULT_AOI:
            return

        if isSuspend:
            self._startAutoCombat(isSuspend, gameconst.SuspendAutoCombatReason.ClientBreak)
        else:
            self._startAutoCombat()

    def _startAutoCombat(self, isSuspend=False, suspendReason=gameconst.SuspendAutoCombatReason.Default, isFightBack=False):
        DEBUG_MSG("_startAutoCombat ", isSuspend, suspendReason)
        if not self.checkConflictState(CCD.datas.autoFighting, True):
            return

        if self.isDie():
            INFO_MSG('startAutoCombat: avatar died')
            return

        if formula.spaceForbidAutoFight(self.spaceNo):
            self.showMsg(MMD.datas.autoFight_forbid, [])
            return

        self.autoCombatInfo['moveController'] = 0
        self.autoCombatInfo['notTarget'] = False
        if isSuspend:
            self.autoCombatSuspendReason = suspendReason
            self.autoCombatInfo['suspendTime'] = utils.getTimestamp64()
            self.autoCombat = gameconst.AutoCombatState.Suspending
        else:
            self.suspendFollow(gameconst.SuspendFollowReason.AutoCombat)
            self.autoCombatInfo['suspendTime'] = 0
            self.autoCombat = gameconst.AutoCombatState.Fighting
            self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

        if self.teamInfo.howManyMember() > 1 and self.gbId == self.teamInfo.getCaptainGbId():
            self.teamInfo.allMembersCellDo('tryChangeCombatStateFollowTeamCaptain', (self.autoCombat, ))

        self.client.onStartAutoCombat()
        self.setState(gameconst.State.autoFight)
        if isFightBack:
            self._updateCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK, True)

        if not self.autoCombatInfo.get('timer', 0):
            self.autoCombatInterval = CONST.datas['autoFightTick']['value']
            self.autoCombatInfo['timer'] = self.pyAddTimer(0, CONST.datas['autoFightTick']['value'], gametimer.AUTO_COMBAT_CHECK)

        if self.getCommonFlagCell(gameconst.AvatarFlagCell.RETURN_IDLE):
            self.combatReturnInfo.spaceNo = self.spaceNo
            self.combatReturnInfo.pos = tuple(self.position)

    @gamedecorator.crossServer
    @utils.isMyself
    def stopAutoCombat(self, exposed):
        DEBUG_MSG('stopAutoCombat', exposed)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())
        self.autoCombatInfo.pop('priorityTargetEnemyId', None)
        self.removeState(gameconst.State.autoFight)

    def doFollowCaptainStopAutoCombat(self):
        dstPos = self.getCaptainPosition()
        if dstPos and sMath.distance2D(self.position, dstPos) > gameconst.DEFAULT_AOI:
            self.removeState(gameconst.State.autoFight)

    def selfStopAutoCombat(self, reason=''):
        DEBUG_MSG("selfStopAutoCombat::", reason)
        if self.hasState(gameconst.State.autoFight):
            self.removeState(gameconst.State.autoFight)

    def _stopAutoCombat(self):
        INFO_MSG("_stopAutoCombat  ")
        self._cancelAutoCombatMoveController()
        if self.autoCombatInfo.get('timer', 0):
            self.pyDelTimer(self.autoCombatInfo['timer'], gametimer.AUTO_COMBAT_CHECK)
        self.autoCombatInfo['timer'] = 0
        self.autoCombatInfo['suspendTime'] = 0
        self.autoCombatInfo['skill'] = None
        self.autoCombatInfo['targetId'] = 0
        self.autoCombatInfo['notTarget'] = False
        self.autoCombatInfo['targetEnemyId'] = 0
        self.autoCombatInfo['moveToTargetFailTimes'] = 0
        self.autoCombatInfo['waitAfterUseSkill'] = False
        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReason.Default
        self.autoCombat = gameconst.AutoCombatState.Idle
        self.releaseControlleBy(gameconst.ControlledByReason.AutoCombat)

        self._updateCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK, False)

        if self.teamInfo.howManyMember() > 1 and self.gbId == self.teamInfo.getCaptainGbId() \
                and not self.hasState(gameconst.State.Death):
            self.teamInfo.allMembersCellDo('tryChangeCombatStateFollowTeamCaptain', (gameconst.AutoCombatState.Idle, ))

        self.client and self.client.onStopAutoCombat()

    def setControlleByReason(self, reason):
        reason = str(reason)
        DEBUG_MSG("setControlleByReason begin", self.controlledBy, self.controlledByReasonDic, reason)
        self.setControlledBy(True)
        self.controlledByReasonDic[reason] = utils.getNow()
        DEBUG_MSG("setControlleByReason end ", self.controlledBy, self.controlledByReasonDic, reason)

    def releaseControlleBy(self, reason):
        DEBUG_MSG("releaseControlleBy begin ", self.controlledBy, self.controlledByReasonDic, reason)
        reason = str(reason)
        if reason in self.controlledByReasonDic:
            self.controlledByReasonDic.pop(reason)

        if len(self.controlledByReasonDic) == 0:
            self.setControlledBy(False)
        DEBUG_MSG("releaseControlleBy end ", self.controlledBy, self.controlledByReasonDic, reason)

    def setControlledBy(self, isServerControl):
        DEBUG_MSG("setControlledBy ", isServerControl, self.hasState(gameconst.State.serverControl), self.controlledBy)
        if isServerControl:
            if not self.hasState(gameconst.State.serverControl):
                self.setState(gameconst.State.serverControl)
        else:
            if self.hasState(gameconst.State.serverControl):
                self.removeState(gameconst.State.serverControl)

        # if self.setControlledByTimer:
        #     self._cancelCallback(self.setControlledByTimer, gametimer.TIMER_TAG_SET_CONTROLLED_BY)
        #     self.setControlledByTimer = 0
        #
        # self.setControlledByTimer = self._callback(0.1, '_setControlledBy', (isServerControl, ),
        #                                            gametimer.TIMER_TAG_SET_CONTROLLED_BY, 'setControlledByTimer')

    @gamedecorator.crossServer
    @utils.isMyself
    def breakFollowAndAutoCombat(self, exposed):
        DEBUG_MSG('breakFollowAndAutoCombat')
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())

        if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
            self.stopAutoCombat(self.id)
            return

        self.suspendFollow(gameconst.SuspendFollowReason.ClientBreak)
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.ClientBreak)

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def selectAutoCombatPriorityTarget(self, exposed, targetId):
        DEBUG_MSG('selectAutoCombatPriorityTarget', targetId)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())
        # 优先攻击目标，这里的攻击目标id是怪物的模版id（monsterId）
        self.autoCombatInfo['priorityTargetEnemyId'] = targetId


    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def selectAutoCombatTarget(self, exposed, targetId):
        DEBUG_MSG('selectAutoCombatTarget', targetId)
        self.setTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, utils.getNow())

        target = KBEngine.entities.get(targetId, None)
        if not target:
            return
        if exposed == targetId or sMath.distance2D(self.position, target.position) >= self.getViewRadius():
            return
        if target.IsCombatUnit and utils.checkTargetType('Enemy', self, target):
            self.setSelectedTargetId(targetId)
            self.autoCombatInfo['targetId'] = targetId
            self.autoCombatInfo['targetEnemyId'] = targetId
            self.cancelMoveController()
            self.doAutoCombat(DoAutoCombatReason.CHANGE_TARGET)

    def suspendAutoCombat(self, suspendReason):
        DEBUG_MSG('suspendAutoCombat', self.autoCombat, self.autoCombatSuspendReason, suspendReason)
        if not self.autoCombat:
            return

        self.autoCombatSuspendReason = suspendReason
        self.autoCombatInfo['suspendTime'] = utils.getTimestamp64()
        if self.autoCombat == gameconst.AutoCombatState.Suspending:
            return

        self.autoCombat = gameconst.AutoCombatState.Suspending
        self._cancelAutoCombatMoveController()
        self.releaseControlleBy(gameconst.ControlledByReason.AutoCombat)

    def recoverAutoCombat(self, oldSpaceNo, suspendReason):
        DEBUG_MSG('recoverAutoCombat ', self.autoCombat, oldSpaceNo, suspendReason, self.autoCombatSuspendReason )
        if self.autoCombatSuspendReason != suspendReason:
            return
        if self.autoCombat != gameconst.AutoCombatState.Suspending:
            return

        mapId = formula.getMapId(self.spaceNo)
        sceneInfo = DDID.datas.get(mapId, None)
        if sceneInfo and not sceneInfo['ifAutoFight']:
            self.stopAutoCombat(self.id)
            return

        self.suspendFollow(gameconst.SuspendFollowReason.AutoCombat)
        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReason.Default
        self.autoCombatInfo['suspendTime'] = 0
        self.autoCombatInfo['notTarget'] = False
        self.autoCombat = gameconst.AutoCombatState.Fighting
        self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

    def _cancelAutoCombatMoveController(self):
        if self.autoCombatInfo.get('moveController', 0):
            self.cancelController(self.autoCombatInfo['moveController'])
            self.setMoveController(0)

    def checkClientBreakRecover(self):
        if utils.getTimestamp64() > self.autoCombatInfo['suspendTime'] + CONST.datas['autoFightEnterTime']['value']*1000 \
                and not self.hasState(gameconst.State.Casting) and not self.hasState(gameconst.State.Channeling) \
                and not self.hasState(gameconst.State.moveChannel) \
                and not self.hasState(gameconst.State.Fall) \
                and not self.hasState(gameconst.State.Moving):
            return True
        return False

    def checkFollowRecover(self):
        if self.autoCombat == gameconst.AutoCombatState.Idle:
            return False
        if self.followCaptain == gameconst.TeamFollowState.Idle:
            return True
        captainSpaceNo = self.getCaptainSpaceNo()
        if captainSpaceNo and formula.spaceInWorldLine(captainSpaceNo) and captainSpaceNo != self.spaceNo:
            return False
        dstPos = self.getCaptainPosition()
        if self.autoCombat == gameconst.AutoCombatState.Fighting and self.hasState(gameconst.State.Fighting):
            if self.autoCombatInfo['notTarget']:
                return False
            if dstPos and sMath.distance2D(self.position, dstPos) > CONST.datas['autoFightFollowRange']['value']:
                return False
            else:
                return True
        if dstPos and sMath.distance2D(self.position, dstPos) > self.getFollowCaptainRealDistance() + 1:
            return False
        return True

    def checkForceFollowRecover(self):
        if self.followCaptain != gameconst.TeamFollowState.Follow:
            return True
        captainSpaceNo = self.getCaptainSpaceNo()
        if captainSpaceNo and formula.spaceInWorldLine(captainSpaceNo) and captainSpaceNo != self.spaceNo:
            return False
        dstPos = self.getCaptainPosition()
        if dstPos and sMath.distance2D(self.position, dstPos) > self.getFollowCaptainEndDistance():
            return False
        return True

    def autoCombatTick(self):
        if self.autoCombat == gameconst.AutoCombatState.Suspending:
            if self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReason.ClientBreak:
                if not self.checkClientBreakRecover():
                    return
                self.recoverAutoCombat(self.spaceNo, self.autoCombatSuspendReason)

            elif self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReason.Follow:
                if not self.checkFollowRecover():
                    return
                self.recoverAutoCombat(self.spaceNo, self.autoCombatSuspendReason)

            elif self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReason.ForceFollow:
                if not self.checkForceFollowRecover():
                    return
                self.recoverAutoCombat(self.spaceNo, self.autoCombatSuspendReason)
        elif self.autoCombat == gameconst.AutoCombatState.Fighting:
            self.doAutoCombat(DoAutoCombatReason.TICK)

    def autoCombatCheckUseSkill(self, skillId):
        skill = self.autoCombatInfo.get('lastSkill', None)
        if not skill:
            return
        if skill.skillId != skillId:
            return

        if self.autoCombatInterval != CONST.datas['autoFightTick']['value']:
            return

        if self.autoCombatInfo['skillCD'] > utils.getTimestamp64():
            cdTime = (self.autoCombatInfo['skillCD'] - utils.getTimestamp64()) / 1000 + 0.2
        else:
            cdTime = 0.2

        self._callback(cdTime, 'skillFinishDoAutoCombat', (), gametimer.TIMER_TAG_DO_AUTO_COMBAT)
        self.autoCombatInfo['waitAfterUseSkill'] = True

    def skillFinishDoAutoCombat(self):
        if self.autoCombat != gameconst.AutoCombatState.Fighting:
            self.autoCombatInfo['waitAfterUseSkill'] = False
            return
        self.doAutoCombat(DoAutoCombatReason.USE_SKILL)

    def _returnIdle(self):
        if not self.getCommonFlagCell(gameconst.AvatarFlagCell.RETURN_IDLE):
            return False

        if self.combatReturnInfo.spaceNo != self.spaceNo:
            return False

        if sMath.distance2D(self.position, self.combatReturnInfo.pos) < 1:
            return False

        if self.isDie():
            return False

        dstPos = self.combatReturnInfo.pos
        direction = sMath.vector3WithoutY(dstPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)

        self.autoCombatInfo['moveController'] = self.scriptNavigate(dstPos, self.speed)
        if self.autoCombatInfo['moveController']:
            # self.controlledBy = None
            self.setState(gameconst.State.Moving)
            self.autoCombatInfo['moveToTargetFailTimes'] = 0

        return True

    def doAutoCombat(self, reason):
        if self._checkExitFightBack():
            self.stopAutoCombat(self.id)
            return

        if self.autoCombatInfo.get('waitAfterUseSkill', False):
            if reason != DoAutoCombatReason.USE_SKILL:
                return
            self.autoCombatInfo['waitAfterUseSkill'] = False

        if self.autoCombat != gameconst.AutoCombatState.Fighting:
            return

        if self.hasState(gameconst.State.Teleporting) or self.hasState(gameconst.State.clientPick):
            return

        if utils.getTimestamp64() < self.autoCombatInfo.get('skillCD', 0):
            return

        if not self.useTargetTypeCacheFlag:
            viewRadius = self.getViewRadius() if self.IsAvatar else gameconst.DEFAULT_AOI
            for e in self.entitiesInRange(viewRadius):
                if e.IsCombatUnit:
                    utils.isEnemy(self, e)
                    utils.isFriend(self, e)

            if self.spaceMgr:
                _ents = self.spaceMgr.getEntitiesByTag('largeEnt')
                for e in _ents:
                    if e.IsCombatUnit:
                        utils.isEnemy(self, e)
                        utils.isFriend(self, e)

            self.useTargetTypeCacheFlag = True
            self.stopCacheTargetTypeTimeId = self._callback(30, 'resetTargetTypeCacheFlag', (),
                                                        gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG, 'stopCacheTargetTypeTimeId')
            if not self.checkTargetTypeTimeId:
                self.checkTargetTypeTimeId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
        else:
            if self.stopCacheTargetTypeTimeId:
                self._cancelCallback(self.stopCacheTargetTypeTimeId, gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG)
                self.stopCacheTargetTypeTimeId = self._callback(30, 'resetTargetTypeCacheFlag', (),
                                                                gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG, 'stopCacheTargetTypeTimeId')

        if len(self.enemyCacheSet) <= 0:
            self._returnIdle()
            return

        fightRet = self.normalFight()
        # DEBUG_MSG("doAutoCombat  fightRet", fightRet)
        if fightRet == AutoCombatRet.FAIL_TARGET:
            if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
                self.stopAutoCombat(self.id)
                return

            self._returnIdle()

    def changePKModeResetTargetId(self):
        DEBUG_MSG("changePKModeResetTargetId")
        targetId = self.autoCombatInfo.get('targetId', 0)
        target = KBEngine.entities.get(targetId, None)
        if target and target.IsCombatUnit and utils.checkTargetType('Enemy', self, target):
            return
        self.autoCombatInfo['targetId'] = 0
        self._cancelAutoCombatMoveController()

    def normalFight(self):
        if not self.checkConflictState(CCD.datas.useSkill, False):
            return AutoCombatRet.FAIL_USE_SKILL

        skill = self.autoCombatInfo.get('skill', None)
        targetId = self.autoCombatInfo.get('targetId', 0)
        target = KBEngine.entities.get(targetId, None)
        if not skill or not target or target.spaceNo != self.spaceNo:
            _enemy = self.getNearestEnemy()
            if not _enemy:
                # 进入自动战斗后，若范围内没有可选目标，那么不会自动释放技能。
                return AutoCombatRet.FAIL_TARGET

            skill = self._getCombatSkill()
            self.autoCombatInfo['skill'] = skill
            if not skill:
                return AutoCombatRet.FAIL_SKILL
            target = self._getCombatTarget(skill)
            if not target:
                self.autoCombatInfo['notTarget'] = True
                return AutoCombatRet.FAIL_TARGET
            self.autoCombatInfo['notTarget'] = False
            self.autoCombatInfo['targetId'] = target.id

        ignoreReasons = gameconst.UseSkillCheck.NEED_CAST | gameconst.UseSkillCheck.OUT_OF_RANGE
        ret = skill.checkUseSkill(self, target.id, ignoreReasons)
        if ret == gameconst.UseSkillCheck.CHEKC_OK:
            if self.isInSkillScope(target, skill):
                self._cancelAutoCombatMoveController()
                if not self.useCombatSkill():
                    self.autoCombatInfo['skill'] = None
                    self.autoCombatInfo['targetId'] = 0
                    return AutoCombatRet.FAIL_USE_SKILL
            else:
                if self.autoCombatInfo['moveController'] == 0:
                    self.moveToCombatTarget(target, skill)
        else:
            self.autoCombatInfo['skill'] = None
            self.autoCombatInfo['targetId'] = 0
            return AutoCombatRet.FAIL_USE_SKILL

        return AutoCombatRet.SUCCESS_FIGHT

    def resetAutoCombatSkillInfo(self):
        self.autoCombatInfo['skill'] = None
        self.autoCombatInfo['targetId'] = 0
        self.autoCombatInfo['lastSkill'] = None

    def _needFollowCaptain(self):
        captainSpaceNo = self.getCaptainSpaceNo()
        if captainSpaceNo and formula.spaceInWorldLine(captainSpaceNo) and captainSpaceNo != self.spaceNo:
            return True
        dstPos = self.getCaptainPosition()
        if self.autoCombat == gameconst.AutoCombatState.Idle:
            if dstPos and sMath.distance2D(self.position, dstPos) > CONST.datas['autoFightFollowRange']['value']:
                return True
        if dstPos and sMath.distance2D(self.position, dstPos) > gameconst.DEFAULT_AOI:
            return True
        return False

    def _getCombatTarget(self, skill):
        target = None
        targetType = skill.getTarget(skill.skillId)
        skillRange = skill.getRange(self, skill.skillId)
        if targetType == 'Enemy':
            target = self.getNearestEnemy()
        elif targetType == 'Self':
            target = self
        elif targetType in ('Friend', 'FriendExGB'):
            target = self.getTeamTarget(True, skill)
        elif targetType == 'FriendExS':
            target = self.getTeamTarget(False, skill)
        elif targetType == 'None':
            target = self.getNoneTypeTarget(skill)
        elif targetType == 'Any':
            target = self.getEffectSelectTarget(skill)
        elif targetType == 'AnyExGB':
            target = self.getRandomTarget(skillRange, 'AnyExGB')
        return target

    def getNoneTypeTarget(self, skill):
        if skill.getEffectTarget(skill.skillId) == 'Self':
            return self

        if skill.hasTag(gameconst.SkillTag.Hot) or skill.hasTag(gameconst.SkillTag.Heal):
            target = self.getTeamTarget(True, skill)
        else:
            target = KBEngine.entities.get(self.selectedTargetId, None)
            if not target:
                self.setSelectedTargetId(0)
            if not target or not target.IsCombatUnit or target.isDie() or target.spaceNo != self.spaceNo \
                    or sMath.distance2D(target.position, self.position) > CONST.datas['autoFightRange']['value'] \
                    or not utils.checkTargetType('Enemy', self, target) \
                    or not utils.checkCombatRangeY(self, target):
                target = self.getEffectSelectTarget(skill)
        return target

    def getEffectSelectTarget(self, skill):
        if skill.getEffectTarget(skill.skillId) in ('Friend', 'Self', 'Any', 'FriendExGB'):
            if skill.hasTag(gameconst.SkillTag.Hot) or skill.hasTag(gameconst.SkillTag.Heal):
                return self.getTeamTarget(True, skill)
            return self
        else:
            return self.getNearestEnemy()

    def getTeamTarget(self, includeSelf, skill):
        target = None
        if includeSelf:
            target = self
        if self.teamInfo.howManyMember() <= 0:
            return target
        minHpPercent = -1
        for teamMemberVal in self.teamInfo.teamPlayerDic.values():
            if not teamMemberVal.playerBox:
                continue
            mEnt = KBEngine.entities.get(teamMemberVal.playerBox.id)
            if not mEnt:
                continue
            if not includeSelf and mEnt.id == self.id:
                continue
            if not self.isInSkillScope(mEnt, skill):
                continue
            if mEnt.isDie() or mEnt.spaceNo != self.spaceNo:
                continue
            if sMath.distance2D(mEnt.position, self.position) > CONST.datas['autoFightRange']['value']:
                continue
            if not utils.checkCombatRangeY(self, mEnt):
                continue
            hpPercent = mEnt.hp / mEnt.fullHp
            if minHpPercent != -1 and hpPercent > minHpPercent:
                continue
            minHpPercent = hpPercent
            target = mEnt
        return target

    def getTeamTargets(self):
        _targets = []
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDic.items():
            if playerGBID == self.gbId or not playerBaseVal.playerBox:
                continue

            teamMember = KBEngine.entities.get(playerBaseVal.playerBox.id)
            if not teamMember:
                continue

            _target = KBEngine.entities.get(teamMember.selectedTargetId)
            if not _target:
                continue

            _targets.append(_target.id)

        return _targets

    def _checkFightBack(self, srcEntId):
        if not self.getCommonFlagCell(gameconst.AvatarFlagCell.AUTO_FIGHT_BACK):
            return

        if self.hasState(gameconst.State.autoFight):
            return

        if self.fightBackTimerId:
            return

        if self.hasState(gameconst.State.Moving):
            return

        _ent = KBEngine.entities.get(srcEntId)
        if not _ent:
            return

        _ent = utils.getHostEntity(_ent)
        if _ent.id == self.id:
            return

        if not _ent.isAttackable(self):
            return

        self.fightBackTarget = _ent.id
        self.setSelectedTargetId(_ent.id)

        self.fightBackTimerId = self._callback(
            gameconst.FIGHT_BACK_DELAY,
            '_startFightBack',
            (),
            gametimer.TIMER_TAG_FIGHT_BACK,
            'fightBackTimerId')

    def _startFightBack(self):
        _ts = self.getTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, 0)
        _now = utils.getNow()
        if _now - _ts < gameconst.FIGHT_BACK_DELAY:
            return

        if self.hasState(gameconst.State.Moving):
            return

        self._startAutoCombat(isFightBack=True)

    def _checkExitFightBack(self):
        if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
            _ts = self.getTempMiscProp(gameconst.AvatarProps.AvatarActiveTimestamp, 0)
            _now = utils.getNow()
            if _now - _ts < gameconst.FIGHT_BACK_DELAY:
                return True

        return False

    def getNearestEnemy(self):
        # 反击模式中只能攻击反击目标
        target = None
        _inFightBack = self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK)
        if _inFightBack:
            target = KBEngine.entities.get(self.fightBackTarget)

        # 攻击正在打得目标
        if not target:
            targetId = self.autoCombatInfo.get('targetEnemyId', 0)
            target = KBEngine.entities.get(targetId, None)

        # 攻击锁定目标
        if not target and self.selectedTargetId:
            target = KBEngine.entities.get(self.selectedTargetId, None)
            if not target:
                self.setSelectedTargetId(0)

        # 攻击PVP玩家(这个先不做了，太耗了)
        # 攻击仇恨目标
        _hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord, {})

        if not target or target.spaceNo != self.spaceNo or not target.IsCombatUnit\
                or sMath.distance2D(target.position, self.position) > CONST.datas['autoFightRange']['value'] \
                or not utils.checkTargetType('Enemy', self, target)\
                or not utils.checkCombatRangeY(self, target):
            # 调整后：下面是顺序
            #反击
            #正在打得目标
            #玩家锁定目标
            #仇恨目标
            #任务目标(priorityTargetEnemyId)
            #同伴选择
            #就近
            targetsList = []
            entityIds = self.getTargetIdsByTargetType('Enemy')
            priorityTargetEnemyId = self.autoCombatInfo.get('priorityTargetEnemyId', None)
            _teamTargetIds = self.getTeamTargets()
            _maxVal = None
            target = None
            for eId in entityIds:
                entity = KBEngine.entities.get(eId)
                if not entity:
                    continue
                if entity.id == self.id:
                    continue
                if not utils.checkCombatRangeY(self, entity):
                    continue
                if _inFightBack and eId not in _hateRecord:
                    # 反击过程中，不攻击非仇恨目标
                    continue
                if entity.IsCombatUnit and utils.checkCachedTargetType('Enemy', self, entity):
                    targetsList.append(entity)
                    _val = (
                        # 1.仇恨目标
                        _hateRecord.get(eId, 0),
                        # 2.任务目标
                        1 if entity.IsMonster and entity.monsterId == priorityTargetEnemyId else 0,
                        # 3.队伍目标
                        1 if eId in _teamTargetIds else 0,
                        # 4.距离
                        -sMath.distance2DToCompareFrom3DPosition(self.position, entity.position)
                    )

                    if _maxVal is None:
                        _maxVal = _val
                        target = entity

                    elif _maxVal < _val:
                        _maxVal = _val
                        target = entity

            if not target:
                self.autoCombatInfo['targetEnemyId'] = 0
            else:
                self.autoCombatInfo['targetEnemyId'] = target.id
                return target

        return target

    def getRandomTarget(self, skillRange, targetType):
        if skillRange <= 0:
            return
        target = KBEngine.entities.get(self.selectedTargetId, None)
        if not target:
            self.setSelectedTargetId(0)
        if not target or target.spaceNo != self.spaceNo \
                or sMath.distance2D(target.position, self.position) > CONST.datas['autoFightRange']['value'] \
                or not utils.checkTargetType(targetType, self, target) \
                or not utils.checkCombatRangeY(self, target):

            entityIds = self.getTargetIdsByTargetType(targetType)
            random.shuffle(entityIds)
            for eId in entityIds:
                entity = KBEngine.entities.get(eId)
                if entity and entity.IsCombatUnit and utils.checkCachedTargetType(targetType, self, entity) \
                        and sMath.inRectRange2D(skillRange, entity.position, self.position)\
                        and utils.checkCombatRangeY(self, entity):
                    return target
        return target

    def _getCombatSkill(self):
        skillList = []
        skillWeightList = []
        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        treatmentSkillLimit = CONST.datas['treatmentSkillLimit'].get('value')
        isHpLow = hpPercent < treatmentSkillLimit
        for skillId, skill in self.getSkillDic().items():
            ret = self.getSkillDic().checkSkillSwitch(skillId, gameconst.SkillSwitchStatus.AUTO)
            if not ret:
                continue
            if not skill.hasTag(gameconst.SkillTag.AutoCombat):
                continue
            if skill.inCDTime():
                continue
            if self.mp < skill.getCostMp(self, skill.skillId, self.mpCostRatio):
                continue
            if skill.hasTag(gameconst.SkillTag.FightStateSkill) and not self.hasState(gameconst.State.Fighting):
                continue
            if utils.hasSkillTag(skillId, gameconst.SkillTag.lzSpecialSkill) and not skill.checkCanUse():
                continue
            if utils.hasSkillTag(skillId, gameconst.SkillTag.GeneralSkill) and not self.checkConflictState(CCD.datas.useGeneralSkill, False):
                continue
            if utils.hasSkillTag(skillId, gameconst.SkillTag.UltraSkill) and not self.isUltraSkillPowerMax():
                # 大招进度没满
                continue
            if utils.hasSkillTag(skillId, gameconst.SkillTag.HealSkill) and not isHpLow:
                continue
            skillList.append(skill)
            weight = SSD.datas[skillId].get('autoBattleWeight')
            skillWeightList.append(weight)

        return utils.weightChoice(skillList, skillWeightList)[0][0] if skillList else None

    def moveToCombatTarget(self, target, skill):
        if not skill:
            return
        if self.autoCombat != gameconst.AutoCombatState.Fighting:
            return

        dstPos, dis = self._getGoodPos(target, skill)
        if not dstPos:
            return

        if not self.checkConflictState(CCD.datas.move):
            return

        direction = sMath.vector3WithoutY(dstPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)

        self.autoCombatInfo['moveController'] = self.scriptNavigate(dstPos, self.speed, dis)
        if self.autoCombatInfo['moveController']:
            # self.controlledBy = None
            self.setState(gameconst.State.Moving)
            self.autoCombatInfo['moveToTargetFailTimes'] = 0
        else:
            moveToTargetFailTimes = self.autoCombatInfo.get('moveToTargetFailTimes', 0)
            if moveToTargetFailTimes >= CONST.datas['autoFightFailRetryNum']['value']:
                self.showMsg(CONST.datas['autoFightFailMsg']['value'], [])
                self.stopAutoCombat(self.id)
            else:
                self.autoCombatInfo['moveToTargetFailTimes'] = moveToTargetFailTimes + 1

    def moveToCombatTargetCB(self, isSucceed):
        DEBUG_MSG('moveToCombatTargetCB  isSucceed', isSucceed)
        self.setMoveController(0)
        if isSucceed:
            self.doAutoCombat(DoAutoCombatReason.MOVE_OVER)

    def checkSetSelectedTargetId(self, skill):
        DEBUG_MSG("checkSetSelectedTargetId ", skill)
        if skill.getTarget(skill.skillId) == 'None' and skill.getEffectTarget(skill.skillId) == 'Self':
            return False

        return True

    def useCombatSkill(self):
        skill = self.autoCombatInfo.get('skill', None)
        targetId = self.autoCombatInfo.get('targetId', 0)
        target = KBEngine.entities.get(targetId, None)
        if not skill or not target or target.spaceNo != self.spaceNo:
            return
        if self.autoCombat != gameconst.AutoCombatState.Fighting:
            return

        realSkill, replaceSkill = skill.getRealSkillVal(self)
        isCastSkill = realSkill.hasTag(gameconst.SkillTag.Casting)

        # ignoreReasons = 0
        # if isCastSkill:
        #     ignoreReasons = gameconst.UseSkillCheck.STATE_CONFLICT|gameconst.UseSkillCheck.NEED_CAST
        #
        # ret = skill.checkUseSkill(self, target.id, ignoreReasons=ignoreReasons)
        # if ret != gameconst.UseSkillCheck.CHEKC_OK:
        #     return

        direction = sMath.vector3WithoutY(target.position - self.position)
        if target.id != self.id:
            if direction[0] == direction[1] == direction[2] == 0:
                direction = sMath.getDirFromYaw(self.direction[2])
            else:
                yaw = sMath.getYawFromDirection(direction)
                self.direction = (0.0, 0.0, yaw)

        arr = skill.getSkillArr(self, target, direction)
        if skill.isChangePositionSkill(skill.skillId):
            positionArgs = skill.getSkillDesPosition(self, target, arr)
            arr = arr + positionArgs

        if self.checkSetSelectedTargetId(skill):
            self.setSelectedTargetId(target.id)

        realSkillVal, _ = skill.getRealSkillVal(self)
        skillTime = skill.getSkillTime(realSkillVal.skillId)
        self.autoCombatInfo['skillCD'] = skillTime*1000 + utils.getTimestamp64()

        if isCastSkill:
            self.castingSkillInternal(skill.skillId, target.id, arr,False)
        else:
            self.doUseTargetSkill(skill.skillId, target.id, arr, 0,False)

        self.autoCombatInfo['skill'] = None
        self.autoCombatInfo['targetId'] = 0

        self.autoCombatInfo['lastSkill'] = skill

        return True

    def isInSkillScope(self, target, skill):
        if not skill:
            return False

        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getConfigData().get('attackDistanceCompensation', 0)
        skillRange = skill.getRange(self, skill.skillId) + targetRadius
        if skillRange and sMath.distance2DToCompareFrom3DPosition(self.position, target.position) > math.pow(skillRange, 2):
            return False
        return True

    def _getGoodPos(self, target, skill):
        if not skill:
            return None
        dstPos = None
        skillRange = skill.getRange(self, skill.skillId)
        mDis = max(0.2, int(skillRange * 0.9))
        return target.position, mDis

    #--------------------------------------------bot------------------------

    def isMoving(self):
        return self.hasState(gameconst.State.Moving)

    def removeMoveController(self):
        if self.autoCombatInfo.get('moveController', None):
            self.cancelController(self.autoCombatInfo['moveController'])
            self.setMoveController(0)

        aiController = self.getTempMiscProp(gameconst.AvatarProps.aiController, None)
        if aiController:
            aiController.onOwnerMoveCancelled()

    def removeHate(self, targetId):
        aiController = self.getTempMiscProp(gameconst.AvatarProps.aiController, None)
        if aiController:
            aiController.hateDict.removeHate(targetId)

    def cancelMoveController(self):
        self._cancelAutoCombatMoveController()
        aiController = self.getTempMiscProp(gameconst.AvatarProps.aiController, None)
        if aiController:
            aiController.onOwnerMoveCancelled()

    def setMoveController(self, contoller):
        self.autoCombatInfo['moveController'] = contoller
        if self.autoCombatInfo['moveController']:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.State.Moving)):
                self.setState(gameconst.State.Moving)
            else:
                self.autoCombatInfo['moveController'] = 0
        else:
            self.removeState(gameconst.State.Moving)

    def navigateToPosition(self, pos, userData=None):
        if self.isMoving():
            return
        navController = self.scriptNavigate(pos, self.speed, userData=userData)
        self.setMoveController(navController)
        if not self.autoCombatInfo['moveController']:
            WARNING_MSG('navigate fail', self.spaceNo, self.position, pos)
            return False
        return True

    def actDefVar(self, name, val):
        self.autoCombatInfo['aiVars'][name] = val

    def actGetVar(self, name, defaultVal=None):
        return self.autoCombatInfo['aiVars'].get(name, defaultVal)

    def actDelVar(self, varName):
        self.autoCombatInfo['aiVars'].pop(varName, None)

    def _addBotTrap(self):
        # radii = self.getAlertDistance()
        self.autoCombatInfo['hateTrapId'] = self.addProximity(8, 8, gameconst.HATE_TRAP)

    def tickAI(self):
        aiController = self.getTempMiscProp(gameconst.AvatarProps.aiController, None)
        if aiController:
            aiController.tickOnce()

    def getRandomSkill(self):
        skill = self._getCombatSkill()
        if skill:
            return skill.getSkillId()
        return 0

    def checkAverageLoad(self):
        load = KBEngine.getAverageLoad()
        if load > 0.6:
            if self.autoCombatInfo.get('timer', 0) and self.autoCombatInterval == CONST.datas['autoFightTick']['value']:
                self.pyDelTimer(self.autoCombatInfo['timer'], gametimer.AUTO_COMBAT_CHECK)
                self.autoCombatInterval = CONST.datas['autoFightTick']['value'] * 2
                self.autoCombatInfo['timer'] = self.pyAddTimer(1, self.autoCombatInterval, gametimer.AUTO_COMBAT_CHECK)
        elif load < 0.4:
            if self.autoCombatInfo.get('timer', 0) and self.autoCombatInterval != CONST.datas['autoFightTick']['value']:
                self.pyDelTimer(self.autoCombatInfo['timer'], gametimer.AUTO_COMBAT_CHECK)
                self.autoCombatInterval = CONST.datas['autoFightTick']['value']
                self.autoCombatInfo['timer'] = self.pyAddTimer(1, self.autoCombatInterval, gametimer.AUTO_COMBAT_CHECK)

    @utils.isMyself
    def setAutoCombatReliveReturnTimes(self, exposed, times):
        self.autoCombatReliveReturnTimes = times
