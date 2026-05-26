import random

from KBEDebug import *
import KBEngine

import formula
import gameconst
import gameconfig
import utils
import gamedecorator
import gametimer
import Math
import sMath
import dataUtils
import math
import actionContext

import message_Message_def as MMD
import conflict_conflict_def as C_C_DD
import gamePlay_gamePlay as DDID
import const_const as CONST
import teamMatch_matchConfig as TMMCD
import skill_skill as SSD
import conflict_status as C_SD

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
    RECOVER = 5


class ImpAutoCombat(object):
    def __init__(self):
        self.autoCombat = gameconst.AutoCombatState.Idle
        self.autoCombatSuspendReason = gameconst.SuspendAutoCombatReason.Default
        self.autoCombatInfo['aiVariables'] = {}
        self.autoCombatInfo['moveController'] = 0
        self.autoCombatInfo['targetEnemyId'] = 0
        self.controlledByReasonDic = {}
        # self.pyAddTimer(1, 5, gametimer.AVATAR_CHECK_AVERAGE_LOAD_TIMER)

    def sendAutoCombat(self):
        LOG_DBG("sendAutoCombat")
        if self.autoCombat and self.autoCombatInfo.get('timer', 0):
            self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

        # 登录下发
        self.sendAutoCombatRange()

    @gamedecorator.checkGameconfigEnable('autoCombat')
    @gamedecorator.crossServer
    @utils.isMyself
    def startAutoCombat(self, exposed, isSuspend):
        LOG_DBG('startAutoCombat', exposed, isSuspend)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        if isSuspend:
            self._startAutoCombat(isSuspend, gameconst.SuspendAutoCombatReason.ClientBreak)
        else:
            self._startAutoCombat()

    def _startAutoCombat(self, isSuspend=False, suspendReason=gameconst.SuspendAutoCombatReason.Default, isFightBack=False):
        LOG_DBG("_startAutoCombat ", isSuspend, suspendReason)
        if not self.checkConflictState(C_C_DD.datas.autoFighting, True):
            return

        if self.isDie():
            LOG_INFO('startAutoCombat: avatar died')
            return

        if formula.checkSpaceForbidAutoFight(self.spaceNo):
            return

        self.autoCombatInfo['moveController'] = 0
        self.autoCombatInfo['notTarget'] = False

        if self.doubleBarFlag and not isSuspend:
            LOG_INFO('startAutoCombat: Suspend by doubleBarFlag')
            isSuspend = True
            suspendReason = gameconst.SuspendAutoCombatReason.DoubleBar

        if isSuspend:
            self.autoCombatSuspendReason = suspendReason
            self.autoCombatInfo['suspendTime'] = utils.getTimestamp64()
            self.autoCombat = gameconst.AutoCombatState.Suspending
        else:
            self.autoCombatInfo['suspendTime'] = 0
            self.autoCombat = gameconst.AutoCombatState.Fighting
            self.setControlleByReason(gameconst.ControlledByReason.AutoCombat)

        self.client.onStartAutoCombat()
        self.setState(gameconst.StateEnum.autoFight)
        if isFightBack:
            self._updateCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK, True)

        if not self.autoCombatInfo.get('timer', 0):
            self.autoCombatInterval = CONST.datas['autoFightTick']['value']
            self.autoCombatInfo['timer'] = self.pyAddTimer(0, CONST.datas['autoFightTick']['value'], gametimer.AUTO_COMBAT_CHECK)

        self.combatReturnInfo.spaceNo = self.spaceNo
        self.combatReturnInfo.pos = tuple(self.position)

    @gamedecorator.crossServer
    @utils.isMyself
    def stopAutoCombat(self, exposed):
        LOG_DBG('stopAutoCombat', exposed)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        self.autoCombatInfo.pop('priorityTargetEnemyId', None)
        self.removeState(gameconst.StateEnum.autoFight)

    def doFollowCaptainStopAutoCombat(self):
        dstPos = self.getCaptainPosition()
        if dstPos and sMath.distance2D(self.position, dstPos) > gameconst.DEFAULT_AOI:
            self.removeState(gameconst.StateEnum.autoFight)

    def selfStopAutoCombat(self, reason=''):
        LOG_DBG("selfStopAutoCombat::", reason)
        if self.hasState(gameconst.StateEnum.autoFight):
            self.removeState(gameconst.StateEnum.autoFight)

    def _stopAutoCombat(self):
        LOG_INFO("_stopAutoCombat  ")
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

        self.client and self.client.onStopAutoCombat()

    def setControlleByReason(self, reason):
        reason = str(reason)
        LOG_DBG("setControlleByReason begin", self.controlledBy, self.controlledByReasonDic, reason)
        self.setControlledBy(True)
        self.controlledByReasonDic[reason] = utils.curTS()
        LOG_DBG("setControlleByReason end ", self.controlledBy, self.controlledByReasonDic, reason)

    def releaseControlleBy(self, reason):
        LOG_DBG("releaseControlleBy begin ", self.controlledBy, self.controlledByReasonDic, reason)
        reason = str(reason)
        if reason in self.controlledByReasonDic:
            self.controlledByReasonDic.pop(reason)

        if len(self.controlledByReasonDic) == 0:
            self.setControlledBy(False)
        LOG_DBG("releaseControlleBy end ", self.controlledBy, self.controlledByReasonDic, reason)

    def setControlledBy(self, isServerControl):
        LOG_DBG("setControlledBy ", isServerControl, self.hasState(gameconst.StateEnum.serverControl), self.controlledBy)
        if isServerControl:
            if not self.hasState(gameconst.StateEnum.serverControl):
                self.setState(gameconst.StateEnum.serverControl)
        else:
            if self.hasState(gameconst.StateEnum.serverControl):
                self.removeState(gameconst.StateEnum.serverControl)
        self.checkIdleStatus()
        # if self.setControlledByTimer:
        #     self.cancelTimerCB(self.setControlledByTimer, gametimer.TIMER_TAG_SET_CONTROLLED_BY)
        #     self.setControlledByTimer = 0
        #
        # self.setControlledByTimer = self.addTimerCB(0.1, '_setControlledBy', (isServerControl, ),
        #                                            gametimer.TIMER_TAG_SET_CONTROLLED_BY, 'setControlledByTimer')

    @gamedecorator.crossServer
    @utils.isMyself
    def breakFollowAndAutoCombat(self, exposed):
        LOG_DBG('breakFollowAndAutoCombat')
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())

        if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
            self.stopAutoCombat(self.id)
            return

        self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.ClientBreak)

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def selectAutoCombatPriorityTarget(self, exposed, targetIds):
        LOG_DBG('selectAutoCombatPriorityTarget', targetIds)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())
        # 优先攻击目标，这里的攻击目标id是怪物的模版id（monsterId）
        self.autoCombatInfo['priorityTargetEnemyId'] = targetIds


    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def selectAutoCombatTarget(self, exposed, targetId):
        LOG_DBG('selectAutoCombatTarget', targetId)
        self.setTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, utils.curTS())

        target = KBEngine.entities.get(targetId, None)
        if not target:
            return
        if exposed == targetId or sMath.distance2D(self.position, target.position) >= self.getViewRadius():
            return
        if target.IsCombatUnit and utils.checkTargetTypeValid('Enemy', self, target):
            self.doSetSelectedTargetId(targetId)
            self.autoCombatInfo['targetId'] = targetId
            self.autoCombatInfo['targetEnemyId'] = targetId
            self.removeMoveController()
            self.doAutoCombat(DoAutoCombatReason.CHANGE_TARGET)

    def suspendAutoCombat(self, suspendReason):
        LOG_DBG('suspendAutoCombat', self.autoCombat, self.autoCombatSuspendReason, suspendReason)
        if not self.autoCombat:
            return

        self.autoCombatSuspendReason = suspendReason
        self.autoCombatInfo['suspendTime'] = utils.getTimestamp64()
        if self.autoCombat == gameconst.AutoCombatState.Suspending:
            return

        self.autoCombat = gameconst.AutoCombatState.Suspending
        self._cancelAutoCombatMoveController()
        self.releaseControlleBy(gameconst.ControlledByReason.AutoCombat)

    def recoverAndTickOnce(self):
        LOG_DBG('recoverAndTickOnce', self.autoCombatSuspendReason)
        if not self.checkConflictState(C_C_DD.datas.serverControling):
            LOG_DBG('recoverAndTickOnce: conflict state')
            return
        # 【【自动战斗】开启自动战斗后，按住任意WASD，法师释放移形换影，位移失效】https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001009320
        if self.hasState(gameconst.StateEnum.Dodging) or self.hasState(gameconst.StateEnum.UsingSkill):
            LOG_DBG('recoverAndTickOnce: dodging state conflict')
            return

        self.recoverAutoCombat(self.spaceNo, self.autoCombatSuspendReason)
        self.doAutoCombat(DoAutoCombatReason.CHANGE_TARGET)

    def recoverAutoCombat(self, oldSpaceNo, suspendReason):
        LOG_DBG('recoverAutoCombat ', self.autoCombat, oldSpaceNo, suspendReason, self.autoCombatSuspendReason )
        if self.autoCombatSuspendReason != suspendReason:
            return
        if self.autoCombat != gameconst.AutoCombatState.Suspending:
            return
        if self.hasState(gameconst.StateEnum.Dodging) or self.hasState(gameconst.StateEnum.UsingSkill):
            LOG_DBG('recoverAutoCombat: dodging state conflict')
            return

        mapId = formula.fetchMapId(self.spaceNo)
        sceneInfo = DDID.datas.get(mapId, None)
        if sceneInfo and not sceneInfo['ifAutoFight']:
            self.stopAutoCombat(self.id)
            return

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
                and not self.hasState(gameconst.StateEnum.Casting) and not self.hasState(gameconst.StateEnum.Channeling) \
                and not self.hasState(gameconst.StateEnum.moveChannel) \
                and not self.hasState(gameconst.StateEnum.Fall) \
                and not self.hasState(gameconst.StateEnum.Moving):
            return True
        return False

    def checkFollowRecover(self):
        return True

    def autoCombatTick(self):
        if self.autoCombat == gameconst.AutoCombatState.Suspending:
            if self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReason.ClientBreak:
                if not self.checkClientBreakRecover():
                    return
                self.recoverAutoCombat(self.spaceNo, self.autoCombatSuspendReason)

            elif self.autoCombatSuspendReason == gameconst.SuspendAutoCombatReason.DoubleBar:
                if utils.getTimestamp64() - self.lastDoubleBarTime > 2000:
                    LOG_WARN('recoverAutoCombat: doubleBarFlag timeout')
                    self.setDoubleBarFlag(self.id, False)
        elif self.autoCombat == gameconst.AutoCombatState.Fighting:
            self.doAutoCombat(DoAutoCombatReason.TICK)

    def doAutoCombatCheckUseSkill(self, skillId):
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

        self.addTimerCB(cdTime, 'skillFinishDoAutoCombat', (), gametimer.TIMER_TAG_DO_AUTO_COMBAT)
        self.autoCombatInfo['waitAfterUseSkill'] = True

    def skillFinishDoAutoCombat(self):
        if self.autoCombat != gameconst.AutoCombatState.Fighting:
            self.autoCombatInfo['waitAfterUseSkill'] = False
            return
        self.doAutoCombat(DoAutoCombatReason.USE_SKILL)

    def _returnIdle(self):
        if not self.getCommonFlagCell(gameconst.AvatarFlagCell.RETURN_IDLE):
            return False
        
        if DDID.datas.get(formula.fetchMapId(self.spaceNo), {}).get('closeAutoRangel', None):
            return False

        if self.combatReturnInfo.spaceNo != self.spaceNo:
            return False

        if sMath.distance2D(self.position, self.combatReturnInfo.pos) < 1:
            return False

        if self.isDie():
            return False

        eventId = C_SD.datas[gameconst.StateEnum.Moving].get('event')
        conflictRes = self.checkConflictState(eventId)
        if eventId and not conflictRes:
            return False

        dstPos = self.combatReturnInfo.pos
        direction = sMath.vector3WithoutY(dstPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)

        self.autoCombatInfo['moveController'] = self.scriptNavigate(dstPos, self.speed)
        if self.autoCombatInfo['moveController']:
            # self.controlledBy = None
            self.setState(gameconst.StateEnum.Moving)
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

        if self.hasState(gameconst.StateEnum.Teleporting) or self.hasState(gameconst.StateEnum.clientPick):
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
                _ents = self.spaceMgr.listEntitiesByTag('largeEnt')
                for e in _ents:
                    if e.IsCombatUnit:
                        utils.isEnemy(self, e)
                        utils.isFriend(self, e)

            self.useTargetTypeCacheFlag = True
            self.stopCacheTargetTypeTimerId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                        gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG, 'stopCacheTargetTypeTimerId')
            if not self.checkTargetTypeTimerId:
                self.checkTargetTypeTimerId = self.pyAddTimer(5, 5, gametimer.CHECK_TARGET_TYPE_TIMER)
        else:
            if self.stopCacheTargetTypeTimerId:
                self.cancelTimerCB(self.stopCacheTargetTypeTimerId, gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG)
                self.stopCacheTargetTypeTimerId = self.addTimerCB(30, 'resetTargetTypeCacheFlag', (),
                                                                gametimer.TIMER_TAG_SET_TARGET_TYPE_CACHE_FLAG, 'stopCacheTargetTypeTimerId')

        if len(self.enemiesCacheSet) <= 0:
            self._returnIdle()
            return

        fightRet = self.normalFight()
        # LOG_DBG("doAutoCombat  fightRet", fightRet)
        if fightRet == AutoCombatRet.FAIL_TARGET:
            if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
                self.stopAutoCombat(self.id)
                return

            self._returnIdle()

    def changePKModeResetTargetId(self):
        LOG_DBG("changePKModeResetTargetId")
        targetId = self.autoCombatInfo.get('targetId', 0)
        target = KBEngine.entities.get(targetId, None)
        if target and target.IsCombatUnit and utils.checkTargetTypeValid('Enemy', self, target):
            return
        self.autoCombatInfo['targetId'] = 0
        self._cancelAutoCombatMoveController()

    def normalFight(self):
        if not self.checkConflictState(C_C_DD.datas.useSkill, False):
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
            if not utils.hasSkillTagById(skill.skillId, gameconst.SkillTag.GeneralSkill):
                skillFrequentNormal = CONST.datas['skillFrequentNormal']['value']
                k = random.randint(int(skillFrequentNormal[0] * 1000), int(skillFrequentNormal[1] * 1000))
                self.autoCombatInfo['ungeneralSkillLimitTime'] = utils.getTimestamp64() + k
            target = self._getCombatTarget(skill)
            if not target:
                self.autoCombatInfo['notTarget'] = True
                return AutoCombatRet.FAIL_TARGET
            self.autoCombatInfo['notTarget'] = False
            self.autoCombatInfo['targetId'] = target.id

        ignoreReasons = gameconst.UseSkillCheck.USC_ENUM_NEED_CAST | gameconst.UseSkillCheck.USC_ENUM_OUT_OF_RANGE
        ret = skill.checkUseSkill(self, target.id, ignoreReasons)
        if ret == gameconst.UseSkillCheck.USC_ENUM_CHEKC_OK:
            if self.isInSkillScope(target, skill):
                self._cancelAutoCombatMoveController()
                if not self.useCombatSkill():
                    self.autoCombatInfo['skill'] = None
                    self.autoCombatInfo['targetId'] = 0
                    return AutoCombatRet.FAIL_USE_SKILL
            else:
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
        if captainSpaceNo and formula.inWorldLineScene(captainSpaceNo) and captainSpaceNo != self.spaceNo:
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
        skillRange = skill.getRange(self, skill.skillId, skill.skillLv)
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

    def _getAutoFightRange(self, target):
        range = CONST.datas['autoFightRange']['value']
        if not target or not target.IsAICombatUnit:
            return range
        return range + target.getCreepData().get('attackDistanceCompensation', 0)

    def getNoneTypeTarget(self, skill):
        if skill.getEffectTargetType(skill.skillId) == 'Self':
            return self

        if skill.hasSkillTag(gameconst.SkillTag.Hot) or skill.hasSkillTag(gameconst.SkillTag.Heal):
            target = self.getTeamTarget(True, skill)
        else:
            target = KBEngine.entities.get(self.selectedTargetId, None)
            if not target:
                self.doSetSelectedTargetId(0)
            if not target or not target.IsCombatUnit or target.isDie() or target.spaceNo != self.spaceNo \
                    or sMath.distance2D(target.position, self.position) > self._getAutoFightRange(target) \
                    or not utils.checkTargetTypeValid('Enemy', self, target) \
                    or not self.checkCombatRangeY(target):
                target = self.getEffectSelectTarget(skill)
        return target

    def getEffectSelectTarget(self, skill):
        if skill.getEffectTargetType(skill.skillId) in ('Friend', 'Self', 'Any', 'FriendExGB'):
            if skill.hasSkillTag(gameconst.SkillTag.Hot) or skill.hasSkillTag(gameconst.SkillTag.Heal):
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
        for teamMemberVal in self.teamInfo.teamPlayerDict.values():
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
            if sMath.distance2D(mEnt.position, self.position) > self._getAutoFightRange(mEnt):
                continue
            if not self.checkCombatRangeY(mEnt):
                continue
            hpPercent = mEnt.hp / mEnt.fullHp
            if minHpPercent != -1 and hpPercent > minHpPercent:
                continue
            minHpPercent = hpPercent
            target = mEnt
        return target

    def getTeamTargets(self):
        _targets = []
        for playerGBID, playerBaseVal in self.teamInfo.teamPlayerDict.items():
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

    def _checkFightBack(self, srcEntId, isGather):
        if not gameconfig.visibleConfigEnabled('autoCombat'):
            return

        if not self.getCommonFlagCell(gameconst.AvatarFlagCell.AUTO_FIGHT_BACK):
            return

        _ent = KBEngine.entities.get(srcEntId)
        if not _ent:
            return

        _ent = utils.getHostEntity(_ent)
        if _ent.id == self.id:
            return

        if self.hasState(gameconst.StateEnum.autoFight):
            targetId = self.autoCombatInfo.get('targetId', 0)
            target = KBEngine.entities.get(targetId, None)
            if not target or not target.IsAvatar:
                if _ent.IsAvatar:
                    self.doSetSelectedTargetId(srcEntId)
            return

        if self.fightBackTimerId:
            return

        if not self._isUIVisibleStrCell('AutoCombat'):
            return

        if self.hasState(gameconst.StateEnum.Moving):
            return

        if not _ent.canAttackable(self):
            return

        if self.duelAttr.isDuelEnemy(_ent):
            return

        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        lowHPAutoCounter = CONST.datas['lowHPAutoCounter']['value']
        mapId = formula.fetchMapId(self.spaceNo)
        if not isGather and mapId not in CONST.datas['triggerAutoCounter']['value'] and hpPercent > lowHPAutoCounter / 100.0:
            return

        self.fightBackTarget = _ent.id
        self.doSetSelectedTargetId(_ent.id)

        self.fightBackTimerId = self.addTimerCB(
            gameconst.FIGHT_BACK_DELAY,
            '_startFightBack',
            (),
            gametimer.TIMER_TAG_FIGHT_BACK,
            'fightBackTimerId')

    def _startFightBack(self):
        _ts = self.getTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, 0)
        _now = utils.curTS()
        if _now - _ts < gameconst.FIGHT_BACK_DELAY:
            return

        if self.hasState(gameconst.StateEnum.Moving):
            return

        self._startAutoCombat(isFightBack=True)

    def _checkExitFightBack(self):
        if self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK):
            _ts = self.getTempMiscProp(gameconst.EntityPropsEnum.AvatarActiveTimestamp, 0)
            _now = utils.curTS()
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
                self.doSetSelectedTargetId(0)

        # 攻击PVP玩家(这个先不做了，太耗了)
        # 攻击仇恨目标
        _hateRecord = self.getTempMiscProp(gameconst.EntityPropsEnum.hateRecord, {})

        closeAutoRangel = DDID.datas.get(formula.fetchMapId(self.spaceNo), {}).get('closeAutoRangel', None)

        if not target or target.spaceNo != self.spaceNo or not target.IsCombatUnit\
                or sMath.distance2D(target.position, self.position) > self._getAutoFightRange(target) \
                or not utils.checkTargetTypeValid('Enemy', self, target)\
                or not self.checkCombatRangeY(target):
            # 调整后：下面是顺序
            #反击
            #正在打得目标
            #玩家锁定目标
            #仇恨目标
            #任务目标(priorityTargetEnemyId)
            #同伴选择
            #就近
            targetsList = []
            entityIdList = self.getTargetIdsByTargetType('Enemy')
            priorityTargetEnemyIds = self.autoCombatInfo.get('priorityTargetEnemyId', None)
            _teamTargetIds = self.getTeamTargets()
            _maxVal = None
            target = None
            for eId in entityIdList:
                entity = KBEngine.entities.get(eId)
                if not entity:
                    continue
                if entity.id == self.id:
                    continue
                if not self.checkCombatRangeY(entity):
                    continue
                if _inFightBack and eId not in _hateRecord:
                    # 反击过程中，不攻击非仇恨目标
                    continue
                if entity.IsCombatUnit and utils.checkCachedTargetType('Enemy', self, entity):
                    targetsList.append(entity)
                    _val = (
                        # 1.仇恨目标
                        1 if eId in _hateRecord else 0,
                        # 2.任务目标
                        1 if entity.IsMonster and priorityTargetEnemyIds and entity.monsterId in priorityTargetEnemyIds else 0,
                        # 3.队伍目标
                        1 if eId in _teamTargetIds else 0,
                        # 4.距离
                        -sMath.distance2DToCompareFrom3DPosition(self.position, entity.position)
                    )
                    if not closeAutoRangel and _val < (0, 0, 0, 1.0) and self.combatReturnInfo.switch and sMath.distance2D(entity.position, self.combatReturnInfo.pos) > self.combatReturnInfo.range:
                        continue

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
            self.doSetSelectedTargetId(0)
        if not target or target.spaceNo != self.spaceNo \
                or sMath.distance2D(target.position, self.position) > self._getAutoFightRange(target) \
                or not utils.checkTargetTypeValid(targetType, self, target) \
                or not self.checkCombatRangeY(target):

            entityIdList = list(self.getTargetIdsByTargetType(targetType))
            random.shuffle(entityIdList)
            for eId in entityIdList:
                entity = KBEngine.entities.get(eId)
                if entity and entity.IsCombatUnit and utils.checkCachedTargetType(targetType, self, entity) \
                        and sMath.inRectRange2D(skillRange, entity.position, self.position)\
                        and self.checkCombatRangeY(entity):
                    return target
        return target
    
    def setAutoCombatSkillFrequent(self, exposed, isSet):
        self.autoCombatSkillFrequent = isSet

    def _getCombatSkill(self):
        skillList = []
        skillWeightList = []
        hpPercent = self.hp / self.fullHp if self.fullHp else 1
        treatmentSkillLimit = CONST.datas['treatmentSkillLimit'].get('value')
        isHpLow = hpPercent < treatmentSkillLimit
        _load = KBEngine.getAverageLoad()
        if _load > 0.8:
            _useCreationSkill = False

        elif _load > 0.5:
            _useCreationSkill = random.random() < 0.5

        else:
            _useCreationSkill = True

        inAutoFightSkillCD = utils.getTimestamp64() < self.autoCombatInfo.get('ungeneralSkillLimitTime', 0)
        for skillId, skill in self.skillDic.items():
            ret = self.skillDic.checkSkillSwitch(skillId, gameconst.SkillSwitchStatus.AUTO)
            if not ret:
                continue
            if not skill.hasSkillTag(gameconst.SkillTag.AutoCombat):
                continue
            if skill.inCDTime():
                continue
            if self.mp < skill.getCostMp(self, skill.skillId, self.mpCostRatio):
                continue
            if skill.hasSkillTag(gameconst.SkillTag.FightStateSkill) and not self.hasState(gameconst.StateEnum.Fighting):
                continue
            if utils.hasSkillTagById(skillId, gameconst.SkillTag.GeneralSkill) and not self.checkConflictState(C_C_DD.datas.useGeneralSkill, False):
                continue
            if utils.hasSkillTagById(skillId, gameconst.SkillTag.UltraSkill) and not self.isUltraSkillPowerMax():
                # 大招进度没满
                continue
            if utils.hasSkillTagById(skillId, gameconst.SkillTag.HealSkill) and not isHpLow:
                continue
            # 改变技能CD状态
            if utils.hasSkillTagById(skillId, gameconst.SkillTag.changeCDStatusSkill):
                # 不能用
                if skill.getTempData(gameconst.SkillTempDataKey.CHANGE_SKILL_CD_STATUS, gameconst.SkillCDStatus.DEFAULT) == gameconst.SkillCDStatus.DISABLED:
                    continue

            if not _useCreationSkill and skillId in SSD.hasCreationSkill:
                # 如果负载过高， 不使用创生物技能技能
                continue

            # 自动战斗技能公共CD中，只能用普攻
            if not self.autoCombatSkillFrequent:
                if inAutoFightSkillCD and not utils.hasSkillTagById(skillId, gameconst.SkillTag.GeneralSkill):
                    continue

            skillList.append(skill)
            weight = SSD.datas[skillId].get('autoBattleWeight')
            skillWeightList.append(weight)

        return utils.weightChoices(skillList, skillWeightList)[0][0] if skillList else None

    def moveToCombatTarget(self, target, skill):
        if not skill:
            return
        if self.autoCombat != gameconst.AutoCombatState.Fighting:
            return

        dstPos, distance = self._getGoodPos(target, skill)
        if not dstPos:
            return

        if not self.checkConflictState(C_C_DD.datas.move):
            return

        direction = sMath.vector3WithoutY(dstPos - self.position)
        yaw = sMath.getYawFromDirection(direction)
        self.direction = (0.0, 0.0, yaw)

        self.autoCombatInfo['moveController'] = self.scriptNavigate(dstPos, self.speed, distance)
        if self.autoCombatInfo['moveController']:
            # self.controlledBy = None
            self.setState(gameconst.StateEnum.Moving)
            self.autoCombatInfo['moveToTargetFailTimes'] = 0
        else:
            moveToTargetFailTimes = self.autoCombatInfo.get('moveToTargetFailTimes', 0)
            if moveToTargetFailTimes >= CONST.datas['autoFightFailRetryNum']['value']:
                self.showMsg(CONST.datas['autoFightFailMsg']['value'], [])
                self.stopAutoCombat(self.id)
            else:
                self.autoCombatInfo['moveToTargetFailTimes'] = moveToTargetFailTimes + 1

    def moveToCombatTargetCB(self, isSucceed):
        LOG_DBG('moveToCombatTargetCB  isSucceed', isSucceed)
        self.setMoveController(0)
        if isSucceed:
            self.doAutoCombat(DoAutoCombatReason.MOVE_OVER)

    def checkSetSelectedTargetId(self, skill):
        LOG_DBG("checkSetSelectedTargetId ", skill)
        if skill.getTarget(skill.skillId) == 'None' and skill.getEffectTargetType(skill.skillId) == 'Self':
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
        isCastSkill = realSkill.hasSkillTag(gameconst.SkillTag.Casting)

        direction = sMath.vector3WithoutY(target.position - self.position)
        if target.id != self.id:
            if direction[0] == direction[1] == direction[2] == 0:
                direction = sMath.getDirFromYaw(self.direction[2])
            else:
                yaw = sMath.getYawFromDirection(direction)
                self.direction = (0.0, 0.0, yaw)

        arr = skill.getSkillArr(self, target, direction)
        if skill.isChangePosSkill(skill.skillId):
            positionArgs = skill.getSkillDesPosition(self, target, arr)
            arr = arr + positionArgs

        if self.checkSetSelectedTargetId(skill):
            self.doSetSelectedTargetId(target.id)

        realSkillVal, _ = skill.getRealSkillVal(self)
        skillTime = skill.getSkillTime(realSkillVal.skillId)
        self.autoCombatInfo['skillCD'] = skillTime*1000 + utils.getTimestamp64()

        if not isCastSkill:
            if not self._useTargetSkillPreCheck(skill.skillId, target.id, False):
                return

        actionCtx = actionContext.UseSkillCtx(
            self.id,
            skill.skillId,
            arr,
            target.id,
            isClient=True,
            skillObj=skill,
        )
        self.doUseSkill(skill, actionCtx, 0)

        self.autoCombatInfo['skill'] = None
        self.autoCombatInfo['targetId'] = 0

        self.autoCombatInfo['lastSkill'] = skill

        return True

    def isInSkillScope(self, target, skill):
        if not skill:
            return False

        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)
        skillRange = skill.getRange(self, skill.skillId, skill.skillLv) + targetRadius
        if skillRange and sMath.distance2DToCompareFrom3DPosition(self.position, target.position) > math.pow(skillRange, 2):
            return False
        return True

    def _getGoodPos(self, target, skill):
        if not skill:
            return None
        dstPos = None
        skillRange = skill.getRange(self, skill.skillId, skill.skillLv)

        targetRadius = 0
        if target.IsMonster:
            targetRadius = target.getCreepData().get('attackDistanceCompensation', 0)

        mDis = max(0.2, int(skillRange * 0.9) + targetRadius)
        return target.position, mDis

    #--------------------------------------------bot------------------------

    def isMoving(self):
        return self.hasState(gameconst.StateEnum.Moving)

    def removeMoveController(self):
        self._cancelAutoCombatMoveController()
        aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
        if aiController:
            aiController.onOwnerMoveCancelled()

    def removeHate(self, targetId):
        aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
        if aiController:
            aiController.hateDict.removeHate(targetId)

    def setMoveController(self, contoller):
        self.autoCombatInfo['moveController'] = contoller
        if self.autoCombatInfo['moveController']:
            if self.checkConflictState(dataUtils.getStateEventId(gameconst.StateEnum.Moving)):
                self.setState(gameconst.StateEnum.Moving)
            else:
                self.autoCombatInfo['moveController'] = 0
        else:
            self.removeState(gameconst.StateEnum.Moving)

    def navigateToPosition(self, pos, userData=None):
        if self.isMoving():
            return
        navController = self.scriptNavigate(pos, self.speed, userData=userData)
        self.setMoveController(navController)
        if not self.autoCombatInfo['moveController']:
            LOG_WARN('navigate fail', self.spaceNo, self.position, pos)
            return False
        return True

    def actDefineVar(self, name, val):
        self.autoCombatInfo['aiVariables'][name] = val

    def actGetVar(self, name, defaultVal=None):
        return self.autoCombatInfo['aiVariables'].get(name, defaultVal)

    def actDelVar(self, varName):
        self.autoCombatInfo['aiVariables'].pop(varName, None)

    def _addBotTrap(self):
        # radii = self.getAlertDistance()
        self.autoCombatInfo['hateTrapId'] = self.addProximity(8, 8, gameconst.AGGRO_TRIGGER_TRAP)

    def aiTick(self):
        aiController = self.getTempMiscProp(gameconst.EntityPropsEnum.aiController, None)
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

    @gamedecorator.crossServer
    @utils.isMyself
    def changeAutoCombatRange(self, exposed, switch, range):
        rangeRange = (20, 50)
        if range < rangeRange[0]:
            range = rangeRange[0]
        elif range > rangeRange[1]:
            range = rangeRange[1]

        self.combatReturnInfo.switch = switch
        self.combatReturnInfo.range = range
        self.sendAutoCombatRange()

        self._updateCommonFlagCell(gameconst.AvatarFlagCell.RETURN_IDLE, switch)

    def sendAutoCombatRange(self):
        LOG_DBG('sendAutoCombatRange', self.combatReturnInfo.switch, self.combatReturnInfo.range)
        self.client.onGetAutoCombatRange(self.combatReturnInfo.switch, self.combatReturnInfo.range)

    @utils.isMyself
    def setDoubleBarFlag(self, exposed, flag):
        LOG_INFO("setDoubleBarFlag", flag)
        self.client.onSetDoubleBarFlag(flag)
        if flag != self.doubleBarFlag:
            if flag:
                self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.DoubleBar)
            else:
                self.recoverAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReason.DoubleBar)
        if flag:
            self.lastDoubleBarTime = utils.getTimestamp64()
        self.doubleBarFlag = flag
